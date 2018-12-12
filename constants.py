import pygame
import os
import random
dir = os.path.dirname(os.path.abspath(__file__))
pygame.init()

#SCREEN
screen_width = 1280
screen_height = 720
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

#AUDIO
background = "Data/audio/background.wav"
dead = "Data/audio/dead.wav"
hit1 = pygame.mixer.Sound("Data/audio/hit1.wav")
hit2 = pygame.mixer.Sound("Data/audio/hit2.wav")
hit3 = pygame.mixer.Sound("Data/audio/hit3.wav")
hitsounds = [hit1, hit2, hit3]

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
cake_heal_amount = 20
cookie_heal_amount = 10


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
leather_armor_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","leather_armor.png"))
leather_armor_sprite_inv = pygame.transform.scale(leather_armor_sprite, (50, 50))
leather_armor_sprite = pygame.transform.scale(leather_armor_sprite, (tilesize,tilesize))
leather_boots_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","leather_boots.png"))
leather_boots_sprite_inv = pygame.transform.scale(leather_boots_sprite, (50, 50))
leather_boots_sprite = pygame.transform.scale(leather_boots_sprite, (tilesize,tilesize))
leather_helmet_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","leather_helmet.png"))
leather_helmet_sprite_inv = pygame.transform.scale(leather_helmet_sprite, (50, 50))
leather_helmet_sprite = pygame.transform.scale(leather_helmet_sprite, (tilesize,tilesize))
stick_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","stick.png"))
stick_sprite_inv = pygame.transform.scale(stick_sprite, (50, 50))
stick_sprite = pygame.transform.scale(stick_sprite, (tilesize,tilesize))
metal_armor_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","metal_armor.png"))
metal_armor_sprite_inv = pygame.transform.scale(metal_armor_sprite, (50, 50))
metal_armor_sprite = pygame.transform.scale(metal_armor_sprite, (tilesize,tilesize))
metal_boots_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","metal_boots.png"))
metal_boots_sprite_inv = pygame.transform.scale(metal_boots_sprite, (50, 50))
metal_boots_sprite = pygame.transform.scale(metal_boots_sprite, (tilesize,tilesize))
metal_helmet_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","metal_helmet.png"))
metal_helmet_sprite_inv = pygame.transform.scale(metal_helmet_sprite, (50, 50))
metal_helmet_sprite = pygame.transform.scale(metal_helmet_sprite, (tilesize,tilesize))
good_sword_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","good_sword.png"))
good_sword_sprite_inv = pygame.transform.scale(good_sword_sprite, (50, 50))
good_sword_sprite = pygame.transform.scale(good_sword_sprite, (tilesize,tilesize))
cookie_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","cookie.png"))
cookie_sprite_inv = pygame.transform.scale(cookie_sprite, (50, 50))
cookie_sprite = pygame.transform.scale(cookie_sprite, (tilesize,tilesize))
cake_sprite = pygame.image.load(os.path.join(dir,"Data",  "Sprites","cake.png"))
cake_sprite_inv = pygame.transform.scale(cake_sprite, (50, 50))
cake_sprite = pygame.transform.scale(cake_sprite, (tilesize,tilesize))