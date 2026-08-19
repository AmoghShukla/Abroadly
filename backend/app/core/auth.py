"""Small dependency-free token service for the MVP.

Replace the in-memory stores with database repositories before deploying.
"""
import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status

from app.core.config import get_settings


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    salt, digest = stored.split("$", 1)
    return hmac.compare_digest(hash_password(password, salt), stored)


def _encode(value: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).rstrip(b"=").decode()


def _decode(value: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)))


def create_access_token(email: str) -> str:
    settings = get_settings()
    header = _encode({"alg": "HS256", "typ": "JWT"})
    payload = _encode({"sub": email, "exp": int((datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)).timestamp())})
    signature = hmac.new(settings.jwt_secret_key.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    return f"{header}.{payload}.{base64.urlsafe_b64encode(signature).rstrip(b'=').decode()}"


def read_access_token(token: str) -> str:
    try:
        header, payload, signature = token.split(".")
        expected = hmac.new(get_settings().jwt_secret_key.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
        actual = base64.urlsafe_b64decode(signature + "=" * (-len(signature) % 4))
        claims = _decode(payload)
        if not hmac.compare_digest(expected, actual) or claims["exp"] < datetime.now(UTC).timestamp():
            raise ValueError
        return claims["sub"]
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token") from exc
