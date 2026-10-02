from pathlib import Path
from PIL import Image, ImageDraw

ASSET_ROOT = Path("frontend/assets/character")

names = [
    "eyes_closed",
    "eyes_half_closed",
    "eyes_looking_left",
    "eyes_looking_right",
]

canvas_size = (700, 500)
background = (220, 220, 220, 255)

sheet = Image.new(
    "RGBA",
    (canvas_size[0] * 2, canvas_size[1] * 2),
    background
)

draw = ImageDraw.Draw(sheet)

for index, name in enumerate(names):
    path = ASSET_ROOT / name / f"{name}.png"

    with Image.open(path) as source:
        image = source.convert("RGBA")

        bbox = image.getchannel("A").getbbox()

        if not bbox:
            continue

        cropped = image.crop(bbox)

        scale = min(
            (canvas_size[0] - 40) / cropped.width,
            (canvas_size[1] - 60) / cropped.height
        )

        new_size = (
            round(cropped.width * scale),
            round(cropped.height * scale)
        )

        cropped = cropped.resize(
            new_size,
            Image.Resampling.LANCZOS
        )

        x = (canvas_size[0] - cropped.width) // 2
        y = (canvas_size[1] - cropped.height) // 2

        panel_x = (index % 2) * canvas_size[0]
        panel_y = (index // 2) * canvas_size[1]

        panel = Image.new(
            "RGBA",
            canvas_size,
            background
        )

        panel.alpha_composite(cropped, (x, y))

        draw.text(
            (panel_x + 15, panel_y + 15),
            name,
            fill=(0, 0, 0, 255)
        )

        sheet.alpha_composite(panel, (panel_x, panel_y))

output = Path("scripts/head_alignment_preview.png")
sheet.convert("RGB").save(output)

print(f"Preview created: {output}")