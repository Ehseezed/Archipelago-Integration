from typing import TYPE_CHECKING

from .MapLoadingData import MapLoadingData
from ..PS1File import PS1File
from ..Sector import Sector
from ..TextFile import TextFile, apply_string_table

if TYPE_CHECKING:
    from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass

class ATTACKOut(PS1File, TextFile):
    start_sector = 2448
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 62
    end_location = start_sector_location + (sector_count * Sector.sector_size)
    dev_battle_data: bytearray
    dev_battle_offset = 0x118F8
    dev_battle: MapLoadingData

    portrait_data_table_offset = 0x016BB0
    portrait_data_count = 0x4A
    portrait_data_length = 2
    portrait_data_table_total_length = portrait_data_count * portrait_data_length
    portrait_data_table: list[int]

    job_count: int = 155

    job_names_offset: int = 0xFBAF
    job_names_length = 0x561
    job_names: list[str]
    job_names_data: bytearray



    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        self.dev_battle_data = all_data[self.dev_battle_offset:self.dev_battle_offset + MapLoadingData.data_length]
        self.dev_battle = MapLoadingData(self.dev_battle_data)

        self.portrait_data_table = list()
        for i in range(self.portrait_data_table_offset,
                       self.portrait_data_table_offset + self.portrait_data_table_total_length):
            if i % 2 == 0:
                self.portrait_data_table.append(all_data[i])

        (self.job_names,
         self.job_names_data,
         self.job_names_length) = self.init_string_list(
            self.all_data[self.job_names_offset:], self.job_count)

    def apply_dev_battle(self, map_number, entd, daytime, weather, squad_one, squad_two, music):
        self.dev_battle.map_number = map_number
        self.dev_battle.entd_entry = entd
        self.dev_battle.nighttime_flag = daytime
        self.dev_battle.weather = weather
        self.dev_battle.deployment_first = squad_one
        self.dev_battle.deployment_second = squad_two
        self.dev_battle.music = music
        self.dev_battle.apply_data()
        self.all_data[self.dev_battle_offset:self.dev_battle_offset + MapLoadingData.data_length] = self.dev_battle.raw_data

    def apply_transmooglifier_jobs(self, job_one: "TransmooglifierJobMetaclass", job_two: "TransmooglifierJobMetaclass",
                                   job_three: "TransmooglifierJobMetaclass"):
        self.job_names[0x39] = job_one.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")
        self.job_names[0x3A] = job_two.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")
        self.job_names[0x3B] = job_three.job_name.ljust(16).replace(" ", "{NL}").replace("_", "{SP}")


    def apply_transmooglifier_data(self):
        for i in range(len(self.portrait_data_table)):
            self.all_data[self.portrait_data_table_offset + (i * 2)] = self.portrait_data_table[i]
        job_name_result = apply_string_table(self.job_names)
        assert len(job_name_result) == self.job_names_length, (len(job_name_result), self.job_names_length)
        self.all_data[self.job_names_offset:self.job_names_offset + self.job_names_length] = job_name_result
