from PIL import Image, ImageDraw, ImageFilter
BLUR={
 'IMG_4458':[(900,760,270,235),(1700,1030,330,510),(280,660,190,210)],
 'IMG_0617':[(878,1140,95,110)],
}
def apply(name,im):
    if name not in BLUR: return im
    bl=im.filter(ImageFilter.GaussianBlur(45))
    m=Image.new('L',im.size,0); d=ImageDraw.Draw(m)
    for cx,cy,rx,ry in BLUR[name]: d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),255)
    m=m.filter(ImageFilter.GaussianBlur(15))
    return Image.composite(bl,im,m)
