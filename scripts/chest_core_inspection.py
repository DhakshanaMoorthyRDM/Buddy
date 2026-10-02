from pathlib import Path
from PIL import Image, ImageDraw

SOURCE_ROOT = Path("frontend/assets/character")

BODY = SOURCE_ROOT / "neutral_full_body" / "neutral_full_body.png"
CORE = SOURCE_ROOT / "chest_core_glow" / "chest_core_glow.png"

OUTPUT = Path("scripts/chest_core_inspection.png")

PANEL_WIDTH = 700
PANEL_HEIGHT = 700

sheet = Image.new(
    "RGB",
    (PANEL_WIDTH * 2, PANEL_HEIGHT),
    (45, 45, 45),
)

draw = ImageDraw.Draw(sheet)

# --------------------------------------------------
# Neutral body
# --------------------------------------------------

with Image.open(BODY) as image:
    body = image.convert("RGBA")

body_preview = body.copy()
body_preview.thumbnail(
    (PANEL_WIDTH - 40, PANEL_HEIGHT - 80),
    Image.Resampling.LANCZOS,
)

body_x = (PANEL_WIDTH - body_preview.width) // 2
body_y = 60 + (
    PANEL_HEIGHT - 60 - body_preview.height
) // 2

sheet.paste(
    body_preview,
    (body_x, body_y),
    body_preview,
)

draw.text(
    (20, 20),
    "NEUTRAL FULL BODY",
    fill="white",
)

# --------------------------------------------------
# Chest core
# --------------------------------------------------

with Image.open(CORE) as image:
    core = image.convert("RGBA")

core_preview = core.copy()
core_preview.thumbnail(
    (PANEL_WIDTH - 40, PANEL_HEIGHT - 80),
    Image.Resampling.LANCZOS,
)

core_x = PANEL_WIDTH + (
    PANEL_WIDTH - core_preview.width
) // 2

core_y = 60 + (
    PANEL_HEIGHT - 60 - core_preview.height
) // 2

sheet.paste(
    core_preview,
    (core_x, core_y),
    core_preview,
)

draw.text(
    (PANEL_WIDTH + 20, 20),
    "CHEST CORE GLOW",
    fill="white",
)

# --------------------------------------------------
# Save
# --------------------------------------------------

sheet.save(OUTPUT)

print(f"Created: {OUTPUT}")