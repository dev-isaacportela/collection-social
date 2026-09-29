# Collection Social

Rede social para colecionadores. Catalogar coleções, mostrar peças, seguir outros colecionadores e negociar trocas.

Este projeto é desenvolvido com Spec Driven Development (SDD). A especificação é o artefato principal e o código é derivado dela.

## Fluxo SDD

Cada feature passa pelas mesmas etapas, e cada etapa gera um artefato versionado em `specs/NNN_nome_da_feature/`.

1. Specify. Gera o `spec.md`, que responde o quê e por quê, sem tecnologia. Aprovação de produto.
2. Clarify. Resolve as dúvidas na seção Clarificações do `spec.md`. Aprovação de produto.
3. Plan. Gera `plan.md` e `data_model.md`, que respondem como (arquitetura, stack, dados). Aprovação de engenharia.
4. Tasks. Gera `tasks.md`, com passos pequenos, ordenados e testáveis. Aprovação de engenharia.
5. Implement. Código e testes, uma task por vez. Aprovação por revisão de PR.
6. Document. Ao final das specs, o documento acadêmico em padrão ABNT é gerado a partir delas, em `docs/entrega/`.

Regras do fluxo

* Nenhuma etapa começa enquanto a anterior tiver itens NEEDS CLARIFICATION em aberto.
* Mudou o requisito? Atualize o `spec.md` primeiro e depois propague para plan, tasks e código.
* Todo plano é verificado contra a [constituição](.specify/memory/constitution.md).
* Requisitos têm numeração global (RF01, RNF01, RN01) para manter a rastreabilidade entre specs, diagramas e documento.
* Nenhum texto do projeto usa hífen, travessão ou dois pontos. O script `ferramentas/verificar_texto.py` confere isso.

## Estrutura

```
.specify/
  memory/constitution.md       princípios inegociáveis do projeto
  templates/                   modelos de spec, plan e tasks
docs/
  visao_do_produto.md          visão, personas e roadmap
  arquitetura.md               stack e arquitetura do sistema
  rastreabilidade.md           matriz RF, RN, casos de uso e diagramas
  uml/                         fontes PlantUML e imagens dos diagramas
  entrega/                     documento ABNT em DOCX e PDF
specs/
  001_perfis_e_colecoes/
  002_rede_social_e_moderacao/
  003_descoberta/
  004_listas_e_trocas/
ferramentas/                   scripts de geração e verificação
```

## Status das features

* [001 Perfis e Coleções](specs/001_perfis_e_colecoes/spec.md). Spec, plano, modelo de dados e tasks prontos. Próxima etapa é Implement.
* [002 Rede Social e Moderação](specs/002_rede_social_e_moderacao/spec.md). Spec pronta.
* [003 Descoberta](specs/003_descoberta/spec.md). Spec pronta.
* [004 Listas e Trocas](specs/004_listas_e_trocas/spec.md). Spec pronta.

## Documento acadêmico

O documento de negócios, requisitos e modelagem UML fica em `docs/entrega/`. Para gerar novamente

```
python3 ferramentas/gerar_diagramas.py
python3 ferramentas/gerar_documento.py
python3 ferramentas/verificar_texto.py
```
