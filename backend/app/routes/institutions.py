from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import select

from ..config import settings
from ..database import get_session
from ..models import Institution
from ..schemas.institution import InstitutionCreate, InstitutionResponse
from ..services.branding import build_brand_theme

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get("", response_model=list[InstitutionResponse])
def list_institutions(session=Depends(get_session)):
    return session.exec(select(Institution)).all()


@router.post("", response_model=InstitutionResponse)
def create_institution(payload: InstitutionCreate, session=Depends(get_session)):
    exists = session.exec(select(Institution).where(Institution.slug == payload.slug)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Slug already taken")

    institution = Institution(
        name=payload.name,
        slug=payload.slug,
        domain=payload.domain,
        tagline=payload.tagline,
        branding_colors=settings.default_brand_palette,
    )
    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution


@router.post("/{institution_id}/branding", response_model=InstitutionResponse)
async def upload_branding(
    institution_id: int,
    logo: UploadFile = File(...),
    session=Depends(get_session),
):
    institution = session.get(Institution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution missing")

    logo_dir = settings.storage_dir / "branding" / institution.slug
    logo_dir.mkdir(parents=True, exist_ok=True)
    logo_path = logo_dir / logo.filename
    content = await logo.read()
    logo_path.write_bytes(content)

    theme = build_brand_theme(logo_path, institution.name)
    institution.logo_path = str(logo_path)
    institution.branding_colors = [theme["primary"], theme["secondary"], theme["accent"]]
    institution.typography = theme["typography"]
    institution.tagline = theme["tagline"]

    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution

