import constants
class Item():
            def __init__(self, name, sprite,  x, y, inv_sprite, drop_percent, dmg = None, armor = None):
                self.name = name
                self.sprite = sprite
                self.x  = x
                self.y = y
                self.inv_sprite = inv_sprite
                self.drop_percent = drop_percent
                self.dmg = dmg
                self.armor = armor
                
sword= Item("sword", constants.sword_sprite, 0, 0, constants.sword_sprite_inv, 20, dmg = 5)
shield= Item("shield", constants.shield_sprite, 0, 0, constants.shield_sprite_inv,20, armor = 10)
armor= Item("armor", constants.armor_sprite, 0, 0, constants.armor_sprite_inv, 10, armor = 15)
bag= Item("Bag", constants.bag_sprite, 0, 0, constants.bag_sprite_inv, 30)
beer= Item("Beer", constants.beer_sprite, 0, 0, constants.beer_sprite_inv, 40)
book= Item("book", constants.book_sprite, 0, 0, constants.book_sprite_inv, 30)
boots= Item("boots", constants.boots_sprite, 0, 0, constants.boots_sprite_inv, 30, armor = 5)
flame_sword= Item("flame sword", constants.flame_sword_sprite, 0, 0, constants.flame_sword_sprite_inv, 5, dmg = 10)
hat= Item("hat", constants.hat_sprite, 0, 0, constants.hat_sprite_inv, 30, armor = 5)
potion= Item("Health potion", constants.potion_sprite, 0, 0, constants.potion_sprite_inv, 20)
potion2= Item("Big Health potion", constants.potion2_sprite, 0, 0, constants.potion2_sprite_inv, 20)

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