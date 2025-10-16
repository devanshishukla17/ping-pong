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
    game_over_time = 0 # To store the time when the game ended

    while running:
        # Event handling (only checking for quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game Logic
        engine.handle_input()
        engine.update()
        
        # Rendering
        SCREEN.fill(BLACK)
        engine.render(SCREEN)

        # Game Over Handling
        if not engine.game_active and game_over_time == 0:
            # Game just ended, record the time
            game_over_time = time.time()
        
        # If game over time is recorded, check for the delay
        if game_over_time != 0 and (time.time() - game_over_time) > 3:
            running = False # End the main loop after 3 seconds

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
