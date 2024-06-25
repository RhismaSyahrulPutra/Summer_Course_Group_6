import random

def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1 + dice2, dice1, dice2

def play_game():
    print("Welcome to the Craps Game!")
    print("Rules of Game:")
    print("1. Roll two six-sided dice.")
    print("2. If the sum is 7 or 11 on the first roll, you win.")
    print("3. If the sum is 2, 3, or 12 on the first roll, you lose.")
    print("4. Any other sum becomes your 'point'.")
    print("5. Keep rolling until you 'make your point' or roll a 7 (lose).")
    print()
    
    #Ask the Player to start the Craps Game
    input("Press Enter to roll the dice.")
    
    #First Roll
    sum_dice, dice1, dice2 = roll_dice()
    print(f"You rolled: {dice1} + {dice2} = {sum_dice}")
    
    if sum_dice in {7, 11}:
        print("Congratulations! You win!")
    elif sum_dice in {2, 3, 12}:
        print("Oh no! You lose!")
    else:
        point = sum_dice
        print(f"Your point is: {point}. Keep rolling to make your point.")
        
        while True:
            input("Press Enter to roll the dice...")
            sum_dice, dice1, dice2 = roll_dice()
            print(f"You rolled: {dice1} + {dice2} = {sum_dice}")

            if sum_dice == point:
                print("Congratulations! You made your point and win!")
                break
            elif sum_dice == 7:
                print("Oh no! You rolled a 7 and lose!")
                break

# run the game
if __name__ == "__main__":
    play_game()
