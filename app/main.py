from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Depends
)
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app import settings
from app.database import init_db
from app.models.user import (
    User,
    UserLogin,
    UserRegister,
)


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
    user = await user.save()
    return


@app.post('/login')
async def user_login(request: Request, login_data: UserLogin, Authorize: AuthJWT = Depends()):
    domain = request.base_url.hostname
    user = await User.get_or_none(domain=domain, email=login_data.email)
    if not ( user and user.verify_password(login_data.password) ):
        raise HTTPException(400, "Wrong credentials.")
    access_token = Authorize.create_access_token(
        user.id,
        user_claims={'domain':domain, 'email':user.email}
    )
    refresh_token = Authorize.create_refresh_token(
        user.id
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }



@app.get('/users')
async def user_list():
    users = await User.all()
    return users
