import typing
from typing import TYPE_CHECKING
#from BaseClasses import MultiWorld, Region, Entrance, Location
from BaseClasses import MultiWorld, Region, Location
from .Locations import FFVWLocation, location_table

if TYPE_CHECKING:
    from . import FFVWWorld

import logging
logger = logging.getLogger("Final Fantasy V: Whirlwind")

#v6areas = ["Laboratory", "The Tower", "Space Station 2", "Warp Zone"]

#def create_regions(world: MultiWorld, player: int):
#def create_regions(world: FFVWWorld, player: int):
def create_regions(world: "FFVWWorld"):
    #regOvr = Region("Menu", player, world, "Interdimensional Rift")
    #regOvr = Region("Menu", player, world)
    regOvr = Region("Menu", world.player, world.multiworld)
    locOvr_names = ["Kuzar 1", "Kuzar 2", "Kuzar 3", "Kuzar 4", "Kuzar 5", "Kuzar 6",
                    "Kuzar 7", "Kuzar 8", "Kuzar 9", "Kuzar 10", "Kuzar 11", "Kuzar 12"]
    regOvr.locations += [FFVWLocation(world.player, loc_name, location_table[loc_name], regOvr) for loc_name in locOvr_names]
    #world.regions.append(regOvr)
    world.multiworld.regions.append(regOvr)
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
    
    #location_table["Kuzar 1"].address 
    #for location in world.multiworld.get_locations(world.player):
    #    logger.info(location.address)
    #    assert location.address is not None and location.item is not None
