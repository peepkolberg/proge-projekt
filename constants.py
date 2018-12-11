import pygame
import os
import random
dir = os.path.dirname(os.path.abspath(__file__))
pygame.init()

#SCREEN
screen_width = 1280
screen_height = 720
resolutions = {'1920x1080':(1920, 1080), '1366x720':(1366, 720), '800x600':(800, 600)}
white_transparent= 255, 255,255,0
fullscreen=False


#MAP
tilesize = 64
map_width = 20
map_height = 20
room_max_size = 6
room_min_size = 4
max_rooms = 200 # mitu ruumi PROOVIB genereerida

floor_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "floor.png"))
wall_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "wall.png"))
floor_dark_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "floor_dark.png"))
wall_dark_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "wall_dark.png"))
player_pilt = pygame.image.load(os.path.join(dir,"Data", "Sprites", "character.png"))
enemy_pilt = pygame.image.load(os.path.join(dir,"Data", "Sprites", "enemy.png"))
grave = pygame.image.load(os.path.join(dir,"Data", "Sprites", "grave.png"))
grave_dark = pygame.image.load(os.path.join(dir,"Data", "Sprites", "grave.png"))

floor_sprite = pygame.transform.scale(floor_sprite,(tilesize, tilesize))
wall_sprite = pygame.transform.scale(wall_sprite,(tilesize, tilesize))
floor_dark_sprite = pygame.transform.scale(floor_dark_sprite,(tilesize, tilesize))
wall_dark_sprite = pygame.transform.scale(wall_dark_sprite,(tilesize, tilesize))
player_pilt = pygame.transform.scale(player_pilt, (tilesize, tilesize))
enemy_pilt = pygame.transform.scale(enemy_pilt, (tilesize, tilesize))
grave = pygame.transform.scale(grave, (tilesize, tilesize))
grave_dark = pygame.transform.scale(grave_dark, (tilesize, tilesize))

#UI
healthbar_color_low = 255, 0,0
healthbar_color_med = 255, 255, 0
healthbar_color_high = 0, 255, 0
font = pygame.font.Font('Data\\fonts\\VCR_OSD_MONO_1.001.ttf', 40)
font_small = pygame.font.Font('Data\\fonts\\VCR_OSD_MONO_1.001.ttf', 20)
font_very_small = pygame.font.Font('Data\\fonts\\VCR_OSD_MONO_1.001.ttf', 12)
white = 255, 255, 255

#PLAYER
player_dmg = 5
player_armor = 0
max_health = 200
player_min_dmg = 0
player_max_dmg = 10
enemy_min_dmg = 0
enemy_max_dmg = 10
#ENEMY
enemy_dmg = 4
min_enemies = 3

#FOV
Fov_enabled = True
fov_radius = 6
fov_light_walls = True


#ITEMS
inv_rows = 4
inv_columns = 4
health_potion_heal_amount = 30
big_health_potion_heal_amount = 60
beer_heal_amount = 15


sword_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","sword.png"))
sword_sprite_inv = pygame.transform.scale(sword_sprite, (50, 50))
sword_sprite = pygame.transform.scale(sword_sprite, (tilesize,tilesize))
shield_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","shield.jpg"))
shield_sprite_inv = pygame.transform.scale(shield_sprite, (50, 50))
shield_sprite = pygame.transform.scale(shield_sprite, (tilesize,tilesize))
beer_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","beer.png"))
beer_sprite_inv = pygame.transform.scale(beer_sprite, (50, 50))
beer_sprite = pygame.transform.scale(beer_sprite, (tilesize,tilesize))
book_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","book.png"))
book_sprite_inv = pygame.transform.scale(book_sprite, (50, 50))
book_sprite = pygame.transform.scale(book_sprite, (tilesize,tilesize))
boots_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","boots.png"))
boots_sprite_inv = pygame.transform.scale(boots_sprite, (50, 50))
boots_sprite = pygame.transform.scale(boots_sprite, (tilesize,tilesize))
flame_sword_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","flame_sword.png"))
flame_sword_sprite_inv = pygame.transform.scale(flame_sword_sprite, (50, 50))
flame_sword_sprite = pygame.transform.scale(flame_sword_sprite, (tilesize,tilesize))
hat_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","hat.png"))
hat_sprite_inv = pygame.transform.scale(hat_sprite, (50, 50))
hat_sprite = pygame.transform.scale(hat_sprite, (tilesize,tilesize))
potion_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","potion.png"))
potion_sprite_inv = pygame.transform.scale(potion_sprite, (50, 50))
potion_sprite = pygame.transform.scale(potion_sprite, (tilesize,tilesize))
potion2_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","potion2.png"))
potion2_sprite_inv = pygame.transform.scale(potion2_sprite, (50, 50))
potion2_sprite = pygame.transform.scale(potion2_sprite, (tilesize,tilesize))
bag_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","bag.png"))
bag_sprite_inv = pygame.transform.scale(bag_sprite, (50, 50))
bag_sprite = pygame.transform.scale(bag_sprite, (tilesize,tilesize))
armor_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","armor1.png"))
armor_sprite_inv = pygame.transform.scale(armor_sprite, (50, 50))
armor_sprite = pygame.transform.scale(armor_sprite, (tilesize,tilesize))