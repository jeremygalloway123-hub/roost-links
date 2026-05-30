from PIL import Image

src = "roost logo owl.png"
out = "roost-logo-owl-transparent.png"

img = Image.open(src).convert("RGBA")
px = img.load()
w, h = img.size

# Black background -> transparent. Smooth alpha ramp on near-black pixels
# so anti-aliased edges don't get a harsh halo.
LOW = 18    # at/below this brightness -> fully transparent
HIGH = 55   # at/above this brightness -> fully opaque

for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        brightness = max(r, g, b)
        if brightness <= LOW:
            px[x, y] = (r, g, b, 0)
        elif brightness < HIGH:
            alpha = int(255 * (brightness - LOW) / (HIGH - LOW))
            px[x, y] = (r, g, b, alpha)
        # else: keep fully opaque

# The source has a faint 1px non-black border around the edges. Force the
# outermost rows/cols fully transparent so they don't defeat the auto-crop.
for x in range(w):
    px[x, 0] = px[x, 0][:3] + (0,)
    px[x, h - 1] = px[x, h - 1][:3] + (0,)
for y in range(h):
    px[0, y] = px[0, y][:3] + (0,)
    px[w - 1, y] = px[w - 1, y][:3] + (0,)

# Auto-crop to the meaningful content. Ignore near-transparent noise specks
# by thresholding the alpha channel before computing the bounding box.
alpha = img.split()[3]
mask = alpha.point(lambda v: 255 if v > 40 else 0)
bbox = mask.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(out)
print("Saved", out, img.size)
