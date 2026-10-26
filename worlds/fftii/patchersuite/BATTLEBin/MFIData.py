from ...data.items import item_name_lookup_by_game_id


class MFIData:
    position_data_offset: int = 0x00
    trap_data_offset: int = 0x01
    rare_item_offset: int = 0x02
    common_item_offset: int = 0x03
    position_data: int = None
    position_x: int = None
    position_y: int = None
    trap: int = None
    rare_item: int = None
    common_item: int = None

    def __init__(self, mfi_data: bytearray):
        self.position_data = mfi_data[self.position_data_offset]
        self.position_x = (self.position_data & 0b11110000) >> 4
        self.position_y = self.position_data & 0b00001111
        self.tracker_x = (self.position_x * 28) + 14
        self.tracker_y = (self.position_y * 28) + 14
        self.trap = mfi_data[self.trap_data_offset]
        self.rare_item = mfi_data[self.rare_item_offset]
        self.common_item = mfi_data[self.common_item_offset]

    def __repr__(self):
        return (f"X: {self.position_x}, Y: {self.position_y}, "
                f"Common: {item_name_lookup_by_game_id[self.common_item]}, "
                f"Rare: {item_name_lookup_by_game_id[self.rare_item]}"
                )

    def print_tracker_position(self, offset, index, name):
        return {
            "name": f"{name} MFI {index}",
            "overlay_background": "#000000",
            "access_rules": [" "],
            "sections": [
                {
                    "name": f"MFI {index}",
                    "access_rules": [],
                    "visibility_rules": [],
                    "item_count": 1
                }
            ],
            "map_locations": [
                {
                    "map": f"{name}",
                    "x": f"{self.tracker_x}",
                    "y": f"{(offset * 28) - self.tracker_y}"
                }
            ]
        }