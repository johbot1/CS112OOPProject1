'''
Created on Mar 5, 2023

@author: johnbotonakis
'''
from Project_1.DeckOfCards import DeckOfCards as DC
class Slapjack_Player(object):
    '''
    classdocs
    '''


    def __init__(self, name = "Player"):
        '''
        Constructor
        '''
        self.__hand = []
        self.name = name
    
    #Adding a card to a player's hand    
    def addCard(self, Card):
        self.__hand.append(Card)
    
    #Play the card at the top of the deck and remove it from the hand
    def playCard(self):
        x = self.__hand.pop(0)
        return x
    
    #Returns the length of the hand         
    def cardsLeft(self):
        return len(self.__hand)
    
    #Will be TRUE if Player has cards in their hand
    def hasNext(self):
        return self.cardsLeft() > 0
        
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

    def __str__(self):
        return f"{self.name}"


if __name__ == '__main__':
    print("Testing default constructor... ", end = "")
    p1 = Slapjack_Player()
    assert p1.name == "Player"
    assert p1.cardsLeft() == 0
    print("Passed!")
    
    print("Testing 'name' constructor... ", end = "")
    p2 = Slapjack_Player("Iggy")
    slapjackdeck = DC()
    slapjackdeck.shuffle()
    for i in range(3):
        p2.addCard(slapjackdeck.dealCard())
    assert p2.name == "Iggy"
    assert p2.cardsLeft() == 3
    print("Passed!")      
    print(p2)
