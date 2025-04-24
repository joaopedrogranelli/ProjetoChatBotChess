import gradio as gr
from estudo import analisar_tabuleiro
from utils import carregar_personalidade, carregar_aberturas_variacoes, carregar_dicas, carregar_quizzes
from chatbot import responder_chat, enviar_dica, enviar_quiz, responder_quiz
from estudo import atualizar_variacoes, iniciar_estudo, navegar_lance

PERSONALIDADE_FIXA = carregar_personalidade()
aberturas_data = carregar_aberturas_variacoes()
lista_aberturas = list(aberturas_data.keys())
dicas_xadrez = carregar_dicas()
quizzes_xadrez = carregar_quizzes()

def chat_or_quiz(mensagem, chat_hist):
    from chatbot import quiz_state
    quiz_em_andamento = "em_andamento" in quiz_state and quiz_state["em_andamento"]
    if quiz_em_andamento:
        feito, chat_hist = responder_quiz(mensagem, chat_hist)
        if feito:
            return "", chat_hist
    return responder_chat(mensagem, chat_hist)

with gr.Blocks(theme=gr.themes.Soft(), title="Xadrez Interativo") as demo:
    gr.Markdown("# ♟️ Plataforma de Xadrez: Chatbot + Estudo de Aberturas")
    gr.Markdown(f"**Personalidade do Bot:**\n\nEste Bot está programado para responder perguntas sobre xadrez de forma amigável e informativa. Ele pode ajudar com dúvidas sobre regras, estratégias e aberturas.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Chatbot de Dúvidas")
            chatbot = gr.Chatbot(label="Conversa com o Bot", elem_id="chat_area", type='messages')
            user_input = gr.Textbox(show_label=False, placeholder="Digite sua dúvida de xadrez...")
            btn_dica = gr.Button("Peça uma dica de xadrez", scale=1)
            btn_quiz = gr.Button("Fazer um quiz", scale=1)

            user_input.submit(
                lambda mensagem, chat_hist: chat_or_quiz(mensagem, chat_hist),
                [user_input, chatbot], [user_input, chatbot]
            )
            btn_dica.click(
                lambda chat_hist: enviar_dica(chat_hist, dicas_xadrez),
                [chatbot], [user_input, chatbot]
            )
            btn_quiz.click(
                lambda chat_hist: enviar_quiz(chat_hist, quizzes_xadrez),
                [chatbot], [user_input, chatbot]
            )

        with gr.Column(scale=2):
            gr.Markdown("## Estudo Interativo de Aberturas")
            abertura_dropdown = gr.Dropdown(label="Escolha a abertura", choices=lista_aberturas)
            variacao_dropdown = gr.Dropdown(label="Escolha a variação")

            info_output = gr.Markdown()
            explicacao_output = gr.Markdown()
            tabuleiro_output = gr.HTML()
            btn_analise = gr.Button("Analisar posição atual com Stockfish", scale=1)
            analise_output = gr.Markdown()
            with gr.Row():
                btn_anterior = gr.Button("◀️ Anterior")
                btn_reset = gr.Button("⏮️ Reiniciar")
                btn_proximo = gr.Button("Próximo ▶️")

            lance_atual = gr.State(0)
            ultima_abertura = gr.State("")
            ultima_variacao = gr.State("")

            abertura_dropdown.change(
                lambda ab: gr.update(choices=atualizar_variacoes(ab, aberturas_data), value=None),
                abertura_dropdown, variacao_dropdown
            )
            variacao_dropdown.change(
                lambda ab, var: (*iniciar_estudo(ab, var, aberturas_data), ab, var),
                [abertura_dropdown, variacao_dropdown],
                [tabuleiro_output, info_output, explicacao_output, lance_atual, ultima_abertura, ultima_variacao]
            )
            btn_proximo.click(
                lambda ab, var, idx: navegar_lance(ab, var, idx+1, aberturas_data),
                [abertura_dropdown, variacao_dropdown, lance_atual],
                [tabuleiro_output, explicacao_output, lance_atual]
            )
            btn_reset.click(
                lambda ab, var: navegar_lance(ab, var, 0, aberturas_data),
                [abertura_dropdown, variacao_dropdown],
                [tabuleiro_output, explicacao_output, lance_atual]
            )
            btn_anterior.click(
                lambda ab, var, idx: navegar_lance(ab, var, idx-1, aberturas_data),
                [abertura_dropdown, variacao_dropdown, lance_atual],
                [tabuleiro_output, explicacao_output, lance_atual]
            )
            btn_analise.click(
                lambda ab, var, idx: analisar_tabuleiro(aberturas_data, ab, var, idx),
                [abertura_dropdown, variacao_dropdown, lance_atual],
                analise_output
            )

demo.launch()
