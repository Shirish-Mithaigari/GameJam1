# Game Objects

import pygame

class Player:
    def __init__(self, x, y):
        # Load the player image 
        self.image = pygame.image.load('img/guy1.png')
        # Scale image
        self.image = pygame.transform.scale(self.image, (40, 80))
        # Getting the coordinates for collision detection and drawing
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Draw the player at the current location with rect(coordinates)
        screen.blit(self.image, self.rect)
