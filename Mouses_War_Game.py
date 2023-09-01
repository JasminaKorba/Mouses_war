# Cuberto
# Toys Icons Set
# The images and icons from this Set are free for use.
# Please refer to our site http://www.cuberto.ru
# license: Freeware
# link: https://www.fontspace.com/feasibly-single-line-font-f90749

import pygame, random

pygame.init()

# Set a dispaly_surface
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mouses war")
icon = pygame.image.load("window_icon.png")
pygame.display.set_icon(icon)

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Game values
MOUSE_START_VELOCITY = 2
MOUSE_ACCELERATION = 0.5
PLAYER_START_LIVES = 10
player_lives = PLAYER_START_LIVES
score = 0
# ----Mouse movements-----
mouse_velocity = MOUSE_START_VELOCITY
mouse_dx = random.choice([-1, 1])
mouse_dy = random.choice([-1, 1])

# Import fonts and set texts
introductory_font = pygame.font.Font("font2.otf", 110)
introductory_text = introductory_font.render("Mouse vs mouse", True, (255, 229, 204))
introductory_rect = introductory_text.get_rect()
introductory_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

custom_font = pygame.font.Font("font2.otf", 55)
score_text = custom_font.render(f"Score: {score}", True, (255, 229, 204))
score_rect = score_text.get_rect()
score_rect.center = (WINDOW_WIDTH // 4, 60)

player_lives_text = custom_font.render(f"Lives: {player_lives}", True, (255, 229, 204))
player_lives_rect = player_lives_text.get_rect()
player_lives_rect.center = (WINDOW_WIDTH // 4 * 3, 60)

game_over_text = custom_font.render("GAME OVER", True, (255, 229, 204))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = custom_font.render(
    "Press any key to play again...", True, (255, 229, 204)
)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, 550)

# Import the images
background = pygame.image.load("background.jfif")

mouse_img = pygame.image.load("mouse_lvl1.png")
mouse_rect = mouse_img.get_rect()
mouse_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Import soundtrack
pygame.mixer.music.load(
    "background_sound_violin.mp3",
)
hit_sound = pygame.mixer.Sound("mouse2.wav")
miss_sound = pygame.mixer.Sound("miss2.wav")

# Set introducory display
display_surface.blit(introductory_text, introductory_rect)
pygame.display.update()
pygame.time.delay(3000)

# Main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]
            # The mouse was hited
            if mouse_rect.collidepoint(click_x, click_y):
                rotate_img = pygame.transform.rotate(mouse_img, 90)
                mouse_img = rotate_img
                hit_sound.play()
                score += 1
                mouse_velocity += MOUSE_ACCELERATION
                # Move mouse in a new direction
                previous_mouse_dx = mouse_dx
                previous_mouse_dy = mouse_dy
                while previous_mouse_dx == mouse_dx and previous_mouse_dy == mouse_dy:
                    mouse_dx = random.choice([-1, 1])
            # We missed the mouse
            else:
                miss_sound.play()
                player_lives -= 1

    # Move the mouse
    mouse_rect.x += mouse_dx * mouse_velocity
    mouse_rect.y += mouse_dy * mouse_velocity

    # Bounce the mouse off the edges of the display
    if mouse_rect.x <= 0 and mouse_dx <= 0:
        mouse_dx *= -1
    if mouse_rect.x >= (WINDOW_WIDTH - 128) and mouse_dx >= 0:
        mouse_dx *= -1
    if mouse_rect.y <= 0 and mouse_dy <= 0:
        mouse_dy *= -1
    if mouse_rect.y >= (WINDOW_HEIGHT - 128) and mouse_dy >= 0:
        mouse_dy *= -1

    # Update HUD
    score_text = custom_font.render(f"Score: {score}", True, (255, 229, 154))
    player_lives_text = custom_font.render(
        f"Lives: {player_lives}", True, (255, 229, 154)
    )

    # Check if GAME OVER
    if player_lives == 0:
        display_surface.blit(player_lives_text, player_lives_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Puse the game until player clicks then restet game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            # The player wants to play again or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    player_lives = PLAYER_START_LIVES
                    score = 0

                    mouse_velocity = MOUSE_START_VELOCITY
                    mouse_dx = random.choice([-1, 1])
                    mouse_dy = random.choice([-1, 1])

                    pygame.mixer.music.play()
                    is_paused = False

                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Blit background, HUD and assets to the display surface
    display_surface.blit(background, (0, 0))

    display_surface.blit(score_text, score_rect)
    display_surface.blit(player_lives_text, player_lives_rect)

    display_surface.blit(mouse_img, mouse_rect)

    # Update display surface and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
