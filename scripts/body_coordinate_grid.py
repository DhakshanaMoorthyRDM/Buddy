from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE = Path(
    "frontend/assets/character/neutral_full_body/neutral_full_body.png"
)

OUTPUT = Path(
    "scripts/body_coordinate_grid.png"
)

image = Image.open(SOURCE).convert("RGBA")

background = Image.new(
    "RGBA",
    image.size,
    (220, 220, 220, 255)
)

background.alpha_composite(image)

draw = ImageDraw.Draw(background)

FINE_GRID = 10
STRONG_GRID = 50

# Fine 10px grid
for x in range(0, image.width + 1, FINE_GRID):
    draw.line(
        [(x, 0), (x, image.height)],
        fill=(180, 180, 180, 255),
        width=1,
    )

for y in range(0, image.height + 1, FINE_GRID):
    draw.line(
        [(0, y), (image.width, y)],
        fill=(180, 180, 180, 255),
        width=1,
    )

# Strong 50px grid + coordinate labels
for x in range(0, image.width + 1, STRONG_GRID):
    draw.line(
        [(x, 0), (x, image.height)],
        fill=(100, 100, 100, 255),
        width=2,
    )

    if x < image.width:
        draw.text(
            (x + 3, 5),
            str(x),
            fill=(0, 0, 0, 255),
        )

for y in range(0, image.height + 1, STRONG_GRID):
    draw.line(
        [(0, y), (image.width, y)],
        fill=(100, 100, 100, 255),
        width=2,
    )

    if y < image.height:
        draw.text(
            (5, y + 3),
            str(y),
            fill=(0, 0, 0, 255),
        )

# Exact canvas center
CENTER_X = image.width // 2
CENTER_Y = image.height // 2

draw.line(
    [(CENTER_X, 0), (CENTER_X, image.height)],
    fill=(255, 0, 0, 255),
    width=3,
)

draw.line(
    [(0, CENTER_Y), (image.width, CENTER_Y)],
    fill=(255, 0, 0, 255),
    width=3,
)

draw.text(
    (10, image.height - 30),
    "10px GRID | 50px MAJOR GRID | ORIGINAL 1254 x 1254",
    fill=(0, 0, 0, 255),
)
OUTPUT = Path(
    r"C:\Users\dhaks\Music\chibi-companion\scripts\body_coordinate_grid.png"
)
background.convert("RGB").save(OUTPUT)

