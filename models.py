from beanie import Document
from pydantic import Field, BaseModel, validator, EmailStr
from typing import Union

class User(Document):
    name: str = Field(max_length=400)
    email: EmailStr = Field(max_length=400)
    phone_number: int
    pincode: int

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not (isinstance(value, int) and 10**9 <= value <= 10**10 - 1):
            raise ValueError("Phone number should be a 10-digit integer")
        return value

    @validator("pincode")
    def validate_pincode(cls, value):
        if not (isinstance(value, int) and 10**5 <= value <= 10**6 - 1):
            raise ValueError("Pincode should be a 6-digit integer")
        return value

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "name": "Kamalesh",
            "email": "kamalindevmiygos@gmail.com",
            "phone_number": 7358364675,
            "pincode": 600062,
        }

