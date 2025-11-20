from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .face import transparent_background

CARD_SIZE = (1012, 638)  # 2:1 ratio ~300dpi 3.3x2.1 in


def _load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


FONT_TITLE = _load_font(64)
FONT_BODY = _load_font(36)
FONT_SMALL = _load_font(28)


def draw_glass_card(theme: Dict[str, str], face_path: Path, qr_path: Path, destination: Path, info: Dict[str, str]) -> Path:
    base = Image.new("RGB", CARD_SIZE, theme["primary"])
    gradient = Image.new("L", CARD_SIZE, color=0xFF)
    for y in range(CARD_SIZE[1]):
        gradient.putpixel((0, y), int(255 * (y / CARD_SIZE[1])))
    gradient = gradient.resize(CARD_SIZE)
    overlay = Image.new("RGB", CARD_SIZE, theme["secondary"])
    card = Image.composite(base, overlay, gradient)
    card = card.filter(ImageFilter.GaussianBlur(radius=4))

    draw = ImageDraw.Draw(card)
    glass = (50, 50, CARD_SIZE[0] - 50, CARD_SIZE[1] - 50)
    draw.rounded_rectangle(glass, radius=48, fill=(248, 251, 255, 64), outline=theme["accent"], width=4)

    face = Image.open(face_path)
    face = transparent_background(face)
    face = face.resize((320, 320))
    card.paste(face, (80, 150), mask=face)

    qr = Image.open(qr_path).resize((220, 220))
    card.paste(qr, (CARD_SIZE[0] - 280, CARD_SIZE[1] - 280))

    draw.text((420, 140), theme["title"], fill="#F8FBFF", font=FONT_TITLE)
    draw.text((420, 220), theme["tagline"], fill=theme["accent"], font=FONT_SMALL)
    draw.text((420, 300), f"{info['first_name']} {info['last_name']}", fill="#FFFFFF", font=FONT_BODY)
    draw.text((420, 360), info.get("role", "Member"), fill="#FFFFFF", font=FONT_SMALL)
    draw.text((420, 410), f"ID: {info['external_id']}", fill="#F8FBFF", font=FONT_SMALL)
    draw.text((420, 460), f"Dept: {info.get('department','')}", fill="#F8FBFF", font=FONT_SMALL)
    draw.text((420, 510), f"Valid: {datetime.utcnow():%b %Y} • Smart IDs for smarter institutions.", fill="#E0E6FF", font=FONT_SMALL)

    destination.parent.mkdir(parents=True, exist_ok=True)
    card.save(destination, format="PNG")
    return destination

