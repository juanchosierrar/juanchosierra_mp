#!/usr/bin/env python3
"""Genera una página HTML estática por cada artículo publicado del blog
(blog/<slug>.html) y el sitemap.xml, leyendo los artículos de Supabase.

Así Google, WhatsApp, LinkedIn y Facebook ven el título, la descripción,
la imagen y el texto de cada artículo sin ejecutar JavaScript.

Lo ejecuta automáticamente la GitHub Action .github/workflows/blog.yml.
Uso manual:  python3 scripts/generar_blog.py [posts.json]
(si se pasa un JSON con los artículos, no consulta Supabase).
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://juanchosierrar.com"
SB_URL = "https://kliiibzabizzadhduhxw.supabase.co"
SB_KEY = "sb_publishable__cQ8uYNpBBes0HYNn5hS2w_Ejag1f-1"  # clave pública (solo lee artículos publicados)
OG_DEFAULT = f"{SITE}/img/og-juanchosierra.jpg"
CATS = {"ia": "IA & Tech", "gis": "GIS y Mapas", "video": "Video Blog"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
WA = "https://wa.me/573214322340?text=" + urllib.request.quote(
    "Hola Juancho, leí tu blog y quiero agendar una llamada.")


def obtener_posts():
    if len(sys.argv) > 1:
        return json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    url = (f"{SB_URL}/rest/v1/posts_blog?select=titulo,slug,categoria,resumen,contenido_html,"
           "portada_url,created_at,updated_at&publicado=eq.true&order=created_at.desc")
    req = urllib.request.Request(url, headers={"apikey": SB_KEY, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fecha(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def texto_plano(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()


def recortar(t, n=155):
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def a(v):
    return html.escape(v or "", quote=True)


PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo_doc}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{url}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="author" content="Juancho Sierra" />
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png" />
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png" />
<meta name="theme-color" content="#101318" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Juancho Sierra" />
<meta property="og:locale" content="es_CO" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{titulo}" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="{imagen}" />{og_img_dims}
<meta property="article:published_time" content="{publicado}" />
<meta property="article:modified_time" content="{modificado}" />
<meta property="article:author" content="{site}/" />
<meta property="article:section" content="{categoria}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@juanchosierrar" />
<meta name="twitter:title" content="{titulo}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{imagen}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{ld}
</script>
<style>
  html {{ scroll-behavior: smooth; }}
  body {{ margin: 0; background: #101318; color: #F1EEE7; font-family: 'Instrument Sans', sans-serif; -webkit-font-smoothing: antialiased; }}
  a {{ color: #E9A13B; text-decoration: none; }}
  a:hover {{ color: #F5B65C; }}
  ::selection {{ background: #E9A13B; color: #101318; }}
  header {{ position: sticky; top: 0; z-index: 50; background: rgba(16,19,24,.85); backdrop-filter: blur(14px); border-bottom: 1px solid rgba(255,255,255,.07); }}
  header nav {{ max-width: 1180px; margin: 0 auto; padding: 0 28px; height: 68px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }}
  .logo {{ font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 19px; color: #F1EEE7; letter-spacing: -.02em; }}
  .navlinks {{ display: flex; align-items: center; gap: 28px; font-size: 14.5px; font-weight: 500; flex-wrap: wrap; }}
  .navlinks a {{ color: #C4C9D2; }}
  .navlinks a:hover {{ color: #F1EEE7; }}
  .cta {{ background: #E9A13B; color: #16130C !important; font-weight: 600; font-size: 14.5px; padding: 10px 20px; border-radius: 999px; white-space: nowrap; }}
  .cta:hover {{ background: #F5B65C; }}
  main {{ max-width: 760px; margin: 0 auto; padding: 48px 28px 100px; }}
  .migas {{ font-size: 13.5px; color: #8B92A0; margin-bottom: 26px; }}
  .migas a {{ color: #8B92A0; }}
  .migas a:hover {{ color: #E9A13B; }}
  .badge {{ display: inline-block; font-size: 12.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #E9A13B; margin-bottom: 14px; }}
  h1.titulo {{ font-family: 'Space Grotesk', sans-serif; font-size: clamp(30px, 4.4vw, 46px); letter-spacing: -.02em; line-height: 1.12; margin: 0 0 14px; font-weight: 700; }}
  .fecha {{ font-size: 14px; color: #8B92A0; margin-bottom: 30px; }}
  .portada {{ width: 100%; height: auto; border-radius: 20px; border: 1px solid rgba(255,255,255,.1); margin: 0 0 34px; display: block; }}
  .contenido {{ font-size: 17px; line-height: 1.75; color: #C9CED8; }}
  .contenido h2 {{ font-family: 'Space Grotesk', sans-serif; font-size: 27px; letter-spacing: -.015em; color: #F1EEE7; margin: 40px 0 14px; font-weight: 700; }}
  .contenido h3 {{ font-family: 'Space Grotesk', sans-serif; font-size: 21px; color: #F1EEE7; margin: 32px 0 12px; font-weight: 600; }}
  .contenido p {{ margin: 0 0 18px; }}
  .contenido img {{ max-width: 100%; height: auto; border-radius: 14px; border: 1px solid rgba(255,255,255,.1); }}
  .contenido blockquote {{ margin: 26px 0; padding: 4px 0 4px 20px; border-left: 3px solid #E9A13B; color: #D8DCE3; font-style: italic; }}
  .contenido ul, .contenido ol {{ margin: 0 0 18px; padding-left: 26px; }}
  .contenido li {{ margin-bottom: 8px; }}
  .contenido strong {{ color: #F1EEE7; }}
  .autor {{ display: flex; gap: 18px; align-items: center; margin-top: 52px; padding: 24px; background: #171B22; border: 1px solid rgba(255,255,255,.07); border-radius: 20px; }}
  .autor img {{ width: 72px; height: 72px; border-radius: 50%; object-fit: cover; flex: none; border: 1px solid rgba(255,255,255,.1); }}
  .autor p {{ margin: 4px 0 12px; font-size: 14.5px; line-height: 1.55; color: #A6ADB8; }}
  .volver {{ display: inline-block; margin-top: 36px; border: 1px solid rgba(255,255,255,.18); color: #F1EEE7; font-weight: 600; font-size: 15px; padding: 12px 24px; border-radius: 999px; }}
  .volver:hover {{ border-color: #E9A13B; color: #E9A13B; }}
  footer {{ border-top: 1px solid rgba(255,255,255,.07); background: #0C0F13; }}
  footer .inner {{ max-width: 1180px; margin: 0 auto; padding: 36px 28px; display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; font-size: 13.5px; color: #6E7683; }}
</style>
</head>
<body>
<header>
  <nav>
    <a href="/" class="logo">Juancho<span style="color:#E9A13B">Sierra</span></a>
    <div class="navlinks">
      <a href="/">Inicio</a>
      <a href="/Blog.dc.html" style="color:#E9A13B">Blog</a>
      <a href="/#contacto">Contacto</a>
    </div>
    <a class="cta" href="{wa}" target="_blank" rel="noopener">Hablemos →</a>
  </nav>
</header>

<main>
  <nav class="migas" aria-label="Ruta"><a href="/">Inicio</a> › <a href="/Blog.dc.html">Blog</a> › {categoria}</nav>
  <article>
    <div class="badge">{categoria}</div>
    <h1 class="titulo">{titulo}</h1>
    <div class="fecha">Por Juancho Sierra · <time datetime="{publicado}">{fecha_txt}</time></div>
    {portada}
    <div class="contenido">
{contenido}
    </div>
  </article>
  <aside class="autor">
    <img src="/img/perfil.webp" alt="Juancho Sierra" width="72" height="72" loading="lazy" />
    <div>
      <strong>Juancho Sierra</strong>
      <p>Consultor y formador en IA, datos y GIS. Ayudo a equipos de toda LATAM a usar la IA Generativa de verdad en su trabajo.</p>
      <a href="{wa}" target="_blank" rel="noopener">Agendar una llamada →</a>
    </div>
  </aside>
  <a class="volver" href="/Blog.dc.html">← Volver al blog</a>
</main>

<footer>
  <div class="inner">
    <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:17px;color:#F1EEE7">Juancho<span style="color:#E9A13B">Sierra</span></div>
    <div>Consultor en IA, Datos y GIS · Colombia → LATAM</div>
    <div>© {anio} Juancho Sierra. Todos los derechos reservados.</div>
  </div>
</footer>
</body>
</html>
"""


