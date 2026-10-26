#!/usr/bin/env python3
"""Daily English post to the Facebook Page "Smart Casa".

Alternates day by day between a product post (photo + short caption + link to
the product card on the site) and a buying-guide tip (+ link to the guide).
Selection is deterministic from the date, so no state file is needed.

Secrets (environment): FB_PAGE_ID, FB_PAGE_TOKEN. Never printed or logged.
Usage: python scripts/post_facebook.py [--dry-run] [--kind auto|product|guide] [--date YYYY-MM-DD]
"""
import argparse
import datetime
import json
import os
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

GRAPH = "https://graph.facebook.com/v26.0"
SITE = "https://bayti-smart.github.io"
EPOCH = datetime.date(2026, 10, 26)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(ROOT, "scripts", "fb_post_log.txt")
DISCLOSURE = ("Affiliate disclosure: some links on our site earn us a small "
              "commission at no extra cost to you.")

# Mirrors GUIDE_RULES in script.js (first matching rule wins)
GUIDE_RULES = [
    (r"zigbee", "zigbee"),
    (r"camera|doorbell", "cameras"),
    (r"bulb|lamp-holder", "bulbs"),
    (r"plug|power-strip", "plugs"),
    (r"din-rail|switch|curtain|dimmer|gigabit|breaker|boiler|relay|ups|ceiling-fan", "electrical"),
    (r"sensor|detector|thermometer", "sensors"),
    (r"garden|watering|soil|grow", "garden"),
]

GUIDES = [
    ("bulbs", "💡 Buying smart bulbs? Check this first",
     "Before you order, check two things: your mains voltage (120 or 230 V) and the bulb "
     "base (E27, E14, B22 or E26). A bulb made for 120 V must never go on 230 V mains. "
     "Also remember that many Wi-Fi bulbs only work on 2.4 GHz networks."),
    ("cameras", "📷 Choosing a security camera",
     "A microSD card records locally, while cloud storage usually needs a subscription, so "
     "know which one you're buying. 1080p is enough for many homes and 2K shows more detail. "
     "Point the camera at your own property only, set a strong password and keep the "
     "firmware updated."),
    ("plugs", "🔌 Smart plug basics",
     "Match the plug shape and voltage to your country: many US plugs are 120 V type A/B, "
     "while much of Europe and North Africa uses 230 V type C/F. Never exceed the maximum "
     "load printed on the plug, and don't put a standard smart plug on a heater or air "
     "conditioner unless it is explicitly rated for it."),
    ("zigbee", "📡 Zigbee or Wi-Fi?",
     "Wi-Fi devices connect straight to your router and need no gateway, but many only work "
     "on 2.4 GHz and lots of devices can burden a home router. Zigbee devices need a separate "
     "gateway and suit battery-powered sensors and buttons. With only two or three devices, "
     "Wi-Fi is simpler. Many products come in both versions under the same name, so check the "
     "product page."),
    ("sensors", "🌡️ Smart home sensors, placed right",
     "Keep temperature and humidity sensors away from direct sun and hot appliances. Put leak "
     "sensors near sinks, water heaters and washing machines. Push soil sensors into the root "
     "zone, not the surface. Smoke and gas sensors are a useful extra, not a replacement for "
     "approved alarms."),
    ("garden", "🌱 Smart watering tips",
     "Check your hose or pipe connector size before buying a water valve, since you may need "
     "adapters. Outdoor electronics need shelter from sun and rain unless an explicit rating "
     "such as IP65 is stated, and solar lights need a spot that gets most of the day's sun."),
    ("electrical", "⚡ When to call an electrician",
     "Wired-in switches and modules are not a casual DIY job. Switch off the main breaker "
     "before working, check whether a switch needs a neutral wire before buying, and leave "
     "panel-mounted devices such as DIN rail energy meters to a qualified electrician, "
     "especially at high loads. Never exceed the load printed on a device."),
]


def load_products():
    with open(os.path.join(ROOT, "products.json"), encoding="utf-8") as f:
        items = json.load(f)["products"]
    items = [p for p in items if p.get("image") and p.get("i18n", {}).get("en", {}).get("title")]
    items.sort(key=lambda p: p["id"])
    random.Random(7).shuffle(items)  # fixed seed: mixes categories, stable order
    return items


def guide_for(pid):
    for pattern, gid in GUIDE_RULES:
        if re.search(pattern, pid):
            return gid
    return None


