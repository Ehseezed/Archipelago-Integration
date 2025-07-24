import os
import zipfile
from base64 import b64encode

from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .options import Pikmin2Options
from .items import item_data, get_classification, pikmin2_items, Pikmin2Item, buried_treasure, explorer_kit_treasure
from .locations import location_data, Pikmin2Location, vor_prefixes, aw_prefixes, pp_prefixes, ww_prefixes, pikmin2_locations, impossible_buried_treasure_locations
from BaseClasses import Region, ItemClassification, CollectionState
import json
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths
from settings import UserFilePath, Group, UserFolderPath
from typing import ClassVar

import yaml

from ..Files import APPlayerContainer


def launch_client(*args):
    from .Pikmin2Client import launch
    launch_subprocess(launch, name="Pikmin2Client", args=args)


components.append(
    Component(
        "Pikmin2Client",
        func=launch_client,
        component_type=Type.CLIENT
        # icon="Pikmin 2"
    ),
)
# icon_paths["Pikmin 2"] = "ap:worlds.pikmin2/icon.png"

def item_name_id_mapping(items):
    item_dict = {}
    modifier = 1
    for item in items:
        if (item[0] == "Brute Knuckles"):
            modifier = 501
        item_dict[item[0]] = item[2] + modifier
    return item_dict

def location_name_id_mapping(locations):
    loc_dict = {}
    count = 1
    for loc in locations:
        loc_dict[loc[0]] = count
        count += 1
    return loc_dict

def test_location(name, prefix_list):
    for prefix in prefix_list:
        if (name.startswith(prefix)):
            return True
    return False

class Pikmin2Settings(Group):
    class DolphinPath(UserFilePath):
        """
        Dolphin executable location
        """
        is_exe = True
        description = "Dolphin Executable"
    class SaveFolder(UserFolderPath):
        """
        Path to Dolphin save folder
        """
        description = "Dolphin Save Folder"

    dolphin_path: DolphinPath = DolphinPath(None)
    # game_path: GamePath = GamePath(None)
    # mapping_path: MappingPath = MappingPath(None)
    save_folder: SaveFolder = SaveFolder(None)

class P2Container(APPlayerContainer):
    """
    Container for Pikmin 2 player data.
    """
    game: str = "Pikmin 2"
    patch_file_ending = ".zip"

    def __init__(self, *args, **kwargs) -> None:
        if "data" in kwargs:
            self.data = kwargs["data"]
            del kwargs["data"]

        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)



