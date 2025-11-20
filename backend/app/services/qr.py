from __future__ import annotations

import io
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

import jwt
import qrcode
from qrcode.image.pil import PilImage

from ..config import settings


def generate_tokens(identity_id: int) -> Tuple[str, str]:
    payload = {
        "sub": str(identity_id),
        "exp": datetime.utcnow() + timedelta(days=365),
        "purpose": "smart-id",
    }
    secure_token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    nfc_token = secrets.token_hex(16)
    return secure_token, nfc_token


def build_qr_image(data: str, destination: Path) -> Path:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="#1D6FFF", back_color="#F8FBFF")
    destination.parent.mkdir(parents=True, exist_ok=True)
    img.save(destination)
    return destination


def qr_bytes(data: str) -> bytes:
    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

