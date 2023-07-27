import math
import pygame
import random
import time
import os
from data.scripts.button import Button # By importing Button we can access methods from the Button class
from data.scripts.label import Label

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 227, 0)
RED_ON = (255, 0, 0)
RED_OFF = (227, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 227)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# HUD Constants
HUD_FONT = os.path.join("data", "assets", "Ldfcomicsans-jj7l.ttf")
HUD_HEIGHT = 40
HUD_WIDTH = SCREEN.get_width()
HUD_BG = pygame.Rect(0, 0, HUD_WIDTH, HUD_HEIGHT)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound(os.path.join("data", "assets", "bell1.mp3")) # bell1
RED_SOUND = pygame.mixer.Sound(os.path.join("data", "assets", "bell2.mp3")) # bell2
BLUE_SOUND = pygame.mixer.Sound(os.path.join("data", "assets", "bell3.mp3")) # bell3
YELLOW_SOUND = pygame.mixer.Sound(os.path.join("data", "assets", "bell4.mp3")) # bell4

# Button Sprite Objects (REPLACE NONE VALUES!)
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, HUD_HEIGHT)
red = Button(RED_ON, RED_OFF, RED_SOUND, 260, HUD_HEIGHT)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 260 + HUD_HEIGHT)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 260 + HUD_HEIGHT)

# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""
streak = 0
reset_rect = None


# Generates the HUD
def generate_hud(show_reset=False, show_time=False, time_left=""):
    global clock, reset_rect
    clock.tick(60)

    pygame.draw.rect(SCREEN, BLACK, HUD_BG)

    streak_text = Label(SCREEN, "Streak: " + str(streak), (5, 5), font_name=HUD_FONT)
    streak_text.set_default_size()

    reset_text = Label(SCREEN, "reset", (250, 5), fgc=BLACK, font_name=HUD_FONT)
    reset_text.set_default_size()
    reset_text.x = (SCREEN.get_rect().centerx) - (reset_text.get_width()/2)

    timer_text = Label(SCREEN, "Time: ", (400, 5), font_name=HUD_FONT)
    timer_text.set_default_size()
    timer_text.rect.x = SCREEN.get_width() - timer_text.get_width()
    
    #flags
    if show_reset: 
        reset_text.fgc = WHITE

    if show_time:
        timer_text.txt = "Time: " + time_left
    
    streak_text.update()
    reset_text.update()
    timer_text.update()
    reset_rect = reset_text.rect

def draw_board():
    # Call the draw method on all four button objects
    #if(time): print("drawing: " + str(time_left))
    SCREEN.fill(BLACK)
    generate_hud()
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

'''
Chooses a random color and appends to cpu_sequence.
Illuminates randomly chosen color.
'''
def cpu_turn():
    choice = random.choice(colors) # pick random color
    cpu_sequence.append(choice) # update cpu sequence
    if choice == "green":
        green.update(SCREEN)
    # Check other three color options
    elif choice == "red":
        red.update(SCREEN)
    elif choice == "blue":
        blue.update(SCREEN)
    elif choice == "yellow":
        yellow.update(SCREEN)

'''
Plays pattern sequence that is being tracked by cpu_sequence
'''
def repeat_cpu_sequence():
    if(len(cpu_sequence) != 0):
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)

'''
After cpu sequence is repeated the player must attempt to copy the same
pattern sequence.
The player is given 3 seconds to select a color and checks if the selected
color matches the cpu pattern sequence.
If player is unable to select a color within 3 seconds then the game is
over and the pygame window closes.
'''
def player_turn():
    global streak, clock
    turn_time = time.time()
    players_sequence = []
    handled = None
    count = 0

    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        handled = False
        show_time = True
        
        # Calculate remaining time in turn
        time_left = str(math.ceil((turn_time + 3) - time.time()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: end_session()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # button click occured
            # Grab the current position of mouse here
                pos = pygame.mouse.get_pos()
                if green.selected(pos): # green button was selected
                    green.update(SCREEN) # illuminate button
                    players_sequence.append("green") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer
                    handled = True
                # Check other three options
                elif red.selected(pos):
                    red.update(SCREEN)
                    players_sequence.append("red")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                    handled = True
                elif blue.selected(pos):
                    blue.update(SCREEN)
                    players_sequence.append("blue")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                    handled = True
                elif yellow.selected(pos):
                    yellow.update(SCREEN)
                    players_sequence.append("yellow")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                    handled = True
                if handled:
                    break
        
        # Generate updated HUD every 300000 iterations to reduce timer flickering (perhaps refactoring or multithreading could fix this issue)
        if count % 300000 == 0: generate_hud(show_time=show_time, time_left=time_left)
        count += 1
    
    streak += 1
    show_time = False
    time_left = ""
    count = 0

    # If player does not select a button within 3 seconds then game_over state initiates
    if not time.time() <= turn_time + 3:
        game_over()

'''
Checks if player's move matches the cpu pattern sequence
'''
def check_sequence(players_sequence):
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()

'''
Quits game and closes pygame window
'''
def end_session():
    pygame.display.quit()
    pygame.quit()
    quit()

# Allows player option to reset within "stall_time" seconds, otherwise ends the session
def game_over():
    global reset_rect, cpu_sequence, choice, streak
    
    generate_hud(show_reset=True)
    
    start = time.time()
    stall_time = 5
    broken = False
    
    while time.time() <= start + stall_time and not broken:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and reset_rect.collidepoint(pygame.mouse.get_pos()):
                cpu_sequence = []
                choice = ""
                streak = 0
                broken = True
                break
    if not broken: end_session()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_session()
    
    pygame.display.update()
    
    draw_board() # draws buttons onto pygame screen
    repeat_cpu_sequence() # repeats cpu sequence if it's not empty
    cpu_turn() # cpu randomly chooses a new color
    player_turn() # player tries to recreate cpu sequence
    pygame.time.wait(1000) # waits one second before repeating cpu sequence
    
    clock.tick(60)