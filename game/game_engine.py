import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
MAX_SCORE = 5

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        # Assuming ball.py was updated with the collision fix logic from the previous step
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height) 

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.game_active = True
        self.winner = None

    def handle_input(self):
        # Only allow input if the game is active
        if self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def check_game_over(self):
        """Checks if a player has reached the maximum score and sets the winner."""
        if self.player_score >= MAX_SCORE:
            self.game_active = False
            self.winner = "Player"
            return True
        elif self.ai_score >= MAX_SCORE:
            self.game_active = False
            self.winner = "AI"
            return True
        return False

    def update(self):
        if self.game_active:
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            # Scoring logic
            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)
            
            # Check for game over after scoring
            self.check_game_over()


    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        
        # Only draw the ball if the game is active
        if self.game_active:
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4 - player_text.get_width(), 20))


        # Draw Game Over Screen if the game is over
        if not self.game_active and self.winner:
            message = f"{self.winner} Wins!"
            winner_surface = self.game_over_font.render(message, True, WHITE)
            
            # Center the text
            text_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(winner_surface, text_rect)
