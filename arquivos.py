import json
from datetime import datetime

ARQUIVO_SENHAS_COMUNS = "senhas_comuns.txt"
ARQUIVO_USUARIOS = "usuarios.txt"
ARQUIVO_LOG = "cofre.log"


def registrar_log(nivel, mensagem):
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{data} | {nivel} | {mensagem}\n")


def carregar_senhas_comuns():
    try:
        with open(ARQUIVO_SENHAS_COMUNS, encoding="utf-8") as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        return []


def carregar_usuarios():
    usuarios = {}
    try:
        with open(ARQUIVO_USUARIOS, encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if ";" in linha:
                    email, hash_senha = linha.split(";", 1)
                    usuarios[email] = hash_senha
    except FileNotFoundError:
        pass
    return usuarios


def salvar_usuario(email, hash_senha):
    with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{email};{hash_senha}\n")


def nome_arquivo_credenciais(email):
    return f"credenciais_{email}.json"


def carregar_credenciais(email):
    try:
        with open(nome_arquivo_credenciais(email), encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar_credenciais(email, credenciais):
    with open(nome_arquivo_credenciais(email), "w", encoding="utf-8") as arquivo:
        json.dump(credenciais, arquivo, ensure_ascii=False, indent=2)
