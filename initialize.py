# Initialize game
import pygame
import pickle
from os import path
from configs import screen_width, screen_height, fps, white, blue
from world import World
from objects import Player

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Platformer")
clock = pygame.time.Clock()

# Set font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Load backgorund image
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

# Load level data from the file 'level5_data'
level_data = []
if path.exists("level5_data"):
    with open("level5_data", "rb") as f:
        level_data = pickle.load(f)
else:
    print("level5_data file not found.")

world = World(level_data)

# Create player at (50, screen_height - 120) :- {player character height(80) + Tile height(40) = 120)}
player = Player(50, screen_height - 120)

game_over = 0

run = True
while run:
    clock.tick(fps)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update player based on key inputs 
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        player.direction = -1
    elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        player.direction = 1
    else:
        player.direction = 0
    if keys[pygame.K_UP]:
        if not player.jumped:
            player.y_vel = -15  # Jump strength 
            player.jumped = True
    else:
        # Reset jump flag when jump key is released.
        player.jumped = False


    # Draw bg
    screen.blit(bg_img, (0,0))

    # Draw world
    world.draw(screen)

    # Update and draw player and enemies if game_over == 0 (playing)
    if game_over == 0:
        player.update(world)
        player.draw(screen)
        world.enemy_group.update(world)
        world.enemy_group.draw(screen)
        world.spike_group.draw(screen)


    # Collision -> player & spikes
    if pygame.sprite.spritecollide(player, world.spike_group, False):
        game_over = -1

    # Collision -> player & enemy
    if pygame.sprite.spritecollide(player, world.enemy_group, False):
        game_over = -1


    if game_over == -1:
        draw_text("GAME OVER!", font, blue, (screen_width // 2) - 200, screen_height // 2)

    elif game_over == 1:
        draw_text("YOU WIN!", font, blue, (screen_width // 2) - 200, screen_height // 2)
        # Add transition to next level in next update



    pygame.display.update()

pygame.quit()
