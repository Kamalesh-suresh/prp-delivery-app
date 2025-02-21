"""
    This file consists of all methods to restaurant routes
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status

from schema_model.restaurants import Restaurant, RestaurantCreate

restaurants_router = APIRouter()


@restaurants_router.get("/")
async def get_all_restaurants(
    count: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    search: str = Query(None),
    sort: str = Query("desc", regex=r"^(asc|desc)$"),
    pincode: Optional[int] = Query(None),
):
    print("try ")
    try:
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
                    "service_pincodes": 1,
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

        if pincode:
            pipeline.insert(0, {"$match": {"service_pincodes": pincode}})

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

        total_count = await Restaurant.count()
        restaurants_with_menus = await Restaurant.aggregate(pipeline).to_list()
        print(restaurants_with_menus)
        return {"total_count": total_count, "restaurants": restaurants_with_menus}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching restaurants.",
        ) from e


@restaurants_router.get("/{restaurant_id}")
async def get_byId(restaurant_id: PydanticObjectId):
    try:
        pipeline = [
            {"$match": {"_id": restaurant_id}},
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
                    "service_pincodes": 1,
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
        result = await Restaurant.aggregate(pipeline).to_list()
        if result:
            return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching restaurants.",
        ) from e


@restaurants_router.post("/")
async def create_restaurant(restaurant: RestaurantCreate):
    await restaurant.create()
    return restaurant


@restaurants_router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: PydanticObjectId):
    result = await Restaurant.find_one(Restaurant.id == restaurant_id)
    if result:
        await result.delete()
        return {"message": "Restaurant deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )


# @restaurants_router.get("/{pincode}")
# async def get_restaurants_by_pincode(pincode:int):
