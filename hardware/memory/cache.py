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
        self.__size = size
        # Memory blocks
        self.__mem = []

        for i in range(self.__size):
            # Compute address
            address: str = bin(i)[2:]

            self.__mem.append({
                'address': '0'*(2 - len(address)) + address,
                'data': '0000',
                'state': 'I' 
            })

    def get_mem(self) -> list:
        """This method returns all cache blocks.

        Returns
        --------------------------------------------------------------
            A list of dictionaries with all cache blocks information.
        """
        return self.__mem

    def get_size(self) -> int:
        """This method returns the cache size.

        Returns
        --------------------------------------------------------------
            Cache size.
        """
        return self.__size

    def read(self, addr: str) -> dict:
        """This method reads the data in a memory address and returns
        its contants and its state.

        Params
        --------------------------------------------------------------
            addr: str.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data and the state in the specified memory address.
        """
        for block in self.__mem:
            if block['address'] == addr:
                return block

        return {}

