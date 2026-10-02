from pathlib import Path
from PIL import Image

ASSET_ROOT = Path("frontend/assets/character")

for image_path in sorted(ASSET_ROOT.rglob("*.png")):
    try:
        with Image.open(image_path) as image:
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")

            bbox = alpha.getbbox()

            print("=" * 60)
            print(f"Asset       : {image_path}")
            print(f"Dimensions  : {image.size[0]} x {image.size[1]}")
            print(f"Mode        : {image.mode}")
            print(f"Format      : {image.format}")

            if bbox:
                print(f"Alpha bbox  : {bbox}")
                print(
                    f"Content size: "
                    f"{bbox[2] - bbox[0]} x {bbox[3] - bbox[1]}"
                )
            else:
                print("Alpha bbox  : No visible pixels")

            alpha_values = list(alpha.getdata())

            if all(value == 255 for value in alpha_values):
                print("Transparency: None")
            elif all(value == 0 for value in alpha_values):
                print("Transparency: Fully transparent")
            else:
                print("Transparency: Present")

    except Exception as error:
        print(f"ERROR: {image_path}")
        print(error)

print("=" * 60)
print("Asset inspection complete.")