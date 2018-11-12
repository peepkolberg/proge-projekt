import pygame

pygame.init()

# display resolution px
GAME_WIDTH = 1024
GAME_HEIGHT = 640

# map dimensions
MAP_WIDTH = 64  # cells
MAP_HEIGHT = 40  # cells
CELL_WIDTH = 16  # px
CELL_HEIGHT = 16  # px

# colours
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GRAY = (100, 100, 100)

# game colours
COLOUR_DEFAULT_BG = COLOUR_GRAY

# sprites
S_PLAYER = pygame.image.load('data/character.png')
S_WALL = pygame.image.load('data/wall.png')
S_FLOOR = pygame.image.load('data/floor.png')

# rooms
MIN_WALL_LENGTH = 6
MAX_WALL_LENGTH = 10
