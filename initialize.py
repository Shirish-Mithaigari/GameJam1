# Initialize game
import pygame
import pickle
from os import path
from configs import screen_width, screen_height, fps
from world import World

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Platformer")
clock = pygame.time.Clock()

# Load backgorund image
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

# Load level data from the file 'level1_data'
level_data = []
if path.exists("level1_data"):
    with open("level1_data", "rb") as f:
        level_data = pickle.load(f)
else:
    print("level1_data file not found.")

world = World(level_data)

run = True
while run:
    clock.tick(fps)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw bg
    screen.blit(bg_img, (0,0))

    # Draw world
    world.draw(screen)
    pygame.display.update()

pygame.quit()
