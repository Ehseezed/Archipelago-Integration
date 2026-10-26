from .TransmooglifierTemplates import TimeMaster, Hunter, Testudo, transmooglifier_lookup
from ..ATCHELPLzw.ATCHELPLzw import ATCHELPLzw
from ..ATTACKOut.ATTACKOut import ATTACKOut
from ..BUNITOut.BUNITOut import BUNITOut
from ..ENTD.ENTDEntry import ENTDEntry
from ..ENTD.Unit import Unit
from ..HELPLzw.HELPLzw import HELPLzw
from ..HELPMENUOut.HELPMENUOut import HELPMENUOut
from ..JOBSTTSOut.JOBSTTSOut import JOBSTTSOut
from ..PS1File import PS1FileMetaclass, PS1File
from ..SCUSBin.SCUSBin import SCUSBin
from ..UNITBin.UNITBin import UNITBin
from ..WLDFACEBin.WLDFACEBin import WLDFACEBin
from ..WLDHELPLzw.WLDHELPLzw import WLDHELPLzw
from ..WORLDBin.WORLDBin import WORLDBin
from ..BATTLEBin.BATTLEBin import BATTLEBin
from ..REQUIREOut.REQUIREOut import REQUIREOut
from ..WORLDLzw.WORLDLzw import WORLDLzw

def apply_transmooglifier_entd(entd_data: bytearray, patch_dict: dict):
    new_entd_entry = ENTDEntry(entd_data, "Recruits", 0x101 * ENTDEntry.total_length)
    new_entd_entry.index = 0x101
    for unit in new_entd_entry.units:
        new_unit = Unit(unit)
        new_entd_entry.unit_datas.append(new_unit)
    new_entd_entry.unit_datas[1].job = 0x39
    new_entd_entry.unit_datas[1].sprite_set = 0x39
    new_entd_entry.unit_datas[2].job = 0x3A
    new_entd_entry.unit_datas[2].sprite_set = 0x3A
    new_entd_entry.unit_datas[3].job = 0x3B
    new_entd_entry.unit_datas[3].sprite_set = 0x3B
    new_entd_entry.unit_datas[1].apply_unit_data()
    new_entd_entry.unit_datas[2].apply_unit_data()
    new_entd_entry.unit_datas[3].apply_unit_data()
    new_entd_entry.apply_data()
    return new_entd_entry

def apply_transmooglifier_scus(scus_bin: PS1FileMetaclass | SCUSBin, patch_dict: dict):
    scus_bin.apply_transmooglifier(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    scus_bin.apply_data()

def apply_transmooglifier_battle(battle_bin: PS1FileMetaclass | BATTLEBin, patch_dict: dict):
    battle_bin.sprite_lookup_datas[0x3A].sprite_sector = 58487
    battle_bin.sprite_lookup_datas[0x3A].sprite_size = 45056
    battle_bin.sprite_lookup_datas[0x3B].sprite_sector = 58487
    battle_bin.sprite_lookup_datas[0x3B].sprite_size = 45056
    battle_bin.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    battle_bin.apply_transmooglifier_data()

def apply_transmooglifier_require(require_out: PS1FileMetaclass | REQUIREOut, patch_dict: dict):
    require_out.portrait_data_table[0x08] = 0x19
    require_out.portrait_data_table[0x09] = 0x1E
    require_out.portrait_data_table[0x0B] = 0x1E
    require_out.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    require_out.apply_data()

def apply_transmooglifier_attack(attack_out: PS1FileMetaclass | ATTACKOut, patch_dict: dict):
    attack_out.portrait_data_table[0x39] = 0x08
    attack_out.portrait_data_table[0x3A] = 0x09
    attack_out.portrait_data_table[0x3B] = 0x0B
    attack_out.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    attack_out.apply_transmooglifier_data()

def apply_transmooglifier_world(world_bin: PS1FileMetaclass | WORLDBin, patch_dict: dict):
    world_bin.portrait_data_table_sprite_palette[0x39] = 0x08
    world_bin.portrait_data_table_portrait[0x39] = 0x08
    world_bin.portrait_data_table_help_portrait[0x39] = 0x08
    world_bin.formation_sprite_table[0x39] = 0x18
    world_bin.portrait_data_table_sprite_palette[0x3A] = 0x1D
    world_bin.portrait_data_table_portrait[0x3A] = 0x09
    world_bin.portrait_data_table_help_portrait[0x3A] = 0x09
    world_bin.formation_sprite_table[0x3A] = 0x1D
    world_bin.portrait_data_table_sprite_palette[0x3B] = 0x1D
    world_bin.portrait_data_table_portrait[0x3B] = 0x0B
    world_bin.portrait_data_table_help_portrait[0x3B] = 0x0B
    world_bin.formation_sprite_table[0x3B] = 0x1D
    world_bin.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    world_bin.apply_transmooglifier_data()

def apply_transmooglifier_wldface(wldface_bin: PS1FileMetaclass | WLDFACEBin, patch_dict: dict):
    wldface_bin.portrait_section_datas[0].portrait_datas[0x08] = wldface_bin.portrait_section_datas[0].portrait_datas[0x19]
    wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x08] = wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x19]

    wldface_bin.portrait_section_datas[0].portrait_datas[0x09] = wldface_bin.portrait_section_datas[0].portrait_datas[0x1E]
    wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x09] = wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x1E]

    wldface_bin.portrait_section_datas[0].portrait_datas[0x0B] = wldface_bin.portrait_section_datas[0].portrait_datas[0x1E]
    wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x0B] = wldface_bin.portrait_section_datas[0].portrait_palette_datas[0x1E]

    wldface_bin.apply_data()

