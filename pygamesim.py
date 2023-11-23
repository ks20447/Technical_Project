import pygame 
import random
import math
import sys
import pandas as pd
from scipy.stats import bernoulli
from kilobots import *


# Simulation time (=math.inf for continuous running but no data collection)
SIM_TIME = math.inf
# Number of Kilobots to begin simulation with
NUM_KILOBOTS = 5
    
    
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
    if event.key == pygame.K_a:
        ALIGNMENT *= -1
 
 
if __name__ == "__main__": 
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
    tumbling = True
    detecting = False
    radii = False

    while len(kilobots) < NUM_KILOBOTS:
        
        kilobot = Kilobot()
        
        if not any((bot.x, bot.y) == (kilobot.x, kilobot.y) for bot in kilobots):
            kilobots.append(kilobot)
    
    font = pygame.font.Font(None, 30)
    text = "SPACE : Pause  A : Alignment  T : Tumble  D : Detection  R : Radii  Click : Add Kilobot"

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
                        kilobot_info = {"TimeStep": time_step, "KilobotID": kilobot_id, "X": int(kilobot.x), "Y": int(kilobot.y), "Theta": round(kilobot.theta, 2)}
                        kilobot_df = pd.concat([kilobot_df, pd.DataFrame([kilobot_info])], ignore_index=True)
                    
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
        
        
    # Save the DataFrame to a CSV file
    if SIM_TIME != math.inf:
        csv_filename = "Data/kilobot_simulation_data_pandas.csv"
        kilobot_df.to_csv(csv_filename, index=False)
        
    pygame.quit()
    sys.exit()
    