import os
from datetime import datetime

from gerador_senha import SIMBOLOS, gerar_senha
from agent import montar_dados_para_agente, ocultar_senhas
from arquivos import (
    CATEGORIAS_PADRAO,
    carregar_categorias,
    carregar_credenciais,
    nome_arquivo_categorias,
    nome_arquivo_credenciais,
    salvar_categorias,
    salvar_credenciais,
)
from cifra import criptografar, descriptografar, gerar_chave
from credenciais import buscar_por_trecho, servico_ja_existe
from resumo_seguranca import dias_sem_alterar
from senhas import avaliar_senha, esconder_senha, gerar_hash

SENHAS_COMUNS_TESTE = ["123456", "senha", "qwerty"]

FRACA = 1
MEDIA = 2
FORTE = 3


def criar_credencial(servico, senha):
    return {
        "servico": servico,
        "usuario": "pessoa.ficticia",
        "senha": senha,
        "categoria": "outros",
        "observacoes": "",
        "alterada_em": "01/01/2026 10:00",
    }


# =================
# FORÇA DA SENHA
# =================

def teste_senha_fraca():
    senha = "abc"

    nivel, motivos = avaliar_senha(senha, SENHAS_COMUNS_TESTE)

    assert nivel == FRACA
    assert "tem menos de 8 caracteres" in motivos


def teste_senha_media():
    senha = "Abcdefg1"

    nivel, motivos = avaliar_senha(senha, SENHAS_COMUNS_TESTE)

    assert nivel == MEDIA
    assert "não tem símbolos" in motivos


def teste_senha_forte():
    senha = "Abcdefgh123!"

    nivel, motivos = avaliar_senha(senha, SENHAS_COMUNS_TESTE)

    assert nivel == FORTE
    assert motivos == []


def teste_senha_comum_sempre_fraca():
    senha = "Senha"

    nivel, motivos = avaliar_senha(senha, SENHAS_COMUNS_TESTE)

    assert nivel == FRACA
    assert "ATENÇÃO: está na lista de senhas comuns" in motivos


# ====================
# MÁSCARA DA SENHA
# ====================


def teste_esconder_senha_tamanho_fixo():
    senha_curta = "bobao1"
    senha_longa = "Abcdefghijklmnop"

    mascara_curta = esconder_senha(senha_curta)
    mascara_longa = esconder_senha(senha_longa)

    assert mascara_curta == "bo********"
    assert len(mascara_curta) == len(mascara_longa)


def teste_esconder_senha_muito_curta():
    senha = "abc"

    mascara = esconder_senha(senha)

    assert mascara == "********"


# ==================
# GERADOR DE SENHA
# ==================

def teste_gerador_usa_simbolos_que_o_avaliador_conhece():
    senhas_geradas = []
    for _ in range(100):
        senhas_geradas.append(gerar_senha())

    for senha in senhas_geradas:
        for caractere in senha:
            if not caractere.isalnum():
                assert caractere in SIMBOLOS


# ===================
# BUSCA POR TRECHO
# ===================

def teste_busca_por_trecho():
    credenciais = [
        criar_credencial("Email Escola", "x"),
        criar_credencial("Mail Trabalho", "y"),
        criar_credencial("Banco", "z"),
    ]

    encontradas = buscar_por_trecho(credenciais, "MAIL")

    nomes_encontrados = []
    for credencial in encontradas:
        nomes_encontrados.append(credencial["servico"])
    assert nomes_encontrados == ["Email Escola", "Mail Trabalho"]


def teste_busca_sem_resultado():
    credenciais = [criar_credencial("Banco", "z")]

    encontradas = buscar_por_trecho(credenciais, "xyz")

    assert encontradas == []


def teste_servico_ja_existe():
    credenciais = [criar_credencial("Google", "x")]

    assert servico_ja_existe(credenciais, "google")
    assert not servico_ja_existe(credenciais, "Banco")


# ========
# CIFRA
# ========

def teste_cifra_ida_e_volta():
    chave = gerar_chave("teste@email.com")
    senha = "Senha@123"

    cifrada = criptografar(senha, chave)
    decifrada = descriptografar(cifrada, chave)

    assert cifrada != senha
    assert decifrada == senha


def teste_cifra_com_sal():
    chave = gerar_chave("teste@email.com")
    senha = "Senha@123"

    primeira = criptografar(senha, chave)
    segunda = criptografar(senha, chave)

    assert primeira != segunda


# ========================
# RELATÓRIO DE SEGURANÇA
# ========================


def teste_dias_sem_alterar():
    hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
    credencial_de_hoje = {"alterada_em": hoje}
    credencial_antiga = {"alterada_em": "01/01/2020 10:00"}
    credencial_data_errada = {"alterada_em": "data errada"}
    credencial_sem_data = {}

    dias_hoje = dias_sem_alterar(credencial_de_hoje)
    dias_antiga = dias_sem_alterar(credencial_antiga)
    dias_errada = dias_sem_alterar(credencial_data_errada)
    dias_sem_data = dias_sem_alterar(credencial_sem_data)

    assert dias_hoje == 0
    assert dias_antiga > 365
    assert dias_errada is None
    assert dias_sem_data is None


# ========
# AGENTE
# ========

