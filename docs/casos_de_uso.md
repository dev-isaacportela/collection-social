# Casos de Uso

Descrições derivadas das specs 001 a 004. Cada caso de uso aponta para os requisitos e regras que atende. Este arquivo alimenta o documento ABNT e a matriz de rastreabilidade.

## UC01 Cadastrar conta

* Atores. Visitante.
* Requisitos. RF01, RF02.
* Regras. RN01, RN02, RN03.
* Descrição. O visitante cria uma conta informando email, senha e nome de usuário, e recebe um email de confirmação.
* Precondição. O visitante não está autenticado.
* Fluxo principal.
  1. O visitante acessa a página de cadastro.
  2. O sistema exibe o formulário com email, senha, nome de usuário e aceite dos termos.
  3. O visitante preenche os dados e aceita os termos de uso e a política de privacidade.
  4. O sistema valida os dados conforme RN01 e RN02.
  5. O sistema cria a conta com email não confirmado e registra o consentimento.
  6. O sistema executa o caso de uso UC02 Confirmar email.
* Fluxo alternativo.
  * A1 Email ou nome de usuário já cadastrado. O sistema indica qual campo está em conflito e não cria a conta.
  * A2 Senha fora da regra RN02. O sistema explica a regra e mantém os demais dados preenchidos.
* Condições finais. A conta existe com email pendente de confirmação e nenhum conteúdo do usuário fica público.

## UC02 Confirmar email

* Atores. Visitante, Serviço de Email.
* Requisitos. RF02.
* Regras. RN03.
* Descrição. O sistema envia um link de confirmação e marca o email como confirmado quando o link é acessado.
* Precondição. Existe uma conta com email não confirmado.
* Fluxo principal.
  1. O sistema gera um link de confirmação válido por 24 horas.
  2. O Serviço de Email entrega a mensagem ao endereço cadastrado.
  3. O visitante acessa o link.
  4. O sistema marca o email como confirmado e libera a publicação de conteúdo público.
* Fluxo alternativo.
  * A1 Link expirado. O sistema informa a expiração e oferece o reenvio de um novo link.
* Condições finais. O email da conta está confirmado.

## UC03 Autenticar usuário

* Atores. Visitante.
* Requisitos. RF03.
* Regras. RN04, RN20.
* Descrição. O visitante entra no sistema com email e senha, ou sai de uma sessão ativa.
* Precondição. O visitante possui uma conta.
* Fluxo principal.
  1. O visitante informa email e senha.
  2. O sistema verifica as credenciais e a situação da conta.
  3. O sistema cria a sessão e direciona o usuário para o feed.
* Fluxo alternativo.
  * A1 Credenciais incorretas. O sistema informa erro genérico e contabiliza a tentativa.
  * A2 Quinta tentativa incorreta em 15 minutos. O sistema bloqueia o login da conta por 15 minutos conforme RN04.
  * A3 Conta suspensa. O sistema informa a suspensão e não cria a sessão.
  * A4 Esqueceu a senha. O visitante segue para o caso de uso UC04 Recuperar senha.
* Condições finais. O usuário está autenticado como Colecionador.

## UC04 Recuperar senha

* Atores. Visitante, Serviço de Email.
* Requisitos. RF04.
* Regras. RN02, RN05.
* Descrição. O visitante redefine a senha por meio de um link enviado ao email cadastrado. Estende o caso de uso UC03.
* Precondição. O visitante está na tela de entrada e possui conta.
* Fluxo principal.
  1. O visitante solicita a recuperação e informa o email.
  2. O sistema gera um link de uso único válido por 1 hora.
  3. O Serviço de Email entrega a mensagem.
  4. O visitante acessa o link e informa a nova senha.
  5. O sistema valida a senha conforme RN02, grava a nova senha e invalida o link.
* Fluxo alternativo.
  * A1 Email não cadastrado. O sistema exibe a mesma mensagem de sucesso, sem revelar se a conta existe.
  * A2 Link expirado ou já usado. O sistema informa e oferece nova solicitação.
