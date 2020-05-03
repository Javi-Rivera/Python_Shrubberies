#!/usr/bin/env python
# coding: utf-8

# In[10]:


# we import the necessary libraries 

import random

# Posible game options: 

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# We define our helper functions: 

def name_to_number(name): # This function will return an option given a number
    
    name = str(name)
      
    if name == 'rock':
        return(0)
    elif name == 'Spock':
        return(1)
    elif name == 'paper':
        return(2)
    elif name == 'lizard':
        return(3)
    elif name == 'scissors':
        return(4)
    else:
        print("Option incorrect, Please enter a different option")
        return(5)
    

def number_to_name(number): # This function will return a number given an option

    if number == 0:
        return('rock')
    elif number == 1:
        return('Spock')
    elif number == 2:
        return('paper')
    elif number == 3:
        return('lizard')
    elif number == 4:
        return('scissors')
    else:
        return("Number incorrect, Please enter a different number")

    
# We define the main function of the game: 

def rpsls(player_choice): 
    
    print('\n')
    
    print('Player chooses: %s' %(player_choice)) # show the option player choose.
    
    player_choice = name_to_number(player_choice) # Convert player choice into a number.
    
    if player_choice != 5:
        
        comp_number = random.randrange(0, 5) # The computer generates a random number which will be the option it chooses.

        comp_choice = number_to_name(comp_number) # convert the random number into a different game option.
        
        print("Computer chooses: %s" %(comp_choice)) # show the option computer choose.

        winner = (player_choice - comp_number) % 5 # with this formula we define who's the winner.

        if winner == 1 or winner == 2:
            print('\nPlayer wins!')
        elif winner == 3 or winner == 4:
            print('\nComputer wins!')
        elif winner == 0:
            print('\nPlayer and computer tie!')
        else:
            return()
    else:
        correct_choice = input("\nPlease, enter your choice: ")
        rpsls(correct_choice)
        
    
# With our main function define we make the code interactive with the player.

# We print the name, the rules and the different choices that the user can choose

print('''Welcome to Rock, Paper, Scissors, Lizard, Spock:

            The rules:

            As Sheldon Cooper explains:
            
            "Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, 
             Spock smashes scissors, scissors decapitates lizard, lizard eats paper, paper disproves Spock, 
             Spock vaporizes rock, and as it always has, rock crushes scissors."
            
            Please choose one of the different options:
            
                - rock
                - paper
                - scissors
                - lizard
                - Spock 
            
            To exit the program please type: exit''')

# we ask the user to enter an option

player = input("\nPlease, enter your choice: ")

if player == 'exit':

# If the user want to exit the program we exit the program.

    print("\nThanks for playing :)")
    
else:

# If not the program runs
    
    rpsls(player)

    rerun = 'Yes' 

    # We create a loop for the user to rerun the program as many times as it likes
    
    while rerun == 'Yes':     
    
        rerun = input("\nWant to play again? [Yes/No]: ")

        if rerun == 'Yes':
            
            second_choice = input("Please, enter your choice: ")
        
            rpsls(second_choice)
        
        else: # The user exits the loop when desires to leavve the program.
            
            print('\nThanks for playing :)')
        

