import sys
import pygame, pygame.locals
import time
import os
import random
import math
dir = os.path.dirname(os.path.abspath(__file__))


pygame.init()
screen_width = 800
screen_height = 600
tilesize = 20
white = 255, 255, 255
map_width = int(screen_width/tilesize) #in tiles
map_height = int(screen_height/tilesize) #in tiles
room_max_size = 7
room_min_size = 4
max_rooms = 200   #palju PROOVIB ruume genereerida

def handle_move():

    #turn based
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN  and event.key == pygame.K_UP:
            #player.playerrect = player.playerrect.move(0, -50)
            player.move(0, -1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #player.playerrect = player.playerrect.move(0, 50)
            player.move(0, 1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #player.playerrect = player.playerrect.move(-50, 0)
            player.move(-1, 0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #player.playerrect = player.playerrect.move(50, 0)
            player.move(1, 0)

class Actor:
    def __init__(self, playerrect, pilt, x, y):
        self.playerrect = playerrect
        self.pilt = pilt
        self.x = x
        self.y = y

    def move(self, dx, dy):
        if not map[self.x+dx][self.y+dy].blocked:
            self.playerrect = self.playerrect.move(dx*tilesize, dy*tilesize)
            self.x += dx
            self.y += dy

    def draw(self):
        screen.blit(self.pilt, self.playerrect)

class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)


class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.block_sight = block_sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

def create_room(room, door_x =None, door_y=None):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False
    if door_x is not None and door_y is not None:
        map[door_x][door_y].blocked = False
        map[door_x][door_y].block_sight = False


def make_map():
    global map
    map = [[Tile(True) for y in range(map_height)] for x in range(map_width)]
    rooms = []
    num_rooms = 0
 
    for r in range(max_rooms):
        #random screen_width and screen_height
        w = random.randint(room_min_size, room_max_size)
        h = random.randint(room_min_size, room_max_size)
        #random position without going out of the boundaries of the map
        x = random.randint(0, map_width - w - 1)
        y = random.randint(0, map_height - h - 1)
        if num_rooms == 0:
            new_room = Rect(int(map_width/2-w/2), int(map_height/2-h/2), w, h)
            prev_w = w
            prev_h = h
        else:
            room = random.randint(0, len(rooms)-1) #valib suvaliselt mingi ruumi "vanemaks"
            prev_x = rooms[room].x1
            prev_y = rooms[room].y1
            
            if random.randint(0, 1) == 1:  #valib kas uus ruum teha vanamast üles ja all või paremale ja vasakule
                if random.randint(0, 1) == 1: #loob ruumi vanemast alla
                    new_room = Rect(prev_x, int(prev_y+prev_h), w, h)
                    door_x = int(new_room.x1+w/2) # ukse x koordinaat, mis ühendav vanemaga
                    door_y = int(new_room.y1) # ukse y koordinaat, mis ühendav vanemaga
                    if door_x>=1 and door_y>=1 and door_x<map_width and door_y< map_height:
                        if map[door_x][door_y-1].blocked: continue
                else: #loob ruumi vanemast üles
                    new_room = Rect(prev_x, int(prev_y-h), w, h)
                    door_x = int(new_room.x1+w/2)
                    door_y = int(new_room.y2)
                    if door_x>=1 and door_y>=1 and door_x<map_width and door_y< map_height:
                        if map[door_x][door_y+1].blocked: continue
            else:
                if random.randint(0, 1) == 1: # loob ruumi vanemast paremale
                    new_room = Rect(int(prev_x+prev_w), prev_y, w, h)
                    door_x = int(new_room.x1)
                    door_y = int(new_room.y1+h/2)
                    if door_x>=1 and door_y>=1 and door_x<map_width and door_y< map_height:
                        if map[door_x-1][door_y].blocked: continue
                else: #loob ruumi vanemast vasakule
                    new_room = Rect(int(prev_x-w), prev_y, w, h)
                    door_x = int(new_room.x2)
                    door_y= int(new_room.y1+h/2)
                    if door_x>=1 and door_y>=1 and door_x<map_width and door_y< map_height:
                        if map[door_x+1][door_y].blocked: continue
            if new_room.x1 < 1 or new_room.x2>=map_width or new_room.y1<1 or new_room.y2>=map_height: continue
            
            prev_w = w
            prev_h = h
        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            #this means there are no intersections, so this room is valid
            #"paint" it to the map's tiles
            if num_rooms == 0:
                create_room(new_room)
            else:
                create_room(new_room, door_x, door_y)

            rooms.append(new_room)
            num_rooms += 1



def render():
    for y in range(map_height):
        for x in range(map_width):
            tile = map[x][y].blocked
            if tile:
                screen.blit(wall_sprite, (x*tilesize, y*tilesize))
            else:
                screen.blit(floor_sprite, (x*tilesize, y*tilesize))
    player.draw()


screen = pygame.display.set_mode((screen_width, screen_height))

floor_sprite = pygame.image.load(os.path.join(dir, "floor.png"))
floor_sprite = pygame.transform.scale(floor_sprite,(tilesize, tilesize))
wall_sprite = pygame.image.load(os.path.join(dir, "wall.png"))
wall_sprite = pygame.transform.scale(wall_sprite,(tilesize, tilesize))
floor_rect = floor_sprite.get_rect()
wall_rect = wall_sprite.get_rect()
player_pilt = pygame.image.load(os.path.join(dir, "character.png")).convert_alpha()
player_pilt = pygame.transform.scale(player_pilt, (tilesize, tilesize))
player = Actor(player_pilt.get_rect(), player_pilt, 0, 0)
player.playerrect = player.playerrect.move(screen_width/2, screen_height/2)
player.x = int(screen_width/2/tilesize)
player.y = int(screen_height/2/tilesize)
make_map()
#map = pygame.Surface((screen_width, screen_height))
while 1:
   
    render()
    handle_move()
    pygame.display.flip()
    
