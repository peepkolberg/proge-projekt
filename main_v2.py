import pygame
import pygame.locals
import random
import time
import sys
import constants
import Declare_items
import platform
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
#print(platform.architecture())
if platform.architecture()[0] == '64bit':
    from _x64 import libtcodpy as libtcod
else:
    from _x86 import libtcodpy as libtcod

class Game:
    def initialize(self):
        global camera, player, map_surf, screen, kaart, characters, ui, inv_bool, inv, inv_surface, equipped_items, level, font_xsmall
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((constants.screen_width, constants.screen_height), pygame.HWSURFACE)
        map_surf = pygame.Surface((constants.map_width*constants.tilesize, constants.map_height*constants.tilesize))
        ui = pygame.Surface((constants.screen_width, constants.screen_height)).convert_alpha()
        ui.fill((0, 0, 0, 0))
        pygame.mixer.music.load(constants.background)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        inv_surface = pygame.Surface((constants.screen_width, constants.screen_height)).convert_alpha()
        inv_surface.fill((0, 0, 0, 0))
        camera=Camera()
        player = Actor(constants.player_pilt.get_rect(), constants.player_pilt, 0, 0, constants.max_health)
        Actor().healthBar(player.hp)
        inv=[]
        inv_bool=False
        characters= [player]
        equipped_items = []
        for m in range(5):
            equipped_items.append(0)
        kaart = Map()
        level = 1
        font_xsmall = constants.font_very_small

    def game_loop(self):
        global screen, map_surf,kaart, characters, ui
        kaart.make_map()
        player.move(int(constants.map_width/2), int(constants.map_height/2))
        while len(characters)<constants.min_enemies+1:
            Map().make_map()
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 30)
        while 1:
            clock.tick(60)
            Game().win()
            Game().draw_game()
            fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'), (0,0,0))
            screen.blit(fps, (0, 0))
            pygame.display.update()

    def handle_move(self):
        global inv, inv_bool, fullscreen, fov_calculate, player
        #turn based
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: # Move player up
                    player.move(0, -1)
                    fov_calculate = True
                    return 'move'
                elif event.key == pygame.K_DOWN: # Move player down
                    player.move(0, 1)
                    fov_calculate = True
                    return 'move'
                elif event.key == pygame.K_LEFT: # Move player left
                    player.move(-1, 0)
                    fov_calculate = True
                    return 'move'
                elif event.key == pygame.K_RIGHT: #move player right
                    player.move(1, 0)
                    fov_calculate = True
                    return 'move'
                if event.key == pygame.K_RSHIFT: # pick up item
                    Actor().pick_up(player.x, player.y)
                if event.key == pygame.K_SPACE:
                    #damage = random.randint(constants.player_min_dmg, constants.player_dmg)
                    player.attack(constants.player_dmg)
                    #print("Player attacked for", damage, "damage")
                    Actor().enemy_death()
                    return 'attack'

                if event.key == pygame.K_ESCAPE:
                    Menus().menu()
                if event.key == pygame.K_i:
                    Menus().inventory()
                if event.key == pygame.K_F11:
                    if not constants.fullscreen:
                        constants.fullscreen = True
                        Camera().resolution_control(constants.screen_width, constants.screen_height)
                    else:
                        constants.fullscreen = False
                        Camera().resolution_control(constants.screen_width, constants.screen_height)

    def movement_loop(self):
        Game().restart()
        player_action = 'nothing'
        player_action = Game().handle_move()
        if constants.Fov_enabled:
            Map().calculate_fov()
        if player_action == 'move' or player_action == 'attack':
            for obj in characters:
                if obj != player:
                    obj.ai.take_turn()
        player_action = 'nothing'

    def restart(self, form_menu = False):
        global map_surf, characters, player, map
        if player.hp <= 0:
            game_over = True
            font = constants.font
            over_text = font.render('GAME OVER', False, (255,0,0))
            continue_text = font.render('Press Enter to restart level', False, (255,255,255))
            while game_over:
                screen.blit(over_text, (int(constants.screen_width/2-over_text.get_rect()[2]/2), int(constants.screen_height/2-over_text.get_rect()[3]/2)))
                screen.blit(continue_text, (int(constants.screen_width/2-continue_text.get_rect()[2]/2), int(constants.screen_height/2-continue_text.get_rect()[3]/2+50)))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Menus().quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            characters.clear()
                            characters.append(player)
                            map[0][0].blocked = False
                            player.move(0-player.x, 0-player.y)
                            Map().make_map()
                            map_surf.fill((0,0,0))
                            player.move(int(constants.map_width/2), int(constants.map_height/2))
                            while len(characters)<constants.min_enemies+1:
                                Map().make_map()
                            player.hp = constants.max_health
                            Map().calculate_fov()
                            Map().map_to_surf()
                            Actor().healthBar(player.hp)
                            game_over = False
                pygame.display.update()
        elif form_menu:
            characters.clear()
            characters.append(player)
            map[0][0].blocked = False
            player.move(0-player.x, 0-player.y)
            Map().make_map()
            player.move(int(constants.map_width/2), int(constants.map_height/2))
            while len(characters)<constants.min_enemies+1:
                Map().make_map()
            map_surf.fill((0,0,0))
            player.hp = constants.max_health
            Map().calculate_fov()
            Map().map_to_surf()
            Actor().healthBar(player.hp)

    def draw_game(self):
        global font_xsmall
        Game().movement_loop()
        kaart.calculate_fov()
        kaart.map_to_surf()
        screen.fill((0,0,0))
        for obj in characters:
            obj.draw()
        screen.blit(map_surf, (0, 0),((player.x)*constants.tilesize-int(constants.screen_width/2), (player.y)*constants.tilesize-int(constants.screen_height/2), constants.screen_width, constants.screen_height))
        screen.blit(ui, (0,0))
        disclaimer_text = font_xsmall.render("* It's not a bug, it's a feature", False, constants.white)
        screen.blit(disclaimer_text, (constants.screen_width-disclaimer_text.get_rect()[2]-5, 5))

    def win(self):
        global characters, level
        if len(characters)==1:
            font = constants.font
            over_text = font.render('ALL ENEMIES DESTROYED', False, (255,0,0))
            continue_text = font.render('Press Enter to advance to next level', False, (255,255,255))
            level_over = True
            while level_over:
                screen.blit(over_text, (int(constants.screen_width/2-over_text.get_rect()[2]/2), int(constants.screen_height/2-over_text.get_rect()[3]/2)))
                screen.blit(continue_text, (int(constants.screen_width/2-continue_text.get_rect()[2]/2), int(constants.screen_height/2-continue_text.get_rect()[3]/2+50)))
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            level +=1
                            Game().restart(True)
                            level_over = False
                pygame.display.update()

class Map:
    class Tile():
        def __init__(self, blocked, item = None, grave = None, explored = False):
            self.blocked = blocked
            self.explored = explored
            self.item = item
            self.grave = grave
    class Room():
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

    def create_room(self, room, door_x =None, door_y=None):
        global map, items, spawn_item
        spawn_item = True
        Actor().spawn_enemy(room)
        item_to_gen = random.randint(0, len(Declare_items.items)-1)
        gen_item = random.randint(0, 1)
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                Item().generate_item(room, x, y, item_to_gen, gen_item)
                map[x][y].blocked = False
                map[x][y].block_sight = False
                
        if door_x is not None and door_y is not None:
            map[door_x][door_y].blocked = False
            map[door_x][door_y].block_sight = False

    def map_to_surf(self):
        global map, camera, map_surf
        map_surf.fill((0, 0, 0))
        camera_rect = pygame.Rect(player.x*constants.tilesize-int(constants.screen_width/2), player.y*constants.tilesize-int(constants.screen_height/2), constants.screen_width, constants.screen_height)
        for y in range(constants.map_height):
            for x in range(constants.map_width):
                tilerect = pygame.Rect((x*constants.tilesize, y*constants.tilesize), (constants.tilesize, constants.tilesize))
                if camera_rect.collidepoint(tilerect[0],tilerect[1]+constants.tilesize/2):
                    wall = map[x][y].blocked
                    if constants.Fov_enabled:
                        visible = libtcod.map_is_in_fov(fov_map, x, y)
                        if visible:
                            map[x][y].explored = True
                            if wall:
                                map_surf.blit(constants.wall_sprite, (x*constants.tilesize, y*constants.tilesize))
                            else:
                                map_surf.blit(constants.floor_sprite, (x*constants.tilesize, y*constants.tilesize))
                            if map[x][y].grave:
                                map_surf.blit(constants.grave, (x*constants.tilesize, y*constants.tilesize))
                            if map[x][y].item is not None:
                                map_surf.blit(map[x][y].item.sprite, (x*constants.tilesize, y*constants.tilesize))
                        else:
                            if map[x][y].explored:
                                if wall:
                                    map_surf.blit(constants.wall_dark_sprite, (x*constants.tilesize, y*constants.tilesize))
                                else:
                                    map_surf.blit(constants.floor_dark_sprite, (x*constants.tilesize, y*constants.tilesize))
                                if map[x][y].grave:
                                    map_surf.blit(constants.grave_dark, (x*constants.tilesize, y*constants.tilesize))
                    else:
                        if wall:
                            map_surf.blit(constants.wall_sprite, (x*constants.tilesize, y*constants.tilesize))
                        else:
                            map_surf.blit(constants.floor_sprite, (x*constants.tilesize, y*constants.tilesize))
                        if map[x][y].grave:
                            map_surf.blit(constants.grave, (x*constants.tilesize, y*constants.tilesize))
                        if not map[x][y].item is None:
                            map_surf.blit(map[x][y].item.sprite, (x*constants.tilesize, y*constants.tilesize))
    
    def make_map(self):
        global map, fov_calculate
        map = [[Map().Tile(True) for y in range(constants.map_height)] for x in range(constants.map_width)]
        fov_calculate = True
        rooms = []
        num_rooms = 0
        for r in range(constants.max_rooms):
            #valib ruumile suvalise laiuse ja kõrguse
            w = random.randint(constants.room_min_size, constants.room_max_size)
            h = random.randint(constants.room_min_size, constants.room_max_size)
            if num_rooms == 0:
                new_room = Map().Room(int(constants.map_width/2-w/2), int(constants.map_height/2-h/2), w, h)
                prev_w = w
                prev_h = h
            else:
                room = random.randint(0, len(rooms)-1) #valib suvaliselt mingi ruumi "vanemaks"
                prev_x = rooms[room].x1
                prev_y = rooms[room].y1
                
                if random.randint(0, 1) == 1:  #valib kas uus ruum teha vanamast üles ja all või paremale ja vasakule
                    if random.randint(0, 1) == 1: #loob ruumi vanemast alla
                        new_room = Map().Room(prev_x, int(prev_y+prev_h), w, h)
                        door_x = int(new_room.x1+w/2) # ukse x koordinaat, mis ühendav vanemaga
                        door_y = int(new_room.y1) # ukse y koordinaat, mis ühendav vanemaga
                        if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                            if map[door_x][door_y-1].blocked: continue
                    else: #loob ruumi vanemast üles
                        new_room = Map().Room(prev_x, int(prev_y-h), w, h)
                        door_x = int(new_room.x1+w/2)
                        door_y = int(new_room.y2)
                        if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                            if map[door_x][door_y+1].blocked: continue
                else:
                    if random.randint(0, 1) == 1: # loob ruumi vanemast paremale
                        new_room = Map().Room(int(prev_x+prev_w), prev_y, w, h)
                        door_x = int(new_room.x1)
                        door_y = int(new_room.y1+h/2)
                        if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                            if map[door_x-1][door_y].blocked: continue
                    else: #loob ruumi vanemast vasakule
                        new_room = Map().Room(int(prev_x-w), prev_y, w, h)
                        door_x = int(new_room.x2)
                        door_y= int(new_room.y1+h/2)
                        if door_x>=1 and door_y>=1 and door_x<constants.map_width and door_y< constants.map_height:
                            if map[door_x+1][door_y].blocked: continue
                if new_room.x1 < 1 or new_room.x2>=constants.map_width or new_room.y1<1 or new_room.y2>=constants.map_height: continue
                
                prev_w = w
                prev_h = h
            #nüüd vaatab kas lõikub mingi teise ruumiga
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break
            if not failed:
                #lõikepunkte pole, järelikult asetab mapile
                if num_rooms == 0:
                    Map().create_room(new_room)
                else:
                    Map().create_room(new_room, door_x, door_y)
                rooms.append(new_room)
                num_rooms += 1
        Map().create_fov_map()

    def create_fov_map(self):
        global fov_map
        fov_map = libtcod.map_new(constants.map_width, constants.map_height)
        for y in range(0, constants.map_height):
            for x in range(0, constants.map_width):
                libtcod.map_set_properties(fov_map, x, y, not map[x][y].blocked, not map[x][y].blocked)
    
    def calculate_fov(self):
        global fov_calculate, fov_map
        if fov_calculate:
            fov_calculate = False
            libtcod.map_compute_fov(fov_map, player.x, player.y, constants.fov_radius, constants.fov_light_walls, libtcod.FOV_BASIC)

