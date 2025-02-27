# World generation
import pygame
from configs import tile_size
from objects import Enemy

class World:
    def __init__(self, data):
        self.tile_list = []

        # Sprite group for enemy
        self.enemy_group = pygame.sprite.Group()

        # Load images for static background tiles
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    # Create a dirt tile
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * tile_size, row_count * tile_size)
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    # Create a grass tile
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * tile_size, row_count * tile_size)
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    # Create an enemy
                    enemy = Enemy(col_count * tile_size, row_count * tile_size) # Adjust y offset if needed (currently not required)
                    self.enemy_group.add(enemy)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
