"""One-off helper: brand images (favicon, apple icon, OG image). Output is committed; not run in CI."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
INK=(15,34,51); INK_UP=(22,50,71); PAPER=(250,249,245); MIST=(169,203,201); AMBER=(240,168,60)
BOLD="/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"; REG="/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"
def mark(size, line=PAPER, ss=4, glow=True):
    S=size*ss; u=S/100; layer=Image.new("RGBA",(S,S),(0,0,0,0))
    if glow:
        g=Image.new("RGBA",(S,S),(0,0,0,0)); gd=ImageDraw.Draw(g); cx,cy=50*u,63*u
        gd.ellipse([cx-30*u,cy-30*u,cx+30*u,cy+30*u],fill=AMBER+(120,)); layer=Image.alpha_composite(layer,g.filter(ImageFilter.GaussianBlur(9*u)))
    d=ImageDraw.Draw(layer); P=[(x*u,y*u) for x,y in [(50,10),(90,45),(90,90),(10,90),(10,45)]]; w=7*u
    for a,b in zip(P,P[1:]+P[:1]): d.line([a,b],fill=line,width=int(round(w)))
    for x,y in P: d.ellipse([x-w/2,y-w/2,x+w/2,y+w/2],fill=line)
    r=12*u; d.ellipse([50*u-r,63*u-r,50*u+r,63*u+r],fill=AMBER)
    return layer.resize((size,size),Image.LANCZOS)
def tile(size, mark_ratio=0.62, radius=0.22):
    bg=Image.new("RGBA",(size,size),INK+(255,)); m=mark(int(size*mark_ratio)); bg.alpha_composite(m,((size-m.width)//2,(size-m.height)//2))
    mask=Image.new("L",(size,size),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,size-1,size-1],radius=int(size*radius),fill=255)
    out=Image.new("RGBA",(size,size),(0,0,0,0)); out.paste(bg,(0,0),mask); return out
out="site/assets/img/"
tile(180,0.64,0.0).convert("RGB").save(out+"apple-touch-icon.png")           # iOS rounds it itself
t=tile(256); t.save(out+"favicon-256.png"); t.resize((48,48),Image.LANCZOS).save(out+"favicon-48.png")
t.save(out+"favicon.ico",sizes=[(16,16),(32,32),(48,48)])
# OG image 1200x630
W,H=1200,630; im=Image.new("RGB",(W,H),INK)
for y in range(H):
    c=tuple(int(INK_UP[i]+(INK[i]-INK_UP[i])*y/H) for i in range(3)); ImageDraw.Draw(im).line([(0,y),(W,y)],fill=c)
im=im.convert("RGBA"); im.alpha_composite(mark(330),(790,150)); d=ImageDraw.Draw(im)
d.text((80,300),"Smart Casa",font=ImageFont.truetype(BOLD,128),fill=PAPER,anchor="ls")
d.text((84,370),"Smart home picks,",font=ImageFont.truetype(REG,48),fill=MIST,anchor="ls")
d.text((84,426),"honest buying guides.",font=ImageFont.truetype(REG,48),fill=MIST,anchor="ls")
d.text((84,520),"bayti-smart.github.io",font=ImageFont.truetype(REG,34),fill=(95,179,168),anchor="ls")
im.convert("RGB").save(out+"og-default.png",optimize=True)
print("assets written")
