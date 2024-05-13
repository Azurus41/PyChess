# Pychess main.py

from board import *
from engine import *

b = Board()
e = Engine()
human_white = False
human_turn = False
while e.endgame == False:
    if human_turn:
        # Tour du joueur humain
        move = input("Entrez votre coup (ex: e2e4) : ")
        e.usermove(b, move)
    else:
        # Tour du programme
        e.search(b, human_white)
        e.print_result(b)
        # Afficher l'historique du jeu après chaque coup
        b.showHistory(True)
        
    human_turn = not human_turn