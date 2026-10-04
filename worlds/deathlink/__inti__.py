from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths
from settings import Group, Bool, UserFolderPath, _world_settings_name_cache
from typing import Any, ClassVar, NamedTuple, Callable,Optional
from worlds.AutoWorld import World
from BaseClasses import CollectionState,Entrance
from collections import Counter
from enum import Enum


def launch_client(*args):
    from worlds.LauncherComponents import launch
    from .client import run_as_textclient as launch_deathlink
    launch(launch_deathlink, name="Deathlink Client", args=args)


class DeathlinkClientWorld(World):
    game = "Deathlink Client"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

icon_paths["dlc_ico"] = f"ap:{__name__}/icon.png"
components.append(Component("Deathlink Client", None, func=launch_client, component_type=Type.CLIENT, icon="dlc_ico"))