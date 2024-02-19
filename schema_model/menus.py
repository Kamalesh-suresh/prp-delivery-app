import random
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, validator


class MenuItem(BaseModel):
    name: str
    price: float
    rating: int


class Menu(Document):
    cusine: str
    starters: List[MenuItem]
    drinks: List[MenuItem]
    breads: List[MenuItem]
    main_course: List[MenuItem]
    revision_id: Optional[PydanticObjectId] = None

    @validator("cusine")
    def validate_cusine(cls, value):
        # pylint: disable=no-self-argument
        if not isinstance(value, str):
            raise ValueError("Cuisine must be a string")
        return value

    class Settings:
        name = "menus"

    class Config:
        json_schema_extra = {
            "cusine": "Italian",
            "starters": [
                {"name": "Bruschetta", "price": 8.99, "rating": random.randint(1, 5)},
                {
                    "name": "Caprese Salad",
                    "price": 9.99,
                    "rating": random.randint(1, 5),
                },
            ],
            "drinks": [
                {"name": "Chianti", "price": 15.99, "rating": random.randint(1, 5)},
                {"name": "Espresso", "price": 2.99, "rating": random.randint(1, 5)},
            ],
            "breads": [
                {"name": "Focaccia", "price": 5.99, "rating": random.randint(1, 5)},
                {"name": "Ciabatta", "price": 4.99, "rating": random.randint(1, 5)},
            ],
            "main_course": [
                {
                    "name": "Margherita Pizza",
                    "price": 10.99,
                    "rating": random.randint(1, 5),
                },
                {
                    "name": "Pasta Carbonara",
                    "price": 13.99,
                    "rating": random.randint(1, 5),
                },
            ],
        }
