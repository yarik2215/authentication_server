from fastapi import (
    FastAPI,
    Request
)
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


from authentication_service import settings
from authentication_service.database import init_db
from authentication_service.views import router


app = FastAPI()
# initialize database
init_db(app)

app.include_router(router)


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
