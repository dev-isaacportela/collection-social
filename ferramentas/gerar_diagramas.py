"""Gera os diagramas UML do projeto no formato nativo do draw.io e exporta os PNGs.

Cada diagrama vira um arquivo docs/uml/NN_nome.drawio, que pode ser aberto e
editado no draw.io ou no diagrams.net. As imagens PNG usadas no documento sao
exportadas pelo proprio renderizador do draw.io (export3.html do webapp
oficial), executado no Chromium do Playwright.

Uso
  python3 ferramentas/gerar_diagramas.py            gera .drawio e .png
  python3 ferramentas/gerar_diagramas.py sem_png    gera apenas os .drawio
"""

import os
import subprocess
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from drawio_uml import (  # noqa: E402
    ACAO, AGREGACAO, ASSOCIACAO, ASSOCIACAO_DIRIGIDA, ASSOCIACAO_SIMPLES, ATIVACAO, ATOR, BANCO, BARRA,
    CASO_DE_USO, CLASSE_TEXTO, COMPONENTE, COMPOSICAO, DECISAO, DEPENDENCIA, ESTADO, ESTADO_COMPOSTO,
    ESTADO_TEXTO, FINAL, FLUXO, GENERALIZACAO, HERANCA, INCLUDE, INICIAL, INTERFACE, LINHA_DE_VIDA,
    LINHA_TRACEJADA, MENSAGEM, OBJETO, PACOTE, QUADRO, RAIA, RETORNO, SISTEMA, TEXTO, TRANSICAO,
    Diagrama, classe, dimensoes_classe, largura_texto,
)

RAIZ = Path(__file__).resolve().parent.parent
PASTA_UML = RAIZ / "docs" / "uml"
CACHE = Path(__file__).resolve().parent / ".cache"
VERSAO_DRAWIO = "14.6.12"
ESCALA_PNG = 2.5


# ================================================================ casos de uso

NOMES_UC = {
    "UC01": "UC01 Cadastrar conta", "UC02": "UC02 Confirmar email", "UC03": "UC03 Autenticar usuário",
    "UC04": "UC04 Recuperar senha", "UC05": "UC05 Visualizar conteúdo público",
    "UC06": "UC06 Buscar e explorar comunidade", "UC07": "UC07 Gerenciar perfil",
    "UC08": "UC08 Gerenciar coleções", "UC09": "UC09 Gerenciar itens", "UC10": "UC10 Buscar no acervo",
    "UC11": "UC11 Gerenciar dados pessoais", "UC12": "UC12 Seguir colecionador",
    "UC13": "UC13 Visualizar feed", "UC14": "UC14 Interagir com item", "UC15": "UC15 Bloquear usuário",
    "UC16": "UC16 Denunciar conteúdo", "UC17": "UC17 Moderar denúncias",
    "UC18": "UC18 Gerenciar lista de desejos", "UC19": "UC19 Disponibilizar item para troca",
    "UC20": "UC20 Propor troca", "UC21": "UC21 Negociar proposta", "UC22": "UC22 Concluir troca",
    "UC23": "UC23 Avaliar troca", "UC24": "UC24 Consultar notificações",
}


def casos_de_uso(nome, pacotes, atores_esquerda, atores_direita, generalizacoes, associacoes, relacoes):
    """pacotes lista de (titulo, linhas); cada linha tem um ou dois casos de uso (coluna 1 e coluna 2).

    As associacoes chegam na ponta esquerda ou direita da elipse, assim nenhuma linha atravessa
    outro caso de uso da mesma coluna.
    """
    d = Diagrama(nome)
    uc_w, uc_h, passo, gap = 200, 56, 76, 100
    x_ator_esq = 80
    x_sistema, y_sistema = 250, 20
    x_pacote = x_sistema + 24
    largura_pacote = 2 * uc_w + 3 * gap
    posicoes = {}
    y = y_sistema + 40
    caixas_pacote = []
    for titulo, linhas in pacotes:
        altura = 46 + passo * len(linhas)
        caixas_pacote.append((titulo, y, altura))
        for i, linha in enumerate(linhas):
            for coluna, uc in enumerate(linha):
                if uc:
                    posicoes[uc] = (x_pacote + gap + coluna * (uc_w + gap), y + 40 + i * passo)
        y += altura + 24
    altura_sistema = y - y_sistema
    largura_sistema = largura_pacote + 48
    d.vertice("Collection Social", SISTEMA, x_sistema, y_sistema, largura_sistema, altura_sistema)
    for titulo, y_p, altura in caixas_pacote:
        aba = int(largura_texto(titulo, negrito=True)) + 30
        d.vertice(titulo, PACOTE.replace("tabWidth=120;", f"tabWidth={aba};"), x_pacote, y_p, largura_pacote, altura)
    ids = {uc: d.vertice(NOMES_UC[uc], CASO_DE_USO, x, y_uc, uc_w, uc_h) for uc, (x, y_uc) in posicoes.items()}

    centros = {}

    def posicionar_atores(atores, x):
        desejado = []
        for ator in atores:
            ligados = [posicoes[u][1] + uc_h / 2 for a, u in associacoes if a == ator]
            desejado.append((sum(ligados) / len(ligados), ator))
        desejado.sort()
        colocados, ultimo = {}, -1e9
        for alvo, ator in desejado:
            y_ator = max(alvo - 32, ultimo + 130)
            colocados[ator] = d.vertice(ator, ATOR, x, y_ator, 36, 64)
            centros[ator] = y_ator + 32
            ultimo = y_ator
        return colocados

    esquerda = posicionar_atores(atores_esquerda, x_ator_esq)
    direita = posicionar_atores(atores_direita, x_sistema + largura_sistema + 90)
    atores = {**esquerda, **direita}
    for filho, pai in generalizacoes:
        # a generalizacao contorna os atores pela esquerda para nao cobrir os nomes
        x_volta = x_ator_esq - 30
        d.aresta(atores[filho], atores[pai], GENERALIZACAO, saida=(0, 0.5), entrada=(0, 0.5),
                 pontos=[(x_volta, centros[filho]), (x_volta, centros[pai])])
    for ator, uc in associacoes:
        d.aresta(atores[ator], ids[uc], ASSOCIACAO, entrada=(0, 0.5) if ator in esquerda else (1, 0.5))
    for origem, destino, rotulo in relacoes:
        d.aresta(ids[origem], ids[destino], INCLUDE, valor=f"«{rotulo}»")
    return d


