# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    
    # Starts a new game
    
    global state, turn, exposed, cards, cards_index, deck
    
    # creation of deck
    
    list_1 = range(8)
    list_2 = range(8)

    list_1.extend(list_2)

    deck = list_1
    
    # Setting the different variables and list for each game
    
    random.shuffle(deck)  
    
    state = 0
    
    turn = 0
    
    exposed = [False, False, False, False, False, False, False, False, False, 
           False, False, False, False, False, False, False]

    # auxiliar lists for the game
    
    cards = [None, None]
    cards_index = [None, None]

    label.set_text("Turns = %d" %(turn))

    return deck, state, turn, exposed, cards, cards_index
    
# define event handlers

def mouseclick(pos):

    # add game state logic here
    
    global exposed, state, cards, cards_index, turn
    
    click = list(pos)
    
    click[0] = click[0] // 50
    
    if state == 0:
    
        if exposed[click[0]] == False:
            
            exposed[click[0]] = True
            
            if cards[0] == None:
                
                cards[0] = deck[click[0]]
                cards_index[0] = click[0]
                
                state = 1
            
                turn += 1
            
    elif state == 1:
        
        if exposed[click[0]] == False:
            
            exposed[click[0]] = True
            
            if cards[1] == None:
                
                cards[1] = deck[click[0]]
                cards_index[1] = click[0]
        
                state = 2   
        
    else:
        
        if cards[0] != cards[1]:
            
            exposed[cards_index[0]] = False
            exposed[cards_index[1]] = False
            
        cards = [None, None]
        cards_index = [None, None]
        
        if exposed[click[0]] == False:
            
            exposed[click[0]] = True
            
            if cards[0] == None:
                
                cards[0] = deck[click[0]]
                cards_index[0] = click[0]
        
                state = 1
        
                turn += 1

    label.set_text("Turns = %d" %(turn))
                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    for i in range(len(deck)):
            
        factor = 2 * 25 * i
        
        polygon_pos = [(factor, 0), (factor + 50, 0), (factor + 50, 100),
                       (factor, 100)]
        
        # Set the sides of the cards
        
        if exposed[i] == False:
            
            card_color = "Green"
            text_color = "Green"
            
        elif exposed[i] == True:
            
            card_color = "White"
            text_color = "Black"
        
        # Draw the cards
        
        canvas.draw_polygon(polygon_pos, 1, "Black", card_color)
        canvas.draw_text(str(deck[i]), [(15 + factor), 60], 40, text_color)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric