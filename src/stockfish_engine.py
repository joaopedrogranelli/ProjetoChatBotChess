import chess
import chess.engine
import os

# Caminho para o executável do Stockfish
STOCKFISH_PATH = os.path.join(os.path.dirname(__file__), '..', 'stockfish', 'stockfish-windows-x86-64-avx2.exe')

def analisar_fen(fen, engine_path="stockfish-windows-x86-64-avx2.exe"): 
    board = chess.Board(fen)
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        result = engine.analyse(board, chess.engine.Limit(time=0.1))
        uci_move = result['pv'][0].uci()  # Melhor lance em UCI (ex: 'g8f6')
        san_move = board.san(chess.Move.from_uci(uci_move))  # Converte para SAN (ex: 'Nf6')
        score = result['score'].white().score(mate_score=10000)
        # Retorna SAN em vez de UCI
        return san_move, score


# Exemplo de uso rápido
if __name__ == "__main__":
    fen_inicial = chess.STARTING_FEN
    lance, avaliacao = analisar_fen(fen_inicial)
    print("Melhor lance:", lance)
    print("Avaliação:", avaliacao)
