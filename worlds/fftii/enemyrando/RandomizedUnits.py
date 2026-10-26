from .Abilities import ReactionAbility, SupportAbility, MovementAbility, ActionAbility
from .Birthday import Month
from .Items import Items
from .Job import UnlockedJob, Job
from .SpriteSet import SpriteSet
from ..patchersuite.ENTD.Unit import UnitGender

RANDOM_VALUE = 0xFE

class RandomizedUnitMetaclass(type):
    job: Job = Job.SQUIRE
    sprite_set: SpriteSet = SpriteSet.GENERIC_FEMALE
    gender: UnitGender = UnitGender.FEMALE

    def __repr__(self):
        return f"Sprite: {self.sprite_set.name}, Job: {self.job.name}, Gender: {self.gender.name}"

class RandomizedUnit(object, metaclass=RandomizedUnitMetaclass):
    job: Job
    job_name: str
    sprite_set: SpriteSet
    sprite_set_name: str
    gender: UnitGender
    hidden_stats: bool = False
    birthday_month: Month = Month.RANDOM
    birthday_day: int = RANDOM_VALUE
    brave: int = RANDOM_VALUE
    faith: int = RANDOM_VALUE
    unlocked_job: UnlockedJob = UnlockedJob.BASE
    unlocked_job_level: int = 2
    primary: ActionAbility = ActionAbility.JOB
    secondary: ActionAbility = ActionAbility.RANDOM
    reaction: ReactionAbility = ReactionAbility.RANDOM
    support: SupportAbility = SupportAbility.RANDOM
    movement: MovementAbility = MovementAbility.RANDOM
    head: Items = Items.RANDOM
    body: Items = Items.RANDOM
    accessory: Items = Items.RANDOM
    right_hand: Items = Items.RANDOM
    left_hand: Items = Items.RANDOM
    difficulty: int = 0

    @classmethod
    def to_json(cls):
        return {
            "Job": cls.job.value,
            "SpriteSet": cls.sprite_set.value,
            "Gender": cls.gender.value,
            "BirthdayMonth": cls.birthday_month.value,
            "BirthdayDay": cls.birthday_day,
            "Brave": cls.brave,
            "Faith": cls.faith,
            "UnlockedJob": cls.unlocked_job.value,
            "UnlockedJobLevel": cls.unlocked_job_level,
            "Primary": cls.primary.value,
            "Secondary": cls.secondary.value,
            "Reaction": cls.reaction.value,
            "Support": cls.support.value,
            "Movement": cls.movement.value,
            "Head": cls.head.value,
            "Body": cls.body.value,
            "Accessory": cls.accessory.value,
            "RightHand": cls.right_hand.value,
            "LeftHand": cls.left_hand.value
        }

    def __repr__(self):
        return f"Sprite: {self.sprite_set.name}, Job: {self.job.name}, Gender: {self.gender.name}"

#region Generic humanss
class MaleSquire(RandomizedUnit):
    job = Job.SQUIRE
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 2


class MaleSquireEasy(MaleSquire):
    unlocked_job_level = 4
    difficulty = 2


class MaleSquireModerate1(MaleSquire):
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 2
    difficulty = 4


class MaleSquireModerate2(MaleSquire):
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 2
    difficulty = 4


class MaleSquireAdvanced1(MaleSquire):
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 3
    difficulty = 6


class MaleSquireAdvanced2(MaleSquire):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 3
    difficulty = 6


class MaleSquireExpert1(MaleSquire):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8


class MaleSquireExpert2(MaleSquire):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8


class MaleSquireExpert3(MaleSquire):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleSquireRare(MaleSquireExpert1):
    right_hand = Items.BLOOD_SWORD
    difficulty = 10

class FemaleSquire(RandomizedUnit):
    job = Job.SQUIRE
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 2

class FemaleSquireEasy(FemaleSquire):
    unlocked_job_level = 4
    difficulty = 2

class FemaleSquireModerate1(FemaleSquire):
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 2
    difficulty = 4

class FemaleSquireModerate2(FemaleSquire):
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 2
    difficulty = 4

class FemaleSquireAdvanced1(FemaleSquire):
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 3
    difficulty = 6

class FemaleSquireAdvanced2(FemaleSquire):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 3
    difficulty = 6

class FemaleSquireExpert1(FemaleSquire):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8

class FemaleSquireExpert2(FemaleSquire):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleSquireExpert3(FemaleSquire):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleSquireExpert4(FemaleSquire):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 4
    difficulty = 8

class FemaleSquireRare(FemaleSquireExpert1):
    right_hand = Items.NAGRAROCK
    difficulty = 10

class MaleChemist(RandomizedUnit):
    job = Job.CHEMIST
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.CHEMIST
    unlocked_job_level = 2


class MaleChemistEasy(MaleChemist):
    unlocked_job_level = 4
    difficulty = 2


class MaleChemistModerate1(MaleChemist):
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 2
    difficulty = 4


class MaleChemistModerate2(MaleChemist):
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 2
    difficulty = 4


class MaleChemistAdvanced1(MaleChemist):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6


class MaleChemistAdvanced2(MaleChemist):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6


class MaleChemistExpert1(MaleChemist):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8


class MaleChemistExpert2(MaleChemist):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 4
    difficulty = 8


class MaleChemistExpert3(MaleChemist):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 4
    difficulty = 8

class MaleChemistRare(MaleChemistExpert1):
    right_hand = Items.BLAST_GUN
    difficulty = 10


class FemaleChemist(RandomizedUnit):
    job = Job.CHEMIST
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.CHEMIST
    unlocked_job_level = 2



class FemaleChemistEasy(FemaleChemist):
    unlocked_job_level = 4
    difficulty = 2


class FemaleChemistModerate1(FemaleChemist):
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 2
    difficulty = 4


class FemaleChemistModerate2(FemaleChemist):
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 2
    difficulty = 4


class FemaleChemistAdvanced1(FemaleChemist):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6


class FemaleChemistAdvanced2(FemaleChemist):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6


class FemaleChemistExpert1(FemaleChemist):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8


class FemaleChemistExpert2(FemaleChemist):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 4
    difficulty = 8

class FemaleChemistRare(FemaleChemistExpert1):
    right_hand = Items.BLAZE_GUN
    difficulty = 10


class MaleKnight(RandomizedUnit):
    job = Job.KNIGHT
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.KNIGHT
    unlocked_job_level = 2

class MaleKnightEasy(MaleKnight):
    unlocked_job_level = 4
    difficulty = 2

class MaleKnightModerate(MaleKnight):
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 3
    difficulty = 4

class MaleKnightAdvanced(MaleKnight):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 3
    difficulty = 6

class MaleKnightExpert1(MaleKnight):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8

class MaleKnightExpert2(MaleKnight):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleKnightExpert3(MaleKnight):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleKnightRare(MaleKnightExpert1):
    right_hand = Items.DEFENDER
    reaction = ReactionAbility.WEAPON_GUARD
    difficulty = 10


