# Game Objects

import pygame

class Player:
    def __init__(self, x, y):
        
        # Hold left and right images in list
        self.images_right = []
        self.images_left = []

        # Index and counter to move through images
        self.index = 0
        self.counter = 0

        # images for walking animation
        for i in range(1, 5):
            img = pygame.image.load(f'img/guy{i}.png')
            img = pygame.transform.scale(img, (40, 80)) # Scale image, 40x80
            self.images_right.append(img)
            # flip images for left side movement
            self.images_left.append(pygame.transform.flip(img, True, False))

        # Start with default image facing right
        self.image = self.images_right[self.index]

        # Getting the coordinates for collision detection and drawing
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # Set the movement direction 1 = right, -1 = left, 0 = idle
        self.direction = 0

        # last facing direction (1 = right, -1 = left)
        self.facing = 1

        # Walk spped
        self.speed = 5

        # Vertical velocity (Gravity)
        self.y_vel = 0

        # Flag for jump
        self.jumped = False


    def update(self, world):
        # Set the walk animation speed
        animation_speed = 5

        # Delta x and y coordinates
        dx = 0
        dy = 0

        # Horizontal Movement
        # If player is moving (direction != 0), update animation and delta coordinates
        if self.direction != 0:
            dx = int(self.speed * self.direction)
            self.counter += 1
            # Change frame every animation_speed ticks (adjust this value to speed up or slow down the animation)
            if self.counter > animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]
            self.facing = self.direction
        else:
            # If idle (direction = 0), reset the animation to the first image
            self.index = 0
            if self.facing == 1:
                    self.image = self.images_right[self.index]
            elif self.facing == -1:
                    self.image = self.images_left[self.index]

        
        # Vertical movement and Gravity
        gravity = 1
        self.y_vel += gravity
        if self.y_vel > 10:  # Limit max fall speed
            self.y_vel = 10
        dy += self.y_vel

        # Collision Detection
        # For each tile in the world, adjust dx and dy if a collision would occur.
        for tile in world.tile_list:
            tile_rect = tile[1]
            # Check horizontal collision
            if tile_rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Check vertical collision
            if tile_rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.y_vel > 0:  # align bottom of player with top of tile when falling
                    dy = tile_rect.top - self.rect.bottom
                    self.y_vel = 0
                elif self.y_vel < 0:  # align top of player with bottom of tile when jumping
                    dy = tile_rect.bottom - self.rect.top
                    self.y_vel = 0

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

            
    def draw(self, screen):
        # Draw player at current location with rect(coordinates)
        screen.blit(self.image, self.rect)



