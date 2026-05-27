import httpx
from jose import JWTError, jwt

from app.config import settings
from app.schemas import TokenUser


def verify_token_locally(token: str) -> TokenUser | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        if "sub" not in payload:
            return None
        return TokenUser(
            user_id=int(payload["sub"]),
            username=payload.get("username", ""),
        )
    except JWTError:
        return None


async def verify_token_via_auth_service(token: str) -> TokenUser | None:
    url = f"{settings.auth_service_url.rstrip('/')}/auth/verify"
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json={"token": token})
        if response.status_code != 200:
            return None
        data = response.json()
        if not data.get("valid"):
            return None
        return TokenUser(user_id=data["user_id"], username=data.get("username", ""))


async def verify_token(token: str) -> TokenUser | None:
    if settings.verify_via_auth_service:
        return await verify_token_via_auth_service(token)
    return verify_token_locally(token)
