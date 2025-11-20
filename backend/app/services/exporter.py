from __future__ import annotations

from pathlib import Path

from PIL import Image


def export_pdf(card_png: Path, destination: Path) -> Path:
    image = Image.open(card_png)
    rgb = image.convert("RGB")
    destination.parent.mkdir(parents=True, exist_ok=True)
    rgb.save(destination, format="PDF")
    return destination


def build_wallet_card(card_png: Path, destination: Path) -> Path:
    image = Image.open(card_png)
    phone_ratio = (600, 900)
    wallet = image.resize(phone_ratio, Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    wallet.save(destination, format="PNG")
    return destination

