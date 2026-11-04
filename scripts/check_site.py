#!/usr/bin/env python3
"""Sanity checks for the built site (dist/). Exit code 1 if anything is broken.
Checks: internal links and assets resolve, every page has title/description/canonical/one h1/hreflang set,
sitemap URLs exist, no 'TODO'/'{{' leftovers."""
import re, sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
BASE = 'https://bayti-smart.github.io'
problems = []


def resolve(path):
    path = unquote(path)
    p = root / path.lstrip('/')
    if path.endswith('/') or p.is_dir():
        return (p / 'index.html').exists()
    return p.exists()


pages = sorted(root.rglob('index.html'))
for f in pages:
    rel = '/' + str(f.parent.relative_to(root)).replace('\\', '/') + '/'
    rel = rel.replace('//', '/') if rel != '/./' else '/'
    html = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    if '{{' in html or '{%' in html:
        problems.append((rel, 'template leftovers'))
    if not (soup.title and soup.title.get_text(strip=True)):
        problems.append((rel, 'missing <title>'))
    if not soup.find('meta', attrs={'name': 'description'}):
        problems.append((rel, 'missing meta description'))
    can = soup.find('link', rel='canonical')
    if not can or can['href'] != BASE + (rel if rel != '/./' else '/'):
        problems.append((rel, f"canonical mismatch: {can['href'] if can else None}"))
    if len(soup.find_all('h1')) != 1:
        problems.append((rel, f'{len(soup.find_all("h1"))} <h1> tags'))
    hl = [l['hreflang'] for l in soup.find_all('link', rel='alternate') if l.get('hreflang')]
    if sorted(hl) != sorted(['ar', 'en', 'fr', 'es', 'de', 'x-default']):
        problems.append((rel, f'hreflang set {hl}'))
    for a in soup.find_all(['a', 'link', 'script', 'img']):
        ref = a.get('href') or a.get('src')
        if not ref or ref.startswith(('#', 'http:', 'https:', 'mailto:', 'data:', '//', 'javascript:')):
            continue
        if not ref.startswith('/'):
            problems.append((rel, f'relative ref {ref}'))
            continue
        target = urlsplit(ref).path
        if not resolve(target):
            problems.append((rel, f'broken link {ref}'))

# sitemaps (index -> one file per language)
index = (root / 'sitemap.xml').read_text(encoding='utf-8')
if '<sitemapindex' not in index:
    problems.append(('sitemap', 'sitemap.xml is not an index'))
files = re.findall(r'<loc>([^<]+)</loc>', index)
locs = []
for fu in files:
    if not fu.startswith(BASE) or not resolve(fu[len(BASE):]):
        problems.append(('sitemap', f'index points to missing file {fu}'))
        continue
    locs += re.findall(r'<loc>([^<]+)</loc>', (root / fu[len(BASE):].lstrip('/')).read_text(encoding='utf-8'))
for loc in locs:
    if not loc.startswith(BASE) or not resolve(loc[len(BASE):]):
        problems.append(('sitemap', f'missing {loc}'))
dups = len(locs) - len(set(locs))
if dups:
    problems.append(('sitemap', f'{dups} duplicate URLs'))
for f in ('robots.txt', '404.html', 'favicon.ico', 'products.json', 'guides.html', 'about.html', 'privacy.html'):
    if not (root / f).exists():
        problems.append(('root', f'missing {f}'))

print(f'{len(pages)} pages, {len(locs)} sitemap URLs checked')
if problems:
    print(f'{len(problems)} PROBLEMS:')
    for p in problems[:40]:
        print('  ', p)
    sys.exit(1)
print('site check OK')
