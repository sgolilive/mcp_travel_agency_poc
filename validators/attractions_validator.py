from functools import wraps

from bson import ObjectId

from entities.transfer import Transfer

def validate_attractions(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        attractions = kwargs.get("attractions")

        # 1. Handle string vs list (Robustness)
        if isinstance(attractions, str):
            attractions = [attractions]

        if not attractions:
            return await func(self, *args, **kwargs)

        response = []
        # 2. Basic ID validation
        valid_object_ids = []
        for attr_id in attractions:
            if len(str(attr_id)) == 24:
                valid_object_ids.append(ObjectId(attr_id))
            else:
                response.append(f'invalid attraction id. ignoring the attraction with id {attr_id}')

        # 3. Verify they exist in the DB (Optional but recommended)
        existing = list(self.deps.attractions.collection.find(
            {"_id": {"$in": valid_object_ids}}
        ))

        if len(existing) != len(valid_object_ids):
            response.append("❌ One or more selected attraction IDs were not found in our database.")

        # Update kwargs so the tool receives the cleaned list
        kwargs["attractions"] = valid_object_ids
        return await func(self, *args, **kwargs)

    return wrapper