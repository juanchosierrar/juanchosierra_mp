# Sitio web — Juancho Sierra

Estos son los archivos de tu web (home + blog), listos para subir al repositorio `juanchosierra_mp`.

## Archivos
- `index.html` — página principal (home)
- `Blog.dc.html` — página de blog
- `support.js`, `image-slot.js` — scripts necesarios para que el sitio funcione
- `img/` — imágenes usadas en la web

## Cómo subirlo a GitHub (repo vacío)

Desde una terminal, dentro de esta carpeta descomprimida:

```bash
git init
git remote add origin https://github.com/juanchosierrar/juanchosierra_mp.git
git add .
git commit -m "Primera versión del sitio"
git branch -M main
git push -u origin main
```

Te pedirá tu usuario y un token de acceso personal de GitHub (no tu contraseña) — créalo en GitHub → Settings → Developer settings → Personal access tokens.

## Publicarlo en línea (gratis)
Una vez subido, puedes activarlo con **GitHub Pages**:
1. En el repo, ve a Settings → Pages.
2. Source: rama `main`, carpeta `/root`.
3. Guarda — tu web quedará publicada en `https://juanchosierrar.github.io/juanchosierra_mp/`.

Para futuras actualizaciones: pide los cambios aquí en el chat, descarga de nuevo esta carpeta actualizada, y repite `git add . && git commit -m "actualización" && git push`.
