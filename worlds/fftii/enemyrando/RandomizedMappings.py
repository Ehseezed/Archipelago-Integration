from .FactoryKey import FactoryKey
from .RandomizedUnits import *

generic_job_table: dict[Job, list[FactoryKey]] = {
    Job.SQUIRE: [FactoryKey.SQUIRE, FactoryKey.FEMALE_SQUIRE],
    Job.CHEMIST: [FactoryKey.CHEMIST, FactoryKey.FEMALE_CHEMIST],
    Job.KNIGHT: [FactoryKey.KNIGHT, FactoryKey.FEMALE_KNIGHT],
    Job.ARCHER: [FactoryKey.ARCHER, FactoryKey.FEMALE_ARCHER],
    Job.MONK: [FactoryKey.MONK, FactoryKey.FEMALE_MONK],
    Job.PRIEST: [FactoryKey.PRIEST, FactoryKey.FEMALE_PRIEST],
    Job.WIZARD: [FactoryKey.WIZARD, FactoryKey.FEMALE_WIZARD],
    Job.TIMEMAGE: [FactoryKey.TIMEMAGE, FactoryKey.FEMALE_TIMEMAGE],
    Job.SUMMONER: [FactoryKey.SUMMONER, FactoryKey.FEMALE_SUMMONER],
    Job.THIEF: [FactoryKey.THIEF, FactoryKey.FEMALE_THIEF],
    Job.MEDIATOR: [FactoryKey.MEDIATOR, FactoryKey.FEMALE_MEDIATOR],
    Job.ORACLE: [FactoryKey.ORACLE, FactoryKey.FEMALE_ORACLE],
    Job.GEOMANCER: [FactoryKey.GEOMANCER, FactoryKey.FEMALE_GEOMANCER],
    Job.LANCER: [FactoryKey.LANCER, FactoryKey.FEMALE_LANCER],
    Job.SAMURAI: [FactoryKey.SAMURAI, FactoryKey.FEMALE_SAMURAI],
    Job.NINJA: [FactoryKey.NINJA, FactoryKey.FEMALE_NINJA],
    Job.CALCULATOR: [FactoryKey.CALCULATOR, FactoryKey.FEMALE_CALCULATOR],
    Job.BARD: [FactoryKey.BARD],
    Job.DANCER: [FactoryKey.DANCER],
    Job.MIME: [FactoryKey.MIME, FactoryKey.FEMALE_MIME]
}

generic_monster_table: dict[Job, list[FactoryKey]] = {
    Job.YELLOW_CHOCOBO: [FactoryKey.YELLOW_CHOCOBO],
    Job.GOBLIN: [FactoryKey.GOBLIN],
    Job.BOMB: [FactoryKey.BOMB],
    Job.RED_PANTHER: [FactoryKey.RED_PANTHER],
    Job.PISCO_DEMON: [FactoryKey.PISCO_DEMON],
    Job.SKELETON: [FactoryKey.SKELETON],
    Job.GHOUL: [FactoryKey.GHOUL],
    Job.FLOTIBALL: [FactoryKey.FLOTIBALL],
    Job.JURAVIS: [FactoryKey.JURAVIS],
    Job.URIBO: [FactoryKey.URIBO],
    Job.WOODMAN: [FactoryKey.WOODMAN],
    Job.BULL_DEMON: [FactoryKey.BULL_DEMON],
    Job.MORBOL: [FactoryKey.MORBOL],
    Job.BEHEMOTH: [FactoryKey.BEHEMOTH],
    Job.DRAGON: [FactoryKey.DRAGON],
    Job.HYUDRA: [FactoryKey.HYUDRA]
}

