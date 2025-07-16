import Utils
import settings
import base64
import threading
import requests
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, ItemClassification, Tutorial
from .Items import item_table, create_items, FFVWItem
from .Locations import location_table, FFVWLocation
from .Regions import create_regions
#from .Output import generate_output
#from .Options import FFVWOptions
from .Client import FFVWClient


class FFVWWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy V: Whirlwind with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["clymax"]
        )
    
    
    tutorials = [setup_en]
    game_info_languages = ["en"]


class FFVWWorld(World):
    """Final Fantasy: V: Whirlwind is a light-hearted JRPG for the Super Nintendo."""

    game = "Final Fantasy V: Whirlwind"
    topology_present = False
    web = FFVWWebWorld()
    base_id = 1234

    #item_name_to_id = {name: data.id for name, data in item_table.items() if data.id is not None}
    #location_name_to_id = {name: data.name for name, data in location_table.items() if data.name is not None}
    item_name_to_id = item_table
    location_name_to_id = location_table

    def create_regions(self):
        create_regions(self)

    def create_item(self, name: str, classification: ItemClassification = ItemClassification.useful) -> Item:
        return FFVWItem(name, classification, item_table[name], self.player)

    def create_items(self):
        create_items(self)
        #jobs = [self.create_item("Job " + str(i+1).zfill(2), ItemClassification.useful) for i in range(1, 12)]
        #self.multiworld.itempool += jobs


#   create_regions = create_regions

#    location_name_to_id = location_table
#    options_dataclass = FFVWOptions
#    options: FFVWOptions
#    topology_present = True
#    item_name_groups = item_groups

#generate_output = generate_output
#create_items = create_items
#create_regions = create_regions
#set_rules = set_rules
#stage_set_rules = stage_set_rules

#web = FFVWWebWorld()
# settings: FFVWSettings


