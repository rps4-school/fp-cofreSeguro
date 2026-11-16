from datetime import datetime

from senhas import avaliar_senha


def dias_sem_alterar(credencial):
    texto = credencial.get("alterada_em", "")
    try:
        data = datetime.strptime(texto, "%d/%m/%Y %H:%M")
    except ValueError:
        return None
    return (datetime.now() - data).days


def mostrar_resumo(credenciais, senhas_comuns):
    senhas = [c["senha"] for c in credenciais]
    fracas = 0
    comuns = 0
    repetidas = 0

    for credencial in credenciais:
        senha = credencial["senha"]
        nivel, motivos = avaliar_senha(senha, senhas_comuns)
        if nivel == 1:
            fracas = fracas + 1
        if senha.lower() in senhas_comuns:
            comuns = comuns + 1
        if senhas.count(senha) > 1:
            repetidas = repetidas + 1

    print("\n=== Resumo de segurança ===")
    print(f"Credenciais: {len(credenciais)}")
    print(f"Senhas fracas: {fracas}")
    print(f"Senhas repetidas: {repetidas}")
    print(f"Senhas na lista de comuns: {comuns}")

    print("\nTempo sem alterar:")
    for credencial in credenciais:
        dias = dias_sem_alterar(credencial)
        if dias is None:
            print(f"- {credencial['servico']}: data desconhecida")
        else:
            print(f"- {credencial['servico']}: há {dias} dias")