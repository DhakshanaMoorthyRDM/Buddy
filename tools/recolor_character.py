from pathlib import Path
from PIL import Image
import colorsys


ROOT = Path("frontend/assets/character_prepared")

TARGETS = {
    "blue": {
        "mode": "hue",
        "hue": 0.60,
    },
    "yellow": {
        "mode": "hue",
        "hue": 0.14,
    },
    "green": {
        "mode": "hue",
        "hue": 0.33,
    },
    "purple": {
        "mode": "hue",
        "hue": 0.78,
    },
    "black": {
        "mode": "black",
        "strength": 0.18,
    },
    "white": {
        "mode": "white",
        "strength": 0.92,
    },
}


ASSETS = {
    "body": ROOT / "body" / "body.png",
    "head": ROOT / "head" / "head.png",
    "open_eye": ROOT / "head" / "eyes" / "opened_eye.png",
    "closed_eye": ROOT / "head" / "eyes" / "closed_eye.png",
}


def recolor_hue(r, g, b, hue):
    h, s, v = colorsys.rgb_to_hsv(
        r / 255.0,
        g / 255.0,
        b / 255.0,
    )

    # Preserve very dark neutral shading.
    if s < 0.04:
        return r, g, b

    nr, ng, nb = colorsys.hsv_to_rgb(
        hue,
        s,
        v,
    )

    return (
        round(nr * 255),
        round(ng * 255),
        round(nb * 255),
    )


def recolor_black(r, g, b, strength):
    # Preserve the original luminance structure.
    # Dark pixels remain dark; brighter crimson areas become
    # darker rather than collapsing into one flat black.
    luminance = (
        0.2126 * r +
        0.7152 * g +
        0.0722 * b
    )

    value = luminance * strength

    value = max(0, min(255, value))

    return (
        round(value),
        round(value),
        round(value),
    )


def recolor_white(r, g, b, strength):
    # Preserve the original luminance/shading while removing
    # the original hue.
    luminance = (
        0.2126 * r +
        0.7152 * g +
        0.0722 * b
    )

    value = luminance + (255 - luminance) * strength

    value = max(0, min(255, value))

    return (
        round(value),
        round(value),
        round(value),
    )


def recolor_pixel(r, g, b, a, target):
    if a == 0:
        return r, g, b, a

    mode = target["mode"]

    if mode == "hue":
        nr, ng, nb = recolor_hue(
            r,
            g,
            b,
            target["hue"],
        )

    elif mode == "black":
        nr, ng, nb = recolor_black(
            r,
            g,
            b,
            target["strength"],
        )

    elif mode == "white":
        nr, ng, nb = recolor_white(
            r,
            g,
            b,
            target["strength"],
        )

    else:
        raise ValueError(f"Unknown mode: {mode}")

    return nr, ng, nb, a


def process_asset(source, output, target):
    image = Image.open(source).convert("RGBA")

    pixels = image.load()

    changed = 0
    visible = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]

            if a > 0:
                visible += 1

            nr, ng, nb, na = recolor_pixel(
                r,
                g,
                b,
                a,
                target,
            )

            if (r, g, b) != (nr, ng, nb):
                changed += 1

            pixels[x, y] = (
                nr,
                ng,
                nb,
                na,
            )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(output)

    print(
        f"  {source.name} -> {output.name} "
        f"({visible:,} visible / {changed:,} changed)"
    )


def main():
    print("Generating Buddy character color variants...")
    print()

    for asset_name, source in ASSETS.items():

        if not source.exists():
            print(f"SKIP: {source}")
            continue

        print(f"[{asset_name}]")

        for color_name, target in TARGETS.items():

            output_dir = source.parent / "colors" / color_name

            output = (
                output_dir /
                source.name
            )

            process_asset(
                source,
                output,
                target,
            )

        print()

    print("Finished.")
    print("Original assets were not modified.")


if __name__ == "__main__":
    main()