from pathlib import Path
from PIL import Image

root = Path(r"C:\Users\dhaks\Music\chibi-companion\frontend\assets\character_prepared")

files = [
    root / "body" / "body.png",
    root / "head" / "head.png",
    root / "head" / "eyes" / "opened_eye.png",
    root / "chest_core" / "chest_core_glow.png",
]

for path in files:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")

    print()
    print(path.name)
    print("  Size:", image.size)
    print("  Visible bounds:", alpha.getbbox())

    bbox = alpha.getbbox()

    if bbox:
        left, top, right, bottom = bbox
        print("  Transparent left:", left)
        print("  Transparent top:", top)
        print("  Transparent right:", image.width - right)
        print("  Transparent bottom:", image.height - bottom)