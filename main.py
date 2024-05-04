import pygame
import random
from snowflake import Snowflake

# Initialize Pygame and the screen
pygame.init()
screen = pygame.display.set_mode((1600, 1200))

# Load the snowflake image
snowflake_image = pygame.image.load('snowflake.png')
snowflake_image = pygame.transform.scale(snowflake_image, (80, 80))

# Create a list of snowflakes
snowflakes = [Snowflake(random.randint(0, 1600), 0, random.uniform(0.5, 1.0), random.uniform(-0.5, 0.5)) for _ in range(200)]

# Function to summarize and print snowflake data
def summarize_snowflakes(snowflakes):
    # Example: print the average position and count of snowflakes
    avg_x = sum(s.x for s in snowflakes) / len(snowflakes)
    avg_y = sum(s.y for s in snowflakes) / len(snowflakes)
    print(f"Average Position: ({avg_x}, {avg_y}), Count: {len(snowflakes)}")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for snowflake in snowflakes:
        snowflake.fall()
        if snowflake.y >= 1200:
            snowflake.state = "disintegrating"
        if snowflake.state != "disintegrated":
            snowflake.draw(screen, snowflake_image)

    snowflakes = [s for s in snowflakes if s.state != "disintegrated"]
    summarize_snowflakes(snowflakes)  # Summarize and print data every loop

    pygame.display.flip()

pygame.quit()
