class SCUSPoachData:
    raw_data: bytearray
    common_item: int
    rare_item: int

    def __init__(self, poach_data: bytearray):
        self.raw_data = poach_data
        self.common_item = poach_data[0]
        self.rare_item = poach_data[1]

    def apply_data(self):
        self.raw_data[0] = self.common_item
        self.raw_data[1] = self.rare_item