special_job_table: dict[Job, list[FactoryKey]] = {
    #Job.RAMZA_SQUIRE_CHAPTER_1: [Job.RAMZA_SQUIRE_CHAPTER_1],
    #Job.RAMZA_SQUIRE_CHAPTER_23: [Job.RAMZA_SQUIRE_CHAPTER_23],
    #Job.RAMZA_SQUIRE_CHAPTER_4: [Job.RAMZA_SQUIRE_CHAPTER_4],
    Job.SQUIRE_DELITA: [FactoryKey.SQUIRE_DELITA],
    Job.SQUIRE_ALGUS: [FactoryKey.SQUIRE_ALGUS],
    Job.HOLY_KNIGHT_DELITA: [FactoryKey.HOLY_KNIGHT_DELITA],
    Job.ARC_KNIGHT_DELITA: [FactoryKey.ARC_KNIGHT_DELITA],
    Job.HOLY_KNIGHT_AGRIAS: [FactoryKey.HOLY_KNIGHT_AGRIAS],
    Job.ARC_KNIGHT_ZALBAG: [FactoryKey.ARC_KNIGHT_ZALBAG],
    Job.LUNE_KNIGHT: [FactoryKey.LUNE_KNIGHT],
    Job.PRINCESS: [FactoryKey.PRINCESS],
    Job.HOLY_SWORDSMAN: [FactoryKey.HOLY_SWORDSMAN],
    Job.DRAGONER: [FactoryKey.DRAGONER],
    Job.HOLY_PRIEST: [FactoryKey.HOLY_PRIEST],
    Job.DARK_KNIGHT_ENEMY: [FactoryKey.DARK_KNIGHT_ENEMY],
    Job.ASTROLOGIST: [FactoryKey.ASTROLOGIST],
    Job.ENGINEER_MUSTADIO: [FactoryKey.ENGINEER_MUSTADIO, FactoryKey.ENGINEER_BALK],
    Job.HELL_KNIGHT: [FactoryKey.HELL_KNIGHT],
    Job.ARC_KNIGHT_ELMDOR: [FactoryKey.ARC_KNIGHT_ELMDOR],
    Job.TEMPLE_KNIGHT: [FactoryKey.TEMPLE_KNIGHT],
    Job.WHITE_KNIGHT_C1: [FactoryKey.WHITE_KNIGHT_C1, FactoryKey.WHITE_KNIGHT_C3],
    Job.DIVINE_KNIGHT_VORMAV: [FactoryKey.DIVINE_KNIGHT_VORMAV, FactoryKey.DIVINE_KNIGHT_ROFEL, FactoryKey.DIVINE_KNIGHT_MELIADOUL],
    Job.KNIGHT_BLADE: [FactoryKey.KNIGHT_BLADE],
    Job.SORCERER: [FactoryKey.SORCERER],
    Job.HEAVEN_KNIGHT: [FactoryKey.HEAVEN_KNIGHT],
    Job.ASSASSIN_CELIA: [FactoryKey.ASSASSIN_CELIA, FactoryKey.ASSASSIN_LEDE],
    Job.CLERIC: [FactoryKey.CLERIC],
    Job.SOLDIER: [FactoryKey.SOLDIER],
    Job.KNIGHT_UNDEAD: [
        FactoryKey.KNIGHT_UNDEAD, FactoryKey.ARCHER_UNDEAD, FactoryKey.ORACLE_UNDEAD, FactoryKey.WIZARD_UNDEAD,
        FactoryKey.TIME_MAGE_UNDEAD, FactoryKey.SUMMONER_UNDEAD
    ]
}

special_monster_table: dict[Job, list[FactoryKey]] = {
    Job.HOLY_DRAGON: [FactoryKey.HOLY_DRAGON],
    Job.BYBLOS: [FactoryKey.BYBLOS],
    Job.STEEL_GIANT: [FactoryKey.STEEL_GIANT],
    Job.APANDA: [FactoryKey.APANDA],
    Job.ARCHAIC_DEMON: [FactoryKey.ARCHAIC_DEMON],
}

lucavi_table: dict[Job, list[FactoryKey]] = {
    Job.QUEKLAIN: [FactoryKey.QUEKLAIN],
    Job.VELIUS: [FactoryKey.VELIUS],
    Job.ZALERA: [FactoryKey.ZALERA],
    Job.ADRAMELK: [FactoryKey.ADRAMELK],
    Job.ELIDIBS: [FactoryKey.ELIDIBS],
    Job.HASHMALUM: [FactoryKey.HASHMALUM]
}

altima_table: dict[Job, list[FactoryKey]] = {
    Job.ALTIMA_1: [FactoryKey.ALTIMA_1],
    Job.ALTIMA_2: [FactoryKey.ALTIMA_2],
}

