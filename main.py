import random

class Player:
    def __init__(self, name="Knight"):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.attack = 15
        self.defense = 5
        self.level = 1
        self.experience = 0
        self.inventory = {"Health Potion": 2, "Mana Potion": 1}

    def level_up(self):
        if self.experience >= self.level * 100:
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.max_mana += 10
            self.mana = self.max_mana
            self.attack += 5
            self.defense += 2
            print(f"\n{self.name} leveled up to level {self.level}!")
            print(f"Stats increased: Health +20, Mana +10, Attack +5, Defense +2")

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            if item == "Health Potion":
                heal = min(50, self.max_health - self.health)
                self.health += heal
                print(f"You used a Health Potion and healed {heal} HP!")
            elif item == "Mana Potion":
                mana_restore = min(25, self.max_mana - self.mana)
                self.mana += mana_restore
                print(f"You used a Mana Potion and restored {mana_restore} Mana!")
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            print("You don't have that item!")

class Enemy:
    def __init__(self, name, health, attack, defense, xp_reward, loot=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.loot = loot or {}

def create_enemy():
    enemies = [
        Enemy("Goblin", 50, 10, 2, 20, {"Health Potion": 1}),
        Enemy("Orc", 80, 15, 5, 35, {"Mana Potion": 1}),
        Enemy("Dragon", 150, 25, 10, 50, {"Health Potion": 2, "Mana Potion": 1})
    ]
    return random.choice(enemies)

def fight(player, enemy):
    defending = False
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name} HP: {player.health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
        print(f"{enemy.name} HP: {enemy.health}")
        print("\n[1] Attack")
        print("[2] Spell")
        print("[3] Defend")
        print("[4] Use Item")
        print("[5] Run")

        try:
            action = int(input("Action: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if action == 1:  # Attack
            damage = max(1, player.attack - enemy.defense)
            enemy.health -= damage
            print(f"You attack the {enemy.name} for {damage} damage!")

        elif action == 2:  # Spell
            if player.mana >= 10:
                print("[1] Freeze (10 Mana) - Reduces enemy attack next turn")
                print("[2] Fire (15 Mana) - Deals fire damage")
                print("[3] Spikes (20 Mana) - Deals damage and may cause bleed")
                try:
                    spell = int(input("Spell: "))
                except ValueError:
                    print("Invalid spell choice!")
                    continue

                if spell == 1 and player.mana >= 10:
                    player.mana -= 10
                    print("You cast Freeze! The enemy's attack is reduced next turn.")
                    # For simplicity, just reduce damage this turn
                    damage = max(1, (player.attack + 10) - enemy.defense)
                    enemy.health -= damage
                    print(f"You deal {damage} damage with Freeze!")
                elif spell == 2 and player.mana >= 15:
                    player.mana -= 15
                    damage = max(1, (player.attack + 15) - enemy.defense)
                    enemy.health -= damage
                    print(f"You cast Fire and deal {damage} damage!")
                elif spell == 3 and player.mana >= 20:
                    player.mana -= 20
                    damage = max(1, (player.attack + 20) - enemy.defense)
                    enemy.health -= damage
                    print(f"You cast Spikes and deal {damage} damage!")
                    if random.random() < 0.5:
                        enemy.health -= 10
                        print("The spikes cause bleeding! Enemy takes 10 extra damage.")
                else:
                    print("Not enough mana or invalid spell!")
                    continue
            else:
                print("Not enough mana!")

        elif action == 3:  # Defend
            defending = True
            print("You prepare to defend against the next attack!")

        elif action == 4:  # Use Item
            if player.inventory:
                print("Inventory:")
                for item, count in player.inventory.items():
                    print(f"- {item}: {count}")
                item_choice = input("Which item to use? ").strip()
                player.use_item(item_choice)
            else:
                print("Your inventory is empty!")
            continue  # Skip enemy turn

        elif action == 5:  # Run
            if random.random() < 0.5:
                print("You successfully ran away!")
                return False  # Fight not won
            else:
                print("You failed to run away!")

        else:
            print("Invalid action!")
            continue

        # Enemy turn
        if enemy.health > 0:
            damage = max(1, enemy.attack - (player.defense if not defending else player.defense * 2))
            player.health -= damage
            print(f"The {enemy.name} attacks you for {damage} damage!")
            defending = False

    return player.health > 0

def main():
    print("Welcome to the Dungeon RPG!")
    player_name = input("Enter your character's name (or press Enter for default 'Knight'): ").strip()
    player = Player(player_name if player_name else "Knight")

    dungeon_level = 1
    enemies_defeated = 0

    while player.health > 0 and dungeon_level <= 5:
        print(f"\n=== Dungeon Level {dungeon_level} ===")
        print("You venture deeper into the dungeon...")

        # Random encounter
        if random.random() < 0.7:  # 70% chance of encounter
            enemy = create_enemy()
            print(f"A wild {enemy.name} appears!")

            if fight(player, enemy):
                print(f"You defeated the {enemy.name}!")
                player.experience += enemy.xp_reward
                enemies_defeated += 1

                # Loot
                for item, count in enemy.loot.items():
                    if item in player.inventory:
                        player.inventory[item] += count
                    else:
                        player.inventory[item] = count
                    print(f"You found {count} {item}(s)!")

                player.level_up()
            else:
                print("You were defeated...")
                break
        else:
            print("You find a quiet room. You rest and recover some health.")
            player.health = min(player.max_health, player.health + 20)
            player.mana = min(player.max_mana, player.mana + 10)

        # Check for level progression
        if enemies_defeated >= dungeon_level * 3:
            dungeon_level += 1
            print(f"\nYou cleared level {dungeon_level-1}! Moving to level {dungeon_level}...")

    if player.health > 0:
        print("\nCongratulations! You cleared the dungeon!")
        print(f"Final Stats: Level {player.level}, {enemies_defeated} enemies defeated.")
    else:
        print("\nGame Over. You were defeated in the dungeon.")

if __name__ == "__main__":
    main()

