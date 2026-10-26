from .SkillsetTemplates import SkillsetMetaclass, BerserkArts, RedMagic, VanguardSkill, Hunting, UltimateTimeMagic, \
    ReactionAbility, SupportAbility, MovementAbility, CatalogArts, DarkMagic, VampireArts, HighMagic
from ..SCUSBin.SCUSJobData import EquippableItemsOne, EquippableItemsTwo, EquippableItemsThree, EquippableItemsFour, \
    StatusesOne, StatusesTwo, StatusesThree, StatusesFour, StatusesFive, Elements

class TransmooglifierJobMetaclass(type):
    job_name: str = "Transmooglifier Job"
    job_description: str = "Test description"
    skillset: SkillsetMetaclass

    skillset_id: int = 0x0C

    innate_ability_one: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_two: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_three: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_four: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE

    equip_one: EquippableItemsOne = EquippableItemsOne.KNIFE
    equip_two: EquippableItemsTwo = 0
    equip_three: EquippableItemsThree = EquippableItemsThree.ARMOR | EquippableItemsThree.HELMET
    equip_four: EquippableItemsFour = EquippableItemsFour.STANDARD_ACCESSORIES

    hp_growth: int = 11
    hp_multiplier: int = 125
    mp_growth: int = 11
    mp_multiplier: int = 105
    speed_growth: int = 95
    speed_multiplier: int = 107
    pa_growth: int = 50
    pa_multiplier: int = 111
    ma_growth: int = 48
    ma_multiplier: int = 102

    move: int = 4
    jump: int = 3
    c_evade: int = 10

    innate_status_one: StatusesOne = 0
    innate_status_two: StatusesTwo = 0
    innate_status_three: StatusesThree = 0
    innate_status_four: StatusesFour = 0
    innate_status_five: StatusesFive = 0

    status_immunity_one: StatusesOne = 0
    status_immunity_two: StatusesTwo = 0
    status_immunity_three: StatusesThree = 0
    status_immunity_four: StatusesFour = 0
    status_immunity_five: StatusesFive = 0

    initial_status_one: StatusesOne = 0
    initial_status_two: StatusesTwo = 0
    initial_status_three: StatusesThree = 0
    initial_status_four: StatusesFour = 0
    initial_status_five: StatusesFive = 0

    absorbed_elements: Elements = 0
    halved_elements: Elements = 0
    weak_elements: Elements = 0

    def __repr__(self):
        return self.job_name

    def get_job_description_formatted(self):
        self.job_description = self.job_description.ljust(122)
        assert len(self.job_description) == 122, (len(self.job_description), self.job_description)
        return self.job_description

    def get_skillset_description_formatted(self):
        self.skillset.skillset_description = self.skillset.skillset_description.ljust(98)
        assert len(self.skillset.skillset_description) == 98, (len(self.skillset.skillset_description), self.skillset.skillset_description)
        return self.skillset.skillset_description


class TransmooglifierJob(object, metaclass=TransmooglifierJobMetaclass):
    job_name: str = "Transmooglifier Job"
    job_description: str = "Test description"
    skillset: SkillsetMetaclass = BerserkArts

    skillset_id: int = 0x50

    innate_ability_one: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_two: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_three: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE
    innate_ability_four: ReactionAbility | SupportAbility | MovementAbility = ReactionAbility.NONE

    equip_one: EquippableItemsOne = EquippableItemsOne.KNIFE
    equip_two: EquippableItemsTwo = 0
    equip_three: EquippableItemsThree = EquippableItemsThree.ARMOR | EquippableItemsThree.HELMET
    equip_four: EquippableItemsFour = EquippableItemsFour.STANDARD_ACCESSORIES

    hp_growth: int = 11
    hp_multiplier: int = 125
    mp_growth: int = 11
    mp_multiplier: int = 105
    speed_growth: int = 95
    speed_multiplier: int = 107
    pa_growth: int = 50
    pa_multiplier: int = 111
    ma_growth: int = 48
    ma_multiplier: int = 102

    move: int = 4
    jump: int = 3
    c_evade: int = 10

    innate_status_one: StatusesOne = 0
    innate_status_two: StatusesTwo = 0
    innate_status_three: StatusesThree = 0
    innate_status_four: StatusesFour = 0
    innate_status_five: StatusesFive = 0

    status_immunity_one: StatusesOne = 0
    status_immunity_two: StatusesTwo = 0
    status_immunity_three: StatusesThree = 0
    status_immunity_four: StatusesFour = 0
    status_immunity_five: StatusesFive = 0

    initial_status_one: StatusesOne = 0
    initial_status_two: StatusesTwo = 0
    initial_status_three: StatusesThree = 0
    initial_status_four: StatusesFour = 0
    initial_status_five: StatusesFive = 0

    absorbed_elements: Elements = 0
    halved_elements: Elements = 0
    weak_elements: Elements = 0

