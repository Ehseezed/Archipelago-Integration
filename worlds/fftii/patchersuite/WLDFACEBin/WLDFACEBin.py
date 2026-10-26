from .WLDFACEPortraitSection import WLDFACEPortraitSection
from ..PS1File import PS1File
from ..Sector import Sector


class WLDFACEBin(PS1File):
    start_sector = 6330
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 64
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    portrait_section_data_table_offset = 0x00
    portrait_section_data_length = 0x8000
    portrait_section_data_count = 4
    portrait_section_data_table_total_length = portrait_section_data_count * portrait_section_data_length
    portrait_section_datas: list[WLDFACEPortraitSection]

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        self.portrait_section_datas = list()
        for count in range(self.portrait_section_data_count):
            self.portrait_section_datas.append(WLDFACEPortraitSection(
                all_data[count * self.portrait_section_data_length:
                         (count + 1) * self.portrait_section_data_length]))
        pass

    def apply_data(self):
        for count in range(self.portrait_section_data_count):
            self.portrait_section_datas[count].apply_data()
            self.all_data[count * self.portrait_section_data_length:
                          (count + 1) * self.portrait_section_data_length] = self.portrait_section_datas[count].raw_data
            pass