class Pikmin2World(World):
    """
    Tasked with helping pay off their employer's debt, explorers Olimar and Louie team up with Pikmin (including purple and white Pikmin) to collect treasure on a strange planet. Time ticks away on the surface, but cave systems let you take your time to let your strategy blossom.  
    """
    game = "Pikmin 2"
    options_dataclass = Pikmin2Options
    options: Pikmin2Options
    topology_present = True
    settings: ClassVar[Pikmin2Settings]

    item_name_to_id = item_name_id_mapping(item_data)
    location_name_to_id = location_name_id_mapping(location_data)

    origin_region_name = "Valley of Repose"

    def check_pokos(self, state, amt):
        pokos = 0
        for item in state.prog_items[self.player].keys():
            for i in item_data:
                if (i[0] == item):
                    pokos += i[4]
                    break
        return pokos >= amt
    
    def create_regions(self):
        valley_of_repose_region = Region("Valley of Repose", self.player, self.multiworld)
        valley_of_repose_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, vor_prefixes)}
        valley_of_repose_region.add_locations(valley_of_repose_locations, Pikmin2Location)
        self.multiworld.regions.append(valley_of_repose_region)
        awakening_wood_region = Region("Awakening Wood", self.player, self.multiworld)
        awakening_wood_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, aw_prefixes)}
        awakening_wood_region.add_locations(awakening_wood_locations, Pikmin2Location)
        self.multiworld.regions.append(awakening_wood_region)
        perplexing_pool_region = Region("Perplexing Pool", self.player, self.multiworld)
        perplexing_pool_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, pp_prefixes)}
        perplexing_pool_region.add_locations(perplexing_pool_locations, Pikmin2Location)
        self.multiworld.regions.append(perplexing_pool_region)
        wistful_wild_region = Region("Wistful Wild", self.player, self.multiworld)
        wistful_wild_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, ww_prefixes)}
        wistful_wild_region.add_locations(wistful_wild_locations, Pikmin2Location)
        wistful_wild_region.locations.append(Pikmin2Location(self.player, "Pay Off Debt", None, wistful_wild_region))
        if (self.options.win_condition == 0):
            wistful_wild_region.locations.append(Pikmin2Location(self.player, "Beat Titan Dweevil", None, wistful_wild_region))
        elif (self.options.win_condition == 1):
            wistful_wild_region.locations.append(Pikmin2Location(self.player, "Reach Poko Count", None, wistful_wild_region))
        elif (self.options.win_condition == 2):
            wistful_wild_region.locations.append(Pikmin2Location(self.player, "Reach Treasure Count", None, wistful_wild_region))
        self.multiworld.regions.append(wistful_wild_region)
        valley_of_repose_region.connect(awakening_wood_region)
        valley_of_repose_region.connect(perplexing_pool_region)
        awakening_wood_region.connect(valley_of_repose_region)
        awakening_wood_region.connect(perplexing_pool_region)
        perplexing_pool_region.connect(awakening_wood_region)
        perplexing_pool_region.connect(valley_of_repose_region)
        valley_of_repose_region.connect(wistful_wild_region)
        awakening_wood_region.connect(wistful_wild_region)
        perplexing_pool_region.connect(wistful_wild_region)

    def create_item(self, item):
        return Pikmin2Item(item, get_classification(item), self.item_name_to_id[item], self.player)
    
    def create_event(self, event):
        return Pikmin2Item(event, ItemClassification.progression, None, self.player)
    
    def create_items(self):
        
        for item in map(self.create_item, pikmin2_items):
            self.multiworld.itempool.append(item)
        
        # remove the titan dweevil treasures
        elec = Pikmin2Item("Shock Therapist", get_classification("Shock Therapist"), 80, self.player)
        fire = Pikmin2Item("Flare Cannon", get_classification("Flare Cannon"), 81, self.player)
        gas = Pikmin2Item("Comedy Bomb", get_classification("Comedy Bomb"), 82, self.player)
        water = Pikmin2Item("Monster Pump", get_classification("Monster Pump"), 83, self.player)
        louie = Pikmin2Item("King of Bugs", get_classification("King of Bugs"), 90, self.player)
        self.multiworld.itempool.remove(elec)
        self.multiworld.itempool.remove(fire)
        self.multiworld.itempool.remove(gas)
        self.multiworld.itempool.remove(water)
        self.multiworld.itempool.remove(louie)
    
    def set_rules(self):
        add_item_rule(self.multiworld.get_location("VoR Courage Reactor", self.player),
                      lambda item: item.player != self.player or item.get_weight() == 20) # this is supposed to disallow placing items that weigh not 20
        
        for item in explorer_kit_treasure:
            forbid_item(self.multiworld.get_location("VoR Courage Reactor", self.player), item, self.player) # can't have EK items in day 1 location

        self.multiworld.get_location("Pay Off Debt", self.player).place_locked_item(self.create_event("Pay Off Debt"))

        add_rule(self.multiworld.get_location("Pay Off Debt", self.player),
                        lambda state: self.check_pokos(state, 10000))
        
        if (self.options.win_condition == 0):
            self.multiworld.get_location("Beat Titan Dweevil", self.player).place_locked_item(self.create_event("Victory"))
        elif (self.options.win_condition == 1):
            self.multiworld.get_location("Reach Poko Count", self.player).place_locked_item(self.create_event("Victory"))
            add_rule(self.multiworld.get_location("Reach Poko Count", self.player),
                lambda state: self.check_pokos(state, self.options.poko_amount))
        elif (self.options.win_condition == 2):
            self.multiworld.get_location("Reach Treasure Count", self.player).place_locked_item(self.create_event("Victory"))
            add_rule(self.multiworld.get_location("Reach Treasure Count", self.player),
                lambda state: len(state.prog_items[self.player]) >= self.options.treasure_amount)
            
        for location in location_data: # handle checks locked behind locations, as well as buried treasure
            # In theory, Spherical Atlas should handle opening AW and Geographic Projection should handle opening PP. The code even supports this. But, when the 
            # Geographic Projection is collected before the Spherical Atlas, both AW and PP open, but only AW is selectable. Then, the next time the player visits
            # the world map, only AW shows up. So basically, a single half gets you to AW, and both halves get you to PP.
            needs_one = False
            needs_both = False
            needs_debt_paid = False
            forbid_buried = False
            if ("blue" in location[4] or "yellow" in location[4]): # TODO - split these so that we can actually check where the onions are located (to support pikmin shuffle option)
                needs_both = True
            # if ("red" in location[4]): there are no checks that require reds to my knowledge
            if (test_location(location[0], aw_prefixes)): 
                needs_one = True
            if (test_location(location[0], pp_prefixes)):
                needs_both = True
            if (test_location(location[0], ww_prefixes) or location[0] == "Beat Titan Dweevil"):
                needs_both = True
                needs_debt_paid = True
            if (location[0] in impossible_buried_treasure_locations):
                forbid_buried = True

            if (not(needs_both)):
                # The Doomsday Apparatus requires 100 Purple Pikmin to carry. In order to get 100 Purple Pikmin you need access to the Subterranean Complex, 
                # which requires Blue Pikmin. Since you need both globe halves to get Blue Pikmin, you need both globe halves to get the Doomsday Apparatus, 
                # and it shouldn't appear anywhere that doesn't require both halves of the globe to access.
                forbid_item(self.multiworld.get_location(location[0], self.player), "Doomsday Apparatus", self.player)
            if (needs_both):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player))
            elif (needs_one):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Geographic Projection", self.player) or state.has("Spherical Atlas", self.player))
            if (needs_debt_paid):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Pay Off Debt", self.player))
            if (forbid_buried):
                for item in buried_treasure:
                    forbid_item(self.multiworld.get_location(location[0], self.player), item, self.player)

        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    
    def pre_fill(self):
        # manually assign these since they can't be randomized
        # archipelago items are 1-indexed
        elec = Pikmin2Item("Shock Therapist", get_classification("Shock Therapist"), 80, self.player)
        fire = Pikmin2Item("Flare Cannon", get_classification("Flare Cannon"), 81, self.player)
        gas = Pikmin2Item("Comedy Bomb", get_classification("Comedy Bomb"), 82, self.player)
        water = Pikmin2Item("Monster Pump", get_classification("Monster Pump"), 83, self.player)
        louie = Pikmin2Item("King of Bugs", get_classification("King of Bugs"), 90, self.player)
        self.multiworld.get_location("DD Shock Therapist", self.player).item = elec
        self.multiworld.get_location("DD Flare Cannon", self.player).item = fire
        self.multiworld.get_location("DD Comedy Bomb", self.player).item = gas
        self.multiworld.get_location("DD Monster Pump", self.player).item = water
        self.multiworld.get_location("DD King of Bugs", self.player).item = louie

    def generate_output(self, output_directory: str) -> None:
        multiworld = self.multiworld
        player = self.player


        output = {
            "seed": multiworld.seed_name,  # to verify the server's multiworld
            "slot_number": player,
            "slot": multiworld.player_name[self.player],  # to connect to server
            "items": {location.name: location.item.name
                    if location.item.player == self.player else "Remote"
                    for location in multiworld.get_filled_locations(self.player) if location.name != "Pay Off Debt" and location.name != "Beat Titan Dweevil" and location.name != "Reach Poko Count" and location.name != "Reach Treasure Count"},
            "starter_items": [item.name for item in multiworld.precollected_items[player]],
            "win_condition": int(self.options.win_condition),
            "poko_amount": int(self.options.poko_amount),
            "treasure_amount": int(self.options.treasure_amount)
        }
        p2 = P2Container(
            os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{P2Container.patch_file_ending}"
            ),
            player = player,
            player_name=self.player_name,
            data= output,
        )
        f = open(output_directory + f"\\pikmin2_{self.multiworld.seed_name}_{self.player_name}.json", "w")
        print(output)
        p2.write()

        output_json = json.dumps(output, indent=4)
        second_json_filename = f"pikmin2_{self.multiworld.seed_name}_{self.player_name}.json"
        zip_path = os.path.join(
            output_directory, f"{multiworld.get_out_file_name_base(player)}.zip"
        )
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.writestr(second_json_filename, output_json)

        print(output)


