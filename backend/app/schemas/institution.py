from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class InstitutionCreate(BaseModel):
    name: str
    slug: str
    domain: Optional[str]
    tagline: Optional[str]


class InstitutionResponse(BaseModel):
    id: int
    name: str
    slug: str
    logo_path: Optional[str]
    branding_colors: List[str]
    tagline: Optional[str]

    class Config:
        orm_mode = True

