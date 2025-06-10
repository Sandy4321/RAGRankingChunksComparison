import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define range of x values (rating difference scaled)
x = np.linspace(-4, 4, 500)

# Normal CDF for the Gaussian-based model
normal_cdf = norm.cdf(x)

# Logistic (sigmoid) approximation to normal CDF
# Logistic function scaled to best approximate the normal CDF
k = np.pi / np.sqrt(3)  # optimal scaling factor for logistic ≈ 1.8138
logistic_approx = 1 / (1 + np.exp(-k * x))

# Base-10 logistic used in ELO:
elo_logistic = 1 / (1 + 10 ** (-x * np.log10(np.e) * k))  # base 10 version

# Plotting
plt.plot(x, normal_cdf, label='Normal CDF (Φ)', linewidth=2)
plt.plot(x, logistic_approx, '--', label='Logistic Approx (e-base)', linewidth=2)
plt.plot(x, elo_logistic, ':', label='ELO Logistic (base-10)', linewidth=2)
plt.axhline(0.5, color='gray', linestyle=':')
plt.axvline(0, color='gray', linestyle=':')
plt.legend()
plt.title("Normal CDF vs Logistic Approximations (ELO-style)")
plt.xlabel("Rating Difference (standardized)")
plt.ylabel("Win Probability")
plt.grid(True)
plt.tight_layout()
plt.show()