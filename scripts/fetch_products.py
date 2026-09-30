#!/usr/bin/env python3
"""
سكربت تحديث المنتجات لموقع الأفيليت (5 لغات: عربي، إنجليزي، فرنسي،
إسباني، ألماني).

- scripts/sources.csv: بيانات كل منتج غير النصية (السعر، الصورة، الرابط...)
- scripts/translations.json: نصوص كل منتج بكل اللغات، بالمعرّف (id)

لإضافة منتج جديد: أضف صفًا في sources.csv بنفس id موجود في translations.json
(أو أضف مدخلًا جديدًا هناك بنفس الid).
"""

import csv
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_CSV = ROOT / "scripts" / "sources.csv"
TRANSLATIONS_JSON = ROOT / "scripts" / "translations.json"
PRODUCTS_JSON = ROOT / "products.json"
CONFIG_PATH = ROOT / "affiliate.config.json"

LANGS = ["ar", "en", "fr", "es", "de"]
PLACEHOLDER_MARKER = "PASTE_REAL_PRODUCT_IMAGE_URL_HERE"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


CONFIG = load_config()


def load_translations():
    with open(TRANSLATIONS_JSON, encoding="utf-8") as f:
        return json.load(f)


TRANSLATIONS = load_translations()


def svg_placeholder(label, color="#177E75"):
    svg = f'''<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>
<rect width='400' height='400' fill='#F1EFE7'/>
<circle cx='200' cy='160' r='55' fill='none' stroke='{color}' stroke-width='6'/>
<path d='M170 190 L200 150 L230 190 Z' fill='{color}'/>
<circle cx='185' cy='140' r='10' fill='{color}'/>
<text x='200' y='260' font-family='sans-serif' font-size='18' fill='#3C5064' text-anchor='middle'>{label}</text>
</svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def resolve_image(raw_value, category):
    value = (raw_value or "").strip()
    if not value or value == PLACEHOLDER_MARKER:
        label = TRANSLATIONS["categories"].get(category, {}).get("en", category)
        return svg_placeholder(label)
    return value


def build_affiliate_url(url, network):
    """يضيف معرّف الأفيليت الخاص بك تلقائيًا لروابط Amazon."""
    tag = (CONFIG.get("amazon_tag") or "").strip()
    if network == "amazon" and tag:
        import re
        m = re.search(r"/dp/([A-Z0-9]{10})", url)
        if m:
            domain = CONFIG.get("amazon_domain", "www.amazon.com")
            return f"https://{domain}/dp/{m.group(1)}?tag={tag}"
    return url


def i18n_for(pid):
    entry = TRANSLATIONS["products"].get(pid)
    if not entry:
        return {lang: {"title": pid, "description": "", "tags": []} for lang in LANGS}
    out = {}
    fallback = entry.get("en") or next(iter(entry.values()))
    for lang in LANGS:
        out[lang] = entry.get(lang) or fallback
    return out


def load_from_csv():
    if not SOURCES_CSV.exists():
        print(f"لم يتم العثور على {SOURCES_CSV} — لا تحديث.")
        return None

    products = []
    with open(SOURCES_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                "id": row["id"],
                "category": row["category"],
                "price": float(row.get("price") or 0),
                "currency": row.get("currency", "USD"),
                "rating": float(row.get("rating", 0) or 0),
                "reviews_count": int(row.get("reviews_count", 0) or 0),
                "image": resolve_image(row.get("image"), row["category"]),
                "affiliate_url": build_affiliate_url(row["affiliate_url"], row.get("network", "")),
                "network": row.get("network", ""),
                "i18n": i18n_for(row["id"]),
            })
    return products


def build_categories(products):
    seen = []
    for p in products:
        if p["category"] not in seen:
            seen.append(p["category"])
    return [
        {"id": cid, "name": TRANSLATIONS["categories"].get(cid, {"ar": cid, "en": cid})}
        for cid in seen
    ]


def main():
    products = load_from_csv()
    if products is None:
        print("تم الإبقاء على products.json الحالي بدون تغيير.")
        sys.exit(0)

    if not products:
        print("ملف sources.csv فارغ — لا يوجد منتجات لكتابتها.")
        sys.exit(1)

    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "languages": LANGS,
        "categories": build_categories(products),
        "products": products,
    }

    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"تم تحديث {PRODUCTS_JSON} بعدد {len(products)} منتج ({len(LANGS)} لغات).")


if __name__ == "__main__":
    main()
