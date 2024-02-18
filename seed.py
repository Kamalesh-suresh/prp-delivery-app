import random

from pymongo import MongoClient

from config import MONGODB_CONNECTION_STRING

# Connect to MongoDB
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client["foody"]

menu_data = [
    {
        "cusine": "Indian",
        "starters": [
            {"name": "Samosa", "price": 5.99, "rating": random.randint(1, 5)},
            {"name": "Paneer Tikka", "price": 7.99, "rating": random.randint(1, 5)},
        ],
        "drinks": [
            {"name": "Lassi", "price": 3.99, "rating": random.randint(1, 5)},
            {"name": "Masala Chai", "price": 2.99, "rating": random.randint(1, 5)},
        ],
        "breads": [
            {"name": "Naan", "price": 2.99, "rating": random.randint(1, 5)},
            {"name": "Roti", "price": 1.99, "rating": random.randint(1, 5)},
        ],
        "main_course": [
            {"name": "Butter Chicken", "price": 12.99, "rating": random.randint(1, 5)},
            {"name": "Biryani", "price": 14.99, "rating": random.randint(1, 5)},
        ],
    },
    {
        "cusine": "Italian",
        "starters": [
            {"name": "Bruschetta", "price": 8.99, "rating": random.randint(1, 5)},
            {"name": "Caprese Salad", "price": 9.99, "rating": random.randint(1, 5)},
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
            {"name": "Pasta Carbonara", "price": 13.99, "rating": random.randint(1, 5)},
        ],
    },
    # Add more cuisine items as needed
]

# Insert menu data into the menu collection
menu_collection = db["menu"]
menu_ids = menu_collection.insert_many(menu_data).inserted_ids

# Sample data for restaurants
restaurants_data = [
    {
        "title": "Restaurant A",
        "cusine": "Indian",
        "rating": random.randint(1, 5),
        "menu_id": None,  # We'll update this later
        "service_pincodes": [600001, 600002, 600003],
    },
    {
        "title": "Restaurant B",
        "cusine": "Italian",
        "rating": random.randint(1, 5),
        "menu_id": None,  # We'll update this later
        "service_pincodes": [600004, 600005, 600006],
    },
    # Add more restaurants as needed
]

# Insert restaurants data into the restaurants collection
restaurants_collection = db["restaurants"]
restaurants_ids = restaurants_collection.insert_many(restaurants_data).inserted_ids

# Assign menu_id to each restaurant based on cuisine
for restaurant_id in restaurants_ids:
    restaurant = restaurants_collection.find_one({"_id": restaurant_id})
    cuisine = restaurant["cusine"]
    menu_id = menu_collection.find_one({"cusine": cuisine})["_id"]
    restaurants_collection.update_one(
        {"_id": restaurant_id}, {"$set": {"menu_id": menu_id}}
    )

print("Database populated successfully!")
