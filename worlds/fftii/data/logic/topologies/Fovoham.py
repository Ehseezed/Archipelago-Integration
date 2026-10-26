from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation, MoveFindItemLocation

from ..regions.Fovoham import *
from ..regions.Gallione import Zeakden, Lenalia
from ..regions.Lesalia import Lesalia, BerveniaVolcano
from ..regions.Zeltennia import Doguola

Grog.connections = [
    Connection(Yardow),
    Connection(Lesalia, [HasLesaliaPass]),
    Connection(Doguola, [HasZeltenniaPass])
]

Grog.locations = [
    FFTLocation(LocationNames.GROG_STORY, battle_level=10),
    RareBattleLocation(LocationNames.GROG_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.GROG_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.GROG_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.GROG_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.GROG_MFI_4, battle_level=0)
]

Yardow.connections = [
    Connection(Grog),
    Connection(Yuguo)
]

Yardow.locations = [
    FFTLocation(LocationNames.YARDOW_STORY, battle_level=10),
    FFTLocation(LocationNames.YARDOW_SHOP, battle_level=10),
    MoveFindItemLocation(LocationNames.YARDOW_MFI_1, battle_level=10),
    MoveFindItemLocation(LocationNames.YARDOW_MFI_2, battle_level=10),
    MoveFindItemLocation(LocationNames.YARDOW_MFI_3, battle_level=10),
    MoveFindItemLocation(LocationNames.YARDOW_MFI_4, battle_level=10)
]

Yuguo.connections = [
    Connection(Yardow),
    Connection(Riovanes)
]

Yuguo.locations = [
    FFTLocation(LocationNames.YUGUO_STORY, battle_level=11),
    RareBattleLocation(LocationNames.YUGUO_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.YUGUO_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.YUGUO_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.YUGUO_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.YUGUO_MFI_4, battle_level=0)
]

Riovanes.connections = [
    Connection(Fovoham),
    Connection(Yuguo),
    Connection(BerveniaVolcano, [HasLesaliaPass]),
]

Riovanes.locations = [
    FFTLocation(LocationNames.RIOVANES_1_STORY, battle_level=11),
    FFTLocation(LocationNames.RIOVANES_2_STORY, battle_level=11),
    FFTLocation(LocationNames.RIOVANES_2_STONE, battle_level=11),
    FFTLocation(LocationNames.RIOVANES_3_STORY, battle_level=11),
    FFTLocation(LocationNames.RIOVANES_3_STONE, battle_level=11),
    FFTLocation(LocationNames.RIOVANES_SHOP, battle_level=11),
    FFTLocation(LocationNames.RAMZA_CHAPTER_4_UNLOCK, battle_level=11),
    FFTLocation(LocationNames.RAFA_RECRUIT, battle_level=11),
    FFTLocation(LocationNames.MALAK_RECRUIT, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_1_MFI_1, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_1_MFI_2, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_1_MFI_3, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_1_MFI_4, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_2_MFI_1, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_2_MFI_2, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_2_MFI_3, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_2_MFI_4, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_3_MFI_1, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_3_MFI_2, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_3_MFI_3, battle_level=11),
    MoveFindItemLocation(LocationNames.RIOVANES_3_MFI_4, battle_level=11)
]

Fovoham.connections = [
    Connection(Riovanes),
    Connection(Zeakden, [HasGallionePass]),
    Connection(Lenalia, [HasGallionePass])
]

Fovoham.locations = [
    FFTLocation(LocationNames.FOVOHAM_STORY, battle_level=2),
    RareBattleLocation(LocationNames.FOVOHAM_RARE, battle_level=8),
    MoveFindItemLocation(LocationNames.FOVOHAM_STORY_MFI_1, battle_level=2),
    MoveFindItemLocation(LocationNames.FOVOHAM_STORY_MFI_2, battle_level=2),
    MoveFindItemLocation(LocationNames.FOVOHAM_STORY_MFI_3, battle_level=2),
    MoveFindItemLocation(LocationNames.FOVOHAM_STORY_MFI_4, battle_level=2),
    MoveFindItemLocation(LocationNames.FOVOHAM_RANDOM_MFI_1, battle_level=0),
    MoveFindItemLocation(LocationNames.FOVOHAM_RANDOM_MFI_2, battle_level=0),
    MoveFindItemLocation(LocationNames.FOVOHAM_RANDOM_MFI_3, battle_level=0),
    MoveFindItemLocation(LocationNames.FOVOHAM_RANDOM_MFI_4, battle_level=0)
]