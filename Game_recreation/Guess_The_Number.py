# Import the necessary libraries

import simplegui
import random
import math

# Define Global Variables

secret_number = 0
num_range = 100
low_range = 0
number_of_guesses = 7

# Helper function for number of guesses

def max_guesses():
    
    # Calculates the max number of guesses given the range
    
    n = (num_range - low_range + 1)
    
    max_guesses = int(math.ceil(math.log(n, 2)))

    return(max_guesses)
    
# helper function to start and restart the game

def new_game():

    # initialize global variables used in your code here
    
    global secret_number, number_of_guesses
    
    number_of_guesses = max_guesses()
    
    secret_number = random.randrange(low_range, num_range)
                
    # print(num_range, secret_number)
    
    print("================================================")
    print("New Game: The range is from [0 to %d)" %(num_range))
    print("Number of remaining guesses: %d" %(number_of_guesses))
    
# define event handlers for control panel

def range100():

    # button that changes the range to [0,100) and starts a new game 
    
    global num_range
        
    num_range = 100
        
    new_game()
    
def range1000():

    # button that changes the range to [0,1000) and starts a new game     

    global num_range 
    
    num_range = 1000
        
    new_game()
    
    
def input_guess(player_guess):
    
    global number_of_guesses
    
    # main game logic goes here	
    
    player_guess = int(player_guess)
    
    print("\nGuess was %d" %(player_guess))
    
    if player_guess > secret_number:
        number_of_guesses -= 1
        print("\nNumber of remaining guesses: %d" %(number_of_guesses))
        print("Lower!")
        
    elif player_guess < secret_number:
        number_of_guesses -= 1
        print("\nNumber of remaining guesses: %d" %(number_of_guesses))
        print("Higher!")
                
    elif player_guess == secret_number:
        print("Correct!!!")
        print("")
        print("\nYou win!!!\nGood Job!!!\n")
        new_game()
    
    if number_of_guesses == 0:
        print("\n")
        print("You ran out of guesses. The secret number was: %d\nYou lose!!!\nBetter luck next time.\n" %(secret_number))
        new_game()
    
# create frame

frame = simplegui.create_frame("Guess the Number", 200, 200)
frame.add_label("Game Modes:", 150)
frame.add_button("Range is from: [0, 100)", range100, 200)
frame.add_button("Range is from: [0, 1000)", range1000, 200)
frame.add_input("Enter a guess:", input_guess, 200)

# call new_game

frame.start()
new_game()

