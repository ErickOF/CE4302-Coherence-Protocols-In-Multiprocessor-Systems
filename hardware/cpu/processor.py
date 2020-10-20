from hardware.memory.cache import CacheL1


class Processor():
    """This class models a processor with a L1 Cache
    """
    def __init__(self):
        """Constructor.
        """
        self.__cache_l1: CacheL1 = CacheL1(2, 4)

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

    def read_cache(self, addr: int) -> hex:
        """This method reads L1 cache address.

        Params
        --------------------------------------------------------------
            addr: int.
                Memory address.

        Returns
        --------------------------------------------------------------
            The data in the specified memory address.
        """
        return self.__cache_l1.read(addr)