class FemaleKnight(RandomizedUnit):
    job = Job.KNIGHT
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.KNIGHT
    unlocked_job_level = 2

class FemaleKnightEasy(FemaleKnight):
    unlocked_job_level = 4
    difficulty = 2

class FemaleKnightModerate(FemaleKnight):
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 3
    difficulty = 4

class FemaleKnightAdvanced(FemaleKnight):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 3
    difficulty = 6

class FemaleKnightExpert1(FemaleKnight):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8

class FemaleKnightExpert2(FemaleKnight):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleKnightExpert3(FemaleKnight):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleKnightExpert4(FemaleKnight):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 6
    difficulty = 8

class FemaleKnightRare(FemaleKnightExpert1):
    right_hand = Items.SAVE_THE_QUEEN
    reaction = ReactionAbility.WEAPON_GUARD
    difficulty = 10


class MaleArcher(RandomizedUnit):
    job = Job.ARCHER
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.ARCHER
    unlocked_job_level = 2


class MaleArcherEasy(MaleArcher):
    unlocked_job_level = 4
    difficulty = 2


class MaleArcherModerate(MaleArcher):
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 3
    difficulty = 4


class MaleArcherAdvanced(MaleArcher):
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 3
    difficulty = 6


class MaleArcherExpert1(MaleArcher):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8


class MaleArcherExpert2(MaleArcher):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8


class MaleArcherExpert3(MaleArcher):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleArcherRare(MaleArcherExpert1):
    right_hand = Items.GASTRAFITIS
    left_hand = Items.VENETIAN_SHIELD
    difficulty = 10


class FemaleArcher(RandomizedUnit):
    job = Job.ARCHER
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.ARCHER
    unlocked_job_level = 2

class FemaleArcherEasy(FemaleArcher):
    unlocked_job_level = 4
    difficulty = 2

class FemaleArcherModerate(FemaleArcher):
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 3
    difficulty = 4

class FemaleArcherAdvanced(FemaleArcher):
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 3
    difficulty = 6

class FemaleArcherExpert1(FemaleArcher):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 1
    difficulty = 8

class FemaleArcherExpert2(FemaleArcher):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleArcherExpert3(FemaleArcher):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleArcherExpert4(FemaleArcher):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 6
    difficulty = 8

class FemaleArcherRare(FemaleArcherExpert1):
    right_hand = Items.PERSEUS_BOW
    difficulty = 10


class MaleMonk(RandomizedUnit):
    job = Job.MONK
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 2

class MaleMonkEasy(MaleMonk):
    unlocked_job_level = 4
    difficulty = 2

class MaleMonkModerate(MaleMonk):
    unlocked_job_level = 6
    difficulty = 4

class MaleMonkAdvanced(MaleMonk):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 4
    difficulty = 6

class MaleMonkExpert1(MaleMonk):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleMonkExpert2(MaleMonk):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleMonkExpert3(MaleMonk):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class MaleMonkRare(MaleMonkExpert3):
    accessory = Items.GENJI_GAUNTLET
    difficulty = 10


class FemaleMonk(RandomizedUnit):
    job = Job.MONK
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.MONK
    unlocked_job_level = 2

class FemaleMonkEasy(FemaleMonk):
    unlocked_job_level = 4
    difficulty = 2

class FemaleMonkModerate(FemaleMonk):
    unlocked_job_level = 6
    difficulty = 4

class FemaleMonkAdvanced(FemaleMonk):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 4
    difficulty = 6

class FemaleMonkExpert1(FemaleMonk):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleMonkExpert2(FemaleMonk):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleMonkExpert3(FemaleMonk):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class FemaleMonkExpert4(FemaleMonk):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 6
    difficulty = 8

class FemaleMonkRare(FemaleMonkExpert3):
    accessory = Items.SALTY_RAGE
    difficulty = 10


class MalePriest(RandomizedUnit):
    job = Job.PRIEST
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.PRIEST
    unlocked_job_level = 2

class MalePriestEasy(MalePriest):
    unlocked_job_level = 4
    difficulty = 2

class MalePriestModerate(MalePriest):
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 3
    difficulty = 4

class MalePriestAdvanced1(MalePriest):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6

class MalePriestAdvanced2(MalePriest):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6

class MalePriestExpert1(MalePriest):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class MalePriestExpert2(MalePriest):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 6
    difficulty = 8

class MalePriestRare(MalePriestExpert2):
    right_hand = Items.SAGE_STAFF
    difficulty = 10



class FemalePriest(RandomizedUnit):
    job = Job.PRIEST
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.PRIEST
    unlocked_job_level = 2

class FemalePriestEasy(FemalePriest):
    unlocked_job_level = 4
    difficulty = 2

class FemalePriestModerate(FemalePriest):
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 3
    difficulty = 4

class FemalePriestAdvanced(FemalePriest):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6

class FemalePriestExpert1(FemalePriest):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class FemalePriestExpert2(FemalePriest):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 6
    difficulty = 8

class FemalePriestRare(FemalePriestExpert2):
    accessory = Items.CHANTAGE
    difficulty = 10


class MaleWizard(RandomizedUnit):
    job = Job.WIZARD
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.WIZARD
    unlocked_job_level = 2


class MaleWizardEasy(MaleWizard):
    unlocked_job_level = 4
    difficulty = 2


class MaleWizardModerate(MaleWizard):
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 3
    difficulty = 4


class MaleWizardAdvanced1(MaleWizard):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6


class MaleWizardAdvanced2(MaleWizard):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6


class MaleWizardExpert1(MaleWizard):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8


class MaleWizardExpert2(MaleWizard):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 6
    difficulty = 8

class MaleWizardRare(MaleWizardExpert2):
    body = Items.ROBE_OF_LORDS
    difficulty = 10


class FemaleWizard(RandomizedUnit):
    job = Job.WIZARD
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.WIZARD
    unlocked_job_level = 2


class FemaleWizardEasy(FemaleWizard):
    unlocked_job_level = 4
    difficulty = 2


class FemaleWizardModerate(FemaleWizard):
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 3
    difficulty = 4


class FemaleWizardAdvanced(FemaleWizard):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6


class FemaleWizardExpert1(FemaleWizard):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8


class FemaleWizardExpert2(FemaleWizard):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 6
    difficulty = 8

class FemaleWizardRare(FemaleWizardExpert2):
    right_hand = Items.FAITH_ROD
    difficulty = 10


class MaleTimeMage(RandomizedUnit):
    job = Job.TIMEMAGE
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 2


class MaleTimeMageEasy(MaleTimeMage):
    unlocked_job_level = 4
    difficulty = 2


class MaleTimeMageModerate(MaleTimeMage):
    unlocked_job_level = 6
    difficulty = 4


class MaleTimeMageAdvanced1(MaleTimeMage):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6


class MaleTimeMageAdvanced2(MaleTimeMage):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6


class MaleTimeMageExpert1(MaleTimeMage):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 2
    difficulty = 8


