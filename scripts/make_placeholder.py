def svg_placeholder(label, color="#177E75"):
    svg = f'''<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>
<rect width='400' height='400' fill='#F1EFE7'/>
<circle cx='200' cy='160' r='55' fill='none' stroke='{color}' stroke-width='6'/>
<path d='M170 190 L200 150 L230 190 Z' fill='{color}'/>
<circle cx='185' cy='140' r='10' fill='{color}'/>
<text x='200' y='260' font-family='sans-serif' font-size='20' fill='#3C5064' text-anchor='middle'>{label}</text>
</svg>'''
    import urllib.parse
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

if __name__ == "__main__":
    for label in ["إضاءة ذكية", "أمان ومراقبة", "تحكم بالمناخ", "صوتيات"]:
        print(label, "->", svg_placeholder(label)[:60], "...")
