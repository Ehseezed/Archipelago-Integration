from ..CompressibleTextFile import CompressibleTextFile
from ..PS1File import PS1File
from ..Sector import Sector
from ..TextFile import apply_string_table
from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass

class JOBSTTSOut(PS1File, CompressibleTextFile):
    start_sector = 2384
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 56
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    job_count: int = 155

    job_descriptions_offset = 0x6594
    job_descriptions_length: int
    job_descriptions: list[str]
    job_descriptions_data: bytearray

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)
        (self.job_descriptions,
         self.job_descriptions_data,
         self.job_descriptions_length) = self.init_string_list_compressible(
            self.all_data[self.job_descriptions_offset:], self.job_count, self.job_descriptions_offset)
        pass

    def apply_transmooglifier_jobs(self, job_one: TransmooglifierJobMetaclass, job_two: TransmooglifierJobMetaclass, job_three: TransmooglifierJobMetaclass):
        self.job_descriptions[0x39] = job_one.get_job_description_formatted().replace(" ", "{SP}")
        self.job_descriptions[0x3A] = job_two.get_job_description_formatted().replace(" ", "{SP}")
        self.job_descriptions[0x3B] = job_three.get_job_description_formatted().replace(" ", "{SP}")
        pass

    def apply_transmooglifier_data(self):
        job_description_result = apply_string_table(self.job_descriptions)
        assert len(job_description_result) == self.job_descriptions_length, (len(job_description_result), self.job_descriptions_length)
        self.all_data[self.job_descriptions_offset:self.job_descriptions_offset + self.job_descriptions_length] = job_description_result

