from argon2.exceptions import VerificationError, VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Token, UserRegistration, UserResponse
from app.models import User
from app.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", tags=["register"], response_model=UserResponse)
async def register(user: UserRegistration, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="user already exists")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_pw=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", tags=["login"], response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    try:
        verify_password(form_data.password, str(user.hashed_pw))
    except (VerifyMismatchError, VerificationError):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}
