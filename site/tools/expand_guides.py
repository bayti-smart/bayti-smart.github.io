#!/usr/bin/env python3
"""توسيع الأدلة: يضيف مقدمة وقسم «أخطاء شائعة» و«أسئلة» لكل دليل بالخمس لغات، ويوحّد الألمانية على du.
يعمل مرة واحدة على المحتوى الأصلي (يتخطى أي ملف يحوي <h2> مسبقًا). شغّله من جذر المستودع."""
import html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from guides_data1 import HEAD, G1
from guides_data2 import G2, DE_UL

LANGS = ["en", "ar", "fr", "es", "de"]
G = {**G1, **G2}
ROOT = Path(__file__).resolve().parent.parent / "content" / "guides"
e = lambda s: html.escape(s, quote=False)

for gid, d in G.items():
    for i, lang in enumerate(LANGS):
        p = ROOT / lang / f"{gid}.html"
        old = p.read_text(encoding="utf-8").strip()
        if "<h2>" in old:
            print("skip", p); continue
        ul = DE_UL[gid] if lang == "de" else old
        h = HEAD[lang]
        parts = [f"<p>{e(d['intro'][i])}</p>", f"<h2>{e(h[0])}</h2>", ul,
                 f"<h2>{e(h[1])}</h2>", "<ul>" + "".join(f"<li>{e(x)}</li>" for x in d["mis"][i]) + "</ul>",
                 f"<h2>{e(h[2])}</h2>"]
        for q, a in d["faq"][i]:
            parts += [f"<h3>{e(q)}</h3>", f"<p>{e(a)}</p>"]
        p.write_text("\n".join(parts) + "\n", encoding="utf-8")
        print("wrote", p)
