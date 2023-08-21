'''
Created on Mar 5, 2023

@author: johnbotonakis
'''
from Project_1.DeckOfCards import DeckOfCards as DC

class Blackjack_Player(object):
    '''
    classdocs
    '''
    win = 21

    def __init__(self, name = "Gambler",handvalue = 0):
        '''
        Constructor
        '''
        self.__hand = []
        self.name = name
        self.handvalue = handvalue
    
    def Acecheck (self,Card):
        if Card.getFace()== "A":
            if self.handvalue<10:
                self.handvalue+11
            elif self.handvalue>10:
                self.handvalue+1
            else:
                pass
        
    def hitme(self,Card):
        '''
        Adds a new card to the "Hand"
        '''
        self.__hand.append(Card)
        self.Acecheck(Card)
        value = int(Card.getValue())
        self.handvalue += value
        print(Card.getFace())
        #FIX THIS: IF A MAKES BUST, A IS LOW, ELSE, A IS 11 NEW FUNCTION!!!
        return self.handvalue
        print(self.handvalue)
        
        
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
        for i in range(len(self.__hand)):
            self.__hand[i].draw(cvs, top= top, left = left + 50*i)
        
    
    def __str__(self):
        return f"{self.name}, {self.handvalue}"


if __name__ == '__main__':
    print('testing the class')
    P1 = Blackjack_Player("Jonesy")
    print(P1, "Passed!")
    P2 = Blackjack_Player("Sam")
    assert P2.name == "Sam"
    print(P2,"Passed!")
    
    print(P1)
    
    print("Testing the hit me funciton")
    BlackjackDeck = DC(acesHigh=True)
    BlackjackDeck.shuffle()
    for i in range(3):
        P1.hitme(BlackjackDeck.dealCard())
        print(P1.handvalue)
        if P1.handvalue>21:
            print("Busted!")
    