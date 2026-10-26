from ..data.logic.regions import *

class BattleRegionMapping:
    battle_ids: list[int]
    regions: list[type[FFTRegion]]
    name: str

    def __init__(self, battle_ids: list[int], regions: list[type[FFTRegion]], name: str):
        self.battle_ids = battle_ids
        self.regions = regions
        self.name = name

dolbodar_from_bethla = BattleRegionMapping(
    [0x05, 0x06, 0x07, 0x08],
    [Dolbodar, Bethla],
    "Dolbodar Swamp from Bethla Garrison"
)

dolbodar_from_limberry = BattleRegionMapping(
    [0x01, 0x02, 0x03, 0x04],
    [Dolbodar, Limberry],
    "Dolbodar Swamp from Limberry Castle"
)
dolbodar = BattleRegionMapping(
    [0x5D],
    [Dolbodar],
    "Dolbodar Swamp"
)
fovoham_from_riovanes = BattleRegionMapping(
    [0x15, 0x16, 0x17, 0x18],
    [Fovoham, Riovanes],
    "Fovoham Plains from Riovanes Castle"
)

fovoham_from_zeakden = BattleRegionMapping(
    [0x11, 0x12, 0x13, 0x14],
    [Fovoham, Zeakden],
    "Fovoham Plains from Fort Zeakden"
)

fovoham_from_lenalia = BattleRegionMapping(
    [0x0D, 0x0E, 0x0F, 0x10],
    [Fovoham, Lenalia],
    "Fovoham Plains from Lenalia Plateau"
)

fovoham = BattleRegionMapping(
    [0x82, 0x190],
    [Fovoham],
    "Fovoham Plains"
)

sweegy = BattleRegionMapping(
    [0x84, 0x180],
    [Sweegy],
    "Sweegy Woods"
)

sweegy_from_gariland = BattleRegionMapping(
    [0x1D, 0x1E, 0x1F, 0x20],
    [Sweegy, Gariland],
    "Sweegy Woods from Gariland Magic City"
)

sweegy_from_dorter = BattleRegionMapping(
    [0x19, 0x1A, 0x1B, 0x1C],
    [Sweegy, Dorter],
    "Sweegy Woods from Dorter Trade City"
)

bervenia_from_riovanes = BattleRegionMapping(
    [0x25, 0x26, 0x27, 0x28],
    [BerveniaVolcano, Riovanes],
    "Bervenia Volcano from Riovanes Castle"
)

bervenia_from_zeklaus = BattleRegionMapping(
    [0x29, 0x2A, 0x2B, 0x2C, 0x5F],
    [BerveniaVolcano, Zeklaus],
    "Bervenia Volcano from Zeklaus Desert"
)

bervenia = BattleRegionMapping(
    [0x5F],
    [BerveniaVolcano],
    "Bervenia Volcano"
)

zeklaus_from_dorter = BattleRegionMapping(
    [0x35, 0x36, 0x37, 0x38],
    [Zeklaus, Dorter],
    "Zeklaus Desert from Dorter Trade City"
)

zeklaus_from_bervenia = BattleRegionMapping(
    [0x31, 0x32, 0x33, 0x34],
    [Zeklaus, BerveniaVolcano],
    "Zeklaus Desert from Bervenia Volcano"
)

zeklaus_from_goland = BattleRegionMapping(
    [0x39, 0x3A, 0x3B, 0x3C],
    [Zeklaus, Goland],
    "Zeklaus Desert from Goland Coal City"
)

zeklaus = BattleRegionMapping(
    [0x9C, 0x182],
    [Zeklaus],
    "Zeklaus Desert"
)

lenalia_from_fovoham = BattleRegionMapping(
    [0x41, 0x42, 0x43, 0x44],
    [Lenalia, Fovoham],
    "Lenalia Plateau from Fovoham Plains"
)

