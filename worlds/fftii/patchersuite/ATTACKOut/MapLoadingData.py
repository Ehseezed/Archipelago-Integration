class MapLoadingData:
    index: int
    map_number: int
    map_number_offset: int = 0x02
    weather: int
    weather_offset: int = 0x03
    nighttime_flag: int
    nighttime_flag_offset: int = 0x04
    music: int
    music_offset: int = 0x05
    entd_entry: int
    entd_entry_offset_lower: int = 0x07
    entd_entry_offset_upper: int = 0x08
    deployment_first: int
    deployment_first_offset_lower: int = 0x09
    deployment_first_offset_upper: int = 0x0A
    deployment_second: int
    deployment_second_offset_lower: int = 0x0B
    deployment_second_offset_upper: int = 0x0C
    raw_data: bytearray
    data_length: int = 0x20

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def apply_data(self):
        self.raw_data[self.map_number_offset] = self.map_number
        self.raw_data[self.weather_offset] = self.weather
        self.raw_data[self.nighttime_flag_offset] = self.nighttime_flag
        self.raw_data[self.music_offset] = self.music
        self.raw_data[self.entd_entry_offset_lower] = self.entd_entry % 256
        self.raw_data[self.entd_entry_offset_upper] = self.entd_entry // 256
        self.raw_data[self.deployment_first_offset_lower] = self.deployment_first % 256
        self.raw_data[self.deployment_first_offset_upper] = self.deployment_first // 256
        if self.deployment_second is not None:
            self.raw_data[self.deployment_second_offset_lower] = self.deployment_second % 256
            self.raw_data[self.deployment_second_offset_upper] = self.deployment_second // 256