class CoroWrapper:
    def __init__(self, coro):
        self._it = iter(coro)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            next(self._it) # skip spurious entries
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
