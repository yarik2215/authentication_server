from typing import Optional, Dict, Union
from fastapi import (
    Request,
    HTTPException,
    Depends,
    APIRouter
)
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from authentication_service.models.user import (
    User,
    UserLogin,
    UserRegister,
)
from authentication_service.utils.security import create_tokens


router = APIRouter()

# custom types
RawJwt = Optional[Dict[str,Union[str,int,bool]]]

def verify_token_and_domain(request: Request, Authorize: AuthJWT = Depends(), dummy = Depends(HTTPBearer())) -> RawJwt:
    """
    Check JWT access token and domain, if domain from request anf from token are equal, than pass the validation.
    Argument dummy needs only for generating the documentation.
    """
    domain = request.base_url.hostname
    Authorize.jwt_required()
    raw_jwt = Authorize.get_raw_jwt()
    user_domain = raw_jwt.get('domain')
    if domain != user_domain:
        raise HTTPException(401)
    return raw_jwt

@router.post('/register')
async def user_register(request: Request, user_data: UserRegister):
    domain = request.base_url.hostname
    user = User(**user_data.dict(), domain=domain)
    user.set_password(user_data.password2)
    await user.save()


@router.post('/login')
async def user_login(request: Request, login_data: UserLogin, Authorize: AuthJWT = Depends()):
    domain = request.base_url.hostname
    user = await User.get_or_none(domain=domain, email=login_data.email)
    if not ( user and user.verify_password(login_data.password) ):
        raise HTTPException(400, "Wrong credentials.")
    return create_tokens(Authorize, user.id, domain = domain, email = user.email)


@router.get('/refresh', dependencies=[Depends(HTTPBearer())])
async def get_refresh_token(Authorize: AuthJWT = Depends()):
    """
    Use refresh token to update access and refresh token
    """
    Authorize.jwt_refresh_token_required()
    raw_jwt = Authorize.get_raw_jwt()
    return create_tokens(Authorize, **raw_jwt)


@router.get('/api/security_test')
async def security_verify_domain(raw_token: RawJwt = Depends(verify_token_and_domain)):    
    return {'status': 'success'}
