#!/usr/bin/env python3
"""
إضافة منتجات جديدة تلقائيًا كل يوم (من 5 إلى 20) عبر AliExpress Affiliate API، بلا أي خدمة مدفوعة.

الآلية: كلمات بحث دوّارة (SPECS) ← فرز بالجودة (تقييم ≥ 92% ومبيعات ≥ 200) ← استبعاد المكرر
← جلب رابط العمولة والصورة والسعر ← توليد العنوان والوصف والوسوم بالخمس لغات من قوالب
ثابتة وصادقة (لا ادعاءات خارج عنوان القائمة) ← الكتابة في sources.csv و translations.json.

متغيرات البيئة: ALIEXPRESS_* (أسرار)، AUTO_MIN/AUTO_MAX (افتراضي 5/20)، AUTO_COUNT (تجاوز)،
AUTO_DRY_RUN=true (يكتب التقرير فقط بلا تعديل الملفات).
"""
import csv, json, os, random, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ae_sync as ae
from auto_catalog_data import TYPES, SPECS, MSG, TOKENS, BANNED, LANGS, NEG

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "scripts" / "sources.csv"
TR_PATH = ROOT / "scripts" / "translations.json"
IDS_PATH = ROOT / "scripts" / "ae_ids.json"
STATE_PATH = ROOT / "scripts" / "ae_state.json"
REPORT_PATH = ROOT / "scripts" / "auto_report.txt"

