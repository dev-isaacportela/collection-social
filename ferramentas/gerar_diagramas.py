"""Gera as imagens PNG dos diagramas UML a partir das fontes em docs/uml.

Baixa o PlantUML do Maven Central na primeira execucao e guarda em
ferramentas/.cache. Requer Java e Graphviz instalados.
"""

import subprocess
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_UML = RAIZ / "docs" / "uml"
CACHE = Path(__file__).resolve().parent / ".cache"
VERSAO = "1.2026.8"
JAR = CACHE / f"plantuml_{VERSAO}.jar"
URL = (
    "https://repo1.maven.org/maven2/net/sourceforge/plantuml/plantuml/"
    f"{VERSAO}/plantuml-{VERSAO}.jar"
)


def garantir_plantuml():
    if JAR.exists():
        return
    CACHE.mkdir(exist_ok=True)
    print(f"Baixando PlantUML {VERSAO}")
    urllib.request.urlretrieve(URL, JAR)


def main():
    garantir_plantuml()
    fontes = sorted(PASTA_UML.glob("*.puml"))
    comando = ["java", "-DPLANTUML_LIMIT_SIZE=16384", "-jar", str(JAR), "-tpng", *map(str, fontes)]
    resultado = subprocess.run(comando, cwd=PASTA_UML)
    if resultado.returncode != 0:
        sys.exit(resultado.returncode)
    for fonte in fontes:
        print(f"Gerado {fonte.with_suffix('.png').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