def teste_agente_nao_recebe_senhas_nem_usuarios():
    senha_repetida = "SenhaSecreta#1"
    senha_unica = "OutraSenha$99"
    credenciais = [
        criar_credencial("Google", senha_repetida),
        criar_credencial("Youtube", senha_repetida),
        criar_credencial("Banco", senha_unica),
    ]

    dados = montar_dados_para_agente(credenciais, SENHAS_COMUNS_TESTE)

    assert senha_repetida not in dados
    assert senha_unica not in dados
    assert "pessoa.ficticia" not in dados

    assert "Google;outros;forte;sim;" in dados
    assert "Banco;outros;forte;nao;" in dados


def teste_ocultar_senhas_na_pergunta():
    credenciais = [criar_credencial("Google", "Gato@2024")]
    pergunta = "minha senha Gato@2024, ta boa?"

    texto, ocultadas = ocultar_senhas(pergunta, credenciais)

    assert "Gato@2024" not in texto
    assert "[oculto]" in texto
    assert ocultadas == 1


def teste_ocultar_senha_master():
    senha_master = "MinhaSenhaMaster123"
    hash_master = gerar_hash(senha_master)
    pergunta = f"a master é {senha_master}"

    texto, ocultadas = ocultar_senhas(pergunta, [], hash_master)

    assert senha_master not in texto
    assert ocultadas == 1


EMAIL_TESTE = "teste.categorias@ficticio.com"


def apagar_arquivo_categorias():
    if os.path.exists(nome_arquivo_categorias(EMAIL_TESTE)):
        os.remove(nome_arquivo_categorias(EMAIL_TESTE))


def teste_categorias_sem_arquivo():
    apagar_arquivo_categorias()

    categorias = carregar_categorias(EMAIL_TESTE)

    assert categorias == CATEGORIAS_PADRAO


def teste_salvar_e_carregar_categorias():
    categorias = carregar_categorias(EMAIL_TESTE)
    categorias["jogos"] = 1

    salvar_categorias(EMAIL_TESTE, categorias)
    carregadas = carregar_categorias(EMAIL_TESTE)
    apagar_arquivo_categorias()

    assert carregadas == categorias
    assert carregadas["jogos"] == 1


def teste_categorias_linha_errada():
    with open(nome_arquivo_categorias(EMAIL_TESTE), "w", encoding="utf-8") as arquivo:
        arquivo.write("jogos;1\n")
        arquivo.write("linha sem separador\n")
        arquivo.write("musica;abc\n")
        arquivo.write("filmes;7\n")

    categorias = carregar_categorias(EMAIL_TESTE)
    apagar_arquivo_categorias()

    assert categorias["jogos"] == 1
    assert "musica" not in categorias
    assert "filmes" not in categorias


# ===========================
# ARQUIVO DE CREDENCIAIS
# ===========================

EMAIL_TESTE_CREDENCIAIS = "teste.credenciais@ficticio.com"


def apagar_arquivo_credenciais():
    if os.path.exists(nome_arquivo_credenciais(EMAIL_TESTE_CREDENCIAIS)):
        os.remove(nome_arquivo_credenciais(EMAIL_TESTE_CREDENCIAIS))


def teste_credenciais_sem_arquivo():
    apagar_arquivo_credenciais()

    credenciais = carregar_credenciais(EMAIL_TESTE_CREDENCIAIS)

    assert credenciais == []


def teste_salvar_e_carregar_credenciais():
    credenciais = [
        criar_credencial("Google", "Gato@2024"),
        criar_credencial("Banco", "OutraSenha$99"),
    ]

    salvar_credenciais(EMAIL_TESTE_CREDENCIAIS, credenciais)
    carregadas = carregar_credenciais(EMAIL_TESTE_CREDENCIAIS)
    apagar_arquivo_credenciais()

    assert carregadas == credenciais


def teste_senha_cifrada_no_arquivo():
    credenciais = [criar_credencial("Google", "Gato@2024")]

    salvar_credenciais(EMAIL_TESTE_CREDENCIAIS, credenciais)
    with open(nome_arquivo_credenciais(EMAIL_TESTE_CREDENCIAIS), encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    apagar_arquivo_credenciais()

    assert "Google" in conteudo
    assert "Gato@2024" not in conteudo


# ==========
# EXECUÇÃO
# ==========

def rodar_testes():
    testes = [
        teste_senha_fraca,
        teste_senha_media,
        teste_senha_forte,
        teste_senha_comum_sempre_fraca,
        teste_esconder_senha_tamanho_fixo,
        teste_esconder_senha_muito_curta,
        teste_gerador_usa_simbolos_que_o_avaliador_conhece,
        teste_busca_por_trecho,
        teste_busca_sem_resultado,
        teste_servico_ja_existe,
        teste_cifra_ida_e_volta,
        teste_cifra_com_sal,
        teste_dias_sem_alterar,
        teste_agente_nao_recebe_senhas_nem_usuarios,
        teste_ocultar_senhas_na_pergunta,
        teste_ocultar_senha_master,
        teste_categorias_sem_arquivo,
        teste_salvar_e_carregar_categorias,
        teste_categorias_linha_errada,
        teste_credenciais_sem_arquivo,
        teste_salvar_e_carregar_credenciais,
        teste_senha_cifrada_no_arquivo,
    ]
    passou = 0
    falhou = 0
    for teste in testes:
        try:
            teste()
            print(f"OK      {teste.__name__}")
            passou = passou + 1
        except AssertionError:
            print(f"FALHOU  {teste.__name__}")
            falhou = falhou + 1
    print(f"\n{passou} passaram, {falhou} falharam.")


if __name__ == "__main__":
    rodar_testes()
