import sys
import pygame, pygame.locals
import time
import os
import random
import constants
dir = os.path.dirname(os.path.abspath(__file__))


pygame.init()
pygame.font.init()

inv = []
inv_bool = False
max_health = 100
fullscreen = False


class Actor:
    def __init__(self, playerrect, pilt, x, y, hp=0, ai=None, enemy=None):
        self.playerrect = playerrect
        self.pilt = pilt
        self.x = x
        self.y = y
        self.ai = ai
        self.hp = hp
        self.enemy = enemy
        self.target=None
        if ai:
            ai.owner = self

    def move(self, dx, dy):
        target=None
        for object in characters:
            if (object is not self and object.x == self.x+dx and object.y == self.y+dy):
                target = object
                break
        if not map[self.x+dx][self.y+dy].blocked and  target is None:
            self.playerrect = self.playerrect.move(dx*constants.tilesize, dy*constants.tilesize)
            self.x += dx
            self.y += dy
            
    def attack(self, damage):
        for object in characters:
            if (object is not self and (object.x == self.x+1 and object.y == self.y or # vaatab kas mingi teine Actor on kõrval
                                        object.x == self.x-1 and object.y == self.y or 
                                        object.x == self.x and object.y == self.y+1 or 
                                        object.x == self.x and object.y == self.y-1)):
                if self !=player and object != player:
                    return False
                else:
                    object.hp -=damage

                
                return True
    def draw(self):
        screen.blit(self.pilt, self.playerrect)

class AI:
    def take_turn(self):
        x=random.randint(-1, 1)
        y=random.randint(-1, 1)
        
        if x**2 == y**2: # kui tahab liikuda diagonaalis siis valib x või y ja muudab 0, et liiguks sirgjooneliselt
            c = random.randint(0, 1)
            if c == 0:
                x = 0
            else:
                y=0
        for obj in characters: #käib läbi iga tegelase, millel on AI component ja liigutab tegelast või ründab
            if obj == self.owner:
                if not self.owner.hp <= 0:
                    attack = self.owner.attack(random.randint(0, 5))
                    if not attack :
                        self.owner.move(x,y)

class Item:
    def __init__(self, name, sprite,  x, y, inv_sprite, drop_percent):
        self.name = name
        self.sprite = sprite
        self.x  = x
        self.y = y
        self.inv_sprite = inv_sprite
        self.drop_percent = drop_percent

class Room:
    #ristkülik mis iseloomustab ruumi
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
        #returns true, kui ruum lõikub teise ruumiga
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)

class Tile:
    def __init__(self, blocked, block_sight = None, item = None, grave = None):
        self.blocked = blocked
        self.block_sight = block_sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        self.item = item
        self.grave = grave

#MAP GENERATION

def create_room(room, door_x =None, door_y=None):
    global map, items
    gen_item = random.randint(0, 1) #valib suvaliselt kas asetada item ruumi
    if  gen_item:
        item_x = random.randint(room.x1+1, room.x2-1)
        item_y = random.randint(room.y1+1, room.y2-1)
        item_to_gen=random.randint(0, len(items)-1)
        (items[item_to_gen].x, items[item_to_gen].y) = (item_x, item_y)
    gen_enemy = random.randint(0, 1) #valib suvaliselt kas asetada enemy ruumi
    if gen_enemy:
        enemy_x = random.randint(room.x1+1, room.x2-1)
        enemy_y = random.randint(room.y1+1, room.y2-1)
        characters.append(Actor(constants.enemy_pilt.get_rect(), constants.enemy_pilt, enemy_x, enemy_y, hp=100, ai=AI()))
        characters[-1].playerrect = characters[-1].playerrect.move(enemy_x*constants.tilesize, enemy_y*constants.tilesize)
    #käib läbi vastavad tile-id, et muuta need läbipääsetavaks
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            
            if gen_item and x == items[item_to_gen].x and y == items[item_to_gen].y:
                map[x][y].item = items[item_to_gen]
                map[x][y].blocked = False
                map[x][y].block_sight = False
            else:
                map[x][y].blocked = False
                map[x][y].block_sight = False
            
    if door_x is not None and door_y is not None:
        map[door_x][door_y].blocked = False
        map[door_x][door_y].block_sight = False


    
