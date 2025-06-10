

from openai import OpenAI
from itertools import combinations
import  math,  re
from dotenv import load_dotenv, find_dotenv
load_dotenv(r"api_keys.env", override=True)
client = OpenAI()           # reads OPENAI_API_KEY env var
MODEL  = "gpt-4o-mini"      # or "gpt-4o" for higher quality / cost



# ───────────── configuration ─────────────
MODEL = "gpt-4o-mini"          # or "gpt-4o"
K     = 64 #32                     # ELO K-factor
# ─────────────────────────────────────────

client = OpenAI()              # reads OPENAI_API_KEY from env

# ---------- 1. core QA + “near miss” ----------
qa_core = [
    ("What causes rainfall in the water cycle?",
     "Rainfall happens when water vapor condenses into droplets that become heavy enough to fall.",
     "Rainfall occurs when the ground releases stored moisture upward."),

    ("Why must green plants receive sunlight?",
     "Green plants capture sunlight to drive photosynthesis, making the sugars they need to live.",
     "Plants need sunlight mainly to warm their roots during the day."),

    ("What main job does the human heart perform?",
     "The heart continuously pumps blood, delivering oxygen and nutrients to every part of the body.",
     "The heart’s primary task is to filter toxins from the bloodstream."),

    ("How would you define gravity in simple terms?",
     "Gravity is the attractive force that pulls masses toward each other, such as objects toward Earth.",
     "Gravity is the wind that pushes objects down to the ground."),

    ("Why do people have to sleep each day?",
     "Sleep lets the brain and body restore themselves, process information, and maintain healthy function.",
     "Sleep is required so our eyes can recharge their vision batteries."),

    ("Why do tree leaves change color during fall?",
     "As days shorten and chlorophyll fades, other pigments show through, turning leaves red, orange or yellow.",
     "Leaves change color when trees drink more minerals from the soil."),

    ("What function do the lungs carry out?",
     "The lungs exchange gases, bringing oxygen into the blood and removing carbon dioxide from it.",
     "Lungs act as large pumps that circulate blood through the body."),

    ("Give one major benefit of regular exercise.",
     "Regular exercise strengthens muscles, supports cardiovascular health, and lifts mood.",
     "Exercise mainly increases the brightness of skin tone."),

    ("What is the stomach’s role in digestion?",
     "The stomach churns food and mixes it with acid and enzymes to begin breaking it down.",
     "The stomach cools food so that it can safely enter the intestines.")
]

# ---------- 2. quick synonymiser ----------
syn_map = {
    "rainfall": "precipitation", "water": "liquid", "vapor": "steam",
    "plants": "vegetation", "sunlight": "solar light", "photosynthesis": "photo-synthesis",
    "heart": "cardiac organ", "blood": "circulation fluid",
    "gravity": "gravitational pull", "objects": "bodies",
    "sleep": "slumber", "brain": "cerebrum",
    "lungs": "pulmonary organs", "exercise": "physical activity",
    "stomach": "gastric organ", "enzymes": "biocatalysts",
    "chlorophyll": "green pigment", "pigments": "color compounds"
}
def synonymize(txt: str) -> str:
    out = txt
    for k, v in syn_map.items():
        out = re.sub(rf"\b{k}\b", v, out, flags=re.I)
    return out

questions, truth_answers, pools = [], [], []
all_correct = [c for _, c, _ in qa_core]

for q, correct, near in qa_core:
    questions.append(q)
    truth_answers.append(correct)

    pool = all_correct.copy()                 # 9 correct answers
    pool.append(near)                         # + near miss
    pool.extend([synonymize(a) for a in pool])
    pools.append(pool)

# ---------- 3. ELO helpers ----------
def init_elo(items, base=1000):
    return {it: base for it in items}

def update_elo(r1, r2, score, k=K):
    exp1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
    r1 += k * (score - exp1)
    r2 += k * ((1 - score) - (1 - exp1))
    return r1, r2

# ---------- 4. pairwise judge with A/B/D ----------
def judge_pair(question: str, txt_a: str, txt_b: str):
    """
    Returns
        winner  : "A", "B", or None for draw
        conf    : probability in [0.5,1] that winner is better
    """
    tmp = 0
    prompt = f"""
Pick the better answer **or** declare a draw.

Reply with ONE letter ONLY:
A  – Answer A is clearly better
B  – Answer B is clearly better
D  – Both answers are equally poor / off-topic

QUESTION:
{question}

ANSWER A:
{txt_a}

ANSWER B:
{txt_b}
Reply with exactly one of the following, on its own line *only*:

A
B
D
"""
    rsp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        logprobs=True,
        top_logprobs=3
    )

    tok   = rsp.choices[0].logprobs.content[0]
    picked = tok.token.strip().upper()[:1]          # "A" / "B" / "D"

    # dict {token: logprob} for A, B, D – missing ones get large negative
    lp = {t.token.strip().upper(): t.logprob for t in tok.top_logprobs}
    lp.setdefault("A", -100)
    lp.setdefault("B", -100)
    lp.setdefault("D", -100)

    def gap2prob(lw, ll):
        """sigmoid of the log-prob gap"""
        return 1 / (1 + math.exp(-(lw - ll)))

    if picked == "A":
        conf = gap2prob(lp["A"], lp["B"])
        return "A", max(0.5, conf)
    if picked == "B":
        conf = gap2prob(lp["B"], lp["A"])
        return "B", max(0.5, conf)
    # draw
    return None, 0.5

# ---------- 5. run tournaments ----------
overall_correct = 0

for q_idx, q in enumerate(questions):
    pool    = pools[q_idx]
    correct = truth_answers[q_idx]

    ratings = init_elo(pool)
    n_pairs = len( list( combinations(pool, 2) ) )

    for ipair , (a, b) in enumerate( combinations(pool, 2) ):
        winner, conf = judge_pair(q, a, b)
        print('\n pair # ',ipair, '  from ' , n_pairs)
        print('Question # ',q_idx, ' -> ' , q)
        print(a)
        print(b)
        print(conf)
        print('winner', winner)
        temp = 0
        if winner is None:
            ratings[a], ratings[b] = update_elo(ratings[a], ratings[b], 0.5)
        elif winner == "A":
            ratings[a], ratings[b] = update_elo(ratings[a], ratings[b], conf)
        else:
            ratings[a], ratings[b] = update_elo(ratings[a], ratings[b], 1 - conf)

    ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    top3   = ranked[:6]
    pred   = top3[0][0]
    ok     = pred == correct
    overall_correct += ok

    print(f"\n❓ {q}")
    for rank, (ans, score) in enumerate(top3, 1):
        print(f"  {rank}. ({score:6.1f}) {ans}")
    print(f"✓ Ground-truth : {correct}")
    print("✔️  CORRECT" if ok else "❌ WRONG")
    print("-" * 70)

print(f"\nOverall top-1 accuracy on 9 questions: {overall_correct/len(questions):.2%}")
tmp = 0