def diagrama_casos_de_uso_a():
    return casos_de_uso(
        "Casos de uso contas, acervo e descoberta",
        [
            ("Descoberta", [("UC05",), ("UC06",)]),
            ("Contas e Acesso", [("UC01", "UC02"), ("UC03", "UC04"), ("UC11",)]),
            ("Acervo", [("UC07",), ("UC08",), ("UC09",), ("UC10",)]),
        ],
        {"Visitante": None, "Colecionador": None},
        {"Serviço de Email": None},
        [("Colecionador", "Visitante")],
        [("Visitante", "UC01"), ("Visitante", "UC03"), ("Visitante", "UC05"), ("Visitante", "UC06"),
         ("Colecionador", "UC07"), ("Colecionador", "UC08"), ("Colecionador", "UC09"),
         ("Colecionador", "UC10"), ("Colecionador", "UC11"),
         ("Serviço de Email", "UC02"), ("Serviço de Email", "UC04")],
        [("UC01", "UC02", "include"), ("UC04", "UC03", "extend")],
    )


def diagrama_casos_de_uso_b():
    return casos_de_uso(
        "Casos de uso social, moderação e trocas",
        [
            ("Social e Moderação", [("UC17",), ("UC24",), ("UC12",), ("UC13",), ("UC14",), ("UC15",), ("UC16",)]),
            ("Trocas", [("UC09", "UC19"), ("UC18",), ("UC20",), ("UC21",), ("UC22", "UC23")]),
        ],
        {"Colecionador": None, "Moderador": None},
        {"Serviço de Email": None},
        [("Moderador", "Colecionador")],
        [("Colecionador", u) for u in ("UC12", "UC13", "UC14", "UC15", "UC16", "UC24", "UC09", "UC18",
                                        "UC20", "UC21", "UC22")]
        + [("Moderador", "UC17"), ("Serviço de Email", "UC24")],
        [("UC19", "UC09", "extend"), ("UC23", "UC22", "extend")],
    )


# ================================================================ classes


class Classes:
    """Posiciona classes pelo centro horizontal e liga com conectores ortogonais do draw.io."""

    ESTILOS = {"composicao": COMPOSICAO, "agregacao": AGREGACAO, "heranca": HERANCA, "dirigida": ASSOCIACAO_DIRIGIDA,
               "simples": ASSOCIACAO_SIMPLES, "dependencia": DEPENDENCIA}

    def __init__(self, nome, especificacao):
        self.d = Diagrama(nome)
        self.spec = especificacao
        self.caixas, self.ids = {}, {}

    def tamanho(self, nome):
        atributos, metodos, estereotipo = self.spec[nome]
        return dimensoes_classe(nome, atributos, metodos, estereotipo)

    def por(self, nome, cx, y=None, cy=None):
        w, h = self.tamanho(nome)
        topo = cy - h / 2 if cy is not None else y
        atributos, metodos, estereotipo = self.spec[nome]
        self.ids[nome] = classe(self.d, nome, atributos, metodos, cx - w / 2, topo, w, h, estereotipo)
        self.caixas[nome] = (cx - w / 2, topo, w, h)

    def rx(self, nome, x):
        cx, _, w, _ = self.caixas[nome]
        return (x - cx) / w

    def ry(self, nome, y):
        _, cy, _, h = self.caixas[nome]
        return (y - cy) / h

    def x(self, nome, rel):
        return self.caixas[nome][0] + rel * self.caixas[nome][2]

    def y(self, nome, rel):
        return self.caixas[nome][1] + rel * self.caixas[nome][3]

    def liga(self, tipo, origem, destino, saida, entrada, rotulo="", mult_origem=None, mult_destino=None, pontos=()):
        """composicao e agregacao partem do todo; heranca parte do filho; dirigida e dependencia apontam para o destino."""
        self.d.aresta(self.ids[origem], self.ids[destino], self.ESTILOS[tipo], valor=rotulo or "", saida=saida,
                      entrada=entrada, rotulo_origem=mult_origem, rotulo_destino=mult_destino, pontos=pontos)


def diagrama_classes_a():
    c = Classes("Classes contas e acervo", {
        "Usuario": (["UUID id", "String email", "String nomeUsuario", "String hashSenha",
                     "DateTime emailConfirmadoEm", "SituacaoConta situacao"],
                    ["Boolean confirmarEmail(String token)", "Boolean autenticar(String senha)",
                     "void solicitarExclusao()"], None),
        "Moderador": ([], ["void decidirDenuncia(Denuncia denuncia, String decisao)"], None),
        "Perfil": (["String nomeExibicao", "String bio", "String cidade", "String uf"],
                   ["void atualizar(DadosPerfil dados)"], None),
        "Categoria": (["String nome", "String slug"], [], None),
        "Colecao": (["UUID id", "String nome", "String descricao", "Visibilidade visibilidade", "Integer posicao"],
                    ["Boolean estaPublica()", "void reordenar(Integer novaPosicao)"], None),
        "Item": (["UUID id", "String nome", "String descricao", "Integer ano", "EstadoConservacao estado",
                  "String grau", "Integer quantidade", "Boolean disponivelParaTroca"],
                 ["void moverPara(Colecao destino)", "void marcarDisponivel(Boolean valor)"], None),
        "DadosPrivadosItem": (["Decimal valorPago", "Decimal valorEstimado", "Date dataAquisicao",
                               "String observacoes"], [], None),
        "Foto": (["String chaveOriginal", "Integer posicao", "SituacaoFoto situacao"], ["void processar()"], None),
        "Tag": (["String nome"], [], None),
        "Visibilidade": (["Publica", "Privada"], [], "enumeration"),
        "EstadoConservacao": (["NovoLacrado", "Excelente", "MuitoBom", "Bom", "Regular", "Ruim"], [], "enumeration"),
        "SituacaoConta": (["Ativa", "Suspensa", "EmExclusao"], [], "enumeration"),
        "SituacaoFoto": (["EmProcessamento", "Pronta", "Rejeitada"], [], "enumeration"),
    })
    c.por("Usuario", 560, y=20)
    meio_usuario = c.y("Usuario", 0.5)
    c.por("Moderador", 190, cy=meio_usuario)
    c.por("SituacaoConta", 960, cy=meio_usuario)
    c.por("Perfil", 330, y=290)
    c.por("Colecao", 700, y=290)
    c.por("Visibilidade", 1010, cy=c.y("Colecao", 0.5))
    c.por("Categoria", 330, y=540)
    c.por("Item", 700, y=540)
    c.por("EstadoConservacao", 1010, cy=c.y("Item", 0.5))
    c.por("DadosPrivadosItem", 430, y=840)
    c.por("Foto", 700, y=840)
    c.por("Tag", 930, y=840)
    c.por("SituacaoFoto", 700, y=1000)

    c.liga("heranca", "Moderador", "Usuario", (1, 0.5), (0, 0.5))
    c.liga("composicao", "Usuario", "Perfil", (c.rx("Usuario", 480), 1), (0.5, 0), "", "1", "1",
           pontos=[(480, 250), (330, 250)])
    c.liga("composicao", "Usuario", "Colecao", (c.rx("Usuario", 640), 1), (0.5, 0), "possui", "1", "0..*",
           pontos=[(640, 250), (700, 250)])
    c.liga("dependencia", "Usuario", "SituacaoConta", (1, 0.5), (0, 0.5))
    c.liga("dirigida", "Perfil", "Categoria", (0.5, 1), (0.5, 0), "interesses", "0..*", "0..*")
    c.liga("dirigida", "Colecao", "Categoria", (0, 0.85), (1, 0.5), "", "0..*", "1",
           pontos=[(500, c.y("Colecao", 0.85)), (500, c.y("Categoria", 0.5))])
    c.liga("dependencia", "Colecao", "Visibilidade", (1, 0.5), (0, 0.5))
    c.liga("composicao", "Colecao", "Item", (0.5, 1), (0.5, 0), "contém", "1", "0..*")
    c.liga("dependencia", "Item", "EstadoConservacao", (1, 0.5), (0, 0.5))
    y_filhos = c.y("Item", 1) + 40
    c.liga("composicao", "Item", "DadosPrivadosItem", (c.rx("Item", 620), 1), (0.5, 0), "", "1", "0..1",
           pontos=[(620, y_filhos), (430, y_filhos)])
    c.liga("composicao", "Item", "Foto", (0.5, 1), (0.5, 0), "", "1", "1..10")
    c.liga("agregacao", "Item", "Tag", (c.rx("Item", 780), 1), (0.5, 0), "", "0..*", "0..*",
           pontos=[(780, y_filhos), (930, y_filhos)])
    c.liga("dependencia", "Foto", "SituacaoFoto", (0.5, 1), (0.5, 0))
    return c.d


