import logging
from collections import Counter

from typing import TYPE_CHECKING

from MultiServer import mark_raw
from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from Utils import async_start

from worlds._bizhawk.client import BizHawkClient

from .data.logic.Monsters import monster_family_lookup, MonsterNames, monster_families, MonsterFamilies
from .data import memory
from .data.items import item_data_lookup, gear_item_names, gil_item_names, gil_item_sizes, zodiac_stone_names, \
    jp_item_names, jp_item_sizes, job_names, special_character_names, world_map_pass_names, earned_job_names, \
    item_name_lookup_by_game_id
from .data.locations import linked_reward_names
from .data.logic.JobUnlocks import unlock_dict
from .data.memory import stones_lookup, seed_hash_length, pass_paths, finale_path, location_dot_info, STORY_LOCATIONS, \
    RARE_BATTLE, SIDEQUEST_LOCATIONS, ALTIMA_ONLY_STORY_LOCATIONS, ADDRESS, mfi_locations, get_mfi_byte_bit

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

logger = logging.getLogger("Client")

guard_list = [
    (memory.world_loaded_address, [memory.world_loaded_value[3]], "MainRAM"),
    (memory.world_loaded_address + 1, [memory.world_loaded_value[2]], "MainRAM"),
    (memory.world_loaded_address + 2, [memory.world_loaded_value[1]], "MainRAM"),
    (memory.world_loaded_address + 3, [memory.world_loaded_value[0]], "MainRAM"),
]

battle_guard_list = [
    (memory.battle_loaded_address + 3, [memory.battle_loaded_value[3]], "MainRAM"),
    (memory.battle_loaded_address + 2, [memory.battle_loaded_value[2]], "MainRAM"),
    (memory.battle_loaded_address + 1, [memory.battle_loaded_value[1]], "MainRAM"),
    (memory.battle_loaded_address, [memory.battle_loaded_value[0]], "MainRAM"),
]

def get_byte_bit_from_index(index):
    return index // 8, 2 ** (index % 8)

def get_bit_value_from_position(position):
    return 2 ** position

