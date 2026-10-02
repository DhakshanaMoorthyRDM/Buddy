from pathlib import Path
from PIL import Image, ImageDraw

SOURCE_ROOT = Path("frontend/assets/character")
OUTPUT_ROOT = Path("frontend/assets/character_prepared/head")

NAMES = [
    "eyes_closed",
    "eyes_half_closed",
    "eyes_looking_left",
    "eyes_looking_right",
]

MASTER = "eyes_closed"

# Original 1536x1024 landmark coordinates.
LANDMARKS = {
    "eyes_closed": {
        "P1": (737, 83),
        "P2": (737, 449),
        "P3": (71, 867),
        "P4": (1398, 867),
        "P5": (737, 941),
    },
    "eyes_half_closed": {
        "P1": (789, 74),
        "P2": (789, 463),
        "P3": (137, 909),
        "P4": (1436, 907),
        "P5": (789, 985),
    },
    "eyes_looking_left": {
        "P1": (719, 21),
        "P2": (719, 439),
        "P3": (0, 909),
        "P4": (1436, 907),
        "P5": (719, 988),
    },
    "eyes_looking_right": {
        "P1": (719, 38),
        "P2": (719, 454),
        "P3": (65, 885),
        "P4": (1377, 883),
        "P5": (719, 957),
    },
}

CANVAS_SIZE = 1254
MASTER_CONTENT_SIZE = 1150


def similarity_scale_translation(source_points, target_points):
    """
    Find the best uniform scale + X/Y translation:

        target = scale * source + translation

    Rotation is deliberately NOT allowed.
    """

    source_center_x = sum(p[0] for p in source_points) / len(source_points)
    source_center_y = sum(p[1] for p in source_points) / len(source_points)

    target_center_x = sum(p[0] for p in target_points) / len(target_points)
    target_center_y = sum(p[1] for p in target_points) / len(target_points)

    source_centered = [
        (x - source_center_x, y - source_center_y)
        for x, y in source_points
    ]

    target_centered = [
        (x - target_center_x, y - target_center_y)
        for x, y in target_points
    ]

    numerator = 0.0
    denominator = 0.0

    for (sx, sy), (tx, ty) in zip(source_centered, target_centered):
        numerator += sx * tx + sy * ty
        denominator += sx * sx + sy * sy

    scale = numerator / denominator

    translation_x = (
        target_center_x - scale * source_center_x
    )

    translation_y = (
        target_center_y - scale * source_center_y
    )

    return scale, translation_x, translation_y


def transform_image(image, scale, tx, ty):
    """
    Apply forward transform:

        destination = scale * source + translation

    PIL requires the inverse mapping.
    """

    inverse_scale = 1.0 / scale

    inverse_tx = -tx / scale
    inverse_ty = -ty / scale

    return image.transform(
        image.size,
        Image.Transform.AFFINE,
        (
            inverse_scale,
            0,
            inverse_tx,
            0,
            inverse_scale,
            inverse_ty,
        ),
        resample=Image.Resampling.BICUBIC,
    )


def create_master_canvas(master):
    """
    Create the canonical 1254x1254 master canvas.
    """

    alpha = master.getchannel("A")
    bbox = alpha.getbbox()

    if bbox is None:
        raise RuntimeError("Master image has no visible content.")

    left, top, right, bottom = bbox

    crop = master.crop(bbox)

    scale = MASTER_CONTENT_SIZE / max(
        crop.width,
        crop.height,
    )

    new_width = round(crop.width * scale)
    new_height = round(crop.height * scale)

    crop = crop.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new(
        "RGBA",
        (CANVAS_SIZE, CANVAS_SIZE),
        (0, 0, 0, 0),
    )

    x = (CANVAS_SIZE - new_width) // 2
    y = (CANVAS_SIZE - new_height) // 2

    canvas.alpha_composite(crop, (x, y))

    # Mapping from original master coordinates
    # into canonical canvas coordinates.
    master_scale = scale
    master_tx = x - left * scale
    master_ty = y - top * scale

    return canvas, master_scale, master_tx, master_ty


def main():
    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    images = {}

    for name in NAMES:
        path = (
            SOURCE_ROOT
            / name
            / f"{name}.png"
        )

        with Image.open(path) as image:
            images[name] = image.convert("RGBA")

    master = images[MASTER]

    master_canvas, master_scale, master_tx, master_ty = (
        create_master_canvas(master)
    )

    master_points = [
        LANDMARKS[MASTER][key]
        for key in ["P1", "P2", "P3", "P4", "P5"]
    ]

    registered = {
        MASTER: master_canvas
    }

    print()
    print("Head registration")
    print("=================")
    print()

    for name in NAMES:
        if name == MASTER:
            continue

        source_points = [
            LANDMARKS[name][key]
            for key in ["P1", "P2", "P3", "P4", "P5"]
        ]

        scale, tx, ty = similarity_scale_translation(
            source_points,
            master_points,
        )

        print(name)
        print(f"  Registration scale: {scale:.6f}")
        print(f"  Translation X:      {tx:.2f}")
        print(f"  Translation Y:      {ty:.2f}")

        # First register this image into the master's
        # original coordinate system.
        registered_raw = transform_image(
            images[name],
            scale,
            tx,
            ty,
        )

        # Then convert it into the same canonical
        # 1254x1254 coordinate system as the master.
        final = transform_image(
            registered_raw,
            master_scale,
            master_tx,
            master_ty,
        )

        registered[name] = final

    print()

    # Save prepared assets.
    for name, image in registered.items():
        output = OUTPUT_ROOT / f"{name.replace('eyes_', '')}.png"
        image.save(output)

        print(f"Saved: {output}")

    # --------------------------------------------------
    # Diagnostic overlay
    # --------------------------------------------------

    diagnostic_dir = Path("scripts")
    diagnostic_dir.mkdir(exist_ok=True)

    diagnostic = Image.new(
        "RGBA",
        (
            CANVAS_SIZE * 2,
            CANVAS_SIZE * 2,
        ),
        (35, 35, 35, 255),
    )

    positions = {
        "eyes_closed": (0, 0),
        "eyes_half_closed": (CANVAS_SIZE, 0),
        "eyes_looking_left": (0, CANVAS_SIZE),
        "eyes_looking_right": (CANVAS_SIZE, CANVAS_SIZE),
    }

    for name in NAMES:
        base = master_canvas.copy()

        overlay = registered[name].copy()

        if name == MASTER:
            overlay.putalpha(90)
        else:
            overlay.putalpha(110)

        base.alpha_composite(overlay)

        draw = ImageDraw.Draw(base)

        draw.rectangle(
            (0, 0, 430, 55),
            fill=(0, 0, 0, 180),
        )

        draw.text(
            (15, 15),
            f"MASTER + {name}",
            fill="white",
        )

        x, y = positions[name]

        diagnostic.alpha_composite(
            base,
            (x, y),
        )

    diagnostic_path = (
        diagnostic_dir
        / "head_registration_diagnostic.png"
    )

    diagnostic.save(diagnostic_path)

    print()
    print(f"Diagnostic: {diagnostic_path}")
    print()
    print("Head registration complete.")


if __name__ == "__main__":
    main()