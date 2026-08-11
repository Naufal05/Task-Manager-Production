from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, UserCreate, UserRead, Token
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check for an existing account with this email BEFORE attempting insert --
    # gives a clean 400 instead of a raw DB unique-constraint error.
    existing = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),  # plaintext never stored
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    OAuth2PasswordRequestForm expects standard form fields (not JSON):
    'username' and 'password' -- this is a spec requirement, which is why
    we map OUR 'email' concept onto its 'username' field on the client side.
    This is also why we needed python-multipart installed.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).first()

    # Deliberately identical error whether the email doesn't exist OR the
    # password is wrong -- revealing "email not found" vs "wrong password"
    # tells an attacker which emails are registered. Same error, always.
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise invalid_credentials

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)