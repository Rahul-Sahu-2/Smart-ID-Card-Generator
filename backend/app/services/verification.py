from __future__ import annotations

from datetime import datetime

import jwt

from ..config import settings


def decode_secure_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def verify_payload(payload: dict) -> bool:
    exp = payload.get("exp")
    if exp is None:
        return False
    return datetime.utcfromtimestamp(exp) > datetime.utcnow()

