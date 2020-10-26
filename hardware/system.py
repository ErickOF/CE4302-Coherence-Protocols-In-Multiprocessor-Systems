from random import shuffle
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
        self.__default_time: float = 0.5
        self.__frequency: float = frequency
        self.__size: int = size
        self.__cpus: list = [Processor(i + 1) for i in range(self.__size)]
        self.__memory: RAM = RAM.get_instance(16)
        self.__memory.clear()
        self.__running: bool = False
        self.__instructions: list = [{}] * self.__size
        self.__old_instructions: list = [{}] * self.__size

    def __change_state_miss(self, _id: int, state: str, action: str,
                            address: str) -> None:
        """This method changes to the next state for a cache block.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor ID.
            state: str.
                Current cache block state.
            action: str.
                Action to be executed.
            address: str.
                Memory address.

        Returns
        --------------------------------------------------------------
            The new state for the cache block.
        """
        new_state = state

        if state == 'I':
            if action == 'READ':
                found = False

                # Search in each cache
                for cpu in self.__cpus:
                    if cpu.get_id() != _id:
                        for block in cpu.get_cache_mem():
                            # Check if the block is valid and the
                            # address is the same
                            if block['address'] == address and \
                                block['state'] != 'I':
                                # If the cache block is Exclusive
                                # it must change to Shared
                                if block['state'] == 'E':
                                    block['state'] = 'S'
                                # If the cache block is Modified
                                # it must change to Owned
                                elif block['state'] == 'M':
                                    block['state'] = 'O'

                                found = True

                # If a cache block was found, the new state must be
                # Shared, otherwise Exclusive
                new_state = 'S' if found else 'E'
            else:
                # Search in each cache
                for cpu in self.__cpus:
                    if cpu.get_id() != _id:
                        for block in cpu.get_cache_mem():
                            # Check if the address is the same
                            if block['address'] == address:
                                # Then invalid the block
                                block['state'] = 'I'

                new_state = 'M'

        return new_state

    def __control_processor(self, _id: int, wait: bool) -> None:
        """This method is used to control a single processor.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor ID.
            wait: bool.
                Indicates if the system has to wait each cycle.
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
                        print(f'P{_id} is waiting')
                        self.__cpus[_id].set_state('WAITING BUS')

                        # Wait a cycle
                        if wait:
                            sleep(1 / self.__frequency)
                        else:
                            sleep(self.__default_time)
                            self.__running = False
                    else:
                        # Block the bus
                        self.__memory.block_bus()
                        print(f'P{_id} is using the bus')

                        # Get current instruction
                        instr = self.__instructions[_id]

                        if self.__instructions[_id]['type'] == 'READ':
                            print(f'P{_id} is reading memory')
                            self.__cpus[_id].set_state('READING MEMORY')

                            # Wait a cycle
                            if wait:
                                sleep(1 / self.__frequency)
                            else:
                                sleep(self.__default_time)
                                self.__running = False

                            # Read the data from the memory
                            data = self.__memory.read(instr['address'])
                            # Get the new state
                            s = self.__change_state_miss(_id, 'I', 'READ',
                                                    instr['address'])
                            # Write the date in cache
                            self.__cpus[_id].write(instr['address'], data, s)
                        else:
                            print(f'P{_id} is writing in memory')
                            self.__cpus[_id].set_state('WRITING IN MEMORY')

                            # Wait a cycle
                            if wait:
                                sleep(1 / self.__frequency)
                            else:
                                sleep(self.__default_time)
                                self.__running = False

                            # Write the date in memory
                            self.__memory.write(instr['address'],
                                                instr['data'])
                            # Get the new state
                            s = self.__change_state_miss(_id, 'I', 'WRITE',
                                                    instr['address'])
                            # Write the date in cache
                            self.__cpus[_id].write(instr['address'],
                                                    instr['data'], s)

                        # Free the bus
                        print(f'P{_id} released the bus')
                        self.__memory.free_bus()
                        self.__cpus[_id].finish()
                else:
                    # Wait a cycle
                    if wait:
                        sleep(1 / self.__frequency)
                    else:
                        sleep(self.__default_time)
                        self.__running = False
            else:
                # Wait a cycle
                if wait:
                    sleep(1 / self.__frequency)
                else:
                    sleep(self.__default_time)
                    self.__running = False
    
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

    def turn_on(self, wait: bool = True) -> None:
        """This method starts the system.

        Params
        --------------------------------------------------------------
            wait: bool.
                Indicates if the system has to wait each cycle.
        """
        # Run system
        self.__running: bool = True

        # Create and start threads
        self.__threads: list = [Thread(target=self.__control_processor,
                                args=(i, wait)) for i in range(self.__size)]

        # Shuffle threads
        shuffle(self.__threads)

        # Start all threads
        for thread in self.__threads:
            thread.start()

    def turn_off(self) -> None:
        """This method stops the system.
        """
        self.__running = False

