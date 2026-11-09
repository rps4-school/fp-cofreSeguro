from arquivos import (
    carregar_credenciais,
    carregar_senhas_comuns,
    carregar_usuarios,
    salvar_credenciais,
)
from credenciais import (
    adicionar_credencial,
    cadastrar_categoria,
    consultar_categorias,
    editar_credencial,
    excluir_credencial,
    listar_credenciais,
    revelar_senha,
)
from usuarios import cadastrar_usuario, entrar
from gerador_senha import gerar_senha

def mostrar_menu_inicial():
    print("\n=== Cofre de Senhas ===")
    print("1 - Entrar")
    print("2 - Cadastrar usuário")
    print("0 - Sair")


def mostrar_menu_principal():
    print("\n=== Menu do Cofre ===")
    print("1 - Adicionar credencial")
    print("2 - Listar credenciais")
    print("3 - Revelar senha")
    print("4 - Editar credencial")
    print("5 - Excluir credencial")
    print("6 - Cadastrar categoria")
    print("7 - Consultar categorias")
    print("8 - Criar senha aleatória")
    print("0 - Sair da conta")


def menu_principal(email, hash_master):
    credenciais = carregar_credenciais(email)
    categorias = {
        "banco": 3,
        "rede social": 2,
        "estudo": 1,
        "trabalho": 2,
        "outros": 1,
    }
    senhas_comuns = carregar_senhas_comuns()

    while True:
        mostrar_menu_principal()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Saindo da conta.")
            break
        elif opcao == "1":
            adicionar_credencial(credenciais, categorias, senhas_comuns)
            salvar_credenciais(email, credenciais)
        elif opcao == "2":
            listar_credenciais(credenciais)
        elif opcao == "3":
            revelar_senha(credenciais, hash_master)
        elif opcao == "4":
            editar_credencial(credenciais, categorias, senhas_comuns)
            salvar_credenciais(email, credenciais)
        elif opcao == "5":
            excluir_credencial(credenciais)
            salvar_credenciais(email, credenciais)
        elif opcao == "6":
            cadastrar_categoria(categorias)
        elif opcao == "7":
            consultar_categorias(categorias)
        elif opcao == "8":
            senha = gerar_senha()
            print(senha)
        else:
            print("Opção inválida.")


def main():
    usuarios = carregar_usuarios()

    while True:
        mostrar_menu_inicial()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        elif opcao == "1":
            email = entrar(usuarios)
            if email is not None:
                menu_principal(email, usuarios[email])
        elif opcao == "2":
            cadastrar_usuario(usuarios)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