def diagrama_classes_b():
    c = Classes("Classes social e moderação", {
        "Usuario": (["UUID id", "String nomeUsuario", "SituacaoConta situacao"], [], None),
        "Moderador": ([], [], None),
        "Item": ([], [], None),
        "Seguimento": (["DateTime desde"], [], None),
        "Bloqueio": (["DateTime criadoEm"], [], None),
        "Curtida": (["DateTime criadaEm"], [], None),
        "Comentario": (["String texto", "DateTime criadoEm"], ["void excluir(Usuario solicitante)"], None),
        "Notificacao": (["String tipo", "Boolean lida"], ["void marcarComoLida()"], None),
        "Denuncia": (["String motivo", "SituacaoDenuncia situacao", "String justificativa"],
                     ["void arquivar()", "void removerConteudo()"], None),
        "SituacaoDenuncia": (["Pendente", "Arquivada", "ConteudoRemovido", "AutorSuspenso"], [], "enumeration"),
    })
    c.por("Usuario", 540, y=40)
    y_a, y_b = c.y("Usuario", 0.32), c.y("Usuario", 0.72)
    c.por("Seguimento", 140, cy=c.y("Usuario", 0.52))
    c.por("Bloqueio", 940, cy=c.y("Usuario", 0.52))
    c.por("Moderador", 575, y=230)
    c.por("Notificacao", 140, y=230)
    c.por("Curtida", 940, y=230)
    c.por("Denuncia", 540, y=400)
    c.por("SituacaoDenuncia", 140, cy=c.y("Denuncia", 0.5))
    c.por("Comentario", 800, y=400)
    c.por("Item", 1050, cy=c.y("Comentario", 0.5))

    c.liga("simples", "Usuario", "Seguimento", (0, c.ry("Usuario", y_a)), (1, c.ry("Seguimento", y_a)),
           "seguidor", "1", "0..*")
    c.liga("dirigida", "Seguimento", "Usuario", (1, c.ry("Seguimento", y_b)), (0, c.ry("Usuario", y_b)),
           "seguido", "0..*", "1")
    c.liga("simples", "Usuario", "Bloqueio", (1, c.ry("Usuario", y_a)), (0, c.ry("Bloqueio", y_a)),
           "autor", "1", "0..*")
    c.liga("dirigida", "Bloqueio", "Usuario", (0, c.ry("Bloqueio", y_b)), (1, c.ry("Usuario", y_b)),
           "bloqueado", "0..*", "1")
    c.liga("heranca", "Moderador", "Usuario", (0.5, 0), (c.rx("Usuario", 575), 1))
    y_lateral = c.y("Usuario", 0.92)
    c.liga("composicao", "Usuario", "Notificacao", (0, 0.92), (0.5, 0), "", "1", "0..*",
           pontos=[(c.x("Notificacao", 0.5), y_lateral)])
    c.liga("simples", "Usuario", "Curtida", (1, 0.92), (0.5, 0), "", "1", "0..*",
           pontos=[(c.x("Curtida", 0.5), y_lateral)])
    c.liga("dirigida", "Curtida", "Item", (0.5, 1), (0.5, 0), "", "0..*", "1",
           pontos=[(940, 330), (1050, 330)])
    x_reg = c.x("Usuario", 0.1)
    c.liga("simples", "Usuario", "Denuncia", (0.1, 1), (c.rx("Denuncia", x_reg), 0), "registra", "1", "0..*")
    c.liga("simples", "Moderador", "Denuncia", (0.5, 1), (c.rx("Denuncia", 575), 0), "decide", "0..1", "0..*")
    x_esc = c.x("Usuario", 0.9)
    c.liga("simples", "Usuario", "Comentario", (0.9, 1), (0.5, 0), "escreve", "1", "0..*",
           pontos=[(x_esc, 360), (800, 360)])
    c.liga("composicao", "Item", "Comentario", (0, 0.5), (1, 0.5), "", "1", "0..*")
    c.liga("dependencia", "Denuncia", "SituacaoDenuncia", (0, 0.5), (1, 0.5))
    return c.d


