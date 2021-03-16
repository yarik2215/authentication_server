from tortoise.models import Model
from tortoise.fields import data
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, EmailStr, validator

from app import settings
from app.utils.security import hash_password, verify_password


class User(Model):
    email = data.CharField(max_length=255)
    domain = data.CharField(max_length=511)
    hashed_password = data.CharField(max_length=511, null=True)
    created = data.DatetimeField(
        auto_now_add=True,
        description="Created datetime"
    )

    class Meta:
        unique_together = (('email', 'domain'))

    class PydanticMeta:
        exclude = ('hashed_password')

    def __str__(self) -> str:
        return f'{self.email}|{self.domain}'

    def set_password(self, raw_password: str) -> None:
        self.hashed_password = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return verify_password(raw_password, self.hashed_password)


User_Pydantic = pydantic_model_creator(User, name='User')


class UserRegister(BaseModel):
    email: EmailStr
    password1: str
    password2: str

    @validator('password2')
    def validate_password(cls, password2: str, values: dict) -> str:
        if password2 != values.get('password1'):
            raise ValueError(
                "Passwords not equal"
            )
        if len(password2) < settings.PASWORD_LENGTH:
            raise ValueError(
                f"Password should be minimum {settings.PASWORD_LENGTH} symbols"
            )
        return password2


class UserLogin(BaseModel):
    email: EmailStr
    password: str
