import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60



# Set level editor window to 800x800 using tile_size = 40 and 20 columns
tile_size = 40  
cols = 20
margin = 100
screen_width = tile_size * cols  
screen_height = (tile_size * cols) + margin
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Design')

# Load images from the "images" folder
background_img = pygame.image.load('img/background.png')
# Scale background to fill 800x800
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

border_img = pygame.image.load('img/border.png')
green_img = pygame.image.load('img/green.png')
spirit_img = pygame.image.load('img/Spirit.png')
horizontal_moving_grid_img = pygame.image.load('img/horizontal.png')
vertical_moving_grid_img = pygame.image.load('img/vertical.png')
spikes_img = pygame.image.load('img/spikes.png')
apple_img = pygame.image.load('img/Cherries.png')
exit_door_img = pygame.image.load('img/Exit_door.png')
saveButton_img = pygame.image.load('img/saveButton.png')
loadButton_img = pygame.image.load('img/loadButton.png')
box_img = pygame.image.load('img/box.png')


clicked = False
level = 2

white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

# Create empty 20x20 grid
world_data = []
for row in range(20):
    r = [0] * 20
    world_data.append(r)

# Create boundary
for tile in range(0, 20):
    world_data[19][tile] = 2
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][19] = 1

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_grid():
    for c in range(21):
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

def draw_world():
    for row in range(20):
        for col in range(20):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # Border blocks 
                    img = pygame.transform.scale(border_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    # green blocks
                    img = pygame.transform.scale(green_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                
                if world_data[row][col] == 3:
                    # spirit blocks 
                    img = pygame.transform.scale(spirit_img, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + int(tile_size * 0.25)))
                if world_data[row][col] == 4:
                    # Horizontally moving grid 
                    img = pygame.transform.scale(horizontal_moving_grid_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    # Vertically moving grid 
                    img = pygame.transform.scale(vertical_moving_grid_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    # spikes (40x20)
                    img = pygame.transform.scale(spikes_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                if world_data[row][col] == 7:
                    # Apple (20x20)
                    img = pygame.transform.scale(apple_img, (tile_size // 2, tile_size // 2))
                    screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                if world_data[row][col] == 8:
                    # Exit (40x60)
                    img = pygame.transform.scale(exit_door_img, (tile_size, int(tile_size * 1.5)))
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))

                if world_data[row][col] == 9:
                    # box(40x40)
                    img = pygame.transform.scale(box_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Adjusted button Y-coords so they're fully visible
save_button = Button(screen_width // 2 - 150, screen_height - 80, saveButton_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, loadButton_img)

run = True
while run:
    clock.tick(fps)
    # Fill background and draw the scaled background image
    screen.fill(green)
    screen.blit(background_img, (0, 0))

    # Draw buttons
    if save_button.draw():
        with open(f'level{level}_data', 'wb') as pickle_out:
            pickle.dump(world_data, pickle_out)
    if load_button.draw():
        if path.exists(f'level{level}_data'):
            with open(f'level{level}_data', 'rb') as pickle_in:
                world_data = pickle.load(pickle_in)

    # Draw grid and world
    draw_grid()
    draw_world()

    # Draw text info
    draw_text(f'Level: {level}', font, white, 10, screen_height - 30)
    draw_text('Press UP or DOWN to change level', font, white, 10, screen_height - 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            if x < 20 and y < 20:
                if pygame.mouse.get_pressed()[0]:
                    world_data[y][x] += 1
                    if world_data[y][x] > 9:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2]:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 9
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    pygame.display.update()

pygame.quit()