def diagrama_classes_c():
    c = Classes("Classes trocas", {
        "Usuario": ([], [], None),
        "Item": ([], [], None),
        "Categoria": ([], [], None),
        "Desejo": (["String nome", "String termos", "Visibilidade visibilidade"], ["Boolean corresponde(Item item)"], None),
        "PropostaTroca": (["UUID id", "SituacaoProposta situacao", "DateTime enviadaEm"],
                          ["void aceitar()", "void recusar()", "void contrapropor(List itens)",
                           "void confirmarRecebimento(Usuario parte)", "void cancelar(String motivo)",
                           "void expirar()"], None),
        "ItemProposta": (["String parte"], [], None),
        "MensagemProposta": (["String texto", "DateTime enviadaEm"], [], None),
        "RegistroSituacao": (["SituacaoProposta situacao", "DateTime data"], [], None),
        "Avaliacao": (["Integer nota", "String comentario"], [], None),
        "SituacaoProposta": (["Pendente", "Aceita", "AguardandoConfirmacao", "Concluida", "Recusada", "Expirada",
                              "Cancelada"], [], "enumeration"),
    })
    # Usuario aparece so pelo nome, mas largo o bastante para separar as duas associacoes
    w_usuario = 240
    c.ids["Usuario"] = c.d.vertice("Usuario", "html=1;whiteSpace=wrap;fontStyle=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;",
                                   560 - w_usuario / 2, 20, w_usuario, 40)
    c.caixas["Usuario"] = (560 - w_usuario / 2, 20, w_usuario, 40)
    c.por("PropostaTroca", 560, y=150)
    c.por("Desejo", 170, y=150)
    c.por("Categoria", 170, y=380)
    c.por("SituacaoProposta", 980, cy=c.y("PropostaTroca", 0.5))
    y_filhos = c.y("PropostaTroca", 1) + 90
    c.por("ItemProposta", 360, y=y_filhos)
    c.por("MensagemProposta", 560, y=y_filhos)
    c.por("RegistroSituacao", 780, y=y_filhos)
    c.por("Avaliacao", 990, y=y_filhos)
    c.por("Item", 360, y=c.y("ItemProposta", 1) + 70)

    c.liga("composicao", "Usuario", "Desejo", (0, 0.5), (0.5, 0), "", "1", "0..*", pontos=[(170, 40)])
    c.liga("dirigida", "Desejo", "Categoria", (0.5, 1), (0.5, 0), "", "0..*", "1")
    x_prop, x_dest = c.x("Usuario", 0.15), c.x("Usuario", 0.85)
    c.liga("simples", "Usuario", "PropostaTroca", (0.15, 1), (c.rx("PropostaTroca", x_prop), 0), "proponente", "1", "0..*")
    c.liga("simples", "Usuario", "PropostaTroca", (0.85, 1), (c.rx("PropostaTroca", x_dest), 0), "destinatário", "1", "0..*")
    y_barra = c.y("PropostaTroca", 1) + 45
    for filho, rel, mult, ajuste in (("ItemProposta", 0.12, "2..*", 0), ("MensagemProposta", 0.5, "0..*", 0),
                                     ("RegistroSituacao", 0.7, "1..*", 18), ("Avaliacao", 0.9, "0..2", -18)):
        x_saida = c.x("PropostaTroca", rel)
        cx_filho = c.x(filho, 0.5)
        pontos = [] if abs(x_saida - cx_filho) < 1 else [(x_saida, y_barra + ajuste), (cx_filho, y_barra + ajuste)]
        c.liga("composicao", "PropostaTroca", filho, (rel, 1), (0.5, 0), "", "1", mult, pontos=pontos)
    c.liga("dirigida", "ItemProposta", "Item", (0.5, 1), (0.5, 0), "", "0..*", "1")
    c.liga("dependencia", "PropostaTroca", "SituacaoProposta", (1, 0.5), (0, 0.5))
    return c.d


# ================================================================ atividades


