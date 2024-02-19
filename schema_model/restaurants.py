from typing import Optional

from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, validator

from schema_model.menus import Menu


class Restaurant(Document):
    """
    This class imports Restaurants_attributes and schema extras
    """

    title: str = Field(max_length=400)
    menu_id: PydanticObjectId
    service_pincodes: list[int]
    overall_rating: float
    cusine: str = Field(max_length=400)
    revision_id: Optional[PydanticObjectId] = None
    menu: Optional[Menu] = None  # Define menu field

    @validator("service_pincodes")
    def validate_pincodes(cls, value):
        # pylint: disable=no-self-argument
        """Validate service pincodes to ensure they have 6 digits."""
        for pincode in value:
            if not isinstance(pincode, int) or not 100000 <= pincode <= 999999:
                raise ValueError("Pincode must be an integer with 6 digits")
        return value

    class Settings:
        """
        This class has collection name
        """

        name = "restaurants"

    class Config:
        """
        This class has a example user schema
        """

        json_schema_extra = {
            "title": "SS Hyderabad Biriyani",
            "menu_id": {"$oid": "604be4c073c6b2dfceb6dbfe"},
            "service_pincodes": [600062, 600061],
            "overall_rating": 4.2,
            "cusine": "Indian",
        }
        arbitrary_types_allowed = True  # Allow arbitrary types like ObjectId


class UpdateRestaurant(BaseModel):
    title: str = Field(max_length=400)
    menu_id: Optional[PydanticObjectId]
    service_pincodes: list[int]
    overall_rating: int
    cusine: str = Field(max_length=400)
    revision_id: Optional[PydanticObjectId] = None
