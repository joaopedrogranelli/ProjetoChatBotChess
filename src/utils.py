import os
import json

def resource_path(rel_path):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, rel_path)

def carregar_personalidade():
    with open(resource_path(os.path.join("json", "personalidade.json")), "r", encoding="utf-8") as f:
        return json.load(f)["texto"]

def carregar_aberturas_variacoes():
    with open(resource_path(os.path.join("json", "aberturas_variacoes.json")), "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_dicas():
    with open(resource_path(os.path.join("json", "dicas.json")), "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_quizzes():
    with open(resource_path(os.path.join("json", "quizzes.json")), "r", encoding="utf-8") as f:
        return json.load(f)
