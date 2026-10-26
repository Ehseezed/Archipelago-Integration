from enum import IntFlag, auto


class FlagsFour(IntFlag):
    AI_TARGETING = auto()
    EVADEABLE = auto()
    MATERIA_BLADE = auto()
    SWORD = auto()
    BLADE_GRASP = auto()
    DIRECT_FIRE = auto()
    COUNTER_MAGIC = auto()
    COUNTER_FLOOD = auto()

class SCUSAbilitySecondaryData:
    raw_data: bytearray
    index: int
    flags_four: FlagsFour
    flags_four_offset: int = 0x06
    x_var: int
    x_var_offset: int = 0x09

    def __init__(self, ability_data: bytearray, index: int):
        self.raw_data = ability_data
        self.index = index
        self.flags_four = FlagsFour(ability_data[self.flags_four_offset])
        self.x_var = ability_data[self.x_var_offset]

    def __repr__(self):
        return f"Ability of index {self.index}"

    def apply_data(self):
        self.raw_data[self.flags_four_offset] = self.flags_four
        self.raw_data[self.x_var_offset] = self.x_var