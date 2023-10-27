import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from particles import Particle

# Simulation Parameters
SIM_PARAMS = {
    "NUM_PARTICLES" : 50,
    "SPEED" : 0.1,
    "RADIUS" : 0.1,
    "DETECT_RADIUS" : 1,
    "TUMBLE_RATE" : 20,
    "WIDTH" : 5,
    "HEIGHT" : 5,
    "SIM_TIME" : 500
}

def scatter_plot(ax):
    # Particle Simulation Plot
    ax.set_xlim(-SIM_PARAMS["WIDTH"], SIM_PARAMS["WIDTH"])
    ax.set_ylim(-SIM_PARAMS["HEIGHT"], SIM_PARAMS["HEIGHT"])
    ax.grid(True)
    ax.set_title("Run and Tumble Simulation - Anti Align")
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    scatter = axs[0].scatter([], [], s=50)
        
    return scatter


def mean_distance_plot(ax):
    # Average Distance from Start Plot
    ax.set_xlim(0, SIM_PARAMS["SIM_TIME"])
    ax.set_ylim(0, math.sqrt((2*SIM_PARAMS["WIDTH"])**2 + (2*SIM_PARAMS["HEIGHT"])**2))
    ax.grid(True)
    ax.set_title("Average Particle Distance from Start")
    ax.set_xlabel("Time (frames)")
    ax.set_ylabel("Distance (cm)")
    line, = ax.plot([], [])
    
    return line


def alignment_correlation_plot(ax):
    # Average Distance from Start Plot
    ax.set_xlim(0, SIM_PARAMS["SIM_TIME"])
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True)
    ax.set_title("Alignment Correlation")
    ax.set_xlabel("Time (frames)")
    ax.set_ylabel("Correlation")
    
    line, = ax.plot([], [], lw=2, label="Corr")
    
    return line
    

# Update function for the animation
def scatter_update(frame):
 
    scatter.set_offsets([(particle.x, particle.y) for particle in particles])
    
    time.append(frame)
    
    # mean_distance = np.mean([particle.distance_from_start() for particle in particles])
    # mean_dist.append(mean_distance)
    # line.set_data(time, mean_dist)
    
    directions = np.array([[math.cos(particle.theta), math.sin(particle.theta)] for particle in particles])
    mean_direction = np.mean(directions, axis=0)
    mag = np.linalg.norm(mean_direction)
    align_corr.append(mag)
    line.set_data(time, align_corr)
    
    for particle in particles:
        particle.anti_align(particles)
        particle.run(frame, particles)
        particle.tumble()
    
    return scatter, line


particles = [Particle(SIM_PARAMS) for _ in range(SIM_PARAMS["NUM_PARTICLES"])]

time = []
mean_dist = []
align_corr = []

# Create scatter animation
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
scatter = scatter_plot(axs[0])
# line = mean_distance_plot(axs[1])
line = alignment_correlation_plot(axs[1])
ani = FuncAnimation(fig, scatter_update, frames=range(SIM_PARAMS["SIM_TIME"]), blit=True, interval=50, repeat=False)

# Save Animation
# ani.save("run_and_tumble_anti_align.gif")

# Show the animation
plt.show()