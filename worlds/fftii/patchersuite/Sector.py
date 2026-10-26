class Sector:
    header_size = 0x18
    data_size = 0x800
    error_size = 0x118
    sector_size = header_size + data_size + error_size
    header: bytearray
    data: bytearray
    error: bytearray
    all_data: bytearray

    def __init__(self, new_data):
        self.header = new_data[:self.header_size]
        self.data = bytearray(new_data[self.header_size:self.header_size + self.data_size])
        self.error = new_data[self.header_size + self.data_size:]
        self.all_data = new_data
        assert len(self.header) == self.header_size
        assert len(self.data) == self.data_size
        assert len(self.error) == self.error_size





iso_filename = "Final Fantasy Tactics (USA).bin"
entd_size = 80 * 1024
entd_sector_count = 40
event_count = 128
entd_start = 0x0875FD30