"""
A Blackjack Simulator. This one has betting!

See blackjack() function, the main function at the bottom, for rules.

-Zachary Avant
"""

import random

class Wallet:
    """
    A class used for placing bets.
    Wallet objects may: spend money using spend_money,
                        add money using add_money,
                        display current amount using show_money
    """
    def __init__(self, money):
        self.__money = money
    def spend_money(self, amount):
        if self.__money < amount:
            print('Not enough money!')
        else:
            self.__money -= amount
    def add_money(self, amount):
        self.__money += amount
    def show_money(self): 
        #I know show_ instead of get_ is not conventional,
        # but get_money implies the wrong thing
        return self.__money
    def __str__(self):
        return f'A stack of money containing ${self.__money}'
    

##############################################################################
# Deck Manipulation Functions #
###############################
def create_deck():
    """
    Creates a standard deck of cards. 
    A standard deck has 52 cards of 4 suits.
    A card's color doesn't matter in Black Jack.
    There are 13 faces in each suit:
        9 numbers from 2 to 10, and Jack, Queen, King, and Ace.
    Point values are exlained in calculate_points(user_score, dealer_score).
    
    Is a helper function for: draw(deck, hand) -- only if the deck runs out.
                              blackjack() 
    
    Inputs: None.
    Outputs: deck, a list of tuples which each contain a face and a suit.
    """
    deck = []
    faces = [2,3,4,5,6,7,8,9,10,
            'Jack','Queen','King','Ace']
    suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
    for face in faces:
        for suit in suits:
            # Creates a card-tuple and adds it to the deck.
            deck.append((face, suit))
            
    return deck
    
def deal(deck):
    """
    Used for the initial deal. 
    Removes 2 cards from the deck and puts them in the player's hand.
    
    Helper Functions: draw(deck, hand)
    
    Is a helper function for: blackjack_helper(deck)
    
    Inputs: The deck
    Outputs: The deck, the hand. 
    """      
    hand = []
    for n in range(2):    
        deck, hand = draw(deck, hand)
        
    return deck, hand

def draw(deck, hand):
    """
    Draws a card.
    Removes 1 random card from the deck and puts it in a hand. 
    Remakes the deck if it runs out.
    
    Helper Functions: create_deck() -- only used if the deck runs out.
    
    Is a helper function for: deal(deck),
                              blackjack_helper(deck)
    
    Inputs: deck, hand (any hand of cards)
    Outputs: deck, the hand with one card added. 
    """ 
    # Remakes deck if it becomes empty.
    if len(deck) == 0:
        deck = create_deck()
        
    i = random.randint(0,len(deck)-1)
    card = deck.pop(i)
    hand.append(card)
    
    return deck, hand

##############################################################################
# Point Calculation Functions #
###############################

def calculate_points(hand):
    """
    Calculates the point-value of a hand.
    Numbered cards are worth the number on them.
    Kings, Queens, and Jacks are worth 10 points.
    Aces are worth either 1 point or 11 points, whichever is most beneficial.
    
    Helper Functions: card_value(card)
                      ace_hand_value(ace_count, hand_value)
    Is a helper function for: blackjack_helper()
    
    Inputs: hand (a list representing the cards in a hand)
    Outputs: The integer value of the hand
    """       
    hand_value = 0
    ace_count = 0  
    
    #Finds value of non-Ace cards, and counts number of Aces.
    for card in hand:
        if card[0] == 'Ace':
            ace_count += 1
        else:
            # Calls card_value function to evaluate the card.
            hand_value += card_value(card) 
    
    #Ace card present
    if ace_count > 0:
        return ace_hand_value(ace_count, hand_value)
    
    #Implied "if ace_count == 0:"
    return hand_value

def card_value (card):
    """
    Finds the value of cards other than the Ace, which is handled by ace_value.
    
    Is a helper function to: calculate_points(hand)
    
    Input: card
    Output: the integer point value of the card
    """
    value = card[0]
    if value in ['Jack','Queen','King']:
        return 10
    if value in [2,3,4,5,6,7,8,9,10]:
        return value
    else:
        raise 'CardValueError'

def ace_hand_value(ace_count, hand_value):
    """
    Returns the best value of a hand with one or more ace card.
    An Ace can be worth either 1 or 11 points. 
    Their value may change over the course of a game, 
        so the value must be recalculated at times.
    If you have two Aces, you never want both to be 11 (11+11 > 21, you lose).
        Thus, a player will only have one 11 at most. The rest must be 1s.
        The only question is whether there will be an 11 or not.
        If the 11 can be in play without going over 21, you'd want the 11.
     
    Is a helper function to: calculate_points(hand)    
        
    Inputs: ace_count (the number of Aces in a hand)
            hand_value (the current value of the hand without Aces)
    Outputs: case1 (Ace is 11 points),
             - or -
             case2 (Ace is 1 point), whichever is best. 

    """
    #case1, the case where the Ace in question is worth 11 points,
    #    doesn't reduce 11 to 10 in order to be more clear about where these
    #    values are coming from. ace_count is reduced by 1 to offset 11 being
    #    counted separately. 
    case1 = hand_value + 11 + (ace_count - 1)
    if case1 <= 21:
        return case1
    
    #Implied "if case1 > 21:"
    #case2 is the case where the Ace in question is worth 1 point.
    case2 = hand_value + ace_count
    return case2

