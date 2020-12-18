# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables

in_play = False
outcome = ""
score = 0

# define globals for cards

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:

    """Creates a card based on a suit and rank"""
    
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    
    """Creates a group of cards"""
    
    def __init__(self):
        
        self.hand = []
                
    def __str__(self):
        
        self.str_hand = ""
        
        for i in range(len(self.hand)):
            
            self.str_hand += "%s " %str(self.hand[i])
        
        return "Hand contains: %s" %(self.str_hand)
    
    def add_card(self, card):
        
        # adds a card to the current hand
        
        self.hand.append(card)
        
    def get_value(self):
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        self.hand_value = 0
        
        ace = False
        
        for i in self.hand:
    
            if ace == False:
            
                self.hand_value += VALUES[Card.get_rank(i)]    
            
                if Card.get_rank(i) == "A":
                    
                    self.hand_value += 10
                    
                    ace = True
                    
            elif ace == True:
                
                self.hand_value += VALUES[Card.get_rank(i)]
                
        if self.hand_value > 21 and ace == True:
            
            self.hand_value -= 10
                                
        return self.hand_value

    def draw(self, canvas, pos):
        
        for card in self.hand:
            pos[0] = pos[0] + CARD_SIZE[0] + 5
            card.draw(canvas, pos)
        
# define deck class 
class Deck:
    
    """Creates a deck of cards"""
    
    def __init__(self):
        
        self.deck = []
        
        for suit in SUITS:
            for rank in RANKS:
                
                self.deck.append(Card(suit, rank))
                
    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)
        
    def deal_card(self):
        
        return self.deck.pop()     
        
    def __str__(self):
        
        self.str_deck = ""
        
        for i in range(len(self.deck)):
            
            self.str_deck += "%s " %str(self.deck[i])
            
        return "Deck contains: %s" %(self.str_deck)

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if in_play: 
        score -= 1
        
    # Create deck:
    deck = Deck()
    deck.shuffle()
    outcome = ""

    # Creates hands for each player:
    player_hand = Hand()
    dealer_hand = Hand()
    
    # Deals initial card for player and dealer:
    dealer_hand.add_card(deck.deal_card()) # add first card to dealer hand
    player_hand.add_card(deck.deal_card()) # add first card to player hand
    dealer_hand.add_card(deck.deal_card()) # add second card to dealer hand
    player_hand.add_card(deck.deal_card()) # add second card to player hand

    in_play = True
    
def hit():
    
    global outcome, score, in_play
    
    if in_play == True:
    # if the hand is in play, hit the player
    
        if player_hand.get_value() <= 21:

            player_hand.add_card(deck.deal_card())

        # if busted, assign a message to outcome, update in_play and score

        else:

            in_play = False
            outcome = "You have busted!, Dealer Wins!!!"
            score -= 1


def stand():

    global outcome, game, in_play, score
    if in_play == True:
        in_play = False

        if player_hand.get_value() > 21:

            outcome = "You have busted!, Dealer Wins!!!"
            score -= 1

        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        else: 

            while dealer_hand.get_value() < 17:

                dealer_hand.add_card(deck.deal_card())

            if dealer_hand.get_value() <= 21:

                if player_hand.get_value() <= dealer_hand.get_value():

                    outcome = "Dealer Wins!!!"
                    score -= 1

                else:

                    outcome = "Player Wins!!!"
                    score += 1

            else:

                outcome = "Dealer have busted!, You Win!!!"
                score += 1
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    
    # test to make sure that card.draw works, replace with your code below
    polygon_pos = [(10, 10), (590, 10), (590, 100), (10, 100)]
    canvas.draw_polygon(polygon_pos, 1, "Black", "#8b0000")
    canvas.draw_text("Blackjack", [190, 70], 50, "White")
    canvas.draw_text(outcome, [100, 140], 35, "Black")
    canvas.draw_text("Dealer", [100, 220], 30, "Black")
    canvas.draw_text("Player", [100, 420], 30, "Black")
    canvas.draw_text("Score is: %s" %(score), [400, 220], 30, "Black" )
    player_hand.draw(canvas, [8, 450])
    dealer_hand.draw(canvas, [8, 250])
    
    if in_play == True:

        canvas.draw_text("Hit or Stand?", [200, 420], 30, "Black")
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (122, 298), CARD_SIZE)

    else:
        
        canvas.draw_text("New Deal?", [200, 420], 30, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric