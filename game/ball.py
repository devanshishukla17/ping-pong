import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top/bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        
        # Check collision with Player Paddle (moving left, velocity_x < 0)
        if self.velocity_x < 0 and ball_rect.colliderect(player.rect()):
            # Push ball out of the paddle to prevent sticking
            self.x = player.x + player.width 
            self.velocity_x *= -1

        # Check collision with AI Paddle (moving right, velocity_x > 0)
        elif self.velocity_x > 0 and ball_rect.colliderect(ai.rect()):
            # Push ball out of the paddle to prevent sticking
            self.x = ai.x - self.width
            self.velocity_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