* Condições finais. A senha foi redefinida e as sessões anteriores foram encerradas.

## UC05 Visualizar conteúdo público

* Atores. Visitante.
* Requisitos. RF11.
* Regras. RN10, RN11.
* Descrição. Qualquer pessoa navega por perfis, coleções públicas e itens, sem precisar de login.
* Precondição. Nenhuma.
* Fluxo principal.
  1. O visitante acessa o endereço de um perfil, coleção ou item.
  2. O sistema verifica se o conteúdo é público e se o dono tem email confirmado.
  3. O sistema exibe o conteúdo sem os campos privados.
* Fluxo alternativo.
  * A1 Coleção privada ou dono sem email confirmado. O sistema responde como não encontrado.
* Condições finais. O conteúdo público foi exibido sem expor dados privados.

## UC06 Buscar e explorar comunidade

* Atores. Visitante.
* Requisitos. RF23, RF24, RF25.
* Regras. RN21, RN22.
* Descrição. O visitante busca itens, coleções e colecionadores públicos, aplica filtros e navega pelos destaques de cada categoria.
* Precondição. Nenhuma.
* Fluxo principal.
  1. O visitante informa um termo de busca ou abre a página explorar.
  2. O sistema retorna resultados separados em itens, coleções e colecionadores, aplicando RN21.
  3. O visitante aplica filtros de categoria, estado, tag, UF ou disponibilidade para troca.
  4. O sistema atualiza os resultados respeitando todos os filtros.
* Fluxo alternativo.
  * A1 Nenhum resultado. O sistema sugere termos parecidos e categorias populares.
  * A2 Página explorar. O sistema exibe os destaques dos últimos 7 dias conforme RN22.
* Condições finais. Os resultados exibidos contêm apenas conteúdo público.

## UC07 Gerenciar perfil

* Atores. Colecionador.
* Requisitos. RF05.
* Regras. Nenhuma específica.
* Descrição. O colecionador edita nome de exibição, foto, bio, cidade, UF e categorias de interesse.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador abre as configurações do perfil.
  2. O sistema exibe os dados atuais.
  3. O colecionador altera os dados e salva.
  4. O sistema valida o limite de 500 caracteres da bio e grava as alterações.
* Fluxo alternativo.
  * A1 Bio acima do limite. O sistema informa o limite e não grava.
* Condições finais. O perfil público reflete as alterações.

## UC08 Gerenciar coleções

* Atores. Colecionador.
* Requisitos. RF06, RF07.
* Regras. RN06, RN07.
* Descrição. O colecionador cria, edita, exclui, reordena e define a visibilidade das suas coleções.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador escolhe criar coleção.
  2. O colecionador informa nome, categoria, descrição e capa.
  3. O sistema cria a coleção como privada conforme RN06.
  4. O colecionador altera a visibilidade para pública, se desejar.
  5. O colecionador arrasta as coleções para definir a ordem de exibição.
* Fluxo alternativo.
  * A1 Excluir coleção. O sistema informa quantos itens serão apagados e pede confirmação conforme RN07.
  * A2 Nome ausente ou acima de 80 caracteres. O sistema informa o erro e não grava.
* Condições finais. As coleções estão gravadas com a visibilidade e a ordem escolhidas.

## UC09 Gerenciar itens

* Atores. Colecionador.
* Requisitos. RF08, RF09, RF10.
* Regras. RN08, RN09, RN10, RN13.
* Descrição. O colecionador cadastra, edita, move e exclui itens com fotos, campos padrão, tags, campos personalizados e dados privados.
* Precondição. O colecionador está autenticado e possui ao menos uma coleção.
* Fluxo principal.
  1. O colecionador escolhe adicionar item em uma coleção.
  2. O colecionador informa o nome, tira ou escolhe de 1 a 10 fotos e preenche os campos opcionais.
  3. O sistema valida quantidade, formato e tamanho das fotos conforme RN08.
  4. O sistema grava o item e envia as fotos para processamento.
  5. O sistema remove os metadados de localização e gera as variantes de tamanho conforme RN09.
  6. O sistema exibe o item na coleção com a primeira foto como capa.
