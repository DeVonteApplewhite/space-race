"""
base.py.
"""

# Globals
NOT_IMPLEMENTED_MESSAGE = 'Method not implemented. Please implement the method.'


class BasePlayerState:
    def __init__(self, *args, **kwargs):
        pass

    def handle_input(self, event):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def update(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)


class BaseAIStrategy:
    def strategy(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)