##############################################################################
# Printing/Pretty Functions #
#############################
def pretty_hand(hand):
    """
    Converts the tuple-hand into a prettier string-hand.
    
    Is a helper function to: reveal_one(hand), 
                             blackjack_helper(deck)
    
    Input: hand, with cards stored as tuples.
    Output: string_hand, with cards stored as strings.
    """
    string_hand = ''
    for card in hand:
        string_hand += f'{str(card[0])} of {card[1]}, '
    return string_hand.strip(', ')

def reveal_one(hand):
    """
    Reveals the first card in a given hand.
    
    Is a helper function for: blackjack_helper(deck)
    
    Inputs: A hand.
    Outputs: None. Prints a single card from the hand.
    """
    # Turns the hand into a single string, then splits it into multiple cards.
    hand = pretty_hand(hand).split(',')
    # Displays the first card in the hand.
    print("The dealer turns over a card from their hand:", 
          hand[0])

##############################################################################
# Primary Functions #
#####################
def blackjack_helper(deck):

    # Deals 4 cards in total, two to the user and two to the dealer.
    deck, user_hand = deal(deck)
    deck, dealer_hand = deal(deck)
    
    # Your hand
    print('Your hand:', pretty_hand(user_hand))
    
    # Turns over one of the dealer's cards.
    reveal_one(dealer_hand)
    
    # Get dealer's score and find out if they won on the first draw.
    dealer_score = calculate_points(dealer_hand)
    if dealer_score == 21:
        print('Bad luck!')
        print('Dealer\'s hand:', pretty_hand(dealer_hand))
        return -1, 'Dealer has 21. You lose!'

    # Your turn
    response = ''
    while response != 'stand':
        # Calculates your points & see if you won or lost
        user_score = calculate_points(user_hand)
        if user_score > 21:
            print('Dealer\'s hand:', pretty_hand(dealer_hand))
            return -1, 'You have over 21. You lose.'
        
        # Hit, stand, or quit + validation loops
        response = input('Enter hit, stand, or quit. \n: ')
        while response.lower() not in ('hit','stand','quit'):
            # Validation loop.
            print('Must enter hit, stand, or quit.')
            response = input(': ')
            
        response = response.lower()
        if response == 'quit':
            return None, 'You forfeit.'
        if response == 'hit':
            deck, user_hand = draw(deck, user_hand)
            
        print('\nYour hand:', pretty_hand(user_hand))
        
    # Dealer's turn.
    if dealer_score > 21:
        print('Dealer\'s hand:', pretty_hand(dealer_hand))
        return +1, 'Dealer has over 21 points. You win!'
    # Dealer draws until their score is 17 or more.
    while dealer_score < 17:
        deck, dealer_hand = draw(deck, dealer_hand)
        dealer_score = calculate_points(dealer_hand)
        if dealer_score == 21:
            print('Dealer\'s hand:', pretty_hand(dealer_hand))
            return -1, 'Dealer has 21. You lose!'
        if dealer_score > 21:
            print('Dealer\'s hand:', pretty_hand(dealer_hand))
            return +1, 'Dealer has over 21. You win!'
        
    if user_score == 21: 
        print('Dealer\'s hand:', pretty_hand(dealer_hand))
        return +1, 'You have 21. You win!'
    
    # Compare scores to see who won
    if user_score > dealer_score:
        print('Dealer\'s hand:', pretty_hand(dealer_hand))
        return +1,\
            f'You win! You had {user_score} and the dealer had {dealer_score}.'
    if user_score <= dealer_score:
        # Dealer wins ties.
        print('Dealer\'s hand:', pretty_hand(dealer_hand))
        return -1,\
            f'You lose! You had {user_score} and the dealer had {dealer_score}.'
           
def blackjack():
    """
    Simulates a game of Blackjack between a dealer (the computer) and a player.
   
    No input. Everything is handled inside the program.
    No output. Merely prints relevant card information and prints winner/loser.

    Blackjack Rules:
        -Each player is dealt 2 cards.
        -Each card is worth a certain number of points (see calculate_value())
        -The player's goal is to get as close to 21 as possible.
        -If a player goes over 21 points, they lose.
        -You may "hit" (draw another card) or
            "stand" (stop drawing cards and end your turn)
        -You may bet before each hand starts. You start woth $100.
    """
    your_money = Wallet(100)
    print('You have $100.')
    #Pre-loop condition     
    play = 'yes'
    # Creates a standard deck of cards.
    deck = create_deck()
    #How many games you're winning or losing by.
    tally = 0
    #Main gameplay loop
    while play.lower() in ('yes','y'):
        # Gambling options
        bet = float(input('Enter amount to bet\n: '))
        while bet < 0:
            print('You can\'t bet negative money!')
            bet = float(input('Enter amount to bet\n: '))
        while bet > your_money.show_money():
            print('You can\'t bet more than you have!')
            bet = float(input('Enter amount to bet\n: '))
        your_money.spend_money(bet)
        
        #Calls the rest of the program
        score, win_statement = blackjack_helper(deck)
        print(win_statement)
        
        #Termination, used if player entered 'quit' in input prompt.
        if win_statement == 'You forfeit.':
            return 'Exiting program'
        
        #Accounts for your bet
        if score == +1:
            print("You won your bet!")
            your_money.add_money(bet*2)
        else:
            print("You lost your bet.")
        print('You have $' + format(your_money.show_money(),'.2f'), 'left.')
        
        #Shows score
        tally += score
        if tally < 0:
            print(f"You're losing by {-1 * tally}.")
        elif tally == 0:
            print('You\'re tied!')
        else: #tally > 0
            print(f"You're winning by {tally}.")
        
        if your_money.show_money() == 0:
            return "You're out of money! Game over."
        
        play = input('Enter "Yes" to play again \n: ') 
    print("Ending game")
