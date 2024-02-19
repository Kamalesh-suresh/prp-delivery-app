"""
    This file consists of all methods to restaurant routes
"""

from typing import List, Union

from beanie import PydanticObjectId
from fastapi import APIRouter

from schema_model.menus import Menu
from schema_model.restaurants import Restaurant

restaurants_router = APIRouter()


@restaurants_router.get("/")
async def get_allrestaurants():
    restaurants = await Restaurant.find_all().to_list()
    for restaurant in restaurants:
        menu_id = restaurant.menu_id
        menu = await Menu.find_one(Menu.id == menu_id)
        if menu:
            restaurant.menu = menu
    return restaurants


@restaurants_router.get("/{restaurant_id}")
async def get_byId(restaurant_id: PydanticObjectId):
    result = await Restaurant.find_one(Restaurant.id == restaurant_id)
    return result


@restaurants_router.post("/")
async def create_restaurant(restaurant: Restaurant):
    await restaurant.create()
    return restaurant
