import chess.pgn

def convertir_en_uci(partie):
    uci_moves = []
    board = partie.board()
    for move in partie.mainline_moves():
        uci_moves.append(board.uci(move))
        board.push(move)
    return " ".join(uci_moves)

def convertir_pgn_en_uci(fichier_pgn, fichier_uci):
    with open(fichier_pgn) as pgn_file:
        with open(fichier_uci, "w") as uci_file:
            while True:
                partie = chess.pgn.read_game(pgn_file)
                if partie is None:
                    break
                uci_moves = convertir_en_uci(partie)
                uci_file.write(uci_moves + "\n")
                print(uci_moves)

if __name__ == "__main__":
    fichier_pgn = "parties.pgn"
    fichier_uci = "openingbook.txt"
    convertir_pgn_en_uci(fichier_pgn, fichier_uci)
    print("Conversion terminée. Les parties UCI ont été enregistrées dans", fichier_uci)