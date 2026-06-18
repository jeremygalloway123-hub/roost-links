from PIL import Image

src = "assets/ass-logo-source.png"
out = "assets/ass-logo-white.png"

img = Image.open(src).convert("RGBA")

# Rotate 90 degrees counterclockwise (PIL rotates CCW for positive angles).
img = img.rotate(90, expand=True)

px = img.load()
w, h = img.size

# Source is black artwork on a white background. Make the white background
# transparent and turn the artwork white. Using alpha = 255 - brightness keeps
# anti-aliased edges smooth instead of producing a hard jagged outline.
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        brightness = (r + g + b) // 3
        alpha = 255 - brightness
        # Respect any existing transparency in the source.
        alpha = alpha * a // 255
        px[x, y] = (255, 255, 255, alpha)

# Auto-crop to the meaningful content, ignoring faint noise.
alpha_ch = img.split()[3]
mask = alpha_ch.point(lambda v: 255 if v > 40 else 0)
bbox = mask.getbbox()
if bbox:
    img = img.crop(bbox)

# The winding line protrudes well above the main "A.S.S." body. Trim the top so
# only half of that protruding line remains: find where the dense body begins
# and cut the top edge at half that distance.
w, h = img.size
px = img.split()[3].load()
body_start = 0
for y in range(h):
    if sum(1 for x in range(w) if px[x, y] > 40) > 90:
        body_start = y
        break
top_crop = body_start // 2
if top_crop > 0:
    img = img.crop((0, top_crop, w, h))

img.save(out)
print("Saved", out, img.size)