def diagrama_atividades():
    d = Diagrama("Atividades processo de troca")
    raias = [("Proponente", 250), ("Sistema", 520), ("Destinatário", 250)]
    x_raia, x = {}, 20
    for nome, largura in raias:
        x_raia[nome] = (x, largura)
        x += largura
    topo = 20
    linhas = []  # (altura) de cada linha

    def centro(raia, deslocamento=0.0):
        x0, largura = x_raia[raia]
        return x0 + largura / 2 + deslocamento * largura

    y_atual = [topo + 44]
    nos = {}

    def linha(altura):
        y = y_atual[0]
        y_atual[0] += altura + 26
        linhas.append(altura)
        return y

    def acao(chave, raia, texto, y, deslocamento=0.0, largura=None, altura=36):
        w = largura or min(max(largura_texto(texto) + 36, 120), x_raia[raia][1] - 24)
        linhas_texto = 2 if largura_texto(texto) + 36 > w else 1
        h = altura if linhas_texto == 1 else 48
        nos[chave] = d.vertice(texto, ACAO, centro(raia, deslocamento) - w / 2, y, w, h)
        return y + h

    def inicio(chave, raia, y, deslocamento=0.0):
        nos[chave] = d.vertice("", INICIAL, centro(raia, deslocamento) - 15, y, 30, 30)

    def fim(chave, raia, y, deslocamento=0.0):
        nos[chave] = d.vertice("", FINAL, centro(raia, deslocamento) - 15, y, 30, 30)

    def decisao(chave, raia, texto, y, deslocamento=0.0, w=190, h=64):
        nos[chave] = d.vertice(texto, DECISAO, centro(raia, deslocamento) - w / 2, y, w, h)

    def barra(chave, x0, x1, y):
        nos[chave] = d.vertice("", BARRA, x0, y, x1 - x0, 6)

    # linhas do fluxo
    inicio("inicio", "Proponente", linha(30))
    acao("selecionar", "Proponente", "Selecionar itens do destinatário e itens próprios", linha(48))
    acao("enviar", "Proponente", "Enviar proposta", linha(36))
    decisao("valida", "Sistema", "Proposta atende RN25?", linha(64))
    y = linha(36)
    acao("motivo", "Sistema", "Informar o motivo", y, deslocamento=-0.3)
    fim("fim_invalida", "Proponente", y + 3)
    nos["junta"] = d.vertice("", DECISAO, centro("Sistema") - 20, linha(40), 40, 40)
    acao("registrar", "Sistema", "Registrar proposta como pendente", linha(36))
    acao("notificar", "Sistema", "Notificar a outra parte", linha(36))
    acao("analisar", "Destinatário", "Analisar proposta", linha(36))
    decisao("contra", "Destinatário", "Fazer contraproposta?", linha(64), w=180)
    decisao("resposta", "Sistema", "Resposta", linha(56), w=130, h=56)
    y = linha(48)
    acao("recusa", "Sistema", "Registrar recusa e notificar", y, deslocamento=-0.33, largura=150)
    acao("expira", "Sistema", "Expirar proposta e notificar", y, deslocamento=0.0, largura=150)
    acao("reserva", "Sistema", "Reservar itens envolvidos", y, deslocamento=0.33, largura=150)
    y = linha(30)
    fim("fim_recusa", "Sistema", y, deslocamento=-0.33)
    fim("fim_expira", "Sistema", y)
    x_esq, x_dir = centro("Proponente"), centro("Destinatário")
    barra("fork1", x_esq - 40, x_dir + 40, linha(6))
    y = linha(48)
    acao("envio_p", "Proponente", "Enviar seus itens e confirmar recebimento", y)
    acao("envio_d", "Destinatário", "Enviar seus itens e confirmar recebimento", y)
    barra("join1", x_esq - 40, x_dir + 40, linha(6))
    acao("concluir", "Sistema", "Concluir troca e retirar itens trocados da lista de disponíveis", linha(48), largura=300)
    acao("liberar", "Sistema", "Liberar avaliações", linha(36))
    barra("fork2", x_esq - 40, x_dir + 40, linha(6))
    y = linha(36)
    acao("avaliar_p", "Proponente", "Avaliar destinatário", y)
    acao("avaliar_d", "Destinatário", "Avaliar proponente", y)
    barra("join2", x_esq - 40, x_dir + 40, linha(6))
    acao("reputacao", "Sistema", "Atualizar reputação", linha(36))
    fim("fim", "Sistema", linha(30))

    altura_total = y_atual[0] - topo
    for nome, (x0, largura) in x_raia.items():
        d.vertice(nome, RAIA, x0, topo, largura, altura_total)
    # raias ficam atras dos nos
    raias_celulas = d.celulas[-3:]
    del d.celulas[-3:]
    d.celulas[0:0] = raias_celulas

    def f(a, b, rotulo="", saida=None, entrada=None, pontos=()):
        d.aresta(nos[a], nos[b], FLUXO, valor=rotulo, saida=saida, entrada=entrada, pontos=pontos)

    largura_barra = (x_dir + 40) - (x_esq - 40)

    def rel_barra(x):
        return (x - (x_esq - 40)) / largura_barra

    f("inicio", "selecionar")
    f("selecionar", "enviar")
    f("enviar", "valida", entrada=(0.5, 0))
    f("valida", "motivo", "[não]", saida=(0, 0.5), entrada=(0.5, 0))
    f("motivo", "fim_invalida", entrada=(1, 0.5))
    f("valida", "junta", "[sim]", saida=(0.5, 1), entrada=(0.5, 0))
    f("junta", "registrar")
    f("registrar", "notificar")
    f("notificar", "analisar", saida=(1, 0.5), entrada=(0.5, 0))
    f("analisar", "contra")
    x_retorno = x_raia["Destinatário"][0] + x_raia["Destinatário"][1] - 14
    f("contra", "junta", "[sim]", saida=(1, 0.5), entrada=(1, 0.5), pontos=[(x_retorno, 0), (x_retorno, 0)])
    f("contra", "resposta", "[não]", saida=(0.5, 1), entrada=(0.5, 0))
    f("resposta", "recusa", "[recusar]", saida=(0, 0.5), entrada=(0.5, 0))
    f("resposta", "expira", "[7 dias sem resposta]", saida=(0.5, 1), entrada=(0.5, 0))
    f("resposta", "reserva", "[aceitar]", saida=(1, 0.5), entrada=(0.5, 0))
    f("recusa", "fim_recusa")
    f("expira", "fim_expira")
    f("reserva", "fork1", entrada=(rel_barra(centro("Sistema", 0.33)), 0))
    f("fork1", "envio_p", saida=(rel_barra(x_esq), 1), entrada=(0.5, 0))
    f("fork1", "envio_d", saida=(rel_barra(x_dir), 1), entrada=(0.5, 0))
    f("envio_p", "join1", entrada=(rel_barra(x_esq), 0))
    f("envio_d", "join1", entrada=(rel_barra(x_dir), 0))
    f("join1", "concluir", saida=(rel_barra(centro("Sistema")), 1))
    f("concluir", "liberar")
    f("liberar", "fork2", entrada=(rel_barra(centro("Sistema")), 0))
    f("fork2", "avaliar_p", saida=(rel_barra(x_esq), 1), entrada=(0.5, 0))
    f("fork2", "avaliar_d", saida=(rel_barra(x_dir), 1), entrada=(0.5, 0))
    f("avaliar_p", "join2", entrada=(rel_barra(x_esq), 0))
    f("avaliar_d", "join2", entrada=(rel_barra(x_dir), 0))
    f("join2", "reputacao", saida=(rel_barra(centro("Sistema")), 1))
    f("reputacao", "fim")

    # o laco de contraproposta sobe pela borda direita ate a juncao
    geo = {c["id"]: c for c in d.celulas}
    junta = geo[nos["junta"]]["geo"]
    contra = geo[nos["contra"]]["geo"]
    for c in d.celulas:
        if c["tipo"] == "a" and c["origem"] == nos["contra"] and c["destino"] == nos["junta"]:
            c["pontos"] = [(x_retorno, contra[1] + contra[3] / 2), (x_retorno, junta[1] + junta[3] / 2)]
    return d


# ================================================================ sequencia


