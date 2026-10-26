from ...data.items import item_name_lookup_by_game_id

class SCUSItemData:
    raw_data: bytearray
    item_name: str
    shop_availability: int
    shop_availability_offset: int = 0x0A

    def __init__(self, item_data: bytearray, index: int):
        self.raw_data = item_data
        self.item_name = item_name_lookup_by_game_id[index]
        self.shop_availability = item_data[self.shop_availability_offset]

    def __repr__(self):
        return f"{self.item_name} at shop level {self.shop_availability}."

    def apply_data(self):
        self.raw_data[self.shop_availability_offset] = self.shop_availability