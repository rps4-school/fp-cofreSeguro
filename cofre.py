from arquivos import (
    carregar_credenciais,
    carregar_senhas_comuns,
    carregar_usuarios,
    definir_usuario_do_log,
    salvar_credenciais,
)
from auditoria import consultar_auditoria_sistema, consultar_auditoria_usuario
from csv_cofre import exportar_log_csv
from credenciais import (
    adicionar_credencial,
    cadastrar_categoria,
    consultar_categorias,
    editar_credencial,
    excluir_credencial,
    listar_credenciais,
    revelar_senha,
    verificar_senhas_repetidas,
    buscar_credenciais,
)
from usuarios import cadastrar_usuario, entrar
from senhas import gerar_senha_valida
from agent import perguntar_ao_agente
from resumo_seguranca import mostrar_resumo


def executar_menu(titulo, opcoes, texto_sair, mensagem_saida):
    while True:
        print(f"\n=== {titulo} ===")
        for numero, (descricao, _) in opcoes.items():
            print(f"{numero} - {descricao}")
        print(f"0 - {texto_sair}")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print(mensagem_saida)
            return
        descricao, acao = opcoes.get(escolha, (None, None))
        if acao is None:
            print("Opção inválida.")
            continue
        acao()


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

    def adicionar():
        adicionar_credencial(credenciais, categorias, senhas_comuns)
        salvar_credenciais(email, credenciais)

    def editar():
        editar_credencial(credenciais, categorias, senhas_comuns)
        salvar_credenciais(email, credenciais)

    def excluir():
        excluir_credencial(credenciais)
        salvar_credenciais(email, credenciais)

    opcoes = {
        "1": ("Adicionar credencial", adicionar),
        "2": ("Listar credenciais", lambda: listar_credenciais(credenciais)),
        "3": ("Revelar senha", lambda: revelar_senha(credenciais, hash_master)),
        "4": ("Editar credencial", editar),
        "5": ("Excluir credencial", excluir),
        "6": ("Cadastrar categoria", lambda: cadastrar_categoria(categorias)),
        "7": ("Consultar categorias", lambda: consultar_categorias(categorias)),
        "8": ("Criar senha aleatória", lambda: gerar_senha_valida(3, senhas_comuns)),
        "9": ("Verificar senhas repetidas", lambda: verificar_senhas_repetidas(credenciais, hash_master),),
        "10": ("Perguntar ao assistente de IA", lambda: perguntar_ao_agente(credenciais, senhas_comuns, hash_master),),
        "11": ("Meu histórico (auditoria)", lambda: consultar_auditoria_usuario(email)),
        "12": ("Auditoria do sistema", consultar_auditoria_sistema),
        "13": ("Exportar auditoria para CSV", exportar_log_csv),
        "14": ("Buscar credencial por trecho", lambda: buscar_credenciais(credenciais)),
        "15": ("Relatório de segurança", lambda: mostrar_resumo(credenciais, senhas_comuns)),

    }
    executar_menu("Menu do Cofre", opcoes, "Sair da conta", "Saindo da conta.")


def fazer_login(usuarios):
    email = entrar(usuarios)
    if email is not None:
        menu_principal(email, usuarios[email])
        definir_usuario_do_log(None)  # saiu da conta


def main():
    usuarios = carregar_usuarios()
    opcoes = {
        "1": ("Entrar", lambda: fazer_login(usuarios)),
        "2": ("Cadastrar usuário", lambda: cadastrar_usuario(usuarios)),
    }
    executar_menu("Cofre de Senhas", opcoes, "Sair", "Até logo!")


if __name__ == "__main__":
    main()
