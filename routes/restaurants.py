"""
    This file consists of all methods to restaurant routes
"""

from typing import List, Union

from beanie import PydanticObjectId
from fastapi import APIRouter, Query

from schema_model.menus import Menu
from schema_model.restaurants import Restaurant

restaurants_router = APIRouter()


@restaurants_router.get("/")
async def get_all_restaurants(
    count: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    search: str = Query(None),
    sort: str = Query("desc", regex=r"^(asc|desc)$"),
):
    skip = (page - 1) * count

    sort_stage = {"title": 1 if sort == "asc" else -1}

    pipeline = [
        {"$sort": sort_stage},
        {"$skip": skip},
        {"$limit": count},
        {
            "$lookup": {
                "from": "menus",
                "localField": "menu_id",
                "foreignField": "_id",
                "as": "menu",
            }
        },
        {"$unwind": "$menu"},
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "title": 1,
                "description": 1,
                "menu": {
                    "cusine": 1,
                    "starters": 1,
                    "drinks": 1,
                    "breads": 1,
                    "main_course": 1,
                },
            }
        },
    ]

    if search:
        pipeline.insert(
            0,
            {
                "$search": {
                    "index": "default",
                    "autocomplete": {"query": search, "path": "title"},
                }
            },
        )

    menu_pipeline = [
        {
            "$lookup": {
                "from": "menus",
                "localField": "menu_id",
                "foreignField": "_id",
                "as": "menu",
            },
        },
        {"$unwind": "$menu"},
    ]

    total_count = await Restaurant.count()
    menu_lookup = await Restaurant.aggregate(menu_pipeline).to_list()
    print(menu_lookup)
    restaurants_with_menus = await Restaurant.aggregate(pipeline).to_list()

    return {"total_count": total_count, "restaurants": restaurants_with_menus}


@restaurants_router.get("/{restaurant_id}")
async def get_byId(restaurant_id: PydanticObjectId):
    result = await Restaurant.find_one(Restaurant.id == restaurant_id)
    return result


@restaurants_router.post("/")
async def create_restaurant(restaurant: Restaurant):
    await restaurant.create()
    return restaurant
