from fastapi import APIRouter, HTTPException, status

from app.core.auth import create_access_token, hash_password, verify_password
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["authentication"])
USERS: dict[str, dict[str, str]] = {}


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> AuthResponse:
    email = payload.email.lower()
    if email in USERS:
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    USERS[email] = {"name": payload.name, "email": email, "password": hash_password(payload.password)}
    return AuthResponse(access_token=create_access_token(email), user={"name": payload.name, "email": email})


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    user = USERS.get(payload.email.lower())
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return AuthResponse(access_token=create_access_token(user["email"]), user={"name": user["name"], "email": user["email"]})
