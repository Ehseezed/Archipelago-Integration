from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, SidequestLocation, VanillaFinalFightsLocation, \
    AltimaOnlyFinalFightLocation, MoveFindItemLocation, AltimaOnlyFinalFightMoveFindItemLocation, \
    SidequestMoveFindItemLocation, VanillaFinalFightMoveFindItemLocation

from ..regions.Murond import *
from ..regions.Gallione import Gariland, Dorter
from ..regions.Lionel import Zigolis, Warjilis

Murond.connections = [
    Connection(Gariland, [HasGallionePass]),
    Connection(Goug)
]

Murond.locations = [
    FFTLocation(LocationNames.MUROND_TEMPLE_1_STORY, battle_level=14),
    FFTLocation(LocationNames.MUROND_TEMPLE_2_STORY, battle_level=14),
    FFTLocation(LocationNames.MUROND_TEMPLE_3_STORY, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_1_MFI_1, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_1_MFI_2, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_1_MFI_3, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_1_MFI_4, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_2_MFI_1, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_2_MFI_2, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_2_MFI_3, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_2_MFI_4, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_3_MFI_1, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_3_MFI_2, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_3_MFI_3, battle_level=14),
    MoveFindItemLocation(LocationNames.MUROND_TEMPLE_3_MFI_4, battle_level=14)
]

Goug.connections = [
    Connection(Murond),
    Connection(Zigolis, [HasLionelPass])
]

Goug.locations = [
    FFTLocation(LocationNames.GOUG_STORY, battle_level=6),
    FFTLocation(LocationNames.GOUG_STONE, battle_level=6),
    FFTLocation(LocationNames.MUSTADIO_RECRUIT, battle_level=6),
    MoveFindItemLocation(LocationNames.GOUG_MFI_1, battle_level=6),
    MoveFindItemLocation(LocationNames.GOUG_MFI_2, battle_level=6),
    MoveFindItemLocation(LocationNames.GOUG_MFI_3, battle_level=6),
    MoveFindItemLocation(LocationNames.GOUG_MFI_4, battle_level=6)
]

Orbonne.connections = [
    Connection(Dorter, [HasGallionePass])
]

Orbonne.locations = [
    FFTLocation(LocationNames.UBS_1_STORY, battle_level=9),
    FFTLocation(LocationNames.UBS_2_STORY, battle_level=9),
    FFTLocation(LocationNames.UBS_3_STORY, battle_level=9),
    FFTLocation(LocationNames.ORBONNE_SHOP, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_1_MFI_1, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_1_MFI_2, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_1_MFI_3, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_1_MFI_4, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_2_MFI_1, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_2_MFI_2, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_2_MFI_3, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_2_MFI_4, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_3_MFI_1, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_3_MFI_2, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_3_MFI_3, battle_level=9),
    MoveFindItemLocation(LocationNames.UBS_3_MFI_4, battle_level=9),
    AltimaOnlyFinalFightLocation(LocationNames.UBS_4_STORY, battle_level=14),
    AltimaOnlyFinalFightLocation(LocationNames.UBS_5_STORY, battle_level=14),
    AltimaOnlyFinalFightLocation(LocationNames.MUROND_DEATH_CITY_STORY, battle_level=14),
    AltimaOnlyFinalFightLocation(LocationNames.PRECINCTS_STORY, battle_level=14),
    AltimaOnlyFinalFightLocation(LocationNames.AIRSHIPS_1_STORY, battle_level=14),
    AltimaOnlyFinalFightLocation(LocationNames.AIRSHIPS_1_STONE, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_1, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_2, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_3, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_4, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_1, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_2, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_3, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_4, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_1, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_2, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_3, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_4, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_1, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_2, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_3, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_4, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_1, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_2, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_3, battle_level=14),
    AltimaOnlyFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_4, battle_level=14)
]

DeepDungeon.connections = [
    Connection(Warjilis,  [HasLionelPass]),
    Connection(MurondDeathCity, [HasZodiacStones])
]

DeepDungeon.locations = [
    SidequestLocation(LocationNames.NOGIAS_SIDEQUEST, battle_level=10),
    SidequestLocation(LocationNames.TERMINATE_SIDEQUEST, battle_level=10),
    SidequestLocation(LocationNames.DELTA_SIDEQUEST, battle_level=10),
    SidequestLocation(LocationNames.VALKYRIES_SIDEQUEST, battle_level=10),
    SidequestLocation(LocationNames.MLAPAN_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.TIGER_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.BRIDGE_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.VOYAGE_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.HORROR_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.END_SIDEQUEST, battle_level=14),
    SidequestLocation(LocationNames.END_STONE, battle_level=14),
    SidequestLocation(LocationNames.BYBLOS_RECRUIT, battle_level=14),
    SidequestMoveFindItemLocation(LocationNames.NOGIAS_MFI_1, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.NOGIAS_MFI_2, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.NOGIAS_MFI_3, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.NOGIAS_MFI_4, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.TERMINATE_MFI_1, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.TERMINATE_MFI_2, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.TERMINATE_MFI_3, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.TERMINATE_MFI_4, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.DELTA_MFI_1, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.DELTA_MFI_2, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.DELTA_MFI_3, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.DELTA_MFI_4, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.VALKYRIES_MFI_1, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.VALKYRIES_MFI_2, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.VALKYRIES_MFI_3, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.VALKYRIES_MFI_4, battle_level=10),
    SidequestMoveFindItemLocation(LocationNames.MLAPAN_MFI_1, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.MLAPAN_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.MLAPAN_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.MLAPAN_MFI_4, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.TIGER_MFI_1, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.TIGER_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.TIGER_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.TIGER_MFI_4, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.BRIDGE_MFI_1, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.BRIDGE_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.BRIDGE_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.BRIDGE_MFI_4, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.VOYAGE_MFI_1, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.VOYAGE_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.VOYAGE_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.VOYAGE_MFI_4, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.HORROR_MFI_1, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.HORROR_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.HORROR_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.HORROR_MFI_4, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.END_MFI_1, battle_level=14),
    SidequestMoveFindItemLocation(LocationNames.END_MFI_2, battle_level=14),
    SidequestMoveFindItemLocation(LocationNames.END_MFI_3, battle_level=14),
    SidequestMoveFindItemLocation(LocationNames.END_MFI_4, battle_level=14)
]

MurondDeathCity.connections = [
    Connection(DeepDungeon)
]

MurondDeathCity.locations = [
    VanillaFinalFightsLocation(LocationNames.UBS_4_STORY, battle_level=14),
    VanillaFinalFightsLocation(LocationNames.UBS_5_STORY, battle_level=14),
    VanillaFinalFightsLocation(LocationNames.MUROND_DEATH_CITY_STORY, battle_level=14),
    VanillaFinalFightsLocation(LocationNames.PRECINCTS_STORY, battle_level=14),
    VanillaFinalFightsLocation(LocationNames.AIRSHIPS_1_STORY, battle_level=14),
    VanillaFinalFightsLocation(LocationNames.AIRSHIPS_1_STONE, battle_level=14),
    FFTLocation(LocationNames.AIRSHIPS_2_STORY, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_1, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_2, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_3, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_4_MFI_4, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_1, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_2, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_3, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.UBS_5_MFI_4, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_1, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_2, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_3, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.MUROND_DEATH_CITY_MFI_4, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_1, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_2, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_3, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.PRECINCTS_MFI_4, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_1, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_2, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_3, battle_level=14),
    VanillaFinalFightMoveFindItemLocation(LocationNames.AIRSHIPS_MFI_4, battle_level=14)
]