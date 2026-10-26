from enum import IntFlag, auto


class ShopSellingListOne(IntFlag):
    YARDOW = auto()
    GARILAND = auto()
    ZELTENNIA = auto()
    LIMBERRY = auto()
    LIONEL = auto()
    IGROS = auto()
    RIOVANES = auto()


class ShopSellingListTwo(IntFlag):
    UNUSED = auto()
    ZARGHIDAS = auto()
    BERVENIA = auto()
    WARJILIS = auto()
    GOUG = auto()
    ZALAND = auto()
    DORTER = auto()
    GOLAND = auto()


class ShopSellingData:
    item_name: str
    item_index: int
    raw_data: bytearray
    shop_selling_byte_one: ShopSellingListOne
    shop_selling_byte_two: ShopSellingListTwo

    def __init__(self, shop_data: bytearray, index: int):
        from ... import item_name_lookup_by_game_id
        self.raw_data = shop_data
        self.item_index = index
        self.item_name = item_name_lookup_by_game_id[index]
        self.shop_selling_byte_one = ShopSellingListOne(shop_data[0])
        self.shop_selling_byte_two = ShopSellingListTwo(shop_data[1])

    def __repr__(self):
        return f"{self.item_name} at {self.shop_selling_byte_one.name} and {self.shop_selling_byte_two.name}"

    def apply_data(self):
        self.raw_data[0] = self.shop_selling_byte_one
        self.raw_data[1] = self.shop_selling_byte_two