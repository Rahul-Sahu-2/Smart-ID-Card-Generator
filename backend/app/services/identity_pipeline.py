from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import httpx

from ..config import settings
from ..config import settings
from ..models import Institution
from .branding import build_brand_theme
from .card_renderer import draw_glass_card
from .exporter import build_wallet_card, export_pdf
from .face import crop_align_face, save_face
from .qr import build_qr_image, generate_tokens
from .storage import build_identity_paths


async def fetch_photo_bytes(photo: Optional[bytes] = None, photo_url: str | None = None) -> bytes:
    if photo:
        return photo
    if photo_url:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(photo_url)
            response.raise_for_status()
            return response.content
    raise ValueError("Photo data missing")


async def run_identity_pipeline(
    identity_id: int,
    identity_data: Dict[str, str],
    institution: Institution,
    photo_bytes: bytes | None = None,
    photo_url: str | None = None,
) -> Dict[str, str]:
    image_bytes = await fetch_photo_bytes(photo_bytes, photo_url)
    paths = build_identity_paths(identity_data["external_id"])
    Path(paths["photo"]).write_bytes(image_bytes)

    face_image = crop_align_face(image_bytes)
    save_face(face_image, Path(paths["face"]))

    theme = build_brand_theme(Path(institution.logo_path) if institution.logo_path else None, institution.name)
    secure_token, nfc_token = generate_tokens(identity_id)
    build_qr_image(secure_token, Path(paths["qr"]))
    draw_glass_card(theme, Path(paths["face"]), Path(paths["qr"]), Path(paths["card_png"]), identity_data)
    export_pdf(Path(paths["card_png"]), Path(paths["card_pdf"]))
    build_wallet_card(Path(paths["card_png"]), Path(paths["wallet"]))

    return {
        "photo_path": str(paths["photo"]),
        "face_crop_path": str(paths["face"]),
        "card_png_path": str(paths["card_png"]),
        "card_pdf_path": str(paths["card_pdf"]),
        "wallet_card_path": str(paths["wallet"]),
        "qr_png_path": str(paths["qr"]),
        "secure_token": secure_token,
        "nfc_token": nfc_token,
        "metadata_json": {"theme": theme},
        "last_generated_at": datetime.utcnow(),
    }

