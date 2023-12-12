"""
Module Description:

This module defines the User document model using Beanie and Pydantic.

"""


from beanie import Document
from pydantic import Field, validator, EmailStr


class UserMixin:
    """
    UserMixin class:

    This mixin class defines common attributes and validators for a user.

    Attributes:
        name (str): The name of the user.
        email (EmailStr): The email address of the user.
        phone_number (int): The phone number of the user (must be a 10-digit integer).
        pincode (int): The pincode of the user (must be a 6-digit integer).

    Validators:
        - validate_phone_number: Validates that the phone number is a 10-digit integer.
        - validate_pincode: Validates that the pincode is a 6-digit integer.
    """

    name: str = Field(max_length=400)
    email: EmailStr = Field(max_length=400)
    phone_number: int
    pincode: int

    @validator("phone_number")
    def validate_phone_number(cls, value):
        # pylint: disable=no-self-argument
        """
        This function is used to validate phone number has only 10  digits ao it can be valid
        """
        if not (isinstance(value, int) and 10**9 <= value <= 10**10 - 1):
            raise ValueError("Phone number should be a 10-digit integer")
        return value

    @validator("pincode")
    def validate_pincode(cls, value):
        # pylint: disable=no-self-argument
        """
        This function is used to validate pincode to have only 6  digits
        """
        if not (isinstance(value, int) and 10**5 <= value <= 10**6 - 1):
            raise ValueError("Pincode should be a 6-digit integer")
        return value


class User(Document,UserMixin):
    """
        This class imports usermixin and schema extras
    """
    class Settings:
        """
        This class has collection name
        """
        name = "users"

    class Config:
        """
        This class has a example user schema
        """
        schema_extra = {
            "name": "Kamalesh",
            "email": "kamalindevmiygos@gmail.com",
            "phone_number": 7358364675,
            "pincode": 600062,
        }
