"""
E.L.Y.A.S.-A.I. Live Auth System v1
-----------------------------------

Upload to:
app/live_auth_routes.py

Then edit app/main.py:

from app.live_auth_routes import router as live_auth_router

app.include_router(live_auth_router, prefix="/api/v1")

IMPORTANT:
Place this include BEFORE existing api_router if your old /auth/login route exists.

Recommended order:
app.include_router(live_auth_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")
app.include_router(elyas_api_router, prefix="/api/v1")

Endpoints:
POST /api/v1/auth/login
GET  /api/v1/me
GET  /api/v1/auth/me
POST /api/v1/auth/logout

This version uses stdlib-only HS256 JWT.
No extra dependency required.
Later we will connect it to PostgreSQL users table and password hashing.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import base64
import hashlib
import hmac
import json
import os


router = APIRouter()

JWT_SECRET = os.getenv("ELYAS_JWT_SECRET", "elyas-alpha-institutional-secret-change-me")
JWT_ISSUER = "elyas-ai"
JWT_EXP_HOURS = int(os.getenv("ELYAS_JWT_EXP_HOURS", "24"))


USERS = {
    "investor@elyas-ai.com": {
        "id": 1,
        "email": "investor@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Investor",
        "role": "investor",
        "permissions": [
            "portfolio:read",
            "casks:read",
            "monitoring:read",
            "marketplace:read",
            "transactions:read"
        ]
    },
    "broker@elyas-ai.com": {
        "id": 2,
        "email": "broker@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Broker",
        "role": "broker",
        "permissions": [
            "clients:read",
            "otc:read",
            "casks:read",
            "monitoring:read",
            "marketplace:read"
        ]
    },
    "distillery@elyas-ai.com": {
        "id": 3,
        "email": "distillery@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Distillery",
        "role": "distillery",
        "permissions": [
            "warehouse:read",
            "production:read",
            "netsuite:read",
            "monitoring:read",
            "marketplace:write"
        ]
    },
    "private@elyas-ai.com": {
        "id": 4,
        "email": "private@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Private Seller",
        "role": "private",
        "permissions": [
            "assets:read",
            "assets:write",
            "offers:read",
            "monitoring:read",
            "marketplace:write"
        ]
    },
    "admin@elyas-ai.com": {
        "id": 5,
        "email": "admin@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Admin",
        "role": "admin",
        "permissions": [
            "admin:all",
            "users:read",
            "users:write",
            "casks:read",
            "casks:write",
            "marketplace:read",
            "marketplace:write"
        ]
    },
    "demo@elyas-ai.com": {
        "id": 1,
        "email": "demo@elyas-ai.com",
        "password": "demo123",
        "full_name": "Demo Investor",
        "role": "investor",
        "permissions": [
            "portfolio:read",
            "casks:read",
            "monitoring:read",
            "marketplace:read",
            "transactions:read"
        ]
    },
    "demo@investor.com": {
        "id": 1,
        "email": "demo@investor.com",
        "password": "demo123",
        "full_name": "Demo Investor",
        "role": "investor",
        "permissions": [
            "portfolio:read",
            "casks:read",
            "monitoring:read",
            "marketplace:read",
            "transactions:read"
        ]
    }
}


class LoginRequest(BaseModel):
    email: str
    password: str
    role: Optional[str] = None


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_jwt(payload: Dict[str, Any]) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    now = datetime.now(timezone.utc)
    full_payload = {
        **payload,
        "iss": JWT_ISSUER,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=JWT_EXP_HOURS)).timestamp())
    }

    header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url_encode(json.dumps(full_payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")

    signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        signing_input,
        hashlib.sha256
    ).digest()

    signature_b64 = b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_jwt(token: str) -> Dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        signing_input,
        hashlib.sha256
    ).digest()

    expected_b64 = b64url_encode(expected_signature)

    if not hmac.compare_digest(expected_b64, signature_b64):
        raise HTTPException(status_code=401, detail="Invalid token signature")

    payload = json.loads(b64url_decode(payload_b64).decode("utf-8"))

    exp = payload.get("exp")
    if exp and int(exp) < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=401, detail="Token expired")

    return payload


def get_user_from_authorization(authorization: Optional[str]) -> Dict[str, Any]:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ", 1)[1].strip()
    payload = decode_jwt(token)

    email = payload.get("email")
    if not email or email not in USERS:
        raise HTTPException(status_code=401, detail="User not found")

    user = USERS[email].copy()
    user.pop("password", None)
    return user


@router.post("/auth/login")
def login(payload: LoginRequest):
    email = payload.email.strip().lower()
    password = payload.password.strip()

    user = USERS.get(email)

    if not user or user.get("password") != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = payload.role or user.get("role")

    # prevent role escalation except admin
    if role != user.get("role") and user.get("role") != "admin":
        role = user.get("role")

    safe_user = user.copy()
    safe_user.pop("password", None)
    safe_user["role"] = role

    token = create_jwt({
        "sub": str(user["id"]),
        "email": user["email"],
        "role": role,
        "permissions": user.get("permissions", [])
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_hours": JWT_EXP_HOURS,
        "user": safe_user,
        "role": role
    }


@router.get("/me")
def me(authorization: Optional[str] = Header(default=None)):
    return get_user_from_authorization(authorization)


@router.get("/auth/me")
def auth_me(authorization: Optional[str] = Header(default=None)):
    return get_user_from_authorization(authorization)


@router.post("/auth/logout")
def logout():
    return {
        "status": "ok",
        "message": "Client should remove token from localStorage"
    }


@router.get("/auth/demo-users")
def demo_users():
    return [
        {"email": email, "role": user["role"], "password": "demo123"}
        for email, user in USERS.items()
        if email.endswith("@elyas-ai.com")
    ]
