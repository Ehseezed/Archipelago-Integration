import logging
from typing import Dict

from .items import item_table, item_name_groups, item_name_to_id, create_item, create_all_items
from .locations import get_location_datas, EventId
from .regions import create_regions_and_locations
from BaseClasses import Tutorial, Item, ItemClassification
from .options import AM2ROptions, LocationSettings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, icon_paths, launch


logger = logging.getLogger("AM2R")


def launch_client():
    from .Client import launch as am2r_client
    launch(am2r_client, name="AM2RClient")

icon_paths["am2r_icon"] = f"ap:{__name__}/icon.png"
components.append(
    Component("AM2R Client", func=launch_client, component_type=Type.CLIENT, icon="am2r_icon")
)


class AM2RWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago AM2R software on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Zed"]
    )]


class AM2RWorld(World):
    """
    AM2R is a remake of the classic Metroid 2 game for the Game Boy that tries its best to keep the feel
    of the original as well as filling in some gaps to more closely tie into Metroid Fusion and brings some
    items from there as well.
    """
    game = "AM2R"
    options: AM2ROptions
    options_dataclass = AM2ROptions

    web = AM2RWeb()

    item_name_to_id = item_name_to_id
    location_name_to_id = {location.name: location.code for location in get_location_datas(None, None)}

    item_name_groups = item_name_groups
    data_version = 1

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "MetroidsRequired": self.options.MetroidsRequired.value,
            "MetroidsInPool": self.options.MetroidsInPool.value,
            "LocationSettings": self.options.LocationSettings.value,
            "TrapFillPercentage": self.options.TrapFillPercentage.value,
            "RemoveFloodTrap": self.options.RemoveFloodTrap.value,
            "RemoveTossTrap": self.options.RemoveTossTrap.value,
            "RemoveShortBeam": self.options.RemoveShortBeam.value,
            "RemoveEMPTrap": self.options.RemoveEMPTrap.value,
            "RemoveTouhouTrap": self.options.RemoveTouhouTrap.value,
            "RemoveOHKOTrap": self.options.RemoveOHKOTrap.value,
            "RemoveWrongWarpTrap": self.options.RemoveWrongWarpTrap.value,
            "TrapSprites": self.options.TrapSprites.value,
            "Tozos": self.options.Tozos.value,
            "CustomDeathLinkMessages": list(self.options.CustomDeathLinkMessages.value),
            "DeathlinkMessagePacks": list(self.options.DeathlinkMessagePacks.value),
            "DeathLink": self.options.DeathLink.value,
            "TrapSeed": int(self.random.random() % (2 ** 32))
        }

    def create_regions(self) -> None:
        create_regions_and_locations(self.multiworld, self.player)
        self.multiworld.get_location("The Last Metroid is in Captivity", self.player).place_locked_item(self.create_event("The Galaxy is at Peace"))

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        if self.options.MetroidsRequired > self.options.MetroidsInPool:
            logger.warning(f"Metroids in pool raised to {self.options.MetroidsRequired.value} for {self.multiworld.get_player_name(self.player)} because the given count was too low for the requirement.")
        if self.options.LocationSettings != LocationSettings.option_add_metroids_and_A6:
            self.multiworld.get_location("Deep Caves: Lil\' Bro", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Deep Caves: Big Sis", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: SA-X Queen Lucina", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: Epsilon", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: Druid", self.player).place_locked_item(self.create_item("Metroid"))
            if self.options.LocationSettings != LocationSettings.option_add_metroids_no_A6:
                self.multiworld.get_location("The Forgotten Alpha", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple: Friendly Spider", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Moe", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Larry", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Curly", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Main Caves: Freddy Fazbear", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: Turbine Terror", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: The Lookout", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: Recent Guardian", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: EnderMahan", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Carnage Awful", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Venom Awesome", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Something More, Something Awesome",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Mimolette", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: The Big Cheese", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Mohwir", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Chirn", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: BHHarbinger", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: The Abyssal Creature", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Complex: Sisyphus", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Complex: And then there\'s this Asshole",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Inside Industrial: Guardian of Doom Treadmill",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Inside Industrial: Rawsome1234 by the Lava Lake",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Research Camp Dual Alphas: Marco", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Research Camp Dual Alphas: Polo", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Mines: Unga", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Mines: Gunga", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Patricia", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Variable \"GUH\"", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Slagathor, the Ruler", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Mr.Sandman", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Anakin", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Xander", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("EMP: Sir Zeta Commander of the Alpha Squadron", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Timmy", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Tommy", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Terry", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Telly", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Martin", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center: Gamma Bros Mario", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center: Gamma Bros Luigi", self.player).place_locked_item(self.create_item("Metroid"))

        if self.options.LocationSettings == LocationSettings.option_items_no_A6 or self.options.LocationSettings == LocationSettings.option_add_metroids_no_A6:
            self.options.exclude_locations.value.add("Deep Caves: Drivel Ballspark")
            self.options.exclude_locations.value.add("Deep Caves: Ramulken Lava Pool")
            self.options.exclude_locations.value.add("Deep Caves: After Omega")

        create_all_items(self)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("The Galaxy is at Peace", self.player)
