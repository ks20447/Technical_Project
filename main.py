"""Final Year Technical Project - Anti-Aligning Robots

The control of macroscopic robot collectives is an important techniques in many technological
applications. At a fundamental level, it is important to understand how the rules governing the robot
interactions influence the emergent collective behavior of a robot swarm. In particular, seemingly
innocuous changes in the interaction rules can lead to drastically different collective dynamics. This
project will design and develop a robot swarm whose agents preferentially anti-align (in contrast to
classical models of aligning particles such as the Viczek model of collective motion), comparing the
results to theoretical models developed by collaborators at Brandeis University.

Author - Adam Morris
Created - 05/10/2023

"""


import math
import random as rn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import bernoulli


# Simulation Parameters
NUM_PARTICLES = 20
SPEED = 0.1
TUMBLE_RATE = 20
WIDTH, HEIGHT = 5, 5
SIM_TIM = 200


class Particle():
    
    def __init__(self) -> None:
        # Initial conditions
        self.start_x = rn.uniform(-HEIGHT, HEIGHT)
        self.start_y = rn.uniform(-HEIGHT, HEIGHT)
        self.start_theta = rn.uniform(-2 * math.pi, 2 * math.pi)
        self.speed = SPEED
        self.tumble_rate = TUMBLE_RATE
        # Current states
        self.x = self.start_x
        self.y = self.start_y
        self.theta = self.start_theta
        self.run_num = 0
        # Distance array
        self.dist = np.empty(SIM_TIM + 1)
        
        
        
    def run(self, time_step):
        # Update position
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)
        # Update run number for tumble probability
        self.run_num += 1
        # Uncomment to make semi-infinite domain
        # if self.x > WIDTH or self.x < -WIDTH:
        #     self.x *= -1
        # if self.y > HEIGHT or self.y < -HEIGHT:
        #     self.y *= -1
        # Calculate distance from initial conditions
        self.dist[time_step] = self.distance_from_start()
        

    def tumble(self):
        # Perform tumble with probability 1 - exp(-lambda*x)
        if bernoulli.rvs(self.tumble_probability()):
            self.theta += rn.uniform(0, 2 * math.pi)
            self.run_num = 0
        
        
    def distance_from_start(self):
        return math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
    
    def tumble_probability(self):
        return 1 - math.exp(-(1/self.tumble_rate)*self.run_num)
        
        
particles = [Particle() for _ in range(NUM_PARTICLES)]
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Particle Simulation Plot
axs[0].set_xlim(-WIDTH, WIDTH)
axs[0].set_ylim(-HEIGHT, HEIGHT)
axs[0].grid(True)
axs[0].set_title("Run and Tumble Simulation")
axs[0].set_xlabel("x (cm)")
axs[0].set_ylabel("y (cm)")
scatter = axs[0].scatter([particle.x for particle in particles], [particle.y for particle in particles])

# Average Distance from Start Plot
axs[1].set_xlim(0, SIM_TIM)
axs[1].set_ylim(0, math.sqrt((2*WIDTH)**2 + (2*HEIGHT)**2))
axs[1].grid(True)
axs[1].set_title("Average Particle Distance from Start")
axs[1].set_xlabel("Time (frames)")
axs[1].set_ylabel("Distance (cm)")
line, = axs[1].plot(0, 0)

# Update function for the animation
def update(frame):
    
    for particle in particles:
        particle.run(frame)
        particle.tumble()
 
    scatter.set_offsets([(particle.x, particle.y) for particle in particles])
    
    time = np.linspace(0, SIM_TIM, SIM_TIM + 1)
    y_data = np.mean([particle.dist[0:frame] for particle in particles], axis=0)
    
    line.set_data(time[0:frame], y_data)
    
    return scatter, line


# Create the animation
ani = FuncAnimation(fig, update, frames=range(SIM_TIM), blit=True, interval=50, repeat=False)

# Save Animation
# ani.save("run_and_tumble.gif")

# Show the animation
plt.show()