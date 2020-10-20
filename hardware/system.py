from hardware.cpu.processor import Processor
from hardware.memory.ram import RAM


class System:
    """This class represents a multicore system.
    """
    def __init__(self, size: int) -> None:
        """Constructor.

        Params
        --------------------------------------------------------------
            size: tuple.
                System size.
        """
        self.__size = size
        self.__cpus: list = [Processor() for _ in range(self.__size)]
        self.__memory: RAM = RAM(16)

    def get_size(self) -> int:
        """This method returns the system size.

        Returns
        --------------------------------------------------------------
            The system size.
        """
        return self.__size
    
    def get_shared_mem_size(self) -> int:
        """This method returns the shared memory size.

        Returns
        --------------------------------------------------------------
            The shared memory size.
        """
        return self.__memory.get_size()

    def get_processor(self, pos: int) -> Processor:
        """This method returns a specific processor by its index.

        Params
        --------------------------------------------------------------
            pos: int.
                Position of the processor.

        Returns
        --------------------------------------------------------------
            The processor in the given position.
        """
        return self.__cpus[pos]

    def read_shared_memory(self, addr: int) -> str:
        """This method reads the data in a specific address of the
        shared memory.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data in the specific address of the shared memory.
        """
        return self.__memory.read(addr)

