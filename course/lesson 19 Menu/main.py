import pygame # type: ignore
import os
from pygame import mixer # type: ignore
import random


import config
import menu
import shipClass
from spaceObjects import Asteroid, BlackHole
from projectiles import LaserLine
from sprite_groups import (
    enemy_group, 
    player_lasers,  
    heavyLaser_group, 
    rockets_group, 
    asteroid_group, 
    enemy_beam_group, 
    explosion_group,
    blackholes_group,
    enemy_lasers)






# music for game
def play_music(song_path):
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.set_volume(0.6) # main song volume
        pygame.mixer.music.play()# play the song without looping
        print(f"Playing music: {song_path}") # for song print and debug
    except Exception as e:
        print(f"Error loading music: {e}")
        
current_song = 'song1' # Track the current song
is_paused = False # Track if the game music is paused or not
song1_path = os.path.join('audio', 'Dark Techno  EBM Industrial Type Beat WITCHTRIPPER Background Music [rQBNt7jWFAQ].mp3')

# Play initial song on start
play_music(song1_path)



# background y scroll
scroll_y = 0

def draw_scrolling_bg(surface, background_list, state, speed=3):
    screen_width = surface.get_width()
    screen_height = surface.get_height()
    state['y'] += speed
    
    num_images = len(background_list)# keep track of our list of images to loop
    total_height = screen_height * num_images # get the total height of all pictures
    
    if state['y'] >= total_height:
        state['y'] -= total_height
        
    # add first image again to loop seamlessly
    imgs_to_draw =background_list + [background_list[0]] 
    
    for i, img in enumerate(imgs_to_draw):
        y_pos = state['y'] - i * screen_height # preserve original scroll direction
        
        if y_pos < screen_height and y_pos + screen_height > 0:
            # create rectangle for screen size to check if we should draw img or not / do not draw all images only the one on screen
            source_rect = pygame.Rect(0, 0, screen_width, screen_height) 
            
            if y_pos < 0:
                source_rect.top = -y_pos
                source_rect.height = screen_height + y_pos
            elif y_pos + screen_height > screen_height:
                source_rect.height = screen_height - y_pos
                
            surface.blit(img, (0, max(y_pos, 0)), area=source_rect)
            
            
    




def spawn_enemy():
    x = random.randint(80, config.SCREEN_WIDTH - 80)
    y = -50 # spawn above screen
    
    enemy_type = random.choices(
        ['enemy1', 'enemy2', 'enemy3', 'enemy4','enemy5'],
        weights=[3, 3, 3, 2, 1],# enemy 1,2,3 is 3 times more likley to spawn
        k=1
    )[0]

    
    enemy = shipClass.Ship(enemy_type, x, y, 0.5, 1)
    enemy_group.add(enemy)
    
    enemy.flip = random.choice([True, False])
    
    
    
    
def start_game():
    # --- Ensure global sprite groups exist and are fresh (use .empty() to keep same Group objects) ---
    enemy_group.empty()
    asteroid_group.empty()
    rockets_group.empty()
    explosion_group.empty()
    heavyLaser_group.empty()
    blackholes_group.empty()
    player_lasers.empty()
    enemy_beam_group.empty()
    enemy_lasers.empty()

    # --- Create fresh player & UI objects for this run ---
    player = shipClass.Ship('player', 950, 750, 1, 10)

    # ensure player's projectile container is a Group and linked
    player.lasers = player_lasers  # MUST be a pygame.sprite.Group()
    player.asteroid_group = asteroid_group
    player.enemy_group = enemy_group

    # single LaserLine instance for this run, linked to the fresh groups
    player_beam = LaserLine(player, is_player=True)
    player_beam.asteroid_group = asteroid_group
    player_beam.enemy_group = enemy_group
    player_beam.blackholes_group = blackholes_group

    health_bar = shipClass.HealthBar(30, 970, player.health, player.health)
    shield_bar = shipClass.HealthBar(30, 990, player.shield, player.shield)

    # reset input flags so stale state doesn't persist
    config.moving_left = config.moving_right = config.moving_up = config.moving_down = False
    config.shooting = config.heavy_shooting = config.rocket = config.laserLine_fire = False
    config.score = 0

    # clear pending events (prevents leftover QUIT/KEYUP from earlier)
    pygame.event.clear()

    # Game state variables
    playing = True
    scroll_y = 0
    wave_count = 1
    pending_spawns = 0

    # Spawn events (use local event ids so no conflict)
    SPAWN_EVENT = pygame.USEREVENT + 1
    SPAWN_SINGLE_EVENT = pygame.USEREVENT + 2
    spawn_interval = 12000 # 12 sec (60000 for 1 min)
    pygame.time.set_timer(SPAWN_EVENT, spawn_interval)


    while playing:
        config.frameRate.tick(config.FPS)
        config.game_window.fill(config.BLACK)

        # --- Check death ---
        if player.health <= 0:
            print(f"You died, health={player.health}, score={config.score}")
            playing = False
            break

        # --- Background ---
        draw_scrolling_bg(config.game_window, config.background_list, config.scroll_state, speed=2)

        # --- Blackholes ---
        if random.random() < 0.00125:
            bh = BlackHole()
            blackholes_group.add(bh)
        groups_map = {
            'player': player,
            'enemy_group': enemy_group,
            'asteroids': asteroid_group,
            'player_lasers': player_lasers,
            'enemy_lasers': enemy_lasers,
            'rockets_group': rockets_group,
        }
        for bh in list(blackholes_group):
            bh.update(groups_map)
            bh.draw(config.game_window)

        # --- Explosions ---
        explosion_group.update()
        for exp in explosion_group:
            exp.draw(config.game_window)

        # --- Rockets ---
        for rocket in rockets_group:
            rocket.update()
            rocket.draw()
        if config.rocket:
            player.shoot_rocket(enemy_group, rockets_group, asteroid_group)

        # --- Asteroids ---
        if random.random() < 0.005:
            x = random.randint(50, config.SCREEN_WIDTH - 50)
            asteroid_group.add(Asteroid(x, -50, scale=1.0, health=20))
        for asteroid in asteroid_group:
            asteroid.update(asteroid_group, player)
            asteroid.draw(config.game_window)

        # --- Enemies ---
        for enemy in enemy_group:
            enemy.update_enemy(config.SCREEN_HEIGHT)
            enemy.draw()
            enemy.update_lasers()
            enemy.update(player)
            enemy.ai_shoot(player, enemy_group, asteroid_group)
            enemy.ai_shoot_heavy(player, enemy_group, asteroid_group)
            enemy.ai_shoot_rocket(player, rockets_group, asteroid_group)

            if enemy.character_type == "enemy4":
                enemy.ai_shoot_laserline(player, asteroid_group, enemy_beam_group, blackholes_group)
            if enemy.character_type == "enemy5":
                enemy.ai_shoot_enemy5(player, enemy_group, asteroid_group)

        # --- Enemy Laserlines ---
        for beam in enemy_beam_group:
            beam.update(asteroid_group, enemy_group, player, blackholes_group)
            beam.draw(config.game_window)

        # --- Player Lasers ---
        for laser in player_lasers:
            laser.update()
            laser.draw()
        if config.shooting:
            player.shoot_laser(target_player=player, target_enemy_group=enemy_group, asteroid_group=asteroid_group)
        player.update_lasers()

        # --- Player LaserLine ---
        player_beam.trigger(config.laserLine_fire)
        player_beam.update(asteroid_group, enemy_group, player, blackholes_group)
        player_beam.draw(config.game_window)

        # --- Heavy Lasers ---
        heavyLaser_group.update()
        heavyLaser_group.draw(config.game_window)
        if getattr(config, "heavy_shooting", False):
            player.shoot_heavy(player, enemy_group, asteroid_group)

        # --- Player Update / Draw ---
        player.draw()
        player.update(player)
        player.movement(config.moving_left, config.moving_right, config.moving_up, config.moving_down)

        # --- UI ---
        health_bar.draw(player.health, Shield=False)
    
        menu.drawText(f'Health:', config.font, config.WHITE, 10, 965)

        shield_bar.draw(player.shield, Shield=True)
        
        menu.drawText(f'Shield:', config.font, config.WHITE, 10, 985)

        menu.drawText(f'Score: {config.score}', config.font, config.CAYAN, 10, 1005)

        
        menu.drawText(f'Wave: {wave_count}', config.font, config.RED, 10, 1045)

        # --- Music Logic ---
        if not getattr(config, "is_paused", False):
            if not pygame.mixer.music.get_busy():
                play_music(song1_path)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                return "exit"

            # Key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: config.moving_left = True
                if event.key == pygame.K_RIGHT: config.moving_right = True
                if event.key == pygame.K_UP: config.moving_up = True
                if event.key == pygame.K_DOWN: config.moving_down = True
                if event.key == pygame.K_a: config.shooting = True
                if event.key == pygame.K_d: config.heavy_shooting = True
                if event.key == pygame.K_s: config.rocket = True
                if event.key == pygame.K_w: config.laserLine_fire = True
                if event.key == pygame.K_ESCAPE:
                    playing = False
                    break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: config.moving_left = False
                if event.key == pygame.K_RIGHT: config.moving_right = False
                if event.key == pygame.K_UP: config.moving_up = False
                if event.key == pygame.K_DOWN: config.moving_down = False
                if event.key == pygame.K_a: config.shooting = False
                if event.key == pygame.K_d: config.heavy_shooting = False
                if event.key == pygame.K_s: config.rocket = False
                if event.key == pygame.K_w: config.laserLine_fire = False

            # --- Spawn Events ---
            if event.type == SPAWN_EVENT:
                pending_spawns = wave_count
                wave_count += 1
                spawn_enemy()
                pending_spawns -= 1
                if pending_spawns > 0:
                    pygame.time.set_timer(SPAWN_SINGLE_EVENT, 1000)

            if event.type == SPAWN_SINGLE_EVENT:
                spawn_enemy()
                pending_spawns -= 1
                if pending_spawns <= 0:
                    pygame.time.set_timer(SPAWN_SINGLE_EVENT, 0)

        pygame.display.update()

    return "menu"


# --- Main Loop Controller ---
game_state = "menu"
while game_state != "exit":
    if game_state == "menu":
        game_state = menu.menu_screen()
    if game_state == "play":
        game_state = start_game()

pygame.quit()