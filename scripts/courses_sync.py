#!/usr/bin/env python3
"""
قسم الدورات: يكتشف تلقائيًا دورات من الكتالوج العام لـCoursera (بلا مفتاح ولا موافقة) ويحدّث scripts/courses.json.

- كل 14 يومًا يمسح الكتالوج كله (نحو 25 ألف دورة) ويحتفظ بما يطابق مواضيع الموقع في scripts/courses_pool.json،
  ويحذف من القائمة أي دورة اختفت من الكتالوج.
- كل يوم يضيف 3 دورات (48 في أول تشغيل) موزعة على المواضيع واللغات، بسقف 150 دورة.
- واجهة Coursera العامة لا تعطي تقييمات، لذا لا نزعم أي تقييم؛ الموقع يذكر ذلك صراحة.
"""
import json, os, random, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURSES = ROOT / "scripts" / "courses.json"
POOL = ROOT / "scripts" / "courses_pool.json"
REPORT = ROOT / "scripts" / "courses_report.txt"
API = "https://api.coursera.org/api/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
LANGS = ["en", "ar", "fr", "es", "de"]
CAP, FIRST_BATCH, DAILY = 150, 48, int(os.environ.get("COURSES_PER_DAY") or 3)
RESCAN_DAYS = 14
LOG = []

TOPICS = {
    "smart-home": r"smart ?home|home automation|internet of things|\biot\b|connected (home|device)|smart (building|device|city)",
    "electronics": r"arduino|raspberry ?pi|embedded|electronics|circuit|microcontroller|robotics|esp32|\bsensors?\b",
    "network-security": r"home network|computer networks?|network fundamentals|networking basics|wi-?fi|cyber ?security (fundamentals|basics|essentials)|online safety|digital privacy",
    "energy": r"solar|renewable energy|energy efficien|energy management|smart grid|photovoltaic|heat pump",
}
BAN = re.compile(r"exam|prep\b|practice test|aws certified|azure|salesforce|tableau|blockchain|crypto|mba|tutorial for|capstone|clinical|nursing|medic", re.I)


def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


def get(path, params, tries=4):
    url = API + path + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            time.sleep(2 * (i + 1))
    return None


def paged(path, fields, limit=100, max_pages=400):
    start, total = 0, None
    for _ in range(max_pages):
        d = get(path, {"limit": limit, "start": start, "fields": fields})
        if d is None:
            return None, False
        for e in d.get("elements", []):
            yield e
        nxt = (d.get("paging") or {}).get("next")
        if not nxt:
            return
        start = int(nxt)
        time.sleep(0.2)


def scan():
    partners = {}
    for p in paged("partners.v1", "name"):
        partners[str(p["id"])] = p.get("name", "")
    pool, seen, n = [], set(), 0
    complete = True
    gen = paged("courses.v1", "name,slug,photoUrl,primaryLanguages,partnerIds,workload,courseType")
    for e in gen:
        n += 1; seen.add(e["id"])
        langs = e.get("primaryLanguages") or []
        name = (e.get("name") or "").strip()
        if not langs or langs[0] not in LANGS or not e.get("photoUrl") or len(name) < 8 or BAN.search(name):
            continue
        if e.get("courseType") not in (None, "v2.ondemand"):
            continue
        low = name.lower()
        for topic, rx in TOPICS.items():
            if re.search(rx, low):
                pids = e.get("partnerIds") or []
                pool.append({"id": e["id"], "slug": e["slug"], "title": name, "image": e["photoUrl"], "lang": langs[0],
                             "partner": partners.get(str(pids[0]), "") if pids else "", "workload": e.get("workload") or "",
                             "topic": topic})
                break
    return pool, seen, n


def main():
    today = datetime.now(timezone.utc).date()
    rng = random.Random(today.toordinal())
    cur = json.loads(COURSES.read_text(encoding="utf-8")) if COURSES.exists() else {"courses": []}
    courses = cur["courses"]
    pool_d = json.loads(POOL.read_text(encoding="utf-8")) if POOL.exists() else {}
    log(f"COURSES {today} existing={len(courses)}")

    stale = (not pool_d) or (today - datetime.strptime(pool_d.get("date", "2000-01-01"), "%Y-%m-%d").date()) > timedelta(days=RESCAN_DAYS)
    if stale:
        log("scanning Coursera catalogue ...")
        pool, seen, n = scan()
        log(f"scanned {n} courses; matched {len(pool)}")
        if n >= 15000:  # مسح مكتمل: احذف ما اختفى
            gone = [c for c in courses if c["id"] not in seen]
            for c in gone: log("  REMOVE (gone from catalogue)", c["id"], c["title"][:60])
            courses = [c for c in courses if c["id"] in seen]
            pool_d = {"date": str(today), "pool": pool}
            POOL.write_text(json.dumps(pool_d, ensure_ascii=False), encoding="utf-8")
        else:
            log("scan incomplete; keeping previous pool and courses")
    pool = pool_d.get("pool", [])

    have = {c["id"] for c in courses}
    want = FIRST_BATCH if not courses else DAILY
    want = max(0, min(want, CAP - len(courses)))
    cand = {}
    for c in pool:
        if c["id"] not in have:
            cand.setdefault((c["topic"], c["lang"]), []).append(c)
    for v in cand.values(): rng.shuffle(v)
    order_l = ["en", "en", "ar", "fr", "es", "de"]
    topics = list(TOPICS)
    added, i = [], 0
    guard = 0
    while len(added) < want and guard < 5000:
        topic = topics[i % len(topics)]; lang = order_l[(i // len(topics)) % len(order_l)]; i += 1; guard += 1
        bucket = cand.get((topic, lang)) or []
        if bucket:
            c = bucket.pop(); c["added"] = str(today); added.append(c)
    for c in added: log(f"ADD [{c['topic']}/{c['lang']}] {c['title'][:70]} — {c['partner']}")
    courses += added
    log(f"RESULT pool={len(pool)} added={len(added)} total={len(courses)}")
    COURSES.write_text(json.dumps({"courses": courses}, ensure_ascii=False, indent=1), encoding="utf-8")
    REPORT.write_text("\n".join(LOG) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("FATAL", repr(e)); REPORT.write_text("\n".join(LOG) + "\n", encoding="utf-8")
