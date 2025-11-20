from __future__ import annotations

from pydantic import BaseModel, EmailStr


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "operator"
    institution_id: int | None = None

