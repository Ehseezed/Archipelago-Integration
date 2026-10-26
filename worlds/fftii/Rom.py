import json
import logging
import os
import pkgutil

from pathlib import Path
from random import Random

import bsdiff4

import Utils
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .Options import VanillaChangesKeys
from .enemyrando.FactoryKey import FactoryKey
from .enemyrando.RandomizedMappings import factory_mappings, all_boss_shuffle_lookup
from .enemyrando.RandomizedUnitFactory import RandomizedUnitFactory
from .enemyrando.EventCodes import EventCode
from .ErrorRecalc import ErrorRecalculator
from .data import memory
from .data.locations import rare_battle_location_names, dd_location_names
from .data.memory import victory_text_offsets, rare_battles_offset, dd_battles_offset, mfi_location_id_to_name
from .data.text import split_text_into_lines
from .data.logic.FFTLocation import LocationNames
from .enemyrando.RandomizedMapping import RandomizedMapping
from .enemyrando.EventIDs import events
from .enemyrando.Job import Job
from .patchersuite.ATTACKOut.ATTACKOut import ATTACKOut
from .patchersuite.BATTLEBin.BATTLEBin import BATTLEBin
from .patchersuite.PS1File import PS1File, PS1FileMetaclass
from .patchersuite.SCUSBin.SCUSAbilitySecondaryData import FlagsFour
from .patchersuite.SCUSBin.SCUSBin import SCUSBin
from .patchersuite.SCUSBin.SCUSJobData import (EquippableItemsOne, EquippableItemsTwo,
                                               EquippableItemsThree, EquippableItemsFour)