lenalia_from_gariland = BattleRegionMapping(
    [0x3D, 0x3E, 0x3F, 0x40, 0x54],
    [Lenalia, Gariland],
    "Lenalia Plateau from Gariland Magic City"
)

lenalia = BattleRegionMapping(
    [0x54, 0x18F],
    [Lenalia],
    "Lenalia Plateau"
)

zigolis_from_goug = BattleRegionMapping(
    [0x4D, 0x4E, 0x4F, 0x50],
    [Zigolis, Goug],
    "Zigolis Swamp from Goug Machine City"
)

zigolis_from_lionel = BattleRegionMapping(
    [0x49, 0x4A, 0x4B, 0x4C],
    [Zigolis, Lionel],
    "Zigolis Swamp from Lionel Castle"
)

zigolis = BattleRegionMapping(
    [0x9A, 0x19A],
    [Zigolis],
    "Zigolis Swamp"
)

yuguo_from_yardow = BattleRegionMapping(
    [0x59, 0x5A, 0x5B, 0x5C],
    [Yuguo, Yardow],
    "Yuguo Woods from Yardow Fort City"
)

yuguo_from_riovanes = BattleRegionMapping(
    [0x55, 0x56, 0x57, 0x58],
    [Yuguo, Riovanes],
    "Yuguo Woods from Riovanes Castle"
)

yuguo = BattleRegionMapping(
    [0x6C, 0x1AE],
    [Yuguo],
    "Yuguo Woods"
)

araguay_from_dorter = BattleRegionMapping(
    [0x61, 0x62, 0x63, 0x64],
    [Araguay, Dorter],
    "Araguay Woods from Dorter Trade City"
)

araguay_from_zirekile = BattleRegionMapping(
    [0x65, 0x66, 0x67, 0x68],
    [Araguay, Zirekile],
    "Araguay Woods from Zirekile Falls"
)

araguay = BattleRegionMapping(
    [0x6B, 0x194],
    [Araguay],
    "Araguay Woods"
)

grog_from_lesalia = BattleRegionMapping(
    [0x71, 0x72, 0x73, 0x74],
    [Grog, Lesalia],
    "Grog Hill from Lesalia Imperial Capital"
)

grog_from_doguola = BattleRegionMapping(
    [0x75, 0x76, 0x77, 0x78],
    [Grog, Doguola],
    "Grog Hill from Doguola Pass"
)

grog_from_yardow = BattleRegionMapping(
    [0x6D, 0x6E, 0x6F, 0x70],
    [Grog, Yardow],
    "Grog Hill from Yardow Fort City"
)

grog = BattleRegionMapping(
    [0x5E, 0x1AA],
    [Grog],
    "Grog Hill"
)

bed_from_bervenia = BattleRegionMapping(
    [0x7D, 0x7E, 0x7F, 0x80],
    [Bed, BerveniaCity],
    "Bed Desert from Bervenia Free City"
)

bed_from_bethla = BattleRegionMapping(
    [0x79, 0x7A, 0x7B, 0x7C],
    [Bed, Bethla],
    "Bed Desert from Bethla Garrison"
)

bed = BattleRegionMapping(
    [0x81, 0x1BF],
    [Bed],
    "Bed Desert"
)

zirekile_from_zaland = BattleRegionMapping(
    [0x8D, 0x8E, 0x8F, 0x90],
    [Zirekile, Zaland],
    "Zirekile Falls from Zaland Fort City"
)

zirekile_from_bethla = BattleRegionMapping(
    [0x89, 0x8A, 0x8B, 0x8C],
    [Zirekile, Bethla],
    "Zirekile Falls from Bethla Garrison"
)

zirekile_from_araguay = BattleRegionMapping(
    [0x85, 0x86, 0x87, 0x88],
    [Zirekile, Araguay],
    "Zirekile Falls from Araguay Woods"
)

zirekile = BattleRegionMapping(
    [0x52, 0x195],
    [Zirekile],
    "Zirekile Falls"
)

