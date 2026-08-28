#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Envuelve cuerpo.html en una pagina HTML completa y la guarda como index.html,
que es lo que sirve GitHub Pages.

cuerpo.html es la fuente y es la misma que se publica como artifact. Ahi va solo
el contenido: sin <!doctype>, sin <html>, sin <head>. Este script le pone
alrededor todo lo que una pagina suelta necesita y que el artifact daba gratis:

  - <!doctype> y <html lang="es">
  - la etiqueta de viewport, sin la cual el celular la muestra diminuta
  - un favicon
  - un reset minimo de CSS
  - el boton de tema (auto / claro / oscuro), porque aqui no hay una app
    alrededor que decida el tema por nosotros

Uso:
    python construir.py
"""

import os
import re
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(AQUI, "cuerpo.html")
SALIDA = os.path.join(AQUI, "index.html")

DESCRIPCION = ("Tablero de progresion de la cuenta de OSRS Leo Glez: los tres muros, "
               "las cinco fases y cada nombre propio explicado.")

# Favicon en linea, para no depender de ningun archivo aparte.
_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<text y=".9em" font-size="90">\U0001F409</text></svg>')
FAVICON = "data:image/svg+xml," + urllib.parse.quote(_SVG)

CSS_EXTRA = """
    /* --- reset minimo: el artifact traia uno, una pagina suelta no --- */
    *, *::before, *::after { box-sizing: border-box; }
    html { -webkit-text-size-adjust: 100%; }
    img, svg { max-width: 100%; height: auto; }
    button { font-family: inherit; }

    /* --- boton de tema --- */
    #tema {
      position: fixed;
      top: 14px;
      right: 14px;
      z-index: 80;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 7px 11px;
      background: var(--surface);
      color: var(--ink-2);
      border: 1px solid var(--line);
      cursor: pointer;
      font-family: "IBM Plex Mono", ui-monospace, monospace;
      font-size: 11px;
      letter-spacing: .06em;
      text-transform: uppercase;
      box-shadow: var(--shadow);
    }
    #tema:hover { color: var(--ink); border-color: var(--ink-3); }
    #tema:focus-visible { outline: 2px solid var(--bronze); outline-offset: 2px; }
    @media (max-width: 620px) {
      #tema { top: 8px; right: 8px; padding: 6px 9px; font-size: 10px; }
    }
"""

JS_TEMA = """
  (function () {
    var raiz = document.documentElement;
    var boton = document.getElementById('tema');
    var modos = ['auto', 'light', 'dark'];
    var nombres = { auto: 'Auto', light: 'Claro', dark: 'Oscuro' };
    var actual = 'auto';

    try {
      var guardado = localStorage.getItem('tema');
      if (modos.indexOf(guardado) !== -1) { actual = guardado; }
    } catch (e) { /* navegacion privada: se queda en auto */ }

    function aplicar() {
      if (actual === 'auto') {
        raiz.removeAttribute('data-theme');
      } else {
        raiz.setAttribute('data-theme', actual);
      }
      boton.textContent = 'Tema: ' + nombres[actual];
      boton.setAttribute('aria-label', 'Cambiar tema. Ahora: ' + nombres[actual]);
    }

    boton.addEventListener('click', function () {
      actual = modos[(modos.indexOf(actual) + 1) % modos.length];
      try { localStorage.setItem('tema', actual); } catch (e) {}
      aplicar();
    });

    aplicar();
  })();
"""


def construir():
    with open(FUENTE, encoding="utf-8") as f:
        cuerpo = f.read()

    m = re.search(r"<title>(.*?)</title>", cuerpo, re.S)
    titulo = m.group(1).strip() if m else "Tablero"
    # El <title> vuelve a salir en el <head>, asi que se quita del cuerpo.
    cuerpo = re.sub(r"<title>.*?</title>\s*", "", cuerpo, count=1, flags=re.S)

    # El CSS extra entra al final del <style> que ya trae el cuerpo, para que
    # herede los mismos tokens de color y no haya un segundo sistema.
    corte = cuerpo.rfind("</style>")
    if corte == -1:
        raise SystemExit("cuerpo.html no trae <style>; algo cambio de formato")
    cuerpo = cuerpo[:corte] + CSS_EXTRA + cuerpo[corte:]

    # Los <link> de las fuentes van en el <head>. Dentro del <body> los navegadores
    # los toleran, pero preconnect ahi no es HTML valido y ademas llega tarde.
    enlaces = re.findall(r"<link\b[^>]*>", cuerpo)
    cuerpo = re.sub(r"<link\b[^>]*>\s*", "", cuerpo)

    partes = [
        "<!doctype html>",
        '<html lang="es">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>" + titulo + "</title>",
        '<meta name="description" content="' + DESCRIPCION + '">',
        '<meta name="robots" content="noindex">',
        '<meta name="color-scheme" content="light dark">',
        '<link rel="icon" href="' + FAVICON + '">',
        *enlaces,
        "</head>",
        "<body>",
        '<button id="tema" type="button">Tema</button>',
        cuerpo,
        "<script>" + JS_TEMA + "</script>",
        "</body>",
        "</html>",
        "",
    ]

    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(partes))

    print("index.html generado")
    print("  titulo :", titulo)
    print("  tamano :", os.path.getsize(SALIDA), "bytes")


if __name__ == "__main__":
    construir()
