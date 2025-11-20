import io
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ..database import get_session
from ..models import Identity, Institution
from ..schemas.identity import IdentityBulkUploadResult, IdentityResponse
from ..services.identity_pipeline import run_identity_pipeline

router = APIRouter(prefix="/identities", tags=["identities"])


@router.post("", response_model=IdentityResponse)
async def create_identity(
    external_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(""),
    role: str = Form("Member"),
    department: str = Form("General"),
    institution_id: int = Form(...),
    photo: UploadFile = File(...),
    session=Depends(get_session),
):
    institution = session.get(Institution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    identity = Identity(
        external_id=external_id,
        first_name=first_name,
        last_name=last_name,
        email=email or None,
        role=role,
        department=department,
        institution_id=institution_id,
        status="processing",
    )
    session.add(identity)
    session.commit()
    session.refresh(identity)

    photo_bytes = await photo.read()
    try:
        assets = await run_identity_pipeline(
            identity_id=identity.id,
            identity_data={
                "external_id": external_id,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "department": department,
            },
            institution=institution,
            photo_bytes=photo_bytes,
        )
        for key, value in assets.items():
            setattr(identity, key, value)
        identity.status = "ready"
        session.add(identity)
        session.commit()
        session.refresh(identity)
        return identity
    except Exception as exc:  # noqa: BLE001
        identity.status = "failed"
        session.add(identity)
        session.commit()
        raise HTTPException(status_code=500, detail=f"Failed to generate identity: {exc}") from exc


@router.get("", response_model=List[IdentityResponse])
def list_identities(session=Depends(get_session)):
    identities = session.exec(select(Identity)).all()
    return identities


@router.post("/bulk", response_model=IdentityBulkUploadResult)
async def bulk_upload(
    institution_id: int = Form(...),
    file: UploadFile = File(...),
    session=Depends(get_session),
):
    institution = session.get(Institution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    content = await file.read()
    suffix = file.filename.split(".")[-1].lower()
    buffer = io.BytesIO(content)
    if suffix in {"xlsx", "xls"}:
        df = pd.read_excel(buffer)
    else:
        df = pd.read_csv(buffer)

    processed = 0
    created_ids: List[int] = []
    errors: List[str] = []

    for _, row in df.iterrows():
        try:
            identity = Identity(
                external_id=str(row.get("external_id") or row.get("id")),
                first_name=row.get("first_name") or row.get("First Name"),
                last_name=row.get("last_name") or row.get("Last Name"),
                email=row.get("email"),
                role=row.get("role") or "Member",
                department=row.get("department") or "General",
                institution_id=institution_id,
                status="processing",
            )
            session.add(identity)
            session.commit()
            session.refresh(identity)
            created_ids.append(identity.id)
            processed += 1

            photo_url = row.get("photo_url")
            if pd.isna(photo_url):
                identity.status = "pending_photo"
                session.add(identity)
                session.commit()
                continue

            assets = await run_identity_pipeline(
                identity.id,
                {
                    "external_id": identity.external_id,
                    "first_name": identity.first_name,
                    "last_name": identity.last_name,
                    "role": identity.role or "Member",
                    "department": identity.department or "General",
                },
                institution,
                photo_url=str(photo_url),
            )
            for key, value in assets.items():
                setattr(identity, key, value)
            identity.status = "ready"
            session.add(identity)
            session.commit()
        except Exception as exc:  # noqa: BLE001
            session.rollback()
            errors.append(f"{row.get('external_id')}: {exc}")

    return IdentityBulkUploadResult(processed=processed, created_ids=created_ids, errors=errors)

