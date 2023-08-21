'''
Created on Feb 27, 2023

@author: johnbotonakis
'''
import tkinter as tk
from PIL import Image,ImageTk
from tkmacosx import Button
from Project_1.GUIWar import WarGUI
from Project_1.GUIBlackjack import Blackjack
from Project_1.GUISlapjack2 import SlapjackGUI

#This will set up the game, by taking the input from each button, checking against a list of acceptable inputs, and setting it in the window
def current_game(x):
    global game_name
    game_name = x
    game_list = [Blackjack,WarGUI, SlapjackGUI]
    if x in game_list:
        x(wn)

if __name__ == '__main__':
    wn = tk.Tk()
    wn.geometry("800x500")
    img = ImageTk.PhotoImage(Image.open(f"../img/table.jpeg").resize(((1550, 1080))))
    background = tk.Label(wn, image=img)
    background.img = img
    background.place(relx=0.5, rely=0.5, anchor='center') 
    title = tk.Label(wn, text = "Card Party Pack 3",font=('Bookman Old Style',50),bd=0).place(relx=0.5,rely=0.2,anchor="c")
    btnWar = Button(wn,text = "Play War",command = lambda:current_game(WarGUI)).place(relx=.47,rely=.5)
    btnBlackJack = Button(wn,text = "Play Blackjack",command = lambda: current_game(Blackjack)).place(relx = .45,rely=.6)
    btnSlapjack = Button(wn,text = "Play Slapjack",command = lambda: current_game(SlapjackGUI)).place(relx = .454,rely = .7)
    btnQuit= Button(wn, text = "Quit",font=('Courier',25),bd=0, command = quit).place(relx = 0.8, rely = 0.9)
    
    wn.mainloop()