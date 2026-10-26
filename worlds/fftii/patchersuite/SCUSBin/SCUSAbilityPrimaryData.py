class SCUSAbilityPrimaryData:
    raw_data: bytearray
    index: int
    jp_cost: int
    jp_cost_offset: int = 0x00
    jp_cost_length: int = 2
    chance_to_learn: int
    chance_to_learn_offset: int = 0x02

    def __init__(self, ability_data: bytearray, index: int):
        self.raw_data = ability_data
        self.index = index
        self.jp_cost = int.from_bytes(ability_data[self.jp_cost_offset:self.jp_cost_offset + self.jp_cost_length], "little")
        self.chance_to_learn = ability_data[self.chance_to_learn_offset]

    def __repr__(self):
        return f"Ability of index {self.index}"

    def apply_data(self):
        self.raw_data[self.jp_cost_offset:self.jp_cost_offset + self.jp_cost_length] = self.jp_cost.to_bytes(2, "little")
        self.raw_data[self.chance_to_learn_offset] = self.chance_to_learn