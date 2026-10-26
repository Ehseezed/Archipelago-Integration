from ..CompressibleTextFile import CompressibleTextFile
from ..PS1File import PS1File
from ..Sector import Sector
from ..TextFile import apply_string_table
from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass

class WORLDLzw(PS1File, CompressibleTextFile):
    start_sector = 7128
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 29
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    job_count: int = 155

    job_names_offset = 0x86
    job_names_length = 0x593
    job_names: list[str]
    job_names_data: bytearray

    skillset_count = 188

    skillset_names_offset: int = 0x7850
    skillset_names_length: int
    skillset_names: list[str]
    skillset_names_data: bytearray

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        (self.job_names,
         self.job_names_data,
         self.job_names_length) = self.init_string_list_compressible(
            self.all_data[self.job_names_offset:], self.job_count, self.job_names_offset)
        (self.skillset_names,
         self.skillset_names_data,
         self.skillset_names_length) = self.init_string_list_compressible(
            self.all_data[self.skillset_names_offset:], self.skillset_count, self.skillset_names_offset)
        pass

    def apply_transmooglifier_jobs(self, job_one: TransmooglifierJobMetaclass, job_two: TransmooglifierJobMetaclass, job_three: TransmooglifierJobMetaclass):
        self.job_names[0x39] = job_one.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.job_names[0x3A] = job_two.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.job_names[0x3B] = job_three.job_name.ljust(16).replace(" ", "{SP}").replace("_", "{SP}")
        self.skillset_names[0x50] = job_one.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x51] = job_two.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        self.skillset_names[0x52] = job_three.skillset.skillset_name.ljust(20).replace(" ", "{SP}")
        pass

    def apply_transmooglifier_data(self):
        job_name_result = apply_string_table(self.job_names)
        assert len(job_name_result) == self.job_names_length, (len(job_name_result), self.job_names_length)
        self.all_data[self.job_names_offset:self.job_names_offset + self.job_names_length] = job_name_result

        skillset_names_result = apply_string_table(self.skillset_names)
        #self.test_bytes(skillset_names_result, self.skillset_names_offset)
        assert len(skillset_names_result) == self.skillset_names_length, (len(skillset_names_result), self.skillset_names_length)
        self.all_data[
            self.skillset_names_offset:self.skillset_names_offset + self.skillset_names_length] = skillset_names_result