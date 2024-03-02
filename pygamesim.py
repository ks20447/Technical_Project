import pygame 
import math
import sys
import csv
from kilobots import *

# Simulation time (ms) (=math.inf for continuous running but no data collection)
SIM_TIME = 100000
# Number of Kilobots to begin simulation with
NUM_KILOBOTS = 50
# SIM_PARAMS = {0 : {"tumbling" : False, "detecting" : False}, 
#               1 : {"tumbling" : True, "detecting" : False}, 
#               2 : {"tumbling" : False, "detecting" : True}, 
#               3 : {"tumbling" : True, "detecting" : True}
#               }
SIM_PARAMS = {0 : {"tumbling" : True, "detecting" : True, "alignment" : -1, "pattern" : 0}}
NUM_SIMS = len(SIM_PARAMS)
SIM_NAME = "test"
SQUARE_LENGTH = 10

    
def handle_inputs(event):
    global paused, tumbling, detecting, radii
    
    if event.key == pygame.K_SPACE:
        paused = not paused
    if event.key == pygame.K_t:
        tumbling = not tumbling
    if event.key == pygame.K_d:
        detecting = not detecting
    if event.key == pygame.K_r:
        radii = not radii  
        
        
if __name__ == "__main__": 
    
    for sim in range(NUM_SIMS):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Kilobot Run and Tumble Simulation")
        
        if SIM_PARAMS[sim]["pattern"] == 1:
            bg = pygame.image.load("Patterns/pattern_very_tiny.png")
        elif SIM_PARAMS[sim]["pattern"] == 2:
            bg = pygame.image.load("Patterns/pattern_intensity.png")
        else:
            grid_size = 50

        clock = pygame.time.Clock()
        time_step = 0
        kilobots = []
        added_kilobots = 0
        com_x, com_y = 0, 0
        
        simulating = True
        paused = False
        tumbling = SIM_PARAMS[sim]["tumbling"]
        detecting = SIM_PARAMS[sim]["detecting"]
        alignment = SIM_PARAMS[sim]["alignment"]
        pattern = SIM_PARAMS[sim]["pattern"]
        radii = False

        while len(kilobots) < NUM_KILOBOTS:
            
            kilobot = Kilobot()
            
            if not any((bot.x, bot.y) == (kilobot.x, kilobot.y) for bot in kilobots):
                kilobots.append(kilobot)
        
        font = pygame.font.Font(None, 30)
        text = "SPACE : Pause  T : Tumble  D : Detection  R : Radii  Click : Add Kilobot"
        
        csv_file_path = f"Data/kilobot_simulation_data_pandas_{SIM_NAME}.csv"
        with open(csv_file_path, 'w', newline='') as csvfile:
            
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['TimeStep', 'KilobotID', 'X', 'Y', 'Theta', 'Neighbors', 'CoMX', 'CoMY', 'EstimateHeading', 'EstimateError']) 

            while simulating:

                if pattern:
                    screen.blit(bg, (0, 0))
                else:
                    screen.fill(Color.WHITE.value)
                    
                
                if SIM_TIME != math.inf:
                    if time_step == milliseconds_to_frames(SIM_TIME):
                        simulating = False
                
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        simulating = False  
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        added_kilobots += 1
                        kilobots.append(Kilobot(click_place=(mouse_x, mouse_y, added_kilobots*math.pi/2)))
                    elif event.type == pygame.KEYDOWN:
                        handle_inputs(event)                                         
                    
                text_surface = font.render(text, True, Color.BLACK.value)
                screen.blit(text_surface, (0, 0))
                        
                if not pattern:
                    for x in range(0, WIDTH, grid_size):
                        pygame.draw.line(screen, Color.GREY.value, (x, 0), (x, HEIGHT), 1)

                    for y in range(0, HEIGHT, grid_size):
                        pygame.draw.line(screen, Color.GREY.value, (0, y), (WIDTH, y), 1)

                if kilobots:
                    for kilobot_id, kilobot in enumerate(kilobots):
                        
                        if not paused:
                            
                            if time_step % milliseconds_to_frames(100) == 0 and SIM_TIME != math.inf:
                                # Record kilobot information
                                data = [time_step, kilobot_id, int(kilobot.x), int(kilobot.y),
                                        round(kilobot.theta, 2), int(kilobot.neighbor_count),
                                        int(com_x), int(com_y), round(kilobot.est_heading, 2),
                                        round(kilobot.heading_error, 2)]
                                csv_writer.writerow(data)                   
                            
                            if detecting:
                                kilobot.neighbor_detect(kilobots, alignment)  
                                
                            kilobot.events()
                            
                            com_x, com_y = kilobot.centre_of_mass(kilobots)
                            
                            if pattern == 1:
                                bg_color = bg.get_at((int(kilobot.x), int(kilobot.y)))
                                old_sequence = kilobot.sequence.copy()
                                kilobot.color_sequence(bg_color)
                                
                                if (kilobot.sequence != old_sequence):
                                    kilobot.estimate_heading()
                                    
                            elif pattern == 2:
                                prev_reading = 0
                                if kilobot.intensity_read:
                                    prev_reading = kilobot.intensity_read
                                    prev_time_step = kilobot.intense_read_time
                                
                                kilobot.intensity_read = bg.get_at((int(kilobot.x), int(kilobot.y)))
                                kilobot.intense_time_read = time_step
                                
                                if prev_reading:
                                    kilobot.intensity_heading(prev_reading, prev_time_step, SQUARE_LENGTH) 
                                
                            if tumbling:
                                kilobot.tumble()           
                        
                        pygame.draw.circle(screen, kilobot.status, (kilobot.x, kilobot.y), RADIUS)
                        pygame.draw.circle(screen, Color.GREY.value, (com_x, com_y), RADIUS/2)
                        
                        if radii:
                            pygame.draw.circle(screen, kilobot.detection, (kilobot.x, kilobot.y), DETECT_RADIUS, 2)
                
                pygame.display.flip()
                time_step += 1
                clock.tick(FPS)
                
        pygame.quit()
    
    
    sys.exit()
    