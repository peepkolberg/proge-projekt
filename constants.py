import pygame
import os
import random
dir = os.path.dirname(os.path.abspath(__file__))
pygame.init()

#SCREEN
screen_width = 800
screen_height = 600

white_transparent= 255, 255,255,0


#MAP
tilesize = 20
map_width = int(screen_width/tilesize)
map_height = int(screen_height/tilesize)
room_max_size = 8
room_min_size = 5
max_rooms = 200 # mitu ruumi PROOVIB genereerida

floor_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "floor.png"))
floor_sprite = pygame.transform.scale(floor_sprite,(tilesize, tilesize))
wall_sprite = pygame.image.load(os.path.join(dir,"Data", "Sprites", "wall.png"))
wall_sprite = pygame.transform.scale(wall_sprite,(tilesize, tilesize))
player_pilt = pygame.image.load(os.path.join(dir,"Data", "Sprites", "character.png"))
player_pilt = pygame.transform.scale(player_pilt, (tilesize, tilesize))
enemy_pilt = pygame.image.load(os.path.join(dir,"Data", "Sprites", "enemy.png"))
enemy_pilt = pygame.transform.scale(enemy_pilt, (tilesize, tilesize))
grave = pygame.image.load(os.path.join(dir,"Data", "Sprites", "grave.png"))
grave = pygame.transform.scale(grave, (tilesize, tilesize))

#UI
healthar_color = 255, 0,0

#PLAYER
player_dmg = 10
#ENEMY
enemy_dmg = 10


#ITEMS
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