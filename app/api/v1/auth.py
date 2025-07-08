from fastapi import APIRouter, status, HTTPException, Depends
from app.models.pydantic_schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    LogoutRequest,
    LogoutResponse,
)
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

router = APIRouter()

# In-memory user store for demo
fake_users = {}
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post(
    "/register/", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(request: RegisterRequest):
    if request.email in fake_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = {
        "id": str(len(fake_users) + 1),
        "username": request.username,
        "email": request.email,
        "password": get_password_hash(request.password),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    fake_users[request.email] = user
    return RegisterResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )


@router.post("/login/", response_model=LoginResponse)
def login(request: LoginRequest):
    user = fake_users.get(request.email)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        {"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token({"sub": user["email"]})
    return LoginResponse(access=access_token, refresh=refresh_token)


@router.post("/refresh/", response_model=RefreshResponse)
def refresh_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type")
        email = payload.get("sub")
        if email not in fake_users:
            raise HTTPException(status_code=401, detail="User not found")
        access_token = create_access_token(
            {"sub": email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return RefreshResponse(access_token=access_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout/", response_model=LogoutResponse)
def logout(request: LogoutRequest):
    # For stateless JWT, logout is handled on client side (token discard)
    # To support blacklist, would need persistent storage
    return LogoutResponse(success=True)
