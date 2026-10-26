from enum import IntEnum

class Ability(IntEnum):
    NOTHING = 0x00
    CURE = 0x01
    CURE_2 = 0x02
    RAISE = 0x05
    RAISE_2 = 0x06
    PROTECT = 0x09
    PROTECT_2 = 0x0A
    SHELL = 0x0B
    SHELL_2 = 0x0C
    WALL = 0x0D
    ESUNA = 0x0E
    HOLY = 0x0F
    FIRE = 0x10
    FIRE_2 = 0x11
    BOLT = 0x14
    BOLT_2 = 0x15
    ICE = 0x18
    ICE_2 = 0x19
    FLARE = 0x1F
    HASTE = 0x20
    HASTE_2 = 0x21
    SLOW = 0x22
    SLOW_2 = 0x23
    STOP = 0x24
    FLOAT = 0x26
    REFLECT = 0x27
    QUICK = 0x29
    SPELL_ABSORB = 0x2F
    LIFE_DRAIN = 0x30
    ZOMBIE_ORACLE = 0x33
    CONFUSION_SONG = 0x37
    SLEEP = 0x3A
    LICH = 0x49
    CHAKRA = 0x6A
    REVIVE = 0x6B
    INSULT = 0x7C
    THREATEN = 0x77
    MIMIC_DARAVON = 0x7D
    MAGIC_BREAK = 0x8E
    SPEED_BREAK = 0x8F
    POWER_BREAK = 0x90
    MIND_BREAK = 0x91
    YELL = 0x96
    CHEER_UP = 0x97
    SCREAM = 0x99
    ULTIMA = 0x9A
    DARK_HOLY = 0xA6
    NIGHT_SWORD = 0xA5
    LOSE_VOICE = 0xBF
    BLOOD_SUCK_HUMAN = 0xC8
    BIO_POISON = 0xCB
    BIO_2_SLOW = 0xCE
    BIO_3_UNDEAD = 0xD2
    LEG_AIM = 0xD5
    MELT = 0xD8
    TORNADO = 0xD9
    QUAKE = 0xDA
    GRAVI_2 = 0xDE
    FLARE_2 = 0xDF
    MUTE = 0xE7
    DESPAIR_2 = 0xE8
    RETURN_2 = 0xE9
    PROTECT_SPIRIT = 0x13C
    CLAM_SPIRIT = 0x13D
    GATHER_POWER = 0x143
    DARK_WHISPER = 0x158
    MIDGAR_SWARM = 0x15B
    LIFEBREAK = 0x15C
    GRAND_CROSS = 0x15E
    DISPOSE = 0x161
    ENERGY = 0x163


class ReactionAbility(IntEnum):
    NONE = 0x0000
    FACE_UP = 0x1AE
    CRITICAL_QUICK = 0x1B1
    COUNTER_TACKLE = 0x1B4
    COUNTER = 0x1BA
    WEAPON_GUARD = 0x1BF

class SupportAbility(IntEnum):
    NONE = 0x0000
    EQUIP_AXE = 0x1CC
    HALF_OF_MP = 0x1CE
    GAINED_JP_UP = 0x1CF
    DEFENSE_UP = 0x1D2
    MAGIC_DEFEND_UP = 0x1D4
    CONCENTRATE = 0x1D5
    TRAIN = 0x1D6
    SECRET_HUNT = 0x1D7
    MARTIAL_ARTS = 0x1D8
    MONSTER_TALK = 0x1D9
    THROW_ITEM = 0x1DA
    MAINTANENCE = 0x1DB
    TWO_HANDS = 0x1DC
    TWO_SWORDS = 0x1DD
    MONSTER_SKILL = 0x1DE
    DEFEND = 0x1DF
    SHORT_CHARGE = 0x1E2
    NON_CHARGE = 0x1E3

class MovementAbility(IntEnum):
    NONE = 0x0000
    MOVE_PLUS_1 = 0x1E6
    IGNORE_HEIGHT = 0x1EC
    NO_WATER = 0x1F1
    TELEPORT = 0x1F2
    TELEPORT_2 = 0x1F3
    ANY_WEATHER = 0x1F4
    ANY_GROUND = 0x1F5
    MOVE_IN_WATER = 0x1F6
    WALK_ON_WATER = 0x1F7
    MOVE_UNDER_WATER = 0x1F9
    FLOAT = 0x1FA
    FLY = 0x1FB
    MOVE_FIND_ITEM = 0x1FD


