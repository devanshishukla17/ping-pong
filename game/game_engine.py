import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        # Assumes the latest ball.py with robust collision is used
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height) 

        self.player_score = 0
        self.ai_score = 0
        self.max_score = 5  # Default target to win
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 24) # Font for the replay menu
        self.game_active = True
        self.winner = None

    def set_max_score(self, new_max):
        """Sets the new score required to win."""
        self.max_score = new_max

    def reset_game(self):
        """Resets scores, game state, and ball position to start a new game."""
        self.player_score = 0
        self.ai_score = 0
        self.game_active = True
        self.winner = None
        self.ball.reset() # Reset ball position and direction

    def handle_input(self):
        # Only allow paddle input if the game is active
        if self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                # Move up
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                # Move down
                self.player.move(10, self.height)

    def check_game_over(self):
        """Checks if a player has reached the maximum score and sets the winner."""
        if self.player_score >= self.max_score:
            self.game_active = False
            self.winner = "Player"
            return True
        elif self.ai_score >= self.max_score:
            self.game_active = False
            self.winner = "AI"
            return True
        return False

    def update(self):
        # Only run game logic if the game is active
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

            # AI movement logic
            self.ai.auto_track(self.ball, self.height)
            
            # Check for game over after scoring
            self.check_game_over()


    def render(self, screen):
        # Draw paddles and center line
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
        
        # Only draw the ball if the game is active
        if self.game_active:
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width(), 20))


        # Draw Game Over Screen and Replay Menu
        if not self.game_active and self.winner:
            # 1. Winner Message
            message = f"{self.winner} Wins! (First to {self.max_score})"
            winner_surface = self.game_over_font.render(message, True, WHITE)
            text_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(winner_surface, text_rect)

            # 2. Menu Options
            menu_options = [
                ("Best of 3 (Press 3)", 3),
                ("Best of 5 (Press 5)", 5),
                ("Best of 7 (Press 7)", 7),
                ("Exit (Press ESC)", -1)
            ]
            
            y_offset = 50
            for text, key in menu_options:
                menu_surface = self.menu_font.render(text, True, WHITE)
                menu_rect = menu_surface.get_rect(center=(self.width // 2, self.height // 2 + y_offset))
                screen.blit(menu_surface, menu_rect)
                y_offset += 40
