import random
import math
from scipy.stats import bernoulli


WIDTH, HEIGHT = 1000, 800       # Domain size (pixels correspond to mm)
FPS = 60                        # Simulation FPS
BLACK = (0, 0, 0)            
RED = (255, 0, 0)           
GREEN = (0, 255, 0)         
BLUE = (0, 0, 255)          
ORANGE = (255, 165, 0)      
GREY = (128, 128, 128)      
WHITE = (255, 255, 255)     
SCALE = 3                       # Scales the Kilobots to user preference (1 represents real size compared to domain)
SPEED = 10 / SCALE          
RADIUS = 30 / SCALE         
DETECT_RADIUS = 500 / SCALE     # Kilobot neighborhood detection radius
TUMBLE_RATE = 5000              # Tumble probability rate 
TUMBLE_DELAY = 500              # Time (ms) to complete tumbling action
ADJUST_DELAY = 250              # Time (ms) to complete adjusting action
ADJUST_TICK = 1000              # Time (ms) between neighbor detection
ALIGNMENT = -1                  # 1: align, -1: anti-align
STATES = {
    "RUNNING"  : BLACK,
    "TUMBLING" : RED,
    "ADJUSTING" : GREEN,
    "COLLISION" : ORANGE
}


class Kilobot():
    
    """CLass to define Kilobot objects for simulating Kilobots in Pygame
    """
    def __init__(self, click_place=False) -> None:
        """Initialise Kilobots with a random location and heading unless specified (typically with a mouse placement)

        Args:
            click_place (optional): Optional parameter that passes (x, y, theta) for specified placements. Defaults to False.
        """
        if click_place:
            self.x, self.y, self.theta = click_place
        else:
            self.x = random.uniform(0, WIDTH)
            self.y = random.uniform(0, HEIGHT)
            self.theta = random.uniform(0, 2*math.pi)
        self.step_since_run = 0
        self.step_since_tumble = 0
        self.step_since_adjust = 0
        self.step_since_colliding = 0
        self.adjust_tick = 0
        self.neighbor_count = 0
        self.tumbling = False
        self.adjusting = False
        self.colliding = False
        self.status = STATES["RUNNING"]
        self.detection = BLACK
        self.trail = []
        
    
    def events(self):
        """Handles event logic based on Kilobot current state
        """
        if self.tumbling:
            self.handle_tumble()
        elif self.adjusting:
            self.handle_adjusting()
        elif self.colliding:            # Currently not being used
            self.handle_collision()
        else:
            self.handle_run()
        
    
    def tumble(self):
        """Randomly tumble based on exponential distribution
        """
        if bernoulli.rvs(self.tumble_probability()):
            self.tumbling = True
            self.theta = random.uniform(0, 2 * math.pi)
            self.step_since_tumble = 0
            
            
    def neighbor_detect(self, kilobots):
        """Detect Kilobots within the specified DETECT_RADIUS and adjusts heading based on ALIGNMENT

        Args:
            kilobots (list): List of all other Kilobots
        """
        avg_theta = 0
        count = 1
        if self.adjust_tick == 0:
            self.adjust_tick = milliseconds_to_frames(ADJUST_TICK)
            avg_theta = self.theta
            for kilobot in kilobots:
                if kilobot != self and self.distance_from_neighbor(kilobot) < DETECT_RADIUS:
                    avg_theta += kilobot.theta
                    count += 1
            if count > 1:
                avg_theta /= ALIGNMENT*count
                self.theta += ALIGNMENT*(avg_theta - self.theta)
                self.theta %= 2*math.pi    
                self.adjusting = True
                self.step_since_adjust = 0
                self.detection = BLUE
                self.neighbor_count = count - 1 
            else:
                self.status = STATES["RUNNING"]
                self.detection = BLACK
                self.neighbor_count = 0
        else:      
            self.adjust_tick -= 1
            
            
    def collision(self, collision):
        """Calculates resultant collision positions and headings - Currently not in use

        Args:
            collision (Kilobot): Colliding Kilobot object
        """
        self.colliding, collision.colliding = True, True
        self.x -= SPEED * math.cos(self.theta)
        self.y -= SPEED * math.sin(self.theta)
        collision.x -= SPEED * math.cos(collision.theta)
        collision.y -= SPEED * math.sin(collision.theta)
        self.theta += math.pi
        collision.theta += math.pi
            
            
    def handle_run(self):   
        """Handles running logic 
        """
        self.x += SPEED * math.cos(self.theta)
        self.y += SPEED * math.sin(self.theta)
        # Periodic boundary conditions
        self.x %= WIDTH
        self.y %= HEIGHT
        self.step_since_tumble += 1
        self.status = STATES["RUNNING"]
        self.trail.append(tuple([self.x, self.y]))
        
        # Collision detection - currently not in use
        # for kilobot in kilobots:
        #     if kilobot != self and self.distance_from_neighbor(kilobot) < 2*RADIUS:
        #         self.collision(kilobot)
    
    
    def handle_tumble(self):
        """Handles tumbling logic
        """
        self.step_since_run += 1
        self.status = STATES["TUMBLING"]
        if self.step_since_run >= milliseconds_to_frames(TUMBLE_DELAY):
            self.tumbling = False
            self.step_since_run = 0
            
    
    def handle_adjusting(self):
        """Handles adjusting (AKA alignment) logic
        """
        self.step_since_run += 1
        self.status = STATES["ADJUSTING"]
        if self.step_since_run >= milliseconds_to_frames(ADJUST_DELAY):
            self.adjusting = False
            self.step_since_run = 0        
        
        
    def handle_collision(self):
        """Handles collision logic - Currently not in use
        """
        self.step_since_colliding += 1
        self.adjust_tick = milliseconds_to_frames(500)
        self.status = STATES["COLLISION"]
        if self.step_since_colliding == milliseconds_to_frames(500):
            self.colliding = False
            self.step_since_colliding = 0
        
    
    def tumble_probability(self):
        """Calculates probability of a tumbling event occurring based on TUMBLE_RATE and number of 

        Returns:
            float: Tumble probability
        """
        return 1 - math.exp(-(1/TUMBLE_RATE)*(self.step_since_tumble))
               
            
    def distance_from_neighbor(self, neighbor):
        """Calculates euclidean distance to neighboring Kilobot

        Args:
            neighbor (Kilobot): neighboring kilobot

        Returns:
            float: Euclidean distance
        """
        return math.sqrt((self.x - neighbor.x) ** 2 + (self.y - neighbor.y) ** 2) 
            
    
def milliseconds_to_frames(time):
    return int(time / 1000 * FPS)


def frames_to_milliseconds(frame):
    return 1000 * frame / FPS  