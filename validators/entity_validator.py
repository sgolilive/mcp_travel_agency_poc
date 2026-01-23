import inspect
from functools import wraps


def validate_entity(arg_name: str, dep_name: str, entity_class=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # 1. Extract the ID from arguments
            entity_id = kwargs.get(arg_name)
            if not entity_id:
                return f"❌ Error: {arg_name} is missing."

            # 2. Access the repository (e.g., self.deps.hotels)
            repo = getattr(self.deps, dep_name)

            # 3. Use the repository's own method
            doc = repo.find_by_id(entity_id)

            if not doc:
                return f"❌ {dep_name.title()} Error: ID {entity_id} not found."

            target_key = f"_injected_{dep_name.rstrip('s')}"
            setattr(self, target_key, entity_class.from_dict(doc) if entity_class else doc)

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator