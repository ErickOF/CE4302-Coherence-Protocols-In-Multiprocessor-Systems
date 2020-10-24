from threading import Thread
from time import sleep

from hardware.cpu.processor import Processor
from hardware.memory.ram import RAM


class System:
    """This class represents a multicore system.
    """
    def __init__(self, size: int, frequency: float = 1) -> None:
        """Constructor.

        Params
        --------------------------------------------------------------
            size: tuple.
                System size.
        """
        self.__cache_cycles: int = 2
        self.__frequency: float = frequency
        self.__ram_cycles: int = 8
        self.__size: int = size
        self.__cpus: list = [Processor(i + 1) for i in range(self.__size)]
        self.__memory: RAM = RAM(16)
        self.__running: bool = False
        self.__instructions: list = [{} for _ in range(self.__size)]

    def __processor_controller(self, _id) -> None:
        """This method is used to control a single processor.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor ID.
        """
        while (self.__running):
            # Get an instruction
            instruction = self.__cpus[_id].generate_instruction()
            self.__instructions[_id] = instruction

            sleep(1 / self.__frequency)
    
    def get_instructions(self) -> list:
        """This method returns all instructions in the processors.

        Returns
        --------------------------------------------------------------
            A list with the current instruction in each processor.
        """
        return self.__instructions

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

    def set_frequency(self, frequency: float) -> None:
        """This method sets the system clock frequency.

        Params
        --------------------------------------------------------------
            frequency: float.
                System clock frequency.
        """
        self.__frequency = frequency

    def turn_on(self) -> None:
        """This method starts the system.
        """
        # Run system
        self.__running: bool = True

        # Create and start threads
        self.__threads: list = [Thread(target=self.__processor_controller,
                                args=(i,)) for i in range(self.__size)]

        for thread in self.__threads:
            thread.start()

    def turn_off(self) -> None:
        """This method stops the system.
        """
        self.__running = False
