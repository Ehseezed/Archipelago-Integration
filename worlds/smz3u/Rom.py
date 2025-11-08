import hashlib
import json
import logging
import os
from json import JSONDecodeError
from typing import Optional, cast

import Utils
from Utils import read_snes_rom
from settings import get_settings
from worlds.Files import APProcedurePatch, APPatchExtension, APTokenMixin, APTokenTypes
from worlds.smz3u.ips import IPS_Patch

SMJUHASH = '21f3e98df4780ee1c667b84e57d88675'
LTTPJPN10HASH = '03a63945398191337e896e5771f77173'
ROM_PLAYER_LIMIT = 256

world_folder = os.path.dirname(__file__)
logger = logging.getLogger("SMZ3")

class SMZ3UPatchExtensions(APPatchExtension):
    game = "SMZ3U"

    @staticmethod
    def apply_basepatch(caller: APProcedurePatch, _rom: bytes) -> bytes:
        extra_patches_file = "extra_patches.json"
        error = False

        try:
            json.loads(caller.get_file(extra_patches_file))
        except JSONDecodeError:
            error = True
        except UnicodeDecodeError:
            error = True

        if error:
            extra_patches_dict = {}
        else:
            extra_patches_dict = json.loads(caller.get_file(extra_patches_file))

        basepatch = IPS_Patch.load(f"{world_folder}/data/zsm.ips")
        return basepatch.apply(get_base_rom_bytes(extra_patches_dict))

class SMZ3UProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "3a177ba9879e3dd04fb623a219d175b2"
    game = "SMZ3U"
    patch_file_ending = ".apsmz3"

    procedure = [
        ("apply_basepatch", []),
        ("apply_tokens", ["token_data.bin"]),
    ]

    def write_tokens(self, patches, extra_patches):
        for addr, data in patches.items():
            self.write_token(APTokenTypes.WRITE, addr, bytes(data))
        self.write_file("token_data.bin", self.get_token_binary())
        self.write_file("extra_patches.json", json.dumps(extra_patches).encode("UTF-8"))

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def apply_sm_patches(rom: bytes, extra_patches_dict: dict):
    def apply_patch(r: bytes, p_fn: str):
        ed_r = cast(bytearray, r)

        if patch_fn == "Infinite_Space_Jump":
            ed_r[0x82493] = 0x80
            ed_r[0x82494] = 0x0D
        elif patch_fn == "LN_Chozo_SpaceJump_Check_Disable":
            for i in range(8):
                ed_r[0x2518f+i] = 0xEA
        else:
            basepatch = IPS_Patch.load(f"{world_folder}/data/sm/{p_fn}.ips")
            r = basepatch.apply(r)
        return r

    PATCHES = []

    if extra_patches_dict.get("sm_layout_patches", 0) > 0:
        PATCHES.extend([
            "brinstar_map_room",
            "early_super_bridge",
            "high_jump",
            "LN_Chozo_SpaceJump_Check_Disable",
            "mission_impossible",
            "moat",
            "nova_boost_platform",
            "red_tower",
            "spazer",
            "spospo_save",
        ])

    if extra_patches_dict.get("sm_infinite_space_jump", 0) > 0:
        PATCHES.append("Infinite_Space_Jump")

    if extra_patches_dict.get("sm_respin", 0) > 0:
        PATCHES.append("spinjumprestart")

    if extra_patches_dict.get("sm_save_station_refill", 0) > 0:
        PATCHES.append("refill_before_save")

    if extra_patches_dict.get("sm_fast_doors", 0) > 0:
        PATCHES.append("fast_doors")

    if extra_patches_dict.get("sm_fast_elevators", 0) > 0:
        PATCHES.append("elevators_speed")
        PATCHES.append("elevators_doors_speed")

    if extra_patches_dict.get("sm_disable_screen_shake", 0) > 0:
        PATCHES.append("disable_screen_shake")

    if extra_patches_dict.get("sm_disable_shinespark_damage", 0) > 0:
        PATCHES.append("disable_spark_damage")

    if extra_patches_dict.get("sm_nerfed_charge_beam", 0) > 0:
        PATCHES.append("nerfed_charge")

    if extra_patches_dict.get("sm_better_reserve_tanks", 0) > 0:
        PATCHES.append("better_reserves")

    if len(PATCHES) > 0:
        logger.info("Applying Super Metroid extra patches...")

    for patch_fn in PATCHES:
        rom = apply_patch(rom, patch_fn)

    return rom


def apply_z3_patches(rom: bytes, extra_patches_dict: dict):
    def apply_patch(r: bytes, p_fn: str):
        #ed_r = cast(bytearray, r)

        basepatch = IPS_Patch.load(f"{world_folder}/data/z3/{p_fn}.ips")
        r = basepatch.apply(r)
        return r

    PATCHES = []

    if extra_patches_dict.get("z3_respawn_with_full_health", 0) > 0:
        PATCHES.append("start_with_full_health")

    if len(PATCHES) > 0:
        logger.info("Applying A Link to the Past extra patches...")

    for patch_fn in PATCHES:
        rom = apply_patch(rom, patch_fn)

    return rom


def get_base_rom_bytes(extra_patches_dict: Optional[dict]=None) -> bytes:
    # override original get_base_rom_bytes, wait for second pass
    if extra_patches_dict is None:
        return b''

    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        sm_file_name = get_sm_base_rom_path()
        sm_base_rom_bytes = bytes(read_snes_rom(open(sm_file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(sm_base_rom_bytes)
        if SMJUHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for SM Japan+US release. '
                            'Get the correct game and version, then dump it')

        # Only if using extra_patches
        if extra_patches_dict is not None:
            sm_base_rom_bytes = apply_sm_patches(sm_base_rom_bytes, extra_patches_dict)

        lttp_file_name = get_lttp_base_rom_path()
        lttp_base_rom_bytes = bytes(read_snes_rom(open(lttp_file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(lttp_base_rom_bytes)
        if LTTPJPN10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for LttP Japan(1.0) release. '
                            'Get the correct game and version, then dump it')

        # Only if using extra_patches
        if extra_patches_dict is not None:
            lttp_base_rom_bytes = apply_z3_patches(lttp_base_rom_bytes, extra_patches_dict)

        get_base_rom_bytes.base_rom_bytes = bytes(combine_smz3_rom(sm_base_rom_bytes, lttp_base_rom_bytes))
    return get_base_rom_bytes.base_rom_bytes


def get_sm_base_rom_path(file_name: str = "") -> str:
    options = get_settings()
    if not file_name:
        file_name = options["sm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def get_lttp_base_rom_path(file_name: str = "") -> str:
    options = get_settings()
    if not file_name:
        file_name = options["lttp_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def combine_smz3_rom(sm_rom: bytes, lttp_rom: bytes) -> bytearray:
    combined = bytearray(0x600000)
    # SM hi bank
    pos = 0
    srcpos = 0
    for i in range(0x40):
        combined[pos + 0x8000:pos + 0x8000 + 0x8000] = sm_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    # SM lo bank
    pos = 0
    for i in range(0x20):
        combined[pos:pos + 0x8000] = sm_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    # Z3 hi bank
    pos = 0x400000
    srcpos = 0
    for i in range(0x20):
        combined[pos + 0x8000:pos + 0x8000 + 0x8000] = lttp_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    return combined