class MaleTimeMageExpert2(MaleTimeMage):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class MaleTimeMageRare(MaleTimeMageExpert1):
    right_hand = Items.MACE_OF_ZEUS
    difficulty = 10


class FemaleTimeMage(RandomizedUnit):
    job = Job.TIMEMAGE
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.TIMEMAGE
    unlocked_job_level = 2

class FemaleTimeMageEasy(FemaleTimeMage):
    unlocked_job_level = 4
    difficulty = 2

class FemaleTimeMageModerate(FemaleTimeMage):
    unlocked_job_level = 6
    difficulty = 4

class FemaleTimeMageAdvanced(FemaleTimeMage):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3
    difficulty = 6

class FemaleTimeMageExpert1(FemaleTimeMage):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 2
    difficulty = 8

class FemaleTimeMageExpert2(FemaleTimeMage):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class FemaleTimeMageRare(FemaleTimeMageExpert1):
    right_hand = Items.HEALING_STAFF
    difficulty = 10

class MaleSummoner(RandomizedUnit):
    job = Job.SUMMONER
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 2

class MaleSummonerEasy(MaleSummoner):
    unlocked_job_level = 4
    difficulty = 2

class MaleSummonerModerate(MaleSummoner):
    unlocked_job_level = 6
    difficulty = 4

class MaleSummonerAdvanced1(MaleSummoner):
    unlocked_job_level = 8
    difficulty = 6

class MaleSummonerAdvanced2(MaleSummoner):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6

class MaleSummonerExpert(MaleSummoner):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class MaleSummonerRare(MaleSummonerExpert):
    primary = ActionAbility.SUMMON_MAGIC
    support = SupportAbility.SHORT_CHARGE
    difficulty = 10

class FemaleSummoner(RandomizedUnit):
    job = Job.SUMMONER
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 2

class FemaleSummonerEasy(FemaleSummoner):
    unlocked_job_level = 4
    difficulty = 2

class FemaleSummonerModerate(FemaleSummoner):
    unlocked_job_level = 6
    difficulty = 4

class FemaleSummonerAdvanced(FemaleSummoner):
    unlocked_job_level = 8
    difficulty = 6

class FemaleSummonerExpert(FemaleSummoner):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class FemaleSummonerRare(FemaleSummonerExpert):
    primary = ActionAbility.SUMMON_MAGIC
    accessory = Items.CHERCHE
    difficulty = 10


class MaleThief(RandomizedUnit):
    job = Job.THIEF
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 2

class MaleThiefEasy(MaleThief):
    unlocked_job_level = 4
    difficulty = 2

class MaleThiefModerate(MaleThief):
    unlocked_job_level = 6
    difficulty = 4

class MaleThiefAdvanced(MaleThief):
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 4
    difficulty = 6

class MaleThiefExpert1(MaleThief):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleThiefExpert2(MaleThief):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleThiefExpert3(MaleThief):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class MaleThiefRare(MaleThiefExpert3):
    right_hand = Items.ZORLIN_SHAPE
    difficulty = 10

class FemaleThief(RandomizedUnit):
    job = Job.THIEF
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.THIEF
    unlocked_job_level = 2

class FemaleThiefEasy(FemaleThief):
    unlocked_job_level = 4
    difficulty = 2

class FemaleThiefModerate(FemaleThief):
    unlocked_job_level = 6
    difficulty = 4

class FemaleThiefAdvanced(FemaleThief):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 4
    difficulty = 6

class FemaleThiefExpert1(FemaleThief):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleThiefExpert2(FemaleThief):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleThiefExpert3(FemaleThief):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class FemaleThiefExpert4(FemaleThief):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 6
    difficulty = 8

class FemaleThiefRare(FemaleThiefExpert3):
    head = Items.RIBBON
    difficulty = 10


class MaleMediator(RandomizedUnit):
    job = Job.MEDIATOR
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 2

class MaleMediatorEasy(MaleMediator):
    unlocked_job_level = 4
    difficulty = 2

class MaleMediatorModerate(MaleMediator):
    unlocked_job_level = 6
    difficulty = 4

class MaleMediatorAdvanced1(MaleMediator):
    unlocked_job_level = 8
    difficulty = 6

class MaleMediatorAdvanced2(MaleMediator):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6

class MaleMediatorExpert(MaleMediator):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class MaleMediatorRare(MaleMediatorExpert):
    right_hand = Items.GLACIER_GUN


class FemaleMediator(RandomizedUnit):
    job = Job.MEDIATOR
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 2

class FemaleMediatorEasy(FemaleMediator):
    unlocked_job_level = 4
    difficulty = 2

class FemaleMediatorModerate(FemaleMediator):
    unlocked_job_level = 6
    difficulty = 4

class FemaleMediatorAdvanced(FemaleMediator):
    unlocked_job_level = 8
    difficulty = 6

class FemaleMediatorExpert(FemaleMediator):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class FemaleMediatorRare(FemaleMediatorExpert):
    right_hand = Items.MADLEMGEN
    difficulty = 10



class MaleOracle(RandomizedUnit):
    job = Job.ORACLE
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 2


class MaleOracleEasy(MaleOracle):
    unlocked_job_level = 4
    difficulty = 2


class MaleOracleModerate(MaleOracle):
    unlocked_job_level = 6
    difficulty = 4


class MaleOracleAdvanced1(MaleOracle):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6


class MaleOracleAdvanced2(MaleOracle):
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6


class MaleOracleExpert1(MaleOracle):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 2
    difficulty = 8


class MaleOracleExpert2(MaleOracle):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class MaleOracleRare(MaleOracleExpert1):
    body = Items.RUBBER_COSTUME
    difficulty = 10


class FemaleOracle(RandomizedUnit):
    job = Job.ORACLE
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.ORACLE
    unlocked_job_level = 2


class FemaleOracleEasy(FemaleOracle):
    unlocked_job_level = 4
    difficulty = 2


class FemaleOracleModerate(FemaleOracle):
    unlocked_job_level = 6
    difficulty = 4


class FemaleOracleAdvanced(FemaleOracle):
    unlocked_job = UnlockedJob.MEDIATOR
    unlocked_job_level = 3
    difficulty = 6


class FemaleOracleExpert1(FemaleOracle):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 2
    difficulty = 8


class FemaleOracleExpert2(FemaleOracle):
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 8

class FemaleOracleRare(FemaleOracleExpert1):
    right_hand = Items.WHALE_WHISKER
    difficulty = 10


class MaleGeomancer(RandomizedUnit):
    job = Job.GEOMANCER
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 4
    difficulty = 2

class MaleGeomancerModerate(MaleGeomancer):
    unlocked_job_level = 6
    difficulty = 4

class MaleGeomancerAdvanced(MaleGeomancer):
    unlocked_job_level = 8
    difficulty = 6

class MaleGeomancerExpert1(MaleGeomancer):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleGeomancerExpert2(MaleGeomancer):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleGeomancerExpert3(MaleGeomancer):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class MaleGeomancerRare(MaleGeomancerExpert3):
    left_hand = Items.KAISER_PLATE
    difficulty = 10


