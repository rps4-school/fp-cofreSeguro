from datetime import datetime
from getpass import getpass

from arquivos import registrar_log
from senhas import NIVEIS, esconder_senha, gerar_hash, pedir_senha_valida


def data_de_agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def consultar_categorias(categorias):
    print("\nCategorias cadastradas:")
    for nome, minimo in categorias.items():
        print(f"- {nome} (senha no mínimo {NIVEIS[minimo]})")


def cadastrar_categoria(categorias):
    nome = input("Nome da categoria: ").strip().lower()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return
    print("Exigência mínima de senha: 1 - fraca, 2 - média, 3 - forte")
    opcao = input("Escolha (1, 2 ou 3): ").strip()
    if opcao not in ("1", "2", "3"):
        print("Opção inválida. Categoria não cadastrada.")
        return
    categorias[nome] = int(opcao)
    registrar_log("INFO", f"Categoria cadastrada: {nome}")
    print(f"Categoria '{nome}' salva com exigência mínima {NIVEIS[int(opcao)]}.")


def escolher_categoria(categorias):
    consultar_categorias(categorias)
    nome = input("Categoria da credencial: ").strip().lower()
    if nome in categorias:
        return nome
    print("Categoria não encontrada. Usando 'outros'.")
    return "outros"


def encontrar_credencial(credenciais):
    servico = input("Nome do serviço: ").strip().lower()
    for credencial in credenciais:
        if credencial["servico"].lower() == servico:
            return credencial
    print("Credencial não encontrada.")
    return None


def adicionar_credencial(credenciais, categorias, senhas_comuns):
    servico = input("Nome do serviço: ").strip()
    if servico == "":
        print("O nome do serviço não pode ficar vazio.")
        return
    usuario = input("Usuário ou e-mail: ").strip()
    categoria = escolher_categoria(categorias)
    senha = pedir_senha_valida(categoria, categorias, senhas_comuns)
    observacoes = input("Observações: ").strip()
    credenciais.append(
        {
            "servico": servico,
            "usuario": usuario,
            "senha": senha,
            "categoria": categoria,
            "observacoes": observacoes,
            "alterada_em": data_de_agora(),
        }
    )
    registrar_log("INFO", f"Credencial adicionada: {servico}")
    print("Credencial salva.")


def listar_credenciais(credenciais):
    if not credenciais:
        print("Nenhuma credencial cadastrada.")
        return
    for numero, credencial in enumerate(credenciais, start=1):
        print(f"\n{numero}) {credencial['servico']}")
        print(f"   Usuário: {credencial['usuario']}")
        print(f"   Senha: {esconder_senha(credencial['senha'])}")
        print(f"   Categoria: {credencial['categoria']}")
        print(f"   Observações: {credencial['observacoes']}")
        print(f"   Última alteração: {credencial['alterada_em']}")


def revelar_senha(credenciais, hash_master):
    credencial = encontrar_credencial(credenciais)
    if credencial is None:
        return
    senha_master = getpass("Confirme a senha master: ")
    if gerar_hash(senha_master) != hash_master:
        registrar_log(
            "AVISO", f"Revelação recusada (senha master errada): {credencial['servico']}"
        )
        print("Senha master incorreta.")
        return
    registrar_log("INFO", f"Senha revelada: {credencial['servico']}")
    print(f"Senha de {credencial['servico']}: {credencial['senha']}")


def editar_credencial(credenciais, categorias, senhas_comuns):
    credencial = encontrar_credencial(credenciais)
    if credencial is None:
        return
    print("Deixe em branco para manter o valor atual.")
    servico = input(f"Novo serviço [{credencial['servico']}]: ").strip()
    usuario = input(f"Novo usuário [{credencial['usuario']}]: ").strip()
    observacoes = input(f"Novas observações [{credencial['observacoes']}]: ").strip()
    if servico != "":
        credencial["servico"] = servico
    if usuario != "":
        credencial["usuario"] = usuario
    if observacoes != "":
        credencial["observacoes"] = observacoes
    trocar = input("Trocar a senha? (s/n): ").strip().lower()
    if trocar == "s":
        credencial["senha"] = pedir_senha_valida(
            credencial["categoria"], categorias, senhas_comuns
        )
    credencial["alterada_em"] = data_de_agora()
    registrar_log("INFO", f"Credencial editada: {credencial['servico']}")
    print("Credencial atualizada.")


def excluir_credencial(credenciais):
    credencial = encontrar_credencial(credenciais)
    if credencial is None:
        return
    confirmacao = input(f"Digite SIM para excluir '{credencial['servico']}': ")
    if confirmacao.strip().upper() == "SIM":
        credenciais.remove(credencial)
        registrar_log("INFO", f"Credencial excluída: {credencial['servico']}")
        print("Credencial excluída.")
    else:
        print("Exclusão cancelada.")
