from copy import deepcopy

from ..CompressibleTextFile import decompress_data, compress_data
from ..PS1File import PS1File
from ..Sector import Sector
from .ShopSellingData import ShopSellingData
from ..TextFile import TextFile, apply_string_table
from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass


class WORLDBin(PS1File, TextFile):
    start_sector = 84261
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 476
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    shop_town_data_offset: int = 0x0AD844
    shop_town_data_length: int = 2
    shop_town_data_count: int = 254
    shop_town_data_total_length = shop_town_data_length * shop_town_data_count
    shop_town_datas: list[ShopSellingData]

    portrait_data_count = 0x4A
    portrait_data_length = 2
    portrait_data_table_total_length = portrait_data_count * portrait_data_length

    portrait_data_table_offset_one = 0x0AA168
    portrait_data_table_sprite_palette: list[int]

    portrait_data_table_offset_two = 0x0AA8B8
    portrait_data_table_portrait: list[int]

    portrait_data_table_offset_three = 0x074B14
    portrait_data_table_help_portrait: list[int]

    formation_sprite_table_offset = 0xADE34
    formation_sprite_count = 0x4A
    formation_sprite_table_total_length = formation_sprite_count
    formation_sprite_table: list[int]

    job_count: int = 155

    job_names_offset: int = 0xAE938
    job_names_length: int
    job_names: list[str]
    job_names_data: bytearray

    job_change_descriptions_count = 0x4E
    job_change_descriptions_offset: int = 0xB1550
    job_change_descriptions_length: int
    job_change_descriptions: list[str]
    job_change_descriptions_data: bytearray

    job_descriptions_count = 161
    job_descriptions_offset: int = 0x920AE
    job_descriptions_length: int
    job_descriptions: list[str]
    job_descriptions_data: bytearray
    job_descriptions_datas: list[bytearray]

    skillset_count = 188

    skillset_names_offset: int = 0xAE4E8
    skillset_names_length: int
    skillset_names: list[str]
    skillset_names_data: bytearray

    transmooglifier_job_one: TransmooglifierJobMetaclass
    transmooglifier_job_two: TransmooglifierJobMetaclass
    transmooglifier_job_three: TransmooglifierJobMetaclass

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        self.init_shop_data()
        self.init_transmooglifier_data()

    def init_shop_data(self):
        self.shop_town_datas = list()
        shop_town_data = self.all_data[
            self.shop_town_data_offset:self.shop_town_data_offset + self.shop_town_data_total_length]
        for i in range(self.shop_town_data_count):
            self.shop_town_datas.append(
                ShopSellingData(shop_town_data[i * self.shop_town_data_length:(i + 1) * self.shop_town_data_length], i))


    def init_transmooglifier_data(self):
        (self.job_names,
         self.job_names_data,
         self.job_names_length) = self.init_string_list(self.all_data[self.job_names_offset:], self.job_count)

        (self.job_change_descriptions,
         self.job_change_descriptions_data,
         self.job_change_descriptions_length) = self.init_string_list(
            self.all_data[self.job_change_descriptions_offset:], self.job_change_descriptions_count)

        #decompressed_data = decompress_data(self.all_data, self.all_data[self.job_descriptions_offset:], self.job_descriptions_offset)
        (self.job_descriptions,
         self.job_descriptions_data,
         self.job_descriptions_length) = self.init_string_list(
            self.all_data[self.job_descriptions_offset:], self.job_descriptions_count)

        self.job_descriptions_datas = list()
        working_array = bytearray()
        for byte in self.job_descriptions_data[:self.job_descriptions_length]:
            working_array.append(byte)
            if byte == 0xFE:
                self.job_descriptions_datas.append(working_array.copy())
                working_array = bytearray()

        (self.skillset_names,
         self.skillset_names_data,
         self.skillset_names_length) = self.init_string_list(
            self.all_data[self.skillset_names_offset:], self.skillset_count)

        #compressed_data = bytearray(self.job_descriptions_length)
        #output_position = 0
        #compress_data(decompressed_data, len(decompressed_data), compressed_data, output_position)
        self.portrait_data_table_sprite_palette = list()
        for i in range(self.portrait_data_table_offset_one,
                       self.portrait_data_table_offset_one + self.portrait_data_table_total_length):
            if i % 2 == 0:
                self.portrait_data_table_sprite_palette.append(self.all_data[i])

        self.portrait_data_table_portrait = list()
        for i in range(self.portrait_data_table_offset_two,
                       self.portrait_data_table_offset_two + self.portrait_data_table_total_length):
            if i % 2 == 0:
                self.portrait_data_table_portrait.append(self.all_data[i])

        self.portrait_data_table_help_portrait = list()
        for i in range(self.portrait_data_table_offset_three,
                       self.portrait_data_table_offset_three + self.portrait_data_table_total_length):
            if i % 2 == 0:
                self.portrait_data_table_help_portrait.append(self.all_data[i])

        self.formation_sprite_table = list()
        for i in range(self.formation_sprite_table_offset,
                       self.formation_sprite_table_offset + self.formation_sprite_table_total_length):
            self.formation_sprite_table.append(self.all_data[i])



    def apply_shop_data(self):
        new_shop_town_data: bytearray = bytearray()
        for shop_data in self.shop_town_datas:
            shop_data.apply_data()
            new_shop_town_data.extend(shop_data.raw_data)
        self.all_data[self.shop_town_data_offset:self.shop_town_data_offset + self.shop_town_data_total_length] = new_shop_town_data

    def apply_transmooglifier_jobs(self, job_one: TransmooglifierJobMetaclass, job_two: TransmooglifierJobMetaclass, job_three: TransmooglifierJobMetaclass):
        self.transmooglifier_job_one = job_one
        self.transmooglifier_job_two = job_two
        self.transmooglifier_job_three = job_three
        self.job_names[0x39] = job_one.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")
        self.job_names[0x3A] = job_two.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")
        self.job_names[0x3B] = job_three.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")
        #self.job_descriptions[0x39] = (job_one.get_job_description_formatted().replace(" ", "{SP}")) + "{SP}"
        #self.job_descriptions[0x3A] = (job_two.get_job_description_formatted().replace(" ", "{SP}")) + "{SP}"
        #self.job_descriptions[0x3B] = (job_three.get_job_description_formatted().replace(" ", "{SP}"))
        self.skillset_names[0x50] = job_one.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x51] = job_two.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x52] = job_three.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        pass

    def apply_transmooglifier_data(self):
        self.all_data[0x458B0] = 0x4A
        for i in range(len(self.portrait_data_table_sprite_palette)):
            self.all_data[self.portrait_data_table_offset_one + (i * 2)] = self.portrait_data_table_sprite_palette[i]

        for i in range(len(self.portrait_data_table_portrait)):
            self.all_data[self.portrait_data_table_offset_two + (i * 2)] = self.portrait_data_table_portrait[i]

        for i in range(len(self.portrait_data_table_help_portrait)):
            self.all_data[self.portrait_data_table_offset_three + (i * 2)] = self.portrait_data_table_help_portrait[i]

        for i in range(len(self.formation_sprite_table)):
            self.all_data[self.formation_sprite_table_offset + i] = self.formation_sprite_table[i]

        job_name_result = apply_string_table(self.job_names)
        assert len(job_name_result) == self.job_names_length, (len(job_name_result), self.job_names_length)
        self.all_data[self.job_names_offset:self.job_names_offset + self.job_names_length] = job_name_result

        # job_change_description_result = apply_string_table(self.job_change_descriptions)
        # assert len(job_change_description_result) == self.job_change_descriptions_length, \
        #     (len(job_change_description_result), self.job_change_descriptions_length)
        # self.all_data[self.job_change_descriptions_offset:
        #               self.job_change_descriptions_offset +
        #               self.job_change_descriptions_length] = job_change_description_result

        skillset_names_result = apply_string_table(self.skillset_names)
        assert len(skillset_names_result) == self.skillset_names_length, (len(skillset_names_result), self.skillset_names_length)
        self.all_data[self.skillset_names_offset:
                      self.skillset_names_offset +
                      self.skillset_names_length] = skillset_names_result

        # job_description_result = bytearray()
        # descriptions_to_cut = [0x0A, 0x0B, 0x0E, 0x13, 0x18, 0x1C, 0x21]
        # for i, data in enumerate(self.job_descriptions_datas):
        #     if i in descriptions_to_cut:
        #         job_description_result.extend([0x0C, 0xFE])
        #     elif i == 0x39:
        #         new_data = apply_string_table([self.transmooglifier_job_one.get_job_description_formatted().replace(" ", "{SP}")])
        #         job_description_result.extend(new_data[:len(data) - 1])
        #         if job_description_result[-1] != 0xFE:
        #             job_description_result.append(0xFE)
        #     elif i == 0x3A:
        #         new_data = apply_string_table(
        #             [self.transmooglifier_job_two.get_job_description_formatted().replace(" ", "{SP}")])
        #         job_description_result.extend(new_data[:len(data) - 1])
        #         if job_description_result[-1] != 0xFE:
        #             job_description_result.append(0xFE)
        #     elif i == 0x3B:
        #         new_data = apply_string_table(
        #             [self.transmooglifier_job_three.get_job_description_formatted().replace(" ", "{SP}")])
        #         job_description_result.extend(new_data[:len(data) - 1])
        #         if job_description_result[-1] != 0xFE:
        #             job_description_result.append(0xFE)
        #     else:
        #         job_description_result.extend(data)
        # difference = self.job_descriptions_length - len(job_description_result)
        # if difference > 0:
        #     job_description_result[-1] = 0xFA
        #     for i in range(difference - 1):
        #         job_description_result.append(0xFA)
        #     job_description_result.append(0xFE)
        #job_description_result = apply_string_table(self.job_descriptions)
        #assert len(job_description_result) == self.job_descriptions_length, (len(job_description_result), self.job_descriptions_length)
        #self.all_data[self.job_descriptions_offset:self.job_descriptions_offset + self.job_descriptions_length] = job_description_result



