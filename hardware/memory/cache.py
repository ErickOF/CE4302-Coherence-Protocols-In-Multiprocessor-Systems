class Cache:
    def __init__(self, associativity, state, size):
        self.__associativity = associativity
        self.__state = state
        self.__size = size