class Berserker(TransmooglifierJob):
    job_name = "Berserker"
    job_description = ("Warrior who enters an unending{NL}"
                       "rage upon taking damage. Their{NL}"
                       "Berserk Arts channel primal{NL}"
                       "power to destroy foes.")
    skillset = BerserkArts

    innate_ability_one = SupportAbility.TWO_HANDS
    innate_status_three = StatusesThree.BERSERK

    move = 5
    jump = 4
    c_evade = 20

    hp_growth = 9
    hp_multiplier = 150
    mp_growth = 15
    mp_multiplier = 95
    speed_growth = 85
    speed_multiplier = 120
    pa_growth = 40
    pa_multiplier = 145
    ma_growth = 65
    ma_multiplier = 80

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.KNIFE | EquippableItemsOne.SWORD | EquippableItemsOne.KNIGHTSWORD | EquippableItemsOne.KATANA | EquippableItemsOne.AXE
    equip_two = EquippableItemsTwo.POLEARM | EquippableItemsTwo.FLAIL
    equip_three = EquippableItemsThree.HAT
    equip_four = EquippableItemsFour.CLOTHING | EquippableItemsFour.STANDARD_ACCESSORIES

class RedMage(TransmooglifierJob):
    job_name = "Red_Mage"
    job_description = ("Fighter skilled in both swords{NL}"
                       "and sorcery. Not mighty, but Red{NL}"
                       "Magic contains a wide variety of{NL}"
                       "spell power.   ")
    skillset = RedMagic

    move = 4
    jump = 3
    c_evade = 5

    hp_growth = 11
    hp_multiplier = 95
    mp_growth = 11
    mp_multiplier = 105
    speed_growth = 100
    speed_multiplier = 100
    pa_growth = 50
    pa_multiplier = 105
    ma_growth = 60
    ma_multiplier = 105

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.ROD | EquippableItemsOne.SWORD
    equip_two = EquippableItemsTwo.CROSSBOW
    equip_three = EquippableItemsThree.HAT | EquippableItemsThree.SHIELD | EquippableItemsThree.ARMOR | EquippableItemsThree.POLE
    equip_four = EquippableItemsFour.CLOTHING | EquippableItemsFour.STANDARD_ACCESSORIES

class Testudo(TransmooglifierJob):
    job_name = "Testudo"
    job_description = ("A mighty weapon master who stands{NL}"
                       "tall on battlefields. Their{NL}"
                       "Vanguard Skill allows protection{NL}"
                       "of nearby allies.")
    skillset = VanguardSkill

    innate_ability_one = SupportAbility.DEFENSE_UP
    innate_ability_two = SupportAbility.MAGIC_DEFEND_UP
    halved_elements = Elements.ALL

    move = 3
    jump = 3
    c_evade = 20

    hp_growth = 9
    hp_multiplier = 130
    mp_growth = 9
    mp_multiplier = 120
    speed_growth = 100
    speed_multiplier = 110
    pa_growth = 50
    pa_multiplier = 110
    ma_growth = 50
    ma_multiplier = 90

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.KATANA | EquippableItemsOne.KNIGHTSWORD
    equip_two = EquippableItemsTwo.BOW | EquippableItemsTwo.POLEARM
    equip_three = EquippableItemsThree.ARMOR | EquippableItemsThree.SHIELD | EquippableItemsThree.HELMET
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES

class Hunter(TransmooglifierJob):
    job_name = "Hunter"
    job_description = ("A trapper turned fighter that {NL}"
                       "wears down their foes. Hunting{NL}"
                       "reveals their skill with their{NL}"
                       "arsenal.")
    skillset = Hunting

    innate_ability_one = SupportAbility.SECRET_HUNT

    move = 5
    jump = 3
    c_evade = 15

    hp_growth = 9
    hp_multiplier = 100
    mp_growth = 9
    mp_multiplier = 90
    speed_growth = 100
    speed_multiplier = 115
    pa_growth = 50
    pa_multiplier = 115
    ma_growth = 50
    ma_multiplier = 70

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.KNIFE | EquippableItemsOne.NINJA_BLADE
    equip_two = EquippableItemsTwo.BOW | EquippableItemsTwo.CROSSBOW | EquippableItemsTwo.GUN
    equip_three = EquippableItemsThree.HAT
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.CLOTHING

