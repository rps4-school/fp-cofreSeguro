# Projeto: "CofreSeguro" — Gerenciador de Credenciais Didático
## Sobre o projeto
Esse projeto tem como objetivo abordar os temas aprendindos da disciplina do primeiro período do curso de Ciência da Computação **Fundamentos de Programação**.


## Descrição do Problema
Lucas tem conta em dezenas de serviços: e-mail, banco, redes sociais, plataformas da faculdade,
jogos. Para não esquecer, ele usa a mesma senha em quase todos e quando um site exige senha
diferente, anota num bloco de notas do celular.
Ele sabe que isso é um problema, mas não sabe o tamanho do problema. Não faz ideia de quantas
senhas repetidas tem, quais são fracas, nem o que aconteceria se um daqueles sites vazasse.
Vamos criar o sistema "CofreSeguro", que ajudará Lucas (e outras pessoas) a organizar suas
credenciais, entender a força de cada senha, e enxergar os riscos que hoje ele não vê.

## Estrutura do projeto
O projeto é dividido em 7 partes sendo elas:
- CRUD de Credenciais
- Análise de força de senha
- Detecção de Risco
- Registro de auditoria
- Armazenamento de Dados
- Relatório de Segurança
- Funcionalidade Extra

## Como rodar

Requisito: Python 3 instalado.

Todos os comandos abaixo devem ser executados **dentro da pasta do projeto** (`fp-cofreSeguro`), pois o programa lê e grava os arquivos de dados nessa pasta.

1. Crie o ambiente virtual (só na primeira vez):
   ```
   python -m venv .venv
   ```
2. Ative o ambiente virtual (toda vez que abrir um terminal novo):
   ```
   .venv\Scripts\Activate.ps1
   ```
   Se o PowerShell bloquear a execução de scripts, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.
3. Instale as dependências (só na primeira vez):
   ```
   pip install -r requirements.txt
   ```
4. Configure a chave do assistente de IA (opcional, só para a opção "Perguntar ao assistente de IA"):
   - copie o arquivo `.env.example` e renomeie a cópia para `.env`;
   - crie uma chave em https://console.groq.com/keys e coloque no lugar de `sua_chave_aqui`.

   O arquivo `.env` não vai para o GitHub. Nunca compartilhe sua chave.
5. Execute o programa:
   ```
   python cofre.py
   ```

# Documentações
- [Definições do projeto](DOCS/definicoes_projeto.md)
- [Busca de credencial por trecho (funcionalidade extra)](DOCS/busca_por_trecho.md)
- [Resumo de segurança](DOCS/resumo_seguranca.md)


# Grupo:
- Lucas Mendes Bezerra Galindo
- Genival da Hora e Silva Neto
- Nunno Wakiyama Diniz Carvalho
- Lucas Barros Cavalcanti
- Mateus Farias dos Santos
- Raphael Pinheiro dos Santos