MAX_SEARCHES = 30
MAX_PER_SPEC = 2
MIN_RATE, MIN_SOLD = 92.0, 200
PRICE_MIN, PRICE_MAX = 1.0, 200.0
MAX_PAGE = 5

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def load_json(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def pct(x):
    try: return float(str(x).replace("%", ""))
    except Exception: return 0.0


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


SPEC_TOKENS = [
    (r"\b(\d{1,2}) ?(?:gang|way)\b", lambda m: f"{m.group(1)} Gang"),
    (r"\b(\d{1,3}) ?v\b", lambda m: f"{m.group(1)}V"),
    (r"\b(\d{1,3}) ?w\b", lambda m: f"{m.group(1)}W"),
    (r"\b(\d{1,2}(?:\.\d)?) ?m\b", lambda m: f"{m.group(1)}M"),
    (r"\b(\d{1,2}) ?ch\b", lambda m: f"{m.group(1)}CH"),
    (r"\b(\d{3,5}) ?mah\b", lambda m: f"{m.group(1)}mAh"),
    (r"\b(\d{1,2}) ?(?:pcs|pack)\b", lambda m: f"{m.group(1)}-Pack"),
]


def tokens_for(title):
    low = title.lower()
    out = [name for name, rx in TOKENS if re.search(rx, low)][:3]
    for rx, fmt in SPEC_TOKENS:
        if len(out) >= 4: break
        m = re.search(rx, low)
        if m and fmt(m) not in out: out.append(fmt(m))
    return out


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build_texts(tkey, cat, title_en, cat_names, pid="", used_titles=()):
    slug_base, names, blurbs, warn = TYPES[tkey]
    toks = tokens_for(title_en)
    out = {}
    for i, lang in enumerate(LANGS):
        name = names[i]
        title = f"{name} ({', '.join(toks)})" if toks else name
        parts = [blurbs[i]]
        if toks:
            parts.append(f"{MSG['lead'][i]} {', '.join(toks)}.")
        if "Zigbee" in toks and tkey != "gateway":
            parts.append(MSG["zigbee"][i])
        if warn:
            parts.append(MSG[warn][i])
        parts.append(MSG["check"][i])
        tags = list(toks[:3])
        for extra in (cat_names.get(cat, {}).get(lang, cat), name, "Smart Home", "AliExpress"):
            if len(tags) >= 4: break
            if extra not in tags: tags.append(extra)
        out[lang] = {"title": title, "description": " ".join(parts), "tags": tags[:4]}
    if out["en"]["title"] in used_titles:  # عنوان مكرر: أضف مرجعًا قصيرًا ليبقى كل عنوان فريدًا
        for lang in LANGS:
            out[lang]["title"] += f" · #{pid[-4:]}"
    return slug_base, toks, out


def search(kw, page):
    st, data = ae.call("aliexpress.affiliate.product.query", {
        "keywords": kw, "page_size": "40", "page_no": str(page), "sort": "LAST_VOLUME_DESC",
        "target_currency": "USD", "target_language": "EN", "ship_to_country": "DZ", "tracking_id": ae.TRACK,
        "fields": "commission_rate,target_sale_price,product_title,evaluate_rate,lastest_volume,product_id"})
    if "error_response" in data:
        log("search error", kw, data["error_response"].get("code"), data["error_response"].get("msg")); return None
    if "http_error_body" in data or "exception" in data:
        log("search failed", kw, json.dumps(data, ensure_ascii=False)[:200]); return None
    return ae.products_of(data)


def details(ids):
    got = {}
    for i in range(0, len(ids), 10):
        chunk = ids[i:i + 10]
        time.sleep(1.5)
        st, data = ae.call("aliexpress.affiliate.productdetail.get", {
            "product_ids": ",".join(chunk),
            "fields": "commission_rate,target_sale_price,product_title,product_main_image_url,promotion_link,evaluate_rate,lastest_volume",
            "target_currency": "USD", "target_language": "EN", "tracking_id": ae.TRACK, "country": "DZ"})
        if "error_response" in data:
            log("detail error", data["error_response"].get("code"), data["error_response"].get("msg")); continue
        for p in ae.products_of(data):
            got[str(p.get("product_id"))] = p
    return got


def main():
    dry = os.environ.get("AUTO_DRY_RUN", "").lower() in ("1", "true", "yes")
    today = datetime.now(timezone.utc).date()
    rng = random.Random(today.toordinal())
    lo, hi = int(os.environ.get("AUTO_MIN") or 5), int(os.environ.get("AUTO_MAX") or 20)
    target = int(os.environ.get("AUTO_COUNT") or 0) or rng.randint(lo, hi)
    log(f"AUTO {today} dry={dry} target={target}")

    if not ae.KEY or not ae.SECRET:
        log("AE keys missing, skipping"); return 0

    ids_db = load_json(IDS_PATH, {"known": [], "added": {}})
    known = set(map(str, ids_db["known"]))
    state = load_json(STATE_PATH, {"page": {}, "cursor": 0})
    tr = load_json(TR_PATH, {"categories": {}, "products": {}})
    existing_slugs = set(tr["products"])
    banned = re.compile(BANNED, re.I)

    pool, seen_prefix, searches = [], set(), 0
    n = len(SPECS)
    start = state.get("cursor", 0) % n
    order = [(start + i) % n for i in range(n)]
    last_idx = start
    for idx in order:
        if len(pool) >= target or searches >= MAX_SEARCHES:
            break
        kw, tkey, cat, rx = SPECS[idx]
        page = state["page"].get(kw, 1)
        time.sleep(1.5)
        res = search(kw, page); searches += 1; last_idx = idx
        if res is None:
            continue
        fresh = []
        for p in res:
            pid = str(p.get("product_id"))
            title = clean(p.get("product_title"))
            low = title.lower()
            try: price = float(p.get("target_sale_price") or 0)
            except Exception: price = 0
            if pid in known or pid in {c["pid"] for c in pool}: continue
            if pct(p.get("evaluate_rate")) < MIN_RATE or int(p.get("lastest_volume") or 0) < MIN_SOLD: continue
            if not (PRICE_MIN <= price <= PRICE_MAX): continue
            if banned.search(low) or not re.search(rx, low): continue
            if tkey in NEG and re.search(NEG[tkey], low): continue
            prefix = re.sub(r"[^a-z0-9]", "", low)[:35]
            if prefix in seen_prefix: continue
            fresh.append({"pid": pid, "kw": kw, "tkey": tkey, "cat": cat, "title": title,
                          "sold": int(p.get("lastest_volume") or 0)})
        fresh.sort(key=lambda c: c["sold"], reverse=True)
        take = fresh[:MAX_PER_SPEC]
        for c in take:
            seen_prefix.add(re.sub(r"[^a-z0-9]", "", c["title"].lower())[:35])
            pool.append(c)
        log(f"search [{kw}] p{page}: {len(res)} results, {len(fresh)} fresh, took {len(take)}")
        if not fresh:  # الصفحة مستنفدة: انتقل للتالية في المرة القادمة
            state["page"][kw] = page + 1 if page < MAX_PAGE else 1
    state["cursor"] = (last_idx + 1) % n
    pool = pool[:target]

    added = []
    if pool:
        det = details([c["pid"] for c in pool])
        cat_names = tr.get("categories", {})
        used_titles = {v["en"]["title"] for v in tr["products"].values() if "en" in v}
        for c in pool:
            d = det.get(c["pid"])
            if not d:
                log("no detail for", c["pid"]); continue
            link = clean(d.get("promotion_link")); img = clean(d.get("product_main_image_url"))
            try: price = float(d.get("target_sale_price") or 0)
            except Exception: price = 0
            if not link.startswith("https://s.click.aliexpress.com/"): log("bad link", c["pid"]); continue
            if not img.startswith("https://"): log("bad image", c["pid"]); continue
            if not (PRICE_MIN <= price <= PRICE_MAX): log("bad price", c["pid"]); continue
            slug_base, toks, texts = build_texts(c["tkey"], c["cat"], c["title"], cat_names, c["pid"], used_titles)
            slug = "-".join([slug_base] + [slugify(t) for t in toks[:2]] + [c["pid"][-5:]]).strip("-")
            if slug in existing_slugs: slug += "-" + c["pid"][-8:-5]
            if slug in existing_slugs: log("slug clash", slug); continue
            assert all(len(texts[l]["tags"]) == 4 and texts[l]["title"] and texts[l]["description"] for l in LANGS)
            existing_slugs.add(slug); used_titles.add(texts["en"]["title"])
            added.append({"slug": slug, "pid": c["pid"], "cat": c["cat"], "price": price, "img": img,
                          "link": link, "texts": texts, "src_title": c["title"]})

    for a in added:
        log(f"ADD {a['slug']} | {a['cat']} | ${a['price']:.2f} | {a['src_title'][:60]}")
    log(f"RESULT searches={searches} pool={len(pool)} added={len(added)}")

    if not dry and added:
        raw = CSV_PATH.read_bytes()
        if not raw.endswith(b"\r\n"):
            raw += b"\r\n"
        with open(CSV_PATH, "wb") as f:
            f.write(raw)
        with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\r\n")
            for a in added:
                w.writerow([a["slug"], a["cat"], f"{a['price']:.2f}", "USD", "", 0, a["img"], a["link"], "aliexpress"])
        for a in added:
            tr["products"][a["slug"]] = a["texts"]
            ids_db["known"].append(a["pid"])
            ids_db["added"][a["slug"]] = {"ae_id": a["pid"], "date": str(today), "src_title": a["src_title"][:120]}
        TR_PATH.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
        IDS_PATH.write_text(json.dumps(ids_db, ensure_ascii=False, indent=1), encoding="utf-8")
    if not dry:
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    REPORT_PATH.write_text("\n".join(LOG) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:  # لا يوقف النشر
        log("FATAL", repr(e))
        REPORT_PATH.write_text("\n".join(LOG) + "\n", encoding="utf-8")
        rc = 0
    sys.exit(rc)
