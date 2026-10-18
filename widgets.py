import pygame
pygame.init()

FONT_SIZE = 44

# Create all the necessary buttons and texts

font = pygame.font.Font("assets/fonts/cursive.ttf", FONT_SIZE)
game_over_msg_font = pygame.font.Font("assets/fonts/cursive.ttf", 30)

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