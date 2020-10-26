from threading import Lock


class RAM:
    """This class models a Memory RAM of 16 blocks.
    """
    # Memory instance
    __instance = None

    @staticmethod
    def get_instance(size: int):
        """Static access method to get a RAM instance.

        Params
        --------------------------------------------------------------
            size: int.
                Numbers of blocks.
        """
        if RAM.__instance == None:
            RAM(size)

        return RAM.__instance

    def __init__(self, size: int) -> None:
        """Constructor.

        Params
        --------------------------------------------------------------
            size: int.
                Numbers of blocks.
        """
        if RAM.__instance != None:
            raise Exception('This class is a singleton!')
        else:
            RAM.__instance = self
            self.__size: int = size
            self.__mem: list = ['0000'] * self.__size
            self.__bus: Lock = Lock()

    def block_bus(self) -> None:
        """This method asks for the bus and block it.
        """
        self.__bus.acquire(True)

    def clear(self) -> None:
        """This method clears the memory and puts '0000' in all
        blocks.
        """
        self.__mem: list = ['0000'] * self.__size

    def free_bus(self) -> None:
        """This method releases the bus.
        """
        self.__bus.release()

    def get_size(self) -> int:
        """This method returns the memory size.

        Returns
        --------------------------------------------------------------
            The memory size.
        """
        return self.__size

    def is_busy(self) -> bool:
        """This method indicates if the bus is busy.

        Returns
        --------------------------------------------------------------
            True if the bus is busy, False otherwise.
        """
        return self.__bus.locked()

    def read(self, addr: str) -> str:
        """This method reads the data in a memory address.

        Params
        --------------------------------------------------------------
            addr: str.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data in the specified memory address.
        """
        return self.__mem[int(addr, 2)]

    def write(self, addr: int, data: str) -> None:
        """This method writes the data in a specific memory address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.
            data: str.
                Data to write in hexadecimal.
        """
        self.__mem[int(addr, 2)] = data

