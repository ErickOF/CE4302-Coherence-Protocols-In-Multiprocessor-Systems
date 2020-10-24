class FSM_Controller:
    """This class is used to control the cache using a FSM.
    """
    def __init__(self) -> None:
        """Constructor.
        """
        self.__states = ['M', 'O', 'E', 'S', 'I']

    def change_state(self, state: str, transition: str) -> str:
        """This method is used to get the new state of a cache block.

        Params
        --------------------------------------------------------------
            state: str.
                Current state of the cache block.
            transition: str.
                Transition to be executed by the controller.
        
        Returns
        --------------------------------------------------------------
            New cache block state.
        """
        return

