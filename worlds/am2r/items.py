from itertools import groupby
from typing import Dict, List, Set, NamedTuple
from BaseClasses import ItemClassification


class AM2RItemData(NamedTuple):
    classification: ItemClassification
    game_id: int
    quantity_in_item_pool: int
    item_group: str = ""


item_base_id = 108678000

item_table: Dict[str, AM2RItemData] = {
    "Missile":                  AM2RItemData(ItemClassification.filler, 15, 0),
    "Main Missiles":            AM2RItemData(ItemClassification.progression, 300, 0),

    "Super Missile":            AM2RItemData(ItemClassification.filler, 16, 0),
    "Main Super Missile":       AM2RItemData(ItemClassification.progression, 301, 0),

    "Power Bomb":               AM2RItemData(ItemClassification.filler, 18, 0),
    "Main Power Bombs":         AM2RItemData(ItemClassification.progression, 302, 0),

    "Energy Tank":              AM2RItemData(ItemClassification.filler, 17, 0),

    "Morph Ball":               AM2RItemData(ItemClassification.progression, 303, 0),
    "Power Grip":               AM2RItemData(ItemClassification.progression, 304, 0),
    "Bombs":                    AM2RItemData(ItemClassification.progression, 0, 1),
    "Spider Ball":              AM2RItemData(ItemClassification.progression, 2, 1),
    "Hi Jump":                  AM2RItemData(ItemClassification.progression, 4, 1),
    "Spring Ball":              AM2RItemData(ItemClassification.progression, 3, 1),

    "Space Jump":               AM2RItemData(ItemClassification.progression, 6, 1),
    "Speed Booster":            AM2RItemData(ItemClassification.progression, 7, 1),
    "Shinespark":               AM2RItemData(ItemClassification.progression, 306, 1),
    "Screw Attack":             AM2RItemData(ItemClassification.progression, 8, 1),

    "Varia Suit":               AM2RItemData(ItemClassification.progression, 5, 1),
    "Gravity Suit":             AM2RItemData(ItemClassification.progression, 9, 1),

    "Arm Cannon Main":          AM2RItemData(ItemClassification.progression, 305, 0),
    "Charge Beam":              AM2RItemData(ItemClassification.progression, 10, 1),
    "Wave Beam":                AM2RItemData(ItemClassification.useful, 12, 1),
    "Spazer":                   AM2RItemData(ItemClassification.useful, 13, 1),
    "Plasma Beam":              AM2RItemData(ItemClassification.useful, 14, 1),
    "Ice Beam":                 AM2RItemData(ItemClassification.progression, 11, 1),

    "Flood Trap":               AM2RItemData(ItemClassification.trap, 21, 0),
    "Big Toss Trap":            AM2RItemData(ItemClassification.trap, 22, 0),
    "Short Beam":               AM2RItemData(ItemClassification.trap, 23, 0),
    "EMP Trap":                 AM2RItemData(ItemClassification.trap, 24, 0),
    "OHKO Trap":                AM2RItemData(ItemClassification.trap, 25, 0),
    "Touhou Trap":              AM2RItemData(ItemClassification.trap, 26, 0),

    "EMP":                      AM2RItemData(ItemClassification.event, None, 0),  # todo: This will be made in init as a event not in items I just needed this down somewhere
    "Tower Activation":         AM2RItemData(ItemClassification.event, None, 0),
    "Geothermal":               AM2RItemData(ItemClassification.event, None, 0),

    "Metroid":                  AM2RItemData(ItemClassification.progression_skip_balancing, 19, 0),


    "Unknown Item SM":          AM2RItemData(ItemClassification.progression, 312, 0),
    "Unknown Item IM":          AM2RItemData(ItemClassification.progression, 313, 0),
    "Unknown Item PS":          AM2RItemData(ItemClassification.progression, 310, 0),
    "Unknown Item CB":          AM2RItemData(ItemClassification.progression, 316, 0),
    "Unknown Item SB":          AM2RItemData(ItemClassification.progression, 311, 0),
    "Unknown Item DB":          AM2RItemData(ItemClassification.progression, 314, 0),
    "Unknown Item FS":          AM2RItemData(ItemClassification.progression, 315, 0),
    "Unknown Item DC":          AM2RItemData(ItemClassification.progression, 308, 0),
    "Unknown Item LB":          AM2RItemData(ItemClassification.progression, 317, 0),

}

item_name_to_id: Dict[str, int] = {name: item_base_id + data.game_id for name, data in item_table.items()}

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == ItemClassification.filler]

trap_items: List[str] = [name for name, data in item_table.items() if data.classification == ItemClassification.trap]
