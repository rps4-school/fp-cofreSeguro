import os

ARQUIVO_LOG = "cofre.log"
ARQUIVO_CSV = "log_auditoria.csv"


def exportar_log_csv():
    if not os.path.exists(ARQUIVO_LOG):
        print("Log não encontrado.")
        return False

    try:
        with open(ARQUIVO_LOG, encoding="utf-8") as log:
            linhas = log.readlines()
    except (OSError, ValueError):
        print("Erro: não foi possível ler o log.")
        return False

    total = 0
    try:
        with open(ARQUIVO_CSV, "w", encoding="utf-8-sig") as csv:
            csv.write("data;nivel;usuario;operacao;alvo\n")
            for linha in linhas:
                partes = [p.replace(";", ",") for p in linha.strip().split(" | ")]
                if len(partes) == 3:  # formato antigo, sem usuário nem alvo
                    partes = [partes[0], partes[1], "-", partes[2], "-"]
                if len(partes) == 5:
                    csv.write(";".join(partes) + "\n")
                    total += 1
    except OSError:
        print(
            f"Erro: não foi possível salvar {ARQUIVO_CSV}. "
            "Verifique a permissão da pasta ou se o arquivo está aberto em outro programa."
        )
        return False

    print(f"{total} registros exportados para {ARQUIVO_CSV}")
    return True