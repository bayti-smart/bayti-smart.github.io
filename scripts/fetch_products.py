#!/usr/bin/env python3
"""
سكربت تحديث المنتجات لموقع الأفيليت.

الوضع الافتراضي: يقرأ منتجات من ملف scripts/sources.csv (تضيفه أنت يدويًا
بروابط الأفيليت الحقيقية) ويحوّله إلى products.json — هذا يعمل فورًا
بدون أي API مدفوع أو تسجيل.

خيار متقدم (اختياري لاحقًا): استبدل دالة load_from_csv() بدالة تستدعي
API رسمي مثل AliExpress Affiliate API أو Amazon Product Advertising API
بعد التسجيل المجاني في برنامج العمولة الخاص بهما. تركنا أماكن جاهزة
(TODO) بالأسفل لتفعيل ذلك متى صار لديك مفاتيح API.
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
    "lighting": "إضاءة ذكية",
    "security": "أمان ومراقبة",
    "climate": "تحكم بالمناخ",
    "audio": "صوتيات",
}

# قيمة تُكتب في عمود image بملف sources.csv كتذكير للمستخدم؛ إذا تُركت
# كما هي أو تُركت فارغة، نولّد صورة SVG بديلة تلقائيًا بدل كسر الموقع.
PLACEHOLDER_MARKER = "PASTE_REAL_PRODUCT_IMAGE_URL_HERE"


def svg_placeholder(label, color="#177E75"):
    svg = f'''<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>
<rect width='400' height='400' fill='#F1EFE7'/>
<circle cx='200' cy='160' r='55' fill='none' stroke='{color}' stroke-width='6'/>
<path d='M170 190 L200 150 L230 190 Z' fill='{color}'/>
<circle cx='185' cy='140' r='10' fill='{color}'/>
<text x='200' y='260' font-family='sans-serif' font-size='20' fill='#3C5064' text-anchor='middle'>{label}</text>
</svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def resolve_image(raw_value, category):
    value = (raw_value or "").strip()
    if not value or value == PLACEHOLDER_MARKER:
        return svg_placeholder(CATEGORY_LABELS.get(category, category))
    return value


def load_from_csv():
    """يقرأ المنتجات من ملف CSV بسيط تحرره يدويًا أو تصدّره من لوحة
    تحكم برنامج العمولة (معظمها يوفر تصدير CSV لمنتجاتك المفضّلة)."""
    if not SOURCES_CSV.exists():
        print(f"لم يتم العثور على {SOURCES_CSV} — لا تحديث.")
        return None

    products = []
    with open(SOURCES_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                "id": row["id"],
                "title": row["title"],
                "category": row["category"],
                "price": float(row["price"]),
                "currency": row.get("currency", "USD"),
                "rating": float(row.get("rating", 0) or 0),
                "reviews_count": int(row.get("reviews_count", 0) or 0),
                "image": resolve_image(row.get("image"), row["category"]),
                "description": row.get("description", ""),
                "affiliate_url": row["affiliate_url"],
                "network": row.get("network", ""),
                "tags": [t.strip() for t in row.get("tags", "").split("|") if t.strip()],
            })
    return products


# TODO (اختياري): جلب من AliExpress Affiliate API
# سجّل في https://portals.aliexpress.com/ (مجاني)، ثم استبدل هذه الدالة:
#
# def load_from_aliexpress_api():
#     import requests
#     API_KEY = os.environ["ALIEXPRESS_APP_KEY"]
#     API_SECRET = os.environ["ALIEXPRESS_APP_SECRET"]
#     resp = requests.get("https://api-sg.aliexpress.com/sync", params={...})
#     ...
#     return products

# TODO (اختياري): جلب من Amazon Product Advertising API
# سجّل في https://affiliate-program.amazon.com/ (مجاني بعد أول عملية بيع)
# ثم استخدم مكتبة python-amazon-paapi أو requests مباشرة مع التوقيع المطلوب.


def build_categories(products):
    seen = {}
    for p in products:
        seen.setdefault(p["category"], p["category"])
    # حافظ على أسماء الفئات الافتراضية إن وُجدت، وإلا استخدم المعرف كاسم
    default_names = {
        "lighting": "إضاءة ذكية",
        "security": "أمان ومراقبة",
        "climate": "تحكم بالمناخ",
        "audio": "صوتيات",
    }
    return [{"id": cid, "name": default_names.get(cid, cid)} for cid in seen]


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

    print(f"تم تحديث {PRODUCTS_JSON} بعدد {len(products)} منتج.")


if __name__ == "__main__":
    main()
