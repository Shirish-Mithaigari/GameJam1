# Initialize game
import pygame
import pickle
from os import path
from configs import screen_width, screen_height, fps, blue
from world import World
from objects import Player
from ui import Button

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

# Create restart button
restart_img = pygame.image.load('img/restart_btn.png')
restart_img = pygame.transform.scale(restart_img, (150, 50))  # Button size
restart_button = Button((screen_width // 2) - 75, (screen_height // 2) + 100, restart_img) # BUtton pos

# Create start button
start_img = pygame.image.load('img/start_btn.png')
start_img = pygame.transform.scale(start_img, (150, 50)) # Button size
start_button = Button((screen_width // 2) - 75, (screen_height // 2) + 100 , start_img) # Button pos

# Initialize game variables
game_over = 0
main_menu = True

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw bg
    screen.blit(bg_img, (0,0))

    # Main menu
    if main_menu:
        draw_text("PIXEL PLATFORMER", font, blue, (screen_width // 2) - 250, (screen_height // 2) - 150)
        if start_button.draw(screen):
            main_menu = False  

    
    else:

        # Update player based on key inputs (when game_over = 0) 
        if game_over == 0:
        
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

            # Update and draw world, player and enemies if game_over == 0 (playing)
            world.draw(screen)
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


        else:
            if game_over == -1:
                draw_text("GAME OVER!", font, blue, (screen_width // 2) - 200, screen_height // 2)

            elif game_over == 1:
                draw_text("YOU WIN!", font, blue, (screen_width // 2) - 200, screen_height // 2)
                # Add transition to next level in next update

            # Draw restart button and check if it's clicked.
            if restart_button.draw(screen):
                # Reset level (Player and game_over for now, add other objects)
                player = Player(50, screen_height - 120)
                game_over = 0
            

    pygame.display.update()

pygame.quit()
