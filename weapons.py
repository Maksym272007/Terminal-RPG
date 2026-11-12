import random

# Generate rarity for weapon
def generate_rarity(enemy):
    rarity_weights = {
        "Goblin": [70, 20, 8, 2, 0],
        "Skeleton": [50, 25, 15, 8, 2],
        "Orc": [30, 30, 20, 15, 5],
        "Dragon": [10, 20, 25, 25, 20]
    }

    random_rarity = random.choices(
        ["Common", "Uncommon", "Rare", "Epic", "Legendary"], 
        weights = rarity_weights[enemy.__class__.__name__], 
        k=1)
    return random_rarity[0]

# Difficult class weapon
class Weapon():
    def __init__(self, weapon_name, damage, rarity="Common", durability=100):
        self.weapon_name = weapon_name
        self.damage = damage
        self.rarity = rarity
        self.durability = durability
        
    def use(self):
        if self.durability == 0:
            print(f"{self.weapon_name} is broken!.")
            return 0
        else:
            print(f"{self.weapon_name} deals {self.get_damage()} damage!")
            self.durability = max(0, self.durability - 10)
            return self.get_damage()

    def get_rarity_color(self):
        rarity_colors_dict = {
            "Common": "\033[37m",
            "Uncommon": "\033[32m",
            "Rare": "\033[34m",
            "Epic": "\033[35m",
            "Legendary": "\033[33m"
        }
        try:
            rarity_color = rarity_colors_dict[self.rarity]
        except KeyError:
            rarity_color = rarity_colors_dict["Common"]

        weapon_rarity_color = (f"{rarity_color}{self.rarity}\033[0m") 
        return weapon_rarity_color

    def get_damage(self):
        multipliers = {
            "Common": 1.0,
            "Uncommon": 1.2,
            "Rare": 1.5,
            "Epic": 1.7,
            "Legendary": 2
        }

        try:
            damage = self.damage * multipliers[self.rarity]
        except KeyError:
            damage = self.damage * multipliers["Common"]
        return damage

    def show_info(self):
        print(f"{self.weapon_name}| Rarity: {self.get_rarity_color()} | Damage: {self.get_damage()} | Durability: {self.durability}")

class Magic_sword(Weapon):
    def __init__(self, weapon_name, damage, rarity="Common", durability=300):
        super().__init__(weapon_name, damage, rarity, durability)

    def use(self):
        if self.durability == 0:
            print(f"{self.weapon_name} is broken!")
            return 0
        else:
            crit = random.random() < 0.1
            if crit:
                crit_damage = self.get_damage() * 2
                print(f"{self.weapon_name} deal critical damage! You deals {crit_damage} damage!")
                self.durability = max(0, self.durability - 10)
                return crit_damage
            else:
                return super().use()

class Magic_staff(Weapon):
    def __init__(self, weapon_name, damage, rarity="Common", durability=200):
        super().__init__(weapon_name, damage, rarity, durability)

    def use(self):
        if self.durability == 0:
            print(f"{self.weapon_name} is brocken.")
            return 0
        else:
            magic_attack = random.random()
        
            if magic_attack < 0.1:
                magic_damage = self.get_damage() * 2
                print(f"You cast Fireball! You deals {magic_damage} damage!")
            
            elif magic_attack < 0.3:
                magic_damage = self.get_damage() * 1.5
                print(f"You cast Shatter! You deals {magic_damage} damage!")

            elif magic_attack < 0.6:
                magic_damage = self.get_damage() * 1.2
                print(f"You cast Ice Knife! You deals {magic_damage} damage!")
            else:
                return super().use()

            self.durability = max(0, self.durability - 10)
            return magic_damage

