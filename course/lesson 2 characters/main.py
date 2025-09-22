import pygame
import config
import shipClass






#create player object
player = shipClass.Ship('player', 800, 700, 1, 10)





playing = True
while playing:
    config.frameRate.tick(config.FPS) # get time and frame rate (loop rate)
    config.game_window.fill(config.BLACK)
    
    
    

    
    
    player.draw()
    
 
   
        
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
            
        if event.type == pygame.KEYDOWN:
        
            
            if event.key == pygame.K_ESCAPE: playing = False
            
        
        
            
            
            

    
    pygame.display.update()

pygame.quit()