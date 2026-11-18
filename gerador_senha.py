import secrets
import string

SIMBOLOS = "!@#$%&*()-_=+[]{};:,.?/"
TAMANHO_SENHA = 16


def gerar_senha():
    caracteres = string.ascii_letters + string.digits + SIMBOLOS
    senha = ""
    for _ in range(TAMANHO_SENHA):
        senha = senha + secrets.choice(caracteres)
    return senha
