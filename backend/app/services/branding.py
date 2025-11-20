from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from colorthief import ColorThief

from ..config import settings


def extract_palette(image_path: Path, color_count: int = 5) -> List[str]:
    if not image_path or not image_path.exists():
        return settings.default_brand_palette

    thief = ColorThief(str(image_path))
    palette = thief.get_palette(color_count=color_count)
    return [f"#{r:02X}{g:02X}{b:02X}" for r, g, b in palette]


def build_brand_theme(logo_path: Path | None, institution_name: str) -> Dict[str, str]:
    palette = extract_palette(logo_path) if logo_path else settings.default_brand_palette
    primary, *rest = palette
    secondary = rest[0] if rest else settings.default_brand_palette[1]
    accent = rest[1] if len(rest) > 1 else settings.default_brand_palette[2]

    return {
        "primary": primary,
        "secondary": secondary,
        "accent": accent,
        "typography": "Space Grotesk",
        "title": f"{institution_name}",
        "tagline": "Identity that protects itself.",
    }

