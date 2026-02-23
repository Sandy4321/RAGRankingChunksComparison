#!/usr/bin/env python

import asyncio, datetime, math, random, time
from itertools import combinations
from pathlib import Path

import networkx as nx
import pandas as pd
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAIError
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

# ─── FLAGS ─────────────────────────────────────────────────────────
SHOW_RICH_TABLES = True
SHOW_PLAIN_TEXT  = True
SURVIVE_MARK = "Y"
POOR_MARK    = "!"

# ─── PARAMETERS ────────────────────────────────────────────────────
DATAFILE                 = "answers130.csv"      # ← your CSV
MODEL_NAME               = "gpt-4o-mini"
GROUP_SIZE               = 5 #10 #40 #7
PAIR_TIMEOUT             = 2 #7 #3#7.0                   # per-pair watchdog
ROUND_TIMEOUT            = PAIR_TIMEOUT * 2      # whole-round watchdog
MAX_CONCURRENT_PAIRS     = 60 #40                    # 30-50 works for mini key
RETRY_LIMIT              = 1
RETRY_DELAY              = 1.0
SUCCESS_THRESHOLD        = 0.70
PAGERANK_ALPHA           = 0.85
ELBOW_MIN_KEEP           = 2
ELBOW_DROP_PCT           = 10.0
TEMPERATURE              = 0.0
MAX_TOKENS               = 1
TOP_LOGPROBS             = 3
TRUNCATE_LENGTH          = 120
TRUNCATE_SUFFIX          = "…"
APIKEY_ENV               = r"api_keys.env"

# ─── LOAD DATA ─────────────────────────────────────────────────────
load_dotenv(APIKEY_ENV, override=True)
QUESTION = Path("question.txt").read_text(encoding="utf8")
ANSWERS  = (pd.read_csv(DATAFILE, header=None, names=["answer"],
                        on_bad_lines="skip")
              .fillna("")
              .answer.tolist())

# ─── LOG LISTS ─────────────────────────────────────────────────────
comparison_logs  = []
group_scores_rows = []
runtime_rows     = []

# ─── HELPERS ───────────────────────────────────────────────────────
def make_prompt(q, a, b):
    return f"""Pick the better answer **or** declare a draw.

Reply with one letter only:

A – Answer A is clearly better  
B – Answer B is clearly better  
D – Both answers are equally poor / off-topic

QUESTION:
{q}

ANSWER A:
{a}

ANSWER B:
{b}

---
OUTPUT:
A
B
D""".strip()

def parse_response(rsp):
    try:
        tok = rsp.choices[0].logprobs.content[0]
        picked = tok.token.strip().upper()[:1]
        if picked not in "ABD":
            picked = "D"
        best = {"A": -math.inf, "B": -math.inf, "D": -math.inf}
        for alt in tok.top_logprobs:
            k = alt.token.strip().upper()[:1]
            if k in best:
                best[k] = max(best[k], alt.logprob)
        pA, pB, pD = map(math.exp, (best["A"], best["B"], best["D"]))
        total = pA + pB + pD
        if picked in "AB":
            conf = pA / (pA + pB) if picked == "A" else pB / (pA + pB)
        else:
            conf = pD / total
        return picked, conf
    except Exception:
        return "D", 0.0

def elbow_top(scores):
    vals = [s for _, s in scores]
    for k in range(len(vals) - 1):
        if vals[k] > 0 and (vals[k] - vals[k + 1]) / vals[k] * 100 > ELBOW_DROP_PCT:
            return [idx for idx, _ in scores[:max(ELBOW_MIN_KEEP, k + 1)]]
    return [idx for idx, _ in scores]

