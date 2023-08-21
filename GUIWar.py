'''
Created on Feb 22, 2023

@author: twendt
'''

import tkinter as tk
from tkinter import messagebox
from Project_1.WarPlayer import WarPlayer
from Project_1.DeckOfCards import DeckOfCards as DC

class WarGUI():
    '''
    classdocs
    '''

    def __init__(self, wn, card_images = "deck_of_cards.png"):
        '''
        Constructor
        '''
        
        # Create a deck
        
        self.__warDeck = DC(card_images)
        self.__player1 = WarPlayer()
        self.__player2 = WarPlayer()
        self.__spoils = WarPlayer()
        self.wn = wn
        self.card1 = None
        self.card2 = None
        
        
        # Set up the canvases
        self.__player1Frame = tk.LabelFrame(wn, text = "Player1", width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__p1Canvas = tk.Canvas(self.__player1Frame, width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__player2Frame = tk.LabelFrame(wn, text = "Player2", width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__p2Canvas = tk.Canvas(self.__player2Frame, width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__battleGroundFrame = tk.LabelFrame(wn, text = "Battlegrounds", width = 3* DC.width, height = DC.height * 2.5)
        self.__BGCanvas = tk.Canvas(self.__battleGroundFrame,  width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__player1Frame.place(relx=0.02,rely=0.05)
        self.__battleGroundFrame.place(relx=0.34,rely=0.05)
        self.__player2Frame.place(relx=0.66,rely=0.05)
        self.__p1Canvas.grid(row = 0, column = 0)
        self.__p2Canvas.grid(row = 0, column = 0)
        self.__BGCanvas.grid(row = 0, column = 0)

    #This section builds each button used in the game
        self.__btnFlip = tk.Button(self.__battleGroundFrame, text = "Play Round", command = self.flip)
        self.__btnFlip.grid(row = 1, column = 0)
        self.__btnFlip10 = tk.Button(self.__battleGroundFrame, text = "Play 10 Rounds", command = self.flip10)
        self.__btnFlip10.grid(row = 2, column = 0)
        self.__btnNewGame = tk.Button(self.__battleGroundFrame, text = "New Game", command = self.newGame)
        self.__btnNewGame.grid(row = 3, column = 0)
        self.__btnQuit = tk.Button(self.__battleGroundFrame, text = "Quit",command = lambda:self.destroy())
        self.__btnQuit.grid(row = 4, column =0)

    #This function will destroy the frame to go back to the main menu.    
    def destroy(self):
        self.__BGCanvas.destroy()
        self.__battleGroundFrame.destroy()
        self.__player1Frame.destroy()
        self.__player2Frame.destroy()

    #This funciton helps reset each piece of the overall game frame, including shuffling the cards, resetting the players, and cards
    def reset(self):
        self.__warDeck.shuffle()
        self.__player1 = WarPlayer()
        self.__player2 = WarPlayer()
        self.__spoils = WarPlayer()
        
        self.card1 = None
        self.card2 = None
    
    #This function will add a Card object into the Player Hand object    
    def dealCards(self):
        while self.__warDeck.hasNext():
            self.__player1.addCard(self.__warDeck.dealCard())
            self.__player2.addCard(self.__warDeck.dealCard()) 
    
    #Similar to the reset function, including it first, this will start a brand new game by resetting, dealing, and rendering
    def newGame(self):
        self.reset()
        self.dealCards()
        self.render()
    
    #This render function will delete each part of the canvas, and redraw each card individually.
    def render(self):
        self.__p1Canvas.delete(tk.ALL)
        self.__p2Canvas.delete(tk.ALL)
        self.__BGCanvas.delete(tk.ALL)
        
        if self.card1 is not None:
            self.card1.draw(self.__BGCanvas, top = 10, left = 10)
        if self.card2 is not None:
            self.card2.draw(self.__BGCanvas, top = 10, left = 2*DC.width - 10)    
        self.__player1.draw(self.__p1Canvas)
        self.__player2.draw(self.__p2Canvas)
        self.__spoils.draw(self.__BGCanvas, left = DC.width - 10, top = 30 + DC.height)            
    
    #The flip function will determine if it can activate via the amount of cards held, then "flip" the card into the battleground
    #From there, it will determine if a war should take place   
    def flip(self):
        if self.__player1.hasNext() and self.__player2.hasNext():
            self.card1 = self.__player1.playCard()
            self.card2 = self.__player2.playCard()
            
            self.__spoils.addCard(self.card1)
            self.__spoils.addCard(self.card2)
            
            print(self.card1)
            print(self.card2)
            
            if self.card1 == self.card2:
                temp1 = self.__player1.prepWar()
                temp2 = self.__player2.prepWar()
                temp = temp1 + temp2
                for card in temp:
                    self.__spoils.addCard(card)
            else:
                if self.card1 > self.card2:
                    winner = self.__player1
                else:
                    winner = self.__player2
            
                self.assign_spoils(winner)
        
        else:
            answer = messagebox.askyesno(title = "Game Over", message = "Game is over.  Play again?")
            if answer == tk.YES:
                self.reset()
                self.dealCards()
        
        self.render()
    
    #Flip10 will do  the same as above, just 10 times.
    def flip10(self):
        for i in range(10):
            self.flip()
    
    #Assigning the spoils is done when the spoils area is bigger than 0, and a Player has won a War.
    def assign_spoils(self, player):
        while self.__spoils.cardsLeft() > 0:
            player.addCard(self.__spoils.playCard())         
if __name__ == "__main__":
    wn = tk.Tk()
    wn.geometry("800x500")
    def example():
        print("BUtton A has been pressed")
    myWar = WarGUI(wn)
    wn.mainloop()
    