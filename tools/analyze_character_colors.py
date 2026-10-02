from pathlib import Path
from PIL import Image
from collections import Counter
import colorsys


ROOT = Path(
    r"C:\Users\dhaks\Music\chibi-companion\frontend\assets\character_prepared"
)

REPORT_PATH = Path(
    r"C:\Users\dhaks\Music\chibi-companion\tools\color_analysis_report.txt"
)

FILES = {
    "body": ROOT / "body" / "body.png",
    "head": ROOT / "head" / "head.png",
    "opened_eye": ROOT / "head" / "eyes" / "opened_eye.png",
    "closed_eye": ROOT / "head" / "eyes" / "closed_eye.png",
}


def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(
        r / 255,
        g / 255,
        b / 255,
    )


def is_colorful(r, g, b):
    return max(r, g, b) - min(r, g, b) >= 20


def is_red_family(r, g, b):
    return (
        r > g * 1.03
        and r > b * 1.03
        and r > 20
    )


def analyze_image(name, path):
    image = Image.open(path).convert("RGBA")
    pixels = list(image.getdata())

    total = len(pixels)

    visible = [
        p for p in pixels
        if p[3] > 0
    ]

    transparent = total - len(visible)

    partial_alpha = sum(
        1
        for p in pixels
        if 0 < p[3] < 255
    )

    fully_opaque = sum(
        1
        for p in pixels
        if p[3] == 255
    )

    color_counter = Counter(visible)

    red_pixels = [
        p for p in visible
        if is_red_family(p[0], p[1], p[2])
    ]

    red_counter = Counter(red_pixels)

    colorful_pixels = [
        p for p in visible
        if is_colorful(p[0], p[1], p[2])
    ]

    colorful_counter = Counter(colorful_pixels)

    brightness_values = []

    for r, g, b, a in visible:
        brightness = (
            0.2126 * r +
            0.7152 * g +
            0.0722 * b
        )

        brightness_values.append(brightness)

    average_brightness = (
        sum(brightness_values) / len(brightness_values)
        if brightness_values
        else 0
    )

    darkest = min(brightness_values) if brightness_values else 0
    brightest = max(brightness_values) if brightness_values else 0

    report = []

    report.append("=" * 80)
    report.append(name.upper())
    report.append("=" * 80)

    report.append(f"File: {path}")
    report.append(f"Size: {image.width} x {image.height}")
    report.append(f"Total pixels: {total:,}")
    report.append(f"Visible pixels: {len(visible):,}")
    report.append(f"Transparent pixels: {transparent:,}")
    report.append(f"Partial alpha pixels: {partial_alpha:,}")
    report.append(f"Fully opaque pixels: {fully_opaque:,}")
    report.append(f"Unique visible RGBA colors: {len(color_counter):,}")

    report.append("")
    report.append("BRIGHTNESS")
    report.append("-" * 80)
    report.append(f"Darkest pixel: {darkest:.2f}")
    report.append(f"Brightest pixel: {brightest:.2f}")
    report.append(f"Average brightness: {average_brightness:.2f}")

    report.append("")
    report.append("COLOR INFORMATION")
    report.append("-" * 80)
    report.append(f"Colorful pixels: {len(colorful_pixels):,}")
    report.append(f"Unique colorful colors: {len(colorful_counter):,}")
    report.append(f"Red-family pixels: {len(red_pixels):,}")
    report.append(f"Unique red-family colors: {len(red_counter):,}")

    if red_counter:
        red_hues = []

        for r, g, b, a in red_pixels:
            h, s, v = rgb_to_hsv(r, g, b)

            if s > 0.05:
                red_hues.append(h * 360)

        report.append(
            f"Red-family hue range: "
            f"{min(red_hues):.2f}° - {max(red_hues):.2f}°"
        )

    report.append("")
    report.append("MOST COMMON RED-FAMILY COLORS")
    report.append("-" * 80)

    for (r, g, b, a), count in red_counter.most_common(20):
        h, s, v = rgb_to_hsv(r, g, b)

        report.append(
            f"RGB({r:3},{g:3},{b:3}) "
            f"Alpha={a:3} "
            f"H={h * 360:6.2f}° "
            f"S={s * 100:6.2f}% "
            f"V={v * 100:6.2f}% "
            f"Pixels={count:,}"
        )

    report.append("")
    report.append("ALPHA SUMMARY")
    report.append("-" * 80)

    alpha_counter = Counter(
        p[3]
        for p in pixels
    )

    report.append(
        f"Unique alpha levels: {len(alpha_counter):,}"
    )

    report.append(
        f"Minimum alpha: {min(alpha_counter)}"
    )

    report.append(
        f"Maximum alpha: {max(alpha_counter)}"
    )

    report.append("")
    report.append("TOP 10 MOST COMMON VISIBLE COLORS")
    report.append("-" * 80)

    for (r, g, b, a), count in color_counter.most_common(10):
        report.append(
            f"RGB({r:3},{g:3},{b:3}) "
            f"Alpha={a:3} "
            f"Pixels={count:,}"
        )

    report.append("")

    return "\n".join(report)


def main():
    all_reports = []

    all_reports.append(
        "CHARACTER COLOR ANALYSIS REPORT"
    )

    all_reports.append(
        "=" * 80
    )

    all_reports.append(
        "Every pixel was inspected individually."
    )

    all_reports.append(
        "The report summarizes the pixel data rather than printing every pixel."
    )

    all_reports.append("")

    for name, path in FILES.items():
        if not path.exists():
            all_reports.append(
                f"\nMISSING FILE: {path}"
            )
            continue

        all_reports.append(
            analyze_image(name, path)
        )

    all_reports.append(
        "\n" + "=" * 80
    )

    all_reports.append(
        "END OF REPORT"
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        "\n".join(all_reports),
        encoding="utf-8",
    )

    print("Analysis complete.")
    print()
    print(f"Report saved to:")
    print(REPORT_PATH)


if __name__ == "__main__":
    main()