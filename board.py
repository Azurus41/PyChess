# Pychess board.py

from piece import *
import time
import os
import colorama
colorama.init()
import random

class Board:
    
    "The chess board"
    
    # Names of the 64 sqares
    coord=[
        'a8','b8','c8','d8','e8','f8','g8','h8',
        'a7','b7','c7','d7','e7','f7','g7','h7',
        'a6','b6','c6','d6','e6','f6','g6','h6',
        'a5','b5','c5','d5','e5','f5','g5','h5',
        'a4','b4','c4','d4','e4','f4','g4','h4',
        'a3','b3','c3','d3','e3','f3','g3','h3',
        'a2','b2','c2','d2','e2','f2','g2','h2',
        'a1','b1','c1','d1','e1','f1','g1','h1',
        ]

    ####################################################################
    
    def __init__(self):
        self.init()
    
    ####################################################################
    
    def init(self):
        
        "Init the chess board at starting position"
        
        # Chessboard has 64 squares, numbered from 0 to 63 (a8 to h1)
        # Placing pieces ('cases' is 'square' in french :)
        self.cases = [
            Piece('TOUR','noir'),Piece('CAVALIER','noir'),Piece('FOU','noir'),Piece('DAME','noir'),Piece('ROI','noir'),Piece('FOU','noir'),Piece('CAVALIER','noir'),Piece('TOUR','noir'),
            Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),Piece('PION','noir'),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),
            Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),Piece('PION','blanc'),
            Piece('TOUR','blanc'),Piece('CAVALIER','blanc'),Piece('FOU','blanc'),Piece('DAME','blanc'),Piece('ROI','blanc'),Piece('FOU','blanc'),Piece('CAVALIER','blanc'),Piece('TOUR','blanc')
            ]
            
        self.side2move='blanc'
        self.ep=-1 # the number of the square where to take 'en passant'
        self.history=[] # the moves history
        self.ply=0 # half-move number since the start

        # Castle rights
        self.white_can_castle_56=True
        self.white_can_castle_63=True
        self.black_can_castle_0=True
        self.black_can_castle_7=True    
        
    ####################################################################
    
    def is_capture(self, destination):
        #It work, but it it disabeled in engine.py so far
        return self.cases[destination].isEmpty == False
    
    ####################################################################

    def gen_moves_list(self,color='',dontCallIsAttacked=False):
        if(color==''):
            color=self.side2move
        mList=[]
        
        # For each 'piece' on the board (pos1 = 0 to 63)
        for pos1,piece in enumerate(self.cases):
                
            # Piece (or empty square) color is not the wanted ? pass
            if piece.couleur!=color:
                continue
            
            if(piece.nom=='ROI'): # KING
                mList+=piece.pos2_roi(pos1,self.oppColor(color),self,dontCallIsAttacked)
                continue
                
            elif(piece.nom=='DAME'): # QUEEN = ROOK + BISHOP moves !
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue
                
            elif(piece.nom=='TOUR'): # ROOK
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                continue
                
            elif(piece.nom=='CAVALIER'): # KNIGHT
                mList+=piece.pos2_cavalier(pos1,self.oppColor(color),self)
                continue
                
            elif(piece.nom=='FOU'): # BISHOP
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue
                
            if(piece.nom=='PION'): # PAWN
                mList+=piece.pos2_pion(pos1,piece.couleur,self)
                continue
                
        return mList
        
    #################################################################
    
    def getboard(self):
        """Returns the FEN notation of the current board. i.e. :
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - - 0
        """
                
        emptySq=0 # couting empty squares
        s='' # constructring the FEN string
        
        # Parsing each board square (i = 0 to 63)
        for i,piece in enumerate(self.cases):
            
            p=piece.nom
            c=piece.couleur

            if(emptySq==8):
                s+='8'
                emptySq=0
                
            if(i and i%8==0):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0                
                s+='/'
                        
            if(piece.isEmpty()):
                emptySq+=1
                
            elif(p=='ROI'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='k'
                else:
                    s+='K'
                    
            elif(p=='DAME'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0                
                if(c=='noir'):
                    s+='q'
                else:
                    s+='Q'
                    
            elif(p=='TOUR'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='r'
                else:
                    s+='R'
                    
            elif(p=='CAVALIER'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='n'
                else:
                    s+='N'
                              
            elif(p=='FOU'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='b'
                else:
                    s+='B'
                    
            elif(p=='PION'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='p'
                else:
                    s+='P'

        if(emptySq>0):
            s+=str(emptySq)
            
        # b or w (black,white)
        if(self.side2move=='blanc'):
            s+=' w '
        else:
            s+=' b '
            
        # Castle rights (KQkq)
        no_castle_right=True
        if(self.white_can_castle_63):
            s+='K'
            no_castle_right=False
        if(self.white_can_castle_56):
            s+='Q'
            no_castle_right=False            
        if(self.black_can_castle_7):
            s+='k'
            no_castle_right=False
        if(self.black_can_castle_0):
            s+='q'
            no_castle_right=False
        if(no_castle_right):
            s+='-'
        
        '''
        # prise en passant e3
        if(self.ep!=-1):
            s+=' '+self.coord[self.ep]
        else:
            s+=' -'
        
        # TODO
        # number of half-moves for 50 moves rule
        s+=' -'

        # numéro du coup
        s+=' '+str(int(len(self.history)/2))
        '''

        return s
    
    #########################################################################
    
    def setboard(self,fen):
        
        """Set the board to the FEN position given. i.e. :
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - - 0
        Returns TRUE or FALSE if done or not.
        If not : print errors.
        """
        
        f=fen.split()
        err=""
        
        if(len(f)!=3):
            err+="Wrong FEN notation. It should be :\n"
            err+="[pieces] [side to move] [castle rights]\n"
            err+="i.e. : rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq\n"
            print(err)
            return False
            
        self.init()
        self.white_can_castle_56=False
        self.white_can_castle_63=False
        self.black_can_castle_0=False
        self.black_can_castle_7=False        
        
        fen =   f[0] # rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR
        trait = f[1] # b ou w (black,white)
        roque = f[2] # KQkq
        
        # Setting pieces
        i=0
        for c in fen:
            if(c=='k'):
                self.cases[i]=Piece('ROI','noir')
                i=i+1
            elif(c=='q'):
                self.cases[i]=Piece('DAME','noir')
                i=i+1
            elif(c=='r'):
                self.cases[i]=Piece('TOUR','noir')
                i=i+1
            elif(c=='n'):
                self.cases[i]=Piece('CAVALIER','noir')
                i=i+1
            elif(c=='b'):
                self.cases[i]=Piece('FOU','noir')
                i=i+1
            elif(c=='p'):
                self.cases[i]=Piece('PION','noir')
                i=i+1
            elif(c=='K'):
               self.cases[i]=Piece('ROI','blanc')
               i=i+1
            elif(c=='Q'):
               self.cases[i]=Piece('DAME','blanc') 
               i=i+1
            elif(c=='R'):
                self.cases[i]=Piece('TOUR','blanc')
                i=i+1
            elif(c=='N'):
                self.cases[i]=Piece('CAVALIER','blanc')
                i=i+1
            elif(c=='B'):
                self.cases[i]=Piece('FOU','blanc')
                i=i+1
            elif(c=='P'):
                self.cases[i]=Piece('PION','blanc')
                i=i+1
            elif(c=='/'):
                pass
            else: # a number of empty squares is given
                try:
                    nb=int(c)
                except ValueError:
                    print('Error : wrong FEN. Integer expected.')
                    return                
                cpt=0
                while(cpt<nb):
                    self.cases[i]=Piece()
                    cpt=cpt+1
                    i=i+1

        # Checking number of squares
        if(i!=64):
            print('Error : wrong FEN.')
            self.init()
            return False
                    
        # Site to move
        if(trait=='b'):
            self.side2move='noir'
        else:
            self.side2move='blanc'
            
        # Castle rights
        if(roque!='-'):
            if('K' in roque):
                self.white_can_castle_63=True
            if('Q' in roque):
                self.white_can_castle_56=True
            if('k' in roque):
                self.black_can_castle_7=True
            if('q' in roque):
                self.black_can_castle_0=True
        
        return True
    
    ####################################################################
    
    def domove(self,depart,arrivee,promote):
        
        """Move a piece on the board from the square numbers
        'depart' to 'arrivee' (0..63) respecting rules :
        - prise en passant
        - promote and under-promote
        - castle rights
        Returns :
        - TRUE if the move do not let king in check
        - FALSE otherwise and undomove is done.
        """

		# Informations to save in the history moves
        pieceDeplacee=self.cases[depart] # moved piece
        piecePrise=self.cases[arrivee] # taken piece, can be null : Piece()
        isEp=False # will be used to undo a ep move
        histEp=self.ep # saving the actual ep square (-1 or square number TO)
        hist_roque_56=self.white_can_castle_56
        hist_roque_63=self.white_can_castle_63
        hist_roque_0=self.black_can_castle_0
        hist_roque_7=self.black_can_castle_7       
        flagViderEp=True # flag to erase ep or not : if the pawn moved is not taken directly, it can't be taken later
        
        # Moving piece
        self.cases[arrivee]=self.cases[depart]
        self.cases[depart]=Piece()
        
        self.ply+=1
                
        # a PAWN has been moved -------------------------------------
        if(pieceDeplacee.nom=='PION'):
            
            # White PAWN
            if(pieceDeplacee.couleur=='blanc'):
                
                # If the move is "en passant"
                if(self.ep==arrivee):
                    piecePrise=self.cases[arrivee+8] # take black pawn
                    self.cases[arrivee+8]=Piece()
                    isEp=True

                # The white pawn moves 2 squares from starting square
                # then blacks can take "en passant" next move
                elif(self.ROW(depart)==6 and self.ROW(arrivee)==4):
                    self.ep=arrivee+8
                    flagViderEp=False
		
            # Black PAWN
            else:
                
                if(self.ep==arrivee):
                    piecePrise=self.cases[arrivee-8]
                    self.cases[arrivee-8]=Piece()
                    isEp=True

                elif(self.ROW(depart)==1 and self.ROW(arrivee)==3):
                    self.ep=arrivee-8
                    flagViderEp=False
                    
        # a ROOK has been moved--------------------------------------
        # update castle rights
        
        elif(pieceDeplacee.nom=='TOUR'):
            
            # White ROOK
            if(pieceDeplacee.couleur=='blanc'):
                if(depart==56):
                    self.white_can_castle_56=False
                elif(depart==63):
                    self.white_can_castle_63=False
                
            # Black ROOK
            else:
                if(depart==0):
                    self.black_can_castle_0=False
                elif(depart==7):
                    self.black_can_castle_7=False
                
        # a KING has been moved-----------------------------------------
        
        elif(pieceDeplacee.nom=='ROI'):
            
            # White KING
            if(pieceDeplacee.couleur=='blanc'):    
                
                # moving from starting square
                if(depart==60):
                    # update castle rights
                    self.white_can_castle_56=False
                    self.white_can_castle_63=False                    

                    # If castling, move the rook
                    if(arrivee==58):
                        self.cases[56]=Piece()
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.cases[63]=Piece()
                        self.cases[61]=Piece('TOUR','blanc')
                
            # Black KING
            else:                

                if(depart==4):
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False                    

                    if(arrivee==6):
                        self.cases[7]=Piece()
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.cases[0]=Piece()
                        self.cases[3]=Piece('TOUR','noir')                
        
        # End pieces cases-----------------------------------------------
                
        # Any move cancels the ep move
        if(flagViderEp==True):
            self.ep=-1
            
        # Promote : the pawn is changed to requested piece
        if(promote!=''):
            if(promote=='q'):
                self.cases[arrivee]=Piece('DAME',self.side2move)
            elif(promote=='r'):
                self.cases[arrivee]=Piece('TOUR',self.side2move)
            elif(promote=='n'):
                self.cases[arrivee]=Piece('CAVALIER',self.side2move)
            elif(promote=='b'):
                self.cases[arrivee]=Piece('FOU',self.side2move)

        # Change side to move
        self.changeTrait()
            
        # Save move to the history list
        self.history.append((depart,\
        arrivee,\
        pieceDeplacee,\
        piecePrise,\
        isEp,\
        histEp,\
        promote,\
        hist_roque_56,\
        hist_roque_63,\
        hist_roque_0,\
        hist_roque_7))
		
        # If the move lets king in check, undo it and return false
        if(self.in_check(self.oppColor(self.side2move))):
            self.undomove()
            return False
            
        return True
        
    ####################################################################
    
    def undomove(self):
        
        if(len(self.history)==0):
            print('No move played')
            return

        # The last move in history is : self.historique[-1]
        lastmove=self.history[-1]
        
        pos1=lastmove[0]
        pos2=lastmove[1]
        piece_deplacee=lastmove[2]
        piece_prise=lastmove[3]
        isEp=lastmove[4]
        ep=lastmove[5]
        promote=lastmove[6]
        self.white_can_castle_56=lastmove[7]
        self.white_can_castle_63=lastmove[8]
        self.black_can_castle_0=lastmove[9]
        self.black_can_castle_7 =lastmove[10]
        
        self.ply-=1

        # Change side to move
        self.changeTrait()
                
        # Replacing piece on square number 'pos1'
        self.cases[pos1]=self.cases[pos2]
        
        # Square where we can take "en pasant"
        self.ep=ep
        
        # If undoing a promote, the piece was a pawn
        if(promote!=''):
            self.cases[pos1]=Piece('PION',self.side2move)

        # Replacing capture piece on square 'pos2'
        self.cases[pos2]=piece_prise

        # Switch the piece we have replaced to 'pos1'-------------------
        if(self.cases[pos1].nom=='PION'):
            # If a pawn has been taken "en passant", replace it
            if(isEp):
                self.cases[pos2]=Piece()
                if(self.cases[pos1].couleur=='noir'):
                    self.cases[pos2-8]=Piece('PION','blanc')
                else:
                    self.cases[pos2+8]=Piece('PION','noir')
                    
        # Replacing KING -----------------------------------------------
        elif(self.cases[pos1].nom=='ROI'):
            
            # White KING
            if(self.cases[pos1].couleur=='blanc'):
                # Replacing on initial square
                if(pos1==60):
                    # If the move was castle, replace ROOK
                    if(pos2==58):
                        self.cases[56]=Piece('TOUR','blanc')
                        self.cases[59]=Piece()
                    elif(pos2==62):
                        self.cases[63]=Piece('TOUR','blanc')
                        self.cases[61]=Piece()
            # Black KING
            else:
                if(pos1==4):
                    if(pos2==2):
                        self.cases[0]=Piece('TOUR','noir')
                        self.cases[3]=Piece()
                    elif(pos2==6):
                        self.cases[7]=Piece('TOUR','noir')
                        self.cases[5]=Piece()
        # End switch piece----------------------------------------------
 
        # Delete the last move from history
        self.history.pop()
            
    ####################################################################
    
    def changeTrait(self):
        
        "Change the side to move"
        
        if(self.side2move=='blanc'):
            self.side2move='noir'
        else:
            self.side2move='blanc'   
            
    ####################################################################
    
    def oppColor(self,c):
        
        "Returns the opposite color of the 'c' color given"
        
        if(c=='blanc'):
            return 'noir'
        else:
            return 'blanc'           

    ####################################################################

    def in_check(self,couleur):
        
        """Returns TRUE or FALSE 
        if the KING of the given 'color' is in check"""
        
        # Looking for the id square where is the king
        # sure, we can code better to avoid this and win kn/s...
        for i in range(0,64):
            if(self.cases[i].nom=='ROI' and self.cases[i].couleur==couleur):
                pos=i
                break

        return self.is_attacked(pos,self.oppColor(couleur))
        
    ####################################################################

    def is_attacked(self,pos,couleur):
        
        """Returns TRUE or FALSE if the square number 'pos' is a 
        destination square for the color 'couleur'.
        If so we can say that 'pos' is attacked by this side.
        This function is used for 'in check' and for castle moves."""
        
        mList=self.gen_moves_list(couleur,True)

        for pos1,pos2,promote in mList:
            if(pos2==pos):
                return True
        
        return False    
            
    ####################################################################
            
    def render(self, score, nodes, time, mode, nps):
        
        "Display the chessboard in console mode"
        os.system('cls' if os.name == 'nt' else 'clear')
   
        print('8',end='   ')
        i,y=1,7
        for piece in self.cases:
            if(piece.couleur=='noir'):
                print(piece.nom[0].lower(),end='   ')
            else:
                print(piece.nom[0],end='   ')
                                    
            if(i%8==0):
                print()
                print()
                if(y>0):
                    print(str(y),end='   ')
                y=y-1

            i+=1
        print('    a   b   c   d   e   f   g   h')
        if score >= 0:
            score_text = colorama.Fore.RED + str(round(-score, 2)) + colorama.Fore.WHITE
        else:
            score_text = colorama.Fore.GREEN + "+" + str(round(-score, 2)) + colorama.Fore.WHITE
        print()
        print("Le score pour le joueur humain est", score_text, ",", nodes, "positions analysées en", round(time,2), "secondes", "(", nps, "coups/seconde )")
        print('Aux', self.side2move, "de jouer.")
        print(mode)
        
    ####################################################################
    
    def get_current_position(self):
        """
        Returns the current position of the chess pieces on the board as a list.
        Each element of the list represents a square on the board and contains
        the piece in that square.
        """
        return self.cases
        
    ####################################################################
    
    def caseStr2Int(self,c):
        
        """'c' given in argument is a square name like 'e2'
        "This function returns a square number like 52"""

        err=(
        'The square name must be 2 caracters i.e. e2,e4,b1...',
        'Incorrect square name. Please enter i.e. e2,e4,b1...'
        )            
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
                
        if(len(c)!=2):
            print(err[0])
            return -1
        
        if(c[0] not in letters):
            print(err[1])
            return -1
            
        if(c[1] not in numbers):
            print(err[1])
            return -1
            
        return self.coord.index(c)
        
    ####################################################################
    
    def caseInt2Str(self,i):
        
        """Given in argument : an integer between 0 and 63
        Returns a string like 'e2'"""

        err=(
        'Square number must be in 0 to 63',
        )            
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
                
        if(i<0 or i>63):
            print(err[0])
            return

        return self.coord[i] 
        
    ####################################################################
    
    @staticmethod
    def ROW(x):
        """ROW returns the number of the row from 0(a8-h8) to 7(a1-h1)
        in which is the square 'x'"""
        return (x >> 3)

    ####################################################################

    @staticmethod
    def COL(x):
        """COL returns the number of the colon (from 0 to 7)
        in which is the square 'x'"""
        return (x & 7)
        
    ####################################################################
    
    def last_move(self):
        # Vérifiez d'abord si l'historique des mouvements n'est pas vide
        if len(self.history) < 2:
            return None  # Aucun mouvement n'a été enregistré

        # Récupérez le dernier mouvement de l'historique (c'est le plus récent)
        last_move = self.history[-2]

        # Obtenez les informations pertinentes sur le dernier mouvement
        (start_square, end_square, moved_piece, captured_piece, is_en_passant, en_passant_history, promotion, kingside_castle, queenside_castle, kingside_castle, queenside_castle) = last_move

        # Convertir les indices des cases en notation PGN (par exemple, de 0 à 'a8')
        start_square_pgn = self.caseInt2Str(start_square)
        end_square_pgn = self.caseInt2Str(end_square)

        # Gérer la promotion
        if promotion:
            last_move_pgn = f"{start_square_pgn}{end_square_pgn}{promotion}"
        else:
            last_move_pgn = f"{start_square_pgn}{end_square_pgn}"

        return last_move_pgn

    ####################################################################
    
    def showHistory(self, print_log):
        
        "Displays the history of the moves played"
        
        pgn = ""
        for (start_square, end_square, moved_piece, captured_piece, is_en_passant, en_passant_history, promotion, kingside_castle, queenside_castle, kingside_castle, queenside_castle) in self.history:

            # Convertir les indices des cases en notation PGN (par exemple, de 0 à 'a8')
            start_square_pgn = self.caseInt2Str(start_square)
            end_square_pgn = self.caseInt2Str(end_square)

            # Gérer la promotion
            if promotion:
                pgn += f"{start_square_pgn}{end_square_pgn}{promotion} "
            else:
                pgn += f"{start_square_pgn}{end_square_pgn} "

        histo = pgn.strip()
        if print_log == True:
            print()
            print("Pgn de la partie: ", histo)
            print("FEN de la position actuelle :", self.getboard())
            print()
        return histo
        
    ###################################################################
    
    def material_everyone(self):
        WhiteScore=0
        BlackScore=0
        for pos1,piece in enumerate(self.cases):
            if piece.nom == 'VIDE':
                continue

            if(piece.couleur=='blanc'):
                if piece.nom == 'PION':
                    WhiteScore += 1.2
                elif piece.nom == 'CAVALIER':
                    WhiteScore += 3.1
                elif piece.nom == 'FOU':
                    WhiteScore += 3.4
                elif piece.nom == 'TOUR':
                    WhiteScore += 5.3
                elif piece.nom == 'DAME':
                    WhiteScore += 8.5
                    
            elif(piece.couleur=='noir'): 
                if piece.nom == 'PION':
                    BlackScore += 1.2
                elif piece.nom == 'CAVALIER':
                    BlackScore += 3.1
                elif piece.nom == 'FOU':
                    BlackScore += 3.4
                elif piece.nom == 'TOUR':
                    BlackScore += 5.3
                elif piece.nom == 'DAME':
                    BlackScore += 8.5
                    
        return WhiteScore + BlackScore
    
    def material(self):
        WhiteScore=0
        BlackScore=0
        for pos1,piece in enumerate(self.cases): 
            if piece.nom == 'VIDE':
                continue

            if(piece.couleur=='blanc'):
                if piece.nom == 'PION':
                    WhiteScore += 1.2
                elif piece.nom == 'CAVALIER':
                    WhiteScore += 3.1
                elif piece.nom == 'FOU':
                    WhiteScore += 3.4
                elif piece.nom == 'TOUR':
                    WhiteScore += 5.3
                elif piece.nom == 'DAME':
                    WhiteScore += 8.5
                    
            elif(piece.couleur=='noir'): 
                if piece.nom == 'PION':
                    BlackScore += 1.2
                elif piece.nom == 'CAVALIER':
                    BlackScore += 3.1
                elif piece.nom == 'FOU':
                    BlackScore += 3.4
                elif piece.nom == 'TOUR':
                    BlackScore += 5.3
                elif piece.nom == 'DAME':
                    BlackScore += 8.5
    
        return WhiteScore - BlackScore
    
    ###################################################################
    
    def evaluer(self):
        
        """A wonderful evaluate() function returning score"""
        
        WhiteScore = 0
        BlackScore = 0
        
        total_material_score = self.material_everyone()
        
        # Parsing the board squares from 0 to 63
        for pos1,piece in enumerate(self.cases):       
            if piece.nom == 'VIDE':
                continue

            # Score ( using PESTO table )
            if(piece.couleur=='blanc'):
                WhiteScore += piece.valeur
                
                if piece.nom == 'PION':
                    if total_material_score < 40:
                        WhiteScore += pawn_position_bonus_END[pos1]/50
                    else:
                        WhiteScore += ((-(63-pos1)//8) + 3)/30
                
                elif piece.nom == 'CAVALIER':
                    WhiteScore += knight_position_bonus[pos1]/50
                
                elif piece.nom == 'FOU':
                    WhiteScore += bishop_position_bonus[pos1]/50
                
                if piece.nom == 'ROI':
                    if total_material_score < 30:
                        WhiteScore += king_position_bonus_END[pos1]/50
                    else:
                        WhiteScore += king_position_bonus[pos1]/50 
                        
                '''
                elif piece.nom == 'TOUR':
                    WhiteScore += rook_position_bonus[pos1]/50
                
                elif piece.nom == 'DAME':
                    WhiteScore += queen_position_bonus[pos1]/50
                '''
                
            elif(piece.couleur=='noir'): 
                BlackScore+=piece.valeur
                
                if piece.nom == 'PION':
                    if total_material_score < 40:
                        BlackScore += pawn_position_bonus_END[pos1^56]/50
                    else:
                        BlackScore += ((-(63-pos1^56)//8) + 3)/30
                
                elif piece.nom == 'CAVALIER':
                    BlackScore += knight_position_bonus[pos1^56]/50
                
                elif piece.nom == 'FOU':
                    BlackScore += bishop_position_bonus[pos1^56]/50
                                
                elif piece.nom == 'ROI':
                    if total_material_score < 30:
                        BlackScore += king_position_bonus_END[pos1^56]/50
                    else:
                        BlackScore += king_position_bonus[pos1^56]/50
                
                '''
                elif piece.nom == 'TOUR':
                    BlackScore += rook_position_bonus[pos1^56]/50
                
                elif piece.nom == 'DAME':
                    BlackScore += queen_position_bonus[pos1^56]/50
                '''

        r = random.randint(-10,10)/33
        if(self.side2move=='blanc'):
            return WhiteScore-BlackScore + r
        else:
            return BlackScore-WhiteScore + r
                        
pawn_position_bonus_END =  [ 0,  0,  0,  0,  0,  0,  0,  0,
                           150,150,150,150,150,150,150,150,
                            50, 50, 50, 50, 50, 50, 50, 50,
                            35, 35, 35, 35, 35, 35, 35, 35,
                            20, 20, 20, 20, 20, 20, 20, 20,
                             5,  5,  5,  5,  5,  5,  5,  5,
                             0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0]
        
knight_position_bonus = [-30,  0,-10,  0,  0,-10,  0,-30,
                         -20, -5,  0,  0,  0,  0, -5,-20,
                         -20,  0,  0, 15, 15,  0,  0,-20,
                         -10,  0, 15,  0,  0, 15,  0,-10,
                         -10,  0, 15,  0,  0, 15,  0,-10,
                         -30, 15, 15, 15, 15, 15, 15,-30,
                         -20, -5,  0,-10,-10,  0, -5,-20,
                         -30,-20,-10,  0,  0,-10,-20,-30]
        
bishop_position_bonus = [-20,-10,-10,-10,-10,-10,-10,-20,
                         -10,  0,  0,  0,  0,  0,  0,-10,
                          10,  0, 15, 10, 10, 15,  0, 10,
                         -10, 10,  5, 10, 10,  5, 10,-10,
                         -10,  0, 10, 10, 10, 10,  0,-10,
                          10, 10, 10,  0, -5, 10, 10, 10,
                         -10, 10,  0,-10,-10,  0, 15,-10,
                         -20,-10,-10,-10,-10,-10,-10,-30]
                         
king_position_bonus =  [-30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-20,-10, 20, 20,-10,-20,-30,
                        -30,-10, 20, 30, 30, 20,-10,-30,
                        -30,-10, 30, 30, 30, 30,-10,-30,
                        -30,-10, 30, 30, 30, 30,-10,-30,
                        -30,-10, 20, 30, 30, 20,-10,-30,
                        -30,-30,-20,-50,-50,-50, 20,-30,
                        -50, 30, 50,-30,  0,-30, 50,-50]
                        
king_position_bonus_END =  [-30,-40,-40,-50,-50,-40,-40,-30,
                            -30,-20,-10, 20, 20,-10,-20,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-10, 30, 30, 30, 30,-10,-30,
                            -30,-10, 30, 30, 30, 30,-10,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-30,-20, 10, 10,-20,-30,-30,
                            -30,-40,-40,-50,-50,-40,-40,-30]