# Plano Técnico da Spec 001 Perfis e Coleções

Spec de origem em [spec.md](./spec.md). Status Aprovado.

## 1. Resumo técnico

A feature cria a fundação do sistema. Projeto Next.js, banco PostgreSQL, armazenamento de fotos, fila de tarefas e os módulos contas, perfis, acervo e midia. As páginas públicas de perfil, coleção e item são renderizadas no servidor e as ações do dono usam Server Actions validadas com Zod. As fotos são enviadas direto ao armazenamento por URL assinada, e uma tarefa da fila gera as variantes e remove os metadados antes de liberar a foto.

## 2. Contexto técnico

Herda todas as decisões de [arquitetura.md](../../docs/arquitetura.md). Nenhuma dependência nova além das listadas lá.

## 3. Verificação da Constituição

* I. Spec como fonte da verdade. Atendido. Cada rota e ação aponta para um RF na seção 7.
* II. Teste primeiro. Atendido. Em `tasks.md` cada história começa pelos testes.
* III. Dono dos dados. Atendido. Campos privados ficam em tabela separada, lida apenas por consultas do dono (RN10). Exportação e exclusão fazem parte desta feature.
* IV. Simplicidade. Atendido. Um projeto, um banco, fila no próprio banco, busca no próprio banco.
* V. Celular primeiro e acessível. Atendido. Layout desenhado a partir de 360 pixels e testes automáticos de acessibilidade com axe no Playwright.
* VI. Imagens. Atendido. Variantes de 320, 960 e 1920 pixels em WEBP, sem metadados de localização.
* VII. Observabilidade e segurança. Atendido. Pino, limite de tentativas no login, validação Zod no servidor.
* VIII. Texto sem hífen e sem dois pontos. Atendido. Textos da interface externalizados e verificados pelo script do projeto.

## 4. Arquitetura

Fluxo de cadastro de item com fotos

1. O dono preenche o formulário e escolhe as fotos.
2. O cliente pede ao servidor URLs assinadas de envio, uma por foto, e o servidor valida formato e tamanho declarados (RN08).
3. O cliente envia cada foto direto ao armazenamento.
4. O cliente chama a ação criar item com os dados e as chaves das fotos. O servidor valida tudo, grava o item e as fotos com situação em processamento, em uma única transação, e enfileira uma tarefa por foto.
5. A tarefa baixa o original, confere o formato real, remove os metadados, gera as variantes, grava no armazenamento e marca a foto como pronta. Falha de validação marca a foto como rejeitada e notifica o dono.
6. O item só aparece para terceiros quando a foto de capa estiver pronta.

Controle de visibilidade

* Toda consulta pública passa por uma função única do módulo acervo que aplica coleção pública, dono com email confirmado e conta ativa (RN03, RN11).
* Os campos privados ficam na entidade DadosPrivadosItem e nunca são incluídos em consultas públicas (RN10).

## 5. Modelo de dados

Ver [data_model.md](./data_model.md).

## 6. Interfaces

Páginas

* `/cadastro`, `/entrar`, `/recuperar_senha`, `/confirmar_email`
* `/u/[usuario]` perfil público
* `/u/[usuario]/c/[colecao]` coleção
* `/u/[usuario]/c/[colecao]/i/[item]` item
* `/acervo` busca no próprio acervo
* `/configuracoes` perfil, exportação e exclusão de conta

Server Actions

* contas. cadastrar, entrar, sair, solicitarRecuperacao, redefinirSenha, solicitarExclusao
* perfis. atualizarPerfil
* acervo. criarColecao, editarColecao, excluirColecao, reordenarColecoes, criarItem, editarItem, excluirItem, moverItem, buscarNoAcervo, solicitarExportacao
* midia. gerarUrlsDeEnvio

Tarefas da fila

* processarFoto, enviarEmail, gerarExportacao, excluirContaDefinitivamente

## 7. Rastreabilidade

* RF01 e RF02. contas.cadastrar, página `/confirmar_email`. Teste de integração de cadastro e teste de ponta a ponta do fluxo de cadastro.
* RF03. contas.entrar e contas.sair. Teste do bloqueio após 5 tentativas (RN04).
* RF04. contas.solicitarRecuperacao e contas.redefinirSenha. Teste de link de uso único (RN05).
* RF05. perfis.atualizarPerfil. Teste de validação da bio.
* RF06 e RF07. acervo.criarColecao, editarColecao, excluirColecao, reordenarColecoes. Testes de RN06 e RN07.
* RF08 e RF09. acervo.criarItem, editarItem, excluirItem, moverItem, midia.gerarUrlsDeEnvio, tarefa processarFoto. Testes de RN08 e RN09.
* RF10. DadosPrivadosItem. Teste que garante ausência dos campos em toda resposta pública (RN10).
* RF11. Páginas públicas. Teste de não encontrado para coleção privada (RN11).
* RF12. acervo.buscarNoAcervo. Teste de busca sem acentos e com filtros combinados.
* RF13. acervo.solicitarExportacao e tarefa gerarExportacao. Teste do conteúdo do arquivo.
* RF14. contas.solicitarExclusao e tarefa excluirContaDefinitivamente. Teste de RN12.

## 8. Riscos e decisões em aberto

* Fotos HEIC exigem suporte do sharp compilado com libheif. Se não houver, a conversão acontece no navegador antes do envio.
* Custo de armazenamento sem cota por usuário. Monitorar e reavaliar a cota após 3 meses.
