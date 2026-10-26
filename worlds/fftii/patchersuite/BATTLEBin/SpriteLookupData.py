from ...enemyrando.Job import Job


class SpriteLookupData:
    raw_data: bytearray
    index: int
    job_name: str
    sprite_sector: int
    sprite_size: int


    def __init__(self, sprite_data: bytearray, index: int):
        self.raw_data = sprite_data
        self.index = index
        try:
            self.job_name = Job(index).name
        except ValueError:
            self.job_name = f"Unknown Job {hex(index)}"
        self.sprite_sector = int.from_bytes(sprite_data[0:4], byteorder="little")
        self.sprite_size = int.from_bytes(sprite_data[4:8], byteorder="little")

    def __repr__(self):
        return self.job_name

    def apply_data(self):
        self.raw_data[0:4] = self.sprite_sector.to_bytes(4, byteorder="little")
        self.raw_data[4:8] = self.sprite_size.to_bytes(4, byteorder="little")