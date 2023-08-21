'''
Created on Feb 22, 2023

@author: johnbotonakis
'''

'''
Created on Feb 22, 2023

@author: johnbotonakis
'''

import tkinter as tk
from tkinter import messagebox,Label
from PIL import ImageTk,Image
from Project_1.DeckOfCards import DeckOfCards as DC
from Project_1.Blackjack_Player import Blackjack_Player

class Blackjack(object):
    '''
    classdocs
    '''
    def __init__(self, wn,card_images = "deck_of_cards.png"):
        '''
        Constructor
        '''
        #Create the Deck, the player, and the Dealer
        DC.faces= {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
        self.__Deck = DC(card_images)
        self.__Player1 = Blackjack_Player()
        self.__Dealer = Blackjack_Player("Dealer")
        self.card1 = None
        self.card2 = None
        self.wn = wn
        
        #This creates the frames and canvases for both the Dealer and the Player
        self.__frnBattleField = tk.LabelFrame(wn,text = f"{self.__Dealer}")
        self.__frnBattleField.place(relx =.3,rely= 0)
        self.__cvsBattlefield = tk.Canvas(self.__frnBattleField)
        self.__cvsBattlefield.grid(row = 0,column = 0)

        self.__frmPlayer1 = tk.LabelFrame(wn,text = f"{self.__Player1}")
        self.__frmPlayer1.place(relx =.1,rely= .45)
        self.__cvsPlayer1 = tk.Canvas(self.__frmPlayer1)
        self.__cvsPlayer1.grid(row = 0,column = 0)
        
        #This section is the setup for each individual button
        self.__btnHitMe = tk.Button(self.__frmPlayer1, text = "Hit Me", command = lambda:self.dealCard())
        self.__btnHitMe.grid(row = 1, column = 0, padx=0.1)
        self.__btnHold = tk.Button(self.__frmPlayer1, text = "Hold",command = lambda:self.hold())
        self.__btnHold.grid(row = 1, column = 1)
        self.__btnNewGame = tk.Button(self.__frmPlayer1, text = "New Game",command = lambda:self.NewGame())
        self.__btnNewGame.grid(row = 1, column =2)
        self.__btnQuit = tk.Button(self.__frmPlayer1, text = "Quit",command = lambda:self.destroy())
        self.__btnQuit.grid(row = 1, column =3)
   
    #This function will destroy the frame to go back to the main menu.
    def destroy(self):
        self.__frnBattleField.destroy()
        self.__frmPlayer1.destroy()
    
    #This is the main function of the game, and will compare both hands against each other, alongside
    #comparing the values of each hand to the winning number: 21. It also accounts for the rare "Push" occurrence
    def compareO(self):
        self.render()
        if int(self.__Player1.handvalue)  > int(self.__Dealer.handvalue) and int(self.__Player1.handvalue)<=21 or int(self.__Dealer.handvalue)>21:
            YN = messagebox.askyesno(title="Winner!",message = "You won against the dealer!\n Would you like to play again?")
            if YN == tk.YES:
                self.NewGame()
            else:
                self.destroy()
        elif int(self.__Dealer.handvalue) > int(self.__Player1.handvalue) and int(self.__Dealer.handvalue)<=21 or int(self.__Player1.handvalue)>21:
            YN = messagebox.askyesno(title="You have Busted!(Score over 21)",message = "Looks like the house always wins. You lose!\n Would you like to play again?")
            if YN == tk.YES:
                self.NewGame()
            else:
                self.destroy()
        elif self.__Player1.handvalue == self.__Dealer.handvalue:
            YN = messagebox.askyesno(title="You have Busted!(Score over 21)",message = "Hmm, looks like you Pushed. Nobody wins!\n Would you like to play again?")
            if YN == tk.YES:
                self.NewGame()
            else:
                self.destroy()
    
    #Holding, will not only allow the player to pass on their turn, but allow the dealer to make a decision to hit or compare
    #Based on the value of the currently held hand.
    def hold(self):
        if self.__Dealer.handvalue<20:
            self.__Dealer.hitme(self.__Deck.dealCard())
        elif int(self.__Dealer.handvalue) == int(self.__Player1.handvalue):
            self.compareO()
        else:
            self.compareO()
        if int(self.__Dealer.handvalue)>21:
            self.compareO()
        self.render()
        
    #This funciton helps reset each piece of the overall game frame, including shuffling the cards, resetting the players, and cards    
    def reset(self):
        self.__Deck.shuffle()
        self.__Player1 = Blackjack_Player()
        self.__Dealer = Blackjack_Player()
        self.__frmScore = self.__Player1.handvalue
        self.card1 = None
        self.card2 = None
   
    #This function will add a Card object into the Player Hand object.
    #This will also check if the player has busted by comparing their value to 21   
    def dealCard(self):
        temp = self.__Deck.dealCard()
        self.__Player1.hitme(temp)
        self.render()
        self.__frmPlayer1.config(text = f"{self.__Player1}")
        if int(self.__Dealer.handvalue)==21:
            self.compareO()
        if self.__Player1.handvalue >21:
            print("BUST!")
            YN = messagebox.askyesno(title="You have Busted!(Score over 21)",message = "You have Busted!(Score over 21)\n Would you like to play again?")
            if YN == tk.YES:
                self.NewGame()
            else:
                self.destroy()
    
    #Similar to the reset function, including it first, this will start a brand new game by resetting, dealing, and rendering        
    def NewGame(self):
        self.reset()
        self.dealCard()
        self.hold()
        self.hold()
        self.__frmScore = self.__Player1.handvalue
        self.render()
    
    #This render function will delete each part of the canvas, and redraw each card individually.
    def render(self):
        self.__cvsPlayer1.delete(tk.ALL)
        self.__cvsBattlefield.delete(tk.ALL)
        self.__Player1.draw(self.__cvsPlayer1)
        self.__Dealer.draw(self.__cvsBattlefield)    
        self.__frnBattleField.config(text = f"{self.__Dealer}")
        
if __name__ == "__main__":        
    wn = tk.Tk()
    wn.geometry("800x500")
    img = ImageTk.PhotoImage(Image.open(f"../img/table.jpeg").resize(((1550, 1080))))
    background = tk.Label(wn, image=img)
    background.img = img 
    background.place(relx=0.5, rely=0.5, anchor='center')
    x = Blackjack(wn)
    wn.mainloop()