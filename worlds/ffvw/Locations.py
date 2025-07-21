from typing import List, Optional, NamedTuple, TYPE_CHECKING

from worlds.generic.Rules import CollectionRule

if TYPE_CHECKING:
    from . import FFVWWorld


# from BaseClasses import ItemClassification
#from worlds.generic.Rules import add_item_rule
#from .Items import arch_item_offset
loc_id_start = 0

LOC_TYPE_JOB = 1

"""class LocationData:
    def __init__(self, name, address = None, parent = None, area = Non"", type="Job"):
        self.name = name
        self.address = address + loc_id_start
        self.address_hex = address
        self.parent = parent
        self.area = area
        self.location_type = location_type
        self.type = type
        
location_table = {
    "Kuzar 1": LocationData(0xC00001, ItemClassification.useful, ["Jobs"]),
    "Kuzar 2": LocationData(0xC00002, ItemClassification.useful, ["Jobs"]),    
    "Kuzar 3": LocationData(0xC00003, ItemClassification.useful, ["Jobs"]),
    
    "Kuzar 4": LocationData(0xC00004, ItemClassification.useful, ["Jobs"]),
    "Kuzar 5": LocationData(0xC00005, ItemClassification.useful, ["Jobs"]),
    "Kuzar 6": LocationData(0xC00006, ItemClassification.useful, ["Jobs"]),
    
    "Kuzar 7": LocationData(0xC00007, ItemClassification.useful, ["Jobs"]),
    "Kuzar 8": LocationData(0xC00008, ItemClassification.useful, ["Jobs"]),
    "Kuzar 9": LocationData(0xC00009, ItemClassification.useful, ["Jobs"]),
    
    "Kuzar 10": LocationData(0xC0000A, ItemClassification.useful, ["Jobs"]),
    "Kuzar 11": LocationData(0xC0000B, ItemClassification.useful, ["Jobs"]),
    "Kuzar 12": LocationData(0xC0000C, ItemClassification.useful, ["Jobs"]),
}"""

EventId: Optional[int] = None

LOC_TYPE_JOB = 1

class LocationData(NamedTuple):
    name: str
    id: Optional[int]
    area: str
    location_type: int
    rule: CollectionRule = lambda state: True


def get_locations(world: Optional["FFVWWorld"]) -> List[LocationData]:
    location_data = [

        LocationData("Sealed Room, 1 O'Clock", 0xC00001, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 2 O'Clock", 0xC00002, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 3 O'Clock", 0xC00003, "Sealed Castle of Kuzar", LOC_TYPE_JOB),

        LocationData("Sealed Room, 4 O'Clock", 0xC00004, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 5 O'Clock", 0xC00005, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 6 O'Clock", 0xC00006, "Sealed Castle of Kuzar", LOC_TYPE_JOB),

        LocationData("Sealed Room, 7 O'Clock", 0xC00007, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 8 O'Clock", 0xC00008, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 9 O'Clock", 0xC00009, "Sealed Castle of Kuzar", LOC_TYPE_JOB),

        LocationData("Sealed Room, 10 O'Clock", 0xC0000A, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 11 O'Clock", 0xC0000B, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
        LocationData("Sealed Room, 12 O'Clock", 0xC0000C, "Sealed Castle of Kuzar", LOC_TYPE_JOB),
    ]
    return location_data

"""def __init__(self, player, location_data, parent=None, progression_checks_setting = 0):
    super(FFVWLocation, self).__init__(
        player, location_data.name,
        location_data.address,
        parent
    )
    self.location_data = location_data
    self.mib_flag = False"""


"""def create_location(world, player, location_data, parent=None):
    progression_checks_setting = world.worlds[player].options.progression_checks.value
    return_location = FFVWLocation(player, location_data, parent, progression_checks_setting)
    return return_location"""

""""""