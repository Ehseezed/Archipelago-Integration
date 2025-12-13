try:
    from . import kivy_data_prep as _kdp
    try:
        _kdp.ensure_kivy_data_available()
    except Exception:
        import logging
        logging.exception("Failed calling worlds.multi_manager.kivy_data_prep.ensure_kivy_data_available()")
except Exception:
    import logging
    logging.exception("Failed importing worlds.multi_manager.kivy_data_prep (best-effort)")

from worlds.LauncherComponents import Component, Type, components, launch_subprocess, icon_paths

from worlds.AutoWorld import World

# class MultiManagerSettings(Group):
#     a: str = "A Dummy Setting"
#     "A Dummy Setting Description"

class MultiManagerWorld(World):
    """
    A system fo keeping your slots in Multiworlds in order.
    """
    # settings: ClassVar[MultiManagerSettings]
    # settings_key = "multi_manager"

    game: str = "Multi Manager"
    hidden = True

    item_name_to_id = {}
    location_name_to_id = {}

def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="MultiManager", args=args)


components.append(Component("Multiworld Manager", component_type=Type.TOOL, func=launch_client, icon="MultiManager"))

icon_paths["MultiManager"] = f"ap:{__name__}/assets/icon.png"