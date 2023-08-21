'''
NAME
    WarGame

DESCRIPTION
    This module provides a class to conduct a game of War

DEPENDENCIES
    Card.py    (implicitly)
    DeckOfCards.py
    WarPlayer.py
             
Created by: Ted Wendt
Created on: February 1, 2022
Modified by: Ted Wendt
Modified on: February 20, 2022
'''

from activity_4b.DeckOfCards import DeckOfCards as DC
from activity_4b.WarPlayer import WarPlayer as WP

class WarGame(object):
    '''
    A class used to conduct and manage a game of War.
    
    Attributes:
        warDeck: DeckOfCards
            the deck to be used for this game
        p1: WarPlayer
            used to represent player 1 in the game
        p2: WarPlayer
            used to represent player 2 in the game
        spoils: WarPlayer
            used as a place to store Card objects while we determine who wins the round
        rounds: int
            the number of rounds the game has lasted
    
    Methods:
        deal(): None
            assigns cards from the deck to each of the players
        reset(): None
            resets the deck and clears out the spoils, p1, and p2
        playRound(): None
            conducts a single round of War
        assignSpoils(winner: WarPlayer): None
            assigns the Cards from the spoils player to the 'winner'
        playGame(): None
            conducts rounds of War until either one player is out of cards or 
            the maximum number of rounds has been reached.
        main(): None
            implements a loop to allow the user to play the game multiple times.
        __getValidYN(): bool
            local helper function for validating input
    '''


    def __init__(self, p1Name = "Player 1", p2Name = "Player 2"):
        '''
        Constructor
        
        Parameters:
            p1Name: str
            p2Name: str
        '''
        self.warDeck = DC(acesHigh = True)
        self.p1 = WP(name = p1Name)
        self.p2 = WP(name = p2Name)
        self.spoils = WP()
        self.reset()
        
    def deal(self):
        '''
            assigns cards from the deck to each of the players
            
            preconditions:
              * warDeck is not empty
              * warDeck has enough cards to EVENLY split between the players
            postcondition:
              * each player has half of the cards from the deck in their hand.
        '''
        while self.warDeck.hasNext():
            self.p1.addCard(self.warDeck.dealCard())
            self.p2.addCard(self.warDeck.dealCard())
    
    def reset(self):
        '''
            resets the deck and clears out the spoils, p1, and p2
            
            preconditions: none
            postconditions:
              * Resets and reshuffles the deck
              * Empties the hands of both players and the spoils
        '''
        self.warDeck.reset()
        self.warDeck.shuffle()
        
        while self.p1.hasNext():
            self.p1.playCard()
        while self.p2.hasNext():
            self.p2.playCard()
        while self.spoils.hasNext():
            self.spoils.playCard()
        self.rounds = 0
    
    def playRound(self):
        '''
            conducts a single round of War
            gets one card from each player, compares them, and assigns 'spoils' to the winner.
            if there's a 'war', have each player bury 3 cards in the spoils.
            
            preconditions:
              * Each player must have at least one card in their hand
            postconditions:
              * Either the winning player will receive the spoils OR (in the case of a tie), the spoils
                will contain each players' card plus 3 more from their hand.
        '''
        
        # Ask each player for a card and add them to the spoils
        c1 = self.p1.playCard()
        c2 = self.p2.playCard()
        self.spoils.addCard(c1)
        self.spoils.addCard(c2)
        
        if c1 == c2:
            # If the card values match, get 3 cards from each player and bury them.
            p1bury = self.p1.prepWar()
            p2bury = self.p2.prepWar()
            bury = p1bury + p2bury
            print(f"WAAAAAR!")
            for c in bury:
                self.spoils.addCard(c)
        else:
            # If there's a clear winner, get ready to assign them the spoils.
            if c1 < c2:
                winner = self.p2
                print(f"{self.p2.name}'s {c2} beats {self.p1.name}'s {c1}.")
            elif c2 < c1:
                winner = self.p1
                print(f"{self.p1.name}'s {c1} beats {self.p2.name}'s {c2}.")
                
            self.assignSpoils(winner)
    
    
    def assignSpoils(self, winner):
        '''
            assign all cards from the 'spoils' player to the 'winner'
            
            Parameters:
                winner: WarPlayer
                    the WarPlayer object representing the winner of the battle
            
            preconditions: none
            postconditions:
              * the 'winner' has the cards from 'spoils' added to the end of their hand.
        '''
        while self.spoils.hasNext():
            winner.addCard(self.spoils.playCard())
    
    def playGame(self):
        '''
            conducts rounds of War until either one player is out of cards or 
            the maximum number of rounds has been reached.
            
            precondition: none
            postconditions:
              * Either one of the players is out of cards or more than 5000 rounds have been played.
        '''
        while self.p1.hasNext() and self.p2.hasNext() and self.rounds < 5000:
            self.playRound()
            self.rounds += 1
        if self.rounds >= 5000:
            print(f'The war has lasted {self.rounds} long, hard-fought rounds.  Time for peace.')
        elif not self.p1.hasNext():
            print(f"{self.p1.name} is out of cards.  {self.p2.name} wins after {self.rounds} rounds!")
        else:
            print(f"{self.p2.name} is out of cards.  {self.p1.name} wins after {self.rounds} rounds!")
            
    def main(self):
        '''
            implements a loop to allow the user to play the game multiple times.
            
            preconditions: none
            postconditions: none, really...
        '''
        playAgain = True
        while playAgain:
            self.reset()
            self.deal()
            self.playGame()
            playAgain = self.__getValidYN()
            
                
    def __getValidYN(self):
        '''
            local helper function for validating input
            Returns True if the user selects something yes-like.  Returns False if they select something no-like.
            
            preconditions: None
            postconditions:
              * Returns True if user enters something from the validY list.
              * Returns False if user enters something from the validN list.
        '''
        validY = ["y", "yes", "yeah", "yup", "ok", "yes please"]
        validN = ["n", "no", "nope", "nah", "no thanks", "no thank you"]
        user_in = ""
        while user_in.lower() not in validY + validN:
            user_in = input("Play again? (Y/N)")
        if user_in.lower() in validY:
            return True
        else:
            return False
    
if __name__ == "__main__":
    myGame = WarGame(p1Name = "Bob", p2Name = "Doug")
    myGame.main()    
    