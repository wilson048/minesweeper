from enum import Enum
from board import Grid, Mine
import pygame
import os
import random


class Button:
    def __init__(self, bounds, extents, image):
        """ A button class for creating buttons containing images and bounds"""
        self.x_pos = bounds[0]
        self.y_pos = bounds[1]
        self.x_len = extents[0]
        self.y_len = extents[1]
        self.image = image

    def in_bounds(self, pos):
        """Returns true if the mouse position is in the boundary created by the button. The purpose of this is to
        check whether a mouse click is on top of a button """
        return self.x_pos <= pos[0] <= self.x_pos + self.x_len and self.y_pos <= pos[1] <= self.y_pos + self.y_len

    def display(self, screen):
        """ Displays the button on the given screen"""
        screen.blit(self.image, (self.x_pos, self.y_pos))


class GameState(Enum):
    """Enums for representing game screens"""
    MAIN_MENU = 1
    GAME_SCREEN = 2


# Sound playing function
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace(' ', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
    sound.play()


# Random music player function
def play_a_different_song():
    global _currently_playing_song, _songs
    next_song = random.choice(_songs)
    while next_song == _currently_playing_song:
        next_song = random.choice(_songs)
    _currently_playing_song = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()


# Image processing function
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace(' ', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


# Num displaying function for main menu and timer
def display_nums(ten_num, ones_num, x, y):
    global screen
    global switch
    global game_state_num
    if ten_num == 0:
        screen.blit(get_image("assets/nums/0-main.png"), (x, y))
    elif ten_num == 1:
        screen.blit(get_image("assets/nums/1-main.png"), (x, y))
    elif ten_num == 2:
        screen.blit(get_image("assets/nums/2-main.png"), (x, y))
    elif ten_num == 3:
        screen.blit(get_image("assets/nums/3-main.png"), (x, y))
    elif ten_num == 4:
        screen.blit(get_image("assets/nums/4-main.png"), (x, y))
    elif ten_num == 5:
        screen.blit(get_image("assets/nums/5-main.png"), (x, y))
    elif ten_num == 6:
        screen.blit(get_image("assets/nums/6-main.png"), (x, y))
    elif ten_num == 7:
        screen.blit(get_image("assets/nums/7-main.png"), (x, y))
    elif ten_num == 8:
        screen.blit(get_image("assets/nums/8-main.png"), (x, y))
    elif ten_num == 9:
        screen.blit(get_image("assets/nums/9-main.png"), (x, y))
    x += 40
    if ones_num == 0:
        screen.blit(get_image("assets/nums/0-main.png"), (x, y))
    elif ones_num == 1:
        screen.blit(get_image("assets/nums/1-main.png"), (x, y))
    elif ones_num == 2:
        screen.blit(get_image("assets/nums/2-main.png"), (x, y))
    elif ones_num == 3:
        screen.blit(get_image("assets/nums/3-main.png"), (x, y))
    elif ones_num == 4:
        screen.blit(get_image("assets/nums/4-main.png"), (x, y))
    elif ones_num == 5:
        screen.blit(get_image("assets/nums/5-main.png"), (x, y))
    elif ones_num == 6:
        screen.blit(get_image("assets/nums/6-main.png"), (x, y))
    elif ones_num == 7:
        screen.blit(get_image("assets/nums/7-main.png"), (x, y))
    elif ones_num == 8:
        screen.blit(get_image("assets/nums/8-main.png"), (x, y))
    elif ones_num == 9:
        screen.blit(get_image("assets/nums/9-main.png"), (x, y))


""" 
Variables for helper functions
"""

# Stores the images in a list for future use
_image_library = {}
# Stores the currently plaiying song
_currently_playing_song = None
# List of available songs in the scripts package# g
_songs = {'audio.mp3'}
# Stores the sounds in a list for future use
_sound_library = {}

# Rows and columns for the game
grid_rows = 10
grid_cols = 15

# Width of the pygame window
width = 500
# Height of the pygame window
height = 500
# pygame shenanigans
pygame.init()
res = (width, height)
screen = pygame.display.set_mode(res)
done = False
clock = pygame.time.Clock()
# Name the pygame window
pygame.display.set_caption('Minesweeper')
# Set the pygame icon
pygame.display.set_icon(get_image('assets/grid/Mine.png'))

pygame.font.init()

# Buttons for main menu
row_up_button = Button((100, 150), (80, 40), get_image("assets/buttons/up-arrow.png"))
row_down_button = Button((100, 230), (80, 40), get_image("assets/buttons/down-arrow.png"))
col_up_button = Button((320, 150), (80, 40), get_image("assets/buttons/up-arrow.png"))
col_down_button = Button((320, 230), (80, 40), get_image("assets/buttons/down-arrow.png"))
play_button = Button((180, 350), (140, 60), get_image("assets/buttons/play-button.png"))
menu_buttons = [row_up_button, row_down_button, col_up_button, col_down_button, play_button]
# Load music located in scripts
# pygame.mixer.music.load('assets/audio.mp3')
#
# # # Play the music
# pygame.mixer.music.play()
# pygame.mixer.music.set_volume(0.3)
switch = {
    1: GameState.MAIN_MENU,
    2: GameState.GAME_SCREEN,
}

# Game Display in action
first_time = True
init_seconds = 0
game_state_num = 1
while not done:
    screen.fill((180, 180, 180))
    # X position represents column number, Y position represents row number
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pygame.mouse.get_pos()
    # Each square is 40 x 40 pixels long
    # Main menu
    if switch.get(game_state_num) == GameState.MAIN_MENU:
        screen.blit(get_image("assets/Title-jp.png"), (150, 70))
        # row numbers
        num_1 = grid_rows // 10
        num_2 = grid_rows % 10
        display_nums(num_1, num_2, 100, 190)
        # column numbers
        num_1 = grid_cols // 10
        num_2 = grid_cols % 10
        display_nums(num_1, num_2, 320, 190)
        # Game buttons
        for b in menu_buttons:
            b.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Button Functionality
                if row_up_button.in_bounds(pos):
                    if grid_rows < 25:
                        grid_rows += 1
                elif row_down_button.in_bounds(pos):
                    if grid_rows > 5:
                        grid_rows -= 1
                elif col_up_button.in_bounds(pos):
                    if grid_cols < 30:
                        grid_cols += 1
                elif col_down_button.in_bounds(pos):
                    if grid_cols > 15:
                        grid_cols -= 1
                elif play_button.in_bounds(pos):
                    width = grid_cols * 40
                    height = grid_rows * 40 + 100
                    screen = pygame.display.set_mode((width, height))
                    # Buttons for game screen
                    reset_button = Button(((width // 2 + 40) + 5, 30), (80, 40), get_image("assets/buttons/reset-button.png"))
                    options_button = Button(((width // 2 + 40) + 90, 30), (80, 40), get_image("assets/buttons/options.png"))
                    quit_button = Button(((width // 2 + 40) + 175, 30), (80, 40), get_image("assets/buttons/quit.png"))
                    game_buttons = [reset_button, options_button, quit_button]
                    # Create new grid
                    grid = Grid(grid_rows, grid_cols)
                    # Set first time to True to guarantee a playable board
                    first_time = True
                    # Change screen to game
                    game_state_num = 2
    # Game is running on this time
    elif switch.get(game_state_num, "Invalid") == GameState.GAME_SCREEN:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Clicking functionality
            if event.type == pygame.MOUSEBUTTONDOWN:
                # make sure the mouse is in the bounds of the grid
                mouseX = mouseX // 40
                mouseY = (mouseY - 100) // 40
                if grid.in_bounds(mouseY, mouseX):
                    # guarantee the first click is an open space by generating grids until the position contains no
                    # bombs
                    if first_time:
                        if event.button == 3:
                            break
                        init_seconds = pygame.time.get_ticks()
                        first_time = False
                        while grid.get_cell(mouseY, mouseX).get_num_mines() != 0:
                            grid = Grid(grid_rows, grid_cols)
                    # right-click - flag
                    if event.button == 3:
                        grid.flag_board(mouseY, mouseX)
                    # left-click - reveal board
                    else:
                        if grid.get_cell(mouseY, mouseX).is_revealed():
                            grid.reveal_unflagged(mouseY, mouseX)
                        else:
                            grid.reveal_board(mouseY, mouseX)
                if grid.has_won() or grid.has_lost():
                    # Game over buttons
                    if reset_button.in_bounds(pos):
                        first_time = True
                        grid = Grid(grid_rows, grid_cols)
                    if quit_button.in_bounds(pos):
                        done = True
                    if options_button.in_bounds(pos):
                        game_state_num = 1
                        screen = pygame.display.set_mode((500, 500))

        tempX = 100
        tempY = 100
        # Display images for the grid
        for i in range(grid.get_rows()):
            tempX = 0
            for j in range(grid.get_cols()):
                if grid.get_cell(i, j).is_flagged():
                    screen.blit(get_image("assets/grid/Flag.png"), (tempX, tempY))
                elif not grid.get_cell(i, j).is_revealed():
                    screen.blit(get_image("assets/grid/Hidden.png"), (tempX, tempY))
                elif isinstance(grid.get_cell(i, j), Mine):
                    screen.blit(get_image("assets/grid/Mine.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 0:
                    screen.blit(get_image("assets/grid/0.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 1:
                    screen.blit(get_image("assets/grid/1.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 2:
                    screen.blit(get_image("assets/grid/2.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 3:
                    screen.blit(get_image("assets/grid/3.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 4:
                    screen.blit(get_image("assets/grid/4.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 5:
                    screen.blit(get_image("assets/grid/5.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 6:
                    screen.blit(get_image("assets/grid/6.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 7:
                    screen.blit(get_image("assets/grid/7.png"), (tempX, tempY))
                elif grid.get_cell(i, j).get_num_mines() == 8:
                    screen.blit(get_image("assets/grid/8.png"), (tempX, tempY))
                tempX += 40
            tempY += 40

        if grid.has_won():
            # Game state - Win
            screen.blit(get_image("assets/face-win.png"), ((width // 2) - 40, 10))
            stuff = 0
            for b in game_buttons:
                b.display(screen)
        elif grid.has_lost():
            # Game state - Lost
            screen.blit(get_image("assets/face-lost.png"), ((width // 2) - 40, 10))
            grid.reveal_mines()
            for b in game_buttons:
                b.display(screen)
        elif not first_time:
            # Game state - Ongoing, update time
            seconds = (pygame.time.get_ticks() - init_seconds) // 1000
            minutes = seconds // 60
            seconds %= 60
            screen.blit(get_image("assets/face.png"), ((width // 2) - 40, 10))
        else:
            # Game state - hasn't begun
            seconds = 0
            minutes = 0
            screen.blit(get_image("assets/face.png"), ((width // 2) - 40, 10))
        # Display the timer for the game
        # text = my_font.render("Time: {:02d}:{:02d}".format(minutes, seconds % 60), False, (0, 0, 0))
        tens_seconds = seconds // 10
        ones_seconds = seconds % 10
        display_nums(tens_seconds, ones_seconds, 90, 30)
        tens_minutes = minutes // 10
        ones_minutes = minutes % 10
        display_nums(tens_minutes, ones_minutes, 10, 30)
        #    screen.blit(get_image("assets/buttonJP.png"), (width - 80, 0))
        # screen.blit(text, (width - 250, height // 8))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