def diagrama_sequencia():
    d = Diagrama("Sequência cadastro de item com fotos")
    participantes = [
        ("C", "Colecionador", "participant=umlActor;"),
        ("UI", "Interface Web", "participant=umlBoundary;"),
        ("S", "Servidor Next.js", "participant=umlControl;"),
        ("A", "Armazenamento S3", "participant=umlEntity;"),
        ("DB", "PostgreSQL", ""),
        ("F", "Fila de Tarefas", ""),
        ("P", "Processador de Fotos", "participant=umlControl;"),
    ]
    passo, largura, topo = 175, 130, 20
    xs = {chave: 30 + i * passo + largura / 2 for i, (chave, _, _) in enumerate(participantes)}
    y = [topo + 90]
    numero = [0]
    elementos = []

    def msg(a, b, texto, retorno=False, altura=34):
        numero[0] += 1
        y[0] += altura
        rotulo = f"{numero[0]} {texto}"
        elementos.append(("msg", a, b, rotulo, retorno, y[0]))

    def propria(a, texto):
        numero[0] += 1
        y[0] += 30
        elementos.append(("propria", a, None, f"{numero[0]} {texto}", False, y[0]))
        y[0] += 22

    msg("C", "UI", "preencher dados e escolher fotos")
    msg("UI", "S", "gerarUrlsDeEnvio(fotos)")
    propria("S", "validar quantidade, formato e tamanho (RN08)")
    y_alt = y[0] + 18
    y[0] += 34
    msg("S", "UI", "erro de validação", retorno=True)
    msg("UI", "C", "exibir mensagem de erro", retorno=True)
    y_senao = y[0] + 18
    y[0] += 34
    msg("S", "UI", "URLs assinadas", retorno=True)
    y_loop = y[0] + 16
    y[0] += 30
    msg("UI", "A", "enviar foto original")
    msg("A", "UI", "envio confirmado", retorno=True)
    y_fim_loop = y[0] + 16
    y[0] += 16
    msg("UI", "S", "criarItem(dados, chaves das fotos)")
    msg("S", "DB", "gravar item e fotos em processamento")
    msg("DB", "S", "item gravado", retorno=True)
    msg("S", "F", "enfileirar processarFoto")
    msg("S", "UI", "item criado", retorno=True)
    msg("UI", "C", "exibir item em processamento", retorno=True)
    y_ativo = y[0] + 34
    msg("F", "P", "processarFoto(foto)")
    msg("P", "A", "baixar original")
    propria("P", "remover metadados de localização (RN09)")
    propria("P", "gerar variantes de 320, 960 e 1920 pixels")
    msg("P", "A", "gravar variantes")
    msg("P", "DB", "marcar foto como pronta")
    y_fim_ativo = y[0] + 12
    y_fim_alt = y[0] + 26
    altura_total = y_fim_alt + 40 - topo

    for chave, nome, extra in participantes:
        if extra:
            # participante com simbolo UML fica estreito, com o nome abaixo do simbolo
            w = 50 if "Boundary" in extra else 40
            estilo = LINHA_DE_VIDA.replace("size=50;", "size=40;") + extra + "verticalAlign=top;spacingTop=42;whiteSpace=nowrap;"
            d.vertice(nome, estilo, xs[chave] - w / 2, topo, w, altura_total)
        else:
            d.vertice(nome, LINHA_DE_VIDA.replace("size=50;", "size=40;"), xs[chave] - largura / 2, topo + 8, largura, altura_total - 8)
    x_esq, x_dir = xs["C"] - 50, xs["P"] + 90
    d.vertice("alt", QUADRO, x_esq, y_alt, x_dir - x_esq, y_fim_alt - y_alt)
    d.vertice("[fotos inválidas]", TEXTO, x_esq + 66, y_alt, 200, 22)
    d.aresta(None, None, LINHA_TRACEJADA, ponto_origem=(x_esq, y_senao), ponto_destino=(x_dir, y_senao))
    d.vertice("[fotos válidas]", TEXTO, x_esq + 8, y_senao + 2, 200, 22)
    x_loop0, x_loop1 = xs["UI"] - 40, xs["A"] + 60
    d.vertice("loop", QUADRO, x_loop0, y_loop, x_loop1 - x_loop0, y_fim_loop - y_loop)
    d.vertice("[para cada foto]", TEXTO, x_loop0 + 66, y_loop, 200, 22)
    d.vertice("", ATIVACAO, xs["P"] - 5, y_ativo - 6, 10, y_fim_ativo - y_ativo + 6)

    for tipo, a, b, rotulo, retorno, y_m in elementos:
        if tipo == "msg":
            xa = xs[a] + (5 if a == "P" else 0) * (1 if xs[b] > xs[a] else -1)
            xb = xs[b] - (5 if b == "P" else 0) * (1 if xs[b] > xs[a] else -1)
            d.aresta(None, None, RETORNO if retorno else MENSAGEM, valor=rotulo,
                     ponto_origem=(xa, y_m), ponto_destino=(xb, y_m))
        else:
            x0 = xs[a] + (5 if a == "P" else 0)
            d.aresta(None, None, MENSAGEM, ponto_origem=(x0, y_m), ponto_destino=(x0, y_m + 16),
                     pontos=[(x0 + 34, y_m), (x0 + 34, y_m + 16)])
            lado = -1 if a == "P" else 1
            largura_rotulo = largura_texto(rotulo) + 12
            x_rotulo = x0 + 40 if lado > 0 else x0 - 10 - largura_rotulo
            d.vertice(rotulo, TEXTO + "labelBackgroundColor=#FFFFFF;" + ("align=right;" if lado < 0 else ""),
                      x_rotulo, y_m - 4, largura_rotulo, 22)
    return d


# ================================================================ estados


def diagrama_estados():
    d = Diagrama("Estados proposta de troca")
    s = {}

    def estado(chave, nome, x, y, entrada=None, w=200):
        if entrada:
            ident = d.vertice(nome, ESTADO_COMPOSTO, x, y, w, 62)
            d.vertice(f"entry / {entrada}", ESTADO_TEXTO, 0, 30, w, 32, pai=ident)
        else:
            ident = d.vertice(nome, ESTADO, x, y, w, 44)
        s[chave] = ident
        return ident

    s["inicio"] = d.vertice("", INICIAL, 455, 20, 30, 30)
    estado("pendente", "Pendente", 370, 110, "notificar a outra parte")
    estado("recusada", "Recusada", 30, 300, w=150)
    estado("expirada", "Expirada", 220, 300, w=150)
    estado("aceita", "Aceita", 460, 290, "reservar itens")
    estado("cancelada", "Cancelada", 760, 460, "liberar itens reservados", w=210)
    estado("aguardando", "Aguardando Confirmação", 460, 460, w=200)
    estado("concluida", "Concluída", 460, 620, "liberar avaliações")
    s["fim"] = d.vertice("", FINAL, 275, 780, 30, 30)

    def t(a, b, rotulo="", saida=None, entrada=None, pontos=()):
        d.aresta(s[a], s[b], TRANSICAO, valor=rotulo, saida=saida, entrada=entrada, pontos=pontos)

    t("inicio", "pendente", "enviar proposta")
    t("pendente", "pendente", "contrapropor", saida=(0.85, 0), entrada=(1, 0.3), pontos=[(540, 80), (630, 80), (630, 129)])
    t("pendente", "recusada", "recusar", saida=(0, 0.5), entrada=(0.5, 0), pontos=[(105, 141)])
    t("pendente", "expirada", "7 dias sem resposta", saida=(0.25, 1), entrada=(0.5, 0), pontos=[(420, 230), (295, 230)])
    t("pendente", "aceita", "aceitar", saida=(0.75, 1), entrada=(0.5, 0))
    t("pendente", "cancelada", "cancelar [pelo proponente]", saida=(1, 0.8), entrada=(0.5, 0), pontos=[(865, 160)])
    t("aceita", "aguardando", "confirmar recebimento [primeira parte]", saida=(0.5, 1), entrada=(0.5, 0))
    t("aceita", "cancelada", "cancelar [com motivo]", saida=(1, 0.5), entrada=(0.25, 0), pontos=[(812, 321)])
    t("aguardando", "cancelada", "cancelar [com motivo]", saida=(1, 0.5), entrada=(0, 0.35))
    t("aguardando", "concluida", "confirmar recebimento [segunda parte]", saida=(0.5, 1), entrada=(0.5, 0))
    t("recusada", "fim", saida=(0.5, 1), entrada=(0, 0.5), pontos=[(105, 795)])
    t("expirada", "fim", saida=(0.5, 1), entrada=(0.5, 0), pontos=[(295, 700)])
    t("concluida", "fim", saida=(0, 0.5), entrada=(1, 0.5), pontos=[(400, 651), (400, 795)])
    t("cancelada", "fim", saida=(0.5, 1), entrada=(0.5, 1), pontos=[(865, 840), (290, 840)])
    return d


