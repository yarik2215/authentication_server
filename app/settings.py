import os
from datetime import timedelta
from pydantic import BaseModel


# JWT
class JwtSettings(BaseModel):
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")
    authjwt_access_token_expires: timedelta = timedelta(hours=24)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)


# Database settings

# list where to look up for models
MODELS = [
    "app.models.user"
]

DATABASE_URL = os.environ.get("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                *MODELS,
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}


# password settings
PASWORD_LENGTH = 4
