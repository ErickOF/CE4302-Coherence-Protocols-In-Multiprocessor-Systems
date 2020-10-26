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
        self.__state = 'NOP'

    def excute(self) -> None:
        """This method executes the current instruction in the
        processor.
        """
        self.__executing = True
        self.__state = 'EXECUTING'

        # Check if the instruction needs memory
        if self.__instruction['type'] != 'CALC':
            found: bool = False

            # Search for the cache block
            for i, block in enumerate(self.__cache_l1.get_mem()):
                # Check if the block is valid and the memory address
                # is the correct
                if block['state'] != 'I' and \
                    block['address'] == self.__instruction['address']:
                    found = True
                    break

            # Check if the cache block was found
            if found:
                # Check if it has to read
                if self.__instruction['type'] == 'READING':
                    self.__state = 'READING CACHE'
                else:
                    self.__state = 'WRITING IN CACHE'

                    # Get current data and state
                    block: dict = self.__cache_l1.read(self.__instruction['address'])
                    state: str = 'M'

                    # Check data state
                    if block['state'] == '':
                        state = ''

            # Cache miss
            else:
                self.__state = f'MISS {self.__instruction["address"]}'
        else:
            self.__state = 'COMPUTING'
            self.__executing = False

    def finish(self) -> None:
        """This method finished the execution of the instruction.
        """
        self.__executing = False

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
            address: str = bin(randint(0, 15))[2:]
            instr['address'] = '0' * (4 - len(address)) + address

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

    def get_id(self) -> int:
        """This method returns the processor identifier.

        Returns
        --------------------------------------------------------------
            The processor ID.
        """
        return self.__id

    def get_state(self) -> str:
        """This method returns the current processor state.

        Returns
        --------------------------------------------------------------
            The processor state.
        """
        return self.__state

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
        return self.__cache_l1.is_in_cache()

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

    def set_state(self, state: str) -> None:
        """This method sets the new state for the processor.

        Params
        --------------------------------------------------------------
            state: str.
                New state for the processor.
        """
        self.__state = state

    def write(self, addr: str, data: str, state: str = 'E') -> None:
        """This method writes the data in a cache address and change
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
        self.__cache_l1.write(addr, data, state)

