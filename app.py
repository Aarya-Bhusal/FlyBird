# Import all the necessary modules
import pygame
from random import randint

# Define some constants
GAME_HEIGHT = 500
GAME_WIDTH = 700
BIRD_HEIGHT = 50
BIRD_WIDTH = 75
PILLAR_WIDTH = 50

# Load all the necessary images
bird = pygame.image.load("assets/images/bird.png")
background = pygame.image.load("assets/images/background.jpg")
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FlyBird")
pygame.display.set_icon(bird)
font = pygame.font.Font(r"assets\fonts\cursive.ttf", 44)

# Create all the necessary buttons and texts for home screen
play_button = pygame.Rect(275, 170, 160, 50)
play_text = font.render("Play", True, (255, 255, 255))
play_text_rect = play_text.get_rect(center=play_button.center)

settings_button = pygame.Rect(275, 245, 160, 50)
settings_text = font.render("Settings", True, (255, 255, 255))
settings_text_rect = settings_text.get_rect(center=settings_button.center)

quit_button = pygame.Rect(275, 320, 160, 50)
quit_text = font.render("Quit", True, (255, 255, 255))
quit_text_rect = quit_text.get_rect(center=quit_button.center)

settings_window_rect = pygame.Rect(75, 50, 550, 400)

difficulty_button = pygame.Rect(150, 120, 400, 75)

music_button = pygame.Rect(150, 220, 400, 75)

quit_settings_button = pygame.Rect(150, 320, 400, 75)

quit_settings_text = font.render("Quit", True, (255, 255, 255))
quit_settings_text_rect = quit_settings_text.get_rect(center=quit_settings_button.center)

# Game variables
running = True
game_screen = False
setting_window = False
difficulties = ["Easy", "Normal", "Hard"]
difficulty = "Normal"
music = True
bird_x, bird_y = 50, 10

# Create a function to display the home page
def show_home(screen, events):
    global running, game_screen, setting_window, difficulty, music, bird, bird_y
    # Show the logo
    bird_logo = pygame.transform.scale(bird, (125,100))
    screen.blit(bird_logo, (450, 200))

    # Play button
    pygame.draw.rect(screen, (96,165,250), play_button, border_radius=10)
    screen.blit(play_text,play_text_rect)

    # Settings button
    pygame.draw.rect(screen, (192,132,252), settings_button, border_radius=10)
    screen.blit(settings_text,settings_text_rect)

    # Quit button
    pygame.draw.rect(screen, (248,113,113), quit_button, border_radius=10)
    screen.blit(quit_text,quit_text_rect)

    # Show the settings windows
    if setting_window:
        pygame.draw.rect(screen, (245,234,214), settings_window_rect, border_radius=20)

        pygame.draw.rect(screen, (96,165,250), difficulty_button, border_radius=10)
        difficulty_text = font.render(f"Difficulty : {difficulty}", True, (255, 255, 255))
        difficulty_text_rect = difficulty_text.get_rect(center=difficulty_button.center)
        screen.blit(difficulty_text, difficulty_text_rect)

        pygame.draw.rect(screen, (192,132,252), music_button, border_radius=10)

        music_text = font.render(f"Music : {"On" if music else "Off"}", True, (255, 255, 255))
        music_text_rect = music_text.get_rect(center=music_button.center)
        screen.blit(music_text, music_text_rect)

        pygame.draw.rect(screen, (248,113,113), quit_settings_button, border_radius=10)
        screen.blit(quit_settings_text, quit_settings_text_rect)

    # Detect events for homw screen
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_button.collidepoint(pygame.mouse.get_pos()) and not setting_window:
                    game_screen = True
                    bird_y = 10
                elif settings_button.collidepoint(pygame.mouse.get_pos()) and not setting_window:
                    setting_window = True
                elif quit_button.collidepoint(pygame.mouse.get_pos()) and not setting_window:
                    running = False
                elif difficulty_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    i = difficulties.index(difficulty)
                    i+=1
                    if i > 2: i = 0
                    difficulty = difficulties[i]
                elif music_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    music = False if music else True
                elif quit_settings_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    setting_window = False

# Create some variables required for game
pillar_y = 100
pillar_height = randint(100, int(70/100 * GAME_HEIGHT))

# Create the main game function
def game(screen, event):
    global bird_x, bird_y, bird, game_screen, pillar_y, pillar_height

    # Draw the bird and create a rectangle for bird to detect collision
    bird_rect = pygame.rect.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
    pygame.draw.rect(screen, (255,255,255), bird_rect)
    bird_img = pygame.transform.scale(bird, (BIRD_WIDTH,BIRD_HEIGHT))
    screen.blit(bird_img, (bird_x, bird_y))

    # Create pillars
    pillar = pygame.Rect(pillar_y, GAME_HEIGHT-pillar_height, PILLAR_WIDTH, pillar_height)
    pygame.draw.rect(screen, (255,255,255), pillar)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_screen = False
            elif event.key == pygame.K_SPACE:
                bird_y -= 100

    # Move the pillars
    pillar_y -= 0.1

    # Create a new pillar if old pillars pass away form screen
    if pillar_y<(0-PILLAR_WIDTH):
        pillar_height = randint(100, int(70/100 * GAME_HEIGHT))
        pillar_y = GAME_WIDTH

# Run the game
while running:
    # Detech different events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Set the background
    screen.blit(background, (0,0))

    # Show the home page
    if not game_screen:
        show_home(screen, events)
    else:
        game(screen, events)
        # Drag the bird down
        bird_y += 0.1

    # Keep updating the game window
    pygame.display.flip()

# Quit the game
pygame.quit()