# ================================================================ componentes


def diagrama_componentes():
    d = Diagrama("Componentes Collection Social")
    c, caixas = {}, {}

    def comp(chave, nome, cx, y, w=130, h=48):
        c[chave] = d.vertice(nome, COMPONENTE, cx - w / 2, y, w, h)
        caixas[chave] = (cx - w / 2, y, w, h)

    def pacote(chave, nome, x, y, w, h):
        aba = int(largura_texto(nome, negrito=True)) + 30
        c[chave] = d.vertice(nome, PACOTE.replace("tabWidth=120;", f"tabWidth={aba};"), x, y, w, h)
        caixas[chave] = (x, y, w, h)

    def rx(chave, x):
        return (x - caixas[chave][0]) / caixas[chave][2]

    largura = 1200
    pacote("apresentacao", "Camada de Apresentação", 20, 20, largura, 100)
    pacote("aplicacao", "Camada de Aplicação", 20, 140, largura, 100)
    pacote("negocio", "Camada de Negócio", 20, 260, largura, 330)
    pacote("dados", "Camada de Dados", 20, 610, largura, 140)
    pacote("externos", "Serviços Externos", 20, 770, largura, 100)

    comp("web", "Aplicação Web PWA", 510, 58, 190)
    comp("acoes", "Server Actions e Rotas de API", 510, 178, 240)
    comp("worker", "Processador de Tarefas", 960, 178, 200)

    for chave, cx in (("moderacao", 115), ("social", 290), ("trocas", 465), ("descoberta", 640),
                      ("contas", 815), ("perfis", 990)):
        comp(chave, chave, cx, 305)
    c["inotif"] = d.vertice("INotificacoes", INTERFACE, 200 - 11, 430, 22, 22)
    caixas["inotif"] = (189, 430, 22, 22)
    c["iacervo"] = d.vertice("IAcervo", INTERFACE, 552 - 11, 430, 22, 22)
    caixas["iacervo"] = (541, 430, 22, 22)
    comp("notificacoes", "notificacoes", 200, 510)
    comp("acervo", "acervo", 552, 510)
    comp("midia", "midia", 902, 510)

    comp("repos", "Repositórios Prisma", 400, 660, 200)
    c["pg"] = d.vertice("PostgreSQL", BANCO, 580, 648, 130, 72)
    caixas["pg"] = (580, 648, 130, 72)
    comp("cliente", "Cliente de Armazenamento", 902, 660, 210)
    comp("fila", "Fila Graphile Worker", 1115, 660, 170)

    comp("smtp", "Servidor SMTP", 200, 800, 160)
    comp("s3", "Armazenamento S3", 902, 800, 170)

    def dep(a, b, rotulo="", saida=None, entrada=None, pontos=()):
        d.aresta(c[a], c[b], DEPENDENCIA, valor=rotulo, saida=saida, entrada=entrada, pontos=pontos)

    def fornece(a, b):
        d.aresta(c[a], c[b], "endArrow=none;html=1;rounded=0;strokeColor=#000000;", saida=(0.5, 0), entrada=(0.5, 1))

    def x_de(chave, rel):
        return caixas[chave][0] + rel * caixas[chave][2]

    dep("web", "acoes", "HTTPS", saida=(0.5, 1), entrada=(0.5, 0))
    dep("acoes", "negocio", "chama", saida=(0.5, 1), entrada=(rx("negocio", 510), 0))
    # consumidores chegam as interfaces por trilhos horizontais em alturas diferentes
    for origem, rel, alvo, y_trilho in (("moderacao", 0.5, "inotif", 372), ("social", 0.3, "inotif", 372),
                                        ("trocas", 0.3, "inotif", 390), ("social", 0.7, "iacervo", 408),
                                        ("trocas", 0.7, "iacervo", 372), ("descoberta", 0.5, "iacervo", 372)):
        x0 = x_de(origem, rel)
        x1 = caixas[alvo][0] + 11
        dep(origem, alvo, saida=(rel, 1), entrada=(0.5, 0), pontos=[(x0, y_trilho), (x1, y_trilho)])
    fornece("notificacoes", "inotif")
    fornece("acervo", "iacervo")
    dep("acervo", "midia", saida=(1, 0.5), entrada=(0, 0.5))
    dep("worker", "midia", saida=(rx("worker", 902), 1), entrada=(0.5, 0))
    dep("worker", "fila", "consome", saida=(1, 0.5), entrada=(0.5, 0), pontos=[(1170, 202), (1170, 202)])
    dep("negocio", "repos", "persiste", saida=(rx("negocio", 400), 1), entrada=(0.5, 0))
    dep("repos", "pg", saida=(1, 0.5), entrada=(0, 0.5))
    dep("fila", "pg", saida=(0.5, 1), entrada=(0.5, 1), pontos=[(1115, 735), (645, 735)])
    dep("midia", "cliente", saida=(0.5, 1), entrada=(0.5, 0))
    dep("cliente", "s3", saida=(0.5, 1), entrada=(0.5, 0))
    dep("notificacoes", "smtp", saida=(0.5, 1), entrada=(0.5, 0))
    # a seta do processador para a fila desce pela direita do pacote de negocio
    for cel in d.celulas:
        if cel["tipo"] == "a" and cel["origem"] == c["worker"] and cel["destino"] == c["fila"]:
            cel["pontos"] = [(1115, 202)]
    return d