class FinalFantasyTacticsIvaliceIslandClient(BizHawkClient):
    game = "Final Fantasy Tactics Ivalice Island"
    system = "PSX"
    patch_suffix = ".apfftii"

    def __init__(self) -> None:
        self.ram = "MainRAM"
        self.location_name_to_id: dict[str, int] | None = None
        self.item_name_to_id: dict[str, int] | None = None
        self.logged_version = False
        self.poach_mapping = None
        self.current_map = -1
        self.last_known_inventory_on_server: bytearray | None = None
        self.last_known_inventory_on_player: bytearray | None = None
        self.inventory_storage_initialized = False

    def _inventory_storage_key(self, ctx: "BizHawkClientContext") -> str:
        return f"FFTII_Players_Inventory_{ctx.team}"

    def _normalize_inventory_snapshot(self, inventory_data: object) -> bytearray | None:
        if isinstance(inventory_data, (bytes, bytearray, list, tuple)):
            normalized_inventory = bytearray(256)
            max_index = min(256, len(inventory_data))
            for index in range(max_index):
                value = inventory_data[index]
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    value = 0
                normalized_inventory[index] = min(99, max(0, value))
            return normalized_inventory
        return None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(
                ctx.bizhawk_ctx,
                [(memory.cd_name_location, len(memory.cd_name), self.ram)]))[0])
            try:
                rom_name = rom_name.decode("utf-8")
            except UnicodeDecodeError:
                return False
            if rom_name != memory.cd_name:
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        auth_raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(memory.rom_name_location_in_ram, memory.rom_name_length, self.ram)]))[0]
        if auth_raw == bytes(20):
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.command_processor.commands["poach_location"] = self._cmd_poach_locations
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(memory.rom_name_location_in_ram, memory.rom_name_length, self.ram)]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            if self.location_name_to_id is None:
                from . import FinalFantasyTacticsIvaliceIslandWorld
                self.location_name_to_id = FinalFantasyTacticsIvaliceIslandWorld.location_name_to_id
                self.item_name_to_id = FinalFantasyTacticsIvaliceIslandWorld.item_name_to_id
            if self.poach_mapping is None:
                self.poach_mapping = ctx.slot_data["poach_hints"]
                for key, value in self.poach_mapping.items():
                    self.poach_mapping[key] = sorted(value)
            if await self.check_valid_game(ctx):
                await self.check_victory(ctx)
                await self.location_check(ctx)
                await self.received_items_check(ctx)
                await self.write_pass_paths(ctx)
                await self.write_dot_colors(ctx)
                await self.update_current_map(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def check_valid_game(self, ctx: "BizHawkClientContext") -> bool:
        game_started_address, game_started_bit = get_byte_bit_from_index(memory.game_started_flag_address)
        game_started_data_world = await self.read_ram_value_guarded(ctx, memory.event_flags_location + game_started_address)
        game_started_data_battle = await self.read_ram_value_guarded_battle(ctx, memory.event_flags_location + game_started_address)
        if game_started_data_world is None and game_started_data_battle is None:
            return False
        game_started_data = game_started_data_world if game_started_data_battle is None else game_started_data_battle
        if game_started_data & game_started_bit == 0:
            return False
        return True

    async def location_check(self, ctx: "BizHawkClientContext"):
        locations_checked = []
        locations_checked.extend(await self.check_major_locations(ctx))
        locations_checked.extend(await self.check_poaches_world_map(ctx))
        locations_checked.extend(await self.check_poaches_battle(ctx))
        locations_checked.extend(await self.check_job_unlocks_world_map(ctx))
        locations_checked.extend(await self.check_job_unlocks_battle(ctx))
        locations_checked.extend(await self.check_mfi_locations_world_map(ctx))
        locations_checked.extend(await self.check_mfi_locations_battle(ctx))

        found_locations = await ctx.check_locations(locations_checked)
        for location in found_locations:
            ctx.locations_checked.add(location)

    async def check_major_locations(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        major_locations_data = await self.read_ram_values_guarded(
            ctx,
            memory.event_flags_location,
            memory.event_flags_length)
        if major_locations_data is None:
            return locations_checked
        for location, flag in memory.locations_to_read.items():
            offset, bit = get_byte_bit_from_index(flag)
            if major_locations_data[offset] & bit:
                locations_checked.append(self.location_name_to_id[location])
                if location in linked_reward_names.keys():
                    for linked_location in linked_reward_names[location]:
                        locations_checked.append(self.location_name_to_id[linked_location])
        return locations_checked

    async def check_poaches_world_map(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        poach_data = await self.read_ram_values_guarded(
            ctx,
            memory.poaching_flags_location,
            memory.poaching_flags_length)
        if poach_data is None:
            return locations_checked
        for location, flag in memory.poaching_addresses.items():
            offset, bit = get_byte_bit_from_index(flag)
            if poach_data[offset] & bit:
                locations_checked.append(self.location_name_to_id[location])
        return locations_checked

    async def check_poaches_battle(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        poach_data = await self.read_ram_values_guarded_battle(
            ctx,
            memory.poaching_flags_location,
            memory.poaching_flags_length)
        if poach_data is None:
            return locations_checked
        for location, flag in memory.poaching_addresses.items():
            offset, bit = get_byte_bit_from_index(flag)
            if poach_data[offset] & bit:
                locations_checked.append(self.location_name_to_id[location])
        return locations_checked

    async def check_job_unlocks_world_map(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        formation_data = await self.read_ram_values_guarded(ctx, memory.unit_stats_address, memory.unit_stats_length)
        if formation_data is None:
            return locations_checked
        unlocked_jobs = set()
        for unit_number in range(memory.unit_count):
            current_unit_jobs = {}
            base_address = unit_number * memory.unit_stat_size
            party_id_location = base_address + memory.party_id_offset
            unit_party_id_data = formation_data[party_id_location]
            if unit_party_id_data == 0xFF:
                continue
            for index, job in enumerate(memory.job_level_order):
                job_byte_location = base_address + memory.job_level_offset + (index // 2)
                if index % 2 == 0:
                    job_nybble = (formation_data[job_byte_location] & 0xF0) >> 4
                else:
                    job_nybble = formation_data[job_byte_location] & 0x0F
                current_unit_jobs[job] = job_nybble
            for job, requirements in unlock_dict.items():
                job_ids = []
                for earned_job in earned_job_names:
                    job_ids.append(self.item_name_to_id[earned_job])
                all_jobs_obtained = [item.item for item in ctx.items_received if item.item in job_ids]
                jobs_obtained_names = [ctx.item_names.lookup_in_game(pass_id) for pass_id in all_jobs_obtained]
                jobs_obtained_names.extend(["Squire"])
                unlock_job = self.check_job_unlock_condition(
                    current_unit_jobs,
                    requirements,
                    jobs_obtained_names,
                    job)
                if unlock_job:
                    unlocked_jobs.add(f"{job} Unlock")
        for job in unlocked_jobs:
            locations_checked.append(self.location_name_to_id[job])
        return locations_checked

    async def check_job_unlocks_battle(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        formation_data = await self.read_ram_values_guarded_battle(ctx, memory.battle_unit_stats_address, memory.battle_unit_stats_length)
        if formation_data is None:
            return locations_checked
        unlocked_jobs = set()
        for unit_number in range(memory.battle_unit_count):
            current_unit_jobs = {}
            base_address = unit_number * memory.battle_unit_stat_size
            unit_id_location = base_address + memory.unit_id_offset
            party_id_location = base_address + memory.party_id_offset
            unit_id_data = formation_data[unit_id_location]
            if unit_id_data == 0xFF:
                continue
            unit_party_id_data = formation_data[party_id_location]
            if unit_party_id_data >= 0x15:
                continue
            unit_team_data_location = base_address + memory.battle_unit_entd_flag_offset
            unit_team_data = formation_data[unit_team_data_location]
            if unit_team_data & 0x30 != 0: # Check if Blue Team
                continue
            if unit_team_data & 0x08 != 0: # Check if controllable (i.e. not Guest)
                continue
            for index, job in enumerate(memory.job_level_order):
                job_byte_location = base_address + memory.battle_unit_job_level_offset + (index // 2)
                if index % 2 == 0:
                    job_nybble = (formation_data[job_byte_location] & 0xF0) >> 4
                else:
                    job_nybble = formation_data[job_byte_location] & 0x0F
                if job_nybble > 8:
                    job_nybble = 0
                current_unit_jobs[job] = job_nybble
            for job, requirements in unlock_dict.items():
                job_ids = []
                for earned_job in earned_job_names:
                    job_ids.append(self.item_name_to_id[earned_job])
                all_jobs_obtained = [item.item for item in ctx.items_received if item.item in job_ids]
                jobs_obtained_names = [ctx.item_names.lookup_in_game(pass_id) for pass_id in all_jobs_obtained]
                jobs_obtained_names.extend(["Squire"])
                unlock_job = self.check_job_unlock_condition(
                    current_unit_jobs,
                    requirements,
                    jobs_obtained_names,
                    job)
                if unlock_job:
                    unlocked_jobs.add(f"{job} Unlock")
        for job in unlocked_jobs:
            locations_checked.append(self.location_name_to_id[job])
        return locations_checked

    def check_job_unlock_condition(self, job_levels, unlock_requirements, current_jobs, job_to_unlock):
        # If the job level is 0, that means that unit can't unlock that job.
        # IOW, males can't unlock Dancer, females can't unlock Bard. We reflect that here.
        if job_to_unlock == "Bard":
            if job_levels["Bard"] == 0:
                return False
        if job_to_unlock == "Dancer":
            if job_levels["Dancer"] == 0:
                return False
        for requirement_job, required_level in unlock_requirements.items():
            current_level = job_levels[requirement_job]
            if requirement_job not in current_jobs:
                return False
            if current_level < required_level:
                return False
        return True

    async def check_mfi_locations_world_map(self, ctx: "BizHawkClientContext"):
        locations_checked = []
        for battle_map in mfi_locations.keys():
            for i in range(4):
                mfi_byte, mfi_bit = get_mfi_byte_bit(battle_map, i)
                mfi_byte_value = await self.read_ram_value_guarded(ctx, mfi_byte)
                if mfi_byte_value is None:
                    continue
                if mfi_byte_value & mfi_bit > 0:
                    locations_checked.append(self.location_name_to_id[f"{battle_map} MFI {i + 1}"])
        return locations_checked

    async def check_mfi_locations_battle(self, ctx: "BizHawkClientContext"):
        locations_checked = []
        for battle_map in mfi_locations.keys():
            for i in range(4):
                mfi_byte, mfi_bit = get_mfi_byte_bit(battle_map, i)
                mfi_byte_value = await self.read_ram_value_guarded_battle(ctx, mfi_byte)
                if mfi_byte_value is None:
                    continue
                if mfi_byte_value & mfi_bit > 0:
                    locations_checked.append(self.location_name_to_id[f"{battle_map} MFI {i + 1}"])
        return locations_checked

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        await self.print_inventory(ctx)
        await self.get_inventory_from_datastorage(ctx)
        # Pull server inventory first so stale local state does not overwrite shared state.
        await self.sync_inventory_from_datastorage(ctx)
        await self.sync_inventory_to_datastorage(ctx)
        write_list: list[tuple[int, list[int], str]] = []

        items_received_count_low = await self.read_ram_value_guarded(ctx, memory.items_received_low)
        items_received_count_high = await self.read_ram_value_guarded(ctx, memory.items_received_high)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count = int.from_bytes([items_received_count_low, items_received_count_high], "little")
        added_gear_counter = Counter()
        added_shop_levels = 0
        added_gil = 0
        added_zodiac_stones: set = set()
        added_jp = 0
        added_special_characters: set = set()
        added_ramza_job_forms = 0
        added_jobs: set = set()
        items_received = []
        for i in range(items_received_count, len(ctx.items_received)):
        #if items_received_count < len(ctx.items_received):
            current_item = ctx.items_received[i]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            items_received.append(current_item_name)
            # Aggregate section
            if current_item_name in gear_item_names:
                added_gear_counter.update({current_item_name: 1})
            elif current_item_name == "Progressive Shop Level":
                added_shop_levels += 1
            elif current_item_name in gil_item_names:
                gil_item_size = int(ctx.slot_data["bonus_gil_item_size"])
                gil_quantity = gil_item_sizes[gil_item_size][current_item_name]
                added_gil += gil_quantity
            elif current_item_name in zodiac_stone_names:
                added_zodiac_stones.add(current_item_name)
            elif current_item_name in jp_item_names:
                jp_item_size = int(ctx.slot_data["jp_boon_size"])
                jp_quantity = jp_item_sizes[jp_item_size][current_item_name]
                added_jp += jp_quantity
            elif current_item_name in special_character_names:
                added_special_characters.add(current_item_name)
            elif current_item_name == "Progressive Ramza Job Form":
                added_ramza_job_forms += 1
            elif current_item_name in job_names:
                added_jobs.add(current_item_name)
        if items_received_count < len(ctx.items_received):
            # Resolve section
            if len(added_gear_counter) > 0:
                inventory_write_successful = await self.write_inventory_to_datastorage(ctx, added_gear_counter)
                if not inventory_write_successful:
                    return

            if added_shop_levels > 0:
                shop_write = await self.increment_shop_progression(ctx, added_shop_levels)
                if shop_write is None:
                    return
                write_list.append(shop_write)

            if added_gil > 0:
                gil_write = await self.write_gil_item(ctx, added_gil)
                if gil_write is None:
                    return
                write_list.extend(gil_write)

            if len(added_zodiac_stones) > 0:
                stone_write = await self.write_zodiac_stones(ctx, added_zodiac_stones)
                if stone_write is None:
                    return
                write_list.append(stone_write)

            if added_jp > 0:
                jp_write = await self.write_jp_items(ctx, added_jp)
                if jp_write is None:
                    return
                write_list.extend(jp_write)

                boon_write = await self.write_cumulative_boon(ctx, added_jp)
                if boon_write is None:
                    return
                write_list.extend(boon_write)

            if len(added_special_characters) > 0:
                recruit_write = await self.write_character_recruit(ctx, added_special_characters)
                if recruit_write is None:
                    return
                write_list.append(recruit_write)

            if added_ramza_job_forms > 0:
                ramza_write = await self.write_ramza_form(ctx, added_ramza_job_forms)
                if ramza_write is None:
                    return
                write_list.extend(ramza_write)

            if len(added_jobs) > 0:
                job_write = await self.write_job_unlocks(ctx, added_jobs)
                if job_write is None:
                    return
                write_list.append(job_write)

            items_received_count = len(ctx.items_received)
            write_list.append((memory.items_received_low, [items_received_count % 256], self.ram))
            write_list.append((memory.items_received_high, [items_received_count // 256], self.ram))
            write_successful = await self.write_ram_values_guarded(ctx, write_list)
            if write_successful:
                for item_name in items_received:
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {item_name}.")

        # Keep local RAM inventory aligned with server-side authoritative state.
        await self.sync_inventory_from_datastorage(ctx)

    async def check_victory(self, ctx):
        if ctx.finished_game:
            return
        else:
            if self.location_name_to_id["Graveyard of Airships 2 Story Battle"] in ctx.locations_checked:
                await ctx.send_msgs([
                    {"cmd": "StatusUpdate",
                     "status": ClientStatus.CLIENT_GOAL}
                ])
                ctx.finished_game = True

    async def set_options_flags(self, ctx):
        write_list = []
        sidequest_address, sidequest_bit = get_byte_bit_from_index(memory.yaml_options["Sidequests"])
        sidequest_data = await self.read_ram_value_guarded(ctx, memory.event_flags_location + sidequest_address)
        if sidequest_data is None:
            return
        new_sidequest_data = sidequest_data | sidequest_bit
        write_list.append((memory.event_flags_location + sidequest_address, [new_sidequest_data], self.ram))
        await self.write_ram_values_guarded(ctx, write_list)

    async def write_inventory_items(self, ctx: "BizHawkClientContext", items: Counter) -> tuple[int, list[int], str] | None:
        inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
        if inventory_data is None:
            return None
        inventory_data = bytearray(inventory_data)
        for item, quantity in items.items():
            item_index = item_data_lookup[item].game_id
            current_item_quantity = inventory_data[item_index]
            new_item_quantity = min(99, current_item_quantity + 1)
            inventory_data[item_index] = new_item_quantity
        new_inventory_data = list(inventory_data)
        return memory.inventory_start_address, new_inventory_data, self.ram

    async def increment_shop_progression(self, ctx: "BizHawkClientContext", added_levels: int) -> tuple[int, list[int], str] | None:
        current_shop_data = await self.read_ram_value_guarded(ctx, memory.shop_progression_address)
        if current_shop_data is None:
            return None
        new_shop_progression = min(15, current_shop_data + added_levels)
        return memory.shop_progression_address, [new_shop_progression], self.ram

    async def write_gil_item(self, ctx: "BizHawkClientContext", added_gil: int) -> list[tuple[int, list[int], str]] | None:
        current_gil_data = await self.read_ram_values_guarded(ctx, memory.war_funds_address, memory.war_funds_length)
        if current_gil_data is None:
            return None
        current_gil = int.from_bytes(current_gil_data, "little")
        new_gil = min(99999999, current_gil + added_gil)
        return [
            (memory.war_funds_address, [new_gil % 256], self.ram),
            (memory.war_funds_address + 1, [new_gil // 256 % 256], self.ram),
            (memory.war_funds_address + 2, [new_gil // (2**16) % 256], self.ram),
            (memory.war_funds_address + 3, [new_gil // (2**24)], self.ram),
        ]

    async def write_jp_items(self, ctx: "BizHawkClientContext", added_jp: int) -> list[tuple[int, list[int], str]] | None:
        formation_data = await self.read_ram_values_guarded(ctx, memory.unit_stats_address, memory.unit_stats_length)
        if formation_data is None:
            return None
        new_formation_data = bytearray(formation_data)
        for unit_number in range(memory.unit_count):
            base_address = unit_number * memory.unit_stat_size
            party_id_location = base_address + memory.party_id_offset
            unit_party_id_data = formation_data[party_id_location]
            if unit_party_id_data == 0xFF:
                continue
            for job_number in range(memory.job_amount):
                jp_address = base_address + memory.jp_offset + (job_number * 2)
                current_jp = int.from_bytes(formation_data[jp_address:jp_address + 2], "little")
                new_jp = min(current_jp + added_jp, 9999)
                new_jp_lower_byte = new_jp % 256
                new_jp_upper_byte = new_jp // 256
                new_formation_data[jp_address] = new_jp_lower_byte
                new_formation_data[jp_address + 1] = new_jp_upper_byte

        temp_formation_data = await self.read_ram_values_guarded(ctx, memory.temp_unit_stats_address, memory.temp_unit_stats_length)
        if temp_formation_data is None:
            return None
        temp_new_formation_data = bytearray(temp_formation_data)
        for unit_number in range(memory.temp_unit_count):
            base_address = unit_number * memory.temp_unit_stat_size
            for job_number in range(memory.temp_job_amount):
                jp_address = base_address + memory.temp_jp_offset + (job_number * 2)
                current_jp = int.from_bytes(temp_formation_data[jp_address:jp_address + 2], "little")
                new_jp = min(current_jp + added_jp, 9999)
                new_jp_lower_byte = new_jp % 256
                new_jp_upper_byte = new_jp // 256
                temp_new_formation_data[jp_address] = new_jp_lower_byte
                temp_new_formation_data[jp_address + 1] = new_jp_upper_byte
        return [
            (memory.unit_stats_address, list(new_formation_data), self.ram),
            (memory.temp_unit_stats_address, list(temp_new_formation_data), self.ram)
        ]

    async def write_cumulative_boon(self, ctx: "BizHawkClientContext", added_jp: int) -> list[tuple[int, list[int], str]] | None:
        current_jp_data = await self.read_ram_values_guarded(
            ctx,
            memory.total_jp_boon_gained,
            memory.total_jp_boon_gained_length)
        if current_jp_data is None:
            return
        current_jp_amount = int.from_bytes(current_jp_data, "little")
        new_jp_amount = min(9999, current_jp_amount + added_jp)
        return [
            (memory.total_jp_boon_gained, [new_jp_amount % 256], self.ram),
            (memory.total_jp_boon_gained + 1, [new_jp_amount // 256 % 256], self.ram)
        ]


    async def write_zodiac_stones(self, ctx: "BizHawkClientContext", stone_names: set[str]) -> tuple[int, list[int], str] | None:
        current_stone_data = await self.read_ram_values_guarded(ctx, memory.zodiac_stones_1_address, 2)
        if current_stone_data is None:
            return None
        current_stone_data = bytearray(current_stone_data)
        for stone_name in stone_names:
            address, bit = stones_lookup[stone_name]
            offset = 0 if address == memory.zodiac_stones_1_address else 1
            stone_byte = current_stone_data[offset]
            new_stone_byte = stone_byte | get_bit_value_from_position(bit)
            current_stone_data[offset] = new_stone_byte
        new_stone_data = list(current_stone_data)
        return memory.zodiac_stones_1_address, new_stone_data, self.ram

    async def write_character_recruit(self, ctx: "BizHawkClientContext", added_characters: set[str]) -> tuple[int, list[int], str] | None:
        address, bit = get_byte_bit_from_index(memory.character_recruit_addresses["Rafa"])
        recruit_location = memory.event_flags_location + address
        current_recruit_data = await self.read_ram_values_guarded(ctx, recruit_location, 3)
        if current_recruit_data is None:
            return None
        current_recruit_data = bytearray(current_recruit_data)
        for character in added_characters:
            address, bit = get_byte_bit_from_index(memory.character_recruit_addresses[character])
            address = memory.event_flags_location + address
            if address == 0x05792B:
                offset = 0
            elif address == 0x05792C:
                offset = 1
            else:
                offset = 2
            character_byte = current_recruit_data[offset]
            character_byte = character_byte | bit
            current_recruit_data[offset] = character_byte
        new_recruit_data = list(current_recruit_data)
        return recruit_location, new_recruit_data, self.ram

    async def write_ramza_form(self, ctx: "BizHawkClientContext", added_forms: int) -> list[tuple[int, list[int], str]] | None:
        chapter_2_address, chapter_2_bit = get_byte_bit_from_index(
            memory.ramza_job_unlock_addresses["Chapter 2 Ramza Squire Job Unlock"])
        chapter_4_address, chapter_4_bit = get_byte_bit_from_index(
            memory.ramza_job_unlock_addresses["Chapter 4 Ramza Squire Job Unlock"])
        chapter_2_location = memory.event_flags_location + chapter_2_address
        chapter_4_location = memory.event_flags_location + chapter_4_address
        chapter_2_data = await self.read_ram_value_guarded(ctx, chapter_2_location)
        chapter_4_data = await self.read_ram_value_guarded(ctx, chapter_4_location)
        if chapter_2_data is None or chapter_4_data is None:
            return None
        if added_forms == 1:
            if chapter_2_data & chapter_2_bit > 0:
                new_data = chapter_4_data | chapter_4_bit
                return [(chapter_4_location, [new_data], self.ram)]
            else:
                new_data = chapter_2_data | chapter_2_bit
                return [(chapter_2_location, [new_data], self.ram)]
        elif added_forms > 1:
            new_c2_data = chapter_2_data | chapter_2_bit
            new_c4_data = chapter_4_data | chapter_4_bit
            return [
                (chapter_2_location, [new_c2_data], self.ram),
                (chapter_4_location, [new_c4_data], self.ram)
            ]

    async def write_job_unlocks(self, ctx: "BizHawkClientContext", added_jobs: set[str]) -> tuple[int, list[int], str] | None:
        job_unlocked_data = await self.read_ram_values_guarded(ctx, memory.job_unlock_address_location, 3)
        if job_unlocked_data is None:
            return None
        job_unlocked_data = bytearray(job_unlocked_data)
        for job in added_jobs:
            address, bit = get_byte_bit_from_index(memory.available_jobs_addresses[job])
            address = memory.event_flags_location + address
            if address == 0x05793E:
                offset = 0
            elif address == 0x05793F:
                offset = 1
            else:
                offset = 2
            job_byte = job_unlocked_data[offset]
            job_byte = job_byte | bit
            job_unlocked_data[offset] = job_byte
        new_job_data = list(job_unlocked_data)
        return memory.job_unlock_address_location, new_job_data, self.ram

    async def write_pass_paths(self, ctx: "BizHawkClientContext"):
        pass_ids = []
        for world_map_pass in world_map_pass_names:
            pass_ids.append(self.item_name_to_id[world_map_pass])
        all_passes_obtained = [item.item for item in ctx.items_received if item.item in pass_ids]
        pass_obtained_names = [ctx.item_names.lookup_in_game(pass_id) for pass_id in all_passes_obtained]
        flags_to_write = []
        for pass_name in pass_obtained_names:
            if pass_name in pass_paths:
                for companion_pass in pass_paths[pass_name]:
                    if companion_pass in pass_obtained_names:
                        flags_to_write.extend(pass_paths[pass_name][companion_pass])

        stone_ids = []
        for stone in zodiac_stone_names:
            stone_ids.append(self.item_name_to_id[stone])
        all_stones_obtained = [item.item for item in ctx.items_received if item.item in stone_ids]
        if len(all_stones_obtained) >= ctx.slot_data["zodiac_stones_required"]:
            flags_to_write.append(finale_path)
        write_list = []
        for flag in flags_to_write:
            address, bit = get_byte_bit_from_index(flag)
            flag_address = memory.event_flags_location + address
            flag_data = await self.read_ram_value_guarded(ctx, flag_address)
            if flag_data is None:
                return
            new_flag_data = flag_data | bit
            write_list.append((flag_address, [new_flag_data], self.ram))
            await self.write_ram_values_guarded(ctx, write_list)

    async def write_dot_colors(self, ctx: "BizHawkClientContext"):
        for location_dot, location_dot_data in location_dot_info.items():
            needed_locations = []
            needed_locations.extend(location_dot_data[STORY_LOCATIONS])
            if ctx.slot_data["rare_battles"] == 1:
                if RARE_BATTLE in location_dot_data.keys():
                    needed_locations.append(location_dot_data[RARE_BATTLE])
            if ctx.slot_data["sidequest_battles"] == 1:
                if SIDEQUEST_LOCATIONS in location_dot_data.keys():
                    needed_locations.extend(location_dot_data[SIDEQUEST_LOCATIONS])
            if ctx.slot_data["final_battles"] == 1:
                if ALTIMA_ONLY_STORY_LOCATIONS in location_dot_data.keys():
                    needed_locations.extend(location_dot_data[ALTIMA_ONLY_STORY_LOCATIONS])
            toggle_dot = True
            for location in needed_locations:
                location_id = self.location_name_to_id[location.value]
                if location_id not in ctx.checked_locations:
                    toggle_dot = False
            if toggle_dot:
                location_dot_address = location_dot_data[ADDRESS][0]
                location_dot_bit = location_dot_data[ADDRESS][1]
                current_dot_data = await self.read_ram_value_guarded(ctx, location_dot_address)
                if current_dot_data is None:
                    return
                if current_dot_data & location_dot_bit == 0:
                    new_dot_data = current_dot_data | location_dot_bit
                    await self.write_ram_values_guarded(ctx, [
                        (location_dot_address, [new_dot_data], self.ram)
                    ])

    async def update_current_map(self, ctx: "BizHawkClientContext"):
        current_map = await self.read_ram_value_guarded_battle(ctx, memory.current_map_location)
        if current_map is None:
            current_map = -1
        if current_map != self.current_map:
            self.current_map = current_map
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": {
                    "current_map": self.current_map
                }
            }])

    @mark_raw
    def _cmd_poach_locations(self, ctx: "BizHawkClientCommandProcessor", monster: str) -> None:
        """Check where monster families are located."""
        key = monster.title()
        if self.poach_mapping is None:
            logger.info("Please connect to the server first.")
            return
        if key not in self.poach_mapping.keys():
            try:
                new_key = MonsterFamilies(key)
                key = monster_families[new_key][0]
            except ValueError:
                valid_names = [monster_name.value for monster_name in monster_family_lookup.keys()]
                valid_names.extend([family_name.value for family_name in monster_families.keys()])
                logger.info(f"{key} not found. Please enter a valid monster or family name.")
                logger.info(f"Valid names are {", ".join(valid_names)}")
                return
        family = monster_family_lookup[MonsterNames(key)]
        family_members = monster_families[family]
        returned_info = []
        for family_member in family_members:
            returned_info.extend(self.poach_mapping[family_member.value])
        logger.info(f"The {family.value} family can be found in the following locations:")
        for location in returned_info:
            logger.info(f"- {location}")

    async def read_ram_values_guarded(self, ctx: "BizHawkClientContext", location: int, size: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, size, self.ram)], guard_list)
        if value is None:
            return None
        return value[0]

    async def read_ram_value_guarded(self, ctx: "BizHawkClientContext", location: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, 1, self.ram)], guard_list)
        if value is None:
            return None
        return int.from_bytes(value[0], "little")

    async def write_ram_values_guarded(self, ctx: "BizHawkClientContext", write_list: list[tuple[int, list[int], str]]):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, guard_list)

    async def read_ram_value_guarded_battle(self, ctx: "BizHawkClientContext", location: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, 1, self.ram)], battle_guard_list)
        if value is None:
            return None
        return int.from_bytes(value[0], "little")

    async def read_ram_values_guarded_battle(self, ctx: "BizHawkClientContext", location: int, size: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, size, self.ram)], battle_guard_list)
        if value is None:
            return None
        return value[0]


    async def get_inventory_from_datastorage(self, ctx: "BizHawkClientContext") -> Counter | None:
        key = self._inventory_storage_key(ctx)
        if not self.inventory_storage_initialized:
            await ctx.send_msgs([{"cmd": "Set", "key": key,
                                   "default": [0] * 256, "want_reply": True,
                                   "operations": [{"operation": "default", "value": 0}]}])
            self.inventory_storage_initialized = True
        elif self.last_known_inventory_on_server is None:
            await ctx.send_msgs([{"cmd": "Get", "keys": [key]}])
        return None


    async def write_inventory_to_datastorage(self, ctx: "BizHawkClientContext", items: Counter) -> bool:
        if self.last_known_inventory_on_server is None:
            inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
            if inventory_data is None:
                return False
            self.last_known_inventory_on_server = self._normalize_inventory_snapshot(inventory_data)

        server_inventory_data = self._normalize_inventory_snapshot(self.last_known_inventory_on_server)
        if server_inventory_data is None:
            return False
        new_inventory_data = bytearray(server_inventory_data)

        for item, quantity in items.items():
            item_index = item_data_lookup[item].game_id
            current_item_quantity = new_inventory_data[item_index]
            new_item_quantity = min(99, max(0, current_item_quantity + quantity))
            new_inventory_data[item_index] = new_item_quantity

        key = self._inventory_storage_key(ctx)
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": key,
            "default": [0] * 256,
            "want_reply": True,
            "operations": [{"operation": "replace", "value": list(new_inventory_data)}]
        }])
        self.last_known_inventory_on_server = new_inventory_data
        return True

    async def print_inventory(self, ctx: "BizHawkClientContext"):
        inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
        print(f"Current inventory data: {inventory_data}")

    async def sync_inventory_from_datastorage(self, ctx: "BizHawkClientContext") -> None:
        server_inventory_data = self._normalize_inventory_snapshot(self.last_known_inventory_on_server)
        if server_inventory_data is None:
            return
        normalized_server_data = bytearray(server_inventory_data)

        player_inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
        if player_inventory_data is None:
            return
        normalized_player_data = self._normalize_inventory_snapshot(player_inventory_data)
        if normalized_player_data is None:
            return
        self.last_known_inventory_on_player = bytearray(normalized_player_data)
        if normalized_player_data == normalized_server_data:
            return

        write_successful = await self.write_ram_values_guarded(ctx, [
            (memory.inventory_start_address, list(normalized_server_data), self.ram)
        ])
        if write_successful:
            self.last_known_inventory_on_player = bytearray(normalized_server_data)

    async def sync_inventory_to_datastorage(self, ctx: "BizHawkClientContext") -> None:
        player_inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
        if player_inventory_data is None:
            return
        normalized_player_data_optional = self._normalize_inventory_snapshot(player_inventory_data)
        if normalized_player_data_optional is None:
            return
        normalized_player_data = bytearray(normalized_player_data_optional)

        if self.last_known_inventory_on_player is None:
            self.last_known_inventory_on_player = bytearray(normalized_player_data)
            return

        if normalized_player_data == self.last_known_inventory_on_player:
            return

        key = self._inventory_storage_key(ctx)
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": key,
            "default": [0] * 256,
            "want_reply": True,
            "operations": [{"operation": "replace", "value": list(normalized_player_data)}]
        }])
        self.last_known_inventory_on_server = bytearray(normalized_player_data)
        self.last_known_inventory_on_player = bytearray(normalized_player_data)

    async def get_inventory_diff(self, ctx: "BizHawkClientContext") -> Counter | None:
        player_inventory_data = await self.read_ram_values_guarded(ctx, memory.inventory_start_address, 256)
        if player_inventory_data is None:
            return None
        player_inventory_data = self._normalize_inventory_snapshot(player_inventory_data)
        server_inventory_data = self._normalize_inventory_snapshot(self.last_known_inventory_on_server)
        if server_inventory_data is None:
            return None
        if player_inventory_data is None:
            return None
        inventory_diff: Counter[str] = Counter()

        max_length = max(len(server_inventory_data), len(player_inventory_data))
        for item_index in range(max_length):
            server_quantity = server_inventory_data[item_index] if item_index < len(server_inventory_data) else 0
            player_quantity = player_inventory_data[item_index] if item_index < len(player_inventory_data) else 0
            delta = player_quantity - server_quantity
            if delta == 0:
                continue

            item_name = item_name_lookup_by_game_id.get(item_index)
            if item_name is None or item_name == "Nothing":
                continue
            inventory_diff[item_name] += delta

        return inventory_diff if inventory_diff else None



    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        print(f"Received package: {args}")
        if cmd == "Connected":
            key = self._inventory_storage_key(ctx)
            ctx.set_notify(key)
            async_start(ctx.send_msgs([{
                "cmd": "Set",
                "key": key,
                "default": [0] * 256,
                "want_reply": True,
                "operations": [{"operation": "default", "value": 0}]
            }]))
        elif cmd == "Retrieved":
            player_inventory = args["keys"]
            key = self._inventory_storage_key(ctx)
            if key in player_inventory:
                self.last_known_inventory_on_server = self._normalize_inventory_snapshot(player_inventory[key])
        elif cmd == "SetReply":
            key = self._inventory_storage_key(ctx)
            if args.get("key") == key:
                self.last_known_inventory_on_server = self._normalize_inventory_snapshot(args.get("value"))
        return