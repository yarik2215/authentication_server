from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Depends
)
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.security import HTTPBearer

from app import settings
from app.database import init_db
from app.models.user import (
    User,
    UserLogin,
    UserRegister,
)
from app.utils.security import create_tokens


app = FastAPI()
# initialize database
init_db(app)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings.JwtSettings()


# Exception handlers

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exception: AuthJWTException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.message}
    )


# add endpoints here

@app.post('/register')
async def user_register(request: Request, user_data: UserRegister):
    domain = request.base_url.hostname
    user = User(**user_data.dict(), domain=domain)
    user.set_password(user_data.password2)
    await user.save()
    return


@app.post('/login')
async def user_login(request: Request, login_data: UserLogin, Authorize: AuthJWT = Depends()):
    domain = request.base_url.hostname
    user = await User.get_or_none(domain=domain, email=login_data.email)
    if not ( user and user.verify_password(login_data.password) ):
        raise HTTPException(400, "Wrong credentials.")
    return create_tokens(Authorize, user.id, domain = domain, email = user.email)


@app.get('/refresh', dependencies=[Depends(HTTPBearer())])
async def get_refresh_token(Authorize: AuthJWT = Depends()):
    """
    Use refresh token to update access and refresh token
    """
    Authorize.jwt_refresh_token_required()
    raw_jwt = Authorize.get_raw_jwt()
    return create_tokens(Authorize, **raw_jwt)


@app.get('/api/security_test', dependencies=[Depends(HTTPBearer())])
async def security_verify_domain(request: Request, Authorize: AuthJWT = Depends()):
    domain = request.base_url.hostname
    Authorize.jwt_required()
    user_domain = Authorize.get_raw_jwt().get('domain')
    if domain != user_domain:
        raise HTTPException(401)
    return {'status': 'success'}
