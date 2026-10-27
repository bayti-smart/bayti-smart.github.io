#!/usr/bin/env python3
"""Delete OLD Page posts through the Graph API (owner-requested cleanup).

Only posts created BEFORE --before are touched, so the automated posts are safe.
Usage: python scripts/fb_cleanup.py --before 2026-10-26T00:00:00+0000 --limit 1
Results go to scripts/fb_post_log.txt. Needs FB_PAGE_ID and FB_PAGE_TOKEN."""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

GRAPH = "https://graph.facebook.com/v26.0"
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "fb_post_log.txt")
page_id, token = os.environ.get("FB_PAGE_ID", ""), os.environ.get("FB_PAGE_TOKEN", "")
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def log(line):
    line = line.replace(token, "***") if token else line
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def call(method, url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method=method), timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {}


def parse_time(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


ap = argparse.ArgumentParser()
ap.add_argument("--before", required=True)
ap.add_argument("--limit", type=int, default=1)
ap.add_argument("--what", default="posts", choices=["posts", "videos", "photos"])
args = ap.parse_args()
cutoff = parse_time(args.before)

# photos in these albums are the Page's profile/cover pictures: never touched
PROTECTED_ALBUMS = {"profile pictures", "cover photos", "timeline photos"}
LISTING = {
    "posts": (f"{page_id}/posts", "id,created_time", {}),
    "videos": (f"{page_id}/videos", "id,created_time", {}),
    "photos": (f"{page_id}/photos", "id,created_time,album{name}", {"type": "uploaded"}),
}
path, fields, extra = LISTING[args.what]
old, skipped, url = [], 0, f"{GRAPH}/{path}?" + urllib.parse.urlencode(
    {"fields": fields, "limit": 100, "access_token": token, **extra})
while url:
    st, d = call("GET", url)
    if st != 200:
        log(f"{stamp} CLEANUP list {args.what} HTTP {st} " + json.dumps(d.get("error", d), ensure_ascii=False)[:300])
        sys.exit(0)
    for p in d.get("data", []):
        if parse_time(p["created_time"]) >= cutoff:
            continue
        album = ((p.get("album") or {}).get("name") or "").lower()
        if args.what == "photos" and album in PROTECTED_ALBUMS:
            skipped += 1
            log(f"{stamp} CLEANUP skip protected photo {p['id']} album={album!r} ({p['created_time'][:10]})")
            continue
        old.append(p)
    url = d.get("paging", {}).get("next")
log(f"{stamp} CLEANUP found {len(old)} old {args.what} (before {args.before}), protected skipped={skipped}; "
    f"will try {min(args.limit, len(old))}")

ok = failed = 0
for p in old[: args.limit]:
    st, d = call("DELETE", f"{GRAPH}/{p['id']}?" + urllib.parse.urlencode({"access_token": token}))
    if st == 200 and d.get("success") is True:
        ok += 1
        log(f"{stamp} CLEANUP deleted {p['id']} ({p['created_time'][:10]})")
    else:
        failed += 1
        log(f"{stamp} CLEANUP FAIL {p['id']} HTTP {st} " + json.dumps(d.get("error", d), ensure_ascii=False)[:300])
        if failed >= 3:
            log(f"{stamp} CLEANUP stopping after 3 failures")
            break
    time.sleep(1)
log(f"{stamp} CLEANUP summary deleted={ok} failed={failed} remaining_old={len(old) - ok}")
