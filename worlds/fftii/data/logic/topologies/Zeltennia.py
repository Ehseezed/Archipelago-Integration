from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation, SidequestLocation, MoveFindItemLocation, \
    SidequestMoveFindItemLocation

from ..regions.Zeltennia import *
from ..regions.Fovoham import Grog
from ..regions.Limberry import Bed, Poeskas

BerveniaCity.connections = [
    Connection(Doguola, [HasLesaliaPass]),
    Connection(Bed, [HasLimberryPass]),
    Connection(Finath)
]

BerveniaCity.locations = [
    FFTLocation(LocationNames.BERVENIA_CITY_STORY, battle_level=12),
    MoveFindItemLocation(LocationNames.BERVENIA_CITY_MFI_1, battle_level=12),
    MoveFindItemLocation(LocationNames.BERVENIA_CITY_MFI_2, battle_level=12),
    MoveFindItemLocation(LocationNames.BERVENIA_CITY_MFI_3, battle_level=12),
    MoveFindItemLocation(LocationNames.BERVENIA_CITY_MFI_4, battle_level=12)
]

Finath.connections = [
    Connection(BerveniaCity),
    Connection(Zeltennia)
]

Finath.locations = [
    FFTLocation(LocationNames.FINATH_STORY, battle_level=12),
    RareBattleLocation(LocationNames.FINATH_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.FINATH_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.FINATH_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.FINATH_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.FINATH_MFI_4, battle_level=0)
]

Zeltennia.connections = [
    Connection(Finath),
    Connection(Zarghidas),
    Connection(Nelveska)
]

Zeltennia.locations = [
    FFTLocation(LocationNames.ZELTENNIA_STORY, battle_level=12),
    MoveFindItemLocation(LocationNames.ZELTENNIA_MFI_1, battle_level=12),
    MoveFindItemLocation(LocationNames.ZELTENNIA_MFI_2, battle_level=12),
    MoveFindItemLocation(LocationNames.ZELTENNIA_MFI_3, battle_level=12),
    MoveFindItemLocation(LocationNames.ZELTENNIA_MFI_4, battle_level=12)
]

Zarghidas.connections = [
    Connection(Zeltennia),
    Connection(Germinas)
]

Zarghidas.locations = [
    SidequestLocation(LocationNames.ZARGHIDAS_SIDEQUEST, battle_level=14),
    SidequestLocation(LocationNames.CLOUD_RECRUIT, battle_level=14),
    MoveFindItemLocation(LocationNames.ZARGHIDAS_MFI_1, battle_level=14),
    MoveFindItemLocation(LocationNames.ZARGHIDAS_MFI_2, battle_level=14),
    MoveFindItemLocation(LocationNames.ZARGHIDAS_MFI_3, battle_level=14),
    MoveFindItemLocation(LocationNames.ZARGHIDAS_MFI_4, battle_level=14)
]

Germinas.connections = [
    Connection(Zarghidas),
    Connection(Poeskas, [HasLimberryPass])
]

Germinas.locations = [
    FFTLocation(LocationNames.GERMINAS_STORY, battle_level=13),
    RareBattleLocation(LocationNames.GERMINAS_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.GERMINAS_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.GERMINAS_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.GERMINAS_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.GERMINAS_MFI_4, battle_level=0)
]

Nelveska.connections = [
    Connection(Zeltennia)
]

Nelveska.locations = [
    SidequestLocation(LocationNames.NELVESKA_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.NELVESKA_STONE, battle_level=12),
    SidequestLocation(LocationNames.REIS_HUMAN_RECRUIT, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.NELVESKA_MFI_1, [CanAccessNelveskaPillar], battle_level=12), # Pillar check
    SidequestMoveFindItemLocation(LocationNames.NELVESKA_MFI_2, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.NELVESKA_MFI_3, battle_level=12),
    SidequestMoveFindItemLocation(LocationNames.NELVESKA_MFI_4, [CanAccessNelveskaPillar], battle_level=12) # Pillar Check
]

Doguola.connections = [
    Connection(Grog, [HasFovohamPass]),
    Connection(BerveniaCity)
]

Doguola.locations = [
    FFTLocation(LocationNames.DOGUOLA_STORY, battle_level=12),
    RareBattleLocation(LocationNames.DOGUOLA_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.DOGUOLA_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.DOGUOLA_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.DOGUOLA_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.DOGUOLA_MFI_4, battle_level=0)
]