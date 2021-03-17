from typing import Union
from fastapi_jwt_auth.auth_jwt import AuthJWT
from passlib.context import CryptContext
from pydantic.main import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


class JwtTokenPair(BaseModel):
    access_token: str
    refresh_token: str


def create_tokens(Authorize: AuthJWT, sub: Union[str, int], *, email: str, domain: str, **kwargs) -> JwtTokenPair:
    additional_data = {'email': email, 'domain': domain}
    return JwtTokenPair(
        access_token = Authorize.create_access_token(sub, user_claims=additional_data),
        refresh_token = Authorize.create_refresh_token(sub, user_claims=additional_data)
    )
