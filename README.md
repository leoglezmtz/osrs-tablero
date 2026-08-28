# Tablero de Vorkath

Tablero de progresión de la cuenta de Old School RuneScape **Leo Glez**. Se ve en cualquier
navegador, incluido el celular.

**En vivo:** https://leoglezmtz.github.io/osrs-tablero/

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `cuerpo.html` | **La fuente.** Todo el contenido y los estilos. Es lo que se edita. |
| `construir.py` | Envuelve `cuerpo.html` en una página completa y escribe `index.html`. |
| `index.html` | **Generado. No editar a mano** — se sobrescribe en cada build. |
| `.nojekyll` | Le dice a GitHub Pages que sirva los archivos tal cual. |

`cuerpo.html` no lleva `<!doctype>`, `<html>` ni `<head>`: solo el contenido. Eso es a
propósito, porque el mismo archivo se publica como artifact de Claude, donde ese envoltorio lo
pone la plataforma. `construir.py` es lo que agrega, para la versión suelta:

- la etiqueta de *viewport*, sin la cual el celular muestra la página diminuta
- el favicon
- un reset mínimo de CSS
- el botón de tema (auto / claro / oscuro), que recuerda tu elección

## Para actualizarlo

```bash
python construir.py
git add -A
git commit -m "actualiza tablero"
git push
```

GitHub Pages lo republica solo en un minuto o dos.

## Notas

**El sitio es público.** Cualquiera con la dirección puede verlo. Lleva una etiqueta `noindex`
para que no salga en Google, pero eso no lo hace privado. Lo que muestra son niveles y quests
de OSRS, que de todos modos son públicos en los hiscores.

**Los datos son una foto fija.** La página trae los números escritos dentro; no consulta nada
al abrirse. Para refrescarlos hay que regenerar `cuerpo.html` con los datos nuevos y volver a
correr el build.
