# Re-run after every sync from Claude Chat: python3 -I _tools/add-seo.py
# Adds search/social tags to index.html and rebuilds og-image.jpg from the hero photo.
import re, base64, io, os
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(root, 'index.html')
s = open(page, encoding='utf-8').read()
s = re.sub(r'\n?<!-- seo:start -->.*?<!-- seo:end -->', '', s, flags=re.S)
head = open(os.path.join(root, '_tools', 'seo-head.html'), encoding='utf-8').read().rstrip('\n')
s = s.replace('</title>', '</title>\n' + head, 1)
open(page, 'w', encoding='utf-8').write(s)
hero = re.search(r'class="hero"><img src="data:image/\w+;base64,([A-Za-z0-9+/=]+)"', s)
if hero:
    im = Image.open(io.BytesIO(base64.b64decode(hero.group(1)))).convert('RGB')
    w, h = im.size; th = round(w * 630 / 1200)
    if th <= h:
        top = (h - th) // 2; im = im.crop((0, top, w, top + th))
    else:
        tw = round(h * 1200 / 630); left = (w - tw) // 2; im = im.crop((left, 0, left + tw, h))
    im.resize((1200, 630), Image.LANCZOS).save(os.path.join(root, 'og-image.jpg'), quality=85, optimize=True, progressive=True)
