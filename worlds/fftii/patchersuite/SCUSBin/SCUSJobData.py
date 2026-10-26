from typing import TYPE_CHECKING

from ..JobData.Enums import EquippableItemsOne, EquippableItemsTwo, EquippableItemsThree, EquippableItemsFour, \
    StatusesOne, StatusesTwo, StatusesThree, StatusesFour, StatusesFive, Elements

from ..Transmooglifier.SkillsetTemplates import ReactionAbility, SupportAbility, MovementAbility


if TYPE_CHECKING:
    from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass

class SCUSJobData:
    job_name: str
    job_index: int
    raw_data: bytearray

    skillset_id: int
    skillset_offset: int = 0x00

    innate_ability_one: ReactionAbility | SupportAbility | MovementAbility
    innate_ability_one_offset: int = 0x01
    innate_ability_two: ReactionAbility | SupportAbility | MovementAbility
    innate_ability_two_offset: int = 0x03
    innate_ability_three: ReactionAbility | SupportAbility | MovementAbility
    innate_ability_three_offset: int = 0x05
    innate_ability_four: ReactionAbility | SupportAbility | MovementAbility
    innate_ability_four_offset: int = 0x07

    equip_one_offset: int = 0x09
    equip_one: EquippableItemsOne
    equip_two_offset: int = 0x0A
    equip_two: EquippableItemsTwo
    equip_three_offset: int = 0x0B
    equip_three: EquippableItemsThree
    equip_four_offset: int = 0x0C
    equip_four: EquippableItemsFour

    hp_growth: int
    hp_growth_offset: int = 0x0D
    hp_multiplier: int
    hp_multiplier_offset: int = 0x0E
    mp_growth: int
    mp_growth_offset: int = 0x0F
    mp_multiplier: int
    mp_multiplier_offset: int = 0x10
    speed_growth: int
    speed_growth_offset: int = 0x11
    speed_multiplier: int
    speed_multiplier_offset: int = 0x12
    pa_growth: int
    pa_growth_offset: int = 0x13
    pa_multiplier: int
    pa_multiplier_offset: int = 0x14
    ma_growth: int
    ma_growth_offset: int = 0x15
    ma_multiplier: int
    ma_multiplier_offset: int = 0x16

    move: int
    move_offset: int = 0x17
    jump: int
    jump_offset: int = 0x18
    c_evade: int
    c_evade_offset: int = 0x19

    innate_status_one: StatusesOne
    innate_status_one_offset: int = 0x1A
    innate_status_two: StatusesTwo
    innate_status_two_offset: int = 0x1B
    innate_status_three: StatusesThree
    innate_status_three_offset: int = 0x1C
    innate_status_four: StatusesFour
    innate_status_four_offset: int = 0x1D
    innate_status_five: StatusesFive
    innate_status_five_offset: int = 0x1E

    status_immunity_one: StatusesOne
    status_immunity_one_offset: int = 0x1F
    status_immunity_two: StatusesTwo
    status_immunity_two_offset: int = 0x20
    status_immunity_three: StatusesThree
    status_immunity_three_offset: int = 0x21
    status_immunity_four: StatusesFour
    status_immunity_four_offset: int = 0x22
    status_immunity_five: StatusesFive
    status_immunity_five_offset: int = 0x23

    initial_status_one: StatusesOne
    initial_status_one_offset: int = 0x24
    initial_status_two: StatusesTwo
    initial_status_two_offset: int = 0x25
    initial_status_three: StatusesThree
    initial_status_three_offset: int = 0x26
    initial_status_four: StatusesFour
    initial_status_four_offset: int = 0x27
    initial_status_five: StatusesFive
    initial_status_five_offset: int = 0x28

    absorbed_elements: Elements
    absorbed_elements_offset: int = 0x2A
    halved_elements: Elements
    halved_elements_offset: int = 0x2B
    weak_elements: Elements
    weak_elements_offset: int = 0x2C

    def __init__(self, job_data: bytearray, index: int):
        self.raw_data = job_data
        self.job_index = index
        try:
            from ...enemyrando.Job import Job
            self.job_name = Job(index).name
        except ValueError:
            self.job_name = f"Unknown Job {hex(index)}"

        self.skillset_id = job_data[self.skillset_offset]

        self.innate_ability_one: ReactionAbility | SupportAbility | MovementAbility = self.get_innate_ability(self.innate_ability_one_offset)
        self.innate_ability_two: ReactionAbility | SupportAbility | MovementAbility = self.get_innate_ability(self.innate_ability_two_offset)
        self.innate_ability_three: ReactionAbility | SupportAbility | MovementAbility = self.get_innate_ability(self.innate_ability_three_offset)
        self.innate_ability_four: ReactionAbility | SupportAbility | MovementAbility = self.get_innate_ability(self.innate_ability_four_offset)

        self.equip_one = EquippableItemsOne(job_data[self.equip_one_offset])
        self.equip_two = EquippableItemsTwo(job_data[self.equip_two_offset])
        self.equip_three = EquippableItemsThree(job_data[self.equip_three_offset])
        self.equip_four = EquippableItemsFour(job_data[self.equip_four_offset])

        self.hp_growth = job_data[self.hp_growth_offset]
        self.hp_multiplier = job_data[self.hp_multiplier_offset]
        self.mp_growth = job_data[self.mp_growth_offset]
        self.mp_multiplier = job_data[self.mp_multiplier_offset]
        self.speed_growth = job_data[self.speed_growth_offset]
        self.speed_multiplier = job_data[self.speed_multiplier_offset]
        self.pa_growth = job_data[self.pa_growth_offset]
        self.pa_multiplier = job_data[self.pa_multiplier_offset]
        self.ma_growth = job_data[self.ma_growth_offset]
        self.ma_multiplier = job_data[self.ma_multiplier_offset]

        self.move = job_data[self.move_offset]
        self.jump = job_data[self.jump_offset]
        self.c_evade = job_data[self.c_evade_offset]

        self.innate_status_one = StatusesOne(job_data[self.innate_status_one_offset])
        self.innate_status_two = StatusesTwo(job_data[self.innate_status_two_offset])
        self.innate_status_three = StatusesThree(job_data[self.innate_status_three_offset])
        self.innate_status_four = StatusesFour(job_data[self.innate_status_four_offset])
        self.innate_status_five = StatusesFive(job_data[self.innate_status_five_offset])

        self.status_immunity_one = StatusesOne(job_data[self.status_immunity_one_offset])
        self.status_immunity_two = StatusesTwo(job_data[self.status_immunity_two_offset])
        self.status_immunity_three = StatusesThree(job_data[self.status_immunity_three_offset])
        self.status_immunity_four = StatusesFour(job_data[self.status_immunity_four_offset])
        self.status_immunity_five = StatusesFive(job_data[self.status_immunity_five_offset])

        self.initial_status_one = StatusesOne(job_data[self.initial_status_one_offset])
        self.initial_status_two = StatusesTwo(job_data[self.initial_status_two_offset])
        self.initial_status_three = StatusesThree(job_data[self.initial_status_three_offset])
        self.initial_status_four = StatusesFour(job_data[self.initial_status_four_offset])
        self.initial_status_five = StatusesFive(job_data[self.initial_status_five_offset])

        self.absorbed_elements = Elements(job_data[self.absorbed_elements_offset])
        self.halved_elements = Elements(job_data[self.halved_elements_offset])
        self.weak_elements = Elements(job_data[self.weak_elements_offset])

        pass

    def __repr__(self):
        return f"{self.job_name}"


    def get_innate_ability(self, offset) -> ReactionAbility | SupportAbility | MovementAbility:
        innate_ability_value: int = int.from_bytes(self.raw_data[offset:offset + 2], "little")
        try:
            return_value = ReactionAbility(innate_ability_value)
        except ValueError:
            try:
                return_value = SupportAbility(innate_ability_value)
            except ValueError:
                try:
                    return_value = MovementAbility(innate_ability_value)
                except ValueError:
                    raise ValueError(innate_ability_value)
        return return_value

    def apply_transmooglifier_job(self, job: "TransmooglifierJobMetaclass", job_number: int):
        from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass
        self.skillset_id = 0x50 + job_number
        self.innate_ability_one = job.innate_ability_one
        self.innate_ability_two = job.innate_ability_two
        self.innate_ability_three = job.innate_ability_three
        self.innate_ability_four = job.innate_ability_four
        self.equip_one = job.equip_one
        self.equip_two = job.equip_two
        self.equip_three = job.equip_three
        self.equip_four = job.equip_four
        self.hp_growth = job.hp_growth
        self.hp_multiplier = job.hp_multiplier
        self.mp_growth = job.mp_growth
        self.mp_multiplier = job.mp_multiplier
        self.speed_growth = job.speed_growth
        self.speed_multiplier = job.speed_multiplier
        self.pa_growth = job.pa_growth
        self.pa_multiplier = job.pa_multiplier
        self.ma_growth = job.ma_growth
        self.ma_multiplier = job.ma_multiplier
        self.move = job.move
        self.jump = job.jump
        self.c_evade = job.c_evade
        self.innate_status_one = job.innate_status_one
        self.innate_status_two = job.innate_status_two
        self.innate_status_three = job.innate_status_three
        self.innate_status_four = job.innate_status_four
        self.innate_status_five = job.innate_status_five
        self.status_immunity_one = job.status_immunity_one
        self.status_immunity_two = job.status_immunity_two
        self.status_immunity_three = job.status_immunity_three
        self.status_immunity_four = job.status_immunity_four
        self.status_immunity_five = job.status_immunity_five
        self.initial_status_one = job.initial_status_one
        self.initial_status_two = job.initial_status_two
        self.initial_status_three = job.initial_status_three
        self.initial_status_four = job.initial_status_four
        self.initial_status_five = job.initial_status_five
        self.absorbed_elements = job.absorbed_elements
        self.halved_elements = job.halved_elements
        self.weak_elements = job.weak_elements

    def apply_data(self):
        self.raw_data[self.skillset_offset] = self.skillset_id

        self.raw_data[self.innate_ability_one_offset:
                      self.innate_ability_one_offset + 2] = self.innate_ability_one.to_bytes(2, "little")
        self.raw_data[self.innate_ability_two_offset:
                      self.innate_ability_two_offset + 2] = self.innate_ability_two.to_bytes(2, "little")
        self.raw_data[self.innate_ability_three_offset:
                      self.innate_ability_three_offset + 2] = self.innate_ability_three.to_bytes(2, "little")
        self.raw_data[self.innate_ability_four_offset:
                      self.innate_ability_four_offset + 2] = self.innate_ability_four.to_bytes(2, "little")

        self.raw_data[self.equip_one_offset] = self.equip_one
        self.raw_data[self.equip_two_offset] = self.equip_two
        self.raw_data[self.equip_three_offset] = self.equip_three
        self.raw_data[self.equip_four_offset] = self.equip_four

        self.raw_data[self.hp_growth_offset] = self.hp_growth
        self.raw_data[self.hp_multiplier_offset] = self.hp_multiplier
        self.raw_data[self.mp_growth_offset] = self.mp_growth
        self.raw_data[self.mp_multiplier_offset] = self.mp_multiplier
        self.raw_data[self.speed_growth_offset] = self.speed_growth
        self.raw_data[self.speed_multiplier_offset] = self.speed_multiplier
        self.raw_data[self.pa_growth_offset] = self.pa_growth
        self.raw_data[self.pa_multiplier_offset] = self.pa_multiplier
        self.raw_data[self.ma_growth_offset] = self.ma_growth
        self.raw_data[self.ma_multiplier_offset] = self.ma_multiplier

        self.raw_data[self.move_offset] = self.move
        self.raw_data[self.jump_offset] = self.jump
        self.raw_data[self.c_evade_offset] = self.c_evade

        self.raw_data[self.innate_status_one_offset] = self.innate_status_one
        self.raw_data[self.innate_status_two_offset] = self.innate_status_two
        self.raw_data[self.innate_status_three_offset] = self.innate_status_three
        self.raw_data[self.innate_status_four_offset] = self.innate_status_four
        self.raw_data[self.innate_status_five_offset] = self.innate_status_five

        self.raw_data[self.status_immunity_one_offset] = self.status_immunity_one
        self.raw_data[self.status_immunity_two_offset] = self.status_immunity_two
        self.raw_data[self.status_immunity_three_offset] = self.status_immunity_three
        self.raw_data[self.status_immunity_four_offset] = self.status_immunity_four
        self.raw_data[self.status_immunity_five_offset] = self.status_immunity_five

        self.raw_data[self.initial_status_one_offset] = self.initial_status_one
        self.raw_data[self.initial_status_two_offset] = self.initial_status_two
        self.raw_data[self.initial_status_three_offset] = self.initial_status_three
        self.raw_data[self.initial_status_four_offset] = self.initial_status_four
        self.raw_data[self.initial_status_five_offset] = self.initial_status_five

        self.raw_data[self.absorbed_elements_offset] = self.absorbed_elements
        self.raw_data[self.halved_elements_offset] = self.halved_elements
        self.raw_data[self.weak_elements_offset] = self.weak_elements