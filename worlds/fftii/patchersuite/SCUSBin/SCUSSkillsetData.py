from enum import IntFlag, auto

from ..Transmooglifier.SkillsetTemplates import SkillsetMetaclass
from ...enemyrando.Abilities import ReactionAbility, SupportAbility, MovementAbility

class HighByteFlags(IntFlag):
    ABILITY_8 = auto()
    ABILITY_7 = auto()
    ABILITY_6 = auto()
    ABILITY_5 = auto()
    ABILITY_4 = auto()
    ABILITY_3 = auto()
    ABILITY_2 = auto()
    ABILITY_1 = auto()

class SCUSSkillsetData:
    raw_data: bytearray
    index: int

    ability_high_byte_flags = [
        HighByteFlags.ABILITY_1, HighByteFlags.ABILITY_2,
        HighByteFlags.ABILITY_3, HighByteFlags.ABILITY_4,
        HighByteFlags.ABILITY_5, HighByteFlags.ABILITY_6,
        HighByteFlags.ABILITY_7, HighByteFlags.ABILITY_8
    ]

    action_ability_high_byte_flags_one: HighByteFlags = 0
    action_ability_high_byte_flags_two: HighByteFlags = 0
    rsm_ability_high_byte_flags: HighByteFlags = 0
    action_abilities: list[int]
    rsm_abilities: list[int]

    def __init__(self, skillset_data, index: int):
        self.raw_data = skillset_data
        self.index = index

        self.action_abilities = list()
        self.rsm_abilities = list()
        self.action_ability_high_byte_flags_one = skillset_data[0]
        self.action_ability_high_byte_flags_two = skillset_data[1]
        self.rsm_ability_high_byte_flags = skillset_data[2]
        i = 3
        j = 0
        while len(self.action_abilities) < 8:
            value = skillset_data[i]
            if self.action_ability_high_byte_flags_one & self.ability_high_byte_flags[j]:
                value += 0x100
            self.action_abilities.append(value)
            i += 1
            j += 1
        j = 0
        while len(self.action_abilities) < 16:
            value = skillset_data[i]
            if self.action_ability_high_byte_flags_two & self.ability_high_byte_flags[j]:
                value += 0x100
            self.action_abilities.append(value)
            i += 1
            j += 1
        j = 0
        while len(self.rsm_abilities) < 6:
            value = skillset_data[i]
            if self.rsm_ability_high_byte_flags & self.ability_high_byte_flags[j]:
                value += 0x100
            self.rsm_abilities.append(value)
            i += 1
            j += 1


    def apply_transmooglifier_skillset(self, skillset: SkillsetMetaclass):
        self.action_abilities = list()
        for ability in skillset.action_abilities:
            self.action_abilities.append(ability)
        while len(self.action_abilities) < 16:
            self.action_abilities.append(0)
        self.rsm_abilities = list()
        for ability in skillset.rsm_abilities:
            self.rsm_abilities.append(ability)
        while len(self.rsm_abilities) < 6:
            self.rsm_abilities.append(0)


    def apply_data(self):
        action_ability_flag_one = 0
        action_ability_flag_two = 0
        rsm_ability_flag = 0
        for i, ability in enumerate(self.action_abilities[:8]):
            if ability >= 0x100:
                action_ability_flag_one |= self.ability_high_byte_flags[i]
        for i, ability in enumerate(self.action_abilities[8:]):
            if ability >= 0x100:
                action_ability_flag_two |= self.ability_high_byte_flags[i]
        for i, ability in enumerate(self.rsm_abilities):
            if ability >= 0x100:
                rsm_ability_flag |= self.ability_high_byte_flags[i]
        new_raw_data: bytearray = bytearray()
        new_raw_data.append(action_ability_flag_one)
        new_raw_data.append(action_ability_flag_two)
        new_raw_data.append(rsm_ability_flag)
        for ability in self.action_abilities:
            new_raw_data.append(ability & 0xFF)
        for ability in self.rsm_abilities:
            new_raw_data.append(ability & 0xFF)
        self.raw_data = new_raw_data