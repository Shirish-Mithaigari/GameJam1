# Initialize game
import pygame
import pickle
from os import path
from configs import screen_width, screen_height, fps, blue, white, green, tile_size
from world import World
from objects import Player
from ui import Button

# For sound
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

# Load bgm and sound effects
pygame.mixer.music.load('img/music.wav')  
pygame.mixer.music.play(-1, 0.0, 5000) # Loops indefinitely

jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)

coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)

game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)

# Load Easy and Hard buttons
easy_img = pygame.image.load('img/easy_btn.png')
easy_img = pygame.transform.scale(easy_img, (150, 50))
easy_button = Button((screen_width // 2) - 200, (screen_height // 2) + 50, easy_img)

hard_img = pygame.image.load('img/hard_btn.png')
hard_img = pygame.transform.scale(hard_img, (150, 50))
hard_button = Button((screen_width // 2) + 50, (screen_height // 2) + 50, hard_img)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Platformer")
clock = pygame.time.Clock()

# Set font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Functions
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def load_level(level_num):
    level_data = []
    filename = f"level{level_num}_data"
    if path.exists(filename):
        with open(filename, "rb") as f:
            level_data = pickle.load(f)
    else:
        print(f"{filename} file not found.")
    return level_data


# Load backgorund image
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

# Load coin image 
coin_img = pygame.image.load('img/coin.png')
coin_img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))

# Level management variables
level = 1
max_levels = 7


# Load initial level and world
level_data = load_level(level)
world = World(level_data)



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
score = 0
difficulty = None


while main_menu:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
            run = False

    screen.blit(bg_img, (0, 0))
    draw_text("PIXEL PLATFORMER", font, blue, (screen_width // 2) - 250, (screen_height // 2) - 150)
    # subtext for each difficulty option
    draw_text("Double jump, less gravity, slower enemies", font_score, green, 10, (screen_height // 2))
    draw_text("Higher gravity, fall damage, faster enemies", font_score, (120, 0, 0), (screen_width // 2) - 200, (screen_height // 2) + 110)


    if easy_button.draw(screen):
        difficulty = "easy"
        main_menu = False
    elif hard_button.draw(screen):
        difficulty = "hard"
        main_menu = False
        # Enemy and platform speed for hard mode
        for enemy in world.enemy_group.sprites():
            enemy.speed *= 2
        for platform in world.platform_group.sprites():
            if platform.move_x != 0:
                platform.move_x *= 2
            if platform.move_y != 0:
                platform.move_y *= 2

        

    pygame.display.update()

# If no difficulty was selected default to easy.
if difficulty is None:
    difficulty = "easy"

# Now, create the player with the chosen difficulty
player = Player(50, screen_height - 120, difficulty)

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
        # subtext for each difficulty option
        draw_text("Double jump, less gravity, slower enemies", font_score, green, 10, (screen_height // 2))
        draw_text("Higher gravity, fall damage, faster enemies", font_score, (255, 182, 193), (screen_width // 2) - 200, (screen_height // 2) + 110)
        
        # Check if either button is clicked to set difficulty and start game
        if easy_button.draw(screen):
            difficulty = "easy"
            main_menu = False
        elif hard_button.draw(screen):
            difficulty = "hard"
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
                if not player.jumped and player.jumps_remaining > 0:
                    player.jump()
                    jump_fx.play()
                    player.jumped = True
            else:
                # Only reset the jumped flag when the key is released.
                player.jumped = False

            # Update and draw world, player and enemies if game_over == 0 (playing)
            world.draw(screen)
            player.update(world)
            player.draw(screen)
            world.enemy_group.update(world)
            world.enemy_group.draw(screen)
            world.spike_group.draw(screen)
            world.exit_group.draw(screen)
            world.coin_group.draw(screen)
            world.platform_group.update() 
            world.platform_group.draw(screen)

            # Collision -> player & spikes
            if pygame.sprite.spritecollide(player, world.spike_group, False):
                game_over = -1
                game_over_fx.play()

            # Collision -> player & enemy
            if pygame.sprite.spritecollide(player, world.enemy_group, False):
                game_over = -1
                game_over_fx.play()

            # Collision -> player & exit
            if pygame.sprite.spritecollide(player, world.exit_group, False):
                # Maybe add a reset here? (only resetting score for now)
                score = 0
                # Load next level if available, else win the game.
                level += 1
                if level <= max_levels:
                    # Load next level
                    level_data = load_level(level)
                    world = World(level_data)
                    # Reset player position:
                    player = Player(50, screen_height - 120, difficulty)
                else:
                    game_over = 1

            # Collision -> player & coin
            coins_collected = pygame.sprite.spritecollide(player, world.coin_group, True) # (True removes coin on collision)
            if coins_collected:
                score += len(coins_collected)
                coin_fx.play()

            screen.blit(coin_img, (tile_size - 10, 10))
            draw_text("X" + str(score), font_score, white, tile_size + 12, 4)

        else:
            if game_over == -1:
                draw_text("GAME OVER!", font, blue, (screen_width // 2) - 200, screen_height // 2)
                # Restart same level on death
                if restart_button.draw(screen):
                    level_data = load_level(level)
                    world = World(level_data)
                    player = Player(50, screen_height - 120, difficulty)
                    score = 0
                    game_over = 0
            elif game_over == 1:
                draw_text("YOU WIN!", font, blue, (screen_width // 2) - 200, screen_height // 2)
                # Restarts from level 1 if all completed
                if restart_button.draw(screen):
                    level = 1
                    level_data = load_level(level)
                    world = World(level_data)
                    player = Player(50, screen_height - 120, difficulty)
                    score = 0
                    game_over = 0

    pygame.display.update()

pygame.quit()
