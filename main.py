# Pychess main.py

from board import *
from engine import *

b = Board()
e = Engine()
human_white = False
human_turn = False

self_play = None
while self_play == None:
    self_play = str(input("White : b, Black : n, chess960 : 960, self_play : self. Your choice ? "))
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
                e.search(b, human_white, None)
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
                e.search(b, human_white, None)
                e.print_result(b)
                # Afficher l'historique du jeu après chaque coup
                b.showHistory(True)
            human_turn = not human_turn
    elif self_play == "self":
        #SELF PLAY
        e.search(b, False, None)
        while e.endgame == False:
            e.search(b, True, None)
            e.print_result(b)
            # Afficher l'historique du jeu après chaque coup
            b.showHistory(True)
                
            human_turn = not human_turn
    elif self_play == "perft":
        print(e.perft(b,3))
        
    elif self_play == "960":
        print("Keep only this part of a FEN : rnqbbnkr/pppppppp/8/8/8/8/PPPPPPPP/RNQBBNKR w KQkq")
        fen = str(input("FEN of starting position : "))
        b.setboard(fen)
        print("Done !")
        print()
        
        #Asking again for color
        self_play = str(input("White : b, Black : n, chess960 : 960, self_play : self. Your choice ? "))
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
                    e.search(b, human_white, 960)
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
                    e.search(b, human_white, 960)
                    e.print_result(b)
                    # Afficher l'historique du jeu après chaque coup
                    b.showHistory(True)
                human_turn = not human_turn
        elif self_play == "self":
            #SELF PLAY
            e.search(b, False, 960)
            while e.endgame == False:
                e.search(b, True, 960)
                e.print_result(b)
                # Afficher l'historique du jeu après chaque coup
                b.showHistory(True)
                    
                human_turn = not human_turn
        elif self_play == "perft":
            print(e.perft(b,3))