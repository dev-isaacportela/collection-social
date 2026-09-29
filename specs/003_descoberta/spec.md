# Spec 003 Descoberta

Status Aprovada. Criada em 29/09/2026. Depende da Spec 001.

Esta spec descreve o quê e por quê. Nenhuma decisão de tecnologia aparece aqui.

## 1. Contexto

Uma rede de colecionadores só tem valor se as pessoas se encontram. Quem coleciona moedas do Império precisa achar outros colecionadores do mesmo tema, e o iniciante precisa de um ponto de partida. Esta feature cria a busca global e as vitrines de descoberta.

## 2. Histórias de usuário

### US1 Buscar na comunidade (P1)

Como caçador, quero buscar itens, coleções e colecionadores para encontrar quem tem as peças que procuro.

Critérios de aceitação

1. Dado um termo, quando busco, então vejo resultados separados em itens, coleções e colecionadores, apenas com conteúdo público.
2. Dado um termo sem acentos ou com um erro simples de digitação, quando busco, então ainda encontro os resultados esperados.
3. Dado resultados, quando filtro por categoria, estado de conservação, tag, UF ou disponibilidade para troca, então a lista respeita todos os filtros combinados.

### US2 Explorar por categoria (P2)

Como iniciante, quero explorar as coleções em destaque de cada categoria.

Critérios de aceitação

1. Dado a página explorar, quando escolho uma categoria, então vejo as coleções e itens com mais curtidas nos últimos 7 dias.
2. Dado a página explorar sem categoria escolhida, quando a abro, então vejo destaques das minhas categorias de interesse ou, se não tiver nenhuma, de todas.

### US3 Receber sugestões de quem seguir (P2)

Como iniciante, quero sugestões de colecionadores para seguir.

Critérios de aceitação

1. Dado minhas categorias de interesse, quando abro as sugestões, então vejo colecionadores ativos com coleções públicas nessas categorias que ainda não sigo.

## 3. Requisitos funcionais

* RF23 Buscar na comunidade. O sistema deve permitir buscar itens, coleções e colecionadores públicos por texto.
* RF24 Filtrar resultados. O sistema deve permitir filtrar resultados por categoria, estado de conservação, tag, UF e disponibilidade para troca.
* RF25 Explorar destaques. O sistema deve exibir coleções e itens em destaque por categoria.
* RF26 Sugerir colecionadores. O sistema deve sugerir colecionadores para seguir com base nas categorias de interesse.

## 4. Requisitos não funcionais

* RNF12 Desempenho e tolerância da busca. A busca deve responder em até 1 segundo no percentil 95, ignorando acentos e maiúsculas e tolerando erros simples de digitação.

## 5. Regras de negócio

* RN21 (RF23, RF24) A busca retorna somente conteúdo público de contas com email confirmado, não suspensas, e nunca retorna conteúdo de quem bloqueou o usuário ou foi bloqueado por ele.
* RN22 (RF25) O destaque considera as curtidas recebidas nos últimos 7 dias e exclui conteúdo oculto por denúncia.
* RN23 (RF26) Sugestões excluem quem o usuário já segue, quem ele bloqueou e contas sem atividade nos últimos 90 dias.

## 6. Entidades principais

Esta feature não cria entidades novas. Ela lê Usuário, Perfil, Coleção, Item, Categoria, Tag, Curtida, Seguimento e Bloqueio.

## 7. Fora do escopo desta feature

* Busca por imagem (foto de uma peça para achar peças parecidas).
* Recomendação baseada em aprendizado de máquina.

## 8. Métricas de sucesso

* Pelo menos 30% das novas contas seguem alguém a partir de uma sugestão ou da busca na primeira sessão.

## 9. Clarificações

Sessão de 29/09/2026.

* C1 Qual janela de tempo define os destaques? Decisão. Últimos 7 dias (RN22).
