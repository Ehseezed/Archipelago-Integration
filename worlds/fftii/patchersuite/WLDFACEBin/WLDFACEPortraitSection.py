from .WLDFACEPortrait import WLDFACEPortrait
from .WLDFACEPortraitPalette import WLDFACEPortraitPalette


class WLDFACEPortraitSection:
    raw_data: bytearray

    portrait_count: int = 40
    portrait_height: int = 48
    portrait_width: int = 16

    portrait_data_table_offset: int = 0x00
    portrait_data_row_count: int = 240
    portrait_data_row_length: int = 128
    portrait_data_table_total_length: int = portrait_data_row_count * portrait_data_row_length
    portrait_datas: list[WLDFACEPortrait]

    portrait_palette_data_table_offset: int = portrait_data_table_total_length
    portrait_palette_data_count: int = portrait_count
    portrait_palette_data_length: int = 32
    portrait_palette_data_table_total_length: int = portrait_palette_data_count * portrait_palette_data_length
    portrait_palette_datas: list[WLDFACEPortraitPalette]

    def __init__(self, raw_data: bytearray):
        self.raw_data = raw_data
        self.portrait_datas = list()
        self.portrait_palette_datas = list()
        for count in range(self.portrait_count):
            portrait_column = count % 8
            portrait_row = count // 8
            start_position = portrait_column * self.portrait_width
            start_position += self.portrait_height * self.portrait_data_row_length * portrait_row
            new_portrait = WLDFACEPortrait()
            for row in range(self.portrait_height):
                row_position = start_position + (row * self.portrait_data_row_length)
                new_portrait.raw_data.extend(self.raw_data[row_position:row_position + self.portrait_width])
            self.portrait_datas.append(new_portrait)
            new_portrait_palette = WLDFACEPortraitPalette(
                self.raw_data[(count * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset:
                              ((count + 1) * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset])
            self.portrait_palette_datas.append(new_portrait_palette)
        pass

    def apply_data(self):
        for count in range(self.portrait_count):
            portrait_column = count % 8
            portrait_row = count // 8
            start_position = portrait_column * self.portrait_width
            start_position += self.portrait_height * self.portrait_data_row_length * portrait_row
            for row in range(self.portrait_height):
                row_position = start_position + (row * self.portrait_data_row_length)
                new_raw_data = (self.portrait_datas[count].raw_data[row * self.portrait_width:((row + 1) * self.portrait_width)])
                self.raw_data[row_position:row_position + self.portrait_width] = new_raw_data
            self.raw_data[(count * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset:
                          ((count + 1) * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset] = self.portrait_palette_datas[count].raw_data
        pass