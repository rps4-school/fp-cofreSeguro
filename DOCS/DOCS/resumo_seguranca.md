## O que o resumo mostra
A função `mostrar_resumo` (arquivo `resumo_seguranca.py`) apresenta:
- quantas credenciais o usuário tem;
- quantas senhas são fracas;
- quantas senhas estão repetidas;
- quantas senhas aparecem na lista de senhas comuns;
- há quantos dias cada credencial não é alterada.
O resumo nunca mostra a senha, só o nome do serviço.

## Definições
- **Senha fraca:** senha que a função `avaliar_senha` (`senhas.py`) classifica como nível 1.
  A nota soma 1 ponto para cada critério: pelo menos 8 caracteres, pelo menos 12 caracteres,
  letras maiúsculas e minúsculas, números e símbolos. Até 2 pontos é fraca.
  Senha que está na lista de comuns também é sempre fraca.
- **Senha comum:** senha (em minúsculas) que consta no arquivo `senhas_comuns.txt`.
- **Senha repetida:** senha igual em mais de uma credencial. Todas as credenciais que
  usam essa senha entram na contagem (3 credenciais com a mesma senha = 3 repetidas).
- **Tempo sem alterar:** dias entre a data guardada no campo `alterada_em`
  (formato dd/mm/aaaa hh:mm) e o momento atual. Sem data, aparece "data desconhecida".
- Uma mesma senha pode contar em mais de uma categoria (por exemplo, comum e fraca).
