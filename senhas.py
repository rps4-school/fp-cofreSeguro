import hashlib
from getpass import getpass

from gerador_senha import gerar_senha

SIMBOLOS = "!@#$%&*()-_=+[]{};:,.?/"
NIVEIS = {1: "fraca", 2: "média", 3: "forte"}
QUANTIDADE_ASTERISCOS = 8
TAMANHO_MINIMO_PARA_MOSTRAR = 5


def gerar_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def esconder_senha(senha):
    if len(senha) < TAMANHO_MINIMO_PARA_MOSTRAR:
        return "*" * QUANTIDADE_ASTERISCOS
    return senha[:2] + "*" * QUANTIDADE_ASTERISCOS


def avaliar_senha(senha, senhas_comuns):
    motivos = []
    pontos = 0

    if len(senha) >= 8:
        pontos = pontos + 1
    else:
        motivos.append("tem menos de 8 caracteres")

    if len(senha) >= 12:
        pontos = pontos + 1
    else:
        motivos.append("tem menos de 12 caracteres")

    if any(letra.islower() for letra in senha) and any(
        letra.isupper() for letra in senha
    ):
        pontos = pontos + 1
    else:
        motivos.append("não mistura letras minúsculas e maiúsculas")

    if any(letra.isdigit() for letra in senha):
        pontos = pontos + 1
    else:
        motivos.append("não tem números")

    if any(letra in SIMBOLOS for letra in senha):
        pontos = pontos + 1
    else:
        motivos.append("não tem símbolos")

    if senha.lower() in senhas_comuns:
        motivos.append("ATENÇÃO: está na lista de senhas comuns")
        return 1, motivos

    if pontos <= 2:
        return 1, motivos
    if pontos <= 4:
        return 2, motivos
    return 3, motivos


def mostrar_avaliacao(nivel, motivos):
    print(f"Força da senha: {NIVEIS[nivel]}")
    if motivos:
        print("Motivos:")
        for motivo in motivos:
            print(f"- {motivo}")
    else:
        print("- atende todos os critérios de uma senha forte")


def gerar_senha_valida(minimo, senhas_comuns):
    while True:
        senha = gerar_senha()
        nivel, motivos = avaliar_senha(senha, senhas_comuns)
        if nivel >= minimo:
            print(f"Senha gerada: {senha}")
            mostrar_avaliacao(nivel, motivos)
            return senha


def pedir_senha_valida(categoria, categorias, senhas_comuns):
    minimo = categorias[categoria]
    while True:
        escolha = input("Gerar senha automaticamente? (s/n): ").strip().lower()
        if escolha == "s":
            return gerar_senha_valida(minimo, senhas_comuns)
        senha = getpass("Senha: ")
        if senha == "":
            print("A senha não pode ficar vazia.")
            continue
        if any(caractere.isspace() for caractere in senha):
            print("A senha não pode conter espaços.")
            continue
        nivel, motivos = avaliar_senha(senha, senhas_comuns)
        mostrar_avaliacao(nivel, motivos)
        if nivel >= minimo:
            return senha
        print(
            f"A categoria '{categoria}' exige senha no mínimo "
            f"{NIVEIS[minimo]}. Tente outra."
        )