class FemaleGeomancer(RandomizedUnit):
    job = Job.GEOMANCER
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 4
    difficulty = 2

class FemaleGeomancerModerate(FemaleGeomancer):
    unlocked_job_level = 6
    difficulty = 4

class FemaleGeomancerAdvanced1(FemaleGeomancer):
    unlocked_job_level = 8
    difficulty = 6

class FemaleGeomancerAdvanced2(FemaleGeomancer):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 4
    difficulty = 6

class FemaleGeomancerExpert1(FemaleGeomancer):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleGeomancerExpert2(FemaleGeomancer):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleGeomancerExpert3(FemaleGeomancer):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class FemaleGeomancerRare(FemaleGeomancerExpert3):
    left_hand = Items.GENJI_SHIELD
    difficulty = 10


class MaleLancer(RandomizedUnit):
    job = Job.LANCER
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 4
    difficulty = 2

class MaleLancerModerate(MaleLancer):
    unlocked_job_level = 6
    difficulty = 4

class MaleLancerAdvanced(MaleLancer):
    unlocked_job_level = 8
    difficulty = 6

class MaleLancerExpert1(MaleLancer):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class MaleLancerExpert2(MaleLancer):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class MaleLancerExpert3(MaleLancer):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class MaleLancerRare(MaleLancerExpert3):
    right_hand = Items.DRAGON_WHISKER
    difficulty = 10


class FemaleLancer(RandomizedUnit):
    job = Job.LANCER
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.LANCER
    unlocked_job_level = 4
    difficulty = 2

class FemaleLancerModerate(FemaleLancer):
    unlocked_job_level = 6
    difficulty = 4

class FemaleLancerAdvanced1(FemaleLancer):
    unlocked_job_level = 8
    difficulty = 6

class FemaleLancerAdvanced2(FemaleLancer):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 4
    difficulty = 6

class FemaleLancerExpert1(FemaleLancer):
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 4
    difficulty = 8

class FemaleLancerExpert2(FemaleLancer):
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 4
    difficulty = 8

class FemaleLancerExpert3(FemaleLancer):
    unlocked_job = UnlockedJob.MIME
    unlocked_job_level = 4
    difficulty = 8

class FemaleLancerRare(FemaleLancerExpert3):
    right_hand = Items.HOLY_LANCE
    difficulty = 10


class MaleSamurai(RandomizedUnit):
    job = Job.SAMURAI
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 6
    difficulty = 4

class MaleSamuraiAdvanced(MaleSamurai):
    unlocked_job_level = 8
    difficulty = 6

class MaleSamuraiExpert(MaleSamurai):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class MaleSamuraiRare(MaleSamuraiExpert):
    right_hand = Items.MASAMUNE
    difficulty = 10


class FemaleSamurai(RandomizedUnit):
    job = Job.SAMURAI
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.SAMURAI
    unlocked_job_level = 6
    difficulty = 4


class FemaleSamuraiAdvanced1(FemaleSamurai):
    unlocked_job_level = 8
    difficulty = 6

class FemaleSamuraiAdvanced2(FemaleSamurai):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 4
    difficulty = 6


class FemaleSamuraiExpert(FemaleSamurai):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class FemaleSamuraiRare(FemaleSamuraiExpert):
    right_hand = Items.CHIRIJIRADEN
    difficulty = 10


class MaleNinja(RandomizedUnit):
    job = Job.NINJA
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 6
    difficulty = 4

class MaleNinjaAdvanced(MaleNinja):
    unlocked_job_level = 8
    difficulty = 6

class MaleNinjaExpert(MaleNinja):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class MaleNinjaRare(MaleNinjaExpert):
    right_hand = Items.IGA_KNIFE
    difficulty = 10


class FemaleNinja(RandomizedUnit):
    job = Job.NINJA
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.NINJA
    unlocked_job_level = 6
    difficulty = 4

class FemaleNinjaAdvanced1(FemaleNinja):
    unlocked_job_level = 8
    difficulty = 6

class FemaleNinjaAdvanced2(FemaleNinja):
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 4
    difficulty = 6

class FemaleNinjaExpert(FemaleNinja):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8

class FemaleNinjaRare(FemaleNinjaExpert):
    right_hand = Items.KOGA_KNIFE
    difficulty = 10


class MaleCalculator(RandomizedUnit):
    job = Job.CALCULATOR
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 6

class MaleCalculatorExpert(MaleCalculator):
    unlocked_job_level = 8
    difficulty = 8


class FemaleCalculator(RandomizedUnit):
    job = Job.CALCULATOR
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.CALCULATOR
    unlocked_job_level = 6
    difficulty = 6

class FemaleCalculatorExpert(FemaleCalculator):
    unlocked_job_level = 8
    difficulty = 8


class MaleBard(RandomizedUnit):
    job = Job.BARD
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    unlocked_job = UnlockedJob.BARD
    unlocked_job_level = 6
    difficulty = 6


class FemaleDancer(RandomizedUnit):
    job = Job.DANCER
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    unlocked_job = UnlockedJob.DANCER
    unlocked_job_level = 6
    difficulty = 6


class MaleMime(RandomizedUnit):
    job = Job.MIME
    sprite_set = SpriteSet.GENERIC_MALE
    gender = UnitGender.MALE
    difficulty = 8
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE


class FemaleMime(RandomizedUnit):
    job = Job.MIME
    sprite_set = SpriteSet.GENERIC_FEMALE
    gender = UnitGender.FEMALE
    difficulty = 8
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE
#endregion

#region Special humans
class RamzaC1Squire(RandomizedUnit):
    job = Job.RAMZA_SQUIRE_CHAPTER_1
    sprite_set = SpriteSet.RAMZA_C1
    gender = UnitGender.MALE


class RamzaC23Squire(RandomizedUnit):
    job = Job.RAMZA_SQUIRE_CHAPTER_23
    sprite_set = SpriteSet.RAMZA_C23
    gender = UnitGender.MALE


class RamzaC4Squire(RandomizedUnit):
    job = Job.RAMZA_SQUIRE_CHAPTER_4
    sprite_set = SpriteSet.RAMZA_C4
    gender = UnitGender.MALE
    difficulty = 4


class RamzaC4SquireFullSkillset(RamzaC4Squire):
    primary = ActionAbility.GUTS_C4
    difficulty = 6


class DelitaSquire(RandomizedUnit):
    job = Job.SQUIRE_DELITA
    sprite_set = SpriteSet.DELITA_C1
    gender = UnitGender.MALE

class DelitaSquireHard(DelitaSquire):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6

class DelitaHolyKnight(RandomizedUnit):
    job = Job.HOLY_KNIGHT_DELITA
    sprite_set = SpriteSet.DELITA_C2
    gender = UnitGender.MALE
    difficulty = 4

