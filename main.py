# Pychess main.py

from board import *
from engine import *

b = Board()
e = Engine()
human_white = False
human_turn = False

self_play = str(input("Voulez vous jouer avec les blancs (b) ou les noirs (n) ?"))
if self_play == "b":
    human_white = True
    human_turn = True
    #HUMAIN VS BOT
    while e.endgame == False:
        if human_turn:
            move = ""
            # Tour du joueur humain
            while move == "": 
                move = input("Entrez votre coup (ex: e2e4) : ")
                move = e.usermove(b, move)
        else:
            # Tour du programme
            e.search(b, human_white)
            e.print_result(b)
            # Afficher l'historique du jeu après chaque coup
            b.showHistory(True)
            
        human_turn = not human_turn
elif self_play == "n":
    human_white = False
    human_turn = False
    #HUMAIN VS BOT
    while e.endgame == False:
        if human_turn:
            move = ""
            # Tour du joueur humain
            while move == "": 
                move = input("Entrez votre coup (ex: e2e4) : ")
                move = e.usermove(b, move)
        else:
            # Tour du programme
            e.search(b, human_white)
            e.print_result(b)
            # Afficher l'historique du jeu après chaque coup
            b.showHistory(True)
        human_turn = not human_turn
else:
    #SELF PLAY
    e.search(b, False)
    while e.endgame == False:
        e.search(b, True)
        e.print_result(b)
        # Afficher l'historique du jeu après chaque coup
        b.showHistory(True)
            
        human_turn = not human_turn