def pagina(p):
    slug = p["slug"]
    url = f"{SITE}/blog/{slug}.html"
    creado, modificado = fecha(p["created_at"]), fecha(p.get("updated_at") or p["created_at"])
    desc = recortar(p.get("resumen") or texto_plano(p.get("contenido_html")))
    cat = CATS.get(p.get("categoria"), "Blog")
    imagen = p.get("portada_url") or OG_DEFAULT
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": f"{url}#articulo",
                "mainEntityOfPage": url,
                "headline": p["titulo"][:110],
                "description": desc,
                "image": imagen,
                "datePublished": creado.isoformat(),
                "dateModified": modificado.isoformat(),
                "inLanguage": "es",
                "articleSection": cat,
                "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Juancho Sierra", "url": f"{SITE}/"},
                "publisher": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Juancho Sierra", "url": f"{SITE}/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/Blog.dc.html"},
                    {"@type": "ListItem", "position": 3, "name": p["titulo"], "item": url},
                ],
            },
        ],
    }
    portada = ""
    if p.get("portada_url"):
        portada = f'<img class="portada" src="{a(p["portada_url"])}" alt="{a(p["titulo"])}" fetchpriority="high" />'
    return PLANTILLA.format(
        titulo_doc=html.escape(f'{p["titulo"]} | Blog de Juancho Sierra'),
        titulo=html.escape(p["titulo"]), desc=a(desc), url=url, imagen=a(imagen),
        og_img_dims="" if p.get("portada_url") else
        '\n<meta property="og:image:width" content="1200" />\n<meta property="og:image:height" content="630" />',
        publicado=creado.isoformat(), modificado=modificado.isoformat(), site=SITE,
        categoria=html.escape(cat), fecha_txt=f"{creado.day} de {MESES[creado.month - 1]} de {creado.year}",
        portada=portada, contenido=p.get("contenido_html") or "", wa=a(WA), anio=datetime.now().year,
        ld=json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/"),
    )


