class Potion:
    def __init__(self, name, healing, description):
        self.name = name
        self.healing = healing
        self.description = description

    def use(self, character):
        pass

class Healing_potion(Potion):
    def __init__(self, name="Healing Potion", heling=30, description="Restores 30 HP"):
        super().__init__(name, heling, description)

    def use(self, character):
        if character.health >= character.max_health:
            print("Your health is already full!")
        else:
            old_health = character.health
            character.health = min(character.max_health, character.health + self.healing)
            health_restored = character.health - old_health
            print(f"You restored {health_restored} HP!")
            return health_restored
