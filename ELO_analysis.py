# Re-import necessary modules after code state reset
import numpy as np
import matplotlib.pyplot as plt

# Fixed A values
fixed_a_values = [800, 1000, 1200, 1500]
b_values = np.linspace(400, 2000, 200)

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Create smaller plots with better layout
fig, axs = plt.subplots(2, 2, figsize=(10, 7))  # smaller figure
axs = axs.ravel()

for idx, fixed_a in enumerate(fixed_a_values):
    elo_probs = []
    simple_probs = []
    sigmoid_probs = []

    for b in b_values:
        elo_p = 1 / (1 + 10 ** ((b - fixed_a) / 400))
        simple_p = fixed_a / (fixed_a + b)
        sigmoid_input = (fixed_a - b) / 400
        sigmoid_p = sigmoid(sigmoid_input)

        elo_probs.append(elo_p)
        simple_probs.append(simple_p)
        sigmoid_probs.append(sigmoid_p)

    ax = axs[idx]
    ax.plot(b_values, elo_probs, label="ELO Prob", linewidth=2)
    ax.plot(b_values, simple_probs, label="A/(A+B)", linestyle='--')
    ax.plot(b_values, sigmoid_probs, label="Sigmoid((a-b)/400)", linestyle='dotted')
    ax.set_title(f"A Skill = {fixed_a}", fontsize=10)
    ax.set_xlabel("B Skill", fontsize=9)
    ax.set_ylabel("P(A wins)", fontsize=9)
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(True)
    ax.legend(fontsize=7)

plt.suptitle("Win Probability: ELO vs A/(A+B) vs Sigmoid", fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
