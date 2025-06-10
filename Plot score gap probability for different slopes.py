import numpy as np
import matplotlib.pyplot as plt

# Data
gaps = np.linspace(-100, 100, 400)
denoms = [10, 15, 20, 25, 30]

plt.figure(figsize=(8, 5))
for d in denoms:
    probs = 1 / (1 + np.exp(-gaps / d))
    plt.plot(gaps, probs, label=f"d={d}")

plt.title("Logistic mapping: score gap Δ → probability p(Δ)", fontsize=16)
plt.xlabel("Δ = scoreA − scoreB", fontsize=12)
plt.ylabel("Probability p(Δ)  (answer A better)", fontsize=12)
plt.grid(True)
plt.legend()

# Main logistic equation (large)
log_eq = r"$p(\Delta)=\frac{1}{1+e^{-\Delta/d}}$"
plt.text(0.98, 0.10, log_eq,
         transform=plt.gca().transAxes,
         fontsize=32, ha='right', va='bottom',
         bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', pad=6))

# Confidence rule positioned higher (around 0.35 from bottom)
conf_eq = "confidence = p  if winner = A\nconfidence = 1 − p  if winner = B"
plt.text(0.98, 0.35, conf_eq,
         transform=plt.gca().transAxes,
         fontsize=14, ha='right', va='bottom',
         bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', pad=4))

# Removed the mid-plot annotation

plt.tight_layout()
plt.show()
