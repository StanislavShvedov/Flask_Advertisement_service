import pydantic
from pydantic import BaseModel, ValidationError
from errors import HttpError

class UserBase(BaseModel):
    name: str
    password: str
    email: str

    @pydantic.field_validator('password')
    @classmethod
    def check_password(cls, val: str):
        if len(val) < 4:
            raise ValueError('Пароль слишков короткий')
        elif not any(symb.isdigit() for symb in val):
            raise ValueError('В пароле должна содержаться хотя бы одна цифра')
        elif not any(symb.isalpha() for symb in val):
            raise ValueError('В пароле должна содержаться хотя бы одна буква')
        elif not any(symb.isupper() for symb in val):
            raise ValueError('В пароле должна содержаться хотя бы одна буква в верхнем регистре')
        return val

    @pydantic.field_validator('email')
    @classmethod
    def check_email(cls, val: str):
        if '@' not in val or '.' not in val:
            raise ValueError('Не правильный формат адреса электронной почты')
        return val

class CreateUserRequest(UserBase):
    pass


class UpdateUserRequest(UserBase):
    name: str | None = None
    password: str | None = None
    email: str | None = None

def validate(json_data: dict, cls_schema: type[CreateUserRequest] | type[UpdateUserRequest]):
    try:
        schema = cls_schema(**json_data)
        return schema.dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)