# ================================================================ objetos


def diagrama_objetos():
    d = Diagrama("Objetos troca aceita")
    o = {}

    def objeto(chave, nome, valores, cx, y):
        w = max([largura_texto(nome)] + [largura_texto(v) for v in valores]) + 28
        h = 26 + 15 * len(valores) + 10
        ident = d.vertice(nome, OBJETO, cx - w / 2, y, w, h)
        d.vertice("<br>".join(v.replace('"', "&quot;") for v in valores), CLASSE_TEXTO, 0, 26, w, h - 26, pai=ident)
        o[chave] = ident

    colunas = [135, 395, 655, 915, 1175]
    objeto("ana", "ana Usuario", ['nomeUsuario = "ana.moedas"', "situacao = Ativa"], colunas[0], 20)
    objeto("prop", "proposta42 PropostaTroca", ["situacao = Aceita", "enviadaEm = 12/10/2026"], colunas[2], 20)
    objeto("bruno", "bruno Usuario", ['nomeUsuario = "bruno_numismata"', "situacao = Ativa"], colunas[4], 20)
    objeto("imperio", "imperio Colecao", ['nome = "Moedas do Império"', "visibilidade = Publica"], colunas[0], 190)
    objeto("ofertado", "ofertado ItemProposta", ['parte = "Proponente"'], colunas[1], 198)
    objeto("pedido", "pedido ItemProposta", ['parte = "Destinatario"'], colunas[3], 198)
    objeto("colonia", "colonia Colecao", ['nome = "Brasil Colônia"', "visibilidade = Publica"], colunas[4], 190)
    objeto("patacao", "patacao Item", ['nome = "Patacão 960 Réis 1815"', "estado = MuitoBom",
                                      "disponivelParaTroca = true"], colunas[1], 350)
    objeto("foto", "fotoPatacao Foto", ["posicao = 1", "situacao = Pronta"], colunas[2], 358)
    objeto("milreis", "milreis Item", ['nome = "1000 Réis 1851"', "estado = Excelente",
                                      "disponivelParaTroca = true"], colunas[3], 350)
    objeto("moedas", "moedas Categoria", ['nome = "Moedas"'], colunas[2], 520)
    y_moedas = 520 + 51 / 2

    def link(a, b, rotulo="", saida=None, entrada=None, pontos=()):
        d.aresta(o[a], o[b], "endArrow=none;html=1;rounded=0;labelBackgroundColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;",
                 valor=rotulo, saida=saida, entrada=entrada, pontos=pontos)

    link("ana", "prop", "proponente", (1, 0.5), (0, 0.5))
    link("bruno", "prop", "destinatário", (0, 0.5), (1, 0.5))
    link("ana", "imperio", saida=(0.5, 1), entrada=(0.5, 0))
    link("bruno", "colonia", saida=(0.5, 1), entrada=(0.5, 0))
    link("prop", "ofertado", saida=(0.25, 1), entrada=(0.5, 0))
    link("prop", "pedido", saida=(0.75, 1), entrada=(0.5, 0))
    link("ofertado", "patacao", saida=(0.5, 1), entrada=(0.5, 0))
    link("pedido", "milreis", saida=(0.5, 1), entrada=(0.5, 0))
    link("imperio", "patacao", saida=(0.8, 1), entrada=(0, 0.35))
    link("colonia", "milreis", saida=(0.2, 1), entrada=(1, 0.35))
    link("patacao", "foto", saida=(1, 0.5), entrada=(0, 0.5))
    # as colecoes contornam os itens por baixo ate a categoria
    link("imperio", "moedas", saida=(0.3, 1), entrada=(0, 0.5), pontos=[(colunas[0] - 50, y_moedas)])
    link("colonia", "moedas", saida=(0.7, 1), entrada=(1, 0.5), pontos=[(colunas[4] + 50, y_moedas)])
    return d


# ================================================================ execucao

DIAGRAMAS = {
    "01a_casos_de_uso_contas_acervo": diagrama_casos_de_uso_a,
    "01b_casos_de_uso_social_trocas": diagrama_casos_de_uso_b,
    "02a_classes_contas_acervo": diagrama_classes_a,
    "02b_classes_social_moderacao": diagrama_classes_b,
    "02c_classes_trocas": diagrama_classes_c,
    "03_atividades_troca": diagrama_atividades,
    "04_sequencia_cadastrar_item": diagrama_sequencia,
    "05_estados_proposta": diagrama_estados,
    "06_componentes": diagrama_componentes,
    "07_objetos_troca": diagrama_objetos,
}


def garantir_webapp():
    """Baixa o webapp oficial do draw.io (pacote npm drawio-offline) para exportar os PNGs."""
    destino = CACHE / f"drawio_{VERSAO_DRAWIO}"
    if (destino / "export3.html").exists():
        return destino
    CACHE.mkdir(exist_ok=True)
    print(f"Baixando o webapp do draw.io {VERSAO_DRAWIO}")
    saida = subprocess.run(["npm", "pack", f"drawio-offline@{VERSAO_DRAWIO}", "--silent"], cwd=CACHE,
                           capture_output=True, text=True, check=True)
    pacote = CACHE / saida.stdout.strip().splitlines()[-1]
    with tarfile.open(pacote) as tar:
        tar.extractall(CACHE / "extraido", filter="data")
    (CACHE / "extraido" / "package").rename(destino)
    pacote.unlink()
    return destino


def exportar_png(arquivos):
    webapp = garantir_webapp()
    ambiente = dict(os.environ)
    raiz_global = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, check=True).stdout.strip()
    ambiente["NODE_PATH"] = raiz_global
    subprocess.run(["node", str(Path(__file__).resolve().parent / "exportar_drawio.cjs"), str(webapp),
                    str(ESCALA_PNG), *map(str, arquivos)], env=ambiente, check=True)


def main():
    escolhidos = [a for a in sys.argv[1:] if a in DIAGRAMAS] or list(DIAGRAMAS)
    arquivos = []
    for nome in escolhidos:
        caminho = PASTA_UML / f"{nome}.drawio"
        DIAGRAMAS[nome]().salvar(caminho)
        arquivos.append(caminho)
        print(f"Gerado {caminho.relative_to(RAIZ)}")
    if "sem_png" not in sys.argv:
        exportar_png(arquivos)


if __name__ == "__main__":
    main()
