from typing import ClassVar
from settings import Group
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from worlds.AutoWorld import World

class MultiManagerSettings(Group):
    a: str = "A Dummy Setting"
    "A Dummy Setting Description"

class MultiManagerWorld(World):
    """
    A system fo keeping your slots in Multiworlds in order.
    """
    settings: ClassVar[MultiManagerSettings]
    settings_key = "multi_manager"

    game = "Multi Manager"
    world_version_str = "0.0.0"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="MultiManager", args=args)

components