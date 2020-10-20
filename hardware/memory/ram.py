class RAM:
    """This class models a Memory RAM of 16 blocks.
    """
    def __init__(self, size: int) -> None:
        """Constructor.

        Params
        --------------------------------------------------------------
            size: int.
                Numbers of blocks.
        """
        self.__size: int = size
        self.__mem: list = ['0000' for _ in range(self.__size)]

    def get_size(self) -> int:
        """This method returns the memory size.

        Returns
        --------------------------------------------------------------
            The memory size.
        """
        return self.__size

    def read(self, addr: int) -> str:
        """This method reads the data in a memory address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data in the specified memory address.
        """
        return self.__mem[addr]

    def write(self, addr: int, data: str) -> None:
        """This method writes the data in a specific memory address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.
            data: str.
                Data to write in hexadecimal.
        """
        self.__mem[addr] = data

