'''
NAME
    DeckOfCards

DESCRIPTION
    This module provides a simple class to represent a deck of playing cards.
    The deck of cards is a collection of Card objects
    
    It also provides unit testing for each of the class methods.

DEPENDENCIES
    Card.py
    PIL
    random
             
Created by: Ted Wendt
Created on: February 1, 2022
Modified by: Ted Wendt
Modified on: February 20, 2022
'''

from PIL import Image, ImageTk
from Project_1.Card import Card
import random

class DeckOfCards(object):
    '''
    A class used to represent a simple playing card.
    
    Class Variables:  (Remember, these belong to the WHOLE CLASS, not any individual deck.)
        size: int
            the number of cards in a standard deck
        suits: list<str>
            a list containing the names of the suits
        faces: dict<str, int>
            an dictionary containing the 'faces' and corresponding used in the deck.
        cardImages: Image
            an image sheet containing images of all of the playing cards.
        width: int
            the width of a standard card based on the image sheet
        height: int
            the height of a standard card based on the image sheet
            
    Class Methods:  (These belong to DeckOfCards the class and not to individual decks)
        loadCardImages(fileName: str): None
            looks in "../img/" for the specified file.  Opens the file and loads the image.
            Sets the width and height of individual cards based on the image dimensions.

        __loadImage(row: int, col: int): Image
            local helper function for creating individual card images.
            crops the class image to return the card in the specified row and column.
    
    (Instance) Attributes:    (These belong to individual deck objects)
        __cards: list<Card>
            a list containing Card objects.
        backOfCard: Card
            a 'dummy' Card used to display the back of a card (i.e to draw cards 'face down' to a GUI)
        currentCard: int
            a counter used to track location as we iterate through the deck.
            (As we 'deal' cards, the deck itself doesn't change.  We simply point to the 
            next card in the list)
    
    (Instance) Methods:
        shuffle(): None
            shuffles the card list by randomizing locations of each card
        dealCard(): Card
            returns the card at index 'currentCard' and increments the index
        cardsRemaining(): int
            returns the number of cards left after 'currentCard'
        isEmpty(): bool
            return True if there are no cards remaining
        hasNext(): bool
            returns True if there are cards remainaing
        reset(): None
            resets the currentCard counter to 0
        
    '''
    #===================================
    # Class Variables
    #===================================
    
    size = 52
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    faces = {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13}
    cardImages = None
    width = 0
    height = 0
    backOfCard = None
    
    #===================================
    # Class methods
    #===================================
    
    @classmethod
    def loadCardImages(cls, filename):
        '''
            Loads the card deck image sheet from the specified file.
            Sets the width and height of cards based on the image dimensions
            
            Parameters:
                filename: str
                    the name of the file that contains the deck images sheet.
            
            preconditions: 
              * specified file must exist in "../img/".
            postconditions: 
              * The class cardImages, width, and height are set based on the image.
        
        '''
        try:
            DeckOfCards.cardImages = Image.open(f"../img/{filename}")
            DeckOfCards.width, DeckOfCards.height = DeckOfCards.cardImages.size
            
            # We'll assume that the image sheet has one column for each face and one row for each suit,
            # plus one row for jokers and the back-of-card image. 
            DeckOfCards.width //= len(DeckOfCards.faces)        # Divide image width by number of columns
            DeckOfCards.height //= len(DeckOfCards.suits) + 1   # Divide image height by number of rows 
            
        except FileNotFoundError:
            print(f"File '{filename}' cannot be found in the directory '../img'.")
        except:
            print("An error occurred loading your image")
            
    @classmethod
    def __loadImage(self, row, col):
        '''
            local helper function for creating individual card images.
            crops the class image to return the card in the specified row and column.
            
            Parameters:
                row: int
                    the row in the image that contains this Card image
                col: int
                    the column in the image that contains this Card image
                    
            preconditions: 
              * The class 'cardImages' file has been opened.
              * The image for the deck has the cards arranged in 13 rows and 4 columns.
              * The columns are ordered A-2-3-4-...-J-Q-K
              * The rows are ordered Clubs-Diamonds-Hearts-Spades
              * The 'back' image for the cards is in the fifth row in the third column (i.e row = 4, col = 2)
            postconditions:
              * The 'cropped' image for this card is returned.
        '''
        assert DeckOfCards.cardImages is not None
        assert DeckOfCards.width > 0
        assert DeckOfCards.height > 0

        img = DeckOfCards.cardImages.crop((col*DeckOfCards.width, 
                                           row*DeckOfCards.height,
                                           (col + 1)*DeckOfCards.width,
                                            (row + 1)*DeckOfCards.height))
        t = ImageTk.PhotoImage(img)     # Convert the Image to an ImageTk object so we can render it to a tkinter canvas
        return t    
            
    def __init__(self, deckImages = None, acesHigh = False):
        '''
        Constructor
        Parameters:
            deckImages: str
                the name of the file containing the images for this deck of cards.
                if no name is specified, no images are used.
            acesHigh: bool
                used to toggle the value of aces.  If true, set value of aces to 14.
        '''
        
        # If we've got an image, load it to memory and then create the backOfCard dummy.
        # If there's no image, don't do anything.
        if deckImages is not None:
            DeckOfCards.loadCardImages(deckImages)
            DeckOfCards.backOfCard = Card(None, None, 0, DeckOfCards.__loadImage(4, 2))
        else:
            DeckOfCards.backOfCard = None
        
        # If the user declares aces to be high, set their value to be 14.
        if acesHigh:
            DeckOfCards.faces["A"] = 14    
        
        # Create a deck
        self.__cards = []
        self.currentCard = 0
        
        # Create a card of each face in each suit.
        i = 0        
        for f in DeckOfCards.faces:

            for j in range(len(DeckOfCards.suits)):
                face = f
                suit = DeckOfCards.suits[j]
                value = DeckOfCards.faces[f]
                if deckImages is not None:
                    img = DeckOfCards.__loadImage(j, i)
                else:
                    img = None
                self.__cards.append(Card(face, suit, value, img))
            i += 1
    
    def shuffle(self,amt=1):
        '''
            randomly shuffle the cards in the deck.  Reset the currentCard counter to 0.
            
            preconditions: none
            postconditions: 
              * self.__cards has been shuffled.
        '''
        self.reset()
        for i in range (amt):
            random.shuffle(self.__cards)
        
    def dealCard(self):
        '''
            return the card at index 'currentCard' to the user and increment 'currentCard'
            
            precondition: 
             * currentCard <= size
            postcondition:
             * return the card in index 'currentCard'
             * currentCard += 1 
        '''
        # As long as the deck has another card to give, give it and increment the current card.
        if not self.isEmpty():
            c = self.__cards[self.currentCard]
            self.currentCard += 1
        else:
            c = None
        return c
        
    def cardsRemaining(self):
        '''
            return the number of cards remaining that are available to be dealt.
            
            precondition: none
            postcondition:
              * return the integer number of cards left in the deck.
        '''
        return len(self.__cards) - self.currentCard
    
    def isEmpty(self):
        '''
            return True if there are no cards remaining to be dealt.
            
            precondition: none
            postcondition:
              * return a boolean value that tells whether there are cards left to be dealt.
        '''
        return self.cardsRemaining() == 0
    
    def hasNext(self):
        '''
            return True if there is at least one card remaining to be dealt.
            
            precondition: none
            postcondition:
              * return a boolean value that tells whether there are cards left to be dealt.
        '''        
        return not self.isEmpty()
    
    def reset(self):
        '''
            set the currentCard counter back to 0.  Do not otherwise alter the deck (or its order)
            
            precondition: none
            postcondition:
              * set currentCard = 0.        
        '''
        self.currentCard = 0
        
# End of class DeckOfCards

# Begin unit testing
# NOTE: Image testing is not done in this module because of GUI requirements.
if __name__ == '__main__':
    print("Testing default constructor... ", end = "")
    myDeck = DeckOfCards()
    assert myDeck.backOfCard == None
    assert myDeck.currentCard == 0
    assert not myDeck.isEmpty()
    assert myDeck.hasNext()
    assert myDeck.cardsRemaining() == 52
    print("Passed!")
    
    print("Testing 'aces high' constructor... ", end = "")
    acesHighDeck = DeckOfCards(acesHigh = True)
    c = acesHighDeck.dealCard()     # Should be the Ace of Clubs
    assert c.getValue() == 14
    print("Passed!")
    
    print("Testing deal methods... ", end = "")
    for i in range(52):
        myDeck.dealCard()
        
    assert myDeck.isEmpty()
    assert not myDeck.hasNext()
    assert myDeck.currentCard == 52
    assert myDeck.cardsRemaining() == 0
    print("Passed!")
    
    print("Testing reset method... ", end = "")
    myDeck.reset()
    assert myDeck.currentCard == 0
    assert not myDeck.isEmpty()
    assert myDeck.hasNext()
    assert myDeck.cardsRemaining() == 52
    print("Passed!")