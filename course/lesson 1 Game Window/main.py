import pygame
import config








playing = True
while playing:
    config.frameRate.tick(config.FPS) # get time and frame rate (loop rate)
    config.game_window.fill(config.BLACK)
    
    
    

    
    

        
   
        
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
            
        if event.type == pygame.KEYDOWN:
        
            
            if event.key == pygame.K_ESCAPE: playing = False
            
        
        
            
            
            

    
    pygame.display.update()

pygame.quit()