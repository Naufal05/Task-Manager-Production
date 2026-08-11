import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# CryptContext handles the actual bcrypt hashing algorithm details for us --
# bcrypt automatically incorporates a random "salt" per password, which is
# why hashing the same password twice gives two different hash strings.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    We NEVER decrypt a hash back into a password (bcrypt is one-way,
    by design). Instead, we hash the LOGIN attempt the same way and
    compare the two hashes.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Builds a JWT: a signed, tamper-proof string encoding who the user is
    and when the token expires. The client stores this and sends it back
    on every subsequent request via the Authorization header.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Verifies the token's signature (proving it was issued by US, not
    forged) and that it hasn't expired. Returns the decoded payload,
    or None if the token is invalid/expired/tampered with.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None