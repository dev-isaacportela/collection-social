# Matriz de Rastreabilidade

Arquivo gerado por `ferramentas/gerar_documento.py` a partir das specs e de `docs/casos_de_uso.md`. Não edite à mão.

## Casos de uso para requisitos e regras

* UC01 Cadastrar conta. Requisitos RF01, RF02. Regras RN01, RN02, RN03.
* UC02 Confirmar email. Requisitos RF02. Regras RN03.
* UC03 Autenticar usuário. Requisitos RF03. Regras RN04, RN20.
* UC04 Recuperar senha. Requisitos RF04. Regras RN02, RN05.
* UC05 Visualizar conteúdo público. Requisitos RF11. Regras RN10, RN11.
* UC06 Buscar e explorar comunidade. Requisitos RF23, RF24, RF25. Regras RN21, RN22.
* UC07 Gerenciar perfil. Requisitos RF05. Regras nenhuma específica.
* UC08 Gerenciar coleções. Requisitos RF06, RF07. Regras RN06, RN07.
* UC09 Gerenciar itens. Requisitos RF08, RF09, RF10. Regras RN08, RN09, RN10, RN13.
* UC10 Buscar no acervo. Requisitos RF12. Regras nenhuma específica.
* UC11 Gerenciar dados pessoais. Requisitos RF13, RF14. Regras RN12.
* UC12 Seguir colecionador. Requisitos RF15, RF26. Regras RN14, RN23.
* UC13 Visualizar feed. Requisitos RF16. Regras RN15.
* UC14 Interagir com item. Requisitos RF17, RF18. Regras RN16, RN17.
* UC15 Bloquear usuário. Requisitos RF20. Regras RN18.
* UC16 Denunciar conteúdo. Requisitos RF21. Regras RN19.
* UC17 Moderar denúncias. Requisitos RF22. Regras RN19, RN20.
* UC18 Gerenciar lista de desejos. Requisitos RF27, RF29. Regras RN31.
* UC19 Disponibilizar item para troca. Requisitos RF28. Regras RN24.
* UC20 Propor troca. Requisitos RF30. Regras RN25.
* UC21 Negociar proposta. Requisitos RF31, RF32. Regras RN26, RN27.
* UC22 Concluir troca. Requisitos RF33. Regras RN28, RN29.
* UC23 Avaliar troca. Requisitos RF34. Regras RN30.
* UC24 Consultar notificações. Requisitos RF19. Regras nenhuma específica.

## Requisitos funcionais para casos de uso

* RF01 Cadastrar conta. UC01.
* RF02 Confirmar email. UC01, UC02.
* RF03 Autenticar usuário. UC03.
* RF04 Recuperar senha. UC04.
* RF05 Gerenciar perfil. UC07.
* RF06 Gerenciar coleções. UC08.
* RF07 Ordenar coleções. UC08.
* RF08 Gerenciar itens. UC09.
* RF09 Mover item. UC09.
* RF10 Registrar dados privados do item. UC09.
* RF11 Visualizar conteúdo público. UC05.
* RF12 Buscar no próprio acervo. UC10.
* RF13 Exportar dados. UC11.
* RF14 Excluir conta. UC11.
* RF15 Seguir colecionador. UC12.
* RF16 Visualizar feed. UC13.
* RF17 Curtir item. UC14.
* RF18 Comentar item. UC14.
* RF19 Notificar usuário. UC24.
* RF20 Bloquear usuário. UC15.
* RF21 Denunciar conteúdo. UC16.
* RF22 Moderar denúncias. UC17.
* RF23 Buscar na comunidade. UC06.
* RF24 Filtrar resultados. UC06.
* RF25 Explorar destaques. UC06.
* RF26 Sugerir colecionadores. UC12.
* RF27 Gerenciar lista de desejos. UC18.
* RF28 Disponibilizar item para troca. UC19.
* RF29 Notificar correspondência. UC18.
* RF30 Propor troca. UC20.
* RF31 Responder proposta. UC21.
* RF32 Trocar mensagens na proposta. UC21.
* RF33 Concluir troca. UC22.
* RF34 Avaliar troca. UC23.

## Regras de negócio para casos de uso

* RN01 (RF01). UC01.
* RN02 (RF01, RF04). UC01, UC04.
* RN03 (RF02). UC01, UC02.
* RN04 (RF03). UC03.
* RN05 (RF04). UC04.
* RN06 (RF06). UC08.
* RN07 (RF06). UC08.
* RN08 (RF08). UC09.
* RN09 (RF08). UC09.
* RN10 (RF10, RF11). UC05, UC09.
* RN11 (RF11). UC05.
* RN12 (RF14). UC11.
* RN13 (RF06). UC09.
* RN14 (RF15). UC12.
* RN15 (RF16). UC13.
* RN16 (RF17). UC14.
* RN17 (RF18). UC14.
* RN18 (RF20). UC15.
* RN19 (RF21, RF22). UC16, UC17.
* RN20 (RF22). UC03, UC17.
* RN21 (RF23, RF24). UC06.
* RN22 (RF25). UC06.
* RN23 (RF26). UC12.
* RN24 (RF28). UC19.
* RN25 (RF30). UC20.
* RN26 (RF31). UC21.
* RN27 (RF31). UC21.
* RN28 (RF33). UC22.
* RN29 (RF33). UC22.
* RN30 (RF34). UC23.
* RN31 (RF29). UC18.

## Diagramas

* Casos de uso. `docs/uml/01a_casos_de_uso_contas_acervo.puml` e `docs/uml/01b_casos_de_uso_social_trocas.puml`.
* Classes. `docs/uml/02a_classes_contas_acervo.puml`, `docs/uml/02b_classes_social_moderacao.puml` e `docs/uml/02c_classes_trocas.puml`.
* Atividades. `docs/uml/03_atividades_troca.puml`, processo de UC20 a UC23, regras RN25 a RN30.
* Sequência. `docs/uml/04_sequencia_cadastrar_item.puml`, cenário do UC09, regras RN08 e RN09.
* Estados. `docs/uml/05_estados_proposta.puml`, proposta de troca, regras RN26 a RN29.
* Componentes. `docs/uml/06_componentes.puml`, arquitetura de `docs/arquitetura.md`.
* Objetos. `docs/uml/07_objetos_troca.puml`, cenário do UC21, regras RN24 e RN25.
