from arquivos import ARQUIVO_LOG


def _ler_registros():
    try:
        with open(ARQUIVO_LOG, encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        return []

    registros = []
    for linha in linhas:
        partes = linha.strip().split(" | ")
        if len(partes) == 5:
            registros.append(tuple(partes))
        elif len(partes) == 3:  # formato antigo, sem usuário nem alvo
            registros.append((partes[0], partes[1], "-", partes[2], "-"))
    return registros


def _mostrar_registros(registros, mostrar_usuario):
    if not registros:
        print("Nenhum registro encontrado.")
        return
    for data, nivel, usuario, operacao, alvo in registros:
        detalhe = f" ({alvo})" if alvo != "-" else ""
        autor = f" {usuario}" if mostrar_usuario else ""
        print(f"{data} [{nivel}]{autor} {operacao}{detalhe}")
    print(f"\nTotal: {len(registros)} registro(s).")


def consultar_auditoria_usuario(email):
    print(f"\n=== Meu histórico ({email}) ===")
    meus = [r for r in _ler_registros() if r[2] == email]
    _mostrar_registros(meus, mostrar_usuario=False)


def consultar_auditoria_sistema():
    print("\n=== Auditoria do sistema ===")
    _mostrar_registros(_ler_registros(), mostrar_usuario=True)
