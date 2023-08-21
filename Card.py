'''
Created on Feb 8, 2022

@author: twendt
'''

class Card():
    '''
    classdocs
    '''

    def __init__(self, face = None, suit = None, value = None, image = None): #(These are all instance variables)
        '''
        Constructor
        '''
        self.__suit = suit
        self.__face = face
        self.__value = value
        self.__image = image
    #The following are called Accessor functions    
    def getSuit(self):
        return self.__suit
    
    def getFace(self):
        return self.__face
    
    def getValue(self):
        return self.__value
    
    def getImage(self):
        return self.__image
    
    def __str__(self):
        return f"{self.__face} of {self.__suit}"
    #VV draw(self, Canvas, int Left, int Top) VV
    def draw(self, cvs, left, top):
        cvs.create_image(left, top, image = self.__image, anchor = "nw")
        
    
    '''
    Comparison methods.
    For the purposes of this course, we'll assume that all comparisons are done
    based on the face value of the cards.
    '''
    def __eq__(self, other):
        return self.getValue() == other.getValue()
    
    def __lt__(self, other):
        return self.getValue() < other.getValue()
    
    def __gt__(self, other):
        return self.getValue() > other.getValue()
    
    def __le__(self, other):
        return self < other or self == other
    
    def __ge__(self, other):
        return self > other or self == other
    
    def __ne__(self, other):
        return not (self == other)  