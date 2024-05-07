# Pychess main.py

from board import *
from engine import *

b = Board()
e = Engine()
human_turn = False
while e.endgame == False:
    if not human_turn:
        # Tour du joueur humain
        move = input("Entrez votre coup (ex: e2e4) : ")
        e.usermove(b, move)
    else:
        # Tour du programme
        e.search(b)
        e.print_result(b)
        # Afficher l'historique du jeu après chaque coup
        b.showHistory()
        
    human_turn = not human_turn