bariaus_hill_from_zaland = BattleRegionMapping(
    [0x91, 0x92, 0x93, 0x94],
    [BariausHill, Zaland],
    "Bariaus Hill from Zaland Fort City"
)

bariaus_hill_from_lionel = BattleRegionMapping(
    [0x95, 0x96, 0x97, 0x98],
    [BariausHill, Lionel],
    "Bariaus Hill from Lionel Castle"
)

bariaus_hill = BattleRegionMapping(
    [0x53, 0x199],
    [BariausHill],
    "Bariaus Hill"
)

mandalia_from_gariland = BattleRegionMapping(
    [0x9D, 0x9E, 0x9F, 0xA0],
    [Mandalia, Gariland],
    "Mandalia Plains from Gariland Magic City"
)

mandalia_from_igros = BattleRegionMapping(
    [0xA5, 0xA6, 0xA7, 0xA8],
    [Mandalia, Igros],
    "Mandalia Plains from Igros Castle"
)

mandalia_from_thieves_fort = BattleRegionMapping(
    [0xA1, 0xA2, 0xA3, 0xA4],
    [Mandalia, ThievesFort],
    "Mandalia Plains from Thieves' Fort"
)

mandalia = BattleRegionMapping(
    [0x9B, 0x185],
    [Mandalia],
    "Mandalia Plains"
)

doguola_from_grog = BattleRegionMapping(
    [0xAD, 0xAE, 0xAF, 0xB0],
    [Doguola, Grog],
    "Doguola Pass from Grog Hill"
)

doguola_from_bervenia = BattleRegionMapping(
    [0xA9, 0xAA, 0xAB, 0xAC, 0x83],
    [Doguola, BerveniaCity],
    "Doguola Pass from Bervenia Free City"
)

doguola = BattleRegionMapping(
    [0x83, 0x1BA],
    [Doguola],
    "Doguola Pass"
)

bariaus_valley_from_lionel = BattleRegionMapping(
    [0xB5, 0xB6, 0xB7, 0xB8],
    [BariausValley, Lionel],
    "Bariaus Valley from Lionel Castle"
)

bariaus_valley_from_warjilis = BattleRegionMapping(
    [0xB9, 0xBA, 0xBB, 0xBC],
    [BariausValley, Warjilis],
    "Bariaus Valley from Warjilis Trade City"
)

bariaus_valley_from_golgorand = BattleRegionMapping(
    [0xBD, 0xBE, 0xBF, 0xC0],
    [BariausValley, Golgorand],
    "Bariaus Valley from Golgorand Execution Site"
)

bariaus_valley = BattleRegionMapping(
    [0x60, 0x19D],
    [BariausValley],
    "Bariaus Valley"
)

finath_from_bervenia = BattleRegionMapping(
    [0xC1, 0xC2, 0xC3, 0xC4],
    [Finath, BerveniaCity],
    "Finath River from Bervenia Free City"
)

finath_from_zeltennia = BattleRegionMapping(
    [0xC5, 0xC6, 0xC7, 0xC8],
    [Finath, Zeltennia],
    "Finath River from Zeltennia Castle"
)

finath = BattleRegionMapping(
    [0x69, 0x1BC],
    [Finath],
    "Finath River"
)

poeskas_from_germinas = BattleRegionMapping(
    [0xCD, 0xCE, 0xCF, 0xD0],
    [Poeskas, Germinas],
    "Poeskas Lake from Germinas Peak"
)

poeskas_from_limberry = BattleRegionMapping(
    [0xD1, 0xD2, 0xD3, 0xD4],
    [Poeskas, Limberry],
    "Poeskas Lake from Limberry Castle"
)

poeskas = BattleRegionMapping(
    [0x99, 0x1C5],
    [Poeskas],
    "Poeskas Lake"
)

germinas_from_poeskas = BattleRegionMapping(
    [0xDD, 0xDE, 0xDF, 0xE0],
    [Germinas, Poeskas],
    "Germinas Peak from Poeskas Lake"
)

