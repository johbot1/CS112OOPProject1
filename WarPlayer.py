'''
NAME
    WarPlayer

DESCRIPTION
    This module provides a class to represent a single player in a game of War.
    
    It also provides unit testing for each of the class methods.

DEPENDENCIES
    Card.py    (implicitly)
    DeckOfCards.py
             
Created by: Ted Wendt
Created on: February 1, 2022
Modified by: Ted Wendt
Modified on: February 20, 2022
'''

from Project_1.DeckOfCards import DeckOfCards as DC

class WarPlayer(object):
    '''
    A class used to represent a simple playing card.
    
    Attributes:
        __hand: list<Card>
            a list containing this player's war cards
        name: str
            the name of this player.
    
    Methods:
        addCard(c: card): None
            adds specified card to player's hand
        playCard(): Card
            returns the 'top' card from this player's hand
        cardsLeft(): int
            returns the number of cards remaining in the player's hand
        hasNext(): bool
            returns True if this player has cards left in their hand
        prepareWar(): list<Card>
            returns a list of (up to) 3 cards from the player's hand
        draw(cvs: Canvas, left: int, top: int): None 
            renders this player's hand to the specified canvas at the given coordinates.
    '''

    def __init__(self, name = "Anonymous"):
        '''
        Constructor
        Parameters: 
            name: str
                the player's chosen username
        '''
        self.__hand = []
        self.name = name      

    def addCard(self, c):
        '''
            adds the specified card to the END of the player's hand.
            
            Parameters:
                c: Card
                    the card to be added to the hand.
            
            preconditions: none
            postcondition: 
              * the specified card is added to the end of the player's hand
        '''
        self.__hand.append(c)
    
    def playCard(self):
        '''
            removes the 'top' card in the player's hand and returns it
            
            precondition:
              * self.__hand is not empty
            postcondition:
              * The first card in the hand is removed and returned.
        '''
        x = self.__hand.pop(0)
        return x
            
    def cardsLeft(self):
        '''
            returns the number of cards remaining in the player's hand
            
            preconditions: none
            postcondition: returns number of cards in the hand.
        '''
        return len(self.__hand)
    
    def hasNext(self):
        '''
            returns True if the user has cards left in their hand.
        '''
        return self.cardsLeft() > 0

        
    def prepWar(self):
        '''
            returns a list of (up to) 3 cards from the player's hand.
            if the user has fewer than 4 cards left, put all remaining cards into the list to return.
            
            precondition: none
            postcondition:
              * up to 3 cards are removed from the player's hand and returned as a lit.
        '''
        
        # If there are at least 4 cards left, do full war.  Otherwise, do partial.
        # If no cards left after burying, they'll lose
        count = min(3, self.cardsLeft())
        spoils = []
        for _ in range(count):
            spoils.append(self.playCard())       # Bury the next 3 cards
        return spoils
        
    def draw(self, cvs, left = 10, top = 10):
        '''
            Draws the player's hand to the specified canvas
            Since the player should not be able to see the card faces, just
            draw the back of a card a bunch of times to suggest a 'stack'
            
            Parameters:
                cvs: tkinter.Canvas
                    the canvas object to which the image should be rendered
                left: int
                    the x coordinate at which to start our drawing (left most point)
                top: int
                    the y coordinate at which to start our drawing (top most point)
            
            preconditions: cvs must be a tkinter.Canvas object and must have already been instantiated
            postconditions: draws a 'stack' of cards at the specified location.
        '''        
        for i in range(self.cardsLeft()):
            DC.backOfCard.draw(cvs, top = top, left = left + 3*i)   # Draw the images atop one another, offset by 3 pixels each time.

# End of class WarPlayer

# Begin unit testing
# Note: Draw method not tested here.
if __name__ == '__main__':
    print("Testing default constructor... ", end = "")
    p1 = WarPlayer()
    assert p1.name == "Anonymous"
    assert p1.cardsLeft() == 0
    assert not p1.hasNext()
    print("Passed!")
    
    print("Testing 'name' constructor... ", end = "")
    p2 = WarPlayer("Iggy")
    assert p2.name == "Iggy"
    assert p2.cardsLeft() == 0
    assert not p2.hasNext()
    print("Passed!")      
    
    print("Testing addCard, playCard, cardsLeft, and prepWar... ")
    warDeck = DC()
    while warDeck.hasNext():
        p2.addCard(warDeck.dealCard())
    assert p2.cardsLeft() == 52
    assert p2.hasNext()
    print("  addCard...passed!")
    c = p2.playCard()   # This should return the Ace of clubs
    assert c.getFace() == "A"
    assert c.getSuit() == "Clubs"
    print("  playCard...passed!")
    w = p2.prepWar()    # This should return a list containing the other 3 aces.
    assert len(w) == 3
    for card in w:
        assert card.getFace() == "A"
    # Now deal out all of the cards but 1 and see what prepWar does.
    for i in range(47):
        p2.playCard()
        
    assert p2.cardsLeft() == 1
    w = p2.prepWar()
    assert len(w) == 1
    assert w[0].getFace() == "K"
    assert p2.cardsLeft() == 0
    assert not p2.hasNext()
    print("  prepWar...passed!")
    
    