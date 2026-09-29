"""Biblioteca minima para escrever diagramas UML no formato nativo do draw.io.

Gera arquivos .drawio (mxGraphModel sem compressao) com os estilos das formas
UML da biblioteca padrao do draw.io, para que os diagramas possam ser abertos e
editados diretamente no draw.io ou no diagrams.net.
"""

import html
import re
from pathlib import Path

from PIL import ImageFont

FONTE_REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTE_NEGRITO = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
ALTURA_LINHA = 15
PROIBIDOS = set("-‐‑‒–—―−:")

# ---------------------------------------------------------------- estilos

PRETO = "strokeColor=#000000;fontColor=#000000;"
ATOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" + PRETO
CASO_DE_USO = "ellipse;whiteSpace=wrap;html=1;" + PRETO
SISTEMA = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fillColor=none;spacingTop=4;" + PRETO
PACOTE = ("shape=folder;fontStyle=1;spacingTop=10;tabWidth=120;tabHeight=18;tabPosition=left;html=1;"
          "whiteSpace=wrap;verticalAlign=top;align=left;spacingLeft=8;fillColor=#FFFFFF;" + PRETO)
ASSOCIACAO = "endArrow=none;html=1;" + PRETO
INCLUDE = "endArrow=open;endSize=12;dashed=1;html=1;labelBackgroundColor=#FFFFFF;" + PRETO
GENERALIZACAO = "endArrow=block;endSize=16;endFill=0;html=1;" + PRETO

CLASSE = ("swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;"
          "startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;"
          "marginBottom=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;" + PRETO)
CLASSE_TEXTO = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;"
                "overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;"
                "html=1;fontColor=#000000;")
CLASSE_LINHA = ("line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=1;spacingLeft=3;"
                "spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#000000;")
CLASSE_SO_NOME = "html=1;whiteSpace=wrap;fontStyle=1;fillColor=#FFFFFF;" + PRETO
OBJETO = CLASSE.replace("fontStyle=1;", "fontStyle=4;")

COMPOSICAO = ("endArrow=none;startArrow=diamondThin;startFill=1;startSize=16;html=1;rounded=0;"
              "edgeStyle=orthogonalEdgeStyle;" + PRETO)
AGREGACAO = COMPOSICAO.replace("startFill=1;", "startFill=0;")
ASSOCIACAO_DIRIGIDA = "endArrow=open;endSize=12;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;" + PRETO
ASSOCIACAO_SIMPLES = "endArrow=none;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;" + PRETO
HERANCA = "endArrow=block;endSize=16;endFill=0;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;" + PRETO
DEPENDENCIA = ("endArrow=open;endSize=12;dashed=1;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;"
               "labelBackgroundColor=#FFFFFF;" + PRETO)
ROTULO_EXTREMO = "edgeLabel;resizable=0;html=1;labelBackgroundColor=#FFFFFF;fontSize=11;fontColor=#000000;"

INICIAL = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;"
FINAL = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
ACAO = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#FFFFFF;" + PRETO
DECISAO = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontSize=11;" + PRETO
BARRA = "html=1;points=[];fillColor=#000000;strokeColor=#000000;"
FLUXO = ("edgeStyle=orthogonalEdgeStyle;html=1;verticalAlign=bottom;endArrow=open;endSize=8;rounded=0;"
         "labelBackgroundColor=#FFFFFF;" + PRETO)
RAIA = "swimlane;html=1;startSize=26;horizontal=1;fillColor=none;swimlaneFillColor=none;" + PRETO

ESTADO = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#FFFFFF;" + PRETO
ESTADO_COMPOSTO = ("swimlane;fontStyle=0;align=center;verticalAlign=middle;childLayout=stackLayout;horizontal=1;"
                   "startSize=30;horizontalStack=0;resizeParent=0;resizeLast=1;container=0;collapsible=0;"
                   "rounded=1;arcSize=30;fillColor=#FFFFFF;swimlaneFillColor=#FFFFFF;dropTarget=0;" + PRETO)
ESTADO_TEXTO = "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;spacingLeft=4;fontColor=#000000;"
TRANSICAO = "html=1;verticalAlign=bottom;endArrow=open;endSize=8;rounded=0;labelBackgroundColor=#FFFFFF;" + PRETO

