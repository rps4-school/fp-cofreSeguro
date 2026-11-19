import json
from datetime import datetime

from cifra import criptografar, descriptografar, gerar_chave

ARQUIVO_SENHAS_COMUNS = "senhas_comuns.txt"
ARQUIVO_USUARIOS = "usuarios.txt"
ARQUIVO_LOG = "cofre.log"

CATEGORIAS_PADRAO = {
    "banco": 3,
    "rede social": 2,
    "estudo": 1,
    "trabalho": 2,
    "outros": 1,
}

CAMPOS_CREDENCIAL = ["servico", "usuario", "senha", "categoria", "observacoes", "alterada_em"]


# guarda quem está logado para o log registrar o autor de cada operação,
# sem precisar passar o e-mail para todas as funções
USUARIO_DO_LOG = {"email": "-"}


def definir_usuario_do_log(email):
    USUARIO_DO_LOG["email"] = email if email else "-"


def registrar_log(nivel, operacao, alvo="-"):
    """Registra: data e hora | nível | usuário | operação | alvo afetado."""
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
            arquivo.write(
                f"{data} | {nivel} | {USUARIO_DO_LOG['email']} | {operacao} | {alvo}\n"
            )
    except OSError:
        print("Aviso: não foi possível gravar o registro de auditoria.")


def carregar_senhas_comuns():
    try:
        with open(ARQUIVO_SENHAS_COMUNS, encoding="utf-8") as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        print(
            f"Aviso: {ARQUIVO_SENHAS_COMUNS} não encontrado. "
            "A verificação de senhas comuns está desligada."
        )
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
    try:
        with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{email};{hash_senha}\n")
    except OSError:
        print("Erro: não foi possível salvar o usuário. Verifique a permissão da pasta.")
        return False
    return True


def nome_arquivo_categorias(email):
    return f"categorias_{email}.txt"


def carregar_categorias(email):
    categorias = dict(CATEGORIAS_PADRAO)
    try:
        with open(nome_arquivo_categorias(email), encoding="utf-8") as arquivo:
            for linha in arquivo:
                try:
                    nome, nivel = linha.strip().rsplit(";", 1)
                    nivel = int(nivel)
                except ValueError:
                    continue
                if nome != "" and nivel in (1, 2, 3):
                    categorias[nome] = nivel
    except FileNotFoundError:
        pass
    return categorias


def salvar_categorias(email, categorias):
    try:
        with open(nome_arquivo_categorias(email), "w", encoding="utf-8") as arquivo:
            for nome, nivel in categorias.items():
                arquivo.write(f"{nome};{nivel}\n")
    except OSError:
        print("Erro: não foi possível salvar as categorias. Verifique a permissão da pasta.")


def nome_arquivo_credenciais(email):
    return f"credenciais_{email}.json"


def carregar_credenciais(email):
    try:
        with open(nome_arquivo_credenciais(email), encoding="utf-8") as arquivo:
            credenciais = json.load(arquivo)
        chave = gerar_chave(email)
        for credencial in credenciais:
            if credencial.pop("senha_cifrada", False):
                credencial["senha"] = descriptografar(credencial["senha"], chave)
            for campo in CAMPOS_CREDENCIAL:
                credencial.setdefault(campo, "")
    except FileNotFoundError:
        return []
    except (ValueError, KeyError, TypeError, AttributeError, OSError):
        print("Erro: o arquivo de credenciais está corrompido e não pode ser aberto.")
        return None
    return credenciais


def salvar_credenciais(email, credenciais):
    chave = gerar_chave(email)
    para_gravar = []
    for credencial in credenciais:
        copia = dict(credencial)
        copia["senha"] = criptografar(copia["senha"], chave)
        copia["senha_cifrada"] = True
        para_gravar.append(copia)
    try:
        with open(nome_arquivo_credenciais(email), "w", encoding="utf-8") as arquivo:
            json.dump(para_gravar, arquivo, ensure_ascii=False, indent=2)
    except OSError:
        print("Erro: não foi possível salvar as credenciais. Verifique a permissão da pasta.")
