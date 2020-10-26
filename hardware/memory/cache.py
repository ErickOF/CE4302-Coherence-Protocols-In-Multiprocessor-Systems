from random import randint
from threading import Lock


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
                'address': '0' * (4 - len(address)) + address,
                'available': Lock(),
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

    def is_in_cache(self, address: str) -> bool:
        """This method returns True if an address is in cache, False
        otherwise.

        Params
        --------------------------------------------------------------
            address: str.
                Address to be fetched.

        Returns
        --------------------------------------------------------------
            True if an address is in cache, False otherwise.
        """
        for block in self.__mem:
            if block['address'] == address:
                return True

        return False

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

    def write(self, addr: str, data: str, state: str = 'E') -> None:
        """This method writes the data in a memory address and change
        the block state.

        Params
        --------------------------------------------------------------
            addr: str.
                Memory address.
            data: str.
                Data to be written.
            state: str.
                New state for the cache block. Exclusive (E) by
                default.
        """
        found = False

        # Searching for the cache block
        for block in self.__mem:
            # Check if the block is valid and the memory address is
            # the correct
            if block['address'] == addr:
                block['data'] = data
                block['state'] = state
                found = True
                break

        # Check if the block was not in cache
        if not found:
            invalid = False

            # Searching for an invalid block
            for block in self.__mem:
                if block['state'] == 'I':
                    # Set the data in the invalid block
                    block['address'] = addr
                    block['data'] = data
                    block['state'] = state

                    invalid = True
                    break
            
            # If an invalid block does not exist
            if not invalid:
                # Get a random block
                block = randint(0, self.__size - 1)

                # Set the new information
                self.__mem[block] = {
                    'address': addr,
                    'available': Lock(),
                    'data': data,
                    'state': state
                }

