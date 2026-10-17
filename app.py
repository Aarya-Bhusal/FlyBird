# Import all the necessary modules
import pygame

# Define some constants
GAME_HEIGHT = 400
GAME_WIDTH = 600

# Load all the necessary images
bird = pygame.image.load("assets/images/bird.png")
background = pygame.image.load("assets/images/background.jpg")

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FlyBird")
pygame.display.set_icon(bird)

# Run the game
running = True
while running:
    # Detech different events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Set the background
    screen.blit(background, (0,0))

    # Keep updating the game window
    pygame.display.flip()

# Quit the game
pygame.quit()