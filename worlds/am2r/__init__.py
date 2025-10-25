import logging
from collections import Counter
from typing import Dict, TextIO, List

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


# python
def get_version():
    import urllib.request
    import os
    import json
    import zipfile
    from pathlib import Path
    from io import TextIOWrapper

    try:
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/Ehseezed/Archipelago-Integration/refs/heads/8th-Aniversary/worlds/am2r/archipelago.json") as metadata_resp:
            metadata_json = json.loads(metadata_resp.read().decode())
    except Exception as e:
        logger.warning(f"Failed to fetch remote metadata: {e}")
        metadata_json = {}

    dirpath = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(dirpath, "archipelago.json")
    local_json = {}

    # Try to read the file directly first
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            local_json = json.load(f)
    except Exception:
        # If direct read fails, check if this module is inside a .apworld archive and try to open it as a zip
        try:
            p = Path(dirpath)
            parts = p.parts
            ap_index = next((i for i, part in enumerate(parts) if part.lower().endswith(".apworld")), None)
            if ap_index is not None:
                archive_path = Path(*parts[: ap_index + 1])
                internal_parts = parts[ap_index + 1 :]
                # candidate internal path using forward slashes
                candidate = "/".join((*internal_parts, "archipelago.json")) if internal_parts else "archipelago.json"
                try:
                    with zipfile.ZipFile(str(archive_path), "r") as z:
                        namelist = z.namelist()
                        target = candidate if candidate in namelist else next((n for n in namelist if n.lower().endswith("archipelago.json")), None)
                        if target:
                            with z.open(target) as bf:
                                with TextIOWrapper(bf, encoding="utf-8") as f:
                                    local_json = json.load(f)
                        else:
                            logger.warning(f"No archipelago.json found inside archive {archive_path} (checked {candidate})")
                except Exception as e:
                    logger.warning(f"Failed to read metadata from archive {archive_path}: {e}")
            else:
                logger.warning(f"Failed to read local metadata: file not found at {full_path}")
        except Exception as e:
            logger.warning(f"Failed to locate .apworld archive for local metadata: {e}")

    web_version = metadata_json.get("world_version") if metadata_json else None
    local_version = local_json.get("world_version") if local_json else None
    return local_version, web_version



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

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write("\nAM2R Archipelago Debug Spoiler Header\n")
        spoiler_handle.write("=====================================\n\n")
        items = self.multiworld.itempool
        items = Counter(items)
        spoiler_handle.write("Item Pool:\n")
        for item_name, count in items.items():
            spoiler_handle.write(f"  {item_name}: {count}\n")
        spoiler_handle.write("\n")


    def fill_slot_data(self) -> Dict[str, object]:
        local_version, web_version = get_version()
        try:
            if local_version is None or web_version is None:
                raise ValueError("One or both version values are not valid")
                loca
            elif local_version < web_version:
                input(f'A new version of AM2R is available most recent release is version {web_version} and you are using {local_version}, '
                      f'consider updating to the latest version'
                      f'\npress enter to continue.')
            elif local_version > web_version:
                input(f"Hi there developer! It looks like you are running a development version of AM2R {local_version} ahead of the latest release {web_version}."
                      f"\nIf you are seeing this message and are not a developer, I dont know how you managed that, but consider switching to the latest release version."
                      f"\npress enter to continue.")
        except Exception as e:
            err =  f"Failed to validate version data beacuse: "
            if local_version == None:
                err += "local version is invalid. "
            if web_version == None:
                err += "web version is invalid. "
            print(err + str(e))
        local_version = "unknown" if local_version is None else local_version


        return {
            "Version": local_version,
            "MetroidsRequired": self.options.MetroidsRequired.value,
            # "MetroidsInPool": self.options.MetroidsInPool.value,  # I never pull this
            # "LocationSettings": self.options.LocationSettings.value, # I never pull this
            "TrapFillPercentage": self.options.TrapFillPercentage.value,
            # "RemoveFloodTrap": self.options.RemoveFloodTrap.value, # I never pull this
            # "RemoveTossTrap": self.options.RemoveTossTrap.value, # I never pull this
            # "RemoveShortBeam": self.options.RemoveShortBeam.value, # I never pull this
            # "RemoveEMPTrap": self.options.RemoveEMPTrap.value, # I never pull this
            # "RemoveTouhouTrap": self.options.RemoveTouhouTrap.value, # I never pull this
            # "RemoveOHKOTrap": self.options.RemoveOHKOTrap.value, # I never pull this
            # "RemoveWrongWarpTrap": self.options.RemoveWrongWarpTrap.value, # I never pull this
            # "RemoveIceTrap": self.options.RemoveIceTrap.value, # I never pull this
            "TrapSprites": self.options.TrapSprites.value,
            "Tozos": self.options.Tozos.value,
            "CustomDeathLinkMessages": list(self.options.CustomDeathLinkMessages.value),
            "DeathlinkMessagePacks": list(self.options.DeathlinkMessagePacks.value),
            "DeathLink": self.options.DeathLink.value,
            "TrapSeed": int(self.random.randint(0, 2**64 - 1)),
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
