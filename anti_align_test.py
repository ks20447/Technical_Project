import math
import random
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"text.usetex": True, 'font.size': 16})

def plot_polygon_arrows(ax, num_corners, angles, iteration):

    # Calculate the positions of the polygon's corners
    angle_increment = 2 * np.pi / num_corners
    radius = 2  # Set the radius of the circle in which the polygon is inscribed
    center_x, center_y = 5, 5  # Center of the plot
    
    x_positions = [center_x + radius * np.cos(angle_increment * i) for i in range(num_corners)]
    y_positions = [center_y + radius * np.sin(angle_increment * i) for i in range(num_corners)]
    
    # Generate random directions for the arrows
    dx = np.cos(angles)
    dy = np.sin(angles)
    
    # Plotting each arrow
    for x, y, dx, dy in zip(x_positions, y_positions, dx, dy):
        ax.arrow(x, y, dx, dy, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.scatter(x, y)
    
    ax.set_title(f"Iteration: {iteration}")
    # Set plot limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(["Heading", "Fixed Agent"])
    
    # Add grid and show the plot
    ax.grid(True)

# Number of corners/arrows to plot
num_angles = 8  # You can change this number to any other (3 for triangle, 4 for square, etc.)
angles = []
for angle in range(num_angles):
    angles.append(random.uniform(0, 2*math.pi))
    
fig, axs = plt.subplots(2, 2, figsize=(8, 8))
axs = axs.flatten()
    
plot_polygon_arrows(axs[0], num_angles, angles, 0)

for i in range(1, 4):
    avg_sin = 0
    avg_cos = 0
    for angle in angles:
        avg_sin += math.sin(angle)
        avg_cos += math.cos(angle)
    avg_sin /= num_angles
    avg_cos /= num_angles
    avg_sin = round(avg_sin, 5)
    avg_cos = round(avg_cos, 5)
    new_angle = math.atan2(-avg_sin, -avg_cos)
    new_angle %= 2*math.pi

    angles = [new_angle] * num_angles
    plot_polygon_arrows(axs[i], num_angles, angles, i)

plt.suptitle("Anti-Alignment Trivial Case")
plt.tight_layout()
plt.savefig("Results/AntiAlignTrivial.png")
