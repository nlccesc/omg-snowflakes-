import pygame
import random
import csv
from snowflake import Snowflake

# Initialize Pygame and the screen
pygame.init()
screen = pygame.display.set_mode((1600, 1200))

# Load and scale the snowflake image
snowflake_image = pygame.image.load('snowflake.png')
snowflake_image = pygame.transform.scale(snowflake_image, (80, 80))

# Create a list of snowflakes with unique IDs
snowflakes = [Snowflake(random.randint(0, 1600), 0, random.uniform(0.5, 1.0), random.uniform(-0.5, 0.5), i) for i in range(200)]

# Open a CSV file to store the data
csv_file = open('snowflake_data.csv', mode='w', newline='')
writer = csv.writer(csv_file)
writer.writerow(['Snowflake ID', 'X Position', 'Y Position', 'State'])

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
            # Write data for each snowflake to the CSV file
            writer.writerow([snowflake.snowflake_id, snowflake.x, snowflake.y, snowflake.state])

    snowflakes = [s for s in snowflakes if s.state != "disintegrated"]

    pygame.display.flip()

# Close the CSV file when the program is closed
csv_file.close()
pygame.quit()
