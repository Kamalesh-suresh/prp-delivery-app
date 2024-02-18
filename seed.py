import random

from pymongo import MongoClient

from config import MONGODB_CONNECTION_STRING

# Connect to MongoDB
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client["foody"]

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

# Sample data for menu
menu_data = [
    {
        "menu_id": None,  # We'll update this later
        "starters": [
            {"name": "Starter A", "price": 10.99, "rating": random.randint(1, 5)},
            {"name": "Starter B", "price": 8.99, "rating": random.randint(1, 5)},
        ],
        "drinks": [
            {"name": "Drink A", "price": 5.99, "rating": random.randint(1, 5)},
            {"name": "Drink B", "price": 7.99, "rating": random.randint(1, 5)},
        ],
        "breads": [
            {"name": "Bread A", "price": 3.99, "rating": random.randint(1, 5)},
            {"name": "Bread B", "price": 4.99, "rating": random.randint(1, 5)},
        ],
        "main_course": [
            {"name": "Main Course A", "price": 15.99, "rating": random.randint(1, 5)},
            {"name": "Main Course B", "price": 18.99, "rating": random.randint(1, 5)},
        ],
    },
    # Add more menu items as needed
]

# Insert menu data into the menu collection
menu_collection = db["menu"]
menu_ids = menu_collection.insert_many(menu_data).inserted_ids

# Update menu_id in restaurants data with actual menu_ids
for restaurant_id in restaurants_ids:
    menu_id = random.choice(menu_ids)
    restaurants_collection.update_one(
        {"_id": restaurant_id}, {"$set": {"menu_id": menu_id}}
    )

print("Database populated successfully!")
