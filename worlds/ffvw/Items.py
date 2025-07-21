from typing import Dict, Set, Tuple, NamedTuple, Optional
from BaseClasses import ItemClassification, Item
from worlds.ffvw import FFVWLocation


# class ItemData:
#     def __init__(self, item_id, classification, groups=(), data_name=None):
#         self.groups = groups
#         self.classification = classification
#         self.id = None
#         if item_id is not None:
#             #self.id = item_id + 0x6900
#             self.id = item_id
#         self.data_name = data_name


class ItemData(NamedTuple):
    group: str
    code: Optional[int]
    classification: ItemClassification = ItemClassification.useful


class FFVWItem:
    game: str = "Final Fantasy V: Whirlwind"

# item_table = {
#     "Monk, Thief": 0xC00001,
#     "Dragoon, Ninja": 0xC00002,
#     "Samurai": 0xC00003,
#     "Berserker, Hunter": 0xC00004,
#     "Mystic Knight, White Mage": 0xC00005,
#     "Black Mage": 0xC00006,
#     "Time Mage, Summoner": 0xC00007,
#     "Blue Mage, Red Mage": 0xC00008,
#     "Mediator": 0xC00009,
#     "Chemist, Geomancer": 0xC0000A,
#     "Bard, Dancer": 0xC0000B,
#     "Knight": 0xC0000C,
# }


item_table: Dict[str, ItemData] = {
    "Monk, Thief": ItemData("Jobs", 0xC00001, ItemClassification.useful),
    "Dragoon, Ninja": ItemData("Jobs", 0xC00002, ItemClassification.useful),
    "Samurai": ItemData("Jobs", 0xC00003, ItemClassification.useful),
    
    "Berserker, Hunter": ItemData("Jobs", 0xC00004, ItemClassification.useful),
    "Mystic Knight, White Mage": ItemData("Jobs", 0xC00005, ItemClassification.useful),
    "Black Mage": ItemData("Jobs", 0xC00006, ItemClassification.useful),
    
    "Time Mage, Summoner": ItemData("Jobs", 0xC00007, ItemClassification.useful),
    "Blue Mage, Red Mage": ItemData("Jobs", 0xC00008, ItemClassification.useful),
    "Mediator": ItemData("Jobs", 0xC00009, ItemClassification.useful),
    
    "Chemist, Geomancer": ItemData("Jobs", 0xC0000A, ItemClassification.useful),
    "Bard, Dancer": ItemData("Jobs", 0xC0000B, ItemClassification.useful),
    "Knight": ItemData("Jobs", 0xC0000C, ItemClassification.useful),
}

prog_map = {
}


def yaml_item(text):
    return "".join(
        [(" " + c if (c.isupper() or c.isnumeric()) and not (text[i - 1].isnumeric() and c == "F") else c) for
         i, c in enumerate(text)]).strip()


"""item_groups = {}
for item, data in item_table.items():
    for group in data.groups:
        item_groups[group] = item_groups.get(group, []) + [item]"""


def create_items(self) -> None:
    items = []
  
    def add_item(item_name):        
        i = self.create_item(item_name)
        i.classification = ItemClassification.useful
        items.append(i)

    """for item_group in (["Jobs"]):
        for item in sorted(self.item_name_groups[item_group]):
            add_item(item)"""

    self.multiworld.itempool += items



# class FFVWItem(Item):
#     game = "Final Fantasy V: Whirlwind"
#     type = None
#
#     def __init__(self, name, player: int = None):
#         item_data = item_table[name]
#         super(FFVWItem, self).__init__(
#             name,
#             item_data.classification,
#             item_data.id, player
#         )