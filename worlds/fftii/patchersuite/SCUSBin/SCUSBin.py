from .SCUSAbilityPrimaryData import SCUSAbilityPrimaryData
from .SCUSPoachData import SCUSPoachData
from .SCUSSkillsetData import SCUSSkillsetData
from ..PS1File import PS1File
from ..Sector import Sector
from .SCUSAbilitySecondaryData import SCUSAbilitySecondaryData
from .SCUSItemData import SCUSItemData
from .SCUSJobData import SCUSJobData
from ..Transmooglifier.SkillsetTemplates import Ability, MovementAbility
from ..Transmooglifier.TransmooglifierTemplates import TransmooglifierJobMetaclass


class SCUSBin(PS1File):
    start_sector = 24
    start_sector_location = start_sector * Sector.sector_size
    sector_count = 174
    end_location = start_sector_location + (sector_count * Sector.sector_size)

    item_data_offset = 0x0536B8
    item_data_length = 0x0C
    item_data_count = 254
    item_data_total_length = item_data_length * item_data_count
    item_datas: list[SCUSItemData]

    job_data_offset = 0x0518B8
    job_data_length = 0x30
    job_data_count = 0xA0
    job_data_total_length = job_data_length * job_data_count
    job_datas: list[SCUSJobData]

    ability_primary_data_offset = 0x04F3F0
    ability_primary_data_length = 0x08
    ability_primary_data_count = 0x200
    ability_primary_data_total_length = ability_primary_data_length * ability_primary_data_count
    ability_primary_datas: list[SCUSAbilityPrimaryData]

    ability_secondary_data_offset = 0x0503F0
    ability_secondary_data_length = 0x0E
    ability_secondary_data_count = 0x170
    ability_secondary_data_total_length = ability_secondary_data_length * ability_secondary_data_count
    ability_secondary_datas: list[SCUSAbilitySecondaryData]

    skillset_data_offset = 0x055294
    skillset_data_length = 25
    skillset_data_count = 176
    skillset_data_total_length = skillset_data_length * skillset_data_count
    skillset_datas: list[SCUSSkillsetData]

    poach_data_offset = 0x056864
    poach_data_length = 2
    poach_data_count = 48
    poach_data_total_length = poach_data_length * poach_data_count
    poach_datas: list[SCUSPoachData]

    all_data: bytearray

    def __init__(self, all_data: bytearray):
        super().__init__(all_data)

        self.item_datas = list()
        scus_item_data = all_data[self.item_data_offset:self.item_data_offset + self.item_data_total_length]
        for i in range(self.item_data_count):
            self.item_datas.append(
                SCUSItemData(scus_item_data[i * self.item_data_length:(i + 1) * self.item_data_length], i))

        self.job_datas = list()
        scus_job_data = all_data[self.job_data_offset:self.job_data_offset + self.job_data_total_length]
        for i in range(self.job_data_count):
            self.job_datas.append(
                SCUSJobData(scus_job_data[i * self.job_data_length:(i + 1) * self.job_data_length], i))

        self.ability_primary_datas = list()
        scus_ability_primary_data = all_data[self.ability_primary_data_offset:self.ability_primary_data_offset + self.ability_primary_data_total_length]
        for i in range(self.ability_primary_data_count):
            self.ability_primary_datas.append(
                SCUSAbilityPrimaryData(scus_ability_primary_data[i * self.ability_primary_data_length:(i + 1) * self.ability_primary_data_length], i))

        self.ability_secondary_datas = list()
        scus_ability_secondary_data = all_data[self.ability_secondary_data_offset:self.ability_secondary_data_offset + self.ability_secondary_data_total_length]
        for i in range(self.ability_secondary_data_count):
            self.ability_secondary_datas.append(
                SCUSAbilitySecondaryData(scus_ability_secondary_data[i * self.ability_secondary_data_length:(i + 1) * self.ability_secondary_data_length], i))

        self.skillset_datas = list()
        scus_skillset_data = all_data[self.skillset_data_offset:self.skillset_data_offset + self.skillset_data_total_length]
        for i in range(self.skillset_data_count):
            self.skillset_datas.append(
                SCUSSkillsetData(scus_skillset_data[i * self.skillset_data_length:(i + 1) * self.skillset_data_length], i))

        self.poach_datas = list()
        scus_poach_data = all_data[self.poach_data_offset:self.poach_data_offset + self.poach_data_total_length]
        for i in range(self.poach_data_count):
            self.poach_datas.append(SCUSPoachData(scus_poach_data[i * self.poach_data_length:(i + 1) * self.poach_data_length]))


    def apply_transmooglifier(self,
                              job_one: TransmooglifierJobMetaclass,
                              job_two: TransmooglifierJobMetaclass,
                              job_three: TransmooglifierJobMetaclass):
        self.ability_primary_datas[Ability.PROTECT_SPIRIT].jp_cost = 200
        self.ability_primary_datas[Ability.PROTECT_SPIRIT].chance_to_learn = 30
        self.ability_primary_datas[Ability.CLAM_SPIRIT].jp_cost = 200
        self.ability_primary_datas[Ability.CLAM_SPIRIT].chance_to_learn = 30
        self.ability_primary_datas[Ability.GATHER_POWER].jp_cost = 700
        self.ability_primary_datas[Ability.GATHER_POWER].chance_to_learn = 30
        self.ability_primary_datas[Ability.RETURN_2].jp_cost = 1200
        self.ability_primary_datas[Ability.GRAVI_2].jp_cost = 1000
        self.ability_primary_datas[MovementAbility.TELEPORT_2].jp_cost = 3500
        self.ability_primary_datas[Ability.LOSE_VOICE].jp_cost = 500
        self.ability_primary_datas[Ability.MUTE].jp_cost = 600
        self.ability_primary_datas[Ability.ENERGY].jp_cost = 250
        self.ability_primary_datas[Ability.DISPOSE].jp_cost = 450
        self.ability_primary_datas[Ability.BIO_POISON].jp_cost = 100
        self.ability_primary_datas[Ability.BIO_POISON].chance_to_learn = 70
        self.ability_primary_datas[Ability.BIO_3_UNDEAD].jp_cost = 450
        self.ability_primary_datas[Ability.DARK_HOLY].jp_cost = 850
        self.ability_primary_datas[Ability.DARK_WHISPER].jp_cost = 600
        self.ability_primary_datas[Ability.BLOOD_SUCK_HUMAN].jp_cost = 900
        self.ability_primary_datas[Ability.LIFEBREAK].jp_cost = 500
        self.ability_primary_datas[Ability.BIO_2_SLOW].jp_cost = 300
        self.ability_primary_datas[Ability.DESPAIR_2].jp_cost = 450
        self.ability_primary_datas[Ability.FLARE_2].jp_cost = 1000
        self.ability_primary_datas[Ability.MIDGAR_SWARM].jp_cost = 800
        self.ability_primary_datas[Ability.QUAKE].jp_cost = 750
        self.ability_primary_datas[Ability.MELT].jp_cost = 750
        self.ability_primary_datas[Ability.TORNADO].jp_cost = 750
        self.ability_primary_datas[Ability.GRAND_CROSS].jp_cost = 4000




        self.job_datas[0x39].apply_transmooglifier_job(job_one, 0)
        self.job_datas[0x3A].apply_transmooglifier_job(job_two, 1)
        self.job_datas[0x3B].apply_transmooglifier_job(job_three, 2)
        self.skillset_datas[0x50].apply_transmooglifier_skillset(job_one.skillset)
        self.skillset_datas[0x51].apply_transmooglifier_skillset(job_two.skillset)
        self.skillset_datas[0x52].apply_transmooglifier_skillset(job_three.skillset)


    def apply_data(self):
        new_scus_item_data: bytearray = bytearray()
        for item_data in self.item_datas:
            item_data.apply_data()
            new_scus_item_data.extend(item_data.raw_data)
        self.all_data[self.item_data_offset:self.item_data_offset + self.item_data_total_length] = new_scus_item_data

        new_scus_job_data: bytearray = bytearray()
        for job_data in self.job_datas:
            job_data.apply_data()
            new_scus_job_data.extend(job_data.raw_data)
        self.all_data[self.job_data_offset:self.job_data_offset + self.job_data_total_length] = new_scus_job_data

        new_scus_ability_primary_data: bytearray = bytearray()
        for ability_data in self.ability_primary_datas:
            ability_data.apply_data()
            new_scus_ability_primary_data.extend(ability_data.raw_data)
        self.all_data[self.ability_primary_data_offset:self.ability_primary_data_offset + self.ability_primary_data_total_length] = new_scus_ability_primary_data

        new_scus_ability_secondary_data: bytearray = bytearray()
        for ability_data in self.ability_secondary_datas:
            ability_data.apply_data()
            new_scus_ability_secondary_data.extend(ability_data.raw_data)
        self.all_data[self.ability_secondary_data_offset:self.ability_secondary_data_offset + self.ability_secondary_data_total_length] = new_scus_ability_secondary_data

        new_scus_skillset_data: bytearray = bytearray()
        for skillset_data in self.skillset_datas:
            skillset_data.apply_data()
            new_scus_skillset_data.extend(skillset_data.raw_data)
        assert len(new_scus_skillset_data) == self.skillset_data_total_length
        self.all_data[self.skillset_data_offset:self.skillset_data_offset + self.skillset_data_total_length] = new_scus_skillset_data

        new_scus_poach_data: bytearray = bytearray()
        for poach_data in self.poach_datas:
            poach_data.apply_data()
            new_scus_poach_data.extend(poach_data.raw_data)
        assert len(new_scus_poach_data) == self.poach_data_total_length
        self.all_data[self.poach_data_offset:self.poach_data_offset + self.poach_data_total_length] = new_scus_poach_data