def trim(text, limit):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def pick(kind, today, products):
    n = (today - EPOCH).days
    if kind == "auto":
        kind = "product" if n % 2 == 0 else "guide"
    k = max(n, 0) // 2
    if kind == "product":
        p = products[k % len(products)]
        en = p["i18n"]["en"]
        msg = (
            f"🏠 {trim(en['title'], 110)}\n\n"
            f"{trim(en.get('description', ''), 300)}\n\n"
            f"👉 See it on Smart Casa: {SITE}/?lang=en#p-{p['id']}\n\n"
            f"{DISCLOSURE}\n\n#SmartHome #HomeAutomation"
        )
        return {"kind": "product", "id": p["id"], "message": msg, "image": p["image"]}
    gid, headline, body = GUIDES[k % len(GUIDES)]
    related = [p for p in products if guide_for(p["id"]) == gid]
    image = related[k % len(related)]["image"] if related else None
    msg = (
        f"{headline}\n\n{body}\n\n"
        f"📖 Read the full guide: {SITE}/guides.html?lang=en#{gid}\n\n"
        f"{DISCLOSURE}\n\n#SmartHome #HomeAutomation"
    )
    return {"kind": "guide", "id": gid, "message": msg, "image": image}


def http(req, timeout=60):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def download_image(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SmartCasaBot/1.0)",
        "Accept": "image/jpeg,image/png,image/*;q=0.8"})
    status, data, headers = http(req, 30)
    ctype = (headers.get("Content-Type") or "").split(";")[0].strip().lower()
    if status != 200 or ctype not in ("image/jpeg", "image/png", "image/gif") or not (1000 < len(data) < 8_000_000):
        raise RuntimeError(f"image not usable (status={status}, type={ctype}, bytes={len(data)})")
    return data, ctype


def multipart(fields, data, ctype):
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n'.encode()
                     + str(v).encode("utf-8") + b"\r\n")
    ext = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif"}[ctype]
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="source"; '
                 f'filename="post.{ext}"\r\nContent-Type: {ctype}\r\n\r\n'.encode() + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def graph_post(path, fields, image=None):
    url = f"{GRAPH}/{path}"
    if image:
        body, ctype = multipart(fields, *image)
        req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": ctype})
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(fields).encode(), method="POST")
    status, raw, _ = http(req)
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = {"raw": raw[:200].decode("utf-8", "replace")}
    return status, payload


def log(line):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--kind", default="auto", choices=["auto", "product", "guide"])
    ap.add_argument("--date", help="YYYY-MM-DD (testing)")
    args = ap.parse_args()

    today = datetime.date.fromisoformat(args.date) if args.date else datetime.datetime.now(datetime.timezone.utc).date()
    post = pick(args.kind, today, load_products())
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"[{post['kind']}] {post['id']}")
    print(post["message"])
    print(f"image: {post['image']}")
    if args.dry_run:
        print("DRY RUN: nothing was posted.")
        log(f"{stamp} DRY {post['kind']} {post['id']}")
        return 0

    page_id, token = os.environ.get("FB_PAGE_ID", ""), os.environ.get("FB_PAGE_TOKEN", "")
    if not page_id or not token:
        log(f"{stamp} ERROR {post['kind']} {post['id']} missing FB_PAGE_ID/FB_PAGE_TOKEN")
        print("ERROR: missing FB_PAGE_ID or FB_PAGE_TOKEN", file=sys.stderr)
        return 1

    fields = {"message": post["message"], "access_token": token}
    image = None
    if post["image"]:
        try:
            image = download_image(post["image"])
        except Exception as e:  # fall back to a text post
            print(f"WARN: {e}; posting text only")
    if image:
        status, payload = graph_post(f"{page_id}/photos", {**fields, "published": "true"}, image)
    else:
        status, payload = graph_post(f"{page_id}/feed", fields)

    if status == 200 and ("post_id" in payload or "id" in payload):
        pid = payload.get("post_id") or payload.get("id")
        print(f"OK post_id={pid}")
        log(f"{stamp} OK {post['kind']} {post['id']} post_id={pid} {'photo' if image else 'text'}")
        return 0

    err = json.dumps(payload.get("error", payload), ensure_ascii=False)[:300]
    err = err.replace(token, "***")
    print(f"ERROR HTTP {status}: {err}", file=sys.stderr)
    log(f"{stamp} ERROR {post['kind']} {post['id']} HTTP {status} {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
