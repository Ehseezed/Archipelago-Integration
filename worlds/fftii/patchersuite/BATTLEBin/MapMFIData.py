import json
from .MFIData import MFIData
from ...data.memory import mfi_location_id_to_map_name


class MapMFIData:
    name: str
    index: int
    mfi_datas: list[MFIData]
    raw_data: bytearray

    def __init__(self, map_mfi_data: bytearray, index: int):
        self.raw_data = bytearray()
        self.mfi_datas = list()
        for i in range(4):
            self.mfi_datas.append(MFIData(map_mfi_data[4 * i:(4 * i) + 4]))
        self.index = index
        self.name = mfi_location_id_to_map_name.get(index, f"Unknown Map {index}")

    def __repr__(self):
        return (f"{self.name}\n"
                f"--Item 1: {self.mfi_datas[0]}\n"
                f"--Item 2: {self.mfi_datas[1]}\n"
                f"--Item 3: {self.mfi_datas[2]}\n"
                f"--Item 4: {self.mfi_datas[3]}\n")

    def print_tracker_data(self):
        #print(self.name)
        jsonstuff = {
            "name": f"{self.name} MFI",
            "chest_unopened_img": "/images/items/close.png",
            "chest_opened_img": "/images/items/open.png",
            "overlay_background": "#000000",
            "access_rules": [
                " "
            ],
            "visibility_rules": [
                " "
            ],
            "map_locations": [
                {
                    "map": "World Map MFI",
                    "x": "168",
                    "y": "334",
                    "size": 12
                }
            ],
            "sections": [
                {
                    "name": f"{self.name} MFI",
                    "access_rules": [],
                    "visibility_rules": [],
                    "item_count": 4
                }
            ]
        }
        print(json.dumps(jsonstuff, indent=4) + ",")
        for i, mfi_data in enumerate(self.mfi_datas):
             pass
             #print(json.dumps(mfi_data.print_tracker_position(map_heights[self.index], i + 1, self.name), indent=4) + ",")

    def apply_data(self):
        for i in range(4):
            self.raw_data.append(self.mfi_datas[i].position_data)
            self.raw_data.append(self.mfi_datas[i].trap)
            self.raw_data.append(self.mfi_datas[i].rare_item)
            self.raw_data.append(self.mfi_datas[i].common_item)
        assert len(self.raw_data) == 16