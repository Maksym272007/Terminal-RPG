import random

# Difficult class Enemy
class Enemy:
    def __init__(self, name, health, damage, experience_reward):
        self.name = name
        self.health = health
        self.damage = damage
        self.experience_reward = experience_reward

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def attack(self):
        if self.health <= 0:
            print(f"{self.name} is dead!")
            return 0
        
        print(f"{self.name} deald {self.damage} damage!")
        return self.damage

    def show_info(self):
        print("-" * 15)
        print(f"Name: {self.name}")
        print(f"HP: {self.health}")
        print("-" * 15)

class Goblin(Enemy):
    def __init__(self, name = "Goblin", health = 60, damage = 10, experience_reward = 30):
        super().__init__(name, health, damage, experience_reward)

class Skeleton(Enemy):
    def __init__(self, name = "Skeleton", health = 80, damage = 15, experience_reward = 50):
        super().__init__(name, health, damage, experience_reward)

class Orc(Enemy):
    def __init__(self, name = "Orc", health = 150, damage = 25, experience_reward = 100):
        super().__init__(name, health, damage, experience_reward)

    def attack(self):
        if self.health <= 0:
            print(f"{self.name} is dead!")
            return 0

        crit = random.random() < 0.3
        if crit:
            crit_damage = self.damage * 2
            print(f"{self.name} deald critical damage! You take {crit_damage} damage!")
            return crit_damage
        else:
            return super().attack()

class Dragon(Enemy):
    def __init__(self, name="Dragon", health=500, damage=40, experience_reward = 300):
        super().__init__(name, health, damage, experience_reward)

    def attack(self):
        if self.health <= 0:
            print(f"{self.name} is dead!")
            return 0
    
        fire_breath = random.random() < 0.2
        if fire_breath:
            fire_breath_damage = 80
            print(f"{self.name} attacks with fire breath! You take {fire_breath_damage} damage!")
            return fire_breath_damage
        else:
            return super().attack()