from collections.abc import Callable

from .Sector import Sector

class PS1FileMetaclass(type):
    start_sector: int
    start_sector_location: int
    sector_count: int
    end_location: int
    all_data: bytearray

class PS1File(object, metaclass=PS1FileMetaclass):
    start_sector = 0
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 0
    end_location = start_sector_location + (sector_count * Sector.sector_size)
    all_data: bytearray

    def __init__(self, all_data: bytearray):
        self.all_data = all_data


    def apply_data(self):
        pass

    @staticmethod
    def extract_data_and_perform_task(file_class: PS1FileMetaclass, rom_data: bytearray, patch_dict: dict, task: Callable[[PS1FileMetaclass, dict], None]):
        raw_data = rom_data[file_class.start_sector_location:file_class.end_location]
        sectors = []
        for i in range(file_class.sector_count):
            sectors.append(Sector(raw_data[i * Sector.sector_size:(i + 1) * Sector.sector_size]))
        data = bytearray()
        for sector in sectors:
            data.extend(sector.data)
        initial_length = len(data)
        file_object = file_class(data)

        task(file_object, patch_dict)

        assert len(file_object.all_data) == initial_length, (len(file_object.all_data), initial_length)
        for i, sector in enumerate(sectors):
            sector.data = file_object.all_data[i * Sector.data_size:(i + 1) * Sector.data_size]
            sector.all_data = []
            sector.all_data.extend(sector.header)
            sector.all_data.extend(sector.data)
            sector.all_data.extend(sector.error)
        new_iso_data = bytearray(rom_data)
        new_sector_data: bytearray = bytearray()
        for sector in sectors:
            new_sector_data.extend(sector.all_data)
        new_iso_data[
            file_class.start_sector_location:file_class.start_sector_location + len(new_sector_data)] = new_sector_data
        return new_iso_data