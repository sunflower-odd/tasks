from pydantic import BaseModel, Field, EmailStr, validator
import re
from datetime import date

class CustomerRequest(BaseModel):
    last_name: str = Field()
    first_name: str = Field()
    birth_date: date
    phone: str
    email: EmailStr

    @validator("last_name", "first_name")
    def name_must_be_cyrillic(cls, v):
        if not re.fullmatch(r"[А-ЯЁ][а-яё]+", v):
            raise ValueError("Должно быть с заглавной буквы и содержать только кириллицу")
        return v

    @validator("phone")
    def phone_must_be_valid(cls, v):
        if not re.fullmatch(r"\+?\d{10,15}", v):
            raise ValueError("Номер телефона должен содержать 10-15 цифр, можно с +")
        return v