class Item:
    def generate_item(self, room, x, y, item, gen_bool):
        global spawn_item
        #gen_item = 1 #random.randint(0, 1)
        #item_to_gen=random.randint(0, len(Declare_items.items)-1)
        if spawn_item:
            spawn_item = False
            
            if  gen_bool:
                item_x = random.randint(room.x1+1, room.x2-1)
                item_y = random.randint(room.y1+1, room.y2-1)
                
                (Declare_items.items[item].x, Declare_items.items[item].y) = (item_x, item_y)
        if gen_bool and x == Declare_items.items[item].x and y == Declare_items.items[item].y:
            map[x][y].item = Declare_items.items[item]

class Menus:
    def button(self, text, pos, text_color, bg_color, bg_hover_color, font, anchor = "center"):
        button_text = font.render(text, False, text_color, bg_color)
        button_text_hover = font.render(text, False, text_color, bg_hover_color)
        if anchor == "center":
            button_rect=screen.blit(button_text, (int(pos[0]-button_text.get_rect()[2]/2), int(pos[1]-button_text.get_rect()[3]/2)))
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_rect=screen.blit(button_text_hover, (int(pos[0]-button_text.get_rect()[2]/2), int(pos[1]-button_text.get_rect()[3]/2)))
        elif anchor == "right":
            button_rect=screen.blit(button_text, (int(pos[0]-button_text.get_rect()[2]), int(pos[1]-button_text.get_rect()[3])))
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_rect=screen.blit(button_text_hover, (int(pos[0]-button_text.get_rect()[2]), int(pos[1]-button_text.get_rect()[3])))
        elif anchor == "left":
            button_rect=screen.blit(button_text, (int(pos[0]), int(pos[1])))
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_rect=screen.blit(button_text_hover, (int(pos[0]), int(pos[1])))
        return button_rect

    def menu(self):
        global menu_open, screen, level
        menu_open=True
        res_bool = False
        pygame.mixer.music.stop()
        font = constants.font
        textcolor = (255, 255, 255)
        text_pause = font.render('PAUSED', False, textcolor)
        text_level = font.render('Level: '+str(level), False, textcolor)
        while menu_open:
            if not res_bool:
                screen.fill((0,0,0,0))
                screen.blit(text_level, (int(constants.screen_width/2-text_level.get_rect()[2]/2), int(constants.screen_height/2-text_pause.get_rect()[3]/2)-140))
                screen.blit(text_pause, (int(constants.screen_width/2-text_pause.get_rect()[2]/2), int(constants.screen_height/2-text_pause.get_rect()[3]/2)-300))
                resume_btn = Menus().button('RESUME', (constants.screen_width/2, constants.screen_height/2-70), textcolor, (255, 0, 0), (150, 50, 50), font)
                restart_btn = Menus().button('RESTART', (constants.screen_width/2, constants.screen_height/2), textcolor, (255, 0, 0), (150, 50, 50), font)
                quit_btn = Menus().button('QUIT', (constants.screen_width/2, constants.screen_height/2+70), textcolor, (255, 0, 0), (150, 50, 50), font)
                resolution_btn = Menus().button('RESOLUTIONS', (constants.screen_width/2, constants.screen_height/2+140), textcolor, (255, 0, 0), (150, 50, 50), font)
            elif res_bool:
                screen.fill((0,0,0,0))                
                res1 = Menus().button('1920x1080', (constants.screen_width/2, constants.screen_height/2), textcolor, (255, 0, 0), (150, 50, 50), font)
                res2 = Menus().button('1280x720', (constants.screen_width/2, constants.screen_height/2+70), textcolor, (255, 0, 0), (150, 50, 50), font)
                back = Menus().button('BACK', (constants.screen_width/2, (constants.screen_height/2)+140), textcolor, (255, 0, 0), (150, 50, 50), font)
     
                #button function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.play(-1)
                        menu_open = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if res_bool:
                            
                            if back.collidepoint(pygame.mouse.get_pos()):
                                res_bool = False
                            elif res1.collidepoint(pygame.mouse.get_pos()): #resolution controls
                                constants.screen_height=1080
                                constants.screen_width=1920
                                Camera().resolution_control(constants.screen_width, constants.screen_height)

                            elif res2.collidepoint(pygame.mouse.get_pos()):
                                constants.screen_height=720
                                constants.screen_width=1280
                                Camera().resolution_control(constants.screen_width, constants.screen_height)
                            
                        elif resume_btn.collidepoint(pygame.mouse.get_pos()):
                            Menus().resume()
                        elif restart_btn.collidepoint(pygame.mouse.get_pos()):
                            menu_open = False
                            Game().restart(True)
                        elif quit_btn.collidepoint(pygame.mouse.get_pos()):
                            Menus().quit()
                        elif resolution_btn.collidepoint(pygame.mouse.get_pos()):
                            res_bool = True
            pygame.display.update()
            
    def resume(self):
        global menu_open
        menu_open = False
    def quit(self):
        pygame.quit()
        sys.exit()

    class inv_tile:
        def __init__(self, filled, panel = None,  item=None, active=False):
            self.filled = filled
            self.active = active
            if panel:
                self.panel = panel
            self.item = item

    def inventory(self):
        global inv_open, inv, ui, add_health, active, table_spacing, row_width, equipped_items
        inv_surface.fill((0,0,0))
        rows=constants.inv_rows
        columns=constants.inv_columns
        inv_width= int(constants.screen_width/2)
        inv_height = constants.screen_height-300
        row_width=int(inv_width/(columns+1))
        row_height=row_width
        table_spacing=int((inv_width-row_width*columns)/(columns+1))
        inv_open=True
        font = constants.font
        font_small = constants.font_small
        image_size = row_width-10
        text_inv = font.render('INVENTORY', False, (66,75,84))
        textcolor=(255, 255, 255)
        active = None
        equiped_active = None
        add_health = True
        inv_tilemap = [[Menus().inv_tile(False) for y in range(rows)] for x in range(columns)]
        equiped_map = [Menus().inv_tile(False) for a in range(5)]
        height = (row_width-10)*4+table_spacing*8
        equiped_rect_start_y = int((constants.screen_height-height)/2)
        while inv_open:
            inv_surface.fill((0,0,0, 0))
            screen.fill((0,0,0,0))
            pygame.draw.rect(inv_surface, (214,187,192), (int(constants.screen_width/4), 0, int(constants.screen_width*0.5), constants.screen_height))
            inv_surface.blit(text_inv, (int(constants.screen_width/2-text_inv.get_rect()[2]/2), 30-text_inv.get_rect()[3]/2))
            list_pos=0
            use_btn = 0
            equip_btn = 0
            discard_btn=0
            unequip_btn = 0
            
            pygame.draw.rect(inv_surface, (214,187,192), (0, int((constants.screen_height-height)/2), table_spacing+row_width-10, height-10))
            for a in range(5):
                equiped_x = table_spacing/2
                equiped_y = equiped_rect_start_y+table_spacing/2+a*(table_spacing/2+row_width-10)
                equiped_map[a].panel = pygame.draw.rect(inv_surface, (225,206,122), (equiped_x,equiped_y, row_width-10, row_height-10))
                if equiped_active == equiped_map[a] or equiped_map[a].panel.collidepoint(pygame.mouse.get_pos()):
                    equiped_map[a].panel = pygame.draw.rect(inv_surface, (181,123,166), (equiped_x, equiped_y, row_width-10, row_height-10))
                if equipped_items[a]:
                    equiped_map[a].item = equipped_items[a]
                if equiped_map[a].item:
                    inv_surface.blit(pygame.transform.scale(equiped_map[a].item.inv_sprite, (image_size-10, image_size-10)), (equiped_x+5, equiped_y+5))
                if equiped_active == equiped_map[a]:
                    if equiped_map[a].item:
                        equiped_item_name = font.render(equiped_map[a].item.name, False, textcolor)
                        unequip_btn = Menus().button("UNEQUIP", (constants.screen_width-20, constants.screen_height - 90), (66,75,84), (214, 159, 42), (173, 128, 32), font, "right")
                        inv_surface.blit(equiped_item_name, (constants.screen_width-equiped_item_name.get_rect()[2] - 20, constants.screen_height-equiped_item_name.get_rect()[3]/2 - 180))
                        if equiped_active.item.dmg:
                            equiped_item_dmg = font.render("Damage: "+str(equiped_active.item.dmg), False, textcolor)
                            inv_surface.blit(equiped_item_dmg, (constants.screen_width-equiped_item_dmg.get_rect()[2] - 20, equiped_item_dmg.get_rect()[3]/2 + 100))
                        if equiped_active.item.armor:
                            equiped_item_armor = font.render("Armor: "+str(equiped_active.item.armor), False, textcolor)
                            inv_surface.blit(equiped_item_armor, (constants.screen_width-equiped_item_armor.get_rect()[2] - 20, equiped_item_armor.get_rect()[3]/2 + 100))

            for i in range(rows):
                for z in range(columns):
                    if active == inv_tilemap[i][z]:
                        if inv_tilemap[i][z].item:
                            item_name = font.render(inv_tilemap[i][z].item.name, False, textcolor)
                            if inv_tilemap[i][z].item.dmg or inv_tilemap[i][z].item.armor:
                                equip_btn = Menus().button("EQUIP", (constants.screen_width-20, constants.screen_height - 90), (66,75,84), (214, 159, 42), (173, 128, 32), font, "right")
                            else:
                                use_btn = Menus().button("USE", (constants.screen_width-20, constants.screen_height - 90), (66,75,84), (214, 159, 42), (173, 128, 32), font, "right")
                            inv_surface.blit(item_name, (constants.screen_width-item_name.get_rect()[2] - 20, constants.screen_height-item_name.get_rect()[3]/2 - 180))
                            discard_btn = Menus().button("DISCARD", (constants.screen_width-20, constants.screen_height-20), (66,75,84), (214, 159, 42), (173, 128, 32), font, "right")
                            if active.item.dmg:
                                item_dmg = font.render("Damage: "+str(active.item.dmg), False, textcolor)
                                inv_surface.blit(item_dmg, (constants.screen_width-item_dmg.get_rect()[2] - 20, item_dmg.get_rect()[3]/2 + 100))
                            if active.item.armor:
                                item_armor = font.render("Armor: "+str(active.item.armor), False, textcolor)
                                inv_surface.blit(item_armor, (constants.screen_width-item_armor.get_rect()[2] - 20, item_armor.get_rect()[3]/2 + 100))

                    x=(int(constants.screen_width/4)+table_spacing+z*(table_spacing+row_width))
                    y=50+table_spacing+i*(table_spacing+row_height)
                    inv_tilemap[i][z].panel = pygame.draw.rect(inv_surface, (225,206,122), (x, y, row_width, row_height))
                    
                    if active == inv_tilemap[i][z] or inv_tilemap[i][z].panel.collidepoint(pygame.mouse.get_pos()):
                        inv_tilemap[i][z].panel = pygame.draw.rect(inv_surface, (181,123,166), (x, y, row_width, row_height))

                        
                    if list_pos < len(inv):
                        inv_surface.blit(pygame.transform.scale(inv[list_pos].inv_sprite, (image_size, image_size)), (x+5, y+5))
                        inv_tilemap[i][z].item = inv[list_pos]
                        list_pos+=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        inv_open = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(rows):
                            for z in range(columns):
                                if inv_tilemap[i][z].panel.collidepoint(pygame.mouse.get_pos()):
                                    if inv_tilemap[i][z].item:
                                        active = inv_tilemap[i][z]
                                        equiped_active = None
                                    else:
                                        active = None
                                        equiped_active = None
                        for a in range(5):
                            if equiped_map[a].panel.collidepoint(pygame.mouse.get_pos()):
                                if equiped_map[a].item:
                                    equiped_active = equiped_map[a]
                                    active = None
                                else:
                                    equiped_active = None
                                    active = None
                        if use_btn:
                            if use_btn.collidepoint(pygame.mouse.get_pos()):
                                Item_action().use_item()
                        if equip_btn:
                            if equip_btn.collidepoint(pygame.mouse.get_pos()):
                                if active.item in inv:
                                   
                                    if active.item.slot == "shield_slot":
                                        if not equiped_map[1].item:
                                            inv.remove(active.item)
                                            equiped_map[1].item = active.item  
                                            equipped_items[1] = active.item
                                            constants.player_armor += active.item.armor 
                                    if active.item.dmg:
                                        if not equiped_map[0].item:
                                            inv.remove(active.item)
                                            equiped_map[0].item = active.item
                                            equipped_items[0] = active.item
                                            constants.player_dmg += active.item.dmg 
                                    if active.item.slot == "helmet_slot":
                                        if not equiped_map[2].item:
                                            inv.remove(active.item)
                                            equiped_map[2].item = active.item
                                            equipped_items[2] = active.item
                                            constants.player_armor += active.item.armor 
                                    if active.item.slot =="armor_slot":
                                        if not equiped_map[3].item:
                                            inv.remove(active.item)
                                            equiped_map[3].item = active.item
                                            equipped_items[3] = active.item
                                            constants.player_armor += active.item.armor 
                                    if active.item.slot == "boots_slot":
                                        if not equiped_map[4].item:
                                            inv.remove(active.item)
                                            equiped_map[4].item = active.item
                                            equipped_items[4] = active.item
                                            constants.player_armor += active.item.armor 
                                    
                                    active = None
                        if unequip_btn:
                            if unequip_btn.collidepoint(pygame.mouse.get_pos()):
                                if equiped_active.item in equipped_items:
                                    inv.append(equiped_active.item)
                                    if equiped_active.item.name == "shield":
                                        constants.player_armor -= equiped_active.item.armor
                                        equiped_map[1].item = None
                                        equipped_items[1] = 0 
                                    elif equiped_active.item.dmg:
                                        constants.player_dmg -= equiped_active.item.dmg
                                        equiped_map[0].item = None
                                        equipped_items[0] = 0
                                    elif equiped_active.item.name == "hat":
                                        constants.player_armor -= equiped_active.item.armor
                                        equiped_map[2].item = None
                                        equipped_items[2] = 0
                                    elif equiped_active.item.name =="armor":
                                        constants.player_armor -= equiped_active.item.armor
                                        equiped_map[3].item = None
                                        equipped_items[3] = 0
                                    elif equiped_active.item.name == "boots":
                                        constants.player_armor -= equiped_active.item.armor
                                        equiped_map[4].item = None
                                        equipped_items[4] = 0 
                                    equiped_active = None
                        if discard_btn:
                            if discard_btn.collidepoint(pygame.mouse.get_pos()):
                                if active.item in inv:
                                    inv.remove(active.item)
                                    active = None

            screen.blit(inv_surface, (0,0))
            pygame.display.update()

    def equiped(self, weapon, armor):
        global table_spacing, inv_surface, row_width
        height = row_width*4+table_spacing*5
        panel = pygame.Rect(0, int((constants.screen_height-height)/2), table_spacing*2+row_width, height)
        inv_surface.blit(panel, (0,0))
    
