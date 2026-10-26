#!/usr/bin/env python3
"""Diagnostic: list the Page's latest posts as the API sees them (no posting).
Results go to scripts/fb_post_log.txt. Needs FB_PAGE_ID and FB_PAGE_TOKEN."""
import datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

GRAPH = "https://graph.facebook.com/v26.0"
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "fb_post_log.txt")
page_id, token = os.environ.get("FB_PAGE_ID", ""), os.environ.get("FB_PAGE_TOKEN", "")
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def log(line):
    line = line.replace(token, "***") if token else line
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get(path, **params):
    url = f"{GRAPH}/{path}?" + urllib.parse.urlencode({**params, "access_token": token})
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {}


st, d = get(page_id, fields="name,link,is_published")
log(f"{stamp} CHECK page HTTP {st} " + json.dumps(d.get("error", d), ensure_ascii=False)[:300])
st, d = get(f"{page_id}/posts", fields="id,created_time,is_published,is_hidden,permalink_url,message", limit=5)
if st != 200:
    log(f"{stamp} CHECK posts HTTP {st} " + json.dumps(d.get("error", d), ensure_ascii=False)[:300])
    sys.exit(0)
rows = d.get("data", [])
log(f"{stamp} CHECK posts count={len(rows)}")
for p in rows:
    msg = " ".join((p.get("message") or "").split())[:50]
    log(f"{stamp} CHECK post {p.get('id')} created={p.get('created_time')} published={p.get('is_published')} "
        f"hidden={p.get('is_hidden')} url={p.get('permalink_url')} msg={msg!r}")
