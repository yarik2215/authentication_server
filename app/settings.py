import os


# secret key
SECRET_KEY = os.environ.get("SECRET_KEY")

# Database settings
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite://db.sqlite")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}
