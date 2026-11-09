import secrets
import string


def gerar_senha():
    caracteres = (string.ascii_letters + string.digits + string.punctuation)
    senha = ''.join(secrets.choice(caracteres) for _ in range(16))
    
    return senha
