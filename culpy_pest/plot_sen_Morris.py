# This file is part of CuLPy
# This program is free software distributed under the MIT License 
# A copy of the MIT License can be found at 
# https://github.com/kaynarob/CuLPy/blob/main/LICENSE.md

import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Load data from CSV file
data = pd.read_csv('data.csv')

# Extract columns
parameters = data['parameters']
mu_star = data['mu_star']
sigma = data['sigma']

# Create scatter plot
plt.figure(figsize=(6, 6), dpi=300)
plt.scatter(mu_star, sigma, color='blue', s=30, alpha=1, edgecolor='k', linewidths=0.2)

# Add text annotations
texts = [plt.text(mu_star[i], sigma[i], parameters[i], fontsize=8) for i in range(len(parameters))]

# Set logarithmic scale
plt.xscale('log')
plt.yscale('log')

# 1-to-1 line in log scale
line_min = min(min(mu_star), min(sigma)) * 0.9
line_max = max(max(mu_star), max(sigma)) * 1.1
plt.plot([line_min, line_max], [line_min, line_max], 'r--', label='1-to-1 line')

# Adjust text to prevent overlap
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

# Labels and title
plt.xlabel('Mean Sensitivity Index (μ*)', fontsize=12)
plt.ylabel('Standard Deviation (σ)', fontsize=12)
#plt.title('Morris Method Sensitivity Analysis (Logarithmic Scale)', fontsize=14)
#plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()

plt.savefig('morris_sensitivity_analysis.pdf', format='pdf')

# Show plot
plt.show()