# This file is part of CuLPy
# This program is free software distributed under the MIT License 
# A copy of the MIT License can be found at 
# https://github.com/kaynarob/CuLPy/blob/main/LICENSE.md


# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 17:18:12 2024

@author: burak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


# Load the CSV file
file_path = 'data.csv'  # Change this to your actual file path
data = pd.read_csv(file_path)

# Extracting the data
x = data['k_pel_42']
y = data['k_pel_01']
z = data['total']

# Creating a grid for contour plot
x_unique = np.linspace(x.min(), x.max(), 1000)
y_unique = np.linspace(y.min(), y.max(), 1000)
x_grid, y_grid = np.meshgrid(x_unique, y_unique)
z_grid = griddata((x, y), z, (x_grid, y_grid), method='cubic')

# Creating a combined 3D and 2D plot
fig = plt.figure(figsize=(12, 10), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# Plotting the 3D surface
surface = ax.plot_surface(x_grid, y_grid, z_grid, cmap='magma', alpha=1.0)

# Plotting the 2D contour beneath the 3D surface
contour = ax.contourf(x_grid, y_grid, z_grid, zdir='z', offset=-50, levels=100, cmap='magma', alpha=0.6)

# Adding 2D contour lines on the 3D plot
ax.contour(x_grid, y_grid, z_grid, zdir='z', offset=-50, levels=30, cmap='viridis')

# Prolonging the z-axis to -50
ax.set_zlim(-50, 100)

# Adding labels and title
ax.set_xlabel('nitrification rate (1/day)')
ax.set_ylabel('phytoplankton growth rate(1/day)')
ax.set_zlabel('Objective function (phi)')
#ax.set_title('3D Surface Plot with 2D Contour Lines')

# Adding a color bar
fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)

plt.show()
