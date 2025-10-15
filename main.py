# FIGHT TEMPLATE
fight_active = True
while fight_active:
    print("You are a knight, you are going through a dungen, if you mess up it can affect you severely")
    fight_action = int(input("[1] Attack \n[2] Spell \n[3] Defend \n Action: "))

life = 100
enemy_life = 200
if fight_action == 1:
    # attack code
    print("You attack the enemy!")
    print(enemy_life - 20)

elif fight_action == 2:
    # spell code
    print("You cast a spell!")
    cast_decision = int(input("[1] Freeze \n [2] Fire \n [3] Spikes \n Spell: "))


elif fight_action == 3:
    # defend code
    print("You defend against attacks!")
    # Add your defend logic here

else:
    print("Please input a valid option")

