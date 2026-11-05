from getpass import getpass

from arquivos import registrar_log, salvar_usuario
from senhas import gerar_hash

TAMANHO_MINIMO_SENHA_MASTER = 16


def cadastrar_usuario(usuarios):
    email = input("E-mail: ").strip().lower()
    if email == "" or ";" in email:
        print("E-mail inválido.")
        return
    if email in usuarios:
        print("Já existe um usuário com esse e-mail.")
        return
    senha = getpass(
        f"Senha master (mínimo {TAMANHO_MINIMO_SENHA_MASTER} caracteres): "
    )
    if len(senha) < TAMANHO_MINIMO_SENHA_MASTER:
        print(
            "A senha master deve ter pelo menos "
            f"{TAMANHO_MINIMO_SENHA_MASTER} caracteres."
        )
        return
    usuarios[email] = gerar_hash(senha)
    salvar_usuario(email, usuarios[email])
    registrar_log("INFO", f"Usuário cadastrado: {email}")
    print("Usuário cadastrado. Agora escolha 'Entrar'.")


def entrar(usuarios):
    email = input("E-mail: ").strip().lower()
    senha = getpass("Senha master: ")
    if email in usuarios and usuarios[email] == gerar_hash(senha):
        registrar_log("INFO", f"Login realizado: {email}")
        print(f"Bem-vindo(a), {email}!")
        return email
    registrar_log("AVISO", f"Tentativa de login recusada: {email}")
    print("E-mail ou senha master incorretos.")
    return None
