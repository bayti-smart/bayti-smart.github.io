#!/usr/bin/env python3
"""
مزامنة بيانات منتجات AliExpress عبر Affiliate API.
الوضع الحالي: فحص فقط (لا يعدّل أي ملف). يطبع في سجل التشغيل ما تُرجعه الواجهة.
المفاتيح تأتي من متغيرات البيئة (أسرار GitHub) ولا تُطبع أبدًا.
"""
import csv, hashlib, hmac, json, os, re, sys, time
import urllib.parse, urllib.request, urllib.error, builtins
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URLS = ROOT / "scripts" / "product_urls.txt"
SOURCES = ROOT / "scripts" / "sources.csv"
GATEWAY = "https://api-sg.aliexpress.com/sync"

KEY = os.environ.get("ALIEXPRESS_APP_KEY", "")
SECRET = os.environ.get("ALIEXPRESS_APP_SECRET", "")
TRACK = os.environ.get("ALIEXPRESS_TRACKING_ID", "default")


def sign(params):
    base = "".join(f"{k}{params[k]}" for k in sorted(params))
    return hmac.new(SECRET.encode(), base.encode(), hashlib.sha256).hexdigest().upper()


def call(method, extra):
    params = {"app_key": KEY, "timestamp": str(int(time.time() * 1000)),
              "sign_method": "sha256", "method": method, **extra}
    params["sign"] = sign(params)
    req = urllib.request.Request(GATEWAY, data=urllib.parse.urlencode(params).encode(),
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, {"http_error_body": e.read().decode("utf-8", "replace")[:600]}
    except Exception as e:
        return 0, {"exception": repr(e)}


def read_urls():
    out = []
    for line in URLS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        url, _, cat = [p.strip() for p in line.partition("|")]
        m = re.search(r"/item/(\d+)", url)
        if m:
            out.append((m.group(1), cat))
    return out


REPORT = []
_orig_print = builtins.print
def print(*a, **k):
    _orig_print(*a, **k)
    REPORT.append(" ".join(str(x) for x in a))


def main():
    if not KEY or not SECRET:
        print("AE: المفاتيح غير متوفرة في البيئة، تخطّي."); return 0
    items = read_urls()
    print(f"AE: عدد المنتجات في product_urls.txt = {len(items)}")
    ids = ",".join(i for i, _ in items)
    status, data = call("aliexpress.affiliate.productdetail.get", {
        "product_ids": ids,
        "fields": "commission_rate,sale_price,target_sale_price,product_title,product_main_image_url,promotion_link,evaluate_rate,lastest_volume,product_detail_url",
        "target_currency": "USD", "target_language": "EN",
        "tracking_id": TRACK, "country": "DZ"})
    print("AE: HTTP", status)
    if "error_response" in data:
        e = data["error_response"]
        print("AE: error_response:", json.dumps({k: e.get(k) for k in ("code", "msg", "sub_code", "sub_msg")}, ensure_ascii=False))
        return 0
    if "http_error_body" in data or "exception" in data:
        print("AE:", json.dumps(data, ensure_ascii=False)[:700]); return 0
    resp = next((v for k, v in data.items() if k.endswith("_response")), data)
    result = (resp or {}).get("resp_result", {})
    print("AE: resp_code =", result.get("resp_code"), "| resp_msg =", result.get("resp_msg"))
    products = (((result.get("result") or {}).get("products") or {}).get("product")) or []
    print("AE: منتجات مُرجَعة =", len(products))
    ours = {}
    if SOURCES.exists():
        with open(SOURCES, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ours[r["id"]] = r.get("price")
    for p in products:
        print("AE: ", json.dumps({
            "id": p.get("product_id"),
            "title": (p.get("product_title") or "")[:60],
            "price_usd": p.get("target_sale_price") or p.get("sale_price"),
            "commission": p.get("commission_rate"),
            "rating_pct": p.get("evaluate_rate"),
            "volume": p.get("lastest_volume"),
            "has_link": bool(p.get("promotion_link")),
            "has_image": bool(p.get("product_main_image_url")),
        }, ensure_ascii=False))
    return 0


def search_mode():
    f = ROOT / "scripts" / "ae_search.txt"
    if not f.exists():
        return
    for kw in [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]:
        status, data = call("aliexpress.affiliate.product.query", {
            "keywords": kw, "page_size": "40", "page_no": "1",
            "sort": "LAST_VOLUME_DESC", "target_currency": "USD", "target_language": "EN",
            "ship_to_country": "DZ", "tracking_id": TRACK,
            "fields": "commission_rate,target_sale_price,product_title,evaluate_rate,lastest_volume,product_id"})
        print(f"AE-SEARCH [{kw}] HTTP {status}")
        if "error_response" in data:
            e = data["error_response"]; print("AE-SEARCH error:", e.get("code"), e.get("msg"), e.get("sub_msg")); continue
        resp = next((v for k, v in data.items() if k.endswith("_response")), data)
        res = (resp or {}).get("resp_result", {})
        prods = (((res.get("result") or {}).get("products") or {}).get("product")) or []
        def pct(x):
            try: return float(str(x).replace("%", ""))
            except Exception: return 0.0
        good = [p for p in prods if pct(p.get("evaluate_rate")) >= 94 and int(p.get("lastest_volume") or 0) >= 500]
        good.sort(key=lambda p: (pct(p.get("commission_rate")), int(p.get("lastest_volume") or 0)), reverse=True)
        print(f"AE-SEARCH   مرجَع={len(prods)} مقبول={len(good)}")
        for p in good[:4]:
            print("AE-SEARCH   ", json.dumps({"id": p.get("product_id"), "title": (p.get("product_title") or "")[:70],
                  "price": p.get("target_sale_price"), "comm": p.get("commission_rate"),
                  "rating_pct": p.get("evaluate_rate"), "sold": p.get("lastest_volume")}, ensure_ascii=False))


if __name__ == "__main__":
    rc = main()
    search_mode()
    (ROOT / "scripts" / "ae_report.txt").write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    sys.exit(rc)
