from numpy.random import normal
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
        self.__cycles: dict = { 'exec': 1, 'cache': 2, 'memory': 8 }
        self.__executing: bool = False
        self.__instruction: dict = {}
        self.__instruction_types: list = ['READ', 'WRITE', 'CALC']

    def excute(self) -> None:
        """This method executes the current instruction in the
        processor.
        """
        self.__cycles -= 1

    def generate_instruction(self) -> dict:
        """This method generates a random instruction.

        Returns
        --------------------------------------------------------------
            A dictionary representing all the instruction parts.
        """
        instr = { 'processor': self.__id }
        self.__cycles = { 'exec': 1, 'cache': 0, 'memory': 0 }

        # Generate a random number to get an instruction type
        number = normal()
        _type = self.__instruction_types[-1]

        if number < -1:
            _type = self.__instruction_types[0]
        elif number > 1:
            _type = self.__instruction_types[1]

        instr['type'] = _type

        # If the instruction is write or read
        if _type == 'READ' or _type == 'WRITE':
            # Insert the address
            address: str = bin(randint(0, self.get_cache_size() - 1))[2:]
            instr['address'] = '0'*(2 - len(address)) + address

            # Add two cycle to read cache blocks
            self.__cycles['cache'] = 2

            # If the instruction is write
            if _type == 'WRITE':
                # Generate a random value and put it as 16 bit value in hex
                data = hex(randint(0, 65535))[2:]
                instr['data'] = (4 - len(data)) * '0' + data

        self.__instruction = instr

        return instr

    def get_cache_l1(self) -> CacheL1:
        """This method returns the L1 Cache.

        Returns
        --------------------------------------------------------------
            L1 Cache.
        """
        return self.__cache_l1

    def get_cache_mem(self) -> dict:
        """This method returns all cache blocks.

        Returns
        --------------------------------------------------------------
            A list of dictionaries with all cache blocks information.
        """
        return self.__cache_l1.get_mem()
    
    def get_cache_size(self) -> int:
        """This method returns the L1 cache size.

        Returns
        --------------------------------------------------------------
            L1 Cache size.
        """
        return self.__cache_l1.get_size()

    def is_executing(self) -> bool:
        """This method returns True if the processor is executing an
        instruction, False otherwise.

        Returns
        --------------------------------------------------------------
            Returns True if the processor is executing an instruction,
            False otherwise.
        """
        return self.__executing

    def read_cache(self, addr: str) -> dict:
        """This method reads L1 cache address.

        Params
        --------------------------------------------------------------
            addr: str.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data and state in the specified memory address.
        """
        return self.__cache_l1.read(addr)

