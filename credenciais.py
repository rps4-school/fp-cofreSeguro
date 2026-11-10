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


def cadastrar_categoria(categorias, nome=None):
    """Cadastra uma categoria e devolve o nome dela (ou None se falhar)."""
    if nome is None:
        nome = input("Nome da categoria: ").strip().lower()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return None
    print("Exigência mínima de senha: 1 - fraca, 2 - média, 3 - forte")
    opcao = input("Escolha (1, 2 ou 3): ").strip()
    if opcao not in ("1", "2", "3"):
        print("Opção inválida. Categoria não cadastrada.")
        return None
    categorias[nome] = int(opcao)
    registrar_log("INFO", "cadastro de categoria", nome)
    print(f"Categoria '{nome}' salva com exigência mínima {NIVEIS[int(opcao)]}.")
    return nome


def escolher_categoria(categorias):
    consultar_categorias(categorias)
    nome = input("Categoria da credencial: ").strip().lower()
    if nome in categorias:
        return nome
    if nome != "":
        criar = input(
            f"A categoria '{nome}' não existe. Cadastrar agora? (s/n): "
        ).strip().lower()
        if criar == "s" and cadastrar_categoria(categorias, nome) is not None:
            return nome
    print("Usando a categoria 'outros'.")
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
    registrar_log("INFO", "adicionar credencial", servico)
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
            "AVISO", "revelação recusada (senha master errada)", credencial["servico"]
        )
        print("Senha master incorreta.")
        return
    registrar_log("INFO", "revelar senha", credencial["servico"])
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
    registrar_log("INFO", "editar credencial", credencial["servico"])
    print("Credencial atualizada.")


def verificar_senhas_repetidas(credenciais, hash_master):
    if not credenciais:
        print("Nenhuma credencial cadastrada.")
        return
    # agrupa os serviços pela senha usada
    grupos = {}
    for credencial in credenciais:
        senha = credencial["senha"]
        if senha not in grupos:
            grupos[senha] = []
        grupos[senha].append(credencial["servico"])

    encontrou_risco = False
    for senha, servicos in grupos.items():
        if len(servicos) > 1:
            encontrou_risco = True
            print(f"\nALERTA: a mesma senha é usada em {len(servicos)} serviços:")
            for servico in servicos:
                print(f"- {servico}")
            print("Se um desses serviços vazar, todos os outros ficam expostos.")
        if gerar_hash(senha) == hash_master:
            encontrou_risco = True
            print("\nALERTA: a senha master do cofre também é usada em:")
            for servico in servicos:
                print(f"- {servico}")
            print("Quem descobrir essa senha ganha acesso ao cofre inteiro.")

    if encontrou_risco:
        registrar_log("AVISO", "verificar senhas repetidas", "risco detectado")
    else:
        print("Nenhuma senha repetida encontrada. Tudo certo!")


def excluir_credencial(credenciais):
    credencial = encontrar_credencial(credenciais)
    if credencial is None:
        return
    confirmacao = input(f"Digite SIM para excluir '{credencial['servico']}': ")
    if confirmacao.strip().upper() == "SIM":
        credenciais.remove(credencial)
        registrar_log("INFO", "excluir credencial", credencial["servico"])
        print("Credencial excluída.")
    else:
        print("Exclusão cancelada.")
