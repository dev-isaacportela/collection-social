# CLAUDE.md

Este projeto segue Spec Driven Development. Antes de qualquer mudança, leia

1. `.specify/memory/constitution.md`, com os princípios inegociáveis.
2. `docs/visao_do_produto.md`, com a visão e o roadmap.
3. `specs/NNN_*/spec.md` da feature em questão.

## Regras para agentes

* Não escreva código de feature sem `spec.md`, `plan.md` e `tasks.md` aprovados para ela.
* Se um requisito parecer ambíguo, marque NEEDS CLARIFICATION no spec e pergunte. Não invente.
* O `spec.md` não contém tecnologia. O `plan.md` contém.
* Implemente uma task por vez, na ordem de `tasks.md`, com o teste antes da implementação, e marque `[x]` ao concluir.
* Se a implementação revelar que o spec está errado ou incompleto, pare e proponha a alteração no spec primeiro.
* Requisitos usam numeração global. Ao criar uma feature, continue a partir do último RF, RNF e RN existentes.
* Documentação e textos da interface em português do Brasil.
* Nunca use hífen, travessão ou dois pontos em texto (Markdown, interface, diagramas, documento). Use `_` em nomes de arquivos e pastas. Rode `python3 ferramentas/verificar_texto.py` antes de commitar.
* Novas features copiam os modelos de `.specify/templates/` para `specs/NNN_nome/`.
* Diagramas UML são feitos no formato do draw.io (`docs/uml/*.drawio`), gerados por `ferramentas/gerar_diagramas.py` com as formas UML padrão da ferramenta.
* Ao final das specs, atualize `docs/rastreabilidade.md`, os diagramas em `docs/uml/` e gere o documento ABNT com `ferramentas/gerar_documento.py`.
