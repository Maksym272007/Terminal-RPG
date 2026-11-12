from characters import Warrior, Mage, Archer, Character
from weapons import Weapon, Magic_sword, Magic_staff, generate_rarity
from enemies import Goblin, Skeleton, Orc, Dragon
from items import Healing_potion
import random
import json

# Start the battle
def start_battle(character):
    battle_result = None

    # Create new enemy
    random_enemy = random.choices(
        [Goblin(), Skeleton(), Orc(), Dragon()], 
        [40, 35, 20, 5], 
        k=1)
    enemy = random_enemy[0]

    # Fight
    print(f"You met a new enemy: {enemy.__class__.__name__}")
    character_defends = False
    while character.health > 0 and enemy.health > 0:
        print("\n" + "-" * 35)
        print("       BATTLE\n")
        print(f"Your HP: {character.health} | {enemy.__class__.__name__} HP: {enemy.health}\n")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Run away")
        
        try:
            action = int(input("Select an action: "))
            print("\n")
            if action == 1:
                # Character attack
                character_attack = character.attack()
                enemy.take_damage(character_attack)
            elif action == 2:
                character_defends = True
                print("You defended yourself!")
            elif action == 3:
                if not character.inventory_items:
                    print("Your items inventory is empty!")
                    continue
                else:
                    character.show_items()
                    try:
                        character_selection = int(input(f"\nSelect item: "))
                        if 1 <= character_selection <= len(character.inventory_items):
                            potion = character.inventory_items[character_selection - 1]
                            print(f"Selected: {potion.name}")
                            health_restored = potion.use(character)
                            if health_restored is None:
                                continue
                            else:
                                character.inventory_items.pop(character_selection - 1)
                        else:
                            print("Selelted clause is no detected.")
                            continue
                    except ValueError:
                        print("There is no such clause!")
                        continue
            elif action == 4:
                run_away_chance = random.random() < 0.5
                if run_away_chance:
                    battle_result = "escaped"
                else:
                    print("You failed to escape from the battle")
            else:
                print("Enter a number from 1 to 4!")
                continue
        except ValueError:
            print("Enter a number!")
            continue

        # If enemy HP == 0
        if enemy.health > 0 and not battle_result == "escaped":
            enemy_attack = enemy.attack()

            # IF character defends == True
            if character_defends:
                # Enemy atack with defends
                enemy_attack_with_defends = enemy_attack // 2
                character_defends = False

                print("Incoming damage reduced by 50%.")
                print(f"You received {enemy_attack_with_defends} damage instead of {enemy_attack}!")
                character.take_damage(enemy_attack_with_defends)
            else:
                character.take_damage(enemy_attack)

        # Battle result
        if character.health <= 0:
            battle_result = "defeat"
            print("You were defeated...")
        elif battle_result == "escaped":
            print("	You escaped from the battle!")
        elif enemy.health <= 0:
            battle_result = "victory"
            print("	You successfully defeated the enemy!")

            # Gain XP
            character.gain_experience(enemy.experience_reward)
            print(f"You take {enemy.experience_reward} EXP!")

            # Gain Weapon
            if isinstance(enemy, Goblin):
                random_weapon = [
                    Weapon("Rusty sword", 20, generate_rarity(enemy)),
                    Weapon("Old shortbow", 15, generate_rarity(enemy))
                ]
            elif isinstance(enemy, Skeleton):
                random_weapon = [
                    Weapon("Shortsword", 30, generate_rarity(enemy)),
                    Weapon("Shortbow", 25, generate_rarity(enemy))
                ]
            elif isinstance(enemy, Orc):
                random_weapon = [
                    Weapon("Greatclub", 40, generate_rarity(enemy)),
                    Weapon("Longsword", 50, generate_rarity(enemy))
                ]
            elif isinstance(enemy, Dragon):
                random_weapon = [
                    Magic_staff("Magic staff", 60, generate_rarity(enemy)),
                    Magic_sword("Magic sword", 100, generate_rarity(enemy))
                ]

            victory_weapon = random.choice(random_weapon)
            character.add_weapon(victory_weapon)

            battle_reward(victory_weapon, enemy)

# Battle reward
def battle_reward(weapon, enemy):
    print("\n" + "=" * 35)
    print("          BATTLE REWARD")
    print("=" * 35)
    print(f"Enemy defeated: {enemy.__class__.__name__}")
    print(f"Weapon found: {weapon.weapon_name}")
    print(f"Rarity: {weapon.get_rarity_color()}")
    print(f"Base damage: {weapon.damage}")
    print(f"Final damage: {weapon.get_damage()}")
    print("=" * 35)

# Select character
def character_select(character_name):
    while True:
        print("Select class:")
        print("")
        print("1. Warrior")
        print("2. Mage")
        print("3. Archer")
        print("")

        try:
            # Select cherecter
            character_choise = int(input("Your choise: "))

            if character_choise == 1:
                sword = Weapon("Sword", 35)
                character = Warrior(character_name, sword)

            elif character_choise == 2:
                staff = Weapon("Staff", 50)
                character = Mage(character_name, staff)

            elif character_choise == 3:
                bow = Weapon("Bow", 30)
                character = Archer(character_name, bow)

            else:
                print("There is no such clause!")
                continue

            # Подтверждение персонажа
            character.show_info()
            confirm_choise = input(f"Are you sure you want to select this class? (Type 'Yes' to confirm): ")
            if confirm_choise.strip().lower() == "yes":
                character.add_item(Healing_potion())
                character.add_item(Healing_potion())
                return character
            
        except ValueError:
            print("Enter a number from 1 to 3!") 

# Save game
def save_game(character):
    save_data = character.to_dict()
    
    with open("saves/save.json", "w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=4, ensure_ascii=False)

    print("The game was saved!")

# Load game
def load_game():
    with open("saves/save.json", "r", encoding="utf-8") as file:
        save_data = json.load(file)

    return save_data

# New Game / Load Game
while True:
        print("======= PYTHON RPG =======\n")
        print("1. New game")
        print("2. Load game\n")
        try:
            game_choise = int(input("Do you want load the game?: "))
            if game_choise == 2:
                data = load_game()
                character = Character.from_dict(data)
                if character is not None:
                    break
                else:
                    print("The save file is broken! \nCreate a new game.")
            elif game_choise == 1:
                print("======= CREATING A CHARACTER =======\n")
                character_name = input("Enter the character name: ")
                character = character_select(character_name)
                break
            else:
                print("Enter the number 1 for a new game or 2 to download a game!")
        except ValueError:
            print("Enter the number!")
        except json.JSONDecodeError:
            print("The save file is broken! \nCreate a new game.")
        except FileNotFoundError:
            print("The file was not found.")

# Main menu
while True:
    print("======= PYTHON RPG =======\n")
    print("1. Character info")
    print("2. Select weapon")
    print("3. Inventory")
    print("4. Start the battle")
    print("5. Exit")

    try:
        select_action = int(input("Select an action: "))
        if select_action == 1:
            character.show_info()

        elif select_action == 2:
            character.equip_weapon()

        elif select_action == 3:
            character.show_items()

        elif select_action == 4:
            if character.health <= 0:
                print("You can't fight! The character is dead!")
            else:
                start_battle(character)

        elif select_action == 5:
            save_game(character)
            break

        else:
            print("There is no such clause!")
    except ValueError:
        print("Enter a number from 1 to 5!")