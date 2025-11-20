from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


class Institution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str
    domain: Optional[str] = None
    logo_path: Optional[str] = None
    branding_colors: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, default=list),
    )
    typography: Optional[str] = None
    tagline: Optional[str] = None

    identities: List["Identity"] = Relationship(back_populates="institution")


class Identity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    date_of_birth: Optional[str] = None
    join_date: Optional[str] = None
    institution_id: int = Field(foreign_key="institution.id")

    photo_path: Optional[str] = None
    face_crop_path: Optional[str] = None
    card_png_path: Optional[str] = None
    card_pdf_path: Optional[str] = None
    wallet_card_path: Optional[str] = None
    qr_png_path: Optional[str] = None
    secure_token: Optional[str] = None
    nfc_token: Optional[str] = None
    last_generated_at: Optional[datetime] = None
    status: str = Field(default="draft")

    metadata_json: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON, nullable=True))

    institution: Optional[Institution] = Relationship(back_populates="identities")
    scans: List["ScanLog"] = Relationship(back_populates="identity")


class ScanLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identity_id: int = Field(foreign_key="identity.id")
    scan_channel: str
    location: Optional[str] = None
    verified_by: Optional[str] = None
    result: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    identity: Optional[Identity] = Relationship(back_populates="scans")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    hashed_password: str
    role: str = Field(default="operator")
    institution_id: Optional[int] = Field(default=None, foreign_key="institution.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
*** End Patch

