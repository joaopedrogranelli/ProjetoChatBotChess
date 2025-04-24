import requests
import os

from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

quiz_state = {}

def responder_chat(mensagem, chat_hist):
    if not mensagem.strip():
        return "", chat_hist

    contexto = "Você é um mestre internacional de xadrez. Responda dúvidas sobre regras, aberturas e estratégias de forma didática, precisa e somente sobre xadrez.\n"
    for msg in chat_hist[-8:]:
        if msg["role"] == "user":
            contexto += f"Usuário: {msg['content']}\n"
        elif msg["role"] == "assistant":
            contexto += f"Bot: {msg['content']}\n"
    contexto += f"Usuário: {mensagem}\nBot:"

    payload = {
        "inputs": contexto,
        "parameters": {
            "max_new_tokens": 1500,
            "temperature": 0.1,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            resposta = response.json()[0]["generated_text"].strip()
        else:
            resposta = f"(Erro na IA: {response.status_code})"
    except Exception as e:
        resposta = f"(Erro ao conectar com IA: {e})"

    chat_hist = chat_hist + [
        {"role": "user", "content": mensagem},
        {"role": "assistant", "content": resposta}
    ]
    return "", chat_hist

def enviar_dica(chat_hist, dicas_xadrez):
    import os
    dica = dicas_xadrez[os.urandom(1)[0] % len(dicas_xadrez)]
    new_hist = chat_hist.copy()
    new_hist.append({"role": "assistant", "content": f"Dica de Xadrez: {dica}"})
    return "", new_hist

def enviar_quiz(chat_hist, quizzes_xadrez):
    import os
    quiz = quizzes_xadrez[os.urandom(1)[0] % len(quizzes_xadrez)]
    pergunta = quiz["pergunta"]
    resposta = quiz["resposta"]
    quiz_state["em_andamento"] = resposta
    new_hist = chat_hist.copy()
    new_hist.append({"role": "assistant", "content": f"Quiz de Xadrez: {pergunta}"})
    return "", new_hist

def responder_quiz(mensagem, chat_hist):
    if "em_andamento" not in quiz_state or not quiz_state["em_andamento"]:
        return False, chat_hist
    resposta_correta = quiz_state["em_andamento"].strip().lower()
    resposta_usuario = mensagem.strip().lower()
    if resposta_correta in resposta_usuario:
        chat_hist = chat_hist + [
            {"role": "assistant", "content": f"Correto! 🎉 {quiz_state['em_andamento']} é a resposta certa!"}
        ]
    else:
        chat_hist = chat_hist + [
            {"role": "assistant", "content": f"Não é bem isso. A resposta correta era: {quiz_state['em_andamento']}."}
        ]
    quiz_state["em_andamento"] = None
    return True, chat_hist
