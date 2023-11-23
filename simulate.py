import matplotlib.pyplot as plt
import numpy as np
import math
from particles import Particle

SIM_PARAMS = {
    "NUM_PARTICLES" : 50,
    "SPEED" : 0.5,
    "RADIUS" : 1,
    "DETECT_RADIUS" : 1,
    "TUMBLE_RATE" : 10,
    "WIDTH" : 10,
    "HEIGHT" : 10,
    "SIM_TIME" : 500
}

# Sample data
# particles = [Particle(SIM_PARAMS, set_start=[0.5, 0.6, -math.pi/2]), 
#              Particle(SIM_PARAMS, set_start=[0.4, 0.4, math.pi/4]),
#              Particle(SIM_PARAMS, set_start=[0.6, 0.4, 3*math.pi/4])
#             ]
particles = [Particle(SIM_PARAMS, set_start=[1, 1, math.pi/4]), 
             Particle(SIM_PARAMS, set_start=[3, 1, 3*math.pi/4]),
            #  Particle(SIM_PARAMS, set_start=[5, 1, math.pi/2]),
            #  Particle(SIM_PARAMS, set_start=[7, 1, -math.pi/2]),
            #  Particle(SIM_PARAMS, set_start=[9, 1, math.pi/4])
            ]
time_steps = 4

x = []
y = []
theta = []
align_corr = []

for i in range(time_steps + 1):
    
    x.append([particle.x for particle in particles])
    y.append([particle.y for particle in particles])
    theta.append([particle.theta for particle in particles])
    
    directions = np.array([[math.cos(particle.theta), math.sin(particle.theta)] for particle in particles])
    mean_direction = np.mean(directions, axis=0)
    mag = np.linalg.norm(mean_direction)
    align_corr.append(mag)
    
    for particle in particles:
        particle.anti_align(particles)
        particle.run(i, particles)
        # particle.tumble()

 
# Arrow parameters
arrow_length = 1
arrow_color = 'black'

# Number of timesteps to plot
num_plots = 4
step_space = (time_steps // (num_plots - 1))

# Create a scatter plot
fig, axs = plt.subplots(1, num_plots, figsize=(14, 4))

for i in range(num_plots):
    scatter = axs[i].scatter(x[i*step_space], y[i*step_space], s=200)
    
    for j in range(len(particles)):
        dx = arrow_length * np.cos(theta[i*step_space][j])
        dy = arrow_length * np.sin(theta[i*step_space][j])
        axs[i].arrow(x[i*step_space][j], y[i*step_space][j], dx, dy, head_width=0.5, head_length=0.5, fc=arrow_color, ec=arrow_color)

    axs[i].set_title(f"Timestep {i*step_space} - Align_Corr: {align_corr[i*step_space]:.2f}")
    axs[i].set_xlim(0, SIM_PARAMS["HEIGHT"])
    axs[i].set_ylim(0, SIM_PARAMS["WIDTH"])
    axs[i].grid(True)

# Set a common title for the entire figure
fig.suptitle("Particle Orientations over Time")
plt.show()
