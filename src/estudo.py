import chess
import chess.svg

def atualizar_variacoes(abertura, aberturas_data):
    if abertura:
        return list(aberturas_data[abertura].keys())
    return []

def iniciar_estudo(abertura, variacao, aberturas_data):
    if not (abertura and variacao):
        return "", "", "", 0
    board = chess.Board()
    dados = aberturas_data[abertura][variacao]
    lances = dados['lances']
    explicacoes = dados.get('explicacoes', [])
    descricao = dados['descricao']
    jogadores = ", ".join(dados['jogadores'])
    info = f"**Descrição:** {descricao}\n\n**Jogadores famosos:** {jogadores}"
    explicacao_atual = explicacoes[0] if explicacoes else ""
    svg = chess.svg.board(board, size=400)
    return svg, info, explicacao_atual, 0

def navegar_lance(abertura, variacao, indice, aberturas_data):
    if not (abertura and variacao):
        return "", "", indice
    dados = aberturas_data[abertura][variacao]
    lances = dados['lances']
    explicacoes = dados.get('explicacoes', [])
    real_index = max(0, min(len(lances), indice))
    board = chess.Board()
    for lance in lances[:real_index]:
        try:
            board.push_san(lance)
        except Exception:
            break
    svg = chess.svg.board(board, size=400)
    explicacao = explicacoes[real_index] if explicacoes and real_index < len(explicacoes) else ""
    return svg, explicacao, real_index
