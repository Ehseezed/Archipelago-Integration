from typing import TYPE_CHECKING

from .MapMFIData import MapMFIData
from ..PS1File import PS1File
from ..Sector import Sector
from .SpriteLookupData import SpriteLookupData
from ..TextFile import TextFile, apply_string_table

if TYPE_CHECKING:
    from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass

class BATTLEBin(PS1File, TextFile):
    start_sector = 1000
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 683
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    map_mfi_data_offset = 0x08EE74
    map_count = 128
    map_mfi_data_length = 16
    map_mfi_total_length = map_count * map_mfi_data_length
    map_mfi_datas: list[MapMFIData]

    sprite_lookup_data_offset = 0x02DCD4
    sprite_lookup_data_length = 8
    sprite_lookup_count = 0xA0
    sprite_lookup_total_length = sprite_lookup_data_length * sprite_lookup_count
    sprite_lookup_datas: list[SpriteLookupData]

    job_count: int = 155

    job_names_offset: int = 0xFACDA
    job_names_length = 0x593
    job_names: list[str]
    job_names_data: bytearray

    skillset_count = 188

    skillset_names_offset: int = 0xFE89F
    skillset_names_length: int
    skillset_names: list[str]
    skillset_names_data: bytearray

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)

        self.map_mfi_datas = list()
        map_mfi_data = all_data[self.map_mfi_data_offset:self.map_mfi_data_offset + self.map_mfi_total_length]
        for i in range(self.map_count):
            self.map_mfi_datas.append(
                MapMFIData(map_mfi_data[i * self.map_mfi_data_length:(i + 1) * self.map_mfi_data_length], i))

        self.sprite_lookup_datas = list()
        sprite_lookup_data = all_data[self.sprite_lookup_data_offset:
                                      self.sprite_lookup_data_offset + self.sprite_lookup_total_length]
        for i in range(self.sprite_lookup_count):
            self.sprite_lookup_datas.append(
                SpriteLookupData(sprite_lookup_data[i * self.sprite_lookup_data_length:
                                                    (i + 1) * self.sprite_lookup_data_length], i))

        (self.job_names,
         self.job_names_data,
         self.job_names_length) = self.init_string_list(
            self.all_data[self.job_names_offset:], self.job_count)
        (self.skillset_names,
         self.skillset_names_data,
         self.skillset_names_length) = self.init_string_list(
            self.all_data[self.skillset_names_offset:], self.skillset_count)

    def apply_transmooglifier_jobs(self, job_one: "TransmooglifierJobMetaclass", job_two: "TransmooglifierJobMetaclass",
                                   job_three: "TransmooglifierJobMetaclass"):
        self.job_names[0x39] = job_one.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.job_names[0x3A] = job_two.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.job_names[0x3B] = job_three.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.skillset_names[0x50] = job_one.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x51] = job_two.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x52] = job_three.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        pass

    def apply_mfi_data(self):
        for map_mfi_data in self.map_mfi_datas:
            map_mfi_data.apply_data()
            map_mfi_data_start = self.map_mfi_data_offset + (map_mfi_data.index * 16)
            map_mfi_data_end = map_mfi_data_start + 16
            self.all_data[map_mfi_data_start:map_mfi_data_end] = map_mfi_data.raw_data

    def apply_transmooglifier_data(self):
        for sprite_lookup_data in self.sprite_lookup_datas:
            sprite_lookup_data.apply_data()
            sprite_lookup_data_start = self.sprite_lookup_data_offset + (sprite_lookup_data.index * 8)
            sprite_lookup_data_end = sprite_lookup_data_start + 8
            self.all_data[sprite_lookup_data_start:sprite_lookup_data_end] = sprite_lookup_data.raw_data
        job_name_result = apply_string_table(self.job_names)
        assert len(job_name_result) == self.job_names_length, (len(job_name_result), self.job_names_length)
        self.all_data[self.job_names_offset:self.job_names_offset + self.job_names_length] = job_name_result
        skillset_names_result = apply_string_table(self.skillset_names)
        assert len(skillset_names_result) == self.skillset_names_length, (len(skillset_names_result),
                                                                          self.skillset_names_length)
        self.all_data[self.skillset_names_offset:
                      self.skillset_names_offset +
                      self.skillset_names_length] = skillset_names_result


    def test_bytes(self, data_to_test: bytearray, offset: int):
        for i in range(len(data_to_test)):
            assert data_to_test[i] == self.all_data[offset + i], (i, data_to_test[i])