class CacheL1:
    """This class model a L1 cache memory.
    """
    def __init__(self, associativity: int, size: int) -> None:
        """Constructor.

        Params
        --------------------------------------------------------------
            associativity: int.
                Cache associativity.
            size: int.
                Numbers of blocks.
        """
        self.__associativity = associativity
        self.__state = 'I'
        self.__size = size
        self.__mem = ['0000' for _ in range(self.__size)]

    def get_size(self) -> int:
        """This method returns the cache size.

        Returns
        --------------------------------------------------------------
            Cache size.
        """
        return self.__size

    def read(self, addr: int) -> str:
        """This method reads the data in a memory address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data in the specified memory address.
        """
        return self.__mem[addr]

