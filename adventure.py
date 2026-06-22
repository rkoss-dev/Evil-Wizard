import random

# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health  
        self.attack_power = attack_power
        # Track cooldowns for Ability 1 and Ability 2
        self.cooldowns = {1: 0, 2: 0} 

    def get_cooldown_text(self, ability_idx):
        """Helper method to format the cooldown status for the menu."""
        cd = self.cooldowns[ability_idx]
        if cd > 0:
            return f"[Cooldown: {cd} turn{'s' if cd > 1 else ''}]"
        return "[Ready]"

    def decrement_cooldowns(self):
        """Reduces all active cooldowns by 1 at the end of a turn."""
        for key in self.cooldowns:
            if self.cooldowns[key] > 0:
                self.cooldowns[key] -= 1

    def attack(self, opponent, variance=0.2):
        low_damage = self.attack_power * (1 - variance)
        high_damage = self.attack_power * (1 + variance)
        damage = round(random.uniform(low_damage, high_damage))
        opponent.health -= damage
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")

    def heal(self, variance=0.3):
        base_heal_value = 30
        low_heal_value = base_heal_value * (1 - variance)
        high_heal_value = base_heal_value * (1 + variance)
        recovery = round(random.uniform(low_heal_value, high_heal_value))
        proposed_health = self.health + recovery
        self.health = min(proposed_health, self.max_health)
        print(f"{self.name} drinks a potion and recovers {recovery} health! Current health: {self.health}")

    def use_special(self, opponent):
        return False


# Warrior class
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        
    def use_special(self, opponent):
        print("\n--- Warrior Abilities ---")
        print(f"1. Brutal Strike (Deals 1.5x damage) {self.get_cooldown_text(1)}")
        print(f"2. Reckless Swing (Deals 2.0x damage, take 15 recoil) {self.get_cooldown_text(2)}")
        print("3. Cancel")
        
        choice = input("Choose an ability (1-3): ")
        if choice == '1':
            if self.cooldowns[1] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} uses **Brutal Strike**!")
            damage = int(self.attack_power * 1.5)
            opponent.health -= damage
            print(f"It lands heavily, dealing {damage} damage to {opponent.name}!")
            self.cooldowns[1] = 3 # Will decrement to 2 at the end of this turn
            return True
            
        elif choice == '2':
            if self.cooldowns[2] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} uses **Reckless Swing**!")
            damage = int(self.attack_power * 2.0)
            recoil = 15
            opponent.health -= damage
            self.health -= recoil
            print(f"A wild swing deals {damage} damage to {opponent.name}!")
            print(f"{self.name} takes {recoil} recoil damage from the exertion!")
            self.cooldowns[2] = 2 # Will decrement to 1 at the end of this turn
            return True
        else:
            return False


# Mage class
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)
        
    def use_special(self, opponent):
        print("\n--- Mage Abilities ---")
        print(f"1. Unstable Fireball (Wild damage variance: 0.5x to 2.0x) {self.get_cooldown_text(1)}")
        print(f"2. Vampiric Drain (Deals damage, heals you for 100% of it) {self.get_cooldown_text(2)}")
        print("3. Cancel")
        
        choice = input("Choose an ability (1-3): ")
        if choice == '1':
            if self.cooldowns[1] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} casts **Unstable Fireball**!")
            damage = round(random.uniform(self.attack_power * 0.5, self.attack_power * 2.0))
            opponent.health -= damage
            print(f"The fireball explodes for {damage} damage!")
            self.cooldowns[1] = 2 
            return True
            
        elif choice == '2':
            if self.cooldowns[2] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} casts **Vampiric Drain**!")
            damage = self.attack_power
            opponent.health -= damage
            self.health = min(self.max_health, self.health + damage)
            print(f"{self.name} drains {damage} health from {opponent.name}!")
            self.cooldowns[2] = 4 
            return True
        else:
            return False


