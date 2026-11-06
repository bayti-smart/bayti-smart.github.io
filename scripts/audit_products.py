#!/usr/bin/env python3
"""
تدقيق يومي للمنتجات الحالية: صور، روابط عمولة، توفّر المنتج، السعر، الجودة، التكرار.

AUDIT_MODE = report (يكتب التقرير فقط) | apply (يطبّق التعديلات) | off
ما يفعله في apply:
  - تحديث السعر عند تغيّره أكثر من 3% (ضمن 1–1000 دولار).
  - إصلاح صورة معطوبة بصورة حديثة من الـAPI إن كانت صالحة.
  - حذف المنتج إذا غاب عن الـAPI في تدقيقين من يومين مختلفين (سُحب من المتجر)،
    أو انخفض تقييمه الإيجابي عن 88%، أو تجاوز سعره 1000$، أو تكررت صورته مع منتج أقدم.
  - لا يحذف أكثر من 15% من الكتالوج في تشغيلة واحدة (حماية من عطل API).
يبقى معرّف AliExpress في قائمة known حتى لا يُعاد إضافة المنتج المحذوف.
"""
import csv, io, json, os, re, sys, time, urllib.request, urllib.error
import concurrent.futures as cf
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ae_sync as ae
from ae_util import call_retry

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "scripts" / "sources.csv"
TR_PATH = ROOT / "scripts" / "translations.json"
IDS_PATH = ROOT / "scripts" / "ae_ids.json"
STATE_PATH = ROOT / "scripts" / "ae_state.json"
REPORT_PATH = ROOT / "scripts" / "audit_report.txt"
SITE = "https://bayti-smart.github.io/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleCookieWebKit/537.36 Chrome/120 Safari/537.36".replace("AppleCookieWebKit", "AppleWebKit")
BATCH = 300
MAX_REMOVE_FRAC = 0.15
MIN_RATE_KEEP = 88.0
PRICE_MIN, PRICE_MAX = 1.0, 1000.0

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