germinas_from_zarghidas = BattleRegionMapping(
    [0xD9, 0xDA, 0xDB, 0xDC],
    [Germinas, Zarghidas],
    "Germinas Peak from Zarghidas Trade City"
)

germinas = BattleRegionMapping(
    [0x6A, 0x1C4],
    [Germinas],
    "Germinas Peak"
)

nogias = BattleRegionMapping(
    [0xF9, 0xFA, 0xFB, 0xFC],
    [DeepDungeon],
    "NOGIAS"
)

terminate = BattleRegionMapping(
    [0xF5, 0xF6, 0xF7, 0xF8],
    [DeepDungeon],
    "TERMINATE"
)

delta = BattleRegionMapping(
    [0xF1, 0xF2, 0xF3, 0xF4],
    [DeepDungeon],
    "DELTA"
)

valkyries = BattleRegionMapping(
    [0xED, 0xEE, 0xEF, 0xF0],
    [DeepDungeon],
    "VALKYRIES"
)

mlapan = BattleRegionMapping(
    [0xE9, 0xEA, 0xEB, 0xEC],
    [DeepDungeon],
    "MLAPAN"
)

tiger = BattleRegionMapping(
    [0xE5, 0xE6, 0xE7, 0xE8],
    [DeepDungeon],
    "TIGER"
)

bridge = BattleRegionMapping(
    [0xE1, 0xE2, 0xE3, 0xE4],
    [DeepDungeon],
    "BRIDGE"
)

voyage = BattleRegionMapping(
    [0xD5, 0xD6, 0xD7, 0xD8],
    [DeepDungeon],
    "VOYAGE"
)

horror = BattleRegionMapping(
    [0xC9, 0xCA, 0xCB, 0xCC],
    [DeepDungeon],
    "HORROR"
)

end = BattleRegionMapping(
    [0x192],
    [DeepDungeon],
    "END"
)

dorter = BattleRegionMapping(
    [0x181, 0x193],
    [Dorter],
    "Dorter Trade City"
)

gariland = BattleRegionMapping(
    [0x184],
    [Gariland],
    "Gariland Magic City"
)

thieves_fort = BattleRegionMapping(
    [0x18B],
    [ThievesFort],
    "Thieves' Fort"
)

zeakden = BattleRegionMapping(
    [0x191],
    [Zeakden],
    "Fort Zeakden"
)

zaland = BattleRegionMapping(
    [0x197],
    [Zaland],
    "Zaland Fort City"
)

goug = BattleRegionMapping(
    [0x19B],
    [Goug],
    "Goug Machine City"
)

golgorand = BattleRegionMapping(
    [0x19E],
    [Golgorand],
    "Golgorand Execution Site"
)

lionel = BattleRegionMapping(
    [0x19F, 0x1A0],
    [Lionel],
    "Lionel Castle"
)

goland = BattleRegionMapping(
    [0x1A1, 0x1CF, 0x1D0, 0x1D1, 0x1D2],
    [Goland],
    "Goland Coal City"
)

zarghidas = BattleRegionMapping(
    [0x1A3],
    [Zarghidas],
    "Zarghidas Trade City"
)

lesalia = BattleRegionMapping(
    [0x1A4],
    [Lesalia],
    "Lesalia Imperial Capital"
)

orbonne = BattleRegionMapping(
    [0x1A6, 0x1A7, 0x1A8],
    [Orbonne],
    "Orbonne Monastery"
)

yardow = BattleRegionMapping(
    [0x1AC],
    [Yardow],
    "Yardow Fort City"
)

riovanes = BattleRegionMapping(
    [0x1AF, 0x1B0, 0x1B1],
    [Riovanes],
    "Riovanes Castle"
)

orbonne_lower = BattleRegionMapping(
    [0x1B3, 0x1B4, 0x1B6, 0x1B7, 0x1B8, 0x1B9],
    [Orbonne],
    "Orbonne Monastery Depths"
)