COMPONENTE = "shape=module;align=left;spacingLeft=20;align=center;verticalAlign=middle;whiteSpace=wrap;html=1;fillColor=#FFFFFF;jettyWidth=10;jettyHeight=8;" + PRETO
INTERFACE = "ellipse;html=1;verticalLabelPosition=bottom;verticalAlign=top;labelBackgroundColor=#FFFFFF;fillColor=#FFFFFF;" + PRETO
BANCO = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#FFFFFF;" + PRETO
NUVEM = "ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#FFFFFF;verticalAlign=top;fontStyle=1;spacingTop=18;" + PRETO

LINHA_DE_VIDA = ("shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;dropTarget=0;"
                 "collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;size=50;"
                 "fillColor=#FFFFFF;" + PRETO)
ATIVACAO = "html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;targetShapes=umlLifeline;portConstraint=eastwest;fillColor=#FFFFFF;" + PRETO
MENSAGEM = "html=1;verticalAlign=bottom;endArrow=block;endSize=8;rounded=0;labelBackgroundColor=#FFFFFF;" + PRETO
RETORNO = "html=1;verticalAlign=bottom;endArrow=open;dashed=1;endSize=8;rounded=0;labelBackgroundColor=#FFFFFF;" + PRETO
QUADRO = "shape=umlFrame;whiteSpace=wrap;html=1;pointerEvents=0;width=60;height=22;fillColor=none;fontStyle=1;" + PRETO
TEXTO = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontColor=#000000;"
LINHA_TRACEJADA = "endArrow=none;dashed=1;html=1;" + PRETO


def largura_texto(texto, tamanho=12, negrito=False):
    fonte = ImageFont.truetype(FONTE_NEGRITO if negrito else FONTE_REGULAR, tamanho)
    return max((fonte.getlength(linha) for linha in texto.split("\n")), default=0)


def texto_puro(valor):
    return re.sub(r"<[^>]+>", " ", valor)


# ---------------------------------------------------------------- modelo


