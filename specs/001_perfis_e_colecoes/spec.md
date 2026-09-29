# Spec 001 Perfis e Coleções

Status Aprovada. Criada em 29/09/2026.

Esta spec descreve o quê e por quê. Nenhuma decisão de tecnologia aparece aqui, isso é papel do [plan.md](./plan.md).

## 1. Contexto

É o núcleo do produto. Sem conta, perfil, coleções e itens não existe rede social de colecionadores. Todas as features seguintes (feed, busca, trocas) operam sobre as entidades definidas aqui.

## 2. Histórias de usuário

### US1 Criar conta e entrar (P1)

Como visitante, quero criar uma conta e entrar nela para poder cadastrar minhas coleções.

Critérios de aceitação

1. Dado um visitante, quando informa email, senha e nome de usuário válidos e únicos e aceita os termos, então a conta é criada e ele recebe um email de confirmação.
2. Dado um email ou nome de usuário já usado, quando tenta se cadastrar, então recebe mensagem indicando qual campo está em conflito, sem criar conta.
3. Dado uma conta, quando informa credenciais corretas, então entra no sistema.
4. Dado 5 tentativas de login incorretas em 15 minutos para a mesma conta, quando tenta de novo, então o login fica bloqueado por 15 minutos e ele é informado disso.
5. Dado um usuário que esqueceu a senha, quando solicita recuperação, então recebe um link de uso único válido por 1 hora.

### US2 Montar meu perfil (P1)

Como colecionador, quero um perfil com foto, bio e meus interesses para que outros saibam o que coleciono.

Critérios de aceitação

1. Dado um usuário logado, quando edita o perfil, então pode definir nome de exibição, foto, bio de até 500 caracteres, cidade e UF (opcionais) e categorias de interesse.
2. Dado um perfil, quando qualquer pessoa acessa o endereço do perfil pelo nome de usuário, então vê o perfil e somente as coleções públicas.

### US3 Criar e organizar coleções (P1)

Como colecionador, quero agrupar minhas peças em coleções, como Moedas do Império ou Miniaturas dos anos 80.

Critérios de aceitação

1. Dado um usuário logado, quando cria uma coleção com nome, categoria, descrição e foto de capa, então ela aparece no seu perfil.
2. Dado uma coleção, quando o dono define a visibilidade, então ela pode ser pública (qualquer pessoa vê) ou privada (só o dono vê). O padrão é privada.
3. Dado uma coleção, quando o dono a exclui, então o sistema pede confirmação e informa quantos itens serão apagados junto.
4. Dado várias coleções, quando o dono as reordena, então a nova ordem é mantida no perfil.

### US4 Cadastrar itens com fotos (P1)

Como colecionador, quero cadastrar cada peça com fotos e detalhes para ter meu acervo catalogado.

Critérios de aceitação

1. Dado uma coleção, quando o dono adiciona um item com nome e de 1 a 10 fotos, então o item aparece na coleção, com a primeira foto como capa.
2. Dado um item, quando o dono preenche campos opcionais, então pode informar descrição, ano, fabricante ou emissor, estado de conservação, grau, quantidade, tags e campos personalizados no formato chave e valor.
3. Dado um item, quando o dono informa valor pago, valor estimado, data de aquisição ou observações privadas, então esses dados nunca aparecem para outros usuários, qualquer que seja a visibilidade da coleção.
4. Dado uma foto enviada, quando ela é processada, então os metadados de localização são removidos antes de ela ficar visível.
5. Dado um item, quando o dono o move para outra coleção sua, então o item muda de coleção preservando todos os dados.
6. Dado uma foto acima de 15 MB ou em formato não suportado, quando o envio é feito, então o usuário recebe mensagem clara e o item não é salvo parcialmente.

### US5 Ver coleções de outros colecionadores (P2)

Como visitante ou usuário, quero navegar pelas coleções públicas de alguém para conhecer seu acervo.

Critérios de aceitação

