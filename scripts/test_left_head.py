from pathlib import Path
from PIL import Image

SOURCE = Path("frontend/assets/character/eyes_looking_left/eyes_looking_left.png")
OUTPUT = Path("frontend/assets/character_prepared/head/looking_left_test.png")

SCALE = 0.94

# Original landmark used as the structural anchor.
SOURCE_ANCHOR = (770, 82)

# Master anchor.
TARGET_ANCHOR = (737, 83)

with Image.open(SOURCE) as image:
    image = image.convert("RGBA")

    new_width = round(image.width * SCALE)
    new_height = round(image.height * SCALE)

    scaled = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    # Where the source anchor lands after scaling.
    scaled_anchor_x = SOURCE_ANCHOR[0] * SCALE
    scaled_anchor_y = SOURCE_ANCHOR[1] * SCALE

    # Translation required to place that anchor
    # on the master's anchor.
    offset_x = round(TARGET_ANCHOR[0] - scaled_anchor_x)
    offset_y = round(TARGET_ANCHOR[1] - scaled_anchor_y)

    canvas = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0),
    )

    canvas.alpha_composite(
        scaled,
        (offset_x, offset_y),
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(OUTPUT)

print("Created:")
print(OUTPUT)
print()
print(f"Scale: {SCALE}")
print(f"Translation X: {offset_x}")
print(f"Translation Y: {offset_y}")