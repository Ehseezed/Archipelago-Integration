from enum import IntFlag, auto


class EquippableItemsOne(IntFlag):
    ROD = auto()
    AXE = auto()
    KATANA = auto()
    KNIGHTSWORD = auto()
    SWORD = auto()
    NINJA_BLADE = auto()
    KNIFE = auto()
    UNARMED = auto()

class EquippableItemsTwo(IntFlag):
    POLEARM = auto()
    BOOK = auto()
    INSTRUMENT = auto()
    BOW = auto()
    CROSSBOW = auto()
    GUN = auto()
    FLAIL = auto()
    STAFF = auto()

class EquippableItemsThree(IntFlag):
    ARMOR = auto()
    RIBBON = auto()
    HAT = auto()
    HELMET = auto()
    SHIELD = auto()
    CLOTH = auto()
    BAG = auto()
    POLE = auto()

class EquippableItemsFour(IntFlag):
    PERFUME = auto()
    CLOAK = auto()
    ARMLET = auto()
    RING = auto()
    ARMGUARD = auto()
    SHOES = auto()
    ROBE = auto()
    CLOTHING = auto()
    STANDARD_ACCESSORIES = CLOAK | ARMLET | RING | ARMGUARD | SHOES

class StatusesOne(IntFlag):
    PERFORMING = auto()
    DEFENDING = auto()
    JUMP = auto()
    CHARGING = auto()
    UNDEAD = auto()
    DEAD = auto()
    CRYSTAL = auto()
    NONE = auto()

class StatusesTwo(IntFlag):
    TREASURE = auto()
    DARKEVIL = auto()
    BLOOD_SUCK = auto()
    SILENCE = auto()
    CONFUSION = auto()
    DARKNESS = auto()
    INVITE = auto()
    PETRIFY = auto()

class StatusesThree(IntFlag):
    CRITICAL = auto()
    FROG = auto()
    CHICKEN = auto()
    BERSERK = auto()
    TRANSPARENT = auto()
    RERAISE = auto()
    FLOAT = auto()
    OIL = auto()

class StatusesFour(IntFlag):
    WALL = auto()
    STOP = auto()
    SLOW = auto()
    HASTE = auto()
    SHELL = auto()
    PROTECT = auto()
    REGEN = auto()
    POISON = auto()

class StatusesFive(IntFlag):
    DEATH_SENTENCE = auto()
    REFLECT = auto()
    DISABLE = auto()
    IMMOBILIZE = auto()
    SLEEP = auto()
    CHARM = auto()
    INNOCENT = auto()
    FAITH = auto()

class Elements(IntFlag):
    DARK = auto()
    HOLY = auto()
    WATER = auto()
    EARTH = auto()
    WIND = auto()
    ICE = auto()
    LIGHTNING = auto()
    FIRE = auto()
    ALL = DARK | HOLY | WATER | EARTH | WIND | ICE | LIGHTNING | FIRE