1. Dado uma coleção pública, quando acesso seu link, então vejo capa, descrição, número de itens e a grade de itens com foto.
2. Dado um item de coleção pública, quando o abro, então vejo as fotos em tamanho grande e os campos não privados.
3. Dado uma coleção privada, quando um terceiro acessa o link, então recebe a resposta não encontrado, sem revelar que a coleção existe.

### US6 Buscar no meu próprio acervo (P2)

Como catalogadora, quero buscar e filtrar meus itens para achar rapidamente uma peça.

Critérios de aceitação

1. Dado meu acervo, quando busco por texto, então encontro itens pelo nome, descrição, tags ou campos personalizados, em todas as minhas coleções.
2. Dado meu acervo, quando filtro por coleção, categoria, estado de conservação ou tag, então a lista respeita todos os filtros combinados.

### US7 Exportar e apagar meus dados (P2)

Como usuário, quero exportar meu acervo e poder apagar minha conta.

Critérios de aceitação

1. Dado um usuário logado, quando solicita exportação, então recebe um arquivo com todas as suas coleções e itens, incluindo campos privados, em JSON e CSV, com links das fotos.
2. Dado um usuário que solicita a exclusão da conta, quando confirma com a senha, então perfil, coleções, itens e fotos são removidos definitivamente em até 30 dias.

## 3. Requisitos funcionais

* RF01 Cadastrar conta. O sistema deve permitir que o visitante crie uma conta com email, senha e nome de usuário, aceitando os termos de uso e a política de privacidade.
* RF02 Confirmar email. O sistema deve enviar um link de confirmação e marcar a conta como confirmada quando o link for acessado.
* RF03 Autenticar usuário. O sistema deve permitir entrar e sair da conta com email e senha.
* RF04 Recuperar senha. O sistema deve permitir redefinir a senha por meio de link enviado ao email cadastrado.
* RF05 Gerenciar perfil. O sistema deve permitir editar nome de exibição, foto, bio, cidade, UF e categorias de interesse.
* RF06 Gerenciar coleções. O sistema deve permitir criar, editar, excluir e definir a visibilidade de coleções.
* RF07 Ordenar coleções. O sistema deve permitir que o dono defina a ordem de exibição das coleções no perfil.
* RF08 Gerenciar itens. O sistema deve permitir criar, editar e excluir itens com fotos, campos padrão, tags e campos personalizados.
* RF09 Mover item. O sistema deve permitir mover um item entre coleções do mesmo dono.
* RF10 Registrar dados privados do item. O sistema deve permitir registrar valor pago, valor estimado, data de aquisição e observações privadas.
* RF11 Visualizar conteúdo público. O sistema deve exibir perfis, coleções públicas e seus itens para qualquer pessoa, sem exigir login.
* RF12 Buscar no próprio acervo. O sistema deve permitir busca textual e filtros sobre os itens do próprio usuário.
* RF13 Exportar dados. O sistema deve gerar um arquivo com todos os dados do usuário em JSON e CSV.
* RF14 Excluir conta. O sistema deve permitir que o usuário exclua definitivamente a conta e todos os dados associados.

## 4. Requisitos não funcionais

* RNF01 Desempenho. Páginas públicas devem carregar em até 2 segundos no percentil 95 em conexão 4G.
* RNF02 Usabilidade. A interface deve ser utilizável em telas a partir de 360 pixels de largura.
* RNF03 Acessibilidade. A interface deve atender a WCAG 2.1 nível AA.
* RNF04 Imagens. Toda foto deve ser servida em pelo menos 3 tamanhos (miniatura, média e ampliada).
* RNF05 Segurança. Senhas devem ser armazenadas com algoritmo de hash adaptativo e toda comunicação deve ser criptografada.
* RNF06 Privacidade. O sistema deve cumprir a LGPD, com termos de uso, política de privacidade e registro do consentimento.
* RNF07 Idioma. A interface deve estar em português do Brasil, com textos externalizados para permitir tradução futura.
* RNF08 Disponibilidade. O sistema deve estar disponível em 99,5% do tempo em cada mês.
* RNF09 Recuperação. Os dados devem ter cópia de segurança diária com retenção de 30 dias.

## 5. Regras de negócio

