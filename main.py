import pygame
from random import randint, choice
import constants



class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path

class obj_Actor:
    def __init__(self, x, y, sprite):
        self.x = x # map address
        self.y = y # map address
        self.sprite = sprite

  
    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy



def map_create():
    # create empty map
    global NEW_MAP
    NEW_MAP = [[struc_Tile(False) for y in range(constants.MAP_HEIGHT)] for x in range(constants.MAP_WIDTH)]

    # surround map with walls
    for x in range(constants.MAP_WIDTH):
        NEW_MAP[x][0].block_path = True
        NEW_MAP[x][constants.MAP_HEIGHT - 1].block_path = True
    for y in range(constants.MAP_HEIGHT):
        NEW_MAP[0][y].block_path = True
        NEW_MAP[constants.MAP_WIDTH - 1][y].block_path = True

    # draw vertical walls and doors to the map
    vertical_walls = [] # two dimensional list that hold door coordinates for each wall in separate lists
    x_start = 0
    y_start = 0
    x_end = randint(constants.MIN_WALL_LENGTH, constants.MAX_WALL_LENGTH)
    y_end = randint(constants.MIN_WALL_LENGTH, constants.MAX_WALL_LENGTH)

    while x_end <= constants.MAP_WIDTH - 7:
        vertical_walls.append([])
        
        while y_end <= constants.MAP_HEIGHT - 7:
            while y_start <= y_end:
                NEW_MAP[x_end][y_start + 1].block_path = True
                y_start += 1
               
            y_start += 1
            vertical_walls[-1].append((x_end, y_start))
            y_end = y_start + randint(constants.MIN_WALL_LENGTH, constants.MAX_WALL_LENGTH)

            if y_end > constants.MAP_HEIGHT - 7 and y_start + 6 < constants.MAP_HEIGHT:
                y_start += 1

                while not NEW_MAP[x_end][y_start].block_path:
                    NEW_MAP[x_end][y_start].block_path = True
                    y_start += 1
            elif y_end > constants.MAP_HEIGHT - 7:
                for w in range(len(vertical_walls)):
                    if (x_end, y_start) in vertical_walls[w]:
                        vertical_walls[w].remove((x_end, y_start))

                while not NEW_MAP[x_end][y_start].block_path:
                    NEW_MAP[x_end][y_start].block_path = True
                    y_start += 1

        y_start = 0
        y_end = randint(constants.MIN_WALL_LENGTH, constants.MAX_WALL_LENGTH)
        x_end += randint(constants.MIN_WALL_LENGTH, constants.MAX_WALL_LENGTH)

    print('Doors in vertical walls: ', vertical_walls)

    # draw horizontal walls and doors
    x_start = 1

    for doors in range(len(vertical_walls)):
        for door in range(1, len(vertical_walls[doors])):
            door1 = vertical_walls[doors][door - 1][1] # y coordinate of a door
            door2 = vertical_walls[doors][door][1] # y coordinate of the door below the first one
            y_start = randint(door1 + constants.MIN_WALL_LENGTH / 2, door2 - constants.MIN_WALL_LENGTH / 2)
            
            if not NEW_MAP[x_start - 1][y_start].block_path: # check if the new vertical wall blocks a door on the horizontal wall
                if randint(0, 1) == 0:                       # if it does then move the vertical wall up or down by 1
                    y_start -= 1
                else:
                    y_start += 1
            
            if len(vertical_walls) - doors == 1: # if we are at the rightmost wall then also draw a wall to the right
                y_start2 = randint(door1 + constants.MIN_WALL_LENGTH / 2, door2 - constants.MIN_WALL_LENGTH / 2)
                x_start2 = vertical_walls[doors][0][0] + 1
                x_door2 = randint(x_start2, constants.MAP_WIDTH - 2)
                
                resetter2 = 0
                while not NEW_MAP[x_start2][y_start2].block_path:
                    if x_start2 != x_door2:
                        NEW_MAP[x_start2][y_start2].block_path = True
                    x_start2 += 1
                    resetter2 += 1
                x_start2 -= resetter2
                
            x_door = randint(x_start, vertical_walls[doors][0][0] - 1)
            resetter = 0
            while not NEW_MAP[x_start][y_start].block_path:
                if x_start != x_door:
                    NEW_MAP[x_start][y_start].block_path = True
                x_start += 1
                resetter += 1
            x_start -= resetter
            
        x_start = vertical_walls[doors][0][0] + 1

    return NEW_MAP


def draw_map(map_to_draw):
    for x in range(constants.MAP_WIDTH):
        for y in range(constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_game():
    global SURFACE_MAIN

    #clear surface
    SURFACE_MAIN.fill(constants.COLOUR_DEFAULT_BG)

	# draw the map
    draw_map(GAME_MAP)

	# draw the char
    PLAYER.draw()

	#update display
    pygame.display.flip()


def game_main_loop():
    game_quit = False

    while not game_quit:
        events_list = pygame.event.get()

        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_quit = True
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)

        draw_game()

    pygame.quit()
    exit()


def game_initialize():
    global SURFACE_MAIN, GAME_MAP, PLAYER

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    GAME_MAP = map_create()

    PLAYER = obj_Actor(1, 1, constants.S_PLAYER)



if __name__ == '__main__':
    game_initialize()
    game_main_loop()