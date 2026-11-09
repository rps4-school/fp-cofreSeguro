import os

ARQUIVO_LOG = "cofre.log"
ARQUIVO_CSV = "log_auditoria.csv"


def exportar_log_csv():
    if not os.path.exists(ARQUIVO_LOG):
        print("Log não encontrado.")
        return False

    with open(ARQUIVO_LOG, encoding="utf-8") as log:
        linhas = log.readlines()

    total = 0
    with open(ARQUIVO_CSV, "w", encoding="utf-8-sig") as csv:
        csv.write("data;nivel;mensagem\n")
        for linha in linhas:
            partes = linha.strip().split(" | ", 2)
            if len(partes) == 3:
                mensagem = partes[2].replace(";", ",").replace('"', "'")
                csv.write(f"{partes[0]};{partes[1]};{mensagem}\n")
                total += 1

    print(f"{total} registros exportados para {ARQUIVO_CSV}")
    return True