class Camera:
    def resolution_control(self, width, height):
        global screen, inv_surface, camera, player, ui
        if constants.fullscreen:
            constants.screen_height = height
            constants.screen_width = width
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            inv_surface = pygame.Surface((width, height)).convert_alpha()
            ui = pygame.Surface((width, height)).convert_alpha()
            ui.fill((0, 0, 0, 0))
            camera = Camera()
            Actor().healthBar(player.hp)
        else:
            constants.screen_height = height
            constants.screen_width = width
            screen = pygame.display.set_mode((width, height))
            inv_surface = pygame.Surface((width, height)).convert_alpha()
            ui = pygame.Surface((width, height)).convert_alpha()
            ui.fill((0, 0, 0, 0))
            camera = Camera()
            Actor().healthBar(player.hp)

class Actor:
    def __init__(self, playerrect = None, pilt = None, x = 0, y =0, hp=0, ai=None):
        self.playerrect = playerrect
        self.pilt = pilt
        self.x = x
        self.y = y
        self.ai = ai
        self.hp = hp
       
        self.target=None
        if ai:
            ai.owner = self

    def move(self, dx, dy):
        global characters
        target=None
        for object in characters:
            if (object is not self and object.x == self.x+dx and object.y == self.y+dy):
                target = object
                break
        if not map[self.x+dx][self.y+dy].blocked and  target is None:
            self.playerrect = self.playerrect.move(dx*constants.tilesize, dy*constants.tilesize)
            self.x += dx
            self.y += dy
            Map().map_to_surf()
    
    def attack(self, damage):
        global characters
        for object in characters:
            if (object is not self and (object.x == self.x+1 and object.y == self.y or 
                                        object.x == self.x-1 and object.y == self.y or 
                                        object.x == self.x and object.y == self.y+1 or 
                                        object.x == self.x and object.y == self.y-1)):
                if self !=player and object != player:
                    return False
                elif self == player:
                    hitsound = random.choice(constants.hitsounds)
                    pygame.mixer.Sound.play(hitsound)
                else:
                    object.hp -= damage
                    return True

                


    def draw(self):
        global map_surf
        if constants.Fov_enabled:
            visible = libtcod.map_is_in_fov(fov_map, self.x, self.y)
            if visible:
                map_surf.blit(self.pilt, self.playerrect)
        else:
            map_surf.blit(self.pilt, self.playerrect)

    def spawn_enemy(self, room):
        gen_enemy = random.randint(0, 1)
        if gen_enemy:
            enemy_x = random.randint(room.x1+1, room.x2-1)
            enemy_y = random.randint(room.y1+1, room.y2-1)
            characters.append(Actor(constants.enemy_pilt.get_rect(), constants.enemy_pilt, enemy_x, enemy_y, hp=100, ai=Actor().AI()))
            characters[-1].playerrect = characters[-1].playerrect.move(enemy_x*constants.tilesize, enemy_y*constants.tilesize)
    
    class AI:
        def take_turn(self):
            global characters, player
            x=random.randint(-1, 1)
            y=random.randint(-1, 1)
            
            if x**2 == y**2:
                c = random.randint(0, 1)
                if c == 0:
                    x = 0
                else:
                    y=0
            for obj in characters:
                if obj == self.owner:
                    if not self.owner.hp <= 0:
                        #damage = int(random.randint(constants.enemy_min_dmg, constants.enemy_max_dmg)*(1-constants.player_armor/100))
                        attack = self.owner.attack(constants.enemy_dmg*(1-constants.player_armor/100))
                        #print("Enemy attacked for", constants.enemy_dmg*(1-constants.player_armor/100), "damage")
                        if player.hp <0:
                            player.hp = 0
                        Actor().healthBar(player.hp)
                        if not attack :
                            self.owner.move(x,y)

    def enemy_death(self):
        global map, items, characters, player
        for obj in characters:
            if obj is not player:
                if obj.hp <=0:
                    map[obj.x][obj.y].grave = True
                    rand = random.randint(0, len(Declare_items.items)-1)
                    drop = random.randint(0, 100)
                    if Declare_items.items[rand].drop_percent <= drop:
                        map[obj.x][obj.y].item = Declare_items.items[rand]
                    Map().map_to_surf()
                    if obj in characters:
                        characters.remove(obj)
                    print(len(characters))

    def healthBar(self, health):
        global ui
        bg_bar = pygame.draw.rect(ui, (120, 30, 30), (20, constants.screen_height-30, int(constants.max_health), 20))
        
        if health >= 0.66 * constants.max_health:
            healthbar_color = constants.healthbar_color_high
        elif health >= 0.33 * constants.max_health:
            healthbar_color = constants.healthbar_color_med
        else:
            healthbar_color = constants.healthbar_color_low
            
        bar = pygame.draw.rect(ui, healthbar_color, (20, constants.screen_height-30, int((health/constants.max_health)*constants.max_health), 20))
    
    def pick_up(self, x, y):
        global inv, map
        if not map[x][y].item is None:
            if len(inv) < constants.inv_columns*constants.inv_rows:
                inv.append(map[x][y].item)
                map[x][y].item = None
                Map().map_to_surf()

class Item_action:
    def use_item(self):
        global inv, add_health, active
        if active:
            if active.item.name == 'Health potion':
                Item_action().heal_player(constants.health_potion_heal_amount)
                Actor().healthBar(player.hp)
                if active.item in inv:
                    inv.remove(active.item)
                    active = None
            elif active.item.name == 'Big Health potion':
                Item_action().heal_player(constants.big_health_potion_heal_amount)
                Actor().healthBar(player.hp)
                if active.item in inv:
                    inv.remove(active.item)
                    active = None
            elif active.item.name == 'Beer':
                Item_action().heal_player(constants.beer_heal_amount)
                Actor().healthBar(player.hp)
                if active.item in inv:
                    inv.remove(active.item)
                    active = None

    def heal_player(self, amount):
        player.hp += amount
        if player.hp>constants.max_health:
            player.hp = constants.max_health

main = Game()
main.initialize()
main.game_loop()