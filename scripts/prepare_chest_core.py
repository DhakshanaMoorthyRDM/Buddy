from pathlib import Path
from PIL import Image

SOURCE = Path(
    "frontend/assets/character/chest_core_glow/chest_core_glow.png"
)

OUTPUT = Path(
    "frontend/assets/character_prepared/chest_core/chest_core_glow.png"
)

CANVAS_SIZE = 1254

# Runtime anchor on the neutral body.
TARGET_CENTER = (625, 705)

# Target width of the visible glow after cropping.
TARGET_WIDTH = 90


def main():
    with Image.open(SOURCE) as image:
        image = image.convert("RGBA")

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox is None:
        raise RuntimeError("Chest-core image has no visible content.")

    # Remove only the transparent padding.
    cropped = image.crop(bbox)

    scale = TARGET_WIDTH / cropped.width

    new_width = round(cropped.width * scale)
    new_height = round(cropped.height * scale)

    cropped = cropped.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new(
        "RGBA",
        (CANVAS_SIZE, CANVAS_SIZE),
        (0, 0, 0, 0),
    )

    x = round(TARGET_CENTER[0] - new_width / 2)
    y = round(TARGET_CENTER[1] - new_height / 2)

    canvas.alpha_composite(
        cropped,
        (x, y),
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    canvas.save(OUTPUT)

    print("Chest core prepared.")
    print()
    print(f"Original visible area: {bbox}")
    print(f"Cropped size:          {cropped.size}")
    print(f"Target center:         {TARGET_CENTER}")
    print(f"Target visible width:  {TARGET_WIDTH}")
    print(f"Placed at:             ({x}, {y})")
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()