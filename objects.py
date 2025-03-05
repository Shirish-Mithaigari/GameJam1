# Game Objects

import pygame
from configs import tile_size

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, difficulty):
        pygame.sprite.Sprite.__init__(self)
        
        # Hold left and right images in list
        self.images_right = []
        self.images_left = []

        # Index and counter to move through images
        self.index = 0
        self.counter = 0

        # images for walking animation
        for i in range(1, 4):
            img = pygame.image.load(f'img/guy{i}.png')
            img = pygame.transform.scale(img, (40, 80)) # Size modification here
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

        # Flag for in air
        self.in_air = True

        # Set difficulty and jump allowance
        self.difficulty = difficulty
        if difficulty == "easy":
            self.max_jumps = 2
        else:
            self.max_jumps = 1

        # Number of jumps available (reset when player lands)
        self.jumps_remaining = self.max_jumps


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

        # Collision Detection (static tiles)
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
                    self.in_air = False
                    self.jumps_remaining = self.max_jumps # reset remaining jumps
                elif self.y_vel < 0:  # align top of player with bottom of tile when jumping
                    dy = tile_rect.bottom - self.rect.top
                    self.y_vel = 0



        # Moving platform collision
        col_thresh = 15  # Collision Threshold
        for platform in world.platform_group:
            # Check horizontal collision with platform
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Check vertical collision with platform
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # Player's head collides
                if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                    self.y_vel = 0
                    dy = platform.rect.bottom - self.rect.top
                # Player's feet collides
                elif abs((self.rect.bottom) - platform.rect.top) < col_thresh:
                    self.rect.bottom = platform.rect.top
                    self.in_air = False
                    self.jumps_remaining = self.max_jumps # reset remaining jumps
                    dy = 0
                # Move sideways with the platform if it has horizontal movement
                if platform.move_x != 0:
                    self.rect.x += platform.move_direction * platform.move_x


        # Update player position
        self.rect.x += dx
        self.rect.y += dy
    
    def jump(self):
            # If jumps are remaining, perform a jump
            if self.jumps_remaining > 0:
                if self.difficulty == "hard":
                    self.y_vel = -13  # Reduced jump strength in hard mode
                else:
                    self.y_vel = -15  # Normal jump strength in easy mode
                self.jumps_remaining -= 1

    def draw(self, screen):
        # Draw player at current location with rect(coordinates)
        screen.blit(self.image, self.rect)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Load image
        self.image = pygame.image.load('img/Spirit.png')
        # Scale image
        self.image = pygame.transform.scale(self.image, (40, 40)) # Size modification here

        # Get coordinates
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Movement parameters:
        self.move_direction = 1   # 1 = right, -1 = left
        self.speed = 1            # Enemy move speed

    def update(self, world):
        # Calculate delta x
        dx = self.move_direction * self.speed

        can_move = True
        
        # Collision detection for each tile in world
        for tile in world.tile_list:
            tile_rect = tile[1]
            # check horizontal collision
            if tile_rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                can_move = False
                break

        # Ground detection
        # Checking if there is platform under the enemy's moving direction
        if self.move_direction == 1:
            # Check at bottom right corner after moving dx
            check_point = (self.rect.right + dx, self.rect.bottom + 1)
        else:
            # Check at bottom left corner after moving dx
            check_point = (self.rect.left + dx, self.rect.bottom + 1)
        
        ground_found = False
        for tile in world.tile_list:
            if tile[1].collidepoint(check_point):
                ground_found = True
                break

        # Stop movement if no ground ahead
        if not ground_found:
            can_move = False

        
        if not can_move:
            # Reverse direction if can't move ahead
            self.move_direction *= -1
        else:
            # else, update position
            self.rect.x += dx

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('img/spikes.png') # Change image 
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size // 2)) # Size modification here
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load exit/door image 
        self.image = pygame.image.load('img/Exit_door.png')
        self.image = pygame.transform.scale(self.image, (tile_size, int(tile_size * 1.5))) # Size modification here
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load the fruit/coin image
        self.image = pygame.image.load('img/Cherries.png')
        self.image = pygame.transform.scale(self.image, (tile_size // 2, tile_size // 2)) # Size modification here
        self.rect = self.image.get_rect()
        # Position fruit at the center of tile
        self.rect.center = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        # Load platform image 
        self.image = pygame.image.load('img/moving_grid.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size // 2)) # Size modification here
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Movement parameters
        self.move_x = move_x  
        self.move_y = move_y 
        self.move_direction = 1  
        self.move_counter = 0

    def update(self):
        # Update platform position based on movement parameters
        # Move horizontally or vertically based on move_x and move_y
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1

        # Reverse direction after certain distance (50)
        if abs(self.move_counter) >= 50:
            self.move_direction *= -1
            self.move_counter *= -1