def apply_transmooglifier_unitbin(unit_bin: PS1FileMetaclass | UNITBin, patch_dict: dict):
    unit_bin.sprite_datas[0x08].raw_data = unit_bin.sprite_datas[0x18].raw_data
    unit_bin.sprite_datas[0x09].raw_data = unit_bin.sprite_datas[0x1D].raw_data
    unit_bin.sprite_datas[0x0B].raw_data = unit_bin.sprite_datas[0x1D].raw_data
    unit_bin.palette_datas[0x08].raw_data = unit_bin.palette_datas[0x18].raw_data
    unit_bin.palette_datas[0x09].raw_data = unit_bin.palette_datas[0x1D].raw_data
    unit_bin.palette_datas[0x0B].raw_data = unit_bin.palette_datas[0x1D].raw_data
    unit_bin.apply_data()

def apply_transmooglifier_worldlzw(world_lzw: PS1FileMetaclass | WORLDLzw, patch_dict: dict):
    world_lzw.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    world_lzw.apply_transmooglifier_data()

def apply_transmooglifier_wldhelplzw(wldhelp_lzw: PS1FileMetaclass | WLDHELPLzw, patch_dict: dict):
    wldhelp_lzw.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    wldhelp_lzw.apply_transmooglifier_data()

def apply_transmooglifier_atchelplzw(atchelp_lzw: PS1FileMetaclass | ATCHELPLzw, patch_dict: dict):
    atchelp_lzw.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    atchelp_lzw.apply_transmooglifier_data()

def apply_transmooglifier_helplzw(helplzw: PS1FileMetaclass | HELPLzw, patch_dict: dict):
    helplzw.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    helplzw.apply_transmooglifier_data()

def apply_transmooglifier_jobsttsout(jobsttsout: PS1FileMetaclass | JOBSTTSOut, patch_dict: dict):
    jobsttsout.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    jobsttsout.apply_transmooglifier_data()

def apply_transmooglifier_bunitout(bunitout: PS1FileMetaclass | BUNITOut, patch_dict: dict):
    bunitout.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    bunitout.apply_transmooglifier_data()

def apply_transmooglifier_helpmenuout(helpmenuout: PS1FileMetaclass | HELPMENUOut, patch_dict: dict):
    helpmenuout.apply_transmooglifier_jobs(
        transmooglifier_lookup[patch_dict["Transmooglifier"][0]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][1]],
        transmooglifier_lookup[patch_dict["Transmooglifier"][2]])
    helpmenuout.apply_transmooglifier_data()

def apply_transmooglifier(rom_data: bytearray, patch_dict: dict):
    rom_data = PS1File.extract_data_and_perform_task(
        SCUSBin, rom_data, patch_dict, apply_transmooglifier_scus
    )

    rom_data = PS1File.extract_data_and_perform_task(
        BATTLEBin, rom_data, patch_dict, apply_transmooglifier_battle
    )

    rom_data = PS1File.extract_data_and_perform_task(
        REQUIREOut, rom_data, patch_dict, apply_transmooglifier_require
    )

    rom_data = PS1File.extract_data_and_perform_task(
        ATTACKOut, rom_data, patch_dict, apply_transmooglifier_attack
    )

    rom_data = PS1File.extract_data_and_perform_task(
        WORLDBin, rom_data, patch_dict, apply_transmooglifier_world
    )

    rom_data = PS1File.extract_data_and_perform_task(
        WLDFACEBin, rom_data, patch_dict, apply_transmooglifier_wldface
    )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     WORLDLzw, rom_data, patch_dict, apply_transmooglifier_worldlzw
    # )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     WLDHELPLzw, rom_data, patch_dict, apply_transmooglifier_wldhelplzw
    # )
    #
    # rom_data = PS1File.extract_data_and_perform_task(
    #     ATCHELPLzw, rom_data, patch_dict, apply_transmooglifier_atchelplzw
    # )

    rom_data = PS1File.extract_data_and_perform_task(
        UNITBin, rom_data, patch_dict, apply_transmooglifier_unitbin
    )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     HELPLzw, rom_data, patch_dict, apply_transmooglifier_helplzw
    # )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     JOBSTTSOut, rom_data, patch_dict, apply_transmooglifier_jobsttsout
    # )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     BUNITOut, rom_data, patch_dict, apply_transmooglifier_bunitout
    # )

    # rom_data = PS1File.extract_data_and_perform_task(
    #     HELPMENUOut, rom_data, patch_dict, apply_transmooglifier_helpmenuout
    # )

    return rom_data