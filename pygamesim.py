import pygame 
import math
import sys
import pandas as pd
import csv
from kilobots import *


# Simulation time (ms) (=math.inf for continuous running but no data collection)
SIM_TIME = 120000
# Number of Kilobots to begin simulation with
NUM_KILOBOTS = 250
# SIM_PARAMS = {0 : {"tumbling" : False, "detecting" : False}, 
#               1 : {"tumbling" : True, "detecting" : False}, 
#               2 : {"tumbling" : False, "detecting" : True}, 
#               3 : {"tumbling" : True, "detecting" : True}
#               }
SIM_PARAMS = {0 : {"tumbling" : True, "detecting" : True}}
NUM_SIMS = len(SIM_PARAMS)
SIM_NAME = "test"

    
    
def handle_inputs(event):
    global paused, tumbling, detecting, radii, ALIGNMENT
    
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
        grid_size = 50

        clock = pygame.time.Clock()
        time_step = 0
        kilobots = []
        added_kilobots = 0
        kilobot_df = pd.DataFrame(columns=["TimeStep", "KilobotID", "X", "Y", "Theta"])
        
        simulating = True
        paused = False
        tumbling = SIM_PARAMS[sim]["tumbling"]
        detecting = SIM_PARAMS[sim]["detecting"]
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
            csv_writer.writerow(['TimeStep', 'KilobotID', 'X', 'Y', 'Theta', 'Neighbors']) 

            while simulating:
                
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
                        
                screen.fill(WHITE)
                    
                text_surface = font.render(text, True, BLACK)
                screen.blit(text_surface, (0, 0))
                        
                for x in range(0, WIDTH, grid_size):
                    pygame.draw.line(screen, GREY, (x, 0), (x, HEIGHT), 1)

                for y in range(0, HEIGHT, grid_size):
                    pygame.draw.line(screen, GREY, (0, y), (WIDTH, y), 1)

                if kilobots:
                    for kilobot_id, kilobot in enumerate(kilobots):
                        
                        if not paused:
                            
                            if time_step % milliseconds_to_frames(100) == 0 and SIM_TIME != math.inf:
                                # Record kilobot information
                                data = [time_step, kilobot_id, int(kilobot.x), int(kilobot.y), round(kilobot.theta, 2), int(kilobot.neighbor_count)]
                                csv_writer.writerow(data)                   
                            
                            if detecting:
                                kilobot.neighbor_detect(kilobots)  
                                
                            kilobot.events()
                            if tumbling:
                                kilobot.tumble()           
                        
                        pygame.draw.circle(screen, kilobot.status, (kilobot.x, kilobot.y), RADIUS)
                        if radii:
                            pygame.draw.circle(screen, kilobot.detection, (kilobot.x, kilobot.y), DETECT_RADIUS, 2)
                
                pygame.display.flip()
                time_step += 1
                clock.tick(FPS)
                
        pygame.quit()
    
    
    sys.exit()
    