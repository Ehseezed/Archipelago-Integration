from typing import ClassVar
from settings import Group
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from worlds.AutoWorld import World

class ManagerSettings(Group):
    repositories: dict = {"https://raw.githubusercontent.com/silasary/apworlds/refs/heads/main/index.json": True}
    "A list of Repository URLs and whether they're enabled or not."
    github_token: str = ""
    "A GitHub token to use for authentication when accessing private repositories.  Use this if you're encountering rate limits."
    show_after_dark: bool = False
    "Show non-installed After Dark games."
    show_manuals: bool = True
    "Show non-installed Manuals."
    show_prereleases: bool = False
    "Show prerelease versions of games."

class RepoWorld(World):
    """
    Package manager for Archipelago Worlds
    """
    settings: ClassVar[ManagerSettings]
    settings_key = "apworld_manager"

    # to make auto world register happy so we can register our settings
    game = "APWorld Manager"
    world_version_str = "0.0.20"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def launch_client(*args: str) -> None:
    from .kv_app import launch
    launch_subprocess(launch, name="APManager", args=args)

components.append(Component("Install/Update Apworlds", None, func=launch_client, component_type=Type.TOOL))
components.append(Component("worldman", None, func=launch_client, component_type=Type.HIDDEN))
