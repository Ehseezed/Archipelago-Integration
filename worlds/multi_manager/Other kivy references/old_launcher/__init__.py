from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, Type, components, launch_subprocess


class LauncherWorld(World):
    """
    Do you miss the old Archipelago launcher?
    """
    game: str = "Old Launcher"
    hidden = True

    item_name_to_id = {}
    location_name_to_id = {}


def launch_client(*args: str) -> None:
    from .launcher import main
    launch_subprocess(main, name="Old Launcher", args=args)

components.append(Component("Old Launcher", None, func=launch_client, component_type=Type.TOOL))
components.append(Component("kvlauncher", None, func=launch_client, component_type=Type.HIDDEN))
