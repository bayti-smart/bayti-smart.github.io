#!/usr/bin/env python3
"""
جلب بيانات منتجات AliExpress عبر Affiliate API (وضع قراءة فقط: لا يعدّل الموقع).
- يقرأ scripts/product_urls.txt ويطبع AE-DETAIL لكل منتج في scripts/ae_report.txt.
- إن وُجد scripts/ae_search.txt يبحث بالكلمات المفتاحية ويطبع المرشحين.
المفاتيح من متغيرات البيئة (أسرار GitHub) ولا تُطبع أبدًا.
"""
import builtins, hashlib, hmac, json, os, re, sys, time
import urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URLS = ROOT / "scripts" / "product_urls.txt"
SEARCH = ROOT / "scripts" / "ae_search.txt"
GATEWAY = "https://api-sg.aliexpress.com/sync"
KEY = os.environ.get("ALIEXPRESS_APP_KEY", "")
SECRET = os.environ.get("ALIEXPRESS_APP_SECRET", "")
TRACK = os.environ.get("ALIEXPRESS_TRACKING_ID", "default")

REPORT = []
_orig_print = builtins.print
def print(*a, **k):
    _orig_print(*a, **k)
    REPORT.append(" ".join(str(x) for x in a))


def sign(params):
    base = "".join(f"{k}{params[k]}" for k in sorted(params))
    return hmac.new(SECRET.encode(), base.encode(), hashlib.sha256).hexdigest().upper()


def _call_once(method, extra):
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


def call(method, extra):
    """يعيد المحاولة تلقائيًا عند تجاوز حد معدل الاستدعاء."""
    for attempt in range(6):
        status, data = _call_once(method, extra)
        err = data.get("error_response") if isinstance(data, dict) else None
        if err and err.get("code") == "ApiCallLimit":
            time.sleep(3 + attempt * 2)
            continue
        return status, data
    return status, data


def products_of(data):
    resp = next((v for k, v in data.items() if k.endswith("_response")), data)
    res = (resp or {}).get("resp_result", {})
    return (((res.get("result") or {}).get("products") or {}).get("product")) or []


def read_urls():
    out = []
    if URLS.exists():
        for line in URLS.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.search(r"/item/(\d+)", line)
            if m:
                out.append(m.group(1))
    return out


def details(ids):
    for i in range(0, len(ids), 10):
        chunk = ids[i:i + 10]
        time.sleep(1.5)
        status, data = call("aliexpress.affiliate.productdetail.get", {
            "product_ids": ",".join(chunk),
            "fields": "commission_rate,target_sale_price,product_title,product_main_image_url,promotion_link,evaluate_rate,lastest_volume",
            "target_currency": "USD", "target_language": "EN", "tracking_id": TRACK, "country": "DZ"})
        if "error_response" in data:
            e = data["error_response"]; print("AE: error", e.get("code"), e.get("msg")); continue
        if "http_error_body" in data or "exception" in data:
            print("AE:", json.dumps(data, ensure_ascii=False)[:400]); continue
        got = products_of(data)
        print(f"AE: دفعة {i // 10 + 1}: طُلب {len(chunk)} وعاد {len(got)}")
        for p in got:
            print("AE-DETAIL", json.dumps({k: p.get(k) for k in (
                "product_id", "product_title", "target_sale_price", "commission_rate",
                "evaluate_rate", "lastest_volume", "product_main_image_url", "promotion_link")}, ensure_ascii=False))


def search_mode():
    if not SEARCH.exists():
        return
    def pct(x):
        try: return float(str(x).replace("%", ""))
        except Exception: return 0.0
    for kw in [l.strip() for l in SEARCH.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]:
        time.sleep(1.5)
        status, data = call("aliexpress.affiliate.product.query", {
            "keywords": kw, "page_size": "40", "page_no": "1", "sort": "LAST_VOLUME_DESC",
            "target_currency": "USD", "target_language": "EN", "ship_to_country": "DZ", "tracking_id": TRACK,
            "fields": "commission_rate,target_sale_price,product_title,evaluate_rate,lastest_volume,product_id"})
        if "error_response" in data:
            e = data["error_response"]; print("AE-SEARCH error:", kw, e.get("code")); continue
        prods = products_of(data)
        good = [p for p in prods if pct(p.get("evaluate_rate")) >= 92 and int(p.get("lastest_volume") or 0) >= 200]
        good.sort(key=lambda p: int(p.get("lastest_volume") or 0), reverse=True)
        print(f"AE-SEARCH [{kw}] مرجَع={len(prods)} مقبول={len(good)}")
        for p in good[:4]:
            print("AE-SEARCH   ", json.dumps({"id": p.get("product_id"), "title": (p.get("product_title") or "")[:70],
                  "price": p.get("target_sale_price"), "comm": p.get("commission_rate"),
                  "rating_pct": p.get("evaluate_rate"), "sold": p.get("lastest_volume")}, ensure_ascii=False))


def main():
    if not KEY or not SECRET:
        print("AE: المفاتيح غير متوفرة في البيئة، تخطّي."); return 0
    ids = read_urls()
    print(f"AE: عدد المنتجات في product_urls.txt = {len(ids)}")
    if ids:
        details(ids)
    search_mode()
    return 0


if __name__ == "__main__":
    rc = main()
    (ROOT / "scripts" / "ae_report.txt").write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    sys.exit(rc)