factory_mappings: dict[FactoryKey, dict[type[RandomizedUnit], int]] = {
    FactoryKey.RAMZA_SQUIRE_CHAPTER_1: {RamzaC1Squire: 1},
    FactoryKey.RAMZA_SQUIRE_CHAPTER_23: {RamzaC23Squire: 1},
    FactoryKey.RAMZA_SQUIRE_CHAPTER_4: {RamzaC4Squire: 9, RamzaC4SquireFullSkillset: 1},
    FactoryKey.SQUIRE_DELITA: {DelitaSquire: 1, DelitaSquireHard: 9},
    FactoryKey.HOLY_KNIGHT_DELITA: {DelitaHolyKnight: 1, DelitaHolyKnightHard: 9},
    FactoryKey.ARC_KNIGHT_DELITA: {DelitaArcKnight: 1, DelitaArcKnightHard: 9},
    FactoryKey.SQUIRE_ALGUS: {Algus: 9, AlgusWithCrossbow: 1, AlgusHard: 90, AlgusWithCrossbowHard: 10},
    FactoryKey.ARC_KNIGHT_ZALBAG: {ZalbagArcKnight: 1, ZalbagArcKnightHard: 9},
    FactoryKey.LUNE_KNIGHT: {LuneKnight: 1, LuneKnightHard: 9},
    FactoryKey.PRINCESS: {Princess: 1, PrincessHard: 9},
    FactoryKey.HOLY_SWORDSMAN: {HolySwordsman: 1, HolySwordsmanHard: 9, HolySwordsmanWithExcalibur: 1},
    FactoryKey.DRAGONER: {Dragoner: 1, DragonerHard: 9},
    FactoryKey.HOLY_PRIEST: {HolyPriest: 1, HolyPriestHard: 9},
    FactoryKey.DARK_KNIGHT_ENEMY: {DarkKnight: 1, DarkKnightHard: 9},
    FactoryKey.ASTROLOGIST: {Astrologist: 1, AstrologistHard: 9},
    FactoryKey.ENGINEER_MUSTADIO: {EngineerMustadio: 1, EngineerMustadioHard: 9},
    FactoryKey.DARK_KNIGHT_GUEST: {DarkKnight: 1, DarkKnightHard: 9},
    FactoryKey.HEAVEN_KNIGHT_GUEST: {HeavenKnight: 1, HeavenKnightHard: 9},
    FactoryKey.HELL_KNIGHT: {HellKnight: 1, HellKnightHard: 9},
    FactoryKey.ARC_KNIGHT_ELMDOR: {ArcKnightElmdor: 1, ArcKnightElmdorHard: 9, ArcKnightElmdorWithKit: 1},
    FactoryKey.HOLY_KNIGHT_AGRIAS: {HolyKnightAgrias: 1, HolyKnightAgriasHard: 9},
    FactoryKey.TEMPLE_KNIGHT: {TempleKnight: 1, TempleKnightHard: 9},
    FactoryKey.WHITE_KNIGHT_C1: {
        WhiteKnightChapter1: 9, WhiteKnightChapter1WithCounter: 1,
        WhiteKnightChapter1Hard: 90, WhiteKnightChapter1WithCounterHard: 10
    },
    FactoryKey.ENGINEER_GUEST: {EngineerMustadio: 1, EngineerMustadioHard: 9},
    FactoryKey.DIVINE_KNIGHT_VORMAV: {DivineKnightVormav: 1, DivineKnightVormavHard: 9},
    FactoryKey.DIVINE_KNIGHT_ROFEL: {DivineKnightRofel: 1, DivineKnightRofelHard: 9},
    FactoryKey.KNIGHT_BLADE: {
        KnightBlade: 1, KnightBladeWithKit: 1, KnightBladeHard: 9
    },
    FactoryKey.SORCERER: {Sorcerer: 1, SorcererHard: 9},
    FactoryKey.WHITE_KNIGHT_C3: {
        WhiteKnight: 9, WhiteKnightWithCounter: 1,
        WhiteKnightHard: 90, WhiteKnightWithCounterHard: 10
    },
    FactoryKey.HEAVEN_KNIGHT: {HeavenKnight: 1, HeavenKnightHard: 9},
    FactoryKey.DIVINE_KNIGHT_MELIADOUL: {DivineKnightMeliadoul: 1, DivineKnightMeliadoulHard: 9},
    FactoryKey.ENGINEER_BALK: {EngineerBalk: 1, EngineerBalkHard: 9},
    FactoryKey.ASSASSIN_CELIA: {AssassinCelia: 1},
    FactoryKey.ASSASSIN_LEDE: {AssassinLede: 1},
    FactoryKey.DIVINE_KNIGHT_MELIADOUL_ENEMY: {DivineKnightMeliadoul: 1, DivineKnightMeliadoulHard: 9},
    FactoryKey.CLERIC: {
        Cleric: 9, ClericWithUltima: 1,
        ClericHard: 90, ClericWithUltimaHard: 10
    },
    FactoryKey.SOLDIER: {Soldier: 1, SoldierHard: 9},
    FactoryKey.ARC_KNIGHT_ZOMBIE: {ArcKnightZombie: 9, ArcKnightZombieWithKit: 1},
    FactoryKey.HOLY_KNIGHT_AGRIAS_GUEST: {HolyKnightAgrias: 1},
    FactoryKey.KNIGHT_UNDEAD: {UndeadKnight: 1},
    FactoryKey.ARCHER_UNDEAD: {UndeadArcher: 1},
    FactoryKey.ALTIMA_1: {Altima1: 1},
    FactoryKey.WIZARD_UNDEAD: {UndeadWizard: 1},
    FactoryKey.TIME_MAGE_UNDEAD: {UndeadTimeMage: 1},
    FactoryKey.ORACLE_UNDEAD: {UndeadOracle: 1},
    FactoryKey.SUMMONER_UNDEAD: {UndeadSummoner: 1},
    FactoryKey.ALTIMA_2: {Altima2: 1},
    FactoryKey.SQUIRE: {
        MaleSquire: 1,
        MaleSquireEasy: 2,
        MaleSquireModerate1: 3, MaleSquireModerate2: 3,
        MaleSquireAdvanced1: 4, MaleSquireAdvanced2: 4,
        MaleSquireExpert1: 5, MaleSquireExpert2: 5, MaleSquireExpert3: 5,
        MaleSquireRare: 1
    },
    FactoryKey.FEMALE_SQUIRE: {
        FemaleSquire: 1,
        FemaleSquireEasy: 2,
        FemaleSquireModerate1: 3, FemaleSquireModerate2: 3,
        FemaleSquireAdvanced1: 4, FemaleSquireAdvanced2: 4,
        FemaleSquireExpert1: 5, FemaleSquireExpert2: 5, FemaleSquireExpert3: 5, FemaleSquireExpert4: 5,
        FemaleSquireRare: 1
    },
    FactoryKey.CHEMIST: {
        MaleChemist: 1,
        MaleChemistEasy: 2,
        MaleChemistModerate1: 3, MaleChemistModerate2: 3,
        MaleChemistAdvanced1: 4, MaleChemistAdvanced2: 4,
        MaleChemistExpert1: 5, MaleChemistExpert2: 5, MaleChemistExpert3: 5,
        MaleChemistRare: 1
    },
    FactoryKey.FEMALE_CHEMIST: {
        FemaleChemist: 1,
        FemaleChemistEasy: 2,
        FemaleChemistModerate1: 3, FemaleChemistModerate2: 3,
        FemaleChemistAdvanced1: 4, FemaleChemistAdvanced2: 4,
        FemaleChemistExpert1: 5, FemaleChemistExpert2: 5,
        FemaleChemistRare: 1
    },
    FactoryKey.KNIGHT: {
        MaleKnight: 1,
        MaleKnightEasy: 2,
        MaleKnightModerate: 3,
        MaleKnightAdvanced: 4,
        MaleKnightExpert1: 5, MaleKnightExpert2: 5, MaleKnightExpert3: 5,
        MaleKnightRare: 1
    },
    FactoryKey.FEMALE_KNIGHT: {
        FemaleKnight: 1,
        FemaleKnightEasy: 2,
        FemaleKnightModerate: 3,
        FemaleKnightAdvanced: 4,
        FemaleKnightExpert1: 5, FemaleKnightExpert2: 5, FemaleKnightExpert3: 5, FemaleKnightExpert4: 5,
        FemaleKnightRare: 1
    },
    FactoryKey.ARCHER: {
        MaleArcher: 1,
        MaleArcherEasy: 2,
        MaleArcherModerate: 3,
        MaleArcherAdvanced: 4,
        MaleArcherExpert1: 5, MaleArcherExpert2: 5, MaleArcherExpert3: 5,
        MaleArcherRare: 1
    },
    FactoryKey.FEMALE_ARCHER: {
        FemaleArcher: 1,
        FemaleArcherEasy: 2,
        FemaleArcherModerate: 3,
        FemaleArcherAdvanced: 4,
        FemaleArcherExpert1: 5, FemaleArcherExpert2: 5, FemaleArcherExpert3: 5, FemaleArcherExpert4: 5,
        FemaleArcherRare: 1
    },
    FactoryKey.MONK: {
        MaleMonk: 1,
        MaleMonkEasy: 2,
        MaleMonkModerate: 3,
        MaleMonkAdvanced: 4,
        MaleMonkExpert1: 5, MaleMonkExpert2: 5, MaleMonkExpert3: 5,
        MaleMonkRare: 1
    },
    FactoryKey.FEMALE_MONK: {
        FemaleMonk: 1,
        FemaleMonkEasy: 2,
        FemaleMonkModerate: 3,
        FemaleMonkAdvanced: 4,
        FemaleMonkExpert1: 5, FemaleMonkExpert2: 5, FemaleMonkExpert3: 5, FemaleMonkExpert4: 5,
        FemaleMonkRare: 1
    },
    FactoryKey.PRIEST: {
        MalePriest: 1,
        MalePriestEasy: 2,
        MalePriestModerate: 3,
        MalePriestAdvanced1: 4, MalePriestAdvanced2: 4,
        MalePriestExpert1: 5, MalePriestExpert2: 5,
        MalePriestRare: 1
    },
    FactoryKey.FEMALE_PRIEST: {
        FemalePriest: 1,
        FemalePriestEasy: 2,
        FemalePriestModerate: 3,
        FemalePriestAdvanced: 4,
        FemalePriestExpert1: 5, FemalePriestExpert2: 5,
        FemalePriestRare: 1
    },
    FactoryKey.WIZARD: {
        MaleWizard: 1,
        MaleWizardEasy: 2,
        MaleWizardModerate: 3,
        MaleWizardAdvanced1: 4, MaleWizardAdvanced2: 4,
        MaleWizardExpert1: 5, MaleWizardExpert2: 5,
        MaleWizardRare: 1
    },
    FactoryKey.FEMALE_WIZARD: {
        FemaleWizard: 1,
        FemaleWizardEasy: 2,
        FemaleWizardModerate: 3,
        FemaleWizardAdvanced: 4,
        FemaleWizardExpert1: 5, FemaleWizardExpert2: 5,
        FemaleWizardRare: 1
    },
    FactoryKey.TIMEMAGE: {
        MaleTimeMage: 1,
        MaleTimeMageEasy: 2,
        MaleTimeMageModerate: 3,
        MaleTimeMageAdvanced1: 4, MaleTimeMageAdvanced2: 4,
        MaleTimeMageExpert1: 5, MaleTimeMageExpert2: 5,
        MaleTimeMageRare: 1
    },
    FactoryKey.FEMALE_TIMEMAGE: {
        FemaleTimeMage: 1,
        FemaleTimeMageEasy: 2,
        FemaleTimeMageModerate: 3,
        FemaleTimeMageAdvanced: 4,
        FemaleTimeMageExpert1: 5, FemaleTimeMageExpert2: 5,
        FemaleTimeMageRare: 1
    },
    FactoryKey.SUMMONER: {
        MaleSummoner: 1,
        MaleSummonerEasy: 2,
        MaleSummonerModerate: 3,
        MaleSummonerAdvanced1: 4, MaleSummonerAdvanced2: 4,
        MaleSummonerExpert: 5,
        MaleSummonerRare: 1
    },
    FactoryKey.FEMALE_SUMMONER: {
        FemaleSummoner: 1,
        FemaleSummonerEasy: 2,
        FemaleSummonerModerate: 3,
        FemaleSummonerAdvanced: 4,
        FemaleSummonerExpert: 5,
        FemaleSummonerRare: 1
    },
    FactoryKey.THIEF: {
        MaleThief: 1,
        MaleThiefEasy: 2,
        MaleThiefModerate: 3,
        MaleThiefAdvanced: 4,
        MaleThiefExpert1: 5, MaleThiefExpert2: 5, MaleThiefExpert3: 5,
        MaleThiefRare: 1
    },
    FactoryKey.FEMALE_THIEF: {
        FemaleThief: 1,
        FemaleThiefEasy: 2,
        FemaleThiefModerate: 3,
        FemaleThiefAdvanced: 4,
        FemaleThiefExpert1: 5, FemaleThiefExpert2: 5, FemaleThiefExpert3: 5, FemaleThiefExpert4: 5,
        FemaleThiefRare: 1
    },
    FactoryKey.MEDIATOR: {
        MaleMediator: 1,
        MaleMediatorEasy: 2,
        MaleMediatorModerate: 3,
        MaleMediatorAdvanced1: 4, MaleMediatorAdvanced2: 4,
        MaleMediatorExpert: 5,
        MaleMediatorRare: 1
    },
    FactoryKey.FEMALE_MEDIATOR: {
        FemaleMediator: 1,
        FemaleMediatorEasy: 2,
        FemaleMediatorModerate: 3,
        FemaleMediatorAdvanced: 4,
        FemaleMediatorExpert: 5,
        FemaleMediatorRare: 1
    },
    FactoryKey.ORACLE: {
        MaleOracle: 1,
        MaleOracleEasy: 2,
        MaleOracleModerate: 3,
        MaleOracleAdvanced1: 4, MaleOracleAdvanced2: 4,
        MaleOracleExpert1: 5, MaleOracleExpert2: 5,
        MaleOracleRare: 1
    },
    FactoryKey.FEMALE_ORACLE: {
        FemaleOracle: 1,
        FemaleOracleEasy: 2,
        FemaleOracleModerate: 3,
        FemaleOracleAdvanced: 4,
        FemaleOracleExpert1: 5, FemaleOracleExpert2: 5,
        FemaleOracleRare: 1
    },
    FactoryKey.GEOMANCER: {
        MaleGeomancer: 1,
        MaleGeomancerModerate: 2,
        MaleGeomancerAdvanced: 3,
        MaleGeomancerExpert1: 4, MaleGeomancerExpert2: 4, MaleGeomancerExpert3: 4,
        MaleGeomancerRare: 1
    },
    FactoryKey.FEMALE_GEOMANCER: {
        FemaleGeomancer: 1,
        FemaleGeomancerModerate: 2,
        FemaleGeomancerAdvanced1: 3, FemaleGeomancerAdvanced2: 3,
        FemaleGeomancerExpert1: 4, FemaleGeomancerExpert2: 4, FemaleGeomancerExpert3: 4,
        FemaleGeomancerRare: 1
    },
    FactoryKey.LANCER: {
        MaleLancer: 1,
        MaleLancerModerate: 2,
        MaleLancerAdvanced: 3,
        MaleLancerExpert1: 4, MaleLancerExpert2: 4, MaleLancerExpert3: 4,
        MaleLancerRare: 1
    },
    FactoryKey.FEMALE_LANCER: {
        FemaleLancer: 1,
        FemaleLancerModerate: 2,
        FemaleLancerAdvanced1: 3, FemaleLancerAdvanced2: 3,
        FemaleLancerExpert1: 4, FemaleLancerExpert2: 4, FemaleLancerExpert3: 4,
        FemaleLancerRare: 1
    },
    FactoryKey.SAMURAI: {
        MaleSamurai: 2,
        MaleSamuraiAdvanced: 4,
        MaleSamuraiExpert: 6,
        MaleSamuraiRare: 1
    },
    FactoryKey.FEMALE_SAMURAI: {
        FemaleSamurai: 2,
        FemaleSamuraiAdvanced1: 4, FemaleSamuraiAdvanced2: 4,
        FemaleSamuraiExpert: 6,
        FemaleSamuraiRare: 1
    },
    FactoryKey.NINJA: {
        MaleNinja: 2,
        MaleNinjaAdvanced: 4,
        MaleNinjaExpert: 6,
        MaleNinjaRare: 1
    },
    FactoryKey.FEMALE_NINJA: {
        FemaleNinja: 2,
        FemaleNinjaAdvanced1: 4, FemaleNinjaAdvanced2: 4,
        FemaleNinjaExpert: 6,
        FemaleNinjaRare: 1
    },
    FactoryKey.CALCULATOR: {
        MaleCalculator: 1,
        MaleCalculatorExpert: 2
    },
    FactoryKey.FEMALE_CALCULATOR: {
        FemaleCalculator: 1,
        FemaleCalculatorExpert: 2
    },
    FactoryKey.BARD: {MaleBard: 1},
    FactoryKey.DANCER: {FemaleDancer: 1},
    FactoryKey.MIME: {MaleMime: 1},
    FactoryKey.FEMALE_MIME: {FemaleMime: 1},
    FactoryKey.YELLOW_CHOCOBO: {YellowChocobo: 1, BlackChocobo: 1, RedChocobo: 1},
    FactoryKey.BLACK_CHOCOBO: {YellowChocobo: 1, BlackChocobo: 1, RedChocobo: 1},
    FactoryKey.RED_CHOCOBO: {YellowChocobo: 1, BlackChocobo: 1, RedChocobo: 1},
    FactoryKey.GOBLIN: {Goblin: 1, BlackGoblin: 1, Gobbledeguck: 1},
    FactoryKey.BLACK_GOBLIN: {Goblin: 1, BlackGoblin: 1, Gobbledeguck: 1},
    FactoryKey.GOBBLEDEGUCK: {Goblin: 1, BlackGoblin: 1, Gobbledeguck: 1},
    FactoryKey.BOMB: {Bomb: 1, Grenade: 1, Explosive: 1},
    FactoryKey.GRENADE: {Bomb: 1, Grenade: 1, Explosive: 1},
    FactoryKey.EXPLOSIVE: {Bomb: 1, Grenade: 1, Explosive: 1},
    FactoryKey.RED_PANTHER: {RedPanther: 1, Cuar: 1, Vampire: 1},
    FactoryKey.CUAR: {RedPanther: 1, Cuar: 1, Vampire: 1},
    FactoryKey.VAMPIRE: {RedPanther: 1, Cuar: 1, Vampire: 1},
    FactoryKey.PISCO_DEMON: {PiscoDemon: 1, Squidlarkin: 1, Mindflare: 1},
    FactoryKey.SQUIDLARKIN: {PiscoDemon: 1, Squidlarkin: 1, Mindflare: 1},
    FactoryKey.MINDFLARE: {PiscoDemon: 1, Squidlarkin: 1, Mindflare: 1},
    FactoryKey.SKELETON: {Skeleton: 1, BoneSnatch: 1, LivingBone: 1},
    FactoryKey.BONE_SNATCH: {Skeleton: 1, BoneSnatch: 1, LivingBone: 1},
    FactoryKey.LIVING_BONE: {Skeleton: 1, BoneSnatch: 1, LivingBone: 1},
    FactoryKey.GHOUL: {Ghoul: 1, Gust: 1, Revnant: 1},
    FactoryKey.GUST: {Ghoul: 1, Gust: 1, Revnant: 1},
    FactoryKey.REVNANT: {Ghoul: 1, Gust: 1, Revnant: 1},
    FactoryKey.FLOTIBALL: {Flotiball: 1, Ahriman: 1, Plague: 1},
    FactoryKey.AHRIMAN: {Flotiball: 1, Ahriman: 1, Plague: 1},
    FactoryKey.PLAGUE: {Flotiball: 1, Ahriman: 1, Plague: 1},
    FactoryKey.JURAVIS: {Juravis: 1, SteelHawk: 1, Cocatoris: 1},
    FactoryKey.STEEL_HAWK: {Juravis: 1, SteelHawk: 1, Cocatoris: 1},
    FactoryKey.COCATORIS: {Juravis: 1, SteelHawk: 1, Cocatoris: 1},
    FactoryKey.URIBO: {Uribo: 1, Porky: 1, Wildbow: 1},
    FactoryKey.PORKY: {Uribo: 1, Porky: 1, Wildbow: 1},
    FactoryKey.WILDBOW: {Uribo: 1, Porky: 1, Wildbow: 1},
    FactoryKey.WOODMAN: {Woodman: 1, Trent: 1, Taiju: 1},
    FactoryKey.TRENT: {Woodman: 1, Trent: 1, Taiju: 1},
    FactoryKey.TAIJU: {Woodman: 1, Trent: 1, Taiju: 1},
    FactoryKey.BULL_DEMON: {BullDemon: 1, Minitaurus: 1, Sacred: 1},
    FactoryKey.MINITAURUS: {BullDemon: 1, Minitaurus: 1, Sacred: 1},
    FactoryKey.SACRED: {BullDemon: 1, Minitaurus: 1, Sacred: 1},
    FactoryKey.MORBOL: {Morbol: 1, Ochu: 1, GreatMorbol: 1},
    FactoryKey.OCHU: {Morbol: 1, Ochu: 1, GreatMorbol: 1},
    FactoryKey.GREAT_MORBOL: {Morbol: 1, Ochu: 1, GreatMorbol: 1},
    FactoryKey.BEHEMOTH: {Behemoth: 1, KingBehemoth: 1, DarkBehemoth: 1},
    FactoryKey.KING_BEHEMOTH: {Behemoth: 1, KingBehemoth: 1, DarkBehemoth: 1},
    FactoryKey.DARK_BEHEMOTH: {Behemoth: 1, KingBehemoth: 1, DarkBehemoth: 1},
    FactoryKey.DRAGON: {Dragon: 1, BlueDragon: 1, RedDragon: 1},
    FactoryKey.BLUE_DRAGON: {Dragon: 1, BlueDragon: 1, RedDragon: 1},
    FactoryKey.RED_DRAGON: {Dragon: 1, BlueDragon: 1, RedDragon: 1},
    FactoryKey.HYUDRA: {Hyudra: 1, Hydra: 1, Tiamat: 1},
    FactoryKey.HYDRA: {Hyudra: 1, Hydra: 1, Tiamat: 1},
    FactoryKey.TIAMAT: {Hyudra: 1, Hydra: 1, Tiamat: 1},
    FactoryKey.HOLY_DRAGON: {HolyDragon: 1},
    FactoryKey.BYBLOS: {Byblos: 1},
    FactoryKey.STEEL_GIANT: {SteelGiant: 1},
    FactoryKey.APANDA: {Apanda: 1},
    FactoryKey.ARCHAIC_DEMON: {ArchaicDemon: 1, UltimaDemon: 1},
    FactoryKey.ULTIMA_DEMON: {ArchaicDemon: 1, UltimaDemon: 1},
    FactoryKey.VELIUS: {VeliusWithKit: 1},
    FactoryKey.ZALERA: {ZaleraWithKit: 1},
    FactoryKey.HASHMALUM: {HashmalumWithKit: 1},
    FactoryKey.QUEKLAIN: {QueklainWithKit: 1},
    FactoryKey.ADRAMELK: {AdramelkWithKit: 1},
    FactoryKey.ELIDIBS: {Elidibs: 1}
}

