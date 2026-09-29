# Spec 002 Rede Social e Moderação

Status Aprovada. Criada em 29/09/2026. Depende da Spec 001.

Esta spec descreve o quê e por quê. Nenhuma decisão de tecnologia aparece aqui.

## 1. Contexto

Com o acervo catalogado (Spec 001), o colecionador precisa de reconhecimento e conexão. Seguir pessoas, ver o que elas publicam e interagir com as peças é o que transforma um catálogo em rede social. Junto com a interação vem a necessidade de proteger a comunidade com bloqueios, denúncias e moderação.

## 2. Histórias de usuário

### US1 Seguir colecionadores (P1)

Como iniciante, quero seguir colecionadores que admiro para acompanhar o que eles publicam.

Critérios de aceitação

1. Dado o perfil de outro usuário, quando clico em seguir, então passo a seguir esse usuário e o contador de seguidores dele aumenta.
2. Dado um usuário que sigo, quando clico em deixar de seguir, então deixo de ver suas publicações no feed.
3. Dado meu perfil, quando abro seguidores ou seguindo, então vejo as respectivas listas.

### US2 Acompanhar o feed (P1)

Como usuário, quero um feed com as novidades de quem sigo.

Critérios de aceitação

1. Dado que sigo colecionadores, quando abro o feed, então vejo novas coleções públicas e novos itens em coleções públicas deles, do mais recente para o mais antigo.
2. Dado um feed longo, quando chego ao fim da página, então mais publicações são carregadas.
3. Dado que não sigo ninguém, quando abro o feed, então vejo sugestões de colecionadores para seguir.

### US3 Curtir e comentar itens (P1)

Como exibidor, quero receber curtidas e comentários nas minhas peças.

Critérios de aceitação

1. Dado um item público de outro usuário, quando curto, então a curtida é registrada uma única vez e posso desfazer a curtida depois.
2. Dado um item público, quando comento, então o comentário aparece abaixo do item com meu nome e a data.
3. Dado um comentário meu, quando o excluo, então ele deixa de aparecer.
4. Dado um item meu, quando excluo o comentário de outra pessoa, então ele deixa de aparecer.

### US4 Receber notificações (P2)

Como usuário, quero ser avisado quando alguém interage comigo.

Critérios de aceitação

1. Dado um novo seguidor, curtida, comentário ou evento de troca, quando ocorre, então recebo uma notificação dentro do sistema.
2. Dado notificações não lidas, quando abro a central de notificações, então elas são marcadas como lidas.
3. Dado minhas preferências, quando desativo um tipo de notificação por email, então deixo de receber esse tipo por email.

### US5 Bloquear e denunciar (P1)

Como usuário, quero bloquear pessoas e denunciar conteúdo impróprio.

Critérios de aceitação

1. Dado outro usuário, quando o bloqueio, então nenhum de nós consegue seguir, curtir, comentar ou propor troca ao outro, e seguimentos existentes entre nós são desfeitos.
2. Dado um item, comentário ou perfil, quando o denuncio escolhendo um motivo, então a denúncia é registrada e recebo confirmação.

### US6 Moderar denúncias (P1)

Como moderador, quero analisar denúncias para manter a comunidade saudável.

Critérios de aceitação

1. Dado denúncias pendentes, quando abro a fila de moderação, então vejo as mais antigas primeiro, com o conteúdo denunciado e os motivos.
2. Dado uma denúncia, quando decido, então posso arquivar a denúncia, remover o conteúdo ou suspender o autor, registrando a justificativa.
3. Dado uma decisão de remoção ou suspensão, quando ela é aplicada, então o autor é notificado com o motivo.

## 3. Requisitos funcionais

* RF15 Seguir colecionador. O sistema deve permitir seguir e deixar de seguir outros usuários e listar seguidores e seguidos.
* RF16 Visualizar feed. O sistema deve exibir um feed com as publicações públicas dos usuários seguidos.
* RF17 Curtir item. O sistema deve permitir curtir e descurtir itens públicos de outros usuários.
* RF18 Comentar item. O sistema deve permitir comentar itens públicos e excluir comentários.
* RF19 Notificar usuário. O sistema deve notificar novos seguidores, curtidas, comentários, eventos de troca e decisões de moderação, dentro do sistema e por email.
* RF20 Bloquear usuário. O sistema deve permitir bloquear e desbloquear outros usuários.
* RF21 Denunciar conteúdo. O sistema deve permitir denunciar itens, comentários e perfis, informando um motivo.
* RF22 Moderar denúncias. O sistema deve permitir que moderadores analisem denúncias e apliquem arquivamento, remoção de conteúdo ou suspensão de conta.

## 4. Requisitos não funcionais

* RNF10 Desempenho do feed. Uma página do feed com 20 publicações deve carregar em até 1,5 segundo no percentil 95.
* RNF11 Entrega de notificações. Notificações dentro do sistema devem aparecer em até 1 minuto após o evento.

## 5. Regras de negócio

* RN14 (RF15) Um usuário não pode seguir a si mesmo nem seguir quem o bloqueou.
* RN15 (RF16) O feed mostra somente conteúdo público de usuários seguidos, em ordem cronológica decrescente, e nunca mostra campos privados.
* RN16 (RF17) Cada usuário curte um mesmo item no máximo uma vez e não pode curtir itens próprios.
* RN17 (RF18) O comentário tem até 1000 caracteres. O autor pode excluir o próprio comentário e o dono do item pode excluir qualquer comentário no seu item.
* RN18 (RF20) O bloqueio desfaz os seguimentos entre os dois usuários e impede seguir, curtir, comentar e propor troca nos dois sentidos. O bloqueado não é avisado.
* RN19 (RF21, RF22) Conteúdo com denúncias de 3 usuários distintos fica oculto automaticamente até a decisão do moderador.
* RN20 (RF22) Toda decisão de moderação registra moderador, data e justificativa. Usuário suspenso não consegue entrar no sistema durante a suspensão.

## 6. Entidades principais

* Seguimento. Liga um seguidor a um seguido.
* Curtida. Liga um Usuário a um Item.
* Comentário. Texto de um Usuário sobre um Item.
* Notificação. Aviso para um Usuário sobre um evento, com situação lida ou não lida.
* Bloqueio. Liga quem bloqueou a quem foi bloqueado.
* Denúncia. Registro de um Usuário sobre um conteúdo, com motivo, situação e decisão.
* Moderador. Usuário da equipe com permissão para decidir denúncias.

## 7. Fora do escopo desta feature

* Mensagens diretas entre usuários fora de uma negociação de troca.
* Feed ordenado por relevância. O MVP usa ordem cronológica.
* Perfis privados com aprovação de seguidores.

## 8. Métricas de sucesso

* Pelo menos 40% dos usuários ativos seguem 5 pessoas ou mais no primeiro mês.
* Tempo médio entre denúncia e decisão menor que 24 horas.

## 9. Clarificações

Sessão de 29/09/2026.

* C1 O feed é cronológico ou por relevância? Decisão. Cronológico no MVP (RN15).
* C2 Quantas denúncias ocultam um conteúdo? Decisão. Denúncias de 3 usuários distintos (RN19).
* C3 O bloqueado é avisado? Decisão. Não (RN18).