class TimeMaster(TransmooglifierJob):
    job_name = "Time_Master"
    job_description = ("Magic user with low power but {NL}"
                       "has no cast times. Ultimate{NL}"
                       "Time Magic contains several {NL}"
                       "forbidden powers.")
    skillset = UltimateTimeMagic

    innate_ability_one = SupportAbility.NON_CHARGE

    move = 2
    jump = 2
    c_evade = 0

    hp_growth = 9
    hp_multiplier = 80
    mp_growth = 9
    mp_multiplier = 90
    speed_growth = 100
    speed_multiplier = 75
    pa_growth = 50
    pa_multiplier = 60
    ma_growth = 50
    ma_multiplier = 60

    equip_one = EquippableItemsOne.UNARMED
    equip_two = 0
    equip_three = EquippableItemsThree.HAT | EquippableItemsThree.POLE
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.CLOTHING | EquippableItemsFour.ROBE

class Librarian(TransmooglifierJob):
    job_name = "Librarian"
    skillset = CatalogArts

    innate_ability_one = SupportAbility.MONSTER_TALK
    innate_ability_two = MovementAbility.MOVE_FIND_ITEM

    move = 4
    jump = 3
    c_evade = 5

    hp_growth = 9
    hp_multiplier = 125
    mp_growth = 9
    mp_multiplier = 110
    speed_growth = 100
    speed_multiplier = 100
    pa_growth = 50
    pa_multiplier = 90
    ma_growth = 50
    ma_multiplier = 130

    equip_one = EquippableItemsOne.UNARMED
    equip_two = EquippableItemsTwo.BOOK
    equip_three = EquippableItemsThree.HAT
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.CLOTHING | EquippableItemsFour.ROBE

class DarkMagician(TransmooglifierJob):
    job_name = "Dark_Magician"
    skillset = DarkMagic

    halved_elements = Elements.DARK

    move = 3
    jump = 3
    c_evade = 5

    hp_growth = 10
    hp_multiplier = 100
    mp_growth = 11
    mp_multiplier = 120
    speed_growth: int = 100
    speed_multiplier: int = 105
    pa_growth: int = 50
    pa_multiplier: int = 105
    ma_growth: int = 48
    ma_multiplier: int = 115

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.KNIFE
    equip_two = EquippableItemsTwo.BOOK
    equip_three = EquippableItemsThree.HAT | EquippableItemsThree.POLE
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.ROBE

class VampireLord(TransmooglifierJob):
    job_name = "Vampire_Lord"
    skillset = VampireArts

    weak_elements = Elements.HOLY | Elements.EARTH | Elements.WATER
    absorbed_elements = Elements.DARK

    innate_ability_one = MovementAbility.FLY

    status_immunity_two = StatusesTwo.BLOOD_SUCK

    move = 4
    jump = 3
    c_evade = 15

    hp_growth = 8
    hp_multiplier = 130
    mp_growth = 11
    mp_multiplier = 90
    speed_growth: int = 100
    speed_multiplier: int = 120
    pa_growth: int = 45
    pa_multiplier: int = 110
    ma_growth: int = 50
    ma_multiplier: int = 110

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.SWORD
    equip_two = EquippableItemsTwo.INSTRUMENT
    equip_three = EquippableItemsThree.CLOTH | EquippableItemsThree.HAT | EquippableItemsThree.ARMOR
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.ROBE

class Sage(TransmooglifierJob):
    job_name = "Sage"
    skillset = HighMagic

    innate_ability_one = SupportAbility.HALF_OF_MP

    move = 5
    jump = 3
    c_evade = 10

    hp_growth = 10
    hp_multiplier = 85
    mp_growth = 11
    mp_multiplier = 120
    speed_growth: int = 100
    speed_multiplier: int = 95
    pa_growth: int = 50
    pa_multiplier: int = 70
    ma_growth: int = 40
    ma_multiplier: int = 150

    equip_one = EquippableItemsOne.UNARMED | EquippableItemsOne.ROD
    equip_two = EquippableItemsTwo.BOOK | EquippableItemsTwo.STAFF
    equip_three = EquippableItemsThree.HAT
    equip_four = EquippableItemsFour.STANDARD_ACCESSORIES | EquippableItemsFour.ROBE

transmooglifier_lookup = {
    "Berserker": Berserker,
    "Red Mage": RedMage,
    "Testudo": Testudo,
    "Hunter": Hunter,
    "Time Master": TimeMaster,
    "Librarian": Librarian,
    "Dark Magician": DarkMagician,
    "Vampire Lord": VampireLord,
    "Sage": Sage
}