from .patchersuite.REQUIREOut.REQUIREOut import REQUIREOut
from .patchersuite.Sector import Sector
from .patchersuite.ENTD.ENTDEntry import ENTDEntry
from .enemyrando.SourceUnit import SourceUnit
from .enemyrando.SpriteSet import SpriteSet
from .patchersuite.Transmooglifier.PatcherFunctions import apply_transmooglifier, apply_transmooglifier_entd
from .patchersuite.WLDFACEBin.WLDFACEBin import WLDFACEBin
from .patchersuite.WORLDBin.ShopSellingData import ShopSellingListTwo
from .patchersuite.ENTD.Unit import Unit
from .patchersuite.WORLDBin.WORLDBin import WORLDBin


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().fftii_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class FinalFantasyTacticsIIPatchExtension(APPatchExtension):
    game = "Final Fantasy Tactics Ivalice Island"


    @staticmethod
    def write_text_to_location(bytes_to_write, location, rom_data):
        sector_size = 0x930
        data_start = 0x18
        data_size = 0x800
        header_size = 0x18
        ec_size = 0x118
        other_size = header_size + ec_size

        current_sector = location // sector_size
        current_sector_start = current_sector * sector_size
        offset_in_sector = location % sector_size
        data_end = current_sector_start + data_start + data_size

        current_offset = location
        while len(bytes_to_write) > 0:
            rom_data[current_offset] = bytes_to_write.pop(0)
            current_offset += 1
            if current_offset >= data_end:
                current_offset = data_end + other_size
                current_sector = current_offset // sector_size
                current_sector_start = current_sector * sector_size
                data_end = current_sector_start + data_start + data_size
        pass

    @staticmethod
    def apply_enemy_rando(patch_dict, rom_data, seed, randomize_gariland, boss_shuffle, transmooglifier):
        mapping_dict: dict[EventCode, list[RandomizedMapping]] = {}
        for key, value in patch_dict.items():
            new_list = []
            for entry in value:
                new_list.append(RandomizedMapping.from_json(entry))
            mapping_dict[EventCode(int(key))] = new_list

        randomized_factories: dict[FactoryKey, RandomizedUnitFactory] = {
            job: RandomizedUnitFactory(mapping, Random(seed)) for job, mapping in factory_mappings.items()
        }


        entd_size = 80 * 1024
        entd_sector_count = 40
        event_count = 128
        entd_start = 0x0875FD30

        total_entd_length = entd_sector_count * Sector.sector_size
        entd_list: list[bytearray] = list()
        all_entd_sectors: list[Sector] = list()
        for i in range(4):
            start = entd_start + (i * total_entd_length)
            entd = rom_data[start:start + total_entd_length]
            entd_sectors = []
            for j in range(entd_sector_count):
                new_sector = Sector(entd[j * Sector.sector_size:(j + 1) * Sector.sector_size])
                entd_sectors.append(new_sector)
                all_entd_sectors.append(new_sector)
            entd_data = bytearray()
            for sector in entd_sectors:
                entd_data.extend(sector.data)
            entd_list.append(entd_data)
        full_entd = bytearray()
        for entd in entd_list:
            full_entd.extend(entd)
        used_units = []
        entd_entries: list[ENTDEntry] = list()
        for i in range(0x1D5):
            if i == 0x101:
                if len(transmooglifier) > 0:
                    entd_data = full_entd[0x101 * ENTDEntry.total_length:0x102 * ENTDEntry.total_length]
                    new_entd_entry = apply_transmooglifier_entd(entd_data, patch_dict)
                    entd_entries.append(new_entd_entry)
            if i in events.keys():
                mapping_list: list[RandomizedMapping] = []
                if EventCode(i) in mapping_dict.keys():
                    mapping_list = mapping_dict[EventCode(i)]
                if i == 0x184 and randomize_gariland == 0:
                    mapping_list = []
                entd_data = full_entd[i * ENTDEntry.total_length:(i + 1) * ENTDEntry.total_length]
                new_entd_entry = ENTDEntry(entd_data, events[i], i * ENTDEntry.total_length)
                new_entd_entry.index = i
                for unit in new_entd_entry.units:
                    if unit[0] > 0 and unit[1] > 0:
                        new_unit = Unit(unit)
                        if new_unit.job != 0:
                            used_units.append(new_unit.job)
                    else:
                        new_unit = Unit(unit)
                    new_entd_entry.unit_datas.append(new_unit)
                for unit in new_entd_entry.unit_datas:
                    if unit.sprite_set > 0:
                        source_unit = SourceUnit(SpriteSet(unit.sprite_set), Job(unit.job), unit.gender)
                        if len(mapping_list) > 0:
                            for mapping_entry in mapping_list:
                                if source_unit == mapping_entry.source_unit:
                                    destination_unit = None
                                    try:
                                        destination_unit = randomized_factories[mapping_entry.destination_unit].get_unit(
                                            mapping_entry.battle_level)
                                    except KeyError:
                                        if boss_shuffle == 1 or boss_shuffle == 3:
                                            try:
                                                destination_unit = all_boss_shuffle_lookup[
                                                    mapping_entry.destination_unit]
                                            except KeyError:
                                                destination_unit = randomized_factories[
                                                    mapping_entry.destination_unit].get_unit(
                                                    mapping_entry.battle_level)
                                    if destination_unit is None:
                                        raise RuntimeError("Invalid enemy randomization.")
                                    if i == 0x193: # Dorter 2 exclude Gafgarion.
                                        if unit.job == Job.DARK_KNIGHT_GUEST:
                                            continue
                                    if i == 0x194: # Araguay Woods exclude Gafgarion and Boco.
                                        if unit.job == Job.DARK_KNIGHT_GUEST:
                                            continue
                                        if unit.job == Job.YELLOW_CHOCOBO:
                                            continue
                                    unit.set_new_data(destination_unit)
                                    if mapping_entry.boss_unit:
                                        current_level = unit.level
                                        new_level = current_level + mapping_entry.battle_level
                                        if current_level >= 100:
                                            new_level = min(199, new_level)
                                        else:
                                            new_level = min(99, new_level)
                                        unit.level = new_level
                                    unit.apply_unit_data()
                new_entd_entry.apply_data()
                entd_entries.append(new_entd_entry)
        new_full_entd: bytearray = full_entd.copy()
        for entd_entry in entd_entries:
            start_location: int = entd_entry.location
            end_location: int = entd_entry.location + ENTDEntry.total_length
            new_full_entd[start_location:end_location] = entd_entry.all_data
        new_all_entd_sectors: list[Sector] = list()
        for sector in all_entd_sectors:
            new_all_entd_sectors.append(Sector(sector.all_data))
        for i in range(len(new_full_entd)):
            # assert new_full_entd[i] == full_entd[i], (i, new_full_entd[i], full_entd[i])
            sector_number: int = i // 2048
            new_all_entd_sectors[sector_number].data[i % 2048] = new_full_entd[i]
        for i in range(len(all_entd_sectors)):
            for j in range(len(all_entd_sectors[i].data)):
                pass
                # assert all_entd_sectors[i].data[j] == new_all_entd_sectors[i].data[j]
            new_all_data: bytearray = bytearray()
            new_all_data.extend(new_all_entd_sectors[i].header)
            new_all_data.extend(new_all_entd_sectors[i].data)
            new_all_data.extend(new_all_entd_sectors[i].error)
            new_all_entd_sectors[i].all_data = new_all_data
        new_iso_data = bytearray(rom_data)
        new_sector_data: bytearray = bytearray()
        for sector in new_all_entd_sectors:
            new_sector_data.extend(sector.all_data)
        new_iso_data[entd_start:entd_start + len(new_sector_data)] = new_sector_data
        return new_iso_data

    @staticmethod
    def apply_mfi_rando(battle_bin: PS1FileMetaclass | BATTLEBin, patch_dict: dict):
        for map_mfi_data in battle_bin.map_mfi_datas:
            if map_mfi_data.index in mfi_location_id_to_name.keys():
                #map_mfi_data.print_tracker_data()
                new_mfi_data = patch_dict["MFIRandoMapping"][str(map_mfi_data.index)]
                for i in range(4):
                    map_mfi_data.mfi_datas[i].common_item = new_mfi_data[i]["Common"]
                    map_mfi_data.mfi_datas[i].rare_item = new_mfi_data[i]["Rare"]
        battle_bin.apply_mfi_data()

    @staticmethod
    def apply_poach_reward_rando(scus_bin: PS1FileMetaclass | SCUSBin, patch_dict: dict):
        for i, poach_data in enumerate(scus_bin.poach_datas):
            scus_bin.poach_datas[i].common_item = patch_dict["PoachRewards"][i]["Common"]
            scus_bin.poach_datas[i].rare_item = patch_dict["PoachRewards"][i]["Rare"]
        scus_bin.apply_data()

    @staticmethod
    def apply_improved_shops_scus(scus_bin: PS1FileMetaclass | SCUSBin, patch_dict: dict):
        better_shop_dict = {
            "Asura Knife": 1,
            "Javelin": 1
        }
        for item_data in scus_bin.item_datas:
            if item_data.item_name in better_shop_dict.keys():
                item_data.shop_availability = better_shop_dict[item_data.item_name]
        scus_bin.apply_data()

    @staticmethod
    def apply_dev_battle(attack_out: PS1FileMetaclass | ATTACKOut, patch_dict: dict):
        random = Random(patch_dict["Seed"])
        maps = {
            "Igros": 0x09,
            "Warjilis": 0x2A,
            "Riovanes": 0x06,
            "Nelveska": 0x46,
            "Murond": 0x32,
            "Orbonne": 0x38,
            "Fort": 0x73,
            "Tutorial": 0x66
        }
        entd = {
            "Igros": 0x104,
            "Warjilis": 0x105,
            "Riovanes": 0x106,
            "Nelveska": 0x107,
            "Murond": 0x108,
            "Orbonne": 0x109,
            "Fort": 0x10A,
            "Tutorial": 0x10B
        }
        daytime = {
            "Igros": 1,
            "Warjilis": 0,
            "Riovanes": 1,
            "Nelveska": 0,
            "Murond": 1,
            "Orbonne": 1,
            "Fort": 1,
            "Tutorial": 1
        }
        squad_1 = {
            "Igros": 0x14E,
            "Warjilis": 0x14F,
            "Riovanes": 0x150,
            "Nelveska": 0x151,
            "Murond": 0x152,
            "Orbonne": 0x154,
            "Fort": 0x155,
            "Tutorial": 0x157
        }
        squad_2 = {
            "Igros": None,
            "Warjilis": None,
            "Riovanes": None,
            "Nelveska": None,
            "Murond": 0x153,
            "Orbonne": None,
            "Fort": 0x156,
            "Tutorial": None
        }
        music = {
            "Battle on the Bridge": 0x4D,
            "Ultima, the Perfect Body": 0x13,
            "Apoplexy Extended": 0x63,
            "Trisection": 0x0C,
            "Fighting 2": 0x52,
            "Under the Stars": 0x09,
            "Antidote": 0x0D,
            "Treasure": 0x26,
            "Ultima, the Nice Body": 0x12,
            "Decisive Battle": 0x07,
            "Fighting 1": 0x51
        }
        chosen_map_key = random.choice(list(maps.keys()))
        chosen_map = maps[chosen_map_key]
        chosen_entd = entd[chosen_map_key]
        chosen_daytime = daytime[chosen_map_key]
        chosen_daytime = random.randrange(0, chosen_daytime + 1)
        chosen_weather = random.randrange(0, 5)
        chosen_squad_1 = squad_1[chosen_map_key]
        chosen_squad_2 = squad_2[chosen_map_key]
        chosen_music_key = random.choice(list(music.keys()))
        chosen_music = music[chosen_music_key]
        attack_out.apply_dev_battle(
            chosen_map,
            chosen_entd,
            chosen_daytime,
            chosen_weather,
            chosen_squad_1,
            chosen_squad_2,
            chosen_music)
        attack_out.apply_data()

    @staticmethod
    def apply_job_adjustments(scus_bin: PS1FileMetaclass | SCUSBin, patch_dict: dict):
        if VanillaChangesKeys.SWORDSKILL_SWORDS in patch_dict["VanillaChanges"]:
            jobs_to_adjust = {
                Job.HOLY_KNIGHT_DELITA: [EquippableItemsOne.KNIFE, EquippableItemsTwo.FLAIL],
                Job.ARC_KNIGHT_DELITA: [EquippableItemsOne.KNIFE, EquippableItemsTwo.FLAIL],
                Job.HOLY_SWORDSMAN: [EquippableItemsOne.KATANA, EquippableItemsOne.NINJA_BLADE],
                Job.TEMPLE_KNIGHT: [EquippableItemsOne.KNIFE],
                Job.DIVINE_KNIGHT_MELIADOUL: [EquippableItemsTwo.CROSSBOW, EquippableItemsTwo.POLEARM],
                Job.DIVINE_KNIGHT_MELIADOUL_ENEMY: [EquippableItemsTwo.CROSSBOW]
            }
            for job_data in scus_bin.job_datas:
                try:
                    job = Job(job_data.job_index)
                    if job in jobs_to_adjust.keys():
                        adjustments = jobs_to_adjust[job]
                        for adjustment in adjustments:
                            if isinstance(adjustment, EquippableItemsOne):
                                job_data.equip_one = job_data.equip_one & ~adjustment
                            elif isinstance(adjustment, EquippableItemsTwo):
                                job_data.equip_two = job_data.equip_two & ~adjustment
                            elif isinstance(adjustment, EquippableItemsThree):
                                job_data.equip_three = job_data.equip_three & ~adjustment
                            elif isinstance(adjustment, EquippableItemsFour):
                                job_data.equip_four = job_data.equip_four & ~adjustment
                except ValueError:
                    continue
        if VanillaChangesKeys.MATERIA_BLADE in patch_dict["VanillaChanges"]:
            for i in range(0x101, 0x109): # Braver through Cherry Blossom
                current_flags = scus_bin.ability_secondary_datas[i].flags_four
                new_flags = current_flags & ~FlagsFour.MATERIA_BLADE
                new_flags = new_flags | FlagsFour.SWORD
                scus_bin.ability_secondary_datas[i].flags_four = new_flags
        if VanillaChangesKeys.RANDOM_MAGIC in patch_dict["VanillaChanges"]:
            for i in range(0xA9, 0xB5): # All Truth and Untruth skills
                scus_bin.ability_secondary_datas[i].x_var = 10
            scus_bin.ability_secondary_datas[0xFF].x_var = 10 # Holy Bracelet
        scus_bin.apply_data()

    @staticmethod
    def apply_improved_shops_world(world_bin: PS1FileMetaclass | WORLDBin, patch_dict: dict):
        from . import item_name_lookup_by_game_id
        for i in range(len(item_name_lookup_by_game_id)):
            item_name = item_name_lookup_by_game_id[i]
            if item_name == "Romanda Gun" or item_name == "Mythril Gun":
                world_bin.shop_town_datas[i].shop_selling_byte_two |= (ShopSellingListTwo.DORTER |
                                                                       ShopSellingListTwo.WARJILIS |
                                                                       ShopSellingListTwo.ZARGHIDAS)
        world_bin.apply_shop_data()

    @staticmethod
    def apply_mfi_tile_hack(battle_bin: PS1FileMetaclass | BATTLEBin, patch_dict: dict):
        if patch_dict["MFILogic"] == 2:
            battle_bin.all_data[0xF5398:0xF5398 + 4] = bytearray(4)
            battle_bin.all_data[0xF53A0:0xF53A0 + 8] = bytearray(8)

    @staticmethod
    def patch_bin(caller, iso, placement_file):
        patch_dict: dict = json.loads(caller.get_file(placement_file))
        if patch_dict["APJobs"] == 1:
            base_patch = pkgutil.get_data(__name__, "fftiiapjobs.bsdiff4")
        else:
            base_patch = pkgutil.get_data(__name__, "fftiivanillajobs.bsdiff4")
        rom_data = bsdiff4.patch(iso, base_patch)
        rom_data: bytearray = bytearray(rom_data)

        if "RareBattles" in patch_dict.keys():
            if patch_dict["RareBattles"] == 1:
                address, bit = memory.yaml_options["RareBattles"]
                rom_data[address] = rom_data[address] | bit
        if patch_dict["Sidequests"] == 1:
            address, bit = memory.yaml_options["Sidequests"]
            rom_data[address] = rom_data[address] | bit
        if patch_dict["FinalBattles"] == 1:
            address, bit = memory.yaml_options["FinalBattles"]
            rom_data[address] = rom_data[address] | bit
        if "EXPMultiplier" in patch_dict.keys():
            exp_mult_values = [0x00, 0x40, 0x80]
            exp_mult_value = exp_mult_values[patch_dict["EXPMultiplier"]]
            address = memory.yaml_options["EXPMultiplier"]
            rom_data[address] = exp_mult_value
        if "JPMultiplier" in patch_dict.keys():
            exp_mult_values = [0x00, 0x40, 0x80]
            exp_mult_value = exp_mult_values[patch_dict["JPMultiplier"]]
            address = memory.yaml_options["JPMultiplier"]
            rom_data[address] = exp_mult_value
        if "MFILogic" in patch_dict.keys():
            if patch_dict["MFILogic"] == 1:
                address = memory.yaml_options["MFIChemistInnate"]
                rom_data[address] = 0xFD
                rom_data[address + 1] = 0x01
            if patch_dict["MFILogic"] == 2:
                address = memory.yaml_options["MFIBlueTeamInnate"]
                rom_data[address] = 0x00
                rom_data[address + 1] = 0x00
                rom_data[address + 2] = 0x00
                rom_data[address + 3] = 0x00

        location_dict = patch_dict["LocationDict"]
        for location, text in location_dict.items():
            if location in victory_text_offsets:
                text_lines, byte_lines = split_text_into_lines(text)
                all_bytes = []
                for byte_line in byte_lines:
                    all_bytes.extend(byte_line)
                if isinstance(victory_text_offsets[location], list):
                    for offset in victory_text_offsets[location]:
                        bytes_to_write = all_bytes.copy()
                        FinalFantasyTacticsIIPatchExtension.write_text_to_location(bytes_to_write, offset, rom_data)
                else:
                    offset = victory_text_offsets[location]
                    FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_bytes, offset, rom_data)


                #rom_data[offset:offset + len(all_bytes)] = all_bytes
        if LocationNames.MANDALIA_RARE.value in location_dict.keys():
            all_rare_bytes = []
            for location in rare_battle_location_names:
                text = location_dict[location]
                text_lines, byte_lines = split_text_into_lines(text)
                for byte_line in byte_lines:
                    all_rare_bytes.extend(byte_line)
            FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_rare_bytes, rare_battles_offset, rom_data)
        if LocationNames.NOGIAS_SIDEQUEST.value in location_dict.keys():
            all_dd_bytes = []
            for location in dd_location_names:
                text = location_dict[location]
                text_lines, byte_lines = split_text_into_lines(text)
                for byte_line in byte_lines:
                    all_dd_bytes.extend(byte_line)
            FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_dd_bytes, dd_battles_offset, rom_data)

        if "MFIRandoMapping" in patch_dict.keys():
            rom_data = PS1File.extract_data_and_perform_task(
                BATTLEBin,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_mfi_rando)

        if "PoachRewards" in patch_dict.keys():
            rom_data = PS1File.extract_data_and_perform_task(
                SCUSBin,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_poach_reward_rando
            )

        rom_data = FinalFantasyTacticsIIPatchExtension.apply_enemy_rando(
            patch_dict["EnemyRandoMapping"],
            rom_data,
            patch_dict["Seed"],
            patch_dict["RandomizeGariland"],
            patch_dict["BossShuffle"],
            patch_dict["Transmooglifier"]
        )

        if VanillaChangesKeys.IMPROVED_SHOPS in patch_dict["VanillaChanges"]:
            rom_data = PS1File.extract_data_and_perform_task(
                SCUSBin,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_improved_shops_scus
            )
            rom_data = PS1File.extract_data_and_perform_task(
                WORLDBin,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_improved_shops_world
            )

        if True:
            rom_data = PS1File.extract_data_and_perform_task(
                ATTACKOut,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_dev_battle
            )

        if True:
            rom_data = PS1File.extract_data_and_perform_task(
                SCUSBin,
                rom_data,
                patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_job_adjustments
            )

        if True:
            rom_data = PS1File.extract_data_and_perform_task(
                BATTLEBin, rom_data, patch_dict,
                FinalFantasyTacticsIIPatchExtension.apply_mfi_tile_hack
            )

        if len(patch_dict["Transmooglifier"]) > 0:
            rom_data = apply_transmooglifier(rom_data, patch_dict)

        rom_name_text = patch_dict["RomName"]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        rom_data[memory.rom_name_location:memory.rom_name_location + 20] = bytes(rom_name[:20])
        rom_data[memory.volume_name_location:memory.volume_name_location + 20] = bytes(rom_name[:20])
        seed_hash = int(patch_dict["SeedHash"])
        seed_hash_bytes = seed_hash.to_bytes(2)
        rom_data[memory.seed_hash_location:memory.seed_hash_location + 2] = bytes(seed_hash_bytes)

        return rom_data



class FinalFantasyTacticsIIProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Final Fantasy Tactics Ivalice Island"
    hash = "b156ba386436d20fd5ed8d37bab6b624"
    patch_file_ending = ".apfftii"
    result_file_ending = ".cue"

    procedure = [
        ("patch_bin", ["patch_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".cue"):
            os.unlink(file_name + ".cue")
        if os.path.exists(file_name + "patched" + ".bin"):
            os.unlink(file_name + "patched" + ".bin")

        super().patch(target)
        os.rename(target, file_name + "patched" + ".bin")
        error_recalculator = ErrorRecalculator(calculate_form_2_edc=False)
        stats = error_recalculator.recalc(target_file=Path(file_name + "patched" + ".bin"),
                                          base_file=get_settings().fftii_options.rom_file)
        print(
            f"{stats.identical_sectors} identical sectors out of {stats.total_sectors()}, {stats.recalc_sectors} sectors recalculated")
        print(f"{stats.edc_blocks_computed} EDC blocks computed, {stats.ecc_blocks_generated} ECC blocks generated")

        cue_text = f'FILE "{file_name}patched.bin" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00'
        with open(file_name + ".cue", "w") as cue_file:
            cue_file.write(cue_text)