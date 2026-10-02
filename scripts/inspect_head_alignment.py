from pathlib import Path
from PIL import Image

ASSET_ROOT = Path("frontend/assets/character")

names = [
    "eyes_closed",
    "eyes_half_closed",
    "eyes_looking_left",
    "eyes_looking_right",
]

for name in names:
    path = ASSET_ROOT / name / f"{name}.png"

    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        bbox = alpha.getbbox()

        print("=" * 60)
        print(f"Asset       : {name}")
        print(f"Canvas      : {image.width} x {image.height}")

        if bbox:
            left, top, right, bottom = bbox

            print(f"Alpha bbox  : {bbox}")
            print(f"Left        : {left}")
            print(f"Top         : {top}")
            print(f"Right       : {right}")
            print(f"Bottom      : {bottom}")
            print(f"Width       : {right - left}")
            print(f"Height      : {bottom - top}")
        else:
            print("No visible pixels")

print("=" * 60)
print("Head alignment inspection complete.")