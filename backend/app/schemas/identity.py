from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class IdentityCreate(BaseModel):
    external_id: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    institution_id: int


class IdentityResponse(BaseModel):
    id: int
    external_id: str
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    role: Optional[str]
    department: Optional[str]
    status: str
    card_png_path: Optional[str]
    card_pdf_path: Optional[str]
    wallet_card_path: Optional[str]
    qr_png_path: Optional[str]
    secure_token: Optional[str]
    nfc_token: Optional[str]
    last_generated_at: Optional[datetime]

    class Config:
        orm_mode = True


class IdentityBulkUploadResult(BaseModel):
    processed: int
    created_ids: List[int]
    errors: List[str]

