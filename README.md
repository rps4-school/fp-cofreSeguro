# Projeto: "CofreSeguro" — Gerenciador de Credenciais Didático

## Sobre o projeto

Esse projeto tem como objetivo abordar os temas aprendidos na disciplina Fundamentos de Programação, do primeiro período do curso de Ciência da Computação.

## Descrição do Problema

Lucas tem conta em dezenas de serviços: e-mail, banco, redes sociais, plataformas da faculdade, jogos. Para não esquecer, ele usa a mesma senha em quase todos e quando um site exige senha diferente, anota num bloco de notas do celular. Ele sabe que isso é um problema, mas não sabe o tamanho do problema. Não faz ideia de quantas senhas repetidas tem, quais são fracas, nem o que aconteceria se um daqueles sites vazasse. Vamos criar o sistema "CofreSeguro", que ajudará Lucas (e outras pessoas) a organizar suas credenciais, entender a força de cada senha, e enxergar os riscos que hoje ele não vê.

## Estrutura do projeto

O projeto é dividido em 7 partes sendo elas:

* CRUD de Credenciais
* Análise de força de senha
* Detecção de Risco
* Registro de auditoria
* Armazenamento de Dados
* Relatório de Segurança
* Funcionalidade Extra

## Como rodar

Requisito: Python 3 instalado.

Todos os comandos abaixo devem ser executados dentro da pasta do projeto (`fp-cofreSeguro`), pois o programa lê e grava os arquivos de dados nessa pasta.

1. Crie o ambiente virtual (só na primeira vez):

```
python -m venv .venv
```

2. Ative o ambiente virtual (toda vez que abrir um terminal novo):

