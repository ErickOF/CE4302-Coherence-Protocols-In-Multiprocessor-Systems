from random import randint

from hardware.memory.cache import CacheL1


class Processor():
    """This class models a processor with a L1 Cache
    """
    def __init__(self, _id: int):
        """Constructor.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor identifier.
        """
        self.__id: int = _id
        self.__cache_l1: CacheL1 = CacheL1(2, 4)
        self.__instruction_types: list = ['READ', 'WRITE', 'CALC']

    def generate_instruction(self) -> dict:
        """This method generates a random instruction.

        Returns
        --------------------------------------------------------------
            A dictionary representing all the instruction parts.
        """
        instr = { 'processor': self.__id }

        # Generate a random number to get an instruction type
        _type = self.__instruction_types[randint(0,
                                        len(self.__instruction_types) - 1)]
        instr['type'] = _type

        # If the instruction is write or read
        if _type == 'READ' or _type == 'WRITE':
            # Insert the address
            instr['address'] = bin(randint(0, self.get_cache_size() - 1))[2:]

            # If the instruction is write
            if _type == 'WRITE':
                # Generate a random value and put it as 16 bit value in hex
                data = hex(randint(0, 65535))[2:]
                instr['data'] = (4 - len(data)) * '0' + data

        return instr

    def get_cache_l1(self) -> CacheL1:
        """This method returns the L1 Cache.

        Returns
        --------------------------------------------------------------
            L1 Cache.
        """
        return self.__cache_l1
    
    def get_cache_size(self) -> int:
        """This method returns the L1 cache size.

        Returns
        --------------------------------------------------------------
            L1 Cache size.
        """
        return self.__cache_l1.get_size()

    def read_cache(self, addr: int) -> dict:
        """This method reads L1 cache address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data and state in the specified memory address.
        """
        return self.__cache_l1.read(addr)

