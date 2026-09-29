# Arquitetura do Sistema

Decisões técnicas válidas para todas as features. Cada `plan.md` herda estas decisões e só registra o que for novo ou diferente.

## Visão geral

O Collection Social é um monólito modular em TypeScript. Uma única base de código gera uma imagem de container que roda em dois processos, a aplicação web e o processador de tarefas em segundo plano. Os dados ficam em PostgreSQL e as fotos em armazenamento de objetos compatível com S3.

## Stack

* Linguagem TypeScript em modo estrito, no cliente e no servidor. Um só idioma de programação reduz a troca de contexto.
* Next.js com App Router, React Server Components e Server Actions. Entrega páginas públicas renderizadas no servidor (RNF01) e a interface logada no mesmo projeto.
* Tailwind CSS para estilos, com componentes acessíveis (RNF02, RNF03).
* Aplicação web instalável (PWA) com acesso à câmera do celular para fotografar peças.
* PostgreSQL 16 como banco de dados, acessado pelo Prisma ORM, com migrações versionadas.
* Busca textual do próprio PostgreSQL com as extensões unaccent e pg_trgm, que atendem à tolerância a acentos e erros de digitação (RNF12) sem um motor de busca separado (Constituição IV).
* Armazenamento de objetos compatível com S3 para as fotos. MinIO no ambiente local e um provedor gerenciado em produção.
* Processamento de imagens com a biblioteca sharp, que gera as variantes de tamanho (RNF04) e remove metadados de localização (RN09).
* Fila de tarefas Graphile Worker, que usa o próprio PostgreSQL e dispensa um serviço extra. Atende ao processamento de fotos, envio de emails, notificações, exportação de dados e expiração de propostas.
* Autenticação com a biblioteca Better Auth, com email e senha, confirmação de email, recuperação de senha, limite de tentativas (RN04) e hash scrypt (RNF05).
* Validação de toda entrada com Zod, compartilhando os esquemas entre cliente e servidor.
* Emails transacionais por SMTP com Nodemailer.
* Logs estruturados em JSON com Pino (Constituição VII).
* Testes unitários e de integração com Vitest e Testcontainers (PostgreSQL e MinIO reais). Testes de ponta a ponta com Playwright.
* Implantação por container Docker, com HTTPS obrigatório.

## Camadas

1. Apresentação. Páginas e componentes do Next.js, rotas públicas e rotas logadas.
2. Aplicação. Server Actions e rotas de API que validam a entrada e chamam os serviços de domínio.
3. Domínio. Módulos com as regras de negócio, sem dependência de framework.
4. Infraestrutura. Repositórios Prisma, cliente do armazenamento de objetos, fila de tarefas e envio de emails.

## Módulos de domínio

* contas. Cadastro, autenticação, confirmação de email, recuperação de senha, exclusão de conta. Spec 001.
* perfis. Perfil público e categorias de interesse. Spec 001.
* acervo. Coleções, itens, tags, campos personalizados, dados privados, busca no acervo, exportação. Spec 001.
* midia. Envio, validação e processamento de fotos. Spec 001.
* social. Seguimentos, feed, curtidas, comentários, bloqueios. Spec 002.
* moderacao. Denúncias e decisões de moderação. Spec 002.
* notificacoes. Notificações no sistema e por email. Spec 002.
* descoberta. Busca global, explorar e sugestões. Spec 003.
* trocas. Desejos, disponibilidade, correspondências, propostas, mensagens e avaliações. Spec 004.

Regra de dependência. Um módulo só usa outro pela interface pública que ele exporta, nunca acessando suas tabelas diretamente.

## Estrutura de pastas

```
src/
  app/                  rotas do Next.js (apresentação)
  modulos/
    contas/
    perfis/
    acervo/
    midia/
    social/
    moderacao/
    notificacoes/
    descoberta/
    trocas/
  infra/                banco, armazenamento, fila, email, logs
  tarefas/              processadores da fila
prisma/
  schema.prisma
tests/
  integracao/
  ponta_a_ponta/
```

## Ambientes

* Local. Docker Compose com PostgreSQL, MinIO e Mailpit para ver os emails.
* Produção. Container da aplicação web, container do processador de tarefas, PostgreSQL gerenciado com cópia de segurança diária de 30 dias (RNF09) e armazenamento de objetos gerenciado.