```
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução de scripts, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo. Se estiver usando o **cmd** em vez do PowerShell, o comando é `.venv\Scripts\activate.bat`.

3. Instale as dependências (só na primeira vez):

```
pip install -r requirements.txt
```

4. Configure a chave do assistente de IA (opcional, só para a opção "Perguntar ao assistente de IA"):
   * copie o arquivo `.env.example` e renomeie a cópia para `.env`;
   * crie uma chave em https://console.groq.com/keys e coloque no lugar de `sua_chave_aqui`.

   O arquivo `.env` não vai para o GitHub. Nunca compartilhe sua chave.

5. Execute o programa:

```
python cofre.py
```

## Como usar

### Tela inicial

| Opção | O que faz |
|---|---|
| 1 - Entrar | Faz login com seu e-mail e sua senha master. |
| 2 - Cadastrar usuário | Cria uma conta nova (e-mail + senha master). |
| 0 - Sair | Fecha o programa. |

A **senha master** precisa ter **no mínimo 16 caracteres** e **não pode ter espaços**. Ela protege o cofre inteiro, por isso a exigência é maior que a das outras senhas.

### Menu do Cofre (depois de entrar)

**Credenciais**

| Opção | O que faz |
|---|---|
| 1 - Adicionar credencial | Pede o nome do serviço, o usuário/e-mail, a categoria, a senha e observações. Não deixa cadastrar dois serviços com o mesmo nome. A senha pode ser digitada ou gerada automaticamente e precisa atingir o nível mínimo da categoria. |
| 2 - Listar credenciais | Mostra todas as credenciais com a senha escondida, a categoria e a data da última alteração. A senha aparece como os 2 primeiros caracteres seguidos de **sempre 8 asteriscos** (ex.: `Ab********`). Senhas com menos de 5 caracteres ficam totalmente escondidas. O número fixo de asteriscos serve para não revelar o tamanho da senha. |
| 3 - Revelar senha | Pede o nome do serviço e **confirma a senha master** antes de mostrar a senha. Se a senha master estiver errada, a tentativa fica registrada na auditoria. |
| 4 - Editar credencial | Altera serviço, usuário, observações, categoria e senha. Deixe o campo em branco para manter o valor atual. Se a nova categoria exigir uma senha mais forte, o programa obriga a trocar a senha. |
| 5 - Excluir credencial | Pede o nome do serviço e só exclui se você digitar **SIM**. |
| 14 - Buscar credencial por trecho | Procura serviços digitando só parte do nome (ex.: "goo" encontra "Google"). |

**Categorias**

| Opção | O que faz |
|---|---|
| 6 - Cadastrar categoria | Cria uma categoria nova (ex.: "jogos", "streaming"). |
| 7 - Consultar categorias | Lista as categorias cadastradas e a força mínima de senha de cada uma. |

Ao criar uma categoria, você escolhe a força mínima de senha exigida (fraca, média ou forte). Se você digitar uma categoria que não existe ao adicionar uma credencial, o programa oferece cadastrá-la na hora. Se você recusar, a credencial vai para a categoria "outros".

**Segurança**

| Opção | O que faz |
|---|---|
| 8 - Criar senha aleatória | Gera uma senha forte que não está na lista de senhas comuns. |
| 9 - Verificar senhas repetidas | Avisa se a mesma senha é usada em mais de um serviço **e se a senha master do cofre também é usada em algum serviço**. |
| 10 - Perguntar ao assistente de IA | Tira dúvidas sobre as suas senhas e sobre segurança (precisa da chave configurada no `.env`). O assistente **nunca recebe as senhas**: só são enviados metadados (serviço, categoria, força, se é repetida e a data de alteração), e qualquer senha digitada na pergunta vira `[oculto]` antes de ser enviada. |
| 15 - Relatório de segurança | Mostra um resumo da situação das suas senhas: quantas são fracas, repetidas ou comuns e há quanto tempo não são alteradas. |

**Auditoria**

| Opção | O que faz |
|---|---|
| 11 - Meu histórico | Mostra as ações que você fez no cofre. |
| 12 - Auditoria do sistema | Mostra o registro geral de ações do sistema. |
| 13 - Exportar auditoria para CSV | Salva o log de auditoria no arquivo `log_auditoria.csv`, que pode ser aberto no Excel. |
| 0 - Sair da conta | Volta para a tela inicial. |

Tudo o que você adiciona, edita ou exclui é salvo automaticamente.

## Critérios de força da senha

Toda senha cadastrada passa por uma avaliação que dá **1 ponto** para cada critério cumprido:

| Critério | Ponto |
|--- | ---|
| Tem pelo menos 8 caracteres | +1 |
| Tem pelo menos 12 caracteres | +1 |
| Mistura letras minúsculas e maiúsculas | +1 |
| Tem números | +1 |
| Tem símbolos | +1 |

| Pontos | Nível |
|---|---|
| 0 a 2 | Fraca |
| 3 ou 4 | Média |
| 5 | Forte |

Além da nota, o programa mostra **os motivos**, ou seja, o que faltou para a senha ficar mais forte.

### Por que esses critérios?

- **Por que 8 e 12 caracteres:** cada caractere a mais multiplica o número de combinações que um atacante precisa testar. Por isso o tamanho conta duas vezes. 8 é o mínimo aceitável e 12 é o tamanho em que a senha fica bem mais difícil de quebrar por tentativa e erro.
- **Por que até 2 pontos é fraca:** cumprir só 2 critérios é fácil demais. Por exemplo, `abcdefgh1` tem 9 caracteres e um número (2 pontos), mas só usa letras minúsculas e números, o que ainda é fácil de adivinhar.
- **Por que a lista de senhas comuns derruba a nota:** senhas como `123456` ou `senha123` são as primeiras que um atacante testa. Por isso, se a senha estiver no arquivo `senhas_comuns.txt`, ela é classificada como **fraca**, mesmo que tenha pontos suficientes para ser média ou forte. Uma senha "bonita" como `Senha@123`, por exemplo, seria média, mas vira fraca se estiver na lista.

### Outras regras

- A senha não pode ficar vazia nem ter espaços.
- Cada **categoria** pode exigir um nível mínimo de força. Se a senha não alcançar esse nível, o programa pede outra.
- A opção **8 (Criar senha aleatória)** só entrega senhas de nível **forte**.

A explicação completa do relatório de segurança está em [Resumo de segurança](DOCS/resumo_seguranca.md).

## Restrições

- Este é um projeto **didático**, feito para a disciplina, e **não deve ser usado para guardar senhas reais**.
- Use **somente dados fictícios** (e-mails e senhas inventados).
- Por que não serve para uso real:
  - As senhas das credenciais são **cifradas** no arquivo, mas a chave da cifra é gerada a partir do **e-mail**. Quem tiver o código e o arquivo consegue decifrar tudo sem a senha master. Um cofre real usaria a senha master para gerar a chave. Além disso, a cifra foi feita pelo grupo, para fins didáticos, e não usa um algoritmo testado e reconhecido.
  - **Não há limite de tentativas de login**, então alguém pode ficar testando senhas master sem ser bloqueado.
  - A senha master é guardada com SHA-256 **sem "sal"**. Esse é um hash muito rápido, e um atacante com o arquivo consegue testar milhões de senhas por segundo. Sistemas reais usam algoritmos lentos e com sal, como bcrypt ou Argon2.
  - Os dados ficam em **arquivos de texto no computador**, que qualquer pessoa com acesso à máquina pode copiar.
  - O log de auditoria também fica em arquivo comum, então pode ser apagado ou alterado por quem tiver acesso ao computador.
  - O assistente de IA envia as perguntas para um serviço externo (Groq). Para reduzir o risco, as senhas nunca são enviadas: só metadados, e senhas digitadas na pergunta viram `[oculto]`.

## Bibliotecas usadas

- **Externa:** `groq` (assistente de IA), instalada pelo `requirements.txt`.
- **Biblioteca padrão do Python:** `json`, `hashlib`, `secrets`, `base64`, `getpass`, `datetime`, `os`, `string` e `logging`.

## Documentações

* [Definições do projeto](https://github.com/rps4-school/fp-cofreSeguro/blob/main/DOCS/definicoes_projeto.md)
* [Busca de credencial por trecho (funcionalidade extra)](https://github.com/rps4-school/fp-cofreSeguro/blob/main/DOCS/busca_por_trecho.md)
* [Resumo de segurança](https://github.com/rps4-school/fp-cofreSeguro/blob/main/DOCS/resumo_seguranca.md)
* [Manual do usuário](https://github.com/rps4-school/fp-cofreSeguro/blob/main/DOCS/manual_usuario.md)

## Grupo

* Lucas Mendes Bezerra Galindo
* Genival da Hora e Silva Neto
* Nunno Wakiyama Diniz Carvalho
* Lucas Barros Cavalcanti
* Mateus Farias dos Santos
* Raphael Pinheiro dos Santos