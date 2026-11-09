import base64
import hashlib
import secrets

TAMANHO_SAL = 8


def gerar_chave(email):
    return hashlib.sha256(("cifra-cofreseguro:" + email).encode("utf-8")).digest()


def _fluxo_de_chave(chave, sal, tamanho):
    fluxo = b""
    contador = 0
    while len(fluxo) < tamanho:
        bloco = hashlib.sha256(chave + sal + contador.to_bytes(4, "big"))
        fluxo += bloco.digest()
        contador += 1
    return fluxo[:tamanho]


def criptografar(texto, chave):
    dados = texto.encode("utf-8")
    sal = secrets.token_bytes(TAMANHO_SAL)
    fluxo = _fluxo_de_chave(chave, sal, len(dados))
    cifrado = bytes(a ^ b for a, b in zip(dados, fluxo))
    return base64.b64encode(sal + cifrado).decode("ascii")


def descriptografar(texto_cifrado, chave):
    bruto = base64.b64decode(texto_cifrado.encode("ascii"))
    sal, cifrado = bruto[:TAMANHO_SAL], bruto[TAMANHO_SAL:]
    fluxo = _fluxo_de_chave(chave, sal, len(cifrado))
    return bytes(a ^ b for a, b in zip(cifrado, fluxo)).decode("utf-8")
