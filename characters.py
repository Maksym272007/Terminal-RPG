import weapons
import items

# Difficult class Character
class Character:
    def __init__(self, name, health, max_health, weapon):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.level = 1
        self.experience = 0
        self.weapon = weapon
        self.inventory = [weapon]
        self.inventory_items = []

    def show_info(self):
        print("-" * 15)
        print(f"Name: {self.name}")
        print(f"HP: {self.health}/{self.max_health}")
        print(f"Equipped weapon: {self.weapon.weapon_name}")
        print(f"Damage: {self.weapon.damage}")
        print(f"LVL: {self.level}")
        print(f"EXP: {self.experience}")
        print("-" * 15)

    def show_items(self):
        if not self.inventory_items:
            print("Your inventory is empty!")
        else:
            for index, item in enumerate(self.inventory_items):
                print(f"{index + 1}. Item: {item.name} | Description: {item.description}")

    def show_inventory(self):
        print("======= Inventory =======\n")
        for index, weapon in enumerate(self.inventory):
             print(f"{index + 1}. {weapon.weapon_name} | Damage: {weapon.get_damage()} | Rarity: {weapon.get_rarity_color()} | Durability: {weapon.durability}")

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            # Level up
            self.experience -= 100
            self.level += 1

            # Ability Score Improvement
            self.max_health += 20
            self.health = self.max_health

    def add_item(self, item):
        self.inventory_items.append(item)

    def add_weapon(self, weapon):
        self.inventory.append(weapon)

    def equip_weapon(self):
        self.show_inventory()
        try:
            weapon_choise = int(input("Select weapon: "))

            if 1 <= weapon_choise <= len(self.inventory):
                equiped_weapon = self.inventory[weapon_choise - 1]
                self.weapon = equiped_weapon
                print(f"You habe equipped: {self.weapon.weapon_name}")
            else:
                print("There are no weapons in this cell!")
        except ValueError:
            print("Write number!")

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def attack(self):
        damage = self.weapon.use()
        return damage

    def to_dict(self):
        inventory_data = []

        for weapon in self.inventory:
            weapon_data = {
                "weapon_name": weapon.weapon_name,
                "damage": weapon.damage,
                "rarity": weapon.rarity,
                "durability": weapon.durability
            }

            inventory_data.append(weapon_data)

        items_data = []

        for item in self.inventory_items:
            item_data = {
                "name": item.name,
                "healing": item.healing,
                "description": item.description
            }

            items_data.append(item_data)

        save_dict = {
                    "name": self.name,
                    "health": self.health,
                    "max_health": self.max_health,
                    "level": self.level,
                    "experience": self.experience,
                    "class": self.__class__.__name__,
                    "inventory": inventory_data,
                    "inventory_items": items_data,
                    "equipped_weapon": self.weapon.weapon_name
                }
        return save_dict

    @classmethod
    def from_dict(cls, data):
        # Data
        character_class = data["class"]
        name = data["name"]
        max_health = data["max_health"]
        health = data["health"]
        level = data["level"]
        experience = data["experience"]

        # Equipped_weapon
        temp_weapon = weapons.Weapon("Temp_weapon", 0)
        equipped_weapon = data["equipped_weapon"]

        # Inventory
        inventory = data["inventory"]
        new_inventory = []

        # Inventory items
        items_data = data.get("inventory_items", [])
        new_items = []

        # Load character
        if character_class == "Warrior":
            character = Warrior(name, temp_weapon)
        
        elif character_class == "Mage":
            character = Mage(name, temp_weapon)
        
        elif character_class == "Archer":
            character = Archer(name, temp_weapon)
        
        else:
            print("Your class is not detected.")
            return None
        
        character.max_health = max_health
        character.health = health
        character.level = level
        character.experience = experience

        # Load inventory
        for weapon in inventory:
            weapon_data = weapons.Weapon(weapon["weapon_name"], weapon["damage"], weapon["rarity"], weapon["durability"])
            new_inventory.append(weapon_data)

        character.inventory = new_inventory

        # Load inventory items
        for item in items_data:
            item_data = items.Healing_potion(item["name"], item["healing"], item["description"])
            new_items.append(item_data)

        character.inventory_items = new_items
        
        # Load equipped weapon
        for weapon in character.inventory:
            if weapon.weapon_name == equipped_weapon:
                character.weapon = weapon

        return character

class Warrior(Character):
    def __init__(self, name, weapon):
        super().__init__(name, 150, 150, weapon)
        
class Mage(Character):
    def __init__(self, name, weapon):
        super().__init__(name, 80, 80, weapon)

class Archer(Character):
    def __init__(self, name, weapon):
        super().__init__(name, 100, 100, weapon)