# ─── ASYNC PAIR COMPARISON (watchdog inside semaphore) ────────────
PAIR_SEM = asyncio.Semaphore(MAX_CONCURRENT_PAIRS)
async def compare_pair(i, j, client, prog, tid, rnd, gid):
    ai, aj = ANSWERS[i], ANSWERS[j]
    fallback, choice, conf, duration = True, "D", 0.0, 0.0
    async with PAIR_SEM:
        for attempt in range(1, RETRY_LIMIT + 1):
            try:
                start = time.perf_counter()
                rsp = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user",
                                   "content": make_prompt(QUESTION, ai, aj)}],
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        logprobs=True,
                        top_logprobs=TOP_LOGPROBS,
                    ),
                    timeout=PAIR_TIMEOUT
                )
                duration = time.perf_counter() - start
                choice, conf = parse_response(rsp)
                fallback = False
                break
            except (asyncio.TimeoutError, OpenAIError, Exception):
                duration = time.perf_counter() - start
                if attempt < RETRY_LIMIT:
                    await asyncio.sleep(RETRY_DELAY)
    prog.update(tid, advance=1)
    comparison_logs.append(dict(
        i=i, j=j, choice=choice, confidence=conf, duration_s=duration,
        fallback=fallback, round_no=rnd, group_no=gid))
    return i, j, fallback, choice

# ─── GROUP RANK (returns 7-tuple) ──────────────────────────────────
async def rank_group(indices, gid, client, prog, rnd, tid):
    pairs_info = [(i, j) for i, j in combinations(indices, 2)]
    tasks = [compare_pair(i, j, client, prog, tid, rnd, gid)
             for i, j in pairs_info]
    pairs = await asyncio.gather(*tasks, return_exceptions=True)

    clean = []
    for (i, j), res in zip(pairs_info, pairs):
        if isinstance(res, Exception):
            comparison_logs.append(dict(
                i=i, j=j, choice="D", confidence=0.0,
                duration_s=PAIR_TIMEOUT, fallback=True,
                round_no=rnd, group_no=gid))
            clean.append((i, j, True, "D"))
        else:
            clean.append(res)

    good_cnt = {idx: 0 for idx in indices}
    for i, j, fb, _ in clean:
        if not fb:
            good_cnt[i] += 1
            good_cnt[j] += 1

    min_good = 2 if len(indices) > 2 else 1
    poorly   = [idx for idx, c in good_cnt.items() if c < min_good]

    successes = sum(1 for *_ , fb, _ in clean if not fb)
    need_good = math.ceil(SUCCESS_THRESHOLD * len(clean))

    if successes >= need_good:
        G = nx.DiGraph()
        for i, j, fb, ch in clean:
            if fb: continue
            if ch == "A": G.add_edge(j, i)
            elif ch == "B": G.add_edge(i, j)
        pr = nx.pagerank(G, alpha=PAGERANK_ALPHA) if G.edges else {}
        scored = sorted([(idx, pr.get(idx, 1 / len(indices)))
                         for idx in indices], key=lambda x: -x[1])
        insufficient = False
    else:
        scored = [(idx, 0.0) for idx in indices]
        insufficient = True

    winners   = set(elbow_top(scored))
    survivors = winners | set(poorly)
    for rnk, (idx, sc) in enumerate(scored, 1):
        group_scores_rows.append(dict(
            round_no=rnd, group_no=gid, rank=rnk, index=idx, score=sc,
            good_pairs=good_cnt[idx], insufficient=insufficient,
            survive=int(idx in survivors), poorly=int(idx in poorly)))
    return scored, poorly, insufficient, survivors, good_cnt, successes, len(clean)

