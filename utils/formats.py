def instr2string(_id: int, inst: dict) -> str:
    """This method converts and instruction to string.

    Params
    ------------------------------------------------------------------
        _id: int.
            Processor ID.
        inst: dict.
            Instruction data.

    Returns
    ------------------------------------------------------------------
        A string with the instruction format.
    """
    if inst == {}:
        return 'NOP'
    elif inst['type'] == 'CALC':
        return f'P{_id}: {inst["type"]}\n'
    elif inst['type'] == 'READ':
        return f'P{_id}: {inst["type"]} {inst["address"]}\n'
    else:
        return f'P{_id}: {inst["type"]} {inst["address"]}, {inst["data"]}\n'

