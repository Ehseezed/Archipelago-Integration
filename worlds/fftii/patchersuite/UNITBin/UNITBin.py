from .UnitPalette import UnitPalette
from .UnitSection import UnitSection
from .UnitSprite import UnitSprite
from ..PS1File import PS1File
from ..Sector import Sector

sprites_per_row = 10
sprite_width = 12
sprite_height = 40
bytes_per_row = 128
initial_palette_position = 0xF000
palette_length = 32



class UNITBin(PS1File):
    start_sector = 5739
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 32
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    sprite_section_data_table_offset = 0x00
    sprite_section_data_length = 0x500
    sprite_section_data_count = 6
    sprite_section_data_table_total_length = 0x10000
    sprite_section_datas: list[UnitSection]

    sprite_datas: list[UnitSprite]
    palette_datas: list[UnitPalette]

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        self.sprite_datas = list()
        self.palette_datas = list()
        for i in range(60):
            self.sprite_datas.append(self.get_sprite_data(i))
            self.palette_datas.append(self.get_palette_data(i))


    def get_sprite_data(self, index: int):
        sprite_column = index % sprites_per_row
        sprite_row = index // sprites_per_row

        start_position = sprite_column * sprite_width
        start_position += sprite_row * bytes_per_row * sprite_height
        new_raw_data = bytearray()
        for row in range(sprite_height):
            row_position = start_position + (row * bytes_per_row)
            new_raw_data.extend(self.all_data[row_position:row_position + sprite_width])
        return UnitSprite(new_raw_data)
        #new_portrait_palette = WLDFACEPortraitPalette(
        #    self.raw_data[(count * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset:
        #                  ((count + 1) * self.portrait_palette_data_length) + self.portrait_palette_data_table_offset])
        #self.portrait_palette_datas.append(new_portrait_palette)

    def get_palette_data(self, index: int):
        new_raw_data = self.all_data[initial_palette_position + (index * palette_length):
                                     initial_palette_position + ((index + 1) * palette_length)]
        return UnitPalette(new_raw_data)
        pass


    def apply_data(self):
        for index in range(60):
            sprite_column = index % sprites_per_row
            sprite_row = index // sprites_per_row
            start_position = sprite_column * sprite_width
            start_position += sprite_row * bytes_per_row * sprite_height
            for row in range(sprite_height):
                row_position = start_position + (row * bytes_per_row)
                new_raw_data = (self.sprite_datas[index].raw_data[row * sprite_width:((row + 1) * sprite_width)])
                self.all_data[row_position:row_position + sprite_width] = new_raw_data
            self.all_data[initial_palette_position + (index * palette_length):
                          initial_palette_position + ((index + 1) * palette_length)] = self.palette_datas[index].raw_data
        pass
