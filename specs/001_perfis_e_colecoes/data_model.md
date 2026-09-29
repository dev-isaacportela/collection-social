# Modelo de Dados da Spec 001

Identificadores são UUID v7. Toda entidade tem criadoEm e atualizadoEm. Nomes em português, como no código.

## Usuario

* id
* email, texto único
* nomeUsuario, texto único (RN01)
* hashSenha, texto
* emailConfirmadoEm, data e hora, vazio enquanto não confirmado (RN03)
* situacao, enumeração SituacaoConta com Ativa, Suspensa e EmExclusao
* exclusaoSolicitadaEm, data e hora opcional (RN12)
* consentimentoTermosEm, data e hora (RNF06)
* papel, enumeração Papel com Colecionador e Moderador

## Perfil

* usuarioId, chave para Usuario, um para um
* nomeExibicao, texto até 60 caracteres
* bio, texto até 500 caracteres
* fotoChave, texto opcional
* cidade, texto opcional
* uf, texto de 2 letras opcional
* categoriasInteresse, relação muitos para muitos com Categoria

## Categoria

* id
* nome, texto único
* slug, texto único
* ordem, inteiro

## Colecao

* id
* donoId, chave para Usuario
* categoriaId, chave para Categoria
* nome, texto até 80 caracteres (RN06)
* slug, texto único por dono
* descricao, texto opcional
* capaChave, texto opcional
* visibilidade, enumeração Visibilidade com Publica e Privada, padrão Privada (RN06)
* posicao, inteiro (RF07)

## Item

* id
* colecaoId, chave para Colecao
* nome, texto até 120 caracteres
* descricao, texto opcional
* ano, inteiro opcional
* fabricante, texto opcional
* estadoConservacao, enumeração EstadoConservacao opcional (RN13)
* grau, texto opcional (RN13)
* quantidade, inteiro, padrão 1
* camposPersonalizados, JSON com pares de chave e valor
* disponivelParaTroca, booleano, padrão falso (usado na Spec 004)
* vetorBusca, coluna gerada para busca textual (RF12)

## DadosPrivadosItem

Tabela separada para que consultas públicas nunca alcancem estes campos (RN10).

* itemId, chave para Item, um para um
* valorPago, decimal opcional
* valorEstimado, decimal opcional
* dataAquisicao, data opcional
* observacoes, texto opcional

## Foto

* id
* itemId, chave para Item
* chaveOriginal, texto
* chavesVariantes, JSON com as chaves das variantes de 320, 960 e 1920 pixels
* posicao, inteiro de 1 a 10, sendo 1 a capa (RN08)
* situacao, enumeração SituacaoFoto com EmProcessamento, Pronta e Rejeitada

## Tag e ItemTag

* Tag tem id, donoId e nome, único por dono.
* ItemTag liga Item e Tag, muitos para muitos.

## Enumerações

* Visibilidade. Publica, Privada.
* EstadoConservacao. NovoLacrado, Excelente, MuitoBom, Bom, Regular, Ruim.
* SituacaoConta. Ativa, Suspensa, EmExclusao.
* SituacaoFoto. EmProcessamento, Pronta, Rejeitada.
* Papel. Colecionador, Moderador.

## Índices

* Usuario por email e por nomeUsuario, únicos.
* Colecao por donoId e posicao.
* Item por colecaoId e índice GIN em vetorBusca.
* Índice trigram em Item.nome para tolerância a erros de digitação.
