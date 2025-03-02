# World generation
import pygame
from configs import tile_size
from objects import Enemy, Spike, Exit, Coin, Platform

class World:
    def __init__(self, data):
        self.tile_list = []

        # Sprite group for enemy, exit
        self.enemy_group = pygame.sprite.Group()
        self.spike_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()

        # Load images for static background tiles
        dirt_img = pygame.image.load('img/box.png')
        grass_img = pygame.image.load('img/Green.png')
        border_img = pygame.image.load('img/border.png')
        border_img = pygame.transform.scale(border_img, (tile_size, tile_size))
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # if tile == 1:
                #     # Create a dirt tile
                #     img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                #     img_rect = img.get_rect()
                #     img_rect.topleft = (col_count * tile_size, row_count * tile_size)
                #     self.tile_list.append((img, img_rect))
                if tile == 1:
                    # Create boundary walls
                    img = pygame.transform.scale(border_img, (tile_size+2, tile_size+2))
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
                elif tile == 4:
                    # Create Horizontal moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, move_x=1, move_y=0)
                    self.platform_group.add(platform)
                elif tile == 5:
                    # creat Vertical moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, move_x=0, move_y=1)
                    self.platform_group.add(platform)
                elif tile == 6:
                    # Create spikes
                    spike = Spike(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    self.spike_group.add(spike)
                elif tile == 7:
                    # Create coin/fruit
                    # Position it at center of the tile
                    coin = Coin(col_count * tile_size + tile_size // 2, row_count * tile_size + tile_size // 2)
                    self.coin_group.add(coin)
                elif tile == 8:
                    # Create exit
                    exit_obj = Exit(col_count * tile_size, row_count * tile_size - (tile_size//2))
                    self.exit_group.add(exit_obj)
                if tile == 9:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * tile_size, row_count * tile_size)
                    self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
