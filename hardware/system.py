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
        self.__memory: RAM = RAM.get_instance(16)
        self.__running: bool = False
        self.__instructions: list = [{}] * self.__size
        self.__old_instructions: list = [{}] * self.__size

    def __processor_controller(self, _id) -> None:
        """This method is used to control a single processor.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor ID.
        """
        data = '0' * 4

        while (self.__running):
            # Check if there's not instruction
            if not self.__cpus[_id].is_executing():
                # Set old instruction
                self.__old_instructions[_id] = self.__instructions[_id]

                # Get a new instruction
                instruction = self.__cpus[_id].generate_instruction()
                self.__instructions[_id] = instruction

            # Execute a new instruction
            self.__cpus[_id].excute()

            # Check if found the memory address
            if self.__cpus[_id].is_executing():
                state: str = self.__cpus[_id].get_state()

                if 'MISS' in state:
                    # Check if the memory bus is busy
                    if self.__memory.is_busy():
                        print(f'P{_id} waiting')
                        self.__cpus[_id].set_state('WAITING BUS')

                        # Wait a cycle
                        sleep(1 / self.__frequency)
                    else:
                        # Block the bus
                        self.__memory.block_bus()
                        print(f'P{_id} using the bus')

                        # Get current instruction
                        instr = self.__instructions[_id]

                        if self.__instructions[_id]['type'] == 'READ':
                            print(f'P{_id} is reading memory')

                            # Wait a cycle
                            sleep(1 / self.__frequency)

                            # Read the data from the memory
                            data = self.__memory.read(instr['address'])
                            # Write the date in cache
                            self.__cpus[_id].write(instr['address'], data)
                        else:
                            print(f'P{_id} is writing in memory')

                            # Wait a cycle
                            sleep(1 / self.__frequency)

                            # Write the date in memory and cache
                            self.__memory.write(instr['address'], instr['data'])
                            self.__cpus[_id].write(instr['address'], instr['data'])

                        # Free the bus
                        print(f'P{_id} released the bus')
                        self.__memory.free_bus()
                        self.__cpus[_id].finish()
                else:
                    # Wait a cycle
                    sleep(1 / self.__frequency)
            else:
                # Wait a cycle
                sleep(1 / self.__frequency)
    
    def get_instructions(self) -> list:
        """This method returns all instructions in the processors.

        Returns
        --------------------------------------------------------------
            A list with the current instruction in each processor.
        """
        return self.__instructions

    def get_old_instructions(self) -> list:
        """This method returns all old instructions in the processors.

        Returns
        --------------------------------------------------------------
            A list with the old instruction in each processor.
        """
        return self.__old_instructions

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

    def read_shared_memory(self, addr: str) -> str:
        """This method reads the data in a specific address of the
        shared memory.

        Params
        --------------------------------------------------------------
            addr: str.
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