class DelitaHolyKnightHard(DelitaHolyKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10

class DelitaArcKnight(RandomizedUnit):
    job = Job.ARC_KNIGHT_DELITA
    sprite_set = SpriteSet.DELITA_C4
    gender = UnitGender.MALE
    difficulty = 4

class DelitaArcKnightHard(DelitaArcKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 110


class Algus(RandomizedUnit):
    job = Job.SQUIRE_ALGUS
    sprite_set = SpriteSet.ALGUS
    gender = UnitGender.MALE

class AlgusHard(Algus):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6

class AlgusWithCrossbow(Algus):
    support = SupportAbility.EQUIP_CROSSBOW

class AlgusWithCrossbowHard(AlgusWithCrossbow):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class ZalbagArcKnight(RandomizedUnit):
    job = Job.ARC_KNIGHT_ZALBAG
    sprite_set = SpriteSet.ZALBAG
    gender = UnitGender.MALE
    difficulty = 4

class ZalbagArcKnightHard(ZalbagArcKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10

class LuneKnight(RandomizedUnit):
    job = Job.LUNE_KNIGHT
    sprite_set = SpriteSet.DYCEDARG
    gender = UnitGender.MALE
    difficulty = 4

class LuneKnightHard(LuneKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10

class Princess(RandomizedUnit):
    job = Job.PRINCESS
    sprite_set = SpriteSet.OVELIA
    gender = UnitGender.FEMALE

class PrincessHard(Princess):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class HolySwordsman(RandomizedUnit):
    job = Job.HOLY_SWORDSMAN
    sprite_set = SpriteSet.ORLANDU
    gender = UnitGender.MALE
    difficulty = 8

class HolySwordsmanHard(HolySwordsman):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12

class HolySwordsmanWithExcalibur(HolySwordsman):
    right_hand: Items = Items.EXCALIBUR
    difficulty = 12


class Dragoner(RandomizedUnit):
    job = Job.DRAGONER
    sprite_set = SpriteSet.REIS
    gender = UnitGender.FEMALE
    difficulty = 4

class DragonerHard(Dragoner):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10

class HolyPriest(RandomizedUnit):
    job = Job.HOLY_PRIEST
    sprite_set = SpriteSet.ZALMO
    gender = UnitGender.MALE

class HolyPriestHard(HolyPriest):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class DarkKnight(RandomizedUnit):
    job = Job.DARK_KNIGHT_GUEST
    sprite_set = SpriteSet.GAFGARION
    gender = UnitGender.MALE
    difficulty = 4

class DarkKnightHard(DarkKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10


class Astrologist(RandomizedUnit):
    job = Job.ASTROLOGIST
    sprite_set = SpriteSet.OLAN
    gender = UnitGender.MALE
    difficulty = 8

class AstrologistHard(Astrologist):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class EngineerMustadio(RandomizedUnit):
    job = Job.ENGINEER_MUSTADIO
    sprite_set = SpriteSet.MUSTADIO
    gender = UnitGender.MALE

class EngineerMustadioHard(EngineerMustadio):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class HellKnight(RandomizedUnit):
    job = Job.HELL_KNIGHT
    sprite_set = SpriteSet.MALAK
    gender = UnitGender.MALE

class HellKnightHard(HellKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class ArcKnightElmdor(RandomizedUnit):
    job = Job.ARC_KNIGHT_ELMDOR
    sprite_set = SpriteSet.ELMDOR
    gender = UnitGender.MALE
    difficulty = 8

class ArcKnightElmdorHard(ArcKnightElmdor):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12

class ArcKnightElmdorWithKit(ArcKnightElmdor):
    primary = ActionAbility.SWORD_SPIRIT_2
    secondary = ActionAbility.BLOOD_SUCK
    reaction = ReactionAbility.BLADE_GRASP
    difficulty = 12


class HolyKnightAgrias(RandomizedUnit):
    job = Job.HOLY_KNIGHT_AGRIAS
    sprite_set = SpriteSet.AGRIAS
    gender = UnitGender.FEMALE
    difficulty = 4

class HolyKnightAgriasHard(HolyKnightAgrias):
    unlocked_job = UnlockedJob.MIME
    difficulty = 10


class TempleKnight(RandomizedUnit):
    job = Job.TEMPLE_KNIGHT
    sprite_set = SpriteSet.BEOWULF
    gender = UnitGender.MALE
    difficulty = 8

class TempleKnightHard(TempleKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class DivineKnightVormav(RandomizedUnit):
    job = Job.DIVINE_KNIGHT_VORMAV
    sprite_set = SpriteSet.VORMAV
    gender = UnitGender.MALE
    difficulty = 6

class DivineKnightVormavHard(DivineKnightVormav):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class DivineKnightRofel(RandomizedUnit):
    job = Job.DIVINE_KNIGHT_ROFEL
    sprite_set = SpriteSet.ROFEL
    gender = UnitGender.MALE
    difficulty = 6

class DivineKnightRofelHard(DivineKnightRofel):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class KnightBlade(RandomizedUnit):
    job = Job.KNIGHT_BLADE
    sprite_set = SpriteSet.IZLUDE
    gender = UnitGender.MALE

class KnightBladeHard(KnightBlade):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class KnightBladeWithKit(KnightBlade):
    primary = ActionAbility.IZLUDE_BATTLE_SKILL
    secondary = ActionAbility.IZLUDE_JUMP
    support = SupportAbility.MAINTENANCE
    difficulty = 6


class Sorcerer(RandomizedUnit):
    job = Job.SORCERER
    primary = ActionAbility.KLETIAN_ALL_MAGIC
    sprite_set = SpriteSet.KLETIAN
    gender = UnitGender.MALE
    difficulty = 8

class SorcererHard(Sorcerer):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class WhiteKnight(RandomizedUnit):
    job = Job.WHITE_KNIGHT_C3
    sprite_set = SpriteSet.WIEGRAF2
    gender = UnitGender.MALE
    difficulty = 3

class WhiteKnightHard(WhiteKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class WhiteKnightWithCounter(WhiteKnight):
    reaction = ReactionAbility.COUNTER

class WhiteKnightWithCounterHard(WhiteKnightWithCounter):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class WhiteKnightChapter1(WhiteKnight):
    job = Job.WHITE_KNIGHT_C1
    sprite_set = SpriteSet.WIEGRAF1

class WhiteKnightChapter1Hard(WhiteKnightChapter1):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class WhiteKnightChapter1WithCounter(WhiteKnightChapter1):
    reaction = ReactionAbility.COUNTER

class WhiteKnightChapter1WithCounterHard(WhiteKnightChapter1WithCounter):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class HeavenKnight(RandomizedUnit):
    job = Job.HEAVEN_KNIGHT
    sprite_set = SpriteSet.RAFA
    gender = UnitGender.FEMALE

class HeavenKnightHard(HeavenKnight):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class DivineKnightMeliadoul(RandomizedUnit):
    job = Job.DIVINE_KNIGHT_MELIADOUL_ENEMY
    sprite_set = SpriteSet.MELIADOUL
    gender = UnitGender.FEMALE
    difficulty = 6

class DivineKnightMeliadoulHard(DivineKnightMeliadoul):
    unlocked_job = UnlockedJob.MIME
    difficulty = 12


class EngineerBalk(RandomizedUnit):
    job = Job.ENGINEER_BALK
    sprite_set = SpriteSet.BALK
    gender = UnitGender.MALE

class EngineerBalkHard(EngineerBalk):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class AssassinCelia(RandomizedUnit):
    job = Job.ASSASSIN_CELIA
    sprite_set = SpriteSet.CELIA
    gender = UnitGender.FEMALE
    difficulty = 10


class AssassinLede(RandomizedUnit):
    job = Job.ASSASSIN_LEDE
    sprite_set = SpriteSet.LEDE
    gender = UnitGender.FEMALE
    difficulty = 10


class Cleric(RandomizedUnit):
    job = Job.CLERIC
    sprite_set = SpriteSet.ALMA
    gender = UnitGender.FEMALE

class ClericHard(Cleric):
    unlocked_job = UnlockedJob.MIME
    difficulty = 6


class ClericWithUltima(Cleric):
    primary = ActionAbility.HOLY_MAGIC
    difficulty = 3

class ClericWithUltimaHard(Cleric):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class Soldier(RandomizedUnit):
    job = Job.SOLDIER
    sprite_set = SpriteSet.CLOUD
    gender = UnitGender.MALE
    difficulty = 4

class SoldierHard(Soldier):
    unlocked_job = UnlockedJob.MIME
    difficulty = 8


class ArcKnightZombie(RandomizedUnit):
    job = Job.ARC_KNIGHT_ZOMBIE
    sprite_set = SpriteSet.ZALBAG_ZOMBIE
    gender = UnitGender.MALE
    difficulty = 8


class ArcKnightZombieWithKit(ArcKnightZombie):
    secondary = ActionAbility.BLOOD_SUCK
    difficulty = 12


class UndeadKnight(RandomizedUnit):
    job = Job.KNIGHT_UNDEAD
    sprite_set = SpriteSet.UNDEAD_KNIGHT
    gender = UnitGender.MONSTER


class UndeadArcher(RandomizedUnit):
    job = Job.ARCHER_UNDEAD
    sprite_set = SpriteSet.UNDEAD_ARCHER
    gender = UnitGender.MALE


class UndeadWizard(RandomizedUnit):
    job = Job.WIZARD_UNDEAD
    sprite_set = SpriteSet.UNDEAD_WIZARD
    gender = UnitGender.MALE


class UndeadTimeMage(RandomizedUnit):
    job = Job.TIME_MAGE_UNDEAD
    sprite_set = SpriteSet.UNDEAD_TIMEMAGE
    gender = UnitGender.FEMALE


class UndeadOracle(RandomizedUnit):
    job = Job.ORACLE_UNDEAD
    sprite_set = SpriteSet.UNDEAD_ORACLE
    gender = UnitGender.MALE


class UndeadSummoner(RandomizedUnit):
    job = Job.SUMMONER_UNDEAD
    sprite_set = SpriteSet.UNDEAD_SUMMONER
    gender = UnitGender.FEMALE


class Altima1(RandomizedUnit):
    job = Job.ALTIMA_1
    sprite_set = SpriteSet.ALTIMA_1
    gender = UnitGender.MONSTER
    hidden_stats = True
    primary = ActionAbility.ULTIMATE_MAGIC
    secondary = ActionAbility.CHAOS
    difficulty = 14


class Altima2(RandomizedUnit):
    job = Job.ALTIMA_2
    sprite_set = SpriteSet.ALTIMA_2
    gender = UnitGender.MONSTER
    hidden_stats = True
    primary = ActionAbility.COMPLETE_MAGIC
    secondary = ActionAbility.SATURATION
    difficulty = 14
#endregion

#region Generic monsters
class GenericMonster(RandomizedUnit):
    sprite_set = SpriteSet.MONSTER
    gender = UnitGender.MONSTER
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 1


class YellowChocobo(GenericMonster):
    job = Job.YELLOW_CHOCOBO


class BlackChocobo(GenericMonster):
    job = Job.BLACK_CHOCOBO
    difficulty = 4


class RedChocobo(GenericMonster):
    job = Job.RED_CHOCOBO
    difficulty = 6


class Goblin(GenericMonster):
    job = Job.GOBLIN


class BlackGoblin(GenericMonster):
    job = Job.BLACK_GOBLIN


class Gobbledeguck(GenericMonster):
    job = Job.GOBBLEDEGUCK
    difficulty = 4


class Bomb(GenericMonster):
    job = Job.BOMB


class Grenade(GenericMonster):
    job = Job.GRENADE


class Explosive(GenericMonster):
    job = Job.EXPLOSIVE
    difficulty = 4


class RedPanther(GenericMonster):
    job = Job.RED_PANTHER


class Cuar(GenericMonster):
    job = Job.CUAR


class Vampire(GenericMonster):
    job = Job.VAMPIRE
    difficulty = 4


class PiscoDemon(GenericMonster):
    job = Job.PISCO_DEMON


class Squidlarkin(GenericMonster):
    job = Job.SQUIDLARKIN


class Mindflare(GenericMonster):
    job = Job.MINDFLARE
    difficulty = 6


class Skeleton(GenericMonster):
    job = Job.SKELETON


class BoneSnatch(GenericMonster):
    job = Job.BONE_SNATCH


class LivingBone(GenericMonster):
    job = Job.LIVING_BONE
    difficulty = 4


class Ghoul(GenericMonster):
    job = Job.GHOUL


class Gust(GenericMonster):
    job = Job.GUST


class Revnant(GenericMonster):
    job = Job.REVNANT
    difficulty = 4


class Flotiball(GenericMonster):
    job = Job.FLOTIBALL


class Ahriman(GenericMonster):
    job = Job.AHRIMAN


class Plague(GenericMonster):
    job = Job.PLAGUE
    difficulty = 4


class Juravis(GenericMonster):
    job = Job.JURAVIS


class SteelHawk(GenericMonster):
    job = Job.STEEL_HAWK


class Cocatoris(GenericMonster):
    job = Job.COCATORIS
    difficulty = 4


class Uribo(GenericMonster):
    job = Job.URIBO


class Porky(GenericMonster):
    job = Job.PORKY


class Wildbow(GenericMonster):
    job = Job.WILDBOW


class Woodman(GenericMonster):
    job = Job.WOODMAN


class Trent(GenericMonster):
    job = Job.TRENT


class Taiju(GenericMonster):
    job = Job.TAIJU


class BullDemon(GenericMonster):
    job = Job.BULL_DEMON


class Minitaurus(GenericMonster):
    job = Job.MINITAURUS


class Sacred(GenericMonster):
    job = Job.SACRED
    difficulty = 4


class Morbol(GenericMonster):
    job = Job.MORBOL


class Ochu(GenericMonster):
    job = Job.OCHU


class GreatMorbol(GenericMonster):
    job = Job.GREAT_MORBOL
    difficulty = 4


class Behemoth(GenericMonster):
    job = Job.BEHEMOTH
    difficulty = 4


class KingBehemoth(GenericMonster):
    job = Job.KING_BEHEMOTH
    difficulty = 6


class DarkBehemoth(GenericMonster):
    job = Job.DARK_BEHEMOTH
    difficulty = 8


class Dragon(GenericMonster):
    job = Job.DRAGON


class BlueDragon(GenericMonster):
    job = Job.BLUE_DRAGON
    difficulty = 4


class RedDragon(GenericMonster):
    job = Job.RED_DRAGON
    difficulty = 4


class Hyudra(GenericMonster):
    job = Job.HYUDRA
    difficulty = 4


class Hydra(GenericMonster):
    job = Job.HYDRA
    difficulty = 6


class Tiamat(GenericMonster):
    job = Job.TIAMAT
    difficulty = 8
#endregion

#region Special monsters
class SpecialMonster(RandomizedUnit):
    sprite_set = SpriteSet.MONSTER
    gender = UnitGender.MONSTER
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 1
    difficulty = 6


class HolyDragon(SpecialMonster):
    job = Job.HOLY_DRAGON
    sprite_set = SpriteSet.HOLY_DRAGON


class Byblos(SpecialMonster):
    job = Job.BYBLOS


class SteelGiant(SpecialMonster):
    job = Job.STEEL_GIANT


class Apanda(SpecialMonster):
    job = Job.APANDA


class ArchaicDemon(SpecialMonster):
    job = Job.ARCHAIC_DEMON


class UltimaDemon(SpecialMonster):
    job = Job.ULTIMA_DEMON
#endregion

#region Lucavi
class Velius(RandomizedUnit):
    job = Job.VELIUS
    sprite_set = SpriteSet.VELIUS
    gender = UnitGender.MONSTER
    hidden_stats = True
    difficulty = 8


class VeliusWithKit(Velius):
    primary = ActionAbility.VELIUS_FEAR
    secondary = ActionAbility.WARLOCK_SUMMON


class Zalera(RandomizedUnit):
    job = Job.ZALERA
    sprite_set = SpriteSet.ZALERA
    gender = UnitGender.MALE
    hidden_stats = True
    difficulty = 8


class ZaleraWithKit(Zalera):
    primary = ActionAbility.ZALERA_FEAR
    secondary = ActionAbility.JA_MAGIC


class Hashmalum(RandomizedUnit):
    job = Job.HASHMALUM
    sprite_set = SpriteSet.HASHMALUM
    gender = UnitGender.MALE
    hidden_stats = True
    difficulty = 10


class HashmalumWithKit(Hashmalum):
    primary = ActionAbility.HASHMALUM_FEAR
    secondary = ActionAbility.DIMENSION_MAGIC


class Queklain(RandomizedUnit):
    job = Job.QUEKLAIN
    sprite_set = SpriteSet.QUEKLAIN
    gender = UnitGender.MALE
    hidden_stats = True
    difficulty = 6


class QueklainWithKit(Queklain):
    primary = ActionAbility.QUEKLAIN_FEAR
    secondary = ActionAbility.IMPURE


class Adramelk(RandomizedUnit):
    job = Job.ADRAMELK
    sprite_set = SpriteSet.ADRAMELK
    gender = UnitGender.MONSTER
    hidden_stats = True
    difficulty = 8


class AdramelkWithKit(Adramelk):
    primary = ActionAbility.ADRAMELK_FEAR
    secondary = ActionAbility.ADRAMELK_ALL_MAGIC


class Elidibs(RandomizedUnit):
    job = Job.ELIDIBS
    sprite_set = SpriteSet.MONSTER
    gender = UnitGender.MONSTER
    hidden_stats = True
    difficulty = 12
#endregion

#region Story enemies
class Wiegraf1Boss(WhiteKnightChapter1):
    birthday_month = Month.AUGUST
    birthday_day = 23
    brave = 71
    faith = 64
    primary = ActionAbility.WIEGRAF_1_HOLY_SWORD
    reaction = ReactionAbility.COUNTER
    movement = MovementAbility.JUMP_PLUS_1
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 5

class AlgusBoss(Algus):
    birthday_month = Month.AUGUST
    birthday_day = 29
    brave = 32
    faith = 67
    job = Job.KNIGHT
    reaction = ReactionAbility.AUTO_POTION
    support = SupportAbility.EQUIP_CROSSBOW
    movement = MovementAbility.MOVE_PLUS_1
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 3

class Gafgarion(DarkKnight):
    job = Job.DARK_KNIGHT_ENEMY
    birthday_month = Month.AUGUST
    birthday_day = 26
    brave = 61
    faith = 67

class Gafgarion1Boss(Gafgarion):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 4

class Gafgarion2Boss(Gafgarion):
    unlocked_job = UnlockedJob.GEOMANCER
    unlocked_job_level = 5
    right_hand = Items.BLOOD_SWORD

class Gafgarion3Boss(Gafgarion):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 7
    secondary = ActionAbility.NONE

class QueklainBoss(QueklainWithKit):
    birthday_month = Month.NOVEMBER
    birthday_day = 15
    brave = 70
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE

class Zalmo(HolyPriest):
    birthday_month = Month.DECEMBER
    birthday_day = 7
    brave = 54
    faith = 78
    body = Items.WHITE_ROBE

class Zalmo1Boss(Zalmo):
    reaction = ReactionAbility.ARROW_GUARD
    support = SupportAbility.HALF_OF_MP
    movement = MovementAbility.MOVE_HP_UP
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 7

class IzludeBoss(KnightBladeWithKit):
    birthday_month = Month.MAY
    birthday_day = 28
    brave = 73
    faith = 62
    reaction = ReactionAbility.COUNTER
    movement = MovementAbility.IGNORE_HEIGHT

class Wiegraf2Boss(WhiteKnightWithCounter):
    birthday_month = Month.AUGUST
    birthday_day = 23
    brave = 71
    faith = 64
    support = SupportAbility.TWO_HANDS
    movement = MovementAbility.MOVE_PLUS_1
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 7

class Malak(HellKnight):
    birthday_month = Month.JUNE
    birthday_day = 9
    brave = 69
    faith = 31
    unlocked_job = UnlockedJob.BASE

class Malak1Boss(Malak):
    unlocked_job_level = 4

class Malak2Boss(Malak):
    unlocked_job_level = 3

class Wiegraf3Boss(WhiteKnightWithCounter):
    birthday_month = Month.AUGUST
    birthday_day = 23
    brave = 71
    faith = 64
    primary = ActionAbility.WIEGRAF_3_HOLY_SWORD
    secondary = ActionAbility.WIEGRAF_3_PUNCH_SKILL
    support = SupportAbility.MAINTENANCE
    movement = MovementAbility.MOVE_PLUS_1

class VeliusBoss(VeliusWithKit):
    birthday_month = Month.AUGUST
    birthday_day = 23
    brave = 70
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE

class Elmdor(ArcKnightElmdor):
    birthday_month = Month.MAY
    birthday_day = 21
    brave = 70
    faith = 70

class Elmdor1Boss(Elmdor):
    primary = ActionAbility.SWORD_SPIRIT_1
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.HAMEDO
    support = SupportAbility.TWO_HANDS
    movement = MovementAbility.IGNORE_HEIGHT

class Celia(AssassinCelia):
    birthday_month = Month.AUGUST
    birthday_day = 30
    brave = 65
    faith = 70
    primary = ActionAbility.CELIA_USE_HAND

class Lede(AssassinLede):
    birthday_month = Month.DECEMBER
    birthday_day = 13
    brave = 65
    faith = 70
    primary = ActionAbility.LEDE_USE_HAND

class Celia1Boss(Celia):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 8
    accessory = Items.CACHUSHA

class Lede1Boss(Lede):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 8
    accessory = Items.BARETTE

class MeliadoulBoss(DivineKnightMeliadoul):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 4
    birthday_month = Month.DECEMBER
    birthday_day = 24
    brave = 67
    faith = 68
    accessory = Items.CHANTAGE

class Zalmo2Boss(Zalmo):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 8

class Balk(EngineerBalk):
    birthday_month = Month.DECEMBER
    birthday_day = 6
    brave = 64
    faith = 62

class Balk1Boss(Balk):
    right_hand = Items.BLAZE_GUN
    difficulty = 12

class Celia2Boss(Celia):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3

class Lede2Boss(Lede):
    unlocked_job = UnlockedJob.SUMMONER
    unlocked_job_level = 3

class Celia3Boss(Celia2Boss):
    secondary = ActionAbility.CELIA_THROW

class Lede3Boss(Lede2Boss):
    secondary = ActionAbility.LEDE_THROW

class Elmdor2Boss(Elmdor):
    primary = ActionAbility.SWORD_SPIRIT_1
    secondary = ActionAbility.BLOOD_SUCK
    reaction = ReactionAbility.BLADE_GRASP
    support = SupportAbility.MARTIAL_ARTS
    movement = MovementAbility.TELEPORT_2
    right_hand = Items.MASAMUNE
    left_hand = Items.GENJI_SHIELD
    head = Items.GENJI_HELMET
    body = Items.GENJI_ARMOR
    accessory = Items.GENJI_GAUNTLET
    difficulty = 12

class ZaleraBoss(ZaleraWithKit):
    birthday_month = Month.MAY
    birthday_day = 21
    brave = 70
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE

class DycedargBoss(LuneKnight):
    birthday_month = Month.OCTOBER
    birthday_day = 24
    brave = 66
    faith = 77
    primary = ActionAbility.SWORD_SKILL
    secondary = ActionAbility.DYCEDARG_ALL_MAGIC
    reaction = ReactionAbility.CATCH
    support = SupportAbility.DEFEND
    movement = MovementAbility.MOVE_PLUS_1
    difficulty = 6

class AdramelkBoss(AdramelkWithKit):
    birthday_month = Month.OCTOBER
    birthday_day = 24
    brave = 70
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE

class VormavBoss(DivineKnightVormav):
    birthday_month = Month.JULY
    birthday_day = 23
    brave = 65
    faith = 70
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 4
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.COUNTER
    support = SupportAbility.DEFENSE_UP
    movement = MovementAbility.MOVE_PLUS_1

class Rofel(DivineKnightRofel):
    birthday_month = Month.DECEMBER
    birthday_day = 23
    brave = 60
    faith = 68

class Rofel1Boss(Rofel):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 4
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.COUNTER_FLOOD
    support = SupportAbility.DEFENSE_UP
    movement = MovementAbility.JUMP_PLUS_1

class Kletian(Sorcerer):
    birthday_month = Month.JUNE
    birthday_day = 6
    brave = 51
    faith = 81

class Kletian1Boss(Kletian):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 6
    reaction = ReactionAbility.COUNTER_MAGIC
    support = SupportAbility.MAGIC_DEFEND_UP
    movement = MovementAbility.IGNORE_HEIGHT

class ZalbagBoss(ArcKnightZombie):
    birthday_month = Month.JUNE
    birthday_day = 30
    brave = 33
    faith = 77
    primary = ActionAbility.DESTROY_SWORD
    secondary = ActionAbility.BLOOD_SUCK
    reaction = ReactionAbility.SPEED_SAVE
    support = SupportAbility.DEFENSE_UP
    movement = MovementAbility.MOVE_HP_UP

class Rofel2Boss(Rofel):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 8
    secondary = ActionAbility.ROFEL_ALL_MAGIC
    reaction = ReactionAbility.WEAPON_GUARD
    support = SupportAbility.DEFENSE_UP
    movement = MovementAbility.IGNORE_HEIGHT
    right_hand = Items.SAVE_THE_QUEEN
    difficulty = 12

class Kletian2Boss(Kletian):
    unlocked_job = UnlockedJob.BASE
    unlocked_job_level = 6
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.MA_SAVE
    support = SupportAbility.MAGIC_DEFEND_UP
    movement = MovementAbility.FLY
    right_hand = Items.MACE_OF_ZEUS
    difficulty = 10

class Balk2Boss(Balk):
    primary = ActionAbility.SNIPE
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.COUNTER
    support = SupportAbility.MARTIAL_ARTS
    movement = MovementAbility.MOVE_HP_UP
    right_hand = Items.BLAST_GUN
    head = Items.THIEF_HAT
    difficulty = 12

class HashmalumBoss(HashmalumWithKit):
    birthday_month = Month.JULY
    birthday_day = 23
    brave = 70
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE

class Altima1Boss(Altima1):
    birthday_month = Month.SEPTEMBER
    birthday_day = 11
    brave = 70
    faith = 70
    reaction = ReactionAbility.ABSORB_USED_MP
    support = SupportAbility.NONE
    movement = MovementAbility.NONE
    right_hand = Items.NONE
    left_hand = Items.NONE
    head = Items.NONE
    body = Items.NONE
    accessory = Items.NONE


class Altima2Boss(Altima2):
    birthday_month = Month.SEPTEMBER
    birthday_day = 11
    brave = 60
    faith = 70
    reaction = ReactionAbility.NONE
    support = SupportAbility.NONE
    movement = MovementAbility.NONE
    right_hand = Items.NONE
    left_hand = Items.NONE
    head = Items.NONE
    body = Items.NONE
    accessory = Items.NONE

class Worker7Boss(SteelGiant):
    brave = 50
    faith = 0
    primary = ActionAbility.JOB
    secondary = ActionAbility.NONE
    reaction = ReactionAbility.NONE
    support = SupportAbility.DEFENSE_UP
    movement = MovementAbility.NONE
    right_hand = Items.NONE
    left_hand = Items.NONE
    head = Items.NONE
    body = Items.NONE
    accessory = Items.NONE

class ElidibsBoss(Elidibs):
    birthday_month = Month.UNKNOWN
    birthday_day = 0
    brave = 70
    faith = 70
    right_hand = Items.NONE
    left_hand = Items.NONE
    head = Items.NONE
    body = Items.NONE
    accessory = Items.NONE




#endregion