class SkillsetMetaclass(type):
    skillset_name: str = "Skillset"
    skillset_description: str = "Test description"

    action_abilities: list[Ability]
    rsm_abilities: list[ReactionAbility | SupportAbility | MovementAbility]

class Skillset(object, metaclass=SkillsetMetaclass):
    action_abilities = [Ability.NOTHING for i in range(16)]
    rsm_abilities = [
        ReactionAbility.COUNTER_TACKLE,
        SupportAbility.EQUIP_AXE, SupportAbility.MONSTER_SKILL, SupportAbility.DEFEND, SupportAbility.GAINED_JP_UP,
        MovementAbility.MOVE_PLUS_1
    ]

class BerserkArts(Skillset):
    skillset_name = "Berserk Arts"

    action_abilities = [
        Ability.INSULT, Ability.THREATEN, Ability.YELL, Ability.SCREAM, Ability.GATHER_POWER
    ]

class RedMagic(Skillset):
    skillset_name = "Red Magic"

    action_abilities = [
        Ability.CURE, Ability.CURE_2, Ability.RAISE, Ability.PROTECT, Ability.SHELL,
        Ability.FIRE, Ability.FIRE_2, Ability.BOLT, Ability.BOLT_2, Ability.ICE, Ability.ICE_2,
        Ability.HASTE, Ability.SLOW, Ability.SPELL_ABSORB, Ability.CONFUSION_SONG, Ability.SLEEP
    ]

class VanguardSkill(Skillset):
    skillset_name = "Vanguard Skill"

    action_abilities = [
        Ability.PROTECT_SPIRIT, Ability.PROTECT_2, Ability.CLAM_SPIRIT, Ability.SHELL_2,
        Ability.WALL, Ability.FLOAT, Ability.REFLECT
    ]

class Hunting(Skillset):
    skillset_name = "Hunting"

    action_abilities = [
        Ability.MAGIC_BREAK, Ability.SPEED_BREAK, Ability.POWER_BREAK, Ability.MIND_BREAK,
        Ability.LEG_AIM
    ]

class UltimateTimeMagic(Skillset):
    skillset_name = "Ultimate Time"

    action_abilities = [
        Ability.HASTE_2, Ability.SLOW_2, Ability.STOP, Ability.QUICK, Ability.RETURN_2, Ability.GRAVI_2
    ]
    rsm_abilities = [
        ReactionAbility.CRITICAL_QUICK,
        SupportAbility.SHORT_CHARGE, SupportAbility.MONSTER_SKILL, SupportAbility.DEFEND, SupportAbility.GAINED_JP_UP,
        MovementAbility.TELEPORT_2
    ]

class CatalogArts(Skillset):
    skillset_name = "Catalog Arts"

    action_abilities = [
        Ability.LOSE_VOICE, Ability.MIMIC_DARAVON, Ability.MUTE, Ability.CHEER_UP,
        Ability.PROTECT, Ability.SHELL, Ability.ENERGY, Ability.DISPOSE
    ]

class DarkMagic(Skillset):
    skillset_name = "Dark Magic"

    action_abilities = [
        Ability.RAISE_2, Ability.REVIVE, Ability.ZOMBIE_ORACLE, Ability.BIO_POISON,
        Ability.BIO_3_UNDEAD, Ability.DARK_HOLY, Ability.DARK_WHISPER, Ability.LICH,
        Ability.LIFE_DRAIN
    ]

class VampireArts(Skillset):
    skillset_name = "Vampiric Arts"

    action_abilities = [
        Ability.NIGHT_SWORD, Ability.BLOOD_SUCK_HUMAN, Ability.LIFEBREAK, Ability.BIO_2_SLOW,
        Ability.DESPAIR_2
    ]

class HighMagic(Skillset):
    skillset_name = "High Magic"

    action_abilities = [
        Ability.HOLY, Ability.FLARE, Ability.FLARE_2, Ability.MIDGAR_SWARM, Ability.QUAKE,
        Ability.TORNADO, Ability.MELT, Ability.GRAND_CROSS
    ]