class Diagrama:
    def __init__(self, nome):
        self.nome = nome
        self.celulas = []
        self.contador = 1

    def _novo_id(self):
        self.contador += 1
        return f"c{self.contador}"

    def _verificar(self, valor):
        achados = PROIBIDOS & set(texto_puro(valor))
        if achados:
            raise ValueError(f"Texto com caractere proibido {sorted(achados)} em {valor!r} no diagrama {self.nome}")

    def vertice(self, valor, estilo, x, y, w, h, pai="1"):
        self._verificar(valor)
        ident = self._novo_id()
        self.celulas.append({"tipo": "v", "id": ident, "valor": valor, "estilo": estilo, "pai": pai,
                             "geo": (round(x), round(y), round(w), round(h))})
        return ident

    def aresta(self, origem, destino, estilo, valor="", pontos=(), pai="1", ponto_origem=None,
               ponto_destino=None, saida=None, entrada=None, rotulo_origem=None, rotulo_destino=None):
        """saida e entrada sao pares (x, y) relativos a caixa da origem e do destino."""
        self._verificar(valor)
        ident = self._novo_id()
        if saida:
            estilo += f"exitX={saida[0]:.4f};exitY={saida[1]:.4f};exitDx=0;exitDy=0;exitPerimeter=0;"
        if entrada:
            estilo += f"entryX={entrada[0]:.4f};entryY={entrada[1]:.4f};entryDx=0;entryDy=0;entryPerimeter=0;"
        self.celulas.append({"tipo": "a", "id": ident, "valor": valor, "estilo": estilo, "pai": pai,
                             "origem": origem, "destino": destino, "pontos": [tuple(map(round, p)) for p in pontos],
                             "ponto_origem": ponto_origem, "ponto_destino": ponto_destino})
        for texto, lado, ponta in ((rotulo_origem, -1, saida), (rotulo_destino, 1, entrada)):
            if texto:
                self._verificar(texto)
                self.celulas.append({"tipo": "r", "id": self._novo_id(), "valor": texto,
                                     "estilo": ROTULO_EXTREMO + "align=center;verticalAlign=middle;",
                                     "pai": ident, "x": lado, "deslocamento": deslocamento_rotulo(ponta)})
        return ident

    def xml(self):
        partes = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        for c in self.celulas:
            valor = html.escape(c["valor"], quote=True)
            estilo = html.escape(c["estilo"], quote=True)
            if c["tipo"] == "v":
                x, y, w, h = c["geo"]
                partes.append(f'<mxCell id="{c["id"]}" value="{valor}" style="{estilo}" vertex="1" parent="{c["pai"]}">'
                              f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
            elif c["tipo"] == "r":
                partes.append(f'<mxCell id="{c["id"]}" value="{valor}" style="{estilo}" vertex="1" connectable="0" '
                              f'parent="{c["pai"]}"><mxGeometry x="{c["x"]}" relative="1" as="geometry">'
                              f'<mxPoint x="{c["deslocamento"][0]}" y="{c["deslocamento"][1]}" as="offset"/></mxGeometry></mxCell>')
            else:
                ligacoes = ""
                if c["origem"]:
                    ligacoes += f' source="{c["origem"]}"'
                if c["destino"]:
                    ligacoes += f' target="{c["destino"]}"'
                geo = ""
                if c["ponto_origem"]:
                    geo += f'<mxPoint x="{round(c["ponto_origem"][0])}" y="{round(c["ponto_origem"][1])}" as="sourcePoint"/>'
                if c["ponto_destino"]:
                    geo += f'<mxPoint x="{round(c["ponto_destino"][0])}" y="{round(c["ponto_destino"][1])}" as="targetPoint"/>'
                if c["pontos"]:
                    geo += '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in c["pontos"]) + "</Array>"
                partes.append(f'<mxCell id="{c["id"]}" value="{valor}" style="{estilo}" edge="1" parent="{c["pai"]}"{ligacoes}>'
                              f'<mxGeometry relative="1" as="geometry">{geo}</mxGeometry></mxCell>')
        corpo = "".join(partes)
        nome = html.escape(self.nome, quote=True)
        return ('<mxfile host="Electron" type="device">'
                f'<diagram id="{re.sub(r"[^a-z0-9]", "_", self.nome.lower())}" name="{nome}">'
                '<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
                'fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">'
                f"<root>{corpo}</root></mxGraphModel></diagram></mxfile>\n")

    def salvar(self, caminho):
        Path(caminho).write_text(self.xml(), encoding="utf8")


# ---------------------------------------------------------------- classes


def dimensoes_classe(nome, atributos, metodos, estereotipo=None):
    titulo = f"«{estereotipo}»\n{nome}" if estereotipo else nome
    largura = max([largura_texto(titulo, negrito=True)] + [largura_texto(t) for t in atributos + metodos]) + 24
    cabecalho = 40 if estereotipo else 26
    altura = cabecalho
    if atributos:
        altura += ALTURA_LINHA * len(atributos) + 10
    if metodos:
        altura += 8 + ALTURA_LINHA * len(metodos) + 10
    return max(largura, 90), max(altura, 30)


def classe(diagrama, nome, atributos, metodos, x, y, w, h, estereotipo=None, estilo=CLASSE):
    if not atributos and not metodos:
        return diagrama.vertice(nome, CLASSE_SO_NOME, x, y, w, h)
    titulo = f"«{estereotipo}»<br>{nome}" if estereotipo else nome
    cabecalho = 40 if estereotipo else 26
    ident = diagrama.vertice(titulo, estilo.replace("startSize=26;", f"startSize={cabecalho};"), x, y, w, h)
    topo = cabecalho
    if atributos:
        altura = ALTURA_LINHA * len(atributos) + 10
        diagrama.vertice("<br>".join(html.escape(a) for a in atributos), CLASSE_TEXTO, 0, topo, w, altura, pai=ident)
        topo += altura
    if metodos:
        diagrama.vertice("", CLASSE_LINHA, 0, topo, w, 8, pai=ident)
        topo += 8
        diagrama.vertice("<br>".join(html.escape(m) for m in metodos), CLASSE_TEXTO, 0, topo, w, ALTURA_LINHA * len(metodos) + 10, pai=ident)
    return ident


# ---------------------------------------------------------------- posicionamento


def deslocamento_rotulo(ponta):
    """Desloca o rotulo de multiplicidade para fora da caixa, conforme o lado da ligacao."""
    if not ponta:
        return (10, -10)
    x, y = ponta
    if y >= 1:
        return (14, 12)
    if y <= 0:
        return (14, -12)
    if x >= 1:
        return (16, -10)
    return (-16, -10)