def make_map():
    global map
    map = [[Tile(True) for y in range(constants.map_height)] for x in range(constants.map_width)]
    rooms = []
    num_rooms = 0
    for r in range(constants.max_rooms):
        #valib suvaliselt ruumi suuruse
        w = random.randint(constants.room_min_size, constants.room_max_size)
        h = random.randint(constants.room_min_size, constants.room_max_size)
        if num_rooms == 0:
            new_room = Room(int(constants.map_width/2-w/2), int(constants.map_height/2-h/2), w, h)
            prev_w = w
            prev_h = h
        else:
            room = random.randint(0, len(rooms)-1) #valib suvaliselt mingi ruumi "vanemaks"
            prev_x = rooms[room].x1
            prev_y = rooms[room].y1
            
            if random.randint(0, 1) == 1:  #valib kas uus ruum teha vanamast üles ja all või paremale ja vasakule
                if random.randint(0, 1) == 1: #loob ruumi vanemast alla
                    new_room = Room(prev_x, int(prev_y+prev_h), w, h)
                    door_x = int(new_room.x1+w/2) # ukse x koordinaat, mis ühendav vanemaga
                    door_y = int(new_room.y1) # ukse y koordinaat, mis ühendav vanemaga
                    if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                        if map[door_x][door_y-1].blocked: continue
                else: #loob ruumi vanemast üles
                    new_room = Room(prev_x, int(prev_y-h), w, h)
                    door_x = int(new_room.x1+w/2)
                    door_y = int(new_room.y2)
                    if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                        if map[door_x][door_y+1].blocked: continue
            else:
                if random.randint(0, 1) == 1: # loob ruumi vanemast paremale
                    new_room = Room(int(prev_x+prev_w), prev_y, w, h)
                    door_x = int(new_room.x1)
                    door_y = int(new_room.y1+h/2)
                    if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                        if map[door_x-1][door_y].blocked: continue
                else: #loob ruumi vanemast vasakule
                    new_room = Room(int(prev_x-w), prev_y, w, h)
                    door_x = int(new_room.x2)
                    door_y= int(new_room.y1+h/2)
                    if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                        if map[door_x+1][door_y].blocked: continue
            if new_room.x1 < 1 or new_room.x2>=constants.map_width or new_room.y1<1 or new_room.y2>=constants.map_height: continue
            
            prev_w = w
            prev_h = h
        #vaatab et uus ruum ei lõikuks varasematega
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            #ruum ei lõikund teistega järelikult asetab uue ruumi mapile
            if num_rooms == 0:
                create_room(new_room)
            else:
                create_room(new_room, door_x, door_y)

            rooms.append(new_room)
            num_rooms += 1
        
def map_to_surf(): # loob mapile uue surface, et säästa ressursse, kui pole vaja mapi uuendada
    for y in range(constants.map_height):
        for x in range(constants.map_width):
            tile = map[x][y].blocked
            if tile:
                map_surf.blit(constants.wall_sprite, (x*constants.tilesize, y*constants.tilesize))
            else:
                map_surf.blit(constants.floor_sprite, (x*constants.tilesize, y*constants.tilesize))
            if map[x][y].grave:
                map_surf.blit(constants.grave, (x*constants.tilesize, y*constants.tilesize))
            if not map[x][y].item is None:
                map_surf.blit(map[x][y].item.sprite, (x*constants.tilesize, y*constants.tilesize))

            
def render():
    global characters
    screen.blit(map_surf, (0, 0))
    for obj in characters:
        obj.draw()
    healthBar(player.hp)

#GAMEPLAY

