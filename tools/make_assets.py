#!/usr/bin/env python3
"""Andersen Launcher — emblem és ikon generálása (Pillow)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GOLD = (214, 179, 109, 255)
GOLD_SOFT = (214, 179, 109, 110)
PAGE = (24, 40, 64, 255)
NAVY = (10, 18, 32, 255)
NAVY_TOP = (16, 28, 47, 255)
NAVY_BOTTOM = (7, 13, 24, 255)


def star_points(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    k = 0.18
    return [
        (cx, cy - r),
        (cx + r * k, cy - r * k),
        (cx + r, cy),
        (cx + r * k, cy + r * k),
        (cx, cy + r),
        (cx - r * k, cy + r * k),
        (cx - r, cy),
        (cx - r * k, cy - r * k),
    ]


def draw_book(d: ImageDraw.ImageDraw, scale: float = 1.0, dy: float = 0.0) -> None:
    """Nyitott könyv aranyszínű körvonallal, 1024-es koordinátarendszerben."""
    ss = 2  # supersampling

    def p(x: float, y: float) -> tuple[float, float]:
        return ((x * scale + (1 - scale) * 512) * ss, (y * scale + (1 - scale) * 520 + dy) * ss)

    def poly(points: list[tuple[float, float]], fill, outline=None, width: float = 0) -> None:
        pts = [p(x, y) for x, y in points]
        d.polygon(pts, fill=fill)
        if outline:
            d.line(pts + [pts[0]], fill=outline, width=max(1, int(width * scale * ss)), joint="curve")

    def line(points: list[tuple[float, float]], fill, width: float) -> None:
        d.line([p(x, y) for x, y in points], fill=fill, width=max(1, int(width * scale * ss)), joint="curve")

    # Bal oldal
    left_page = [
        (512, 430),
        (430, 395),
        (330, 362),
        (230, 340),
        (170, 352),
        (170, 628),
        (230, 655),
        (330, 682),
        (430, 700),
        (512, 700),
    ]
    # Jobb oldal (tükrözés)
    right_page = [(1024 - x, y) for x, y in left_page]
    poly(left_page, PAGE, GOLD, 12)
    poly(right_page, PAGE, GOLD, 12)

    # Gerinc
    line([(512, 430), (512, 700)], GOLD, 10)

    # Kézirat-sorok
    for i, y in enumerate((470, 525, 580)):
        drop = i * 2
        line([(500, y + 8), (215, 376 + drop)], GOLD_SOFT, 5)
        line([(524, y + 8), (809, 376 + drop)], GOLD_SOFT, 5)

    # Csillagok
    d.polygon([p(x, y) for x, y in star_points(512, 205, 72)], fill=GOLD)
    d.polygon([p(x, y) for x, y in star_points(620, 272, 26)], fill=(214, 179, 109, 190))
    d.polygon([p(x, y) for x, y in star_points(404, 285, 20)], fill=(214, 179, 109, 150))


def make_emblem() -> Image.Image:
    ss = 2
    size = 1024
    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_book(d)
    return img.resize((size, size), Image.LANCZOS)


def make_icon() -> Image.Image:
    ss = 2
    size = 1024
    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))

    # Finom függőleges színátmenet
    grad = Image.new("RGBA", (1, size * ss))
    gd = ImageDraw.Draw(grad)
    for y in range(size * ss):
        t = y / (size * ss - 1)
        color = tuple(
            int(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t) for i in range(3)
        ) + (255,)
        gd.point((0, y), fill=color)

    mask = Image.new("L", (size * ss, size * ss), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, size * ss - 1, size * ss - 1], radius=210 * ss, fill=255)
    img.paste(grad.resize((size * ss, size * ss)), (0, 0), mask)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle(
        [18 * ss, 18 * ss, (size - 18) * ss, (size - 18) * ss],
        radius=196 * ss,
        outline=(214, 179, 109, 150),
        width=4 * ss,
    )
    draw_book(d, scale=0.80, dy=36)
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    emblem = make_emblem()
    emblem.save(ASSETS / "andersen-emblem.png")

    icon = make_icon()
    icon.save(ASSETS / "andersen-icon.png")
    icon.save(
        ASSETS / "andersen-icon.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )

    print(f"Kész: {ASSETS}")


if __name__ == "__main__":
    main()
