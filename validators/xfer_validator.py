from functools import wraps

from entities.transfer import Transfer

def validate_xfer(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # 1. Extract the ID from arguments
        transfer_id = kwargs.get('transfer_id')
        if not transfer_id:
            return await func(self, *args, **kwargs)

        transfer = self.deps.transfers.find_by_id(transfer_id)

        if not transfer:
            return f'Error: unable to find any cab details for the given {transfer_id} transfer_id.'

        setattr(self, '_injected_xfer', Transfer.from_dict(transfer))

        return await func(self, *args, **kwargs)

    return wrapper