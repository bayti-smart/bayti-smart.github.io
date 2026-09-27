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
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_CSV = ROOT / "scripts" / "sources.csv"
PRODUCTS_JSON = ROOT / "products.json"


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
                "image": row["image"],
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
