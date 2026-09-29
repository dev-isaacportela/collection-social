// Exporta arquivos .drawio para PNG usando o proprio renderizador do draw.io.
//
// Abre a pagina export3.html do webapp oficial (a mesma usada pelo servico de
// exportacao do draw.io) no Chromium do Playwright e captura a imagem.
//
// Uso
//   NODE_PATH=$(npm root -g) node ferramentas/exportar_drawio.cjs <webapp> <escala> <arquivo.drawio>...

const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

const TIPOS = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".xml": "application/xml",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".gif": "image/gif",
  ".txt": "text/plain",
};

function servir(raiz) {
  const servidor = http.createServer((req, res) => {
    const caminho = path.join(raiz, decodeURIComponent(req.url.split("?")[0]));
    if (!caminho.startsWith(raiz) || !fs.existsSync(caminho) || fs.statSync(caminho).isDirectory()) {
      res.writeHead(404);
      res.end();
      return;
    }
    res.writeHead(200, { "Content-Type": TIPOS[path.extname(caminho)] || "application/octet-stream" });
    fs.createReadStream(caminho).pipe(res);
  });
  return new Promise((resolve) => servidor.listen(0, "127.0.0.1", () => resolve(servidor)));
}

async function main() {
  const [webapp, escalaTexto, ...arquivos] = process.argv.slice(2);
  const escala = parseFloat(escalaTexto) || 2;
  const servidor = await servir(path.resolve(webapp));
  const porta = servidor.address().port;
  const navegador = await chromium.launch();
  try {
    for (const arquivo of arquivos) {
      const pagina = await navegador.newPage({ deviceScaleFactor: escala });
      const erros = [];
      pagina.on("pageerror", (e) => erros.push(String(e)));
      await pagina.goto(`http://127.0.0.1:${porta}/export3.html`, { waitUntil: "networkidle" });
      const xml = fs.readFileSync(arquivo, "utf8");
      await pagina.evaluate((dados) => render(dados), {
        xml,
        format: "png",
        border: 12,
        bg: "#ffffff",
        scale: 1,
        w: 0,
        h: 0,
      });
      await pagina.waitForSelector("#LoadingComplete", { state: "attached", timeout: 60000 });
      const limites = JSON.parse(await pagina.$eval("#LoadingComplete", (d) => d.getAttribute("bounds")));
      const largura = Math.ceil(limites.x + limites.width);
      const altura = Math.ceil(limites.y + limites.height);
      await pagina.setViewportSize({ width: largura, height: altura });
      const saida = arquivo.replace(/\.drawio$/, ".png");
      await pagina.screenshot({ path: saida, clip: { x: 0, y: 0, width: largura, height: altura } });
      if (erros.length) console.error(`Avisos em ${arquivo}\n${erros.join("\n")}`);
      console.log(`Gerado ${saida}`);
      await pagina.close();
    }
  } finally {
    await navegador.close();
    servidor.close();
  }
}

main().catch((erro) => {
  console.error(erro);
  process.exit(1);
});
