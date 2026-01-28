import random

from db.attractions_mongo_client import AttractionsMongoClient
from db.hubs_mongo_client import HubsMongoClient

def generate_local_attractions(hubs: HubsMongoClient, attractions: AttractionsMongoClient):
    # Templates for data generation
    data_templates = {
        "Sightseeing": [
            {"name": "Historical Old Town", "category": "Cultural"},
            {"name": "Skydeck Observatory", "category": "Modern"},
            {"name": "Central Public Park", "category": "Nature"},
            {"name": "National Museum", "category": "Educational"}
        ],
        "Food": [
            {"name": "Street Food Market", "category": "Authentic"},
            {"name": "Michelin Star Bistro", "category": "Fine Dining"},
            {"name": "Riverside Cafe", "category": "Relaxing"},
            {"name": "Night Food Street", "category": "Nightlife"}
        ],
        "Activity": [
            {"name": "Guided City Walk", "category": "Adventure"},
            {"name": "Cooking Masterclass", "category": "Interactive"},
            {"name": "Sunset Boat Tour", "category": "Romantic"},
            {"name": "Local Craft Workshop", "category": "Creative"}
        ]
    }

    food_items = ["Local Speciality", "Signature Cocktail", "Fusion Dish", "Traditional Dessert"]

    attraction_data = []

    for hub in hubs.find_all_hubs():
        # Create ~50 records per hub (mixed types)
        for i in range(50):
            exp_type = random.choice(list(data_templates.keys()))
            template = random.choice(data_templates[exp_type])

            experience = {
                "city_hub": hub,
                "name": f"{hub} {template['name']} {random.randint(1, 100)}",
                "type": exp_type,  # Sightseeing, Food, or Activity
                "category": template["category"],
                "description": f"A must-visit {template['category'].lower()} experience in the heart of {hub}.",
                "rating": round(random.uniform(4.0, 5.0), 1),
                "avg_cost_pp": random.randint(500, 5000),  # Price per person
                "details": {
                    "must_try": random.sample(food_items, 2) if exp_type == "Food" else None,
                    "duration": f"{random.randint(1, 4)} hours",
                    "best_time": random.choice(["Morning", "Afternoon", "Evening", "Late Night"])
                },
                "tags": [template["category"], exp_type, hub]
            }
            attraction_data.append(experience)

    attractions.insert_records(attraction_data)