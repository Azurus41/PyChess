#Pychess engine.py

from piece import *
import time
import colorama
colorama.init()
import random

class TranspositionEntry:
    def __init__(self, key, score, depth):
        self.key = key  # Clé de hachage pour identifier l'état du plateau
        self.score = score  # Score évalué pour cette entrée
        self.depth = depth

class TranspositionTable:
    def __init__(self, size=2**10):  # Taille par défaut de la table de transposition
        self.size = size
        self.table = [None] * size

    def store(self, entry):
        index = entry.key % self.size
        self.table[index] = entry

    def probe(self, key):
        index = key % self.size
        entry = self.table[index]
        if entry and entry.key == key:
            return entry
        return None

    def clear(self):
        self.table = [None] * self.size

class Engine:
    """Code du moteur d'échecs"""
    
    def __init__(self):
        self.MAX_PLY = 1000
        self.INFINITY = 32000 
        self.pv_length = [0] * self.MAX_PLY
        self.endgame = False
        self.init_depth = 2 # search in fixed depth
        self.nodes = 0 # number of nodes
        self.stop_search = False 
        self.clear_pv()
        self.fen_table = []
        self.transposition_table = TranspositionTable()
        
    def chkCmd(self,c):
        """Check if the command 'c' typed by user is like a move,
        i.e. 'e2e4','b7b8n'...
        Returns '' if correct.
        Returns a string error if not.
        """
        
        err=(
        'The move must be 4 or 5 letters : e2e4, b1c3, e7e8q...',
        'Incorrect move.'
        )        
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
                
        if(len(c)<4 or len(c)>5):
            return err[0]
        
        if(c[0] not in letters):
            return err[1]
            
        if(c[1] not in numbers):
            return err[1]
            
        if(c[2] not in letters):
            return err[1]
            
        if(c[3] not in numbers):
            return err[1]
            
        return ''
    
    def usermove(self,b,c):
        
        """Move a piece for the side to move, asked in command line.
        The command 'c' in argument is like 'e2e4' or 'b7b8q'.
        Argument 'b' is the chessboard.
        """
        
        if(self.endgame):
            self.print_result(b)
            return        
              
        # Testing the command 'c'. Exit if incorrect.
        chk = self.chkCmd(c)
        if(chk!=''):
            print(chk)
            return ""
            
        # Convert cases names to int, ex : e3 -> 44
        pos1=b.caseStr2Int(c[0]+c[1])
        pos2=b.caseStr2Int(c[2]+c[3])
        
        # Promotion asked ?
        promote=''
        if(len(c)>4):
            promote=c[4]
            if(promote=='q'):
                promote='q'
            elif(promote=='r'):
                promote='r'
            elif(promote=='n'):
                promote='n'
            elif(promote=='b'):
                promote='b'
            
        # Generate moves list to check 
        # if the given move (pos1,pos2,promote) is correct
        mList=b.gen_moves_list()
        
        # The move is not in list ? or let the king in check ?
        if(((pos1,pos2,promote) not in mList) or (b.domove(pos1,pos2,promote)==False)):
            print("\n"+c+' : incorrect move or let king in check'+"\n")
            return ""
            

    def search(self, b, human_turn, chess960):
        book = None
        if chess960 == None:
            with open("openingbook.txt", "r") as file:
                opening_lines = file.readlines()
        
            random.shuffle(opening_lines)
        
        if self.endgame:
            self.print_result(b)
            return

        self.transposition_table.clear()
        self.clear_pv()
        self.nodes = 0
        b.ply = 0
        
        if len(b.showHistory(False)) < 76 and chess960 == None:
            print("Looking at the opening file...")
            for line in opening_lines:
                if str(line.strip()).startswith(b.showHistory(False)):
                    if human_turn == False:
                        if len(b.showHistory(False).split(" ")) == 1:
                            next_move = line.strip().split(" ")[len(b.showHistory(False).split(" "))-1]
                            b.domove(b.caseStr2Int(next_move[0:2]), b.caseStr2Int(next_move[2:4]), "")  # Jouer le prochain coup dans la ligne du livre d'ouverture
                            b.render(0, 0, 0, "Livre d'ouverture", 0)
                            book = True
                        else:
                            next_move = line.strip().split(" ")[len(b.showHistory(False).split(" "))]
                            b.domove(b.caseStr2Int(next_move[0:2]), b.caseStr2Int(next_move[2:4]), "")  # Jouer le prochain coup dans la ligne du livre d'ouverture
                            b.render(0, 0, 0, "Livre d'ouverture", 0)
                            book =  True
                    else:
                        if len(b.showHistory(False).split(" ")) == 1:
                            next_move = line.strip().split(" ")[len(b.showHistory(False).split(" "))]
                            b.domove(b.caseStr2Int(next_move[0:2]), b.caseStr2Int(next_move[2:4]), "")  # Jouer le prochain coup dans la ligne du livre d'ouverture
                            b.render(0, 0, 0, "Livre d'ouverture", 0)
                            book = True
                        else:
                            next_move = line.strip().split(" ")[len(b.showHistory(False).split(" "))]
                            b.domove(b.caseStr2Int(next_move[0:2]), b.caseStr2Int(next_move[2:4]), "")  # Jouer le prochain coup dans la ligne du livre d'ouverture
                            b.render(0, 0, 0, "Livre d'ouverture", 0)
                            book = True
                    return None
        if not book == True:
            print("ply\ttime\tnodes\tkn/s\tscore\tpv")
                
            start = time.time()
            for i in range(1, self.init_depth + 1):
                if b.material_everyone() < 30:
                    mode = "Mode finale activé"
                    score = self.alphabeta(i, -self.INFINITY, self.INFINITY, b, False)
                else:
                    mode = "Mode standard"
                    score = self.alphabeta(i, -self.INFINITY, self.INFINITY, b, False)
                end = time.time()
                if b.side2move == 'blanc':
                    if score >= 0:
                        score_text = colorama.Fore.GREEN + "+" + str(round(score, 2)) + colorama.Fore.WHITE
                    else:
                        score_text = colorama.Fore.RED + str(round(score, 2)) + colorama.Fore.WHITE
                    print("{}\t{}\t{}\t{}\t{}\t".format(i, round(end - start, 3), self.nodes, round((self.nodes * (1 / round(end - start + 0.001, 3)) / 1000), 2), score_text), end='')
                elif b.side2move == 'noir':
                    if score >= 0:
                        score_text = colorama.Fore.GREEN + str(round(-score, 2)) + colorama.Fore.WHITE
                    else:
                        score_text = colorama.Fore.RED + "+" + str(round(-score, 2)) + colorama.Fore.WHITE
                    print("{}\t{}\t{}\t{}\t{}\t".format(i, round(end - start, 3), self.nodes, round((self.nodes * (1 / round(end - start + 0.001, 3)) / 1000), 2), score_text), end='')

                j = 0
                while self.pv[j][j] != 0:
                    c = self.pv[j][j]
                    pos1 = b.caseInt2Str(c[0])
                    pos2 = b.caseInt2Str(c[1])
                    print("{}{}{}".format(pos1, pos2, c[2]), end=' ')
                    j += 1
                print()
                if score > 100 or score < -100:
                    break

            best = self.pv[0][0]
            b.domove(best[0], best[1], best[2])
            nps = int(self.nodes * (1 / round(end - start + 0.001, 3)))
            b.render(score, self.nodes, end - start, mode, nps)

    def alphabeta(self, depth, alpha, beta, b, rdm):            
        self.nodes += 1
        self.pv_length[b.ply] = b.ply
    
        if depth == 0:
            return b.evaluer(rdm)

        mList = b.gen_moves_list()

        f = False  # drapeau pour savoir si au moins un coup sera effectué
        for move in mList:
            capture = b.is_capture(move[1])
            if not b.domove(move[0], move[1], move[2]):
                continue

            f = True  # un coup a été effectué
            if b.in_check(b.side2move) or capture:
                score = -self.alphabeta(depth, -beta, -alpha, b, rdm)
            else:
                score = -self.alphabeta(depth - 1, -beta, -alpha, b, rdm)

            # Annuler le coup
            b.undomove()

            if score > alpha:
                if score >= beta:
                    return beta
                alpha = score

                # Mettre à jour la table de PV triangulaire
                self.pv[b.ply][b.ply] = move
                j = b.ply + 1
                while j < self.pv_length[b.ply + 1]:
                    self.pv[b.ply][j] = self.pv[b.ply + 1][j]
                    j += 1
                self.pv_length[b.ply] = self.pv_length[b.ply+1]+1

        if not f:
            chk = b.in_check(b.side2move)
            if chk:
                return -self.INFINITY + b.ply  # MAT
            else:
                return -0.1  # DRAW

        return alpha

    def print_result(self, b):
        f = False
        for pos1, pos2, promote in b.gen_moves_list():
            if b.domove(pos1, pos2, promote):
                b.undomove()
                f = True
                break

        if not f:
            if b.in_check(b.side2move):
                print("0-1 {Black mates}" if b.side2move == 'blanc' else "1-0 {White mates}")
            else:
                print("1/2-1/2")
            self.endgame = True
            b.showHistory(True)
            time.sleep(10000)
            
    def clear_pv(self):
        self.pv = [[0 for x in range(self.MAX_PLY)] for x in range(self.MAX_PLY)]