* Fluxo alternativo.
  * A1 Foto inválida. O sistema informa o motivo e não grava o item parcialmente.
  * A2 Mover item. O colecionador escolhe outra coleção sua e o sistema move o item preservando os dados.
  * A3 Dados privados. O colecionador informa valor pago, valor estimado, data de aquisição ou observações, que ficam visíveis apenas para ele conforme RN10.
* Condições finais. O item está cadastrado com as fotos prontas para exibição.

## UC10 Buscar no acervo

* Atores. Colecionador.
* Requisitos. RF12.
* Regras. Nenhuma específica.
* Descrição. O colecionador busca e filtra itens em todas as suas coleções, inclusive as privadas.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador informa um termo de busca.
  2. O sistema procura em nome, descrição, tags e campos personalizados, ignorando acentos.
  3. O colecionador aplica filtros de coleção, categoria, estado ou tag.
  4. O sistema exibe os itens que atendem a todos os critérios.
* Fluxo alternativo.
  * A1 Nenhum item encontrado. O sistema informa e sugere remover filtros.
* Condições finais. A lista exibida contém apenas itens do próprio colecionador.

## UC11 Gerenciar dados pessoais

* Atores. Colecionador.
* Requisitos. RF13, RF14.
* Regras. RN12.
* Descrição. O colecionador exporta todos os seus dados ou exclui definitivamente a conta.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador solicita a exportação dos dados.
  2. O sistema gera os arquivos JSON e CSV em segundo plano.
  3. O sistema avisa que o arquivo está pronto para download.
* Fluxo alternativo.
  * A1 Excluir conta. O colecionador confirma com a senha, o sistema encerra as sessões, oculta o conteúdo e conclui a exclusão definitiva em até 30 dias conforme RN12.
* Condições finais. O colecionador recebeu seus dados ou a conta entrou em exclusão.

## UC12 Seguir colecionador

* Atores. Colecionador.
* Requisitos. RF15, RF26.
* Regras. RN14, RN23.
* Descrição. O colecionador segue ou deixa de seguir outro usuário, inclusive a partir das sugestões do sistema.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador abre o perfil de outro usuário ou a lista de sugestões.
  2. O colecionador escolhe seguir.
  3. O sistema verifica RN14, registra o seguimento e notifica o seguido.
* Fluxo alternativo.
  * A1 Deixar de seguir. O sistema remove o seguimento e as publicações deixam de aparecer no feed.
  * A2 Usuário bloqueado. O sistema não exibe a opção de seguir.
* Condições finais. O seguimento está registrado e o contador de seguidores foi atualizado.

## UC13 Visualizar feed

* Atores. Colecionador.
* Requisitos. RF16.
* Regras. RN15.
* Descrição. O colecionador vê as novidades públicas de quem segue em ordem cronológica.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador abre o feed.
  2. O sistema lista novas coleções e itens públicos dos seguidos, do mais recente para o mais antigo.
  3. Ao chegar ao fim da lista, o sistema carrega mais publicações.
* Fluxo alternativo.
  * A1 O colecionador não segue ninguém. O sistema exibe sugestões de colecionadores.
* Condições finais. O feed foi exibido sem campos privados.

## UC14 Interagir com item

* Atores. Colecionador.
* Requisitos. RF17, RF18.
* Regras. RN16, RN17.
* Descrição. O colecionador curte e comenta itens públicos de outros usuários e gerencia comentários.
* Precondição. O colecionador está autenticado e o item é público.
* Fluxo principal.
  1. O colecionador abre um item público.
  2. O colecionador curte o item.
  3. O sistema registra a curtida uma única vez e notifica o dono.
  4. O colecionador escreve um comentário.
  5. O sistema valida o limite de 1000 caracteres, publica o comentário e notifica o dono.
* Fluxo alternativo.
  * A1 Descurtir. O sistema remove a curtida.
  * A2 Excluir comentário. O autor exclui o próprio comentário ou o dono do item exclui qualquer comentário no seu item.
  * A3 Item próprio. O sistema não exibe a opção de curtir.
