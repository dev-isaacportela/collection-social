# Spec 004 Listas e Trocas

Status Aprovada. Criada em 29/09/2026. Depende das Specs 001, 002 e 003.

Esta spec descreve o quê e por quê. Nenhuma decisão de tecnologia aparece aqui.

## 1. Contexto

Trocar peças repetidas é uma das práticas mais antigas entre colecionadores, e hoje acontece em conversas soltas, sem registro nem confiança. Esta feature permite dizer o que se procura e o que se tem para trocar, encontra correspondências e conduz a negociação até a conclusão, com histórico e reputação.

## 2. Histórias de usuário

### US1 Manter lista de desejos (P1)

Como caçador, quero registrar as peças que procuro.

Critérios de aceitação

1. Dado um usuário logado, quando adiciona um desejo com nome, categoria e observação, então ele aparece na sua lista de desejos.
2. Dado um desejo, quando o usuário o marca como público ou privado, então apenas desejos públicos aparecem no seu perfil.

### US2 Disponibilizar itens para troca (P1)

Como colecionador, quero marcar itens repetidos como disponíveis para troca.

Critérios de aceitação

1. Dado um item em coleção pública, quando o marco como disponível para troca, então ele recebe um selo de disponível e aparece nos filtros de troca.
2. Dado um item em coleção privada, quando tento marcar como disponível, então o sistema explica que ele precisa estar em coleção pública.

### US3 Ser avisado de correspondências (P2)

Como caçador, quero ser avisado quando alguém disponibilizar algo que procuro.

Critérios de aceitação

1. Dado um desejo público ou privado, quando outro usuário disponibiliza para troca um item da mesma categoria cujo nome contém os termos do desejo, então recebo uma notificação de correspondência.

### US4 Propor troca (P1)

Como caçador, quero propor uma troca oferecendo itens meus em troca de itens de outro colecionador.

Critérios de aceitação

1. Dado itens disponíveis de outro usuário, quando monto uma proposta com pelo menos um item dele e pelo menos um item meu disponível, com mensagem opcional, então a proposta é enviada e ele é notificado.
2. Dado uma proposta enviada, quando ainda não foi respondida, então posso cancelar.

### US5 Negociar a proposta (P1)

Como destinatário, quero aceitar, recusar ou fazer uma contraproposta.

Critérios de aceitação

1. Dado uma proposta pendente, quando aceito, então ela fica aceita e os itens envolvidos ficam reservados.
2. Dado uma proposta pendente, quando recuso, então ela é encerrada e o proponente é notificado.
3. Dado uma proposta pendente, quando faço uma contraproposta alterando os itens, então ela volta a ficar pendente aguardando resposta da outra parte.
4. Dado uma proposta pendente sem resposta por 7 dias, quando o prazo termina, então ela expira e as duas partes são notificadas.
5. Dado uma proposta em negociação, quando envio uma mensagem, então ela fica registrada no histórico da proposta.

### US6 Concluir e avaliar a troca (P1)

Como participante, quero confirmar o recebimento e avaliar a outra parte.

Critérios de aceitação

1. Dado uma troca aceita, quando eu confirmo o recebimento, então ela aguarda a confirmação da outra parte.
2. Dado que as duas partes confirmaram o recebimento, quando a segunda confirmação ocorre, então a troca é concluída e os itens trocados saem da lista de disponíveis.
3. Dado uma troca concluída, quando avalio a outra parte com nota de 1 a 5 e comentário opcional, então a nota entra na reputação dela.
4. Dado uma troca aceita e ainda não concluída, quando uma das partes cancela informando o motivo, então a troca é cancelada e os itens voltam a ficar disponíveis.

## 3. Requisitos funcionais

* RF27 Gerenciar lista de desejos. O sistema deve permitir criar, editar, excluir e definir a visibilidade de desejos.
* RF28 Disponibilizar item para troca. O sistema deve permitir marcar e desmarcar itens como disponíveis para troca.
* RF29 Notificar correspondência. O sistema deve avisar o usuário quando um item disponível corresponder a um desejo seu.
* RF30 Propor troca. O sistema deve permitir montar e enviar propostas de troca e cancelar propostas ainda não respondidas.
* RF31 Responder proposta. O sistema deve permitir aceitar, recusar ou contrapropor uma proposta pendente.
* RF32 Trocar mensagens na proposta. O sistema deve permitir mensagens entre as partes dentro da proposta.
* RF33 Concluir troca. O sistema deve registrar a confirmação de recebimento de cada parte e concluir ou cancelar a troca.
* RF34 Avaliar troca. O sistema deve permitir que cada parte avalie a outra após a conclusão e exibir a reputação no perfil.

## 4. Requisitos não funcionais

* RNF13 Rastreabilidade. Toda mudança de situação de uma proposta deve ficar registrada em histórico imutável, com data e autor.

## 5. Regras de negócio

* RN24 (RF28) Somente itens em coleção pública podem ser marcados como disponíveis para troca.
* RN25 (RF30) A proposta tem pelo menos um item de cada parte, todos disponíveis para troca, e as duas partes precisam ter email confirmado e não ter bloqueio entre si.
* RN26 (RF31) Itens de uma proposta aceita ficam reservados e não podem entrar em outra proposta até a troca ser concluída ou cancelada.
* RN27 (RF31) A proposta pendente sem resposta por 7 dias expira automaticamente.
* RN28 (RF33) A troca só é concluída quando as duas partes confirmam o recebimento. Os itens trocados deixam de estar disponíveis para troca.
* RN29 (RF33) Cancelar uma troca aceita exige motivo, libera os itens reservados e notifica a outra parte.
* RN30 (RF34) Cada parte avalia a outra uma única vez, com nota de 1 a 5, somente após a conclusão. A reputação é a média das notas recebidas.
* RN31 (RF29) A correspondência considera a mesma categoria e a presença de todos os termos do desejo no nome ou nas tags do item.

## 6. Entidades principais

* Desejo. Peça procurada por um Usuário, com categoria, termos e visibilidade.
* Proposta de Troca. Negociação entre proponente e destinatário, com situação e histórico.
* Item da Proposta. Liga um Item a uma Proposta, indicando de qual parte ele é.
* Mensagem da Proposta. Texto trocado entre as partes dentro da Proposta.
* Avaliação. Nota e comentário de uma parte sobre a outra após a troca.

## 7. Fora do escopo desta feature

* Pagamento, frete ou intermediação da entrega.
* Trocas com mais de duas partes.
* Transferência automática do item para o acervo de quem recebeu.

## 8. Métricas de sucesso

* Pelo menos 50% das propostas aceitas chegam à conclusão.
* Reputação média das trocas concluídas igual ou maior que 4.

## 9. Clarificações

Sessão de 29/09/2026.

* C1 Qual o prazo de expiração de propostas? Decisão. 7 dias (RN27).
* C2 O item trocado muda automaticamente de dono? Decisão. Não no MVP. Ele apenas deixa de estar disponível e o dono decide se o exclui ou arquiva.
