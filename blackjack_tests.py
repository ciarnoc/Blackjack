"""
Series of tests for Blackjack programs.

-Zachary Avant
"""
from blackjack import *
##############################################################################
# Deck Manipulation Tests #
###########################
def test_create_deck():
    """
    Tests if create_deck() makes a valid deck. 
    Don't worry, I copy and pasted this out of the console. 
    """
    test_deck = [(2, 'Spades'),
                 (2, 'Diamonds'),
                 (2, 'Clubs'),
                 (2, 'Hearts'),
                 (3, 'Spades'),
                 (3, 'Diamonds'),
                 (3, 'Clubs'),
                 (3, 'Hearts'),
                 (4, 'Spades'),
                 (4, 'Diamonds'),
                 (4, 'Clubs'),
                 (4, 'Hearts'),
                 (5, 'Spades'),
                 (5, 'Diamonds'),
                 (5, 'Clubs'),
                 (5, 'Hearts'),
                 (6, 'Spades'),
                 (6, 'Diamonds'),
                 (6, 'Clubs'),
                 (6, 'Hearts'),
                 (7, 'Spades'),
                 (7, 'Diamonds'),
                 (7, 'Clubs'),
                 (7, 'Hearts'),
                 (8, 'Spades'),
                 (8, 'Diamonds'),
                 (8, 'Clubs'),
                 (8, 'Hearts'),
                 (9, 'Spades'),
                 (9, 'Diamonds'),
                 (9, 'Clubs'),
                 (9, 'Hearts'),
                 (10, 'Spades'),
                 (10, 'Diamonds'),
                 (10, 'Clubs'),
                 (10, 'Hearts'),
                 ('Jack', 'Spades'),
                 ('Jack', 'Diamonds'),
                 ('Jack', 'Clubs'),
                 ('Jack', 'Hearts'),
                 ('Queen', 'Spades'),
                 ('Queen', 'Diamonds'),
                 ('Queen', 'Clubs'),
                 ('Queen', 'Hearts'),
                 ('King', 'Spades'),
                 ('King', 'Diamonds'),
                 ('King', 'Clubs'),
                 ('King', 'Hearts'),
                 ('Ace', 'Spades'),
                 ('Ace', 'Diamonds'),
                 ('Ace', 'Clubs'),
                 ('Ace', 'Hearts')]
    deck = create_deck()
    if deck != test_deck:
        return 'Deck is invalid'
    #Implied deck == test_deck
    return 'Valid deck'
def test_deal():
    """
    Tests that cards are removed from the deck and put in the hand.
    """
    start_deck = create_deck()
    test_deck = start_deck.copy()
    end_deck, hand = deal(start_deck)
    if end_deck == test_deck:
        return 'Deal invalid, cards not removed from deck!'
    if hand == []:
        return 'Deal invalid, cards not put in hand'
    return 'Valid deal'
def test_draw():
    """
    deal(deck) is dependent on draw(deck, hand); for the test_deal to pass, 
        draw(deck, hand) must necessarily pass in its normal usage.
    This tests the scenario where the deck runs out mid-game.
    """
    deck = [('Ace', 'Diamonds')]
    hand = []
    for i in range(2):
        try:
            deck, hand = draw(deck, hand)
        except Exception:
            return 'Invalid draw. Deck didn\'t regenerate after running out.'
    return 'Valid draw.'

##############################################################################
# Point Calculation Tests #
###########################       
def test_calculations():
    """
    This test necessarily tests calculate_points(hand), card_value(card) and 
        ace_value(ace_count, hand_value).
    """
    hand = [('Ace', 'Hearts'), ('Ace','Clubs'),('Jack','Diamonds')]
    if calculate_points(hand) == 12:
        valid1 = True
    hand = [('Ace', 'Hearts'),(10,'Diamonds')]
    if calculate_points(hand) == 21:
        valid2 = True
    if valid1 and valid2:
        return 'Valid point calculation'
    return 'Invalid point calculation'
    
##############################################################################
# Printing/Pretty Function Tests #
##################################
def test_pretty_hand():
    hand = [('Ace', 'Diamonds'), (5,'Spades'), (7, 'Hearts')]
    string_hand = pretty_hand(hand)
    if string_hand == 'Ace of Diamonds, 5 of Spades, 7 of Hearts':
        return 'Valid prettification'
    return 'Invalid prettification'
def test_reveal_one():
    hand = [('Ace', 'Diamonds'), (5,'Spades'), (7, 'Hearts')]
    print('If the next two lines are equal, enter "valid".')
    reveal_one(hand)
    print("The dealer turns over a card from their hand: Ace of Diamonds")
    validity = input(':')
    if validity.lower() == 'valid':
        return 'Valid reveal'
    return 'Invalid reveal'
##############################################################################
# Primary Test Functions #
##########################
def test_blackjack_helper(deck):
    """
    Intended to be run from test_blackjack() function, not on its own.
    Tests the main program, blackjack(), 
        and its primary helper, blackjack_helper()
    Enter as prompted
    """
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
        print()
        print('Enter anything other than hit, stand, or quit to test validation.')
        print('Alternatively, run the main game!')
        response = input(
        'If you\'ve already tested validation, enter hit, stand, or quit.\n: '
        )
        while response.lower() not in ('hit','stand','quit'):
            # Validation loop.
            print('Enter "quit" to test termination.')
            print('Then, come back and enter "hit" to test getting a new card,')
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
        return +1, 'You have 21. You win.'    
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
            
def test_blackjack():
    """
    It's recommended to just run main game itself -- 
        the degree of randomness and importance of user-input makes it very
        difficult/impossible to test the game without actually playing it.
    This program provides some prompts for testing for the sake of completeness
    """
    #Pre-loop condition     
    play = 'yes'
    # Creates a standard deck of cards.
    deck = create_deck()
    #How many games you're winning or losing by.
    tally = 0
    #Main gameplay loop
    while play.lower() in ('yes','y'):
        score, win_statement = test_blackjack_helper(deck)
        #Termination, used if player entered 'quit' in input prompt.
        if win_statement == 'You forfeit.':
            return 'Exiting program'
        tally += score
        print(win_statement)
        #You're losing
        if tally < 0:
            print(f"You're losing by {-1 * tally}.")
        elif tally == 0:
            print('You\'re tied!')
        else: #tally > 0
            print(f"You're winning by {tally}.")
        play = input('Enter "Yes" to play again \n: ') 
    print("Ending 'test'")
##############################################################################
# Test All Except Primaries #
#############################
def test():
    """
    Tests all the components.
    """
    print(test_create_deck())
    print(test_deal())
    print(test_draw())
    print(test_calculations())
    print(test_pretty_hand())
    print(test_reveal_one())
