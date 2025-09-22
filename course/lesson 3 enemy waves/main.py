import pygame
import random
import config
import shipClass
from sprite_groups import enemy_group





#create player object
player = shipClass.Ship('player', 800, 700, 1, 10)

SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_SINGLE_EVENT = pygame.USEREVENT + 2 # for staggered spawns

spawn_interval = 12000 # 12 sec (60000 for 1 min)
pygame.time.set_timer(SPAWN_EVENT, spawn_interval)

wave_count = 1
pending_spawns = 0 # track how many enemies are left in current wave

def spawn_enemy():
    x = random.randint(80, config.SCREEN_WIDTH - 80)
    y = -50 # spawn above screen
    enemy_type = random.choice(['enemy1', 'enemy2', 'enemy3'])
    enemy = shipClass.Ship(enemy_type, x, y, 0.5, 1)
    enemy_group.add(enemy)
    
    if random.randint(1, 2) == 1:
        enemy.flip = True
    else:
        enemy.flip = False




playing = True
while playing:
    config.frameRate.tick(config.FPS) # get time and frame rate (loop rate)
    config.game_window.fill(config.BLACK)
    
    
    

    
    
    player.draw()
    
    
    # update and draw enemies
    for enemy in enemy_group:
        enemy.update_enemy(config.SCREEN_HEIGHT)
        enemy.draw()
        
        
        
   
        
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
            
        if event.type == pygame.KEYDOWN:
        
            
            if event.key == pygame.K_ESCAPE: playing = False
            
        
        
            
            
            
        # _______ Spawn enemy waves ________
        if event.type == SPAWN_EVENT:# 12s
            pending_spawns = wave_count # number to spawn this wave
            wave_count += 1             # next wave is 1 larger
            spawn_enemy()
            pending_spawns -= 1         # we spawned one so less pending now
            if pending_spawns > 0:
                pygame.time.set_timer(SPAWN_SINGLE_EVENT, 1000) # 100ms delay between enemies
                
        # _____ Stagger enemy spawns _____\
        if event.type == SPAWN_SINGLE_EVENT:
            spawn_enemy()               # create enemy
            pending_spawns -= 1
            if pending_spawns <= 0:
                pygame.time.set_timer(SPAWN_SINGLE_EVENT, 0) # stop stagger timer
    
    
    
    
    
    pygame.display.update()

pygame.quit()