* Condições finais. A interação está registrada e o dono foi notificado.

## UC15 Bloquear usuário

* Atores. Colecionador.
* Requisitos. RF20.
* Regras. RN18.
* Descrição. O colecionador bloqueia outro usuário para impedir qualquer interação entre os dois.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador abre o perfil do outro usuário e escolhe bloquear.
  2. O sistema pede confirmação.
  3. O sistema registra o bloqueio e desfaz os seguimentos entre os dois conforme RN18.
* Fluxo alternativo.
  * A1 Desbloquear. O sistema remove o bloqueio, sem restaurar seguimentos.
* Condições finais. Nenhum dos dois consegue seguir, curtir, comentar ou propor troca ao outro.

## UC16 Denunciar conteúdo

* Atores. Colecionador.
* Requisitos. RF21.
* Regras. RN19.
* Descrição. O colecionador denuncia um item, comentário ou perfil impróprio.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador escolhe denunciar o conteúdo.
  2. O sistema exibe a lista de motivos.
  3. O colecionador escolhe o motivo e confirma.
  4. O sistema registra a denúncia e confirma o recebimento.
* Fluxo alternativo.
  * A1 Terceira denúncia de usuários distintos. O sistema oculta o conteúdo até a decisão do moderador conforme RN19.
  * A2 Denúncia repetida do mesmo usuário. O sistema informa que a denúncia já foi registrada.
* Condições finais. A denúncia está na fila de moderação.

## UC17 Moderar denúncias

* Atores. Moderador.
* Requisitos. RF22.
* Regras. RN19, RN20.
* Descrição. O moderador analisa as denúncias pendentes e decide arquivar, remover o conteúdo ou suspender o autor.
* Precondição. O usuário está autenticado com papel de moderador.
* Fluxo principal.
  1. O moderador abre a fila de moderação.
  2. O sistema lista as denúncias pendentes, das mais antigas para as mais recentes.
  3. O moderador analisa o conteúdo e os motivos.
  4. O moderador registra a decisão e a justificativa.
  5. O sistema aplica a decisão e notifica o autor do conteúdo conforme RN20.
* Fluxo alternativo.
  * A1 Arquivar. O sistema volta a exibir o conteúdo, se estava oculto.
  * A2 Suspender autor. O sistema encerra as sessões do autor e impede novas entradas durante a suspensão.
* Condições finais. A denúncia está decidida e registrada com moderador, data e justificativa.

## UC18 Gerenciar lista de desejos

* Atores. Colecionador.
* Requisitos. RF27, RF29.
* Regras. RN31.
* Descrição. O colecionador registra as peças que procura e recebe avisos de correspondência.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador adiciona um desejo com nome, categoria, termos e visibilidade.
  2. O sistema grava o desejo.
  3. Quando um item disponível para troca corresponde ao desejo conforme RN31, o sistema notifica o colecionador.
* Fluxo alternativo.
  * A1 Editar ou excluir desejo. O sistema atualiza a lista.
* Condições finais. A lista de desejos está atualizada e monitorada.

## UC19 Disponibilizar item para troca

* Atores. Colecionador.
* Requisitos. RF28.
* Regras. RN24.
* Descrição. O colecionador marca um item como disponível para troca. Estende o caso de uso UC09.
* Precondição. O colecionador está editando um item próprio.
* Fluxo principal.
  1. O colecionador marca a opção disponível para troca.
  2. O sistema verifica se o item está em coleção pública conforme RN24.
  3. O sistema exibe o selo de disponível e inclui o item nos filtros de troca.
* Fluxo alternativo.
  * A1 Item em coleção privada. O sistema explica a regra e não marca o item.
* Condições finais. O item aparece como disponível para troca.

## UC20 Propor troca

