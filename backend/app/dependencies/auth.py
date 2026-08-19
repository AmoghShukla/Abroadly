from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth import read_access_token

security = HTTPBearer()


def get_current_email(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    return read_access_token(credentials.credentials)