# ─── TOURNAMENT LOOP with round watchdog ──────────────────────────
async def tournament():
    overall_start = time.perf_counter()
    console, client = Console(force_terminal=True), AsyncOpenAI()
    current, rnd = list(range(len(ANSWERS))), 1

    while len(current) > GROUP_SIZE:
        round_start = time.perf_counter()
        random.shuffle(current)
        groups = [current[i:i + GROUP_SIZE]
                  for i in range(0, len(current), GROUP_SIZE)]

        progress = Progress(SpinnerColumn(), TextColumn("{task.description}"),
                            BarColumn(), TextColumn("{task.percentage:>3.0f}%"),
                            console=console, transient=True)
        status = Panel.fit("\n".join(f"G{g+1}: {groups[g]}"
                                    for g in range(len(groups))),
                           title=f"🏆 ROUND {rnd}")

        results = []; surv = {}; poor = {}; good = {}; succ_stat = {}; gtime = {}
        with Live(Group(progress, status), console=console,
                  refresh_per_second=10):
            info = []; tasks = []
            for gid, g in enumerate(groups, 1):
                tid = progress.add_task(f"G{gid}", total=math.comb(len(g), 2))
                info.append((gid, g, tid)); gtime[gid] = time.perf_counter()
                tasks.append(asyncio.create_task(
                    rank_group(g, gid, client, progress, rnd, tid)))

            try:
                outs = await asyncio.wait_for(asyncio.gather(*tasks), ROUND_TIMEOUT)
            except asyncio.TimeoutError:
                console.print(f"[red]⏱ ROUND {rnd} exceeded {ROUND_TIMEOUT}s – "
                              "cancelling stragglers[/]")
                outs = []
                for t in tasks:
                    if not t.done():
                        t.cancel()
                for t in tasks:
                    try:
                        outs.append(await t)
                    except asyncio.CancelledError:
                        pass

            for gid in gtime:
                gtime[gid] = time.perf_counter() - gtime[gid]

        for (gid, g, _), res in zip(info, outs):
            scored, p, insuff, s, gcnt, succ, total = res
            surv[gid], poor[gid], good[gid] = s, p, gcnt
            succ_stat[gid] = (succ, total)
            results.append((gid, scored, insuff))
            runtime_rows.append(dict(
                round_no=rnd, group_no=gid, n_answers=len(g),
                good_pairs=succ, group_time_s=gtime[gid], round_time_s=None))

        # print Rich / plain tables
        console.rule(f" End of ROUND {rnd} — scores & survivors ")
        for gid, scored, insuff in sorted(results, key=lambda x: x[0]):
            succ, total = succ_stat[gid]; t = gtime[gid]
            stat = "OK" if not insuff else f"FAIL (<{int(SUCCESS_THRESHOLD*100)}%)"
            title = f"G{gid} {stat} ({succ}/{total} good)  t={t:.2f}s"
            if SHOW_RICH_TABLES:
                tbl = Table(title=title, header_style="bold")
                for col in ("Rank", "Idx", "Score", "Good", "Surv", "Poor"):
                    tbl.add_column(col, justify="right"
                                   if col in ("Rank", "Idx", "Good") else "center")
                gc = good[gid]
                for r, (idx, sc) in enumerate(scored, 1):
                    surv_mark = SURVIVE_MARK if idx in surv[gid] and idx not in poor[gid] else ""
                    tbl.add_row(str(r), str(idx), f"{sc:.4f}", str(gc[idx]),
                                surv_mark, POOR_MARK if idx in poor[gid] else "")
                console.print(tbl)

            if SHOW_PLAIN_TEXT:
                print(title)
                gc = good[gid]
                for r, (idx, sc) in enumerate(scored, 1):
                    marks = (SURVIVE_MARK if idx in surv[gid] and idx not in poor[gid] else "") + \
                            (POOR_MARK if idx in poor[gid] else "")
                    snippet = ANSWERS[idx].replace("\n", " ")[:TRUNCATE_LENGTH]
                    print(f"  {r:>3}. idx={idx:<4} score={sc:.4f} "
                          f"good={gc[idx]} {marks}  {snippet}")
                print()

        # round timing
        rtime = time.perf_counter() - round_start
        console.rule(f" ROUND-TIME: {rtime:.2f} s ")
        for row in runtime_rows[::-1]:
            if row["round_no"] == rnd and row["round_time_s"] is None:
                row["round_time_s"] = rtime
            if row["round_no"] < rnd:
                break

        current = list(set().union(*surv.values()))
        if len(groups) == 1:
            break
        rnd += 1

    # ── FINAL ROUND (same logic, no watchdog needed) ───────────────
    final_start = time.perf_counter()
    progress = Progress(SpinnerColumn(), TextColumn("FINAL"), BarColumn(),
                        TextColumn("{task.percentage:>3.0f}%"),
                        console=console, transient=True)
    console.print(Panel.fit(f"G0: {current}", title="🏁 FINAL ROUND"))
    with progress:
        tid = progress.add_task("FINAL", total=math.comb(len(current), 2))
        final_scored, *_ = await rank_group(current, 0, client, progress, rnd, tid)
    ftime = time.perf_counter() - final_start
    await client.close()
    runtime_rows.append(dict(round_no=rnd, group_no=0, n_answers=len(current),
                             good_pairs=sum(1 for *_ , fb, _ in final_scored if not fb),
                             group_time_s=ftime, round_time_s=ftime))

    # ── FINAL RANKING TABLES ───────────────────────────────────────
    console.rule(" Final ranking ")
    if SHOW_RICH_TABLES:
        ft = Table(show_header=True, header_style="bold magenta")
        ft.add_column("Rank", justify="right")
        ft.add_column("Idx",  justify="right")
        ft.add_column("Score", justify="right")
        ft.add_column("Answer (truncated)")
        for r, (idx, sc) in enumerate(final_scored, 1):
            trunc = ANSWERS[idx].replace("\n", " ")[:TRUNCATE_LENGTH]
            trunc += TRUNCATE_SUFFIX if len(ANSWERS[idx]) > TRUNCATE_LENGTH else ""
            ft.add_row(str(r), str(idx), f"{sc:.4f}", trunc)
        console.print(ft)
    if SHOW_PLAIN_TEXT:
        for r, (idx, sc) in enumerate(final_scored, 1):
            trunc = ANSWERS[idx].replace("\n", " ")[:TRUNCATE_LENGTH]
            print(f"{r:>3}. idx={idx:<4} score={sc:.4f}  {trunc}")

    # ── SUMMARY TABLE ─────────────────────────────────────────────
    overall = time.perf_counter() - overall_start
    df_rt    = pd.DataFrame(runtime_rows)
    df_pairs = pd.DataFrame(comparison_logs)
    fast10   = df_pairs.loc[df_pairs["fallback"] == False,
                            "duration_s"].quantile(0.10)
    fast10   = fast10 if not math.isnan(fast10) else 0.1
    pairs_df = (df_rt.assign(pairs=lambda d: d.n_answers.apply(
                                lambda n: math.comb(int(n), 2)))
                      .groupby("round_no", as_index=False)
                      .agg(round_time_s=("round_time_s", "max"),
                           total_pairs = ("pairs", "sum"),
                           groups      = ("group_no", "nunique")))
    console.rule("⏱  Run-time summary")
    tbl = Table()
    tbl.add_column("Round", justify="right")
    tbl.add_column("Measured (s)", justify="right")
    tbl.add_column("Lower (s)", justify="right")
    tbl.add_column("Upper (s)", justify="right")
    lower_sum = upper_sum = 0.0
    for _, row in pairs_df.iterrows():
        pairs_round  = int(row.total_pairs)
        groups_round = int(row.groups)
        max_parallel = min(pairs_round, groups_round * MAX_CONCURRENT_PAIRS)
        lower = (pairs_round / max_parallel) * fast10
        upper = math.ceil(pairs_round / MAX_CONCURRENT_PAIRS) * \
                (PAIR_TIMEOUT + RETRY_LIMIT * RETRY_DELAY)
        lower_sum += lower; upper_sum += upper
        tbl.add_row(str(int(row.round_no)),
                    f"{row.round_time_s:.2f}",
                    f"{lower:.2f}", f"{upper:.0f}")
    tbl.add_row("─", "─", "─", "─")
    tbl.add_row("Σ", f"{pairs_df.round_time_s.sum():.2f}",
                f"{lower_sum:.2f}", f"{upper_sum:.0f}")
    tbl.add_row("Overall wall", f"{overall:.2f}", "", "")
    console.print(tbl)

    # ── SAVE CSVs ─────────────────────────────────────────────────--
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    pd.DataFrame(comparison_logs ).to_csv(f"details_{ts}.csv", index=False, float_format="%.6f")
    pd.DataFrame(group_scores_rows).to_csv(f"groupscores_{ts}.csv", index=False, float_format="%.6f")
    pd.DataFrame(runtime_rows    ).to_csv(f"runtime_{ts}.csv", index=False, float_format="%.2f")
    pd.DataFrame([{"overall_time_s": overall}]).to_csv(
        f"overall_{ts}.csv", index=False, float_format="%.2f")
    pd.DataFrame(
        [{"rank": r+1, "index": idx, "score": sc, "answer": ANSWERS[idx]}
         for r, (idx, sc) in enumerate(final_scored)]
    ).to_csv(f"final_{ts}.csv", index=False, float_format="%.6f")
    console.print(f"[green]✅  Saved CSVs with timestamp {ts}[/]")

# ─── RUN ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(tournament())
    except KeyboardInterrupt:
        print("\n[red]Interrupted — partial results may be saved.")
