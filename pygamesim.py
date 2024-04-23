import pygame 
import math
import sys
import csv
from kilobots import *

SQUARE_LENGTH = 50

def handle_inputs(event):
    global PAUSED, TUMBLING, DETECTING, radii, ALIGNMENT
    
    if event.key == pygame.K_SPACE:
        PAUSED = not PAUSED
    if event.key == pygame.K_t:
        TUMBLING = not TUMBLING
    if event.key == pygame.K_d:
        DETECTING = not DETECTING
    if event.key == pygame.K_r:
        radii = not radii 
    if event.key == pygame.K_0:
        ALIGNMENT = 0 
    if event.key == pygame.K_1:
        ALIGNMENT = 1
    if event.key == pygame.K_2:
        ALIGNMENT = -1
        
        
if __name__ == "__main__": 
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kilobot Run and Tumble Simulation")
    
    if PATTERN == 1:
        bg = pygame.image.load("Patterns/pattern_triangles.png")
    elif PATTERN == 2:
        bg = pygame.image.load("Patterns/pattern_intensity.png")
    else:
        grid_size = 50

    clock = pygame.time.Clock()
    time_step = 0
    kilobots = []
    added_kilobots = 0
    com_x, com_y = 0, 0
    
    simulating = True
    radii = False

    while len(kilobots) < NUM_KILOBOTS:
        
        kilobot = Kilobot()
        
        if not any((bot.x, bot.y) == (kilobot.x, kilobot.y) for bot in kilobots):
            kilobots.append(kilobot)
    
    font = pygame.font.Font(None, 20)
    
    csv_file_path = f"Data/Simulation/sim_data_{NAME}.csv"
    with open(csv_file_path, 'w', newline='') as csvfile:
        
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['TimeStep', 'KilobotID', 'X', 'Y', 'Theta', 'Neighbors', 'CoMX', 'CoMY', 'EstimateHeading', 'EstimateError']) 

        while simulating:
            
            text = f"SPACE : Pause  T : Tumble  D : Detection  R : Radii [0, 1, 2] : ALIGNMENT ({ALIGNMENT}) Click : Add Kilobot"

            if PATTERN:
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
                    kilobots.append(Kilobot(click_place=(mouse_x, mouse_y, -math.pi/4)))
                elif event.type == pygame.KEYDOWN:
                    handle_inputs(event)                                         
                
            text_surface = font.render(text, True, Color.BLACK.value)
            screen.blit(text_surface, (0, 0))
                    
            if not PATTERN:
                for x in range(0, WIDTH, grid_size):
                    pygame.draw.line(screen, Color.GREY.value, (x, 0), (x, HEIGHT), 1)

                for y in range(0, HEIGHT, grid_size):
                    pygame.draw.line(screen, Color.GREY.value, (0, y), (WIDTH, y), 1)

            if kilobots:
                for kilobot_id, kilobot in enumerate(kilobots):
                    
                    if not PAUSED:
                        
                        if time_step % milliseconds_to_frames(100) == 0 and SIM_TIME != math.inf:
                            # Record kilobot information
                            data = [time_step, kilobot_id, int(kilobot.x), int(kilobot.y),
                                    round(kilobot.theta, 2), int(kilobot.neighbor_count),
                                    int(com_x), int(com_y), round(kilobot.est_heading, 2),
                                    round(kilobot.heading_error, 2)]
                            csv_writer.writerow(data)                   
                        
                        if DETECTING:
                            kilobot.neighbor_detect(kilobots, ALIGNMENT)  
                            
                        kilobot.events()
                        
                        com_x, com_y = kilobot.centre_of_mass(kilobots)
                        
                        if PATTERN == 1:
                            bg_color = bg.get_at((int(kilobot.x), int(kilobot.y)))
                            old_sequence = kilobot.sequence.copy()
                            kilobot.color_sequence(bg_color)
                            
                            if (kilobot.sequence != old_sequence):
                                kilobot.estimate_heading()
                                
                        elif PATTERN == 2:
                            prev_reading = 0
                            if kilobot.intensity_read:
                                prev_reading = kilobot.intensity_read
                                prev_time_step_x = kilobot.intense_read_time_x
                                prev_time_step_y = kilobot.intense_read_time_y
                            
                            kilobot.intensity_read = bg.get_at((int(kilobot.x), int(kilobot.y)))
                            kilobot.intense_time_read_x = time_step
                            kilobot.intense_time_read_y = time_step
                            
                            if prev_reading:
                                kilobot.intensity_heading(prev_reading, prev_time_step_x, prev_time_step_y, SQUARE_LENGTH) 
                            
                        if TUMBLING:
                            kilobot.tumble()           
                    
                    pygame.draw.circle(screen, kilobot.status, (kilobot.x, kilobot.y), RADIUS)
                    
                    if radii:
                        pygame.draw.circle(screen, kilobot.detection, (kilobot.x, kilobot.y), DETECT_RADIUS, 2)
            
            pygame.display.flip()
            time_step += 1
            clock.tick(FPS)
            
    pygame.quit()
    
    
    sys.exit()
    