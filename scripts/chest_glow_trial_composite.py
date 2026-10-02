from pathlib import Path
from PIL import Image

BODY = Path(
    "frontend/assets/character/neutral_full_body/neutral_full_body.png"
)

TRIAL = Path(
    "frontend/assets/character/chest_core_glow/chest_glow_trial.png"
)

OUTPUT = Path(
    "scripts/chest_glow_trial_composite.png"
)

body = Image.open(BODY).convert("RGBA")
trial = Image.open(TRIAL).convert("RGBA")

print(f"Body:  {body.size}")
print(f"Trial: {trial.size}")

if body.size != trial.size:
    raise ValueError(
        f"Canvas mismatch: body={body.size}, trial={trial.size}"
    )

# IMPORTANT:
# The trial PNG is already positioned.
# Do not resize or move it.
composite = body.copy()
composite.alpha_composite(trial)

composite.save(OUTPUT)

print(f"Created: {OUTPUT}")