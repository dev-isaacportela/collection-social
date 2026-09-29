"""Verifica que nenhum texto do projeto usa hifen, travessao ou dois pontos.

Confere arquivos Markdown, nomes de arquivos e pastas, rotulos dos diagramas
draw.io e o texto do documento DOCX gerado. Codigo (py, puml, js) fica de fora porque sua sintaxe exige esses
caracteres, conforme o principio VIII da constituicao.
"""

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

RAIZ = Path(__file__).resolve().parent.parent
PROIBIDOS = {"-", "‐", "‑", "‒", "–", "—", "―", "−", ":", "︓", "："}
IGNORAR_PASTAS = {".git", "node_modules", "__pycache__", ".cache"}
# modelo e orientacoes originais da disciplina, usados apenas como entrada
IGNORAR_CAMINHOS = {Path("docs/entrega/modelo")}
EXTENSOES_TEXTO = {".md", ".txt"}
NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def problemas_em(texto):
    for numero, linha in enumerate(texto.splitlines(), start=1):
        achados = sorted({c for c in linha if c in PROIBIDOS})
        if achados:
            yield numero, linha.strip(), achados


def texto_docx(caminho):
    with zipfile.ZipFile(caminho) as z:
        partes = [n for n in z.namelist() if n.startswith("word/") and n.endswith(".xml")]
        linhas = []
        for parte in partes:
            raiz = ElementTree.fromstring(z.read(parte))
            for p in raiz.iter(NS_W + "p"):
                linhas.append("".join(t.text or "" for t in p.iter(NS_W + "t")))
        return "\n".join(linhas)


def texto_drawio(caminho):
    raiz = ElementTree.fromstring(caminho.read_text(encoding="utf8"))
    valores = (c.get("value") or "" for c in raiz.iter("mxCell"))
    return "\n".join(re.sub(r"<[^>]+>", " ", v) for v in valores if v)


def main():
    erros = 0
    for caminho in sorted(RAIZ.rglob("*")):
        relativo = caminho.relative_to(RAIZ)
        if any(parte in IGNORAR_PASTAS for parte in relativo.parts):
            continue
        if any(relativo == c or c in relativo.parents for c in IGNORAR_CAMINHOS):
            continue
        if any(c in PROIBIDOS for c in caminho.name):
            print(f"NOME {relativo}")
            erros += 1
        if caminho.is_file() and caminho.suffix in EXTENSOES_TEXTO:
            conteudo = caminho.read_text(encoding="utf8")
        elif caminho.is_file() and caminho.suffix == ".docx":
            conteudo = texto_docx(caminho)
        elif caminho.is_file() and caminho.suffix == ".drawio":
            conteudo = texto_drawio(caminho)
        else:
            continue
        for numero, linha, achados in problemas_em(conteudo):
            print(f"{relativo} linha {numero} {achados} {linha[:100]}")
            erros += 1
    if erros:
        print(f"\n{erros} ocorrencias encontradas")
        sys.exit(1)
    print("Nenhum hifen, travessao ou dois pontos encontrado")


if __name__ == "__main__":
    main()
