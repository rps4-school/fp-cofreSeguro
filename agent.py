import logging
import os

logger = logging.getLogger(__name__)

GROQ_MODEL = "openai/gpt-oss-120b"
CHARACTER_LIMIT = 20000

PROMPT_TEMPLATE = """Você é um assistente inteligente do sistema CofreSeguro.

Analise os dados fornecidos e responda a pergunta do usuário de forma clara e objetiva.

DADOS DO SISTEMA:
---
{content}
---

PERGUNTA DO USUÁRIO: {question}

INSTRUÇÕES:
1. Responda sempre em português do Brasil
2. Baseie sua resposta apenas nos dados fornecidos
3. Se os dados não contêm informação suficiente, diga isso claramente

Responda agora:"""


def _load_env():
    try:
        with open(".env", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, value = line.split("=", 1)
                name = name.strip()
                if name and name not in os.environ:
                    os.environ[name] = value.strip().strip("\"'")
    except OSError:
        pass


def ask_agent(content, question):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("A pergunta não pode ficar vazia.")
    if not content or not content.strip():
        raise ValueError("Não há dados para enviar. Cadastre credenciais antes.")
    if len(content) > CHARACTER_LIMIT:
        raise ValueError("Os dados excedem o limite de envio para o agente.")

    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError(
            "A biblioteca groq não está instalada. Instale com: pip install groq"
        ) from None

    _load_env()
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("Configure a variável GROQ_API_KEY no arquivo .env.")

    prompt = PROMPT_TEMPLATE.format(content=content, question=question.strip())

    try:
        completion = Groq(api_key=api_key).chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_completion_tokens=1024,
        )
    except Exception:
        logger.warning("Consulta ao agente de IA falhou.", extra={"status_code": 502})
        raise RuntimeError("Não foi possível consultar o agente de IA.") from None

    logger.info("Consulta ao agente de IA concluída.", extra={"status_code": 200})
    return completion.choices[0].message.content

DESCRICAO_SISTEMA = """O CofreSeguro é um gerenciador de credenciais de linha de comando.

Funcionalidades do menu principal:
1 - Adicionar credencial: cadastra serviço, usuário, senha e categoria. A senha \
pode ser digitada ou gerada automaticamente, e uma categoria nova pode ser \
criada durante o cadastro.
2 - Listar credenciais: mostra as credenciais com a senha mascarada.
3 - Revelar senha: exibe a senha de um serviço após confirmar a senha master.
4 - Editar credencial: altera serviço, usuário, observações ou senha.
5 - Excluir credencial: remove uma credencial após confirmação.
6 - Cadastrar categoria: cria uma categoria com exigência mínima de senha \
(1 fraca, 2 média, 3 forte).
7 - Consultar categorias: lista as categorias e suas exigências.
8 - Criar senha aleatória: gera uma senha forte de 16 caracteres.
9 - Verificar senhas repetidas: alerta quais serviços compartilham a mesma \
senha e se a senha master do cofre é reutilizada em algum serviço.
10 - Perguntar ao assistente de IA: este assistente.

Regras do sistema: a senha master tem no mínimo 16 caracteres e é guardada \
apenas como hash SHA-256; senhas não podem ser vazias nem conter espaços; a \
força da senha é avaliada por tamanho, mistura de maiúsculas/minúsculas, \
números, símbolos e presença em lista de senhas comuns; as ações ficam \
registradas em um log de auditoria que pode ser exportado para CSV."""


def montar_dados_para_agente(credenciais, senhas_comuns):
    """Monta um resumo das credenciais SEM incluir senhas nem usuários.

    Só metadados saem do computador: serviço, categoria, força da senha,
    se a senha está repetida e a data da última alteração.
    """
    from senhas import NIVEIS, avaliar_senha

    contagem_senhas = {}
    for credencial in credenciais:
        senha = credencial["senha"]
        contagem_senhas[senha] = contagem_senhas.get(senha, 0) + 1

    linhas = ["servico;categoria;forca_da_senha;senha_repetida;ultima_alteracao"]
    for credencial in credenciais:
        nivel, _ = avaliar_senha(credencial["senha"], senhas_comuns)
        repetida = "sim" if contagem_senhas[credencial["senha"]] > 1 else "nao"
        linhas.append(
            f"{credencial['servico']};{credencial['categoria']};"
            f"{NIVEIS[nivel]};{repetida};{credencial['alterada_em']}"
        )
    return "\n".join(linhas)


def perguntar_ao_agente(credenciais, senhas_comuns):
    from arquivos import registrar_log

    print("\nPergunte sobre o funcionamento do CofreSeguro ou sobre suas")
    print("credenciais. O assistente recebe a descrição do sistema e apenas")
    print("metadados das credenciais (serviço, categoria, força, repetição e")
    print("data). Senhas nunca são enviadas.")
    pergunta = input("Sua pergunta: ").strip()

    if credenciais:
        metadados = montar_dados_para_agente(credenciais, senhas_comuns)
    else:
        metadados = "nenhuma credencial cadastrada até o momento"

    dados = (
        f"{DESCRICAO_SISTEMA}\n\n"
        f"CREDENCIAIS DO USUÁRIO (metadados):\n{metadados}"
    )

    try:
        resposta = ask_agent(dados, pergunta)
    except (ValueError, RuntimeError) as erro:
        registrar_log("AVISO", "consulta ao agente de IA falhou")
        print(erro)
        return

    registrar_log("INFO", "consulta ao agente de IA")
    print("\n=== Assistente de IA ===")
    print(resposta)
