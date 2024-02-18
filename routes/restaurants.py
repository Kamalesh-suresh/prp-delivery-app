"""
    This file consists of all methods to restaurant routes
"""

from typing import List, Union

from fastapi import APIRouter, HTTPException

from schema_model.restaurants import Restaurant

restaurants_router = APIRouter()


@restaurants_router.get("/")
async def get_allrestaurants():
    print("hello world")


@restaurants_router.post("/")
async def create_restaurant(restaurant: Restaurant):
    await restaurant.create()
    return restaurant
