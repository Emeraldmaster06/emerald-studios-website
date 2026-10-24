# Builds the site icons (shown in browser tabs and next to the link in Google results)
# from the logo embedded in index.html. Re-run after a sync: python3 -I _tools/make-icons.py
import re, base64, io, os
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
m = re.search(r'src="data:image/png;base64,([A-Za-z0-9+/=]+)" alt="Emerald Studios logo"', s)
logo = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
def icon(size, scale=0.82):
    bg = Image.new('RGBA', (size, size), (255, 255, 255, 255))
    w = round(size * scale); h = round(logo.height * w / logo.width)
    lg = logo.resize((w, h), Image.LANCZOS)
    bg.alpha_composite(lg, ((size - w) // 2, (size - h) // 2))
    return bg.convert('RGB')
icon(192).save(os.path.join(root, 'icon-192.png'), optimize=True)
icon(512).save(os.path.join(root, 'icon-512.png'), optimize=True)
icon(180).save(os.path.join(root, 'apple-touch-icon.png'), optimize=True)
icon(96, 0.9).save(os.path.join(root, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
