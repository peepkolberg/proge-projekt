import constants
class Item():
            def __init__(self, name, sprite,  x, y, inv_sprite, drop_percent, dmg = None, armor = None, slot = None, heal = None, description = None):
                self.name = name
                self.sprite = sprite
                self.x  = x
                self.y = y
                self.inv_sprite = inv_sprite
                self.drop_percent = drop_percent
                self.dmg = dmg
                self.armor = armor
                self.slot = slot
                self.heal = heal
                self.description = description

#WEAPONS               
sword= Item("sword", constants.sword_sprite, 0, 0, constants.sword_sprite_inv, 20, dmg = 5, description = "Stick them with the pointy end")
flame_sword= Item("Flame sword", constants.flame_sword_sprite, 0, 0, constants.flame_sword_sprite_inv, 5, dmg = 10, description = "AHHHH!!!! It's on FIRE!!")
good_sword = Item("Sharp sword", constants.good_sword_sprite, 0, 0, constants.good_sword_sprite_inv, 5, dmg = 7, description = "A rally sharp sword")
stick = Item("Stick", constants.stick_sprite, 0, 0, constants.stick_sprite_inv, 5, dmg = 2, description = "Somewhat more useful than using bare hands")

#ARMOR
shield= Item("shield", constants.shield_sprite, 0, 0, constants.shield_sprite_inv,20, armor = 10, slot = "shield_slot", description = "If I hide behind the shield no one will see me")

armor= Item("Exotic armor", constants.armor_sprite, 0, 0, constants.armor_sprite_inv, 5, armor = 15, slot = "armor_slot", description = "It's really heavy")
metal_armor = Item("Metal armor", constants.metal_armor_sprite, 0, 0, constants.metal_armor_sprite_inv, 10, armor = 10, slot = "armor_slot", description = "Slightly rusty")
leather_armor = Item("Leather armor", constants.leather_armor_sprite, 0, 0, constants.leather_armor_sprite_inv, 10, armor = 5, slot = "armor_slot", description = "Already falling apart")

boots= Item("boots", constants.boots_sprite, 0, 0, constants.boots_sprite_inv, 30, armor = 2, slot = "boots_slot", description = "These boots really smell")
metal_boots = Item("Metal boots", constants.metal_boots_sprite, 0, 0, constants.metal_boots_sprite_inv, 10, armor = 7, slot = "boots_slot", description = "Starting to fill with some kind of yellow liquid")
leather_boots = Item("Leather boots", constants.leather_boots_sprite, 0, 0, constants.leather_boots_sprite_inv, 10, armor = 3, slot = "boots_slot", description = "These are quite nice slippers")


hat= Item("hat", constants.hat_sprite, 0, 0, constants.hat_sprite_inv, 30, armor = 5, slot = "helmet_slot", description = "OOOOO!!! I'm a wizard")
metal_helmet = Item("Metal helmet", constants.metal_helmet_sprite, 0, 0, constants.metal_helmet_sprite_inv, 10, armor = 7, slot = "helmet_slot", description = "So shiny the monsters can see their reflections")
leather_helmet = Item("Leather helmet", constants.leather_helmet_sprite, 0, 0, constants.leather_helmet_sprite_inv, 10, armor = 4, slot = "helmet_slot", description = "Something clever about a leather helmet")

#HEALING ITEMS
potion= Item("Health potion", constants.potion_sprite, 0, 0, constants.potion_sprite_inv, 20, heal = constants.health_potion_heal_amount, description = "Drink up!")
potion2= Item("Big Health potion", constants.potion2_sprite, 0, 0, constants.potion2_sprite_inv, 20, heal = constants.big_health_potion_heal_amount, description = "Smells a bit funny")
beer= Item("Beer", constants.beer_sprite, 0, 0, constants.beer_sprite_inv, 40, heal = constants.beer_heal_amount, description = "Beer is the answer but I can't remember the question")
cake = Item("Cake", constants.cake_sprite, 0, 0, constants.cake_sprite_inv, 40, heal = constants.cake_heal_amount, description = "The cake is a lie")
cookie = Item("Cookie", constants.cookie_sprite, 0, 0, constants.cookie_sprite_inv, 40, heal = constants.cookie_heal_amount, description = "Peek-A-Boo! Here's some cookies for you!")


items=[]
items.append(sword)
items.append(flame_sword)
items.append(good_sword)
items.append(stick)

items.append(shield)

items.append(armor)
items.append(metal_armor)
items.append(leather_armor)

items.append(boots)
items.append(metal_boots)
items.append(leather_boots)

items.append(hat)
items.append(metal_helmet)
items.append(leather_helmet)

items.append(beer)
items.append(potion)
items.append(potion2)
items.append(cake)
items.append(cookie)