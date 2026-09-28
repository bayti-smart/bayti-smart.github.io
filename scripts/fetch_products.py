#!/usr/bin/env python3
"""
سكربت تحديث المنتجات لموقع الأفيليت (ثنائي اللغة: عربي/إنجليزي).

يقرأ scripts/sources.csv ويبني products.json بهيكل i18n لكل منتج.
أعمدة اللغة: title_ar, title_en, description_ar, description_en,
tags_ar, tags_en (الوسوم مفصولة بـ |).

إذا تركت أي عمود EN فارغًا، سيُستخدم النص العربي كبديل مؤقت بدل
كسر الموقع، لحين ترجمته.
"""

import csv
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_CSV = ROOT / "scripts" / "sources.csv"
PRODUCTS_JSON = ROOT / "products.json"

CATEGORY_LABELS = {
    "lighting": {"ar": "إضاءة ذكية", "en": "Smart Lighting"},
    "security": {"ar": "أمان ومراقبة", "en": "Security"},
    "power": {"ar": "مقابس وطاقة", "en": "Smart Plugs"},
    "audio": {"ar": "صوتيات", "en": "Audio"},
}

PLACEHOLDER_MARKER = "PASTE_REAL_PRODUCT_IMAGE_URL_HERE"
CONFIG_PATH = ROOT / "affiliate.config.json"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


CONFIG = load_config()


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
        label = CATEGORY_LABELS.get(category, {}).get("en", category)
        return svg_placeholder(label)
    return value


def split_tags(raw):
    return [t.strip() for t in (raw or "").split("|") if t.strip()]


def load_from_csv():
    if not SOURCES_CSV.exists():
        print(f"لم يتم العثور على {SOURCES_CSV} — لا تحديث.")
        return None

    products = []
    with open(SOURCES_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title_ar = row["title_ar"]
            title_en = row.get("title_en", "").strip() or title_ar
            desc_ar = row.get("description_ar", "")
            desc_en = row.get("description_en", "").strip() or desc_ar
            tags_ar = split_tags(row.get("tags_ar", ""))
            tags_en = split_tags(row.get("tags_en", "")) or tags_ar

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
                "i18n": {
                    "ar": {"title": title_ar, "description": desc_ar, "tags": tags_ar},
                    "en": {"title": title_en, "description": desc_en, "tags": tags_en},
                },
            })
    return products


def build_categories(products):
    seen = []
    for p in products:
        if p["category"] not in seen:
            seen.append(p["category"])
    return [
        {"id": cid, "name": CATEGORY_LABELS.get(cid, {"ar": cid, "en": cid})}
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
        "categories": build_categories(products),
        "products": products,
    }

    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"تم تحديث {PRODUCTS_JSON} بعدد {len(products)} منتج (عربي/إنجليزي).")


if __name__ == "__main__":
    main()
