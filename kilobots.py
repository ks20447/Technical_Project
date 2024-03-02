import random
import math
from headings import HEADINGS_MAP
from scipy.stats import bernoulli
from enum import Enum

class Color(Enum):
        
    BLACK = (0, 0, 0, 255)            
    RED = (255, 0, 0, 255)           
    GREEN = (0, 255, 0, 255)         
    BLUE = (0, 36, 255, 255)
    CYAN =  (0, 234, 255, 255)  
    YELLOW = (252, 255, 0, 255)   
    MAGENTA = (255, 0, 255, 255)          
    GREY = (128, 128, 128, 255)      
    WHITE = (255, 255, 255, 255)
    
    
WIDTH, HEIGHT = 1000, 800      # Domain size (1 pixel correspond to 10mm)
FPS = 60                       # Simulation FPS     
SCALE = 8                      # Scales the Kilobots to user preference (1 represents real size compared to domain)
SPEED = 0.1 * SCALE          
RADIUS = 1.3 * SCALE         
DETECT_RADIUS = 10 * SCALE     # Kilobot neighborhood detection radius
TUMBLE_RATE = 5000             # Tumble probability rate 
TUMBLE_DELAY = 500             # Time (ms) to complete tumbling action
ADJUST_DELAY = 500             # Time (ms) to complete adjusting action
ADJUST_TICK = 1000             # Time (ms) between neighbor detection
STATES = {
    "RUNNING"  : Color.BLACK.value,
    "TUMBLING" : Color.RED.value,
    "ADJUSTING" : Color.GREEN.value,
}
ENUM_COLOR = {
    "BLACK": 0,
    "YELLOW": 1,
    "CYAN": 2,
    "MAGENTA": 3,
    "BLUE": 4,
    "RED": 5,
    "GREEN": 6,
    "WHITE": 7,
    "GREY": 8
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
            self.x = random.uniform(WIDTH / 4, 3 * WIDTH / 4)
            self.y = random.uniform(HEIGHT / 4, 3 * HEIGHT / 4)
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
        self.detection = Color.BLACK.value
        self.trail = []
        self.detected_color = ()
        self.sequence = []
        self.est_heading = 0
        self.intensity_read = 0
        self.intense_read_time = 0
        self.x_vel, self.y_vel = 0, 0
        self.heading_error = 0
        
        
    
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
            
            
    def neighbor_detect(self, kilobots, alignment):
        """Detect Kilobots within the specified DETECT_RADIUS and adjusts heading based on alignment

        Args:
            kilobots (list): List of all other Kilobots
        """
        avg_sin_theta, avg_cos_theta = 0, 0
        count = 0
        if self.adjust_tick == 0:
            self.adjust_tick = milliseconds_to_frames(ADJUST_TICK)
            for kilobot in kilobots:
                if self.distance_from_neighbor(kilobot) < DETECT_RADIUS:
                    avg_sin_theta += math.sin(kilobot.theta)
                    avg_cos_theta += math.cos(kilobot.theta)
                    # avg_theta += kilobot.theta
                    count += 1
            if count > 1:
                avg_sin_theta /= alignment*(count + 1)
                avg_cos_theta /= alignment*(count + 1)
                self.theta = math.atan2(avg_sin_theta, avg_cos_theta)  
                self.adjusting = True
                self.step_since_adjust = 0
                self.detection = Color.BLUE.value
                self.neighbor_count = count - 1 
            else:
                self.status = STATES["RUNNING"]
                self.detection = Color.BLACK.value
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
    
    
    def color_sequence(self, color):
        
        if self.detected_color != color:
            if len(self.sequence) == 3:
                self.sequence.pop(0)
            self.detected_color = color
            self.sequence.append(self.detected_color)
            
    
    def convert_sequence(self):
        
        sequence = []
        
        for i in range(0, 3):
            color = color_enumerate(self.sequence[i], Color)
            sequence.append(ENUM_COLOR[str(color)])
        
        return sequence
            
    
    def estimate_heading(self):
        
        if len(self.sequence) == 3:
            sequence = self.convert_sequence()
            num = 100 * sequence[0] + 10 * sequence[1] + sequence[2]
            
            heading_index = HEADINGS_MAP.get(num, None)
            if heading_index is not None:
                self.est_heading = heading_index * 2 * math.pi / 12
                
                self.heading_error = abs((self.theta - self.est_heading + math.pi) % (2 * math.pi) - math.pi)
    
    
    def evaluate_color(self, reading):
        
        R, G, B, _ = reading
        
        if G == 0 and B == 0:
            return Color.RED
        elif B == 0 and R == 0:
            return Color.GREEN
        else: 
            return Color.WHITE     
             
                  
    def intensity_heading(self, prev_reading, prev_time, square_length):
        
        prev_color = self.evaluate_color(prev_reading)
        cur_color = self.evaluate_color(self.intensity_read)
        
        if prev_color != cur_color:
            diff_time = self.intense_time_read - prev_time
            
            sequence = [prev_color, cur_color]
            
            if sequence == [Color.RED, Color.GREEN] or sequence == [Color.GREEN, Color.WHITE] or sequence == [Color.WHITE, Color.RED]:
                self.x_vel = square_length / diff_time
            else:
                self.x_vel = -square_length / diff_time
                
        else:
            if prev_reading != self.intensity_read:
                
                diff_time = self.intense_time_read - prev_time
                
                if sum(self.intensity_read) > sum(prev_reading):
                    self.y_vel = -square_length / diff_time
                else:
                    self.y_vel = square_length / diff_time
                
        heading = math.atan2(self.y_vel, self.x_vel)   
        
        if heading < 0:
            heading += 2*math.pi
              
        self.est_heading = heading
        self.heading_error = abs((self.theta - self.est_heading + math.pi) % (2 * math.pi) - math.pi)
                                       
                                                   
    def centre_of_mass(self, kilobots):
        
        num_bots = len(kilobots)
        com_x, com_y = 0, 0
        
        for kilobot in kilobots:
            com_x += kilobot.x
            com_y += kilobot.y
            
        return (1 / num_bots) * com_x, (1 / num_bots) * com_y
    
    
def milliseconds_to_frames(time):
    return int(time / 1000 * FPS)


def frames_to_milliseconds(frame):
    return 1000 * frame / FPS  


def color_enumerate(value, enum):
    
    for member in enum:
        if member.value == value:
            return member.name
    return None
    