* RN01 (RF01) O nome de usuário é único, tem de 3 a 30 caracteres e aceita apenas letras minúsculas, números, sublinhado e ponto. O email também é único.
* RN02 (RF01, RF04) A senha tem no mínimo 8 caracteres, com pelo menos uma letra e um número.
* RN03 (RF02) Enquanto o email não for confirmado, o usuário pode cadastrar tudo, mas nenhum conteúdo fica público. O link de confirmação vale 24 horas.
* RN04 (RF03) Após 5 tentativas de login incorretas em 15 minutos, o login da conta fica bloqueado por 15 minutos.
* RN05 (RF04) O link de recuperação de senha é de uso único e vale 1 hora.
* RN06 (RF06) Toda coleção nasce privada, tem nome obrigatório de até 80 caracteres e exatamente uma categoria.
* RN07 (RF06) Excluir uma coleção exclui todos os seus itens, e o sistema exige confirmação informando a quantidade de itens.
* RN08 (RF08) Todo item tem nome obrigatório e de 1 a 10 fotos. Cada foto tem até 15 MB, nos formatos JPEG, PNG, WEBP ou HEIC. A primeira foto é a capa.
* RN09 (RF08) Os metadados de localização de toda foto são removidos antes de a foto ficar visível.
* RN10 (RF10, RF11) Valor pago, valor estimado, data de aquisição e observações privadas nunca são exibidos a outros usuários.
* RN11 (RF11) Uma coleção privada acessada por terceiro responde como não encontrada.
* RN12 (RF14) A exclusão de conta exige confirmação com a senha, é concluída em até 30 dias e o nome de usuário fica reservado por 90 dias.
* RN13 (RF06) O estado de conservação segue a escala Novo lacrado, Excelente, Muito bom, Bom, Regular e Ruim. O campo grau aceita escalas específicas da categoria, como MS70 ou PSA 10.

## 6. Entidades principais

* Usuário. Credenciais, situação do email e situação da conta.
* Perfil. Dados públicos do usuário. Um para um com Usuário.
* Categoria. Tipo de colecionável, mantido pela plataforma.
* Coleção. Pertence a um Usuário, tem uma Categoria, contém Itens, tem visibilidade e posição.
* Item. Pertence a uma Coleção, tem Fotos, Tags, campos padrão, campos personalizados e campos privados.
* Foto. Pertence a um Item, tem posição e variantes de tamanho.
* Tag. Rótulo livre criado pelo usuário e associado a Itens.

## 7. Fora do escopo desta feature

* Seguir usuários, feed, curtidas e comentários, tratados na Spec 002.
* Busca global de coleções e pessoas, tratada na Spec 003.
* Listas de desejo e trocas, tratadas na Spec 004.
* Login social com Google ou Apple.
* Importação de planilhas.

## 8. Métricas de sucesso

* Um novo usuário consegue criar conta, uma coleção e o primeiro item com foto em menos de 3 minutos.
* Pelo menos 60% dos usuários que criam conta cadastram 5 itens ou mais na primeira semana.

## 9. Clarificações

Sessão de 29/09/2026. Todas as perguntas foram resolvidas com a proposta padrão e podem ser revistas.

* C1 Usuário sem email confirmado pode cadastrar itens? Decisão. Pode cadastrar tudo, mas nada fica público até confirmar (RN03).
* C2 Categorias são fixas ou livres? Decisão. Lista fixa com a opção Outros. Categorias iniciais Moedas, Cédulas, Selos, Cards, Miniaturas, Action Figures, Brinquedos, Discos, Quadrinhos, Livros, Relógios, Camisas de Futebol e Outros.
* C3 Existe perfil privado? Decisão. Não no MVP. O perfil é sempre público e a privacidade é controlada por coleção.
* C4 Qual o limite de fotos? Decisão. 15 MB por foto e sem cota total no MVP, com monitoramento de uso (RN08).
* C5 Login social no lançamento? Decisão. Não. Apenas email e senha.
* C6 Escala de conservação única ou por categoria? Decisão. Escala genérica com campo livre de grau (RN13).
* C7 Público inicial é um nicho ou todos os colecionáveis? Decisão. Todos, organizados por categoria.