bervenia_city = BattleRegionMapping(
    [0x1BB],
    [BerveniaCity],
    "Bervenia Free City"
)

zeltennia = BattleRegionMapping(
    [0x1BD],
    [Zeltennia],
    "Zeltennia Castle"
)

bethla = BattleRegionMapping(
    [0x1C0, 0x1C1, 0x1C2],
    [Bethla],
    "Bathla Garrison"
)

limberry = BattleRegionMapping(
    [0x1C6, 0x1C8, 0x1C9],
    [Limberry],
    "Limberry Castle"
)

igros = BattleRegionMapping(
    [0x1CB],
    [Igros],
    "Igros Castle"
)

murond_temple = BattleRegionMapping(
    [0x1CC, 0x1CD, 0x1CE],
    [Murond],
    "Murond Holy Place"
)

nelveska = BattleRegionMapping(
    [0x1D4],
    [Nelveska],
    "Nelveska Temple"
)

all_battle_region_mappings: list[BattleRegionMapping] = [
    dolbodar_from_bethla, dolbodar_from_limberry, dolbodar,
    fovoham_from_riovanes, fovoham_from_zeakden, fovoham_from_lenalia, fovoham,
    sweegy, sweegy_from_gariland, sweegy_from_dorter,
    bervenia_from_riovanes, bervenia_from_zeklaus, bervenia,
    zeklaus_from_dorter, zeklaus_from_bervenia, zeklaus_from_goland, zeklaus,
    lenalia_from_fovoham, lenalia_from_gariland, lenalia,
    zigolis_from_goug, zigolis_from_lionel, zigolis,
    yuguo_from_yardow, yuguo_from_riovanes, yuguo,
    araguay_from_dorter, araguay_from_zirekile, araguay,
    grog_from_lesalia, grog_from_doguola, grog_from_yardow, grog,
    bed_from_bervenia, bed_from_bethla, bed,
    zirekile_from_zaland, zirekile_from_bethla, zirekile_from_araguay, zirekile,
    bariaus_hill_from_zaland, bariaus_hill_from_lionel, bariaus_hill,
    mandalia_from_gariland, mandalia_from_igros, mandalia_from_thieves_fort, mandalia,
    doguola_from_grog, doguola_from_bervenia, doguola,
    bariaus_valley_from_lionel, bariaus_valley_from_warjilis, bariaus_valley_from_golgorand, bariaus_valley,
    finath_from_bervenia, finath_from_zeltennia, finath,
    poeskas_from_germinas, poeskas_from_limberry, poeskas,
    germinas_from_poeskas, germinas_from_zarghidas, germinas,
    nogias, terminate, delta, valkyries, mlapan, tiger, bridge, voyage, horror, end,
    dorter, gariland, thieves_fort, zeakden, zaland, goug, golgorand, lionel,
    goland, zarghidas, lesalia, orbonne, yardow, riovanes, orbonne_lower,
    bervenia_city, zeltennia, bethla, limberry, igros, murond_temple, nelveska,
]

battle_id_to_battle_region_mapping = {}

for mapping in all_battle_region_mappings:
    for battle_id in mapping.battle_ids:
        battle_id_to_battle_region_mapping[battle_id] = mapping

class PoachHintLocation:
    base_name: str
    battle_level: int
    battle_id: int
    formation_id_lookup = {
        0: "Formation 1",
        2: "Formation 2",
        5: "Formation 3",
        8: "Formation 4",
        9: "Rare"
    }

    def __init__(self, base_name: str, battle_level: int, battle_id: int):
        self.base_name = base_name
        self.battle_level = battle_level
        self.battle_id = battle_id

    def get_text(self):
        return_string = self.base_name
        if self.battle_id < 0x100:
            if not self.base_name.isupper():
                return_string += f" {PoachHintLocation.formation_id_lookup[self.battle_level]}"
        return return_string