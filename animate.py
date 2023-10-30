import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from particles import Particle

# Simulation Parameters
SIM_PARAMS = {
    "NUM_PARTICLES" : 10,
    "SPEED" : 0.5,
    "SPAWN": 1/3,
    "RADIUS" : 0.5,
    "DETECT_RADIUS" : 1,
    "TUMBLE_RATE" : 20,
    "WIDTH" : 15,
    "HEIGHT" : 15,
    "SIM_TIME" : 500
}

def scatter_plot(ax, make_path=False):
    # Particle Simulation Plot
    ax.set_xlim(-SIM_PARAMS["WIDTH"], SIM_PARAMS["WIDTH"])
    ax.set_ylim(-SIM_PARAMS["HEIGHT"], SIM_PARAMS["HEIGHT"])
    ax.grid(True)
    ax.set_title("Run and Tumble Simulation - Anti-Align")
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    scatter = ax.scatter([], [], s=50)
    
    if make_path:
        path, = ax.plot([], [])
        return scatter, path
        
    return scatter


def mean_distance_plot(ax):
    # Average Distance from Start Plot
    ax.set_xlim(0, SIM_PARAMS["SIM_TIME"])
    ax.set_ylim(0, math.sqrt((2*SIM_PARAMS["WIDTH"])**2 + (2*SIM_PARAMS["HEIGHT"])**2))
    ax.grid(True)
    ax.set_title("Particle Distance from Start")
    ax.set_xlabel("Time (frames)")
    ax.set_ylabel("Distance (cm)")
    line_mean, = ax.plot([], [])
    
    return line_mean


def alignment_correlation_plot(ax):
    # Average Distance from Start Plot
    ax.set_xlim(0, SIM_PARAMS["SIM_TIME"])
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True)
    ax.set_title("Alignment Correlation")
    ax.set_xlabel("Time (frames)")
    ax.set_ylabel("Correlation")
    
    line_align, = ax.plot([], [], lw=2, label="Corr")
    
    return line_align
    

# Update function for the animation
def scatter_update(frame):
 
    scatter.set_offsets([(particle.x, particle.y) for particle in particles])
    
    # particle_path_x.append([particle.x for particle in particles])
    # particle_path_y.append([particle.y for particle in particles])
    # path.set_data([particle_path_x], [particle_path_y])
    
    time.append(frame)
    
    mean_distance = np.mean([particle.distance_from_start() for particle in particles])
    mean_dist.append(mean_distance)
    line_mean.set_data(time, mean_dist)
    
    directions = np.array([[math.cos(particle.theta), math.sin(particle.theta)] for particle in particles])
    mean_direction = np.mean(directions, axis=0)
    mag = np.linalg.norm(mean_direction)
    align_corr.append(mag)
    line_align.set_data(time, align_corr)
    
    for particle in particles:
        particle.anti_align(particles)
        particle.run(frame, particles)
        particle.tumble()
    
    return scatter, line_mean, line_align


particles = [Particle(SIM_PARAMS) for _ in range(SIM_PARAMS["NUM_PARTICLES"])]
# particles = [Particle(SIM_PARAMS, set_start=[0, 0, 0])]

time = []
particle_path_x, particle_path_y = [], []
mean_dist = []
align_corr = []

# Create scatter animation
fig, axs = plt.subplots(1, 3, figsize=(12, 6))
scatter = scatter_plot(axs[0])
line_mean = mean_distance_plot(axs[1])
line_align = alignment_correlation_plot(axs[2])
ani = FuncAnimation(fig, scatter_update, frames=range(SIM_PARAMS["SIM_TIME"]), blit=True, interval=50, repeat=False)

# Save Animation
# ani.save("run_and_tumble_anti_align.gif")

# Show the animation
plt.show()