base_shuffle_list: list[type[RandomizedUnit]] = [
    Wiegraf1Boss, AlgusBoss, Gafgarion1Boss, Gafgarion2Boss, Gafgarion3Boss, Zalmo1Boss, IzludeBoss, Wiegraf2Boss,
    Malak1Boss, Malak2Boss, Wiegraf3Boss, Elmdor1Boss, Celia1Boss, Lede1Boss, MeliadoulBoss, Zalmo2Boss, Balk1Boss,
    Celia2Boss, Lede2Boss, Celia3Boss, Lede3Boss, Elmdor2Boss, DycedargBoss, VormavBoss, Rofel1Boss, Kletian1Boss,
    ZalbagBoss, Rofel2Boss, Kletian2Boss, Balk2Boss
]

zodiac_story_shuffle_list: list[type[RandomizedUnit]] = [
    QueklainBoss, VeliusBoss, ZaleraBoss, AdramelkBoss, HashmalumBoss
]

altima_story_shuffle_list: list[type[RandomizedUnit]] = [
    Altima1Boss, Altima2Boss
]

sidequest_boss_shuffle_list: list[type[RandomizedUnit]] = [
    Worker7Boss
]

sidequest_zodiac_shuffle_list: list[type[RandomizedUnit]] = [
    ElidibsBoss
]

all_boss_shuffle_lists: list[type[RandomizedUnit]] = [
    *base_shuffle_list, *zodiac_story_shuffle_list, *altima_story_shuffle_list,
    *sidequest_boss_shuffle_list, *sidequest_zodiac_shuffle_list
]

all_boss_shuffle_lookup: dict[Job, type[RandomizedUnit]] = {
    unit.job: unit for unit in all_boss_shuffle_lists
}