def jload(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def fname(url):
    return url.split("?")[0].rsplit("/", 1)[-1]


def check_image(url, referer=None):
    h = {"User-Agent": UA, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8", "Range": "bytes=0-4096"}
    if referer: h["Referer"] = referer
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20) as r:
            ct = r.headers.get("Content-Type", "")
            ok = r.status in (200, 206) and ct.startswith("image/")
            return ok, f"{r.status} {ct}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


def check_link(url):
    op = urllib.request.build_opener(NoRedirect)
    try:
        r = op.open(urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD"), timeout=20)
        return 200 <= r.status < 400, str(r.status)
    except urllib.error.HTTPError as e:
        return 300 <= e.code < 400, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__


def details(pids):
    out, errors = {}, 0
    for i in range(0, len(pids), 10):
        chunk = pids[i:i + 10]
        time.sleep(2)
        st, data = call_retry("aliexpress.affiliate.productdetail.get", {
            "product_ids": ",".join(chunk),
            "fields": "target_sale_price,product_title,product_main_image_url,evaluate_rate,lastest_volume",
            "target_currency": "USD", "target_language": "EN", "tracking_id": ae.TRACK, "country": "DZ"})
        if "error_response" in data or "http_error_body" in data or "exception" in data:
            errors += 1; log("detail error", json.dumps(data, ensure_ascii=False)[:160]); continue
        got = {str(p.get("product_id")) for p in ae.products_of(data)}
        for p in ae.products_of(data):
            out[str(p.get("product_id"))] = p
        out.setdefault("_answered", set()).update(chunk)  # دفعة أجاب عنها الـAPI بلا خطأ
    return out, errors


def main():
    mode = (os.environ.get("AUDIT_MODE") or "apply").lower()
    if mode == "off":
        return
    today = str(datetime.now(timezone.utc).date())
    log(f"AUDIT {today} mode={mode}")

    raw = CSV_PATH.read_bytes().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(raw, newline="")))
    fields = ["id", "category", "price", "currency", "rating", "reviews_count", "image", "affiliate_url", "network"]
    by_slug = {r["id"]: r for r in rows}
    ids_db = jload(IDS_PATH, {"known": [], "added": {}})
    ids_db.setdefault("map", {})
    state = jload(STATE_PATH, {"page": {}, "cursor": 0})
    state.setdefault("audited", {}); state.setdefault("missing", {})
    tr = jload(TR_PATH, {"categories": {}, "products": {}})
    log(f"products in CSV: {len(rows)}")

    # 1) فحص الصور (بدون Referer ومعه) + صيغة الروابط
    def img_job(r):
        a = check_image(r["image"]); b = check_image(r["image"], SITE)
        return r["id"], a, b
    img_bad_noref, img_bad_ref, results = [], [], {}
    with cf.ThreadPoolExecutor(12) as ex:
        for slug, a, b in ex.map(img_job, rows):
            results[slug] = (a, b)
            if not a[0]: img_bad_noref.append((slug, a[1]))
            if not b[0]: img_bad_ref.append((slug, b[1]))
    log(f"IMAGES broken without referer: {len(img_bad_noref)} | with site referer: {len(img_bad_ref)}")
    for s, why in img_bad_noref[:40]: log("  img-bad(noref)", s, why)
    for s, why in img_bad_ref[:40]:
        if s not in dict(img_bad_noref): log("  img-bad(referer-only)", s, why)
    bad_links = [r["id"] for r in rows if not r["affiliate_url"].startswith("https://s.click.aliexpress.com/")]
    log(f"AFFILIATE format bad: {len(bad_links)} {bad_links[:10]}")

    # 2) تكرار الصور (نفس المنتج مدرج مرتين): يبقى الأقدم
    seen, dupes = {}, []
    for r in rows:
        k = fname(r["image"])
        if k in seen: dupes.append((r["id"], seen[k]))
        else: seen[k] = r["id"]
    log(f"DUPLICATE images: {len(dupes)} {dupes[:10]}")

    # 3) روابط العمولة: فحص فعلي لدفعة يومية
    order = sorted(rows, key=lambda r: state["audited"].get(r["id"], ""))
    batch_rows = order[:BATCH]
    with cf.ThreadPoolExecutor(8) as ex:
        link_res = list(ex.map(lambda r: (r["id"],) + check_link(r["affiliate_url"]), batch_rows))
    bad_http = [(s, why) for s, ok, why in link_res if not ok]
    log(f"AFFILIATE live-check {len(link_res)}: bad {len(bad_http)} {bad_http[:10]}")

    if not ae.KEY or not ae.SECRET:
        log("AE keys missing: skipping detail audit"); REPORT_PATH.write_text("\n".join(LOG) + "\n"); return

    # 4) ربط slug ← معرّف AliExpress (مرة واحدة للقديم عبر مطابقة اسم ملف الصورة)
    mapped = ids_db["map"]
    for slug, info in ids_db.get("added", {}).items():
        mapped.setdefault(slug, info["ae_id"])
    unmapped = [s for s in by_slug if s not in mapped]
    if unmapped:
        known_unmapped = [p for p in map(str, ids_db["known"]) if p not in set(mapped.values())][:400]
        det, _ = details(known_unmapped)
        fn2slug = {fname(by_slug[s]["image"]): s for s in unmapped}
        for pid, p in det.items():
            if pid == "_answered": continue
            s = fn2slug.get(fname(p.get("product_main_image_url") or ""))
            if s: mapped[s] = pid
        log(f"mapped {len(unmapped) - len([s for s in unmapped if s not in mapped])} of {len(unmapped)} previously unmapped")

    # 5) تفاصيل الدفعة اليومية
    audit_slugs = [r["id"] for r in batch_rows if r["id"] in mapped]
    pids = [mapped[s] for s in audit_slugs]
    det, errs = details(pids)
    answered = det.pop("_answered", set())
    price_updates, img_fixes, remove = [], [], {}
    for s in audit_slugs:
        pid = mapped[s]; r = by_slug[s]
        state["audited"][s] = today
        if pid in det:
            state["missing"].pop(s, None)
            p = det[pid]
            try: newp = float(p.get("target_sale_price") or 0)
            except Exception: newp = 0
            oldp = float(r["price"] or 0)
            if PRICE_MIN <= newp <= PRICE_MAX and oldp and abs(newp - oldp) / oldp > 0.03:
                price_updates.append((s, oldp, newp))
            elif newp > PRICE_MAX:
                remove[s] = f"price {newp} > {PRICE_MAX}"
            try: rate = float(str(p.get("evaluate_rate") or "").replace("%", ""))
            except Exception: rate = None
            if rate is not None and 0 < rate < MIN_RATE_KEEP:
                remove[s] = f"rating {rate}% < {MIN_RATE_KEEP}%"
            newimg = (p.get("product_main_image_url") or "").strip()
            if newimg and newimg != r["image"] and results.get(s, ((True, ""),))[0][0] is False:
                if check_image(newimg)[0]: img_fixes.append((s, newimg))
        elif pid in answered:
            m = state["missing"].setdefault(s, [])
            if today not in m: m.append(today)
            if len(m) >= 2:
                remove[s] = f"delisted (missing on {m})"
    for slug, keep in dupes:
        remove.setdefault(slug, f"duplicate image of {keep}")
    log(f"DETAIL audit: batch {len(audit_slugs)} | api errors {errs} | missing now {len(state['missing'])}")
    for s, o, n in price_updates: log(f"  price {s}: {o:.2f} -> {n:.2f}")
    for s, u in img_fixes: log(f"  image-fix {s}")
    for s, why in remove.items(): log(f"  REMOVE {s}: {why}")

    cap = max(1, int(len(rows) * MAX_REMOVE_FRAC))
    if len(remove) > cap:
        log(f"SAFETY: {len(remove)} removals exceed cap {cap}; skipping all removals"); remove = {}

    if mode == "apply":
        for s, o, n in price_updates: by_slug[s]["price"] = f"{n:.2f}"
        for s, u in img_fixes:
            by_slug[s]["image"] = u
            (ROOT / "site" / "assets" / "img" / "p" / f"{s}.jpg").unlink(missing_ok=True)  # أعد تخزين الصورة الجديدة
        for s in remove:
            by_slug.pop(s, None); tr["products"].pop(s, None)
            ids_db["map"].pop(s, None); ids_db.get("added", {}).pop(s, None); state["missing"].pop(s, None)
        keep_rows = [by_slug[r["id"]] for r in rows if r["id"] in by_slug]
        buf = io.StringIO(newline="")
        w = csv.writer(buf, lineterminator="\r\n"); w.writerow(fields)
        for r in keep_rows: w.writerow([r[f] for f in fields])
        CSV_PATH.write_bytes(buf.getvalue().encode("utf-8"))
        TR_PATH.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
        IDS_PATH.write_text(json.dumps(ids_db, ensure_ascii=False, indent=1), encoding="utf-8")
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"APPLIED: prices {len(price_updates)}, images {len(img_fixes)}, removed {len(remove)}; catalog now {len(keep_rows)}")
    REPORT_PATH.write_text("\n".join(LOG) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("FATAL", repr(e))
        REPORT_PATH.write_text("\n".join(LOG) + "\n", encoding="utf-8")
