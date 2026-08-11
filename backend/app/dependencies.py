from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.database import get_session
from app.security import decode_access_token
from app.models import User

# This tells FastAPI: "expect a Bearer token, and the login endpoint that
# ISSUES tokens lives at /auth/login." Swagger UI uses tokenUrl to render
# the "Authorize" button and know where to send login attempts from /docs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """
    Runs before any endpoint that declares this as a dependency. FastAPI:
      1. Extracts the token from the 'Authorization: Bearer <token>' header
         (oauth2_scheme handles this -- raises 401 automatically if missing)
      2. We decode/verify it
      3. We look up the matching user in the DB
      4. If anything fails, we raise 401 -- the endpoint body never runs
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_email = payload.get("sub")  # "sub" (subject) = who this token represents
    if user_email is None:
        raise credentials_exception

    user = session.exec(select(User).where(User.email == user_email)).first()
    if user is None:
        raise credentials_exception

    return user