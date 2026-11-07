#!/usr/bin/env python3
"""ينزّل صورة كل منتج مرة واحدة ويحفظها مصغّرة (JPEG ≤ 640px) في site/assets/img/p/<slug>.jpg.
الموقع يستخدم النسخة المحلية إن وُجدت (أسرع، ولا تعتمد على CDN خارجي قد يُحجب أو يتأخر)،
وإلا يعود لرابط AliExpress. يحذف النسخ التي لم يعد لمنتجها وجود."""
import csv, io, sys, urllib.request
import concurrent.futures as cf
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "scripts" / "sources.csv"
OUT = ROOT / "site" / "assets" / "img" / "p"
OUT_C = ROOT / "site" / "assets" / "img" / "c"
COURSES = ROOT / "scripts" / "courses.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
CAP = 400


def fetch(slug, url, out=None):
    out = out or OUT
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        im = Image.open(io.BytesIO(data))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((640, 640))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True, progressive=True)
        (out / f"{slug}.jpg").write_bytes(buf.getvalue())
        return slug, True, len(buf.getvalue())
    except Exception as e:
        return slug, False, type(e).__name__


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8", newline="")))
    slugs = {r["id"] for r in rows}
    removed = 0
    for f in OUT.glob("*.jpg"):
        if f.stem not in slugs:
            f.unlink(); removed += 1
    todo = [(r["id"], r["image"]) for r in rows if not (OUT / f"{r['id']}.jpg").exists()][:CAP]
    ok = bad = size = 0
    with cf.ThreadPoolExecutor(8) as ex:
        for slug, good, info in ex.map(lambda a: fetch(*a), todo):
            if good: ok += 1; size += info
            else: bad += 1; print("FAILED", slug, info)
    if COURSES.exists():
        import json
        OUT_C.mkdir(parents=True, exist_ok=True)
        cs = json.loads(COURSES.read_text(encoding="utf-8"))["courses"]
        ids = {c["id"] for c in cs}
        for f in OUT_C.glob("*.jpg"):
            if f.stem not in ids: f.unlink()
        todo_c = [(c["id"], c["image"], OUT_C) for c in cs if not (OUT_C / f"{c['id']}.jpg").exists()][:CAP]
        okc = 0
        with cf.ThreadPoolExecutor(8) as ex:
            for slug, good, info in ex.map(lambda a: fetch(*a), todo_c):
                if good: okc += 1
                else: print("FAILED course", slug, info)
        print(f"cache_images: courses downloaded {okc}/{len(todo_c)}")
    print(f"cache_images: downloaded {ok} ({size // 1024} KB), failed {bad}, removed {removed}, total local {len(list(OUT.glob('*.jpg')))}/{len(rows)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("cache_images FATAL", repr(e)); sys.exit(0)
