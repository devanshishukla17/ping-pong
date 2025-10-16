import pygame
import time # Import the time module
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True

    while running:
        # Check if the game is over to enable menu input handling
        is_game_over = not engine.game_active

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if is_game_over and event.type == pygame.KEYDOWN:
                # Handle menu selection input when the game is over
                if event.key == pygame.K_3:
                    engine.set_max_score(3)
                    engine.reset_game()
                elif event.key == pygame.K_5:
                    engine.set_max_score(5)
                    engine.reset_game()
                elif event.key == pygame.K_7:
                    engine.set_max_score(7)
                    engine.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False


        # Game Logic (only runs if engine.game_active is True, handled internally by engine.update())
        engine.handle_input()
        engine.update()
        
        # Rendering
        SCREEN.fill(BLACK)
        engine.render(SCREEN)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