* Atores. Colecionador.
* Requisitos. RF30.
* Regras. RN25.
* Descrição. O colecionador monta e envia uma proposta de troca a outro colecionador.
* Precondição. O colecionador está autenticado, com email confirmado e com pelo menos um item disponível para troca.
* Fluxo principal.
  1. O colecionador abre um item disponível de outro usuário e escolhe propor troca.
  2. O colecionador seleciona itens do destinatário e itens próprios disponíveis.
  3. O colecionador escreve uma mensagem opcional e envia.
  4. O sistema valida a proposta conforme RN25.
  5. O sistema registra a proposta como pendente e notifica o destinatário.
* Fluxo alternativo.
  * A1 Proposta inválida. O sistema informa o motivo e não envia.
  * A2 Cancelar antes da resposta. O sistema muda a proposta para cancelada.
* Condições finais. A proposta está pendente aguardando resposta.

## UC21 Negociar proposta

* Atores. Colecionador.
* Requisitos. RF31, RF32.
* Regras. RN26, RN27.
* Descrição. A parte que recebeu a proposta aceita, recusa ou faz contraproposta, e as partes trocam mensagens.
* Precondição. Existe uma proposta pendente para o colecionador.
* Fluxo principal.
  1. O colecionador abre a proposta recebida.
  2. O sistema exibe os itens, as mensagens e o histórico.
  3. O colecionador aceita a proposta.
  4. O sistema muda a proposta para aceita, reserva os itens conforme RN26 e notifica a outra parte.
* Fluxo alternativo.
  * A1 Recusar. O sistema encerra a proposta como recusada e notifica a outra parte.
  * A2 Contrapropor. O colecionador altera os itens e o sistema devolve a proposta como pendente para a outra parte.
  * A3 Enviar mensagem. O sistema registra a mensagem no histórico da proposta.
  * A4 Sem resposta por 7 dias. O sistema expira a proposta conforme RN27.
* Condições finais. A proposta foi aceita, recusada, contraproposta ou expirada, com histórico registrado.

## UC22 Concluir troca

* Atores. Colecionador.
* Requisitos. RF33.
* Regras. RN28, RN29.
* Descrição. Cada parte confirma o recebimento dos itens e o sistema conclui a troca quando as duas confirmam.
* Precondição. Existe uma troca aceita entre as partes.
* Fluxo principal.
  1. O colecionador informa que recebeu os itens.
  2. O sistema registra a confirmação e aguarda a outra parte.
  3. A outra parte confirma o recebimento.
  4. O sistema conclui a troca e retira os itens trocados da lista de disponíveis conforme RN28.
* Fluxo alternativo.
  * A1 Cancelar troca aceita. A parte informa o motivo, o sistema cancela, libera os itens e notifica a outra parte conforme RN29.
* Condições finais. A troca está concluída e as avaliações estão liberadas.

## UC23 Avaliar troca

* Atores. Colecionador.
* Requisitos. RF34.
* Regras. RN30.
* Descrição. Após a conclusão, cada parte avalia a outra com nota e comentário. Estende o caso de uso UC22.
* Precondição. A troca está concluída e o colecionador ainda não avaliou a outra parte.
* Fluxo principal.
  1. O colecionador escolhe avaliar a troca.
  2. O colecionador informa nota de 1 a 5 e comentário opcional.
  3. O sistema grava a avaliação e recalcula a reputação da outra parte.
* Fluxo alternativo.
  * A1 Avaliação já registrada. O sistema exibe a avaliação existente sem permitir nova.
* Condições finais. A reputação da outra parte está atualizada no perfil.

## UC24 Consultar notificações

* Atores. Colecionador, Serviço de Email.
* Requisitos. RF19.
* Regras. Nenhuma específica.
* Descrição. O colecionador consulta os avisos de seguidores, curtidas, comentários, trocas e moderação, e define quais também chegam por email.
* Precondição. O colecionador está autenticado.
* Fluxo principal.
  1. O colecionador abre a central de notificações.
  2. O sistema lista as notificações da mais recente para a mais antiga.
  3. O sistema marca as notificações exibidas como lidas.
* Fluxo alternativo.
  * A1 Preferências. O colecionador desativa um tipo de notificação por email e o Serviço de Email deixa de enviar esse tipo.
* Condições finais. As notificações foram lidas e as preferências estão gravadas.
