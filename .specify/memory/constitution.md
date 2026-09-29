# Constituição do Collection Social

Princípios que todo `plan.md` e todo PR devem respeitar. Alterar esta constituição exige um PR próprio, com justificativa e atualização da versão abaixo.

Versão 1.0.0, ratificada em 29/09/2026.

## I. A especificação é a fonte da verdade

O comportamento do sistema é definido em `specs/`. Código que implementa comportamento não especificado é um defeito, não uma feature. Mudanças de requisito começam no `spec.md`.

## II. Teste primeiro (inegociável)

Cada critério de aceitação do spec vira pelo menos um teste automatizado antes da implementação. A ordem nas tasks é sempre teste falhando, implementação, teste passando. Testes de integração usam dependências reais (banco, armazenamento) em containers, e não simulações, sempre que viável.

## III. O colecionador é dono dos seus dados

* Privacidade por padrão. Nada que o usuário não marcou como público aparece para terceiros.
* Valor pago, valor estimado, data de aquisição e observações privadas nunca aparecem em feed, busca ou página pública.
* O usuário pode exportar (JSON e CSV) e apagar definitivamente todos os seus dados.
* Conformidade com a LGPD desde a primeira feature.

## IV. Simplicidade

* Uma única aplicação implantável (monólito modular) até que exista um motivo medido para dividir.
* Nenhuma abstração para o futuro. Só se generaliza na terceira ocorrência.
* Toda dependência nova precisa ser justificada no `plan.md`.

## V. Celular primeiro e acessível

A maior parte do uso será no celular, fotografando peças. Toda interface é desenhada primeiro para telas pequenas e atende a WCAG 2.1 nível AA.

## VI. Imagens são cidadãs de primeira classe

Fotos são o conteúdo central da rede. Todo envio é redimensionado, tem os metadados de localização removidos e é servido em tamanhos adequados à tela.

## VII. Observabilidade e segurança desde o primeiro dia

Logs estruturados, tratamento explícito de erros, autenticação segura (hash forte de senha, limite de tentativas de login) e validação de toda entrada do usuário no servidor.

## VIII. Texto sem hífen e sem dois pontos

Specs, documentação, textos de interface, diagramas e o documento acadêmico não usam hífen, travessão nem dois pontos. Exceção única para sintaxe de código (arquivos de código e fontes PlantUML), que não é texto de leitura.

## Governança

* Cada `plan.md` tem uma seção Verificação da Constituição listando cada princípio como atendido ou como exceção justificada.
* Exceções sem justificativa bloqueiam o merge.
