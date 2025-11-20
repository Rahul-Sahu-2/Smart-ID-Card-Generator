from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..database import get_session
from ..models import User
from ..schemas.auth import AuthRequest, AuthResponse, UserCreate
from ..services.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register_user(payload: UserCreate, session=Depends(get_session)):
    exists = session.exec(select(User).where(User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        institution_id=payload.institution_id,
        hashed_password=get_password_hash(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(str(user.id))
    return AuthResponse(access_token=token, role=user.role, full_name=user.full_name)


@router.post("/login", response_model=AuthResponse)
def login(payload: AuthRequest, session=Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return AuthResponse(access_token=token, role=user.role, full_name=user.full_name)

