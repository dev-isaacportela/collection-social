# Visão do Produto

## Problema

Colecionadores de cards, moedas, selos, miniaturas, action figures, discos e tantos outros objetos organizam seus acervos em planilhas, cadernos ou aplicativos genéricos, e mostram suas peças em grupos de redes sociais que não foram feitos para isso. As fotos se perdem no feed, não há estrutura para descrever uma peça, é difícil encontrar quem coleciona a mesma coisa e as trocas acontecem de forma informal, sem histórico nem reputação.

## Proposta

Um lugar onde o colecionador

1. cataloga seu acervo de forma estruturada (coleções, itens, fotos, estado de conservação);
2. mostra o que tem, com controle total do que é público;
3. se conecta a outros colecionadores do mesmo nicho (seguir, curtir, comentar);
4. descobre coleções e pessoas por categoria e interesse;
5. negocia trocas a partir de listas de itens procurados e itens disponíveis, com histórico e reputação.

## Personas

* Catalogadora. Tem acervo grande e quer organizar esse acervo. Usa pouco a parte social. Valoriza cadastro rápido, busca no próprio acervo, privacidade e exportação.
* Exibidor. Tem peças de destaque e quer mostrar essas peças. Valoriza fotos bonitas, perfil público, curtidas e comentários.
* Caçador. Está completando uma coleção e procura peças específicas. Valoriza lista de desejos, descobrir quem tem o que procura e trocas seguras.
* Iniciante. Está começando e quer aprender. Valoriza descobrir coleções, seguir pessoas e um feed relevante.
* Moderador. Integrante da equipe da plataforma que analisa denúncias e mantém a comunidade saudável.

## Roadmap de features

1. 001 Perfis e Coleções. Conta, perfil, coleções, itens com fotos, visibilidade, exportação e exclusão de dados. Núcleo do produto. Sem dependências.
2. 002 Rede Social e Moderação. Seguir, feed, curtidas, comentários, notificações, bloqueio, denúncias e moderação. Depende da 001.
3. 003 Descoberta. Busca global, filtros, explorar por categoria e sugestões de quem seguir. Depende da 001.
4. 004 Listas e Trocas. Lista de desejos, itens disponíveis para troca, correspondências, propostas, conclusão e avaliação de trocas. Depende da 001, 002 e 003.

O MVP é composto pelas features 001 a 003. A feature 004 fecha a primeira versão completa.

## Fora do escopo

* Vendas com pagamento dentro da plataforma.
* Avaliação de preço de mercado das peças.
* Catálogos oficiais pré cadastrados (por exemplo, a base de todas as moedas do Brasil).
* Aplicativos nativos. A primeira versão é uma aplicação web responsiva instalável (PWA).