def sitemap(posts):
    urls = [(f"{SITE}/", None), (f"{SITE}/Blog.dc.html", posts[0]["updated_at"] if posts else None)]
    urls += [(f"{SITE}/blog/{p['slug']}.html", p.get("updated_at") or p["created_at"]) for p in posts]
    filas = []
    for loc, mod in urls:
        lm = f"\n    <lastmod>{fecha(mod).date().isoformat()}</lastmod>" if mod else ""
        filas.append(f"  <url>\n    <loc>{loc}</loc>{lm}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(filas) + "\n</urlset>\n")


def main():
    posts = [p for p in obtener_posts() if re.fullmatch(r"[a-z0-9-]+", p.get("slug") or "")]
    carpeta = ROOT / "blog"
    carpeta.mkdir(exist_ok=True)
    vigentes = set()
    for p in posts:
        destino = carpeta / f"{p['slug']}.html"
        destino.write_text(pagina(p), encoding="utf-8")
        vigentes.add(destino.name)
    for viejo in carpeta.glob("*.html"):  # artículos despublicados o borrados
        if viejo.name not in vigentes:
            viejo.unlink()
    (ROOT / "sitemap.xml").write_text(sitemap(posts), encoding="utf-8")
    print(f"{len(posts)} artículo(s) generados; sitemap con {len(posts) + 2} URL")


if __name__ == "__main__":
    main()
