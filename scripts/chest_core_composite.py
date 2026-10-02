from pathlib import Path
from PIL import Image

BODY = Path(
    "frontend/assets/character/neutral_full_body/neutral_full_body.png"
)

CORE = Path(
    "frontend/assets/character_prepared/chest_core/chest_core_glow.png"
)

OUTPUT = Path(
    "scripts/chest_core_composite.png"
)


def main():
    with Image.open(BODY) as image:
        body = image.convert("RGBA")

    with Image.open(CORE) as image:
        core = image.convert("RGBA")

    if body.size != core.size:
        raise RuntimeError(
            f"Canvas mismatch: body={body.size}, core={core.size}"
        )

    result = body.copy()
    result.alpha_composite(core)

    result.save(OUTPUT)

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()