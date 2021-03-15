from tortoise.models import Model
from tortoise.fields import data
from tortoise.contrib.pydantic.creator import pydantic_model_creator


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
        pass

    def verify_password(self, raw_password: str) -> bool:
        pass


User_Pydantic = pydantic_model_creator(User, name='User')
