# Manual do Usuário — CofreSeguro

Este manual explica, passo a passo, como usar o CofreSeguro. Para instalar e rodar o programa, veja a seção "Como rodar" do [README](../README.md).

> O CofreSeguro é um projeto **didático**. Use **somente dados fictícios** (e-mails e senhas inventados). Veja o porquê em [Restrições](#8-restrições).

## Sumário

1. [Primeiros passos](#1-primeiros-passos)
2. [Credenciais](#2-credenciais)
3. [Categorias](#3-categorias)
4. [Força da senha](#4-força-da-senha)
5. [Ferramentas de segurança](#5-ferramentas-de-segurança)
6. [Auditoria](#6-auditoria)
7. [Dúvidas comuns](#7-dúvidas-comuns)
8. [Restrições](#8-restrições)

---

## 1. Primeiros passos

### 1.1 Criar uma conta

1. Rode o programa com `python cofre.py`.
2. Na tela **Cofre de Senhas**, digite `2` (Cadastrar usuário).
3. Informe seu e-mail e crie uma **senha master**.

A senha master precisa ter **no mínimo 16 caracteres** e **não pode ter espaços**. Ela é a "chave" do cofre: é pedida para entrar e para revelar senhas, por isso a exigência é maior que a das outras senhas. Não use a mesma senha master em nenhum outro serviço.

### 1.2 Entrar

1. Na tela **Cofre de Senhas**, digite `1` (Entrar).
2. Informe o e-mail e a senha master.
3. Se estiverem corretos, abre o **Menu do Cofre**.

### 1.3 Navegar pelos menus

Todos os menus funcionam igual: digite o **número** da opção e aperte Enter.

- `0` no Menu do Cofre: sai da conta e volta para a tela inicial.
- `0` na tela inicial: fecha o programa.
- Um número que não existe mostra "Opção inválida." e o menu aparece de novo.

Tudo o que você adiciona, edita ou exclui é **salvo automaticamente**.

---

## 2. Credenciais

Uma credencial é um login guardado no cofre. Ela tem: **serviço** (ex.: Instagram), **usuário/e-mail**, **senha**, **categoria**, **observações** e a **data da última alteração**.

### 2.1 Adicionar credencial (opção 1)

1. Digite `1`.
2. **Nome do serviço:** ex.: `Instagram`. Não pode ficar vazio nem repetir um serviço que já existe. Para mudar um que já existe, use a opção 4.
3. **Usuário ou e-mail:** o login usado nesse serviço.
4. **Categoria:** o programa mostra as categorias existentes. Digite uma delas. Se digitar uma que não existe, ele pergunta se quer cadastrá-la na hora. Se responder `n`, a credencial vai para a categoria `outros`.
5. **"Gerar senha automaticamente? (s/n)"**
   - `s`: o programa cria uma senha que atende a exigência da categoria.
   - `n`: você digita a senha. Ela não aparece na tela enquanto você digita, isso é normal.
6. O programa mostra a **força da senha** e os motivos. Se a senha for mais fraca do que a categoria exige, ele pede outra.
7. **Observações:** opcional. Aperte Enter para deixar em branco.
8. Aparece "Credencial salva."

### 2.2 Listar credenciais (opção 2)

Mostra todas as credenciais numeradas. A senha aparece **escondida**: os 2 primeiros caracteres e depois **sempre 8 asteriscos**, qualquer que seja o tamanho da senha. Senhas com menos de 5 caracteres aparecem só como `********`.

Por que sempre 8 asteriscos? Se o número de asteriscos acompanhasse o tamanho da senha, quem olhasse a tela já saberia quantos caracteres ela tem, o que facilita adivinhar.

Exemplo:

```
1) Instagram
   Usuário: lucas@email.com
   Senha: Ab********
   Categoria: rede social
   Observações:
   Última alteração: 18/11/2026 21:30
```

### 2.3 Revelar senha (opção 3)

1. Digite `3`.
2. Informe o **nome do serviço** (maiúsculas e minúsculas não importam).
3. Confirme a **senha master**.
4. Se estiver correta, a senha completa aparece. Se estiver errada, aparece "Senha master incorreta." e a tentativa é registrada na auditoria.

### 2.4 Editar credencial (opção 4)

1. Digite `4` e informe o nome do serviço.
2. Para cada campo (serviço, usuário, observações), digite o novo valor ou **aperte Enter para manter o atual**. O valor atual aparece entre colchetes.
3. **"Trocar a categoria? (s/n)"**: se `s`, escolha a nova categoria.
4. **"Trocar a senha? (s/n)"**: se `s`, siga o mesmo processo da adição.

Se você trocar para uma categoria que exige senha mais forte e a senha atual não for suficiente, o programa **obriga** você a escolher uma nova. A data de "Última alteração" só muda quando a senha é trocada.

### 2.5 Excluir credencial (opção 5)

1. Digite `5` e informe o nome do serviço.
2. Digite **`SIM`** para confirmar. Qualquer outra coisa cancela a exclusão.

A exclusão não pode ser desfeita.

### 2.6 Buscar credencial por trecho (opção 14)

Digite só parte do nome do serviço. Por exemplo, `goo` encontra `Google` e `Google Drive`. O resultado aparece no mesmo formato da listagem, com as senhas escondidas.

---

## 3. Categorias

Categorias organizam as credenciais e definem **a força mínima de senha** exigida. Por exemplo, a categoria "banco" pode exigir senha **forte**, enquanto "jogos" aceita **média**.

### 3.1 Cadastrar categoria (opção 6)

1. Digite `6`.
2. Informe o nome (é salvo em letras minúsculas).
3. Escolha a exigência mínima: `1` fraca, `2` média ou `3` forte.

### 3.2 Consultar categorias (opção 7)

Lista as categorias e a exigência de cada uma, por exemplo:

```
- banco (senha no mínimo forte)
- jogos (senha no mínimo média)
```

---

## 4. Força da senha

Sempre que uma senha é criada ou trocada, o programa dá **1 ponto** por critério cumprido:

| Critério | Ponto |
|---|---|
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

**Senha comum = sempre fraca.** Se a senha estiver na lista de senhas comuns (`senhas_comuns.txt`), ela é fraca não importa quantos pontos tenha, porque essas são as primeiras senhas que um atacante tenta.

Além do nível, o programa mostra **o que faltou**. Exemplo:

```
Força da senha: média
Motivos:
- tem menos de 12 caracteres
- não tem símbolos
```

Outras regras: a senha não pode ficar vazia nem ter espaços.

### Por que esses critérios?

- **8 e 12 caracteres:** cada caractere a mais multiplica as combinações que um atacante precisa testar. 8 é o mínimo aceitável e 12 já deixa a senha bem mais difícil de quebrar.
- **Até 2 pontos é fraca:** cumprir só 2 critérios é fácil demais. `abcdefgh1` tem 2 pontos e ainda é fácil de adivinhar.
- **Lista de comuns:** uma senha como `Senha@123` parece boa (média), mas se estiver na lista é das primeiras a ser testada.

Mais detalhes em [Resumo de segurança](resumo_seguranca.md).

---

## 5. Ferramentas de segurança

### 5.1 Criar senha aleatória (opção 8)

Gera e mostra uma senha **forte** que não está na lista de senhas comuns. Útil para copiar e usar em um serviço.

### 5.2 Verificar senhas repetidas (opção 9)

Mostra dois tipos de alerta:

- **Mesma senha em vários serviços:** se um deles vazar, todos os outros ficam expostos.
- **Senha master usada em algum serviço:** quem descobrir essa senha ganha acesso ao cofre inteiro.

Se estiver tudo certo, aparece "Nenhuma senha repetida encontrada. Tudo certo!".

### 5.3 Perguntar ao assistente de IA (opção 10)

Permite fazer perguntas sobre segurança e sobre as suas senhas. Só funciona com a chave da Groq configurada no arquivo `.env` (veja o README).

O assistente **nunca recebe as suas senhas**. Ele só recebe metadados de cada credencial: serviço, categoria, força da senha, se ela é repetida e a data da última alteração. Se você digitar uma senha dentro da pergunta, ela é trocada por `[oculto]` antes de ser enviada.

### 5.4 Relatório de segurança (opção 15)

Mostra um resumo da sua situação:

- quantas credenciais você tem;
- quantas senhas são fracas;
- quantas senhas estão repetidas;
- quantas estão na lista de senhas comuns;
- há quantos dias cada credencial não é alterada.

O relatório **nunca mostra senhas**, só o nome dos serviços.

---

## 6. Auditoria

O programa registra as ações importantes (adicionar, editar, excluir, revelar senha, tentativas com senha master errada etc.) em um log.

| Opção | O que faz |
|---|---|
| 11 - Meu histórico | Mostra só as suas ações. |
| 12 - Auditoria do sistema | Mostra o registro geral do sistema. |
| 13 - Exportar auditoria para CSV | Salva o log no arquivo `log_auditoria.csv`, que pode ser aberto no Excel. |

---

## 7. Dúvidas comuns

**A senha não aparece enquanto eu digito.**
É de propósito, para ninguém ver por cima do seu ombro. Digite normalmente e aperte Enter.

**"Já existe uma credencial para ...".**
Cada serviço só pode ter uma credencial. Use a opção 4 para editar a que já existe.

**"A categoria ... exige senha no mínimo ...".**
A senha é mais fraca do que a categoria pede. Digite uma senha mais forte ou responda `s` para gerar uma automaticamente.

**"Credencial não encontrada."**
Confira o nome do serviço. Ele precisa ser o nome completo. Para procurar por parte do nome, use a opção 14.

**"A senha master precisa ter...".**
A senha master precisa ter no mínimo 16 caracteres e não pode ter espaços. Uma frase sem espaços funciona bem, ex.: `MeuCafeDaManha@2026`.

**O assistente de IA não funciona.**
Verifique se o arquivo `.env` existe e se a chave da Groq foi colocada no lugar de `sua_chave_aqui`.

---

## 8. Restrições

- Projeto **didático**, feito para a disciplina Fundamentos de Programação. **Não use para guardar senhas reais.**
- Use **somente dados fictícios**.
- Por que não serve para uso real:
  - As senhas das credenciais são **cifradas** no arquivo, mas a chave da cifra é gerada a partir do **e-mail**. Quem tiver o código e o arquivo consegue decifrar tudo sem a senha master. Um cofre real usaria a senha master para gerar a chave. Além disso, a cifra foi feita pelo grupo, para fins didáticos, e não usa um algoritmo testado e reconhecido.
  - **Não há limite de tentativas de login**, então alguém pode ficar testando senhas master sem ser bloqueado.
  - A senha master é guardada com SHA-256 **sem "sal"**, um hash rápido que permite testar milhões de senhas por segundo. Sistemas reais usam bcrypt ou Argon2.
  - Os dados ficam em **arquivos de texto no computador**, que qualquer pessoa com acesso à máquina pode copiar.
  - O log de auditoria pode ser apagado ou alterado por quem tiver acesso ao computador.
  - O assistente de IA envia as perguntas para um serviço externo (Groq). Para reduzir o risco, as senhas nunca são enviadas: só metadados, e senhas digitadas na pergunta viram `[oculto]`.

### Por que as credenciais ficam em JSON?

O enunciado sugere `.csv` ou `.txt`, mas o grupo escolheu **JSON** porque cada credencial tem vários campos (serviço, usuário, senha cifrada, categoria, observações e data). Em JSON, a lista de credenciais é salva e carregada do mesmo jeito que ela fica no programa. Em CSV, uma vírgula digitada nas observações quebraria a separação das colunas. O log de auditoria pode ser exportado em `.csv` pela opção 13.