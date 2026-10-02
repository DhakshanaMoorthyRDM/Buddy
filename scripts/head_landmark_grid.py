from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_ROOT = Path("frontend/assets/character")

NAMES = [
    "eyes_closed",
    "eyes_half_closed",
    "eyes_looking_left",
    "eyes_looking_right",
]

PANEL_WIDTH = 768
PANEL_HEIGHT = 512
GRID_STEP = 50

sheet = Image.new(
    "RGB",
    (PANEL_WIDTH * 2, PANEL_HEIGHT * 2),
    "white"
)

draw = ImageDraw.Draw(sheet)

for index, name in enumerate(NAMES):
    path = SOURCE_ROOT / name / f"{name}.png"

    with Image.open(path) as source:
        image = source.convert("RGBA")

        background = Image.new(
            "RGBA",
            image.size,
            (220, 220, 220, 255)
        )

        background.alpha_composite(image)

        preview = background.resize(
            (PANEL_WIDTH, PANEL_HEIGHT),
            Image.Resampling.LANCZOS
        )

        panel_x = (index % 2) * PANEL_WIDTH
        panel_y = (index // 2) * PANEL_HEIGHT

        sheet.paste(
            preview.convert("RGB"),
            (panel_x, panel_y)
        )

        draw.text(
            (panel_x + 10, panel_y + 10),
            name,
            fill="black"
        )

        scale_x = PANEL_WIDTH / image.width
        scale_y = PANEL_HEIGHT / image.height

        for x in range(0, image.width + 1, GRID_STEP):
            px = panel_x + int(x * scale_x)

            draw.line(
                [(px, panel_y), (px, panel_y + PANEL_HEIGHT)],
                fill=(150, 150, 150),
                width=1
            )

            if x < image.width:
                draw.text(
                    (px + 2, panel_y + PANEL_HEIGHT - 20),
                    str(x),
                    fill="black"
                )

        for y in range(0, image.height + 1, GRID_STEP):
            py = panel_y + int(y * scale_y)

            draw.line(
                [(panel_x, py), (panel_x + PANEL_WIDTH, py)],
                fill=(150, 150, 150),
                width=1
            )

            if y < image.height:
                draw.text(
                    (panel_x + 2, py + 2),
                    str(y),
                    fill="black"
                )

output = Path("scripts/head_landmark_grid.png")
sheet.save(output)

print(f"Created: {output}")