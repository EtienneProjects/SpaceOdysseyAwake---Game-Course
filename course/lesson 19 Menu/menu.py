import pygame # type: ignore
import os
import config

# --- Menu Setup ---
menu_images = []
for i in range(5): #flash 2 images in folder
    menu_bg = pygame.image.load(os.path.join(f'img/menu/{i}.png')).convert()  # your menu background image
    menu_bg = pygame.transform.scale(menu_bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    menu_images.append(menu_bg)
button_font = pygame.font.SysFont(None, 70)

# Helper function to create buttons
def draw_button(text, x, y, width, height, inactive_col, active_col):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)
    color = active_col if rect.collidepoint(mouse) else inactive_col
    pygame.draw.rect(config.game_window, color, rect, border_radius=10)

    txt_surface = button_font.render(text, True, config.WHITE)
    text_rect = txt_surface.get_rect(center=(x + width // 2, y + height // 2))
    config.game_window.blit(txt_surface, text_rect)

    if rect.collidepoint(mouse) and click[0] == 1:
        return True
    return False




def menu_screen():
    """Draws and handles main menu"""
    in_menu = True
    global is_paused

    idx = 0  # index of current menu image
    last_switch = pygame.time.get_ticks()
    switch_interval = 1000  # ms between images

    while in_menu:
        now = pygame.time.get_ticks()
        if now - last_switch >= switch_interval:
            idx = (idx + 1) % len(menu_images)  # loop to next image
            last_switch = now

        # draw current image
        config.game_window.blit(menu_images[idx], (0, 0))

        # --- Draw buttons ---
        play_pressed = draw_button("Play", 800, 50, 350, 100, (0, 80, 0), (0, 200, 0))
        sound_pressed = draw_button("Sound", 400, 50, 350, 100, (0, 80, 80), (0, 200, 200))
        exit_pressed = draw_button("Exit", 1200, 50, 350, 100, (80, 0, 0), (255, 60, 60))


        drawText(f'Score: {config.score}', config.fontLarge, config.CAYAN, 870, 180)



        # Handle actions
        if play_pressed:
            return "play"
        if sound_pressed:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                is_paused = True
            else:
                pygame.mixer.music.unpause()
                is_paused = False
        if exit_pressed:
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        config.frameRate.tick(30)




# drawa text for ui
def drawText(text, font, text_col, text_x, text_y):
    img = font.render(text, True, text_col)
    config.game_window.blit(img, (text_x, text_y))