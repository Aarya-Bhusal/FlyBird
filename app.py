# Import all the necessary modules
import pygame
from random import randint

# Define some constants
GAME_HEIGHT = 500
GAME_WIDTH = 700
BIRD_HEIGHT = 50
BIRD_WIDTH = 75
PILLAR_WIDTH = 50
VERTICAL_PILLAR_GAP = 200
FONT_SIZE = 44

# Load all the necessary images
bird = pygame.image.load("assets/images/bird.png")
background = pygame.image.load("assets/images/background.jpg")
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FlyBird")
pygame.display.set_icon(bird)
font = pygame.font.Font("assets/fonts/cursive.ttf", FONT_SIZE)
score_font = pygame.font.Font(None, 30)
game_over_msg_font = pygame.font.Font("assets/fonts/cursive.ttf", 30)

# Create all the necessary buttons and texts
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

gameover_text = font.render("Game Over!", True, (255,77,77))
gameover_msg_text1 = game_over_msg_font.render("Press R to replay", True, (96,165,250))
gameover_msg_text2 = game_over_msg_font.render("Press Esc to quit", True, (96,165,250))

# Game variables
running = True
game_screen = False
setting_window = False
difficulties = ["Easy", "Normal", "Hard"]
difficulty = "Normal"
music = True
pillars = [
    (100, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
    (400, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
    (700, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)))
        ]
game_over = False
bird_x, bird_y = 100+PILLAR_WIDTH, 10
score = 0
game_speed = 0.08
jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")
gameover_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")

# Create a function to display the home page
def show_home(screen, events):
    global running, game_screen, setting_window, difficulty, music, bird, bird_y, game_over, game_speed, score, gameover_msg_text, pillars

    # Play the music if music is on
    if music:
        pygame.mixer.music.unpause()
    
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

    # Show the high score
    try:
        with open("assets/highest_score.txt", "r+") as file:
            highest_score = file.read()
            if highest_score == '' : highest_score = 0
            else: highest_score = int(highest_score)
        highest_score_text = score_font.render(f"Highest Score : {highest_score}", True, (255,255,255))
        screen.blit(highest_score_text, (5,5))
    except Exception as e:
        print("Error reading high socre.")

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
                    game_over = False
                    score = 0
                    pillars = [
                            (100, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
                            (400, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
                            (700, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)))
                            ]
                    if music:
                        pygame.mixer.music.unpause()
                elif settings_button.collidepoint(pygame.mouse.get_pos()) and not setting_window:
                    setting_window = True
                elif quit_button.collidepoint(pygame.mouse.get_pos()) and not setting_window:
                    running = False
                elif difficulty_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    i = difficulties.index(difficulty)
                    i+=1
                    if i > 2: i = 0
                    difficulty = difficulties[i]
                    if difficulty == "Easy":
                        game_speed = 0.06
                    elif difficulty == "Normal":
                        game_speed = 0.08
                    else:
                        game_speed = 0.1
                elif music_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    music = False if music else True
                    if music:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif quit_settings_button.collidepoint(pygame.mouse.get_pos()) and setting_window:
                    setting_window = False

# Create the main game function
def game(screen, event):
    global bird_x, bird_y, bird, game_screen, pillars, game_over, score, game_speed

    # Draw the bird and create a rectangle for bird to detect collision
    bird_rect = pygame.rect.Rect(bird_x+10, bird_y+10, BIRD_WIDTH-25, BIRD_HEIGHT-20)
    bird_img = pygame.transform.scale(bird, (BIRD_WIDTH,BIRD_HEIGHT))
    screen.blit(bird_img, (bird_x, bird_y))

    # Draw pillars
    for pillar in pillars:
        pillar_x, pillar_height, pillar_color = pillar

        pillar_rect = pygame.Rect(pillar_x, GAME_HEIGHT-pillar_height, PILLAR_WIDTH, pillar_height)
        pygame.draw.rect(screen, pillar_color, pillar_rect)

        up_side_down_pillar = pygame.Rect(pillar_x, 0, PILLAR_WIDTH, (GAME_HEIGHT-pillar_height)-VERTICAL_PILLAR_GAP)
        pygame.draw.rect(screen, pillar_color, up_side_down_pillar)

    # Show Score
    score_text = score_font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (5,5))

    # Move the bird, pillars and detect colision
    if not game_over: 
        # Drag the bird down
        bird_y += game_speed*1.5

        for index, pillar in enumerate(pillars):
            #Move pillars
            pillar_x, pillar_height, pillar_color = pillar
            pillar_x -= game_speed
            if pillar_x<(0-PILLAR_WIDTH):
                score+=1
                # Increase the game speed gradually
                if score%20 == 0:
                    score += 0.1
                pillar_x = pillars[index-1][0]+300
                pillar_height = randint(100, int(70/100 * GAME_HEIGHT))
                pillar_color = (randint(0,255),randint(0,255),randint(0,255))
            pillars[index] = (pillar_x, pillar_height, pillar_color)
        
            #Detect Collision
            pillar_rect = pygame.Rect(pillar_x, GAME_HEIGHT-pillar_height, PILLAR_WIDTH, pillar_height)
            up_side_down_pillar_rect = pygame.Rect(pillar_x, 0, PILLAR_WIDTH, (GAME_HEIGHT-pillar_height)-VERTICAL_PILLAR_GAP)
            if pillar_rect.colliderect(bird_rect) or up_side_down_pillar_rect.colliderect(bird_rect):
                pygame.mixer.music.pause()
                gameover_sound.play()
                game_over = True

        # Check if the bird is out of screen:
        if bird_y>GAME_HEIGHT or bird_y<0:
            pygame.mixer.music.pause()
            gameover_sound.play()
            game_over = True
    else:
        screen.blit(gameover_text, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//4))
        screen.blit(gameover_msg_text1, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//2.5))
        screen.blit(gameover_msg_text2, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//2))
        try:
            with open("assets/highest_score.txt", "r+") as file:
                highest_score = file.read()
                if highest_score  == '':
                    highest_score = 0
                if score>int(highest_score):
                    file.seek(0)
                    file.truncate(0)
                    file.write(str(score))
        except Exception as e:
            print(e)

    # Detect user events
    for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_screen = False
                    game_over = True

                elif event.key == pygame.K_SPACE and not game_over:
                    jump_sound.play()
                    bird_y -= 85
                elif event.key == pygame.K_r and game_over:
                    game_over = False
                    bird_y = 10
                    score = 0
                    pillars = [
                            (100, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
                            (400, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255))),
                            (700, randint(0, int(70/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)))
                            ]

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

    # Keep updating the game window
    pygame.display.flip()

# Quit the game
pygame.quit()