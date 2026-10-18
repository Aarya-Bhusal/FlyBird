# Import all the necessary modules
import pygame
from random import randint
from game_resources import *
import json

# Define some constants
GAME_HEIGHT = 500
GAME_WIDTH = 700
BIRD_HEIGHT = 50
BIRD_WIDTH = 75
PILLAR_WIDTH = 50
VERTICAL_PILLAR_GAP = 200
FONT_SIZE = 44
FRAME_RATE = 60
BACKGROUND = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))
COIN = pygame.transform.scale(coin, (50,50))

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
pygame.display.set_caption("FlyBird")
pygame.display.set_icon(bird)
font = pygame.font.Font("assets/fonts/cursive.ttf", FONT_SIZE)
in_game_variable_font = pygame.font.Font(None, 30)

# Create the game Class
class Game:
    def __init__(self):
        # Game variables
        self.running = True
        self.game_screen = False
        self.setting_window = False
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.difficulty = "Normal"
        self.difficulty_speed = {
            "Easy": 2,
            "Normal": 3,
            "Hard": 5
        }
        self.music = True
        self.pillars = [
                (100, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False),
                (400, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False),
                (700, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False)
                    ]
        self.game_over = False
        self.bird_x, self.bird_y = 100+PILLAR_WIDTH, 10
        self.score = 0
        self.coins = 0
        self.game_speed = self.difficulty_speed[self.difficulty]
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")
        self.gameover_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
        self.coin_collect_sound = pygame.mixer.Sound("assets/sounds/coin_collect.mp3")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.darkness = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        self.darkness_level = 180 
        self.day = True 

        # Get the highest score
        try:
            with open("assets/json/highest_score.json", "r+") as file:
                data = json.load(file)
                highest_score = data["highest_score"]
                highest_score = int(highest_score)
                self.highest_score = highest_score
        except Exception:
            with open("assets/json/highest_score.json", "w") as file:
                data = {"highest_score":0}
                json.dump(data, file, indent=4)
                self.highest_score = 0

        self.coins_had = self.get_user_coins()

    def get_user_coins(self):
        # Get the number of coins user has
        try:
            with open("assets/json/coins_had.json", "r+") as file:
                data = json.load(file)
                coins_had = data["coins_had"]
                coins_had = int(coins_had)
                return coins_had
        except Exception:
            with open("assets/json/coins_had.json", "w") as file:
                data = {"coins_had":0}
                json.dump(data, file, indent=4)
                return 0
    
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.coins = 0
        self.game_speed = self.difficulty_speed[self.difficulty]
        self.bird_y = 10
        self.pillars = [
                (100, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False),
                (400, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False),
                (700, randint(0, int(60/100 * GAME_HEIGHT)), (randint(0,255),randint(0,255),randint(0,255)), False)
                    ]
        if self.music:
            pygame.mixer.music.unpause()

    def show_home(self, events):
        # Play the music if music is on
        if self.music:
            pygame.mixer.music.unpause()
            
        # Show the logo
        bird_logo = pygame.transform.scale(bird, (125,100))
        self.screen.blit(bird_logo, (450, 200))
        
        # Play button
        pygame.draw.rect(self.screen, (96,165,250), play_button, border_radius=10)
        self.screen.blit(play_text,play_text_rect)
        
        # Settings button
        pygame.draw.rect(self.screen, (192,132,252), settings_button, border_radius=10)
        self.screen.blit(settings_text,settings_text_rect)
        
        # Quit button
        pygame.draw.rect(self.screen, (248,113,113), quit_button, border_radius=10)
        self.screen.blit(quit_text,quit_text_rect)
        
        # Show the high score
        highest_score_text = in_game_variable_font.render(f"Highest Score : {self.highest_score}", True, (255,255,255))
        self.screen.blit(highest_score_text, (5,5))

        # Show the coins user has
        self.coins_had = self.get_user_coins()
        coins_had_text = in_game_variable_font.render(f": {self.coins_had}", True, (255,125,100))
        coins_had_text_x = GAME_WIDTH-(50+8*len(f"{self.coins_had}"))
        self.screen.blit(COIN, (coins_had_text_x-50, -5))
        self.screen.blit(coins_had_text, (coins_had_text_x,5))

        # Show the settings windows
        if self.setting_window:
            pygame.draw.rect(self.screen, (245,234,214), settings_window_rect, border_radius=20)
        
            pygame.draw.rect(self.screen, (96,165,250), difficulty_button, border_radius=10)
            difficulty_text = font.render(f"Difficulty : {self.difficulty}", True, (255, 255, 255))
            difficulty_text_rect = difficulty_text.get_rect(center=difficulty_button.center)
            self.screen.blit(difficulty_text, difficulty_text_rect)
        
            pygame.draw.rect(self.screen, (192,132,252), music_button, border_radius=10)
        
            music_text = font.render(f"Music : {"On" if self.music else "Off"}", True, (255, 255, 255))
            music_text_rect = music_text.get_rect(center=music_button.center)
            self.screen.blit(music_text, music_text_rect)
        
            pygame.draw.rect(self.screen, (248,113,113), quit_settings_button, border_radius=10)
            self.screen.blit(quit_settings_text, quit_settings_text_rect)
        
        # Detect events for home screen
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(pygame.mouse.get_pos()) and not self.setting_window:
                        self.reset_game()
                        self.game_screen = True

                    elif settings_button.collidepoint(pygame.mouse.get_pos()) and not self.setting_window:
                        self.setting_window = True

                    elif quit_button.collidepoint(pygame.mouse.get_pos()) and not self.setting_window:
                        self.running = False

                    elif difficulty_button.collidepoint(pygame.mouse.get_pos()) and self.setting_window:
                        i = self.difficulties.index(self.difficulty)
                        i+=1
                        if i > 2: i = 0
                        self.difficulty = self.difficulties[i]
                        self.game_speed = self.difficulty_speed[self.difficulty]

                    elif music_button.collidepoint(pygame.mouse.get_pos()) and self.setting_window:
                        self.music = False if self.music else True
                        if self.music:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

                    elif quit_settings_button.collidepoint(pygame.mouse.get_pos()) and self.setting_window:
                        self.setting_window = False

    def play_game(self, events):
 
        # Draw the bird and create a rectangle for bird to detect collision
        bird_rect = pygame.rect.Rect(self.bird_x+10, self.bird_y+10, BIRD_WIDTH-25, BIRD_HEIGHT-20)
        bird_img = pygame.transform.scale(bird, (BIRD_WIDTH,BIRD_HEIGHT))
        self.screen.blit(bird_img, (self.bird_x, self.bird_y))
        
        # Draw pillars and Coins
        for index, pillar in enumerate(self.pillars):
            pillar_x, pillar_height, pillar_color, coin_status = pillar

            # Down Pillar
            pillar_y = GAME_HEIGHT-pillar_height
            pillar_rect = pygame.Rect(pillar_x, pillar_y, PILLAR_WIDTH, pillar_height)
            pygame.draw.rect(self.screen, pillar_color, pillar_rect)  

            # Up Pillar
            up_side_down_pillar_y = 0
            up_side_down_pillar_height = pillar_y-VERTICAL_PILLAR_GAP
            up_side_down_pillar = pygame.Rect(pillar_x, up_side_down_pillar_y, PILLAR_WIDTH, up_side_down_pillar_height)
            pygame.draw.rect(self.screen, pillar_color, up_side_down_pillar)

            # Coins
            if coin_status:
                self.screen.blit(COIN, (pillar_x, (pillar_y+(pillar_y-VERTICAL_PILLAR_GAP))//2))

            if not self.game_over:
                #Move pillars
                pillar_x -= self.game_speed
                if pillar_x<(0-PILLAR_WIDTH):
                    self.score+=1
                    # Change the day night cycle
                    if self.score%3==0:
                        if self.day:
                            self.darkness_level += 5
                            if self.darkness_level>=220:
                                self.day = False
                        else:
                            self.darkness_level -= 20
                            if self.darkness_level<=10:
                                self.day = True
                    # Increase the game speed gradually
                    if self.score%10 == 0:
                        self.game_speed += 0.5
                    pillar_x = self.pillars[index-1][0]+300
                    pillar_height = randint(100, int(70/100 * GAME_HEIGHT))
                    pillar_color = (randint(0,255),randint(0,255),randint(0,255))
                    coin_luck = randint(0,50)
                    if coin_luck%5 == 0:
                        coin_status = True
                    else:
                        coin_status = False
                self.pillars[index] = (pillar_x, pillar_height, pillar_color, coin_status)
                                
                # Detect Collision with pilars
                if pillar_rect.colliderect(bird_rect) or up_side_down_pillar.colliderect(bird_rect):
                    pygame.mixer.music.pause()
                    self.gameover_sound.play()
                    self.game_over = True

                # Detect Collision with coins
                if coin_status:
                    coin_rect = pygame.Rect(pillar_x, (pillar_y+(pillar_y-VERTICAL_PILLAR_GAP))//2, 50, 50)
                    if coin_rect.colliderect(bird_rect):
                        self.coin_collect_sound.play()
                        self.coins += 1
                        coin_status = False
                        self.pillars[index] = (pillar_x, pillar_height, pillar_color, coin_status)
        
        # Move the bird, pillars and detect colision
        if not self.game_over: 
            # Drag the bird down
            self.bird_y += self.game_speed*1.5

            # Check if the bird is out of screen:
            if self.bird_y>(GAME_HEIGHT+BIRD_HEIGHT) or self.bird_y<(0-BIRD_HEIGHT):
                pygame.mixer.music.pause()
                self.gameover_sound.play()
                self.game_over = True
        else:
            self.screen.blit(gameover_text, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//4))
            self.screen.blit(gameover_msg_text1, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//2.5))
            self.screen.blit(gameover_msg_text2, (GAME_WIDTH//2-(FONT_SIZE*2.5), GAME_HEIGHT//2))

            # Update highest Score
            if self.score>self.highest_score:
                try:
                    with open("assets/json/highest_score.json", "w") as file:
                        self.highest_score = self.score
                        data = {"highest_score":self.score}
                        json.dump(data, file, indent=4)
                except Exception:
                    print("Error")

            # Update Coin had
            try:
                with open("assets/json/coins_had.json", "w") as file:
                    data = {"coins_had":self.coins_had+self.coins}
                    json.dump(data, file, indent=4)
            except Exception:
                print("Error")

        # Show Score
        score_text = in_game_variable_font.render(f"Score: {self.score}", True, (255,255,255))
        self.screen.blit(score_text, (5,5))

        # Show Coins
        coins_text = in_game_variable_font.render(f": {self.coins}", True, (255,125,100))
        coins_text_x = GAME_WIDTH-(50+8*len(f"{self.coins}"))
        self.screen.blit(COIN, (coins_text_x-50, -5))
        self.screen.blit(coins_text, (coins_text_x,5))
        
        # Detect user events
        for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.game_screen = False
        
                    elif event.key == pygame.K_SPACE and not self.game_over:
                        self.jump_sound.play()
                        self.bird_y -= 100
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

    def run(self):
        while self.running:
            # Detech different events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                        self.running = False
            
            # Set the background
            self.screen.blit(BACKGROUND, (0,0))
            self.darkness.fill((10,15,45, self.darkness_level))
            self.screen.blit(self.darkness, (0,0))
            
            # Show the home page
            if not self.game_screen:
                self.show_home(events)
            else:
                self.play_game(events)
            
            # Keep updating the game window
            pygame.display.flip()
            
            # Set the Frame Rate
            self.clock.tick(FRAME_RATE)

# Start the game
game = Game()
if __name__ == "__main__":
    game.run()
pygame.quit()