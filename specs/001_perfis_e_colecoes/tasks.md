# Tasks da Spec 001 Perfis e Coleções

Plano de origem em [plan.md](./plan.md).

Convenções

* [P] indica que a task pode rodar em paralelo com outras [P] da mesma fase.
* Cada task referencia a história (US1) ou o requisito (RF01) que atende.
* Testes vêm antes da implementação (Constituição, princípio II).

## Fase 0 Preparação

* [ ] T001 Criar o projeto Next.js com TypeScript estrito, Tailwind CSS e a estrutura de pastas de `docs/arquitetura.md`.
* [ ] T002 [P] Criar o Docker Compose local com PostgreSQL, MinIO e Mailpit.
* [ ] T003 [P] Configurar Vitest, Testcontainers e Playwright com axe.
* [ ] T004 [P] Configurar Pino, variáveis de ambiente validadas com Zod e a integração contínua com lint, verificação de tipos, testes e `ferramentas/verificar_texto.py`.

## Fase 1 Fundação (bloqueia as histórias)

* [ ] T010 Escrever o schema Prisma de `data_model.md` e a primeira migração, com as extensões unaccent e pg_trgm.
* [ ] T011 Popular as categorias iniciais definidas na clarificação C2.
* [ ] T012 [P] Implementar o cliente do armazenamento de objetos e a geração de URLs assinadas.
* [ ] T013 [P] Configurar o Graphile Worker e o processo do processador de tarefas.
* [ ] T014 [P] Implementar o envio de emails com Nodemailer e modelos de email em português.
* [ ] T015 Configurar o Better Auth com email e senha, confirmação de email e limite de tentativas.

## Fase 2 US1 Criar conta e entrar (P1)

* [ ] T020 [US1] Testes de integração de cadastro com conflitos de email e nome de usuário (RN01) e regra de senha (RN02).
* [ ] T021 [US1] Testes de confirmação de email com validade de 24 horas (RN03), bloqueio de login (RN04) e link de recuperação (RN05).
* [ ] T022 [US1] Implementar as ações e páginas de cadastro, confirmação, entrada, saída e recuperação de senha (RF01 a RF04).
* [ ] T023 [US1] Teste de ponta a ponta do cadastro até a primeira entrada.

## Fase 3 US2 Montar meu perfil (P1)

* [ ] T030 [US2] Testes de atualização de perfil e validação da bio.
* [ ] T031 [US2] Implementar atualizarPerfil e a página de configurações do perfil (RF05).
* [ ] T032 [US2] Implementar a página pública do perfil (RF11).

## Fase 4 US3 Criar e organizar coleções (P1)

* [ ] T040 [US3] Testes de criação com visibilidade privada por padrão (RN06), exclusão com contagem de itens (RN07) e reordenação.
* [ ] T041 [US3] Implementar as ações de coleção (RF06, RF07).
* [ ] T042 [US3] Implementar as telas de lista, criação e edição de coleções.

## Fase 5 US4 Cadastrar itens com fotos (P1)

* [ ] T050 [US4] Testes de validação de fotos, quantidade de 1 a 10, tamanho e formato (RN08).
* [ ] T051 [US4] Teste da tarefa processarFoto garantindo remoção dos metadados de localização (RN09) e geração das 3 variantes (RNF04).
* [ ] T052 [US4] Teste garantindo que campos privados nunca aparecem em respostas públicas (RN10).
* [ ] T053 [US4] Implementar gerarUrlsDeEnvio e a tarefa processarFoto.
* [ ] T054 [US4] Implementar as ações de item, incluindo mover item (RF08, RF09, RF10).
* [ ] T055 [US4] Implementar o formulário de item com câmera do celular e reordenação de fotos.

## Fase 6 US5 Ver coleções de outros colecionadores (P2)

* [ ] T060 [US5] Teste de não encontrado para coleção privada (RN11) e para dono sem email confirmado (RN03).
* [ ] T061 [US5] Implementar as páginas públicas de coleção e item (RF11).
* [ ] T062 [US5] Teste de desempenho das páginas públicas (RNF01).

## Fase 7 US6 Buscar no meu próprio acervo (P2)

* [ ] T070 [US6] Testes de busca sem acentos, com erro de digitação e com filtros combinados.
* [ ] T071 [US6] Implementar buscarNoAcervo e a página de acervo (RF12).

## Fase 8 US7 Exportar e apagar meus dados (P2)

* [ ] T080 [US7] Testes do arquivo de exportação em JSON e CSV (RF13) e da exclusão definitiva com reserva do nome de usuário (RN12).
* [ ] T081 [US7] Implementar a exportação e a exclusão de conta (RF13, RF14).

## Fase 9 Acabamento

* [ ] T090 Auditoria de acessibilidade em todas as telas (RNF03).
* [ ] T091 Revisão dos textos da interface com o verificador de texto (Constituição VIII).
* [ ] T092 Atualizar `docs/rastreabilidade.md` com os testes criados.