# Thief class
class Thief(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30)
        
    def use_special(self, opponent):
        print("\n--- Thief Abilities ---")
        print(f"1. Flurry of Knives (Hits twice for 0.6x damage each) {self.get_cooldown_text(1)}")
        print(f"2. Shadow Strike (50% chance to deal 2.5x damage, or miss) {self.get_cooldown_text(2)}")
        print("3. Cancel")
        
        choice = input("Choose an ability (1-3): ")
        if choice == '1':
            if self.cooldowns[1] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} uses **Flurry of Knives**!")
            for i in range(2):
                damage = round(self.attack_power * 0.6)
                opponent.health -= damage
                print(f"Knife {i+1} hits for {damage} damage!")
            self.cooldowns[1] = 3
            return True
            
        elif choice == '2':
            if self.cooldowns[2] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} attempts a **Shadow Strike**!")
            if random.random() > 0.5:
                damage = int(self.attack_power * 2.5)
                opponent.health -= damage
                print(f"A critical hit! {self.name} strikes from the shadows for {damage} damage!")
            else:
                print(f"{self.name} lunges from the shadows but misses entirely!")
            self.cooldowns[2] = 2 
            return True
        else:
            return False


# Paladin class
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=20)
        
    def use_special(self, opponent):
        print("\n--- Paladin Abilities ---")
        print(f"1. Holy Smite (Deals damage and heals you for 50% of it) {self.get_cooldown_text(1)}")
        print(f"2. Lay on Hands (Heals you for a massive 60 HP) {self.get_cooldown_text(2)}")
        print("3. Cancel")
        
        choice = input("Choose an ability (1-3): ")
        if choice == '1':
            if self.cooldowns[1] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} uses **Holy Smite**!")
            damage = self.attack_power
            opponent.health -= damage
            heal_amount = round(damage * 0.5)
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} strikes for {damage} damage and is healed by the light for {heal_amount} HP!")
            self.cooldowns[1] = 3
            return True
            
        elif choice == '2':
            if self.cooldowns[2] > 0:
                print("\nAbility is on cooldown!")
                return False
            print(f"\n{self.name} uses **Lay on Hands**!")
            heal_amount = 60
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"A blinding light surrounds {self.name}, restoring {heal_amount} health!")
            self.cooldowns[2] = 4
            return True
        else:
            return False


# EvilWizard class
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=200, attack_power=20)

    def regenerate(self):
        regen_value = random.randint(5, 10)
        self.health = min(self.max_health, self.health + regen_value)
        print(f"{self.name} passively regenerates {regen_value} health! Current health: {self.health}")

    def take_turn(self, opponent):
        self.regenerate()
        roll = random.random()

        if roll < 0.05: 
            print(f"\n{self.name} channels dark energy and casts **Annihilation**!")
            damage = int(self.attack_power * 3.0) 
            opponent.health -= damage
            print(f"A massive beam of void energy hits {opponent.name} for {damage} damage!")
        elif roll < 0.20: 
            print(f"\n{self.name} summons a **Chaos Storm**!")
            damage = int(self.attack_power * 1.8) 
            opponent.health -= damage
            print(f"Lightning strikes {opponent.name} for {damage} damage!")
        elif roll < 0.50: 
            print(f"\n{self.name} casts **Siphon Life**!")
            damage = self.attack_power
            heal = int(damage * 0.5)
            opponent.health -= damage
            self.health = min(self.max_health, self.health + heal)
            print(f"The wizard drains {damage} health from {opponent.name} and heals himself for {heal}!")
        else:
            self.attack(opponent)


def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Thief") 
    print("4. Paladin")  

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Thief(name)
    elif class_choice == '4':
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)


def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Use Healing Potion")
        print("4. View Stats")

        choice = input("Choose an action: ")

        if choice == '1':
            player.attack(wizard)
        elif choice == '2':
            turn_used = player.use_special(wizard)
            if not turn_used:
                # If they backed out OR chose an ability on cooldown, restart turn
                continue
        elif choice == '3':
            player.heal()
        elif choice == '4':
            player.display_stats()
            print(f"Enemy {wizard.name}'s Health: {max(0, wizard.health)}/{wizard.max_health}")
            continue
        else:
            print("Invalid choice. Try again.")
            continue

        # A successful action completes. Decrement cooldown timers.
        player.decrement_cooldowns()

        if wizard.health <= 0:
            break
        if player.health <= 0:
            break

        print("\n--- Enemy Turn ---")
        wizard.take_turn(player)

    if player.health <= 0:
        print(f"\n{player.name} has been defeated! Game Over.")
    elif wizard.health <= 0:
        print(f"\nVictory! {wizard.name} has been defeated by {player.name}!")


def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()