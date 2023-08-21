'''
Created on Feb 22, 2023

@author: twendt
'''

import tkinter as tk
from tkinter import messagebox
from Project_1.Slapjack_Player import Slapjack_Player
from Project_1.DeckOfCards import DeckOfCards as DC

class SlapjackGUI():
    '''
    classdocs
    '''

    def __init__(self, wn, card_images = "deck_of_cards.png"):
        '''
        Constructor
        '''
        
        # Create a deck, players, and the keybindings
        DC.faces  = {"A":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":11, "K":11}
        self.__Slapjack_Deck = DC(card_images)
        self.__player1 = Slapjack_Player("Player1")
        self.__player2 = Slapjack_Player()
        self.__spoils = Slapjack_Player()
        self.wn = wn
        self.card1 = None
        self.card2 = None
        self.wn.bind("a", lambda x:self.flipA())
        self.wn.bind('l', lambda x:self.flipL())
        
        
        # Sets up the canvases along with the frames
        self.__player1Frame = tk.LabelFrame(wn, text = "Player1", width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__p1Canvas = tk.Canvas(self.__player1Frame, width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__player2Frame = tk.LabelFrame(wn, text = "Player2", width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__p2Canvas = tk.Canvas(self.__player2Frame, width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__battleGroundFrame = tk.LabelFrame(wn, text = "Battle Grounds", width = 3* DC.width, height = DC.height * 2.5)
        self.__BGCanvas = tk.Canvas(self.__battleGroundFrame,  width = 52*3 + DC.width, height = DC.height * 2.5)
        self.__player1Frame.place(relx=0.02,rely=0.05)
        self.__battleGroundFrame.place(relx=0.34,rely=0.05)
        self.__player2Frame.place(relx=0.66,rely=0.05)
        self.__p1Canvas.grid(row = 0, column = 0)
        self.__p2Canvas.grid(row = 0, column = 0)
        self.__BGCanvas.grid(row = 0, column = 0)

        #This section sets up the buttons
        self.__btnNewGame = tk.Button(self.__battleGroundFrame, text = "New Game", command = self.newGame)
        self.__btnNewGame.grid(row = 1, column = 0)
        self.__btnQuit = tk.Button(self.__battleGroundFrame, text = "Help",command = lambda:self.FAQ())
        self.__btnQuit.grid(row = 2, column =0)
        self.__btnEnd = tk.Button(self.__battleGroundFrame,text = "Quit", command = lambda:self.destroy())
        self.__btnEnd.grid(row=4,column = 0)
    
    #Providing a short demonstration and explain how to play the game
    def FAQ(self):
        messagebox.showinfo("Welcome", "Welcome to Slapjack! This will show you how to play, and become a Slapjack Master!")
        messagebox.showinfo("Welcome", "Each player gets half a deck, and will flip each card, one after the other")
        messagebox.showinfo("Welcome", "If both cards match in Value, you have to slap down and claim the cards!")
        messagebox.showinfo("Welcome", "Player 1 will used the A key to slap.\nPlayer 2 will use the L key to slap.")
        messagebox.showinfo("Welcome", "Get your reflexes ready, and have fun!")
    
    #This function will destroy the frame to go back to the main menu.   
    def destroy(self):
        self.__BGCanvas.destroy()
        self.__battleGroundFrame.destroy()
        self.__player1Frame.destroy()
        self.__player2Frame.destroy()
    
    #This funciton helps reset each piece of the overall game frame, including shuffling the cards, resetting the players, and cards
    def reset(self):
        self.__Slapjack_Deck.shuffle()
        self.__player1 = Slapjack_Player()
        self.__player2 = Slapjack_Player()
        self.__spoils = Slapjack_Player()
        
        self.card1 = None
        self.card2 = None
    
    #This function will add a Card object into the Player Hand object    
    def dealCards(self):
        while self.__Slapjack_Deck.hasNext():
            self.__player1.addCard(self.__Slapjack_Deck.dealCard())
            self.__player2.addCard(self.__Slapjack_Deck.dealCard()) 
    
    #Similar to the reset function, including it first, this will start a brand new game by resetting, dealing, and rendering
    def newGame(self):
        self.reset()
        self.__Slapjack_Deck.shuffle()
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
    
    #Using the keybinding from earlier, this flip command will work when A is pressed.
    #It will play a card, and then check if a slap condition should occur.
    def flipA(self):
        if self.__player1.hasNext():
            self.card1 = self.__player1.playCard()
            print("Player 1 plays:",self.card1)
            self.SLAP()
            self.__spoils.addCard(self.card1)
        self.render()
    
    #Using the keybinding from earlier, this flip command will work when L is pressed.
    #It will play a card, and then check if a slap condition should occur.    
    def flipL(self):
        if self.__player2.hasNext():
            self.card2 = self.__player2.playCard()
            print("Player 2 plays:",self.card2)
            self.__spoils.addCard(self.card2)
            self.SLAP()
        self.render()
    
    #The SLAP condition will check if the value or face are equivalent. If they are,
    #whomever "slaps" or hits their button first will win.
    def SLAP(self):
        if self.card1.getValue() == self.card2.getValue() or self.card1.getFace()==self.card2.getFace():
            print("SLAP DETECTED")
            if self.flipA():
                messagebox.showinfo("", "Player 1 wins this round!")
            elif self.flipL():
                messagebox.showinfo("", "Player 2 wins this round!")
    
         
if __name__ == "__main__":
    wn = tk.Tk()
    wn.geometry("800x500")
    myWar = SlapjackGUI(wn)
    wn.mainloop()
    