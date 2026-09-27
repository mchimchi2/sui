import glob,sys
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/snapshots/frame-*.png'), key=lambda f: float(f.split('-at-')[1][:-5]))
ims=[Image.open(f).convert('RGB').resize((225,400)) for f in fs]
s=Image.new('RGB',(235*len(ims),400))
for i,im in enumerate(ims): s.paste(im,(i*235,0))
s.save(sys.argv[2])
