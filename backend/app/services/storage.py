from pathlib import Path
from typing import Tuple

from ..config import settings


def ensure_storage() -> Tuple[Path, Path, Path]:
    base = settings.storage_dir
    originals = base / "original"
    faces = base / "faces"
    exports = base / "exports"
    qr_dir = base / "qr"

    for path in (base, originals, faces, exports, qr_dir):
        path.mkdir(parents=True, exist_ok=True)

    return originals, faces, exports


def build_identity_paths(external_id: str) -> dict:
    base = settings.storage_dir / external_id
    base.mkdir(parents=True, exist_ok=True)
    return {
        "photo": base / "photo.png",
        "face": base / "face.png",
        "card_png": base / "card.png",
        "card_pdf": base / "card.pdf",
        "wallet": base / "wallet.png",
        "qr": base / "qr.png",
    }

