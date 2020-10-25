from hardware.system import System


class FSMController:
    """This class is used to control the cache using a FSM.
    """
    def change_state(self, _id: int, state: str, transition: str,
                    system: System) -> str:
        """This method is used to get the new state of a cache block.

        Params
        --------------------------------------------------------------
            _id: int.
                Processor ID.
            state: str.
                Current state of the cache block.
            transition: str.
                Transition to be executed by the controller.
            system: System.
                Multi processor System.
        
        Returns
        --------------------------------------------------------------
            New cache block state.
        """
        return