def handle_move():
    global inv, inv_bool, fullscreen
    #turn based
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # Move player up
                player.move(0, -1)
                return 'move'
            elif event.key == pygame.K_DOWN: # Move player down
                player.move(0, 1)
                return 'move'
            elif event.key == pygame.K_LEFT: # Move player left
                player.move(-1, 0)
                return 'move'
            elif event.key == pygame.K_RIGHT: #move player right
                player.move(1, 0)
                return 'move'
            if event.key == pygame.K_RSHIFT: # pick up item
                pick_up(player.x, player.y)
            if event.key == pygame.K_SPACE:
                player.attack(random.randint(0, 10))
                enemy_death()
                return 'attack'
            if event.key == pygame.K_i and inv_bool:
                inv_surface.set_alpha(0)
                inv_bool = False
            elif event.key == pygame.K_i and not inv_bool:
                inv_surface.set_alpha(255)
                inv_bool = True
            if event.key == pygame.K_ESCAPE:
                menu()
            if event.key == pygame.K_i:
                inventory()
            if event.key == pygame.K_F11:
                if not fullscreen:
                    screen = pygame.display.set_mode((constants.screen_width, constants.screen_height), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    screen = pygame.display.set_mode((constants.screen_width, constants.screen_height))
                    fullscreen = False

   

def movement_loop():
    player_action = 'nothing'
    player_action = handle_move()
    if player_action == 'move' or player_action == 'attack':
        for obj in characters:
            if obj != player:
                obj.ai.take_turn()
    player_action = 'nothing'

def pick_up(x, y):
    global inv, map
    
    if not map[x][y].item is None:
        inv.append(map[x][y].item)
        map[x][y].item = None
    map_to_surf()

def enemy_death():
    global map, items
    for obj in characters:
        if obj is not player:
            if obj.hp <=0:
                map[obj.x][obj.y].grave = True
                rand = random.randint(0, len(items)-1)
                drop = random.randint(0, 100)
                if items[rand].drop_percent <= drop:
                    map[obj.x][obj.y].item = items[rand]
                map_to_surf()
                if obj in characters:
                    characters.remove(obj)

def start():
    player.playerrect = player.playerrect.move(constants.screen_width/2, constants.screen_height/2)
    player.x = int(constants.map_width/2)
    player.y = int(constants.map_height/2)

    make_map()
    map_to_surf()
def restart():
    global inv
    if player.hp <= 0:
        inv = []
        game_over = True
        over_text = font_comic.render('GAME OVER', False, (255,0,0))
        continue_text = font_comic.render('Press Enter to restart level', False, (255,255,255))
        while game_over:
            screen.blit(over_text, (int(constants.screen_width/2-over_text.get_rect()[2]/2), int(constants.screen_height/2-over_text.get_rect()[3]/2)))
            screen.blit(continue_text, (int(constants.screen_width/2-continue_text.get_rect()[2]/2), int(constants.screen_height/2-continue_text.get_rect()[3]/2+50)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        characters.clear()
                        characters.append(player)
                        player.playerrect.move_ip(0-player.x*constants.tilesize, 0-player.y*constants.tilesize)
                        player.x = int(constants.map_width/2)
                        player.y = int(constants.map_height/2)
                        player.playerrect.move_ip(constants.screen_width/2, constants.screen_height/2)
                        player.hp = 100
                        make_map()
                        map_to_surf()
                        game_over = False
            pygame.display.update()

#MENUS/UI

def menu():
    global menu_open
    menu_open=True
    font_comic = pygame.font.SysFont('Comic Sans MS', 40)
    text_pause = font_comic.render('PAUSED', False, textcolor)
    text_resume = font_comic.render('RESUME', False, textcolor, (255, 0, 0))
    text_resume_hover = font_comic.render('RESUME', False, textcolor, (150, 50, 50))
    text_quit = font_comic.render('QUIT', False, textcolor, (255, 0, 0))
    text_quit_hover = font_comic.render('QUIT', False, textcolor, (150, 50, 50))
    while menu_open:
        screen.blit(text_pause, (int(constants.screen_width/2-text_pause.get_rect()[2]/2), int(constants.screen_height/3-text_pause.get_rect()[3]/2)))
        b=screen.blit(text_resume, (int(constants.screen_width/2-text_resume.get_rect()[2]/2), int(constants.screen_height/2-text_resume.get_rect()[3]/2)))
        if b.collidepoint(pygame.mouse.get_pos()):
            b=screen.blit(text_resume_hover, (int(constants.screen_width/2-text_resume.get_rect()[2]/2), int(constants.screen_height/2-text_resume.get_rect()[3]/2)))
        c=screen.blit(text_quit, (int(constants.screen_width/2-text_quit.get_rect()[2]/2), int(constants.screen_height/2-text_quit.get_rect()[3]/2+70)))
        if c.collidepoint(pygame.mouse.get_pos()):
            c=screen.blit(text_quit_hover, (int(constants.screen_width/2-text_quit.get_rect()[2]/2), int(constants.screen_height/2-text_quit.get_rect()[3]/2+70)))
        
            #button function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
               if event.button == 1:
                    if b.collidepoint(pygame.mouse.get_pos()):
                        resume()
                    if c.collidepoint(pygame.mouse.get_pos()):
                        quit()
                        
            
        
        pygame.display.update()
class inv_tile:
    def __init__(self, filled, panel = None,  item=None, active=False):
        self.filled = filled
        self.active = active
        if panel:
            self.panel = panel
        
        self.item = item
        
            


def inventory():
    global inv_open, inv
    rows=4
    columns=4
    inv_width= int(constants.screen_width/2)
    inv_height = constants.screen_height-300
    row_width=int(inv_width/(columns+1))
    row_height=row_width
    table_spacing=int((inv_width-row_width*columns)/(columns+1))
    inv_open=True

    image_size = row_width-10
    text_inv = font_comic.render('INVENTORY', False, (66,75,84))
    active = None
    inv_tilemap = [[inv_tile(False) for y in range(rows)] for x in range(columns)]

    while inv_open:
        pygame.draw.rect(screen, (214,187,192), (int(constants.screen_width/4), 0, int(constants.screen_width*0.5), constants.screen_height))
        screen.blit(text_inv, (int(constants.screen_width/2-text_inv.get_rect()[2]/2), 30-text_inv.get_rect()[3]/2))
        list_pos=0
       

        for i in range(rows):
            for z in range(columns):

                if active == inv_tilemap[i][z]:
                    if inv_tilemap[i][z].item:
                        item_name = font_comic.render(inv_tilemap[i][z].item.name, False, textcolor)
                        screen.blit(item_name, (int(constants.screen_width/2-item_name.get_rect()[2]/2), constants.screen_height - 100))


                x=(int(constants.screen_width/4)+table_spacing+z*(table_spacing+row_width))
                y=50+table_spacing+i*(table_spacing+row_height)
                inv_tilemap[i][z].panel = pygame.draw.rect(screen, (225,206,122), (x, y, row_width, row_height))
                
                if active == inv_tilemap[i][z] or inv_tilemap[i][z].panel.collidepoint(pygame.mouse.get_pos()):
                    inv_tilemap[i][z].panel = pygame.draw.rect(screen, (181,123,166), (x, y, row_width, row_height))

                if list_pos < len(inv):
                    screen.blit(pygame.transform.scale(inv[list_pos].inv_sprite, (image_size, image_size)), (x+5, y+5))
                    inv_tilemap[i][z].item = inv[list_pos]
                    list_pos+=1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inv_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(rows):
                        for z in range(columns):
                            if inv_tilemap[i][z].panel.collidepoint(pygame.mouse.get_pos()):
                                if inv_tilemap[i][z].item:
                                    active = inv_tilemap[i][z]
                                else:
                                    active = None
                                

  
        pygame.display.update()

           
def resume():
    global menu_open
    menu_open = False
def quit():
    pygame.quit()
    sys.exit()

def healthBar(health):
    bg_bar = pygame.draw.rect(screen, (120, 30, 30), (20, constants.screen_height-30, int(max_health*1.5), 20))

    if health >= 0.66 * max_health:
        bar = pygame.draw.rect(screen, constants.healthbar_color_high, (20, constants.screen_height-30, int(health/100*max_health*1.5), 20))
    elif health >= 0.33 * max_health:
        bar = pygame.draw.rect(screen, constants.healthbar_color_med, (20, constants.screen_height-30, int(health/100*max_health*1.5), 20))
    else:
        bar = pygame.draw.rect(screen, constants.healthbar_color_low, (20, constants.screen_height-30, int(health/100*max_health*1.5), 20))


screen = pygame.display.set_mode((constants.screen_width, constants.screen_height))
inv_surface = pygame.Surface((constants.screen_width, constants.screen_height))
inv_surface=pygame.Surface.convert_alpha(inv_surface)
inv_surface.fill(constants.white_transparent)
map_surf = pygame.Surface((constants.screen_width, constants.screen_height))



player = Actor(constants.player_pilt.get_rect(), constants.player_pilt, 0, 0, 100)
characters= [player]

#annab itemitele väärtused
sword= Item("sword", constants.sword_sprite, 0, 0, constants.sword_sprite_inv, 20)
shield= Item("shield", constants.shield_sprite, 0, 0, constants.shield_sprite_inv,20)
armor= Item("armor", constants.armor_sprite, 0, 0, constants.armor_sprite_inv, 10)
bag= Item("bag", constants.bag_sprite, 0, 0, constants.bag_sprite_inv, 30)
beer= Item("beer", constants.beer_sprite, 0, 0, constants.beer_sprite_inv, 40)
book= Item("book", constants.book_sprite, 0, 0, constants.book_sprite_inv, 30)
boots= Item("boots", constants.boots_sprite, 0, 0, constants.boots_sprite_inv, 30)
flame_sword= Item("flame sword", constants.flame_sword_sprite, 0, 0, constants.flame_sword_sprite_inv, 5)
hat= Item("hat", constants.hat_sprite, 0, 0, constants.hat_sprite_inv, 30)
potion= Item("health potion", constants.potion_sprite, 0, 0, constants.potion_sprite_inv, 20)
potion2= Item("mana potion", constants.potion2_sprite, 0, 0, constants.potion2_sprite_inv, 20)

items=[]
items.append(sword)
items.append(shield)
items.append(armor)
items.append(bag)
items.append(beer)
items.append(book)
items.append(boots)
items.append(flame_sword)
items.append(hat)
items.append(potion)
items.append(potion2)
start()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
textcolor = 255, 255, 255
font_comic = pygame.font.SysFont('Comic Sans MS', 40)
font_comic_small = pygame.font.SysFont('Comic Sans MS', 20)
while 1:
    clock.tick(60)
    movement_loop()
    render()
    restart()
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white')) #fps counter
    screen.blit(fps, (0, 0))
    pygame.display.update()
    
