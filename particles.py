"""Final Year Technical Project - Anti-Aligning Robots

The control of macroscopic robot collectives is an important techniques in many technological
applications. At a fundamental level, it is important to understand how the rules governing the robot
interactions influence the emergent collective behavior of a robot swarm. In particular, seemingly
innocuous changes in the interaction rules can lead to drastically different collective dynamics. This
project will design and develop a robot swarm whose agents preferentially anti-align (in contrast to
classical models of aligning particles such as the Viczek model of collective motion), comparing the
results to theoretical models developed by collaborators at Brandeis University.

Simulation of particles performing run-and-tumble motion in a semi-infinite domain. 

Author - Adam Morris
Created - 05/10/2023

"""


import math
import random as rn
import numpy as np
from scipy.stats import bernoulli


class Particle():
    """Particle object. Actions include run, tumble, collide and anti-align with other particles.
    """
    
    def __init__(self, sim_params, set_start=False,) -> None:
        """Initializes particle object with simulation parameters.

        Args:
            set_start (bool, optional): Optional parameter to manually set the starting conditions of a particle. Defaults to False. 
        """
        # Particle parameters
        self.speed = sim_params["SPEED"]
        self.radius = sim_params["RADIUS"]
        self.detect_radius = sim_params["DETECT_RADIUS"]
        self.tumble_rate = sim_params["TUMBLE_RATE"]
        self.domain_width = sim_params["WIDTH"]
        self.domain_height = sim_params["HEIGHT"]

        # Initial conditions
        if set_start:
            self.start_x, self.start_y, self.start_theta = set_start
        else:
            self.start_x = rn.uniform(-self.domain_width / 2, self.domain_width / 2)
            self.start_y = rn.uniform(-self.domain_height / 2, self.domain_height / 2)
            self.start_theta = rn.uniform(-2 * math.pi, 2 * math.pi)
        
        # Current states
        self.x = self.start_x
        self.y = self.start_y
        self.theta = self.start_theta
        self.run_num = 0
        
        # Distance array initialization
        self.dist = np.empty(sim_params["SIM_TIME"] + 1)
        
        
    def run(self, time_step, particles):
        # Update position
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)
        # Check for collisions
        for particle in particles:
            if particle != self and self.distance_from_neighbor(particle) < self.radius:
                self.collision(particle)
        # Update run number for tumble probability
        self.run_num += 1
        # Creates semi-infinite domain
        if self.x > self.domain_width or self.x < -self.domain_width:
            self.x *= -1
        if self.y > self.domain_height or self.y < -self.domain_height:
            self.y *= -1
        # # Creates bounded domain
        # if self.x + self.radius > self.domain_width or self.x - self.radius < - self.domain_width:
        #     self.x -= self.speed * math.cos(self.theta)
        #     self.y -= self.speed * math.sin(self.theta)
        #     self.theta -= math.pi
        # if self.y + self.radius > self.domain_height or self.y - self.radius < - self.domain_height:
        #     self.x -= self.speed * math.cos(self.theta)
        #     self.y -= self.speed * math.sin(self.theta)
        #     self.theta -= math.pi
        # Calculates distance from initial conditions
        self.dist[time_step] = self.distance_from_start()
        

    def tumble(self):
        # Perform tumble with probability 1 - exp(-lambda*x)
        if bernoulli.rvs(self.tumble_probability()):
            self.theta += rn.uniform(0, 2 * math.pi)
            self.run_num = 0
            
            
    def collision(self, particle):
        # Update trajectories on collision
        self.x -= self.speed * math.cos(self.theta)
        self.y -= self.speed * math.sin(self.theta)
        self.theta -= math.pi
        particle.x -= particle.speed * math.cos(particle.theta)
        particle.y -= particle.speed * math.sin(particle.theta)
        particle.theta -= math.pi
        
        
    def anti_align(self, particles):
        # Update particle direction based on neighboring particles
        avg_direction = [0, 0]
        count = 0
        for particle in particles:
            if self.distance_from_neighbor(particle) < self.detect_radius:
                avg_direction[0] += math.cos(particle.theta)
                avg_direction[1] += math.sin(particle.theta)
                count += 1
        if count > 1:
            avg_direction[0] /= count
            avg_direction[1] /= count
            avg_theta = -math.atan2(avg_direction[1], avg_direction[0])
            self.theta -= (avg_theta - self.theta)
               
        
    def distance_from_start(self):
        return math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
    
    def distance_from_neighbor(self, neighbor):
        return math.sqrt((self.x - neighbor.x) ** 2 + (self.y - neighbor.y) ** 2)
    
    def tumble_probability(self):
        return 1 - math.exp(-(1/self.tumble_rate)*self.run_num)