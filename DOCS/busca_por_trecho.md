# Busca de credencial por trecho do nome

Funcionalidade extra do CofreSeguro (issue #7).

## O que faz

Antes, para achar uma credencial era preciso digitar o nome do serviço completo. Se a pessoa digitasse só `mail`, o programa não encontrava `Email Escola`.

Com essa funcionalidade dá para buscar por uma parte do nome. O programa mostra todas as credenciais que têm o trecho digitado no nome do serviço. Não faz diferença digitar com letra maiúscula ou minúscula.

## Como usar

1. Entre na sua conta.
2. No menu do cofre, escolha a opção `14 - Buscar credencial por trecho`.
3. Digite uma parte do nome do serviço.

Exemplo:

```
Escolha uma opção: 14
Trecho do nome do serviço: mail

1) Email Escola
   Usuário: aluna.ficticia
   Senha: Se*************
   Categoria: estudo
   Observações:
   Última alteração: 01/01/2026 10:00

2) Mail Trabalho
   Usuário: pessoa.exemplo
   Senha: Ou*************
   Categoria: trabalho
   Observações:
   Última alteração: 01/01/2026 10:00
```

Se nenhuma credencial tiver o trecho:

```
Trecho do nome do serviço: xyz
Nenhuma credencial encontrada.
```

Se a pessoa apertar Enter sem digitar nada:

```
Trecho do nome do serviço:
O trecho não pode ficar vazio.
```

A senha continua aparecendo escondida, igual na opção de listar. Para ver a senha completa ainda é preciso usar a opção `3 - Revelar senha` e confirmar a senha master.

## Como funciona

Foram criadas duas funções no arquivo `credenciais.py`:

- `buscar_por_trecho(credenciais, trecho)`: percorre a lista de credenciais com um `for` e usa o operador `in` para ver se o trecho está dentro do nome do serviço. Os dois textos passam pelo `.lower()` antes de comparar. Ela devolve uma lista com as credenciais encontradas.
- `buscar_credenciais(credenciais)`: pede o trecho para o usuário, confere se não está vazio, chama a `buscar_por_trecho` e mostra o resultado usando a função `listar_credenciais`, que já existia.

No arquivo `cofre.py` foi adicionada a opção 14 no menu.

A busca não altera nem salva nada, ela só mostra as credenciais.

## Testes feitos

Os testes foram feitos manualmente com dados fictícios:

| O que foi digitado | Resultado |
| --- | --- |
| `mail` | Mostrou `Email Escola` e `Mail Trabalho` |
| `BANCO` | Mostrou `Banco Fictício` |
| `xyz` | Mostrou `Nenhuma credencial encontrada.` |
| Enter sem digitar | Mostrou `O trecho não pode ficar vazio.` |
