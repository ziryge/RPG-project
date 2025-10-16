import random

class Player:
    def __init__(self, name="Chevalier"):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.attack = 15
        self.defense = 5
        self.level = 1
        self.experience = 0
    self.inventory = {"Potion de vie": 2, "Potion de mana": 1}

    def level_up(self):
        if self.experience >= self.level * 100:
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.max_mana += 10
            self.mana = self.max_mana
            self.attack += 5
            self.defense += 2
            print(f"\n{self.name} a monté au niveau {self.level} !")
            print(f"Statistiques augmentées : Vie +20, Mana +10, Attaque +5, Défense +2")

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            if item == "Potion de vie":
                heal = min(50, self.max_health - self.health)
                self.health += heal
                print(f"Vous avez utilisé une Potion de vie et soigné {heal} PV !")
            elif item == "Potion de mana":
                mana_restore = min(25, self.max_mana - self.mana)
                self.mana += mana_restore
                print(f"Vous avez utilisé une Potion de mana et restauré {mana_restore} Mana !")
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            print("Vous n'avez pas cet objet !")

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
        Enemy("Gobelin", 50, 10, 2, 20, {"Potion de vie": 1}),
        Enemy("Orque", 80, 15, 5, 35, {"Potion de mana": 1}),
        Enemy("Dragon", 150, 25, 10, 50, {"Potion de vie": 2, "Potion de mana": 1})
    ]
    return random.choice(enemies)

def fight(player, enemy):
    defending = False
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name} PV : {player.health}/{player.max_health} | Mana : {player.mana}/{player.max_mana}")
        print(f"{enemy.name} PV : {enemy.health}")
        print("\n[1] Attaquer")
        print("[2] Sort")
        print("[3] Défendre")
        print("[4] Utiliser un objet")
        print("[5] Fuir")

        try:
            action = int(input("Action: "))
        except ValueError:
            print("Entrée invalide ! Veuillez entrer un nombre.")
            continue

        if action == 1:  # Attaque
            damage = max(1, player.attack - enemy.defense)
            enemy.health -= damage
            print(f"Vous attaquez le {enemy.name} et infligez {damage} dégâts !")

        elif action == 2:  # Spell
            if player.mana >= 10:
                print("[1] Geler (10 Mana) - Réduit l'attaque de l'ennemi le tour suivant")
                print("[2] Feu (15 Mana) - Inflige des dégâts de feu")
                print("[3] Épines (20 Mana) - Inflige des dégâts et peut provoquer une hémorragie")
                try:
                    spell = int(input("Sort : "))
                except ValueError:
                    print("Choix de sort invalide !")
                    continue

                if spell == 1 and player.mana >= 10:
                    player.mana -= 10
                    print("Vous lancez Geler ! L'attaque de l'ennemi est réduite le prochain tour.")
                    # Par simplicité, réduit les dégâts ce tour-ci
                    damage = max(1, (player.attack + 10) - enemy.defense)
                    enemy.health -= damage
                    print(f"Vous infligez {damage} dégâts avec Geler !")
                elif spell == 2 and player.mana >= 15:
                    player.mana -= 15
                    damage = max(1, (player.attack + 15) - enemy.defense)
                    enemy.health -= damage
                    print(f"Vous lancez Feu et infligez {damage} dégâts !")
                elif spell == 3 and player.mana >= 20:
                    player.mana -= 20
                    damage = max(1, (player.attack + 20) - enemy.defense)
                    enemy.health -= damage
                    print(f"Vous lancez Épines et infligez {damage} dégâts !")
                    if random.random() < 0.5:
                        enemy.health -= 10
                        print("Les épines provoquent une hémorragie ! L'ennemi subit 10 dégâts supplémentaires.")
                else:
                    print("Pas assez de mana ou sort invalide !")
                    continue
            else:
                print("Pas assez de mana !")

        elif action == 3:  # Défendre
            defending = True
            print("Vous vous préparez à défendre contre la prochaine attaque !")

        elif action == 4:  # Utiliser un objet
            if player.inventory:
                print("Inventaire :")
                for item, count in player.inventory.items():
                    print(f"- {item} : {count}")
                item_choice = input("Quel objet utiliser ? ").strip()
                player.use_item(item_choice)
            else:
                print("Votre inventaire est vide !")
            continue  # Passer le tour de l'ennemi

        elif action == 5:  # Fuir
            if random.random() < 0.5:
                print("Vous vous êtes enfui avec succès !")
                return False  # Combat non gagné
            else:
                print("Vous n'avez pas réussi à fuir !")

        else:
            print("Action invalide !")
            continue

        # Enemy turn
        if enemy.health > 0:
            damage = max(1, enemy.attack - (player.defense if not defending else player.defense * 2))
            player.health -= damage
            print(f"Le {enemy.name} vous attaque et inflige {damage} dégâts !")
            defending = False

    return player.health > 0

def main():
    print("Bienvenue dans le RPG du Donjon !")
    player_name = input("Entrez le nom de votre personnage (ou appuyez sur Entrée pour 'Chevalier') : ").strip()
    player = Player(player_name if player_name else "Chevalier")

    dungeon_level = 1
    enemies_defeated = 0

    while player.health > 0 and dungeon_level <= 5:
    print(f"\n=== Niveau du donjon {dungeon_level} ===")
    print("Vous vous enfoncez plus profondément dans le donjon...")

        # Random encounter
        if random.random() < 0.7:  # 70% chance of encounter
            enemy = create_enemy()
            print(f"Un {enemy.name} apparaît !")

            if fight(player, enemy):
                print(f"Vous avez vaincu le {enemy.name} !")
                player.experience += enemy.xp_reward
                enemies_defeated += 1

                # Loot
                for item, count in enemy.loot.items():
                    if item in player.inventory:
                        player.inventory[item] += count
                    else:
                        player.inventory[item] = count
                    print(f"Vous avez trouvé {count} {item} !")

                player.level_up()
            else:
                print("Vous avez été vaincu...")
                break
        else:
            print("Vous trouvez une pièce tranquille. Vous vous reposez et récupérez un peu de vie.")
            player.health = min(player.max_health, player.health + 20)
            player.mana = min(player.max_mana, player.mana + 10)

        # Check for level progression
        if enemies_defeated >= dungeon_level * 3:
            dungeon_level += 1
            print(f"\nVous avez terminé le niveau {dungeon_level-1} ! Passage au niveau {dungeon_level}...")

    if player.health > 0:
        print("\nFélicitations ! Vous avez terminé le donjon !")
        print(f"Statistiques finales : Niveau {player.level}, {enemies_defeated} ennemis vaincus.")
    else:
        print("\nFin de la partie. Vous avez été vaincu dans le donjon.")

if __name__ == "__main__":
    main()

