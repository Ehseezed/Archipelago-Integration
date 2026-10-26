import json
import logging
import os

import Utils
import settings
import typing

from typing import Dict, Any, TextIO
from BaseClasses import MultiWorld, ItemClassification, Tutorial, Item, Region
from rule_builder.field_resolvers import FromWorldAttr
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasGroupUnique, CanReachRegion, Rule, False_, Filtered

from worlds.AutoWorld import World, WebWorld

from .Items import item_table
from .Locations import all_locations, FinalFantasyTacticsIILocation
from .Logic import create_logic_rule, create_logic_rule_for_list, LogicObject, PoachLogicObject
from .Options import FinalFantasyTacticsIIOptions, fftii_option_groups, MoveFindItemLocationLogic
from .Rom import FinalFantasyTacticsIIProcedurePatch
from .Client import FinalFantasyTacticsIvaliceIslandClient

from .data.items import zodiac_stone_names, world_map_pass_names, job_names, shop_levels, \
    special_character_names, ramza_job_levels, rare_item_names, shop_item_names, \
    gil_item_names_weighted, earned_job_names, filler_item_names, jp_item_names_weighted, gear_item_names, \
    item_name_lookup_by_game_id, item_data_lookup
from .data.locations import all_regions, world_map_regions, story_battle_locations, character_recruit_locations, \
    sidequest_battle_locations, job_unlock_locations, rare_battle_locations, default_murond_fights, \
    shop_unlock_locations, monster_location_names, \
    ramza_job_unlock_locations, location_sort_list_names, locations_with_text, linked_reward_names, \
    location_groups, story_stone_locations, altima_only_stone_locations, \
    sidequest_stone_locations, rare_battle_location_names, mfi_locations, mfi_location_names, main_mfi_locations, \
    sidequest_mfi_locations, four_jump_mfi_locations, five_jump_mfi_locations, lava_mfi_locations, \
    chocobo_ferry_exclusion_locations
from .data.logic.FFTLocation import LocationNames
from .data.logic.Monsters import monster_locations_lookup, monster_family_lookup, monster_families, MonsterNames, \
    RegionAccessRequirement, monster_locations, MonsterFamilies, large_monster_families, flying_monster_families, \
    lava_monster_families
from .data.logic.regions.Fovoham import fovoham_regions
from .data.logic.regions.Gallione import gallione_regions
from .data.logic.regions.Jobs import jobs_regions
from .data.logic.regions.Lesalia import lesalia_regions
from .data.logic.regions.Limberry import limberry_regions
from .data.logic.regions.Lionel import lionel_regions
from .data.logic.regions.Murond import murond_regions
from .data.logic.regions.Zeltennia import zeltennia_regions
from .data.memory import mfi_location_id_to_name
from .data.text import create_text_for_own_item, create_text_for_offworld_item
from .enemyrando.BattleMappingLists import gallione_only_randoms, gallione_story_fights, gallione_randoms_from_fovoham
from .enemyrando.BattleMappings import valid_shuffle_source_units, zodiac_shuffle_source_units, \
    sidequest_shuffle_source_units, zodiac_sidequest_source_units, altima_source_units
from .enemyrando.BattleRegionMapping import all_battle_region_mappings, PoachHintLocation
from .enemyrando.EventCodes import EventCode
from .enemyrando.FactoryKey import FactoryKey
from .enemyrando.GenerationFunctions import get_eligible_destination_jobs, get_logic_adjusted_fight_level, \
    get_randomized_mapping, check_if_source_unit_randomized, create_poach_mappings, create_default_poach_mappings
from .enemyrando.Job import Job, generic_jobs, generic_monster_jobs, special_character_jobs, special_monster_jobs, \
    lucavi_jobs, monster_job_name_lookup
from .enemyrando.RandomizedMapping import RandomizedMapping
from .enemyrando.RandomizedMappings import base_shuffle_list, zodiac_story_shuffle_list, sidequest_zodiac_shuffle_list, \
    sidequest_boss_shuffle_list, generic_job_table, special_job_table, generic_monster_table, \
    special_monster_table, lucavi_table, factory_mappings, altima_story_shuffle_list
from .enemyrando import BattleMappingLists
from .enemyrando.RandomizedPoachBattleSource import RandomizedPoachBattleSource
from .enemyrando.RandomizedUnitFactory import RandomizedUnitFactory
from .enemyrando.RandomizedUnits import RandomizedUnit
from .enemyrando.SourceUnit import SourceUnit
from .enemyrando.SpriteSet import SpriteSet


class FinalFantasyTacticsIISettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Final Fantasy Tactics ISO"""
        description = "Final Fantasy Tactics ISO File"
        copy_to = "Final Fantasy Tactics (USA).bin"
        md5s = ["b156ba386436d20fd5ed8d37bab6b624"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False


class FinalFantasyTacticsIIWeb(WebWorld):
    theme = "ocean"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Final Fantasy Tactics for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie"]
    )

    tutorials = [setup]

    rich_text_options_doc = True
    option_groups = fftii_option_groups


class FinalFantasyTacticsIvaliceIslandWorld(World):
    """
    An open world mod for Final Fantasy Tactics for Archipelago.
    Find all the Zodiac Stones and make your way to Murond Death City to confront Altima!
    """
    settings: typing.ClassVar[FinalFantasyTacticsIISettings]
    game = "Final Fantasy Tactics Ivalice Island"
    options_dataclass = FinalFantasyTacticsIIOptions
    options: FinalFantasyTacticsIIOptions

    base_id = 0
    web = FinalFantasyTacticsIIWeb()

    item_name_to_id = {item: item_data.id for item, item_data in item_table.items()}
    location_name_to_id = {location.name: location.id for location in all_locations}
    item_name_groups = {
        "Zodiac Stones": zodiac_stone_names,
        "Characters": special_character_names,
        "Jobs": job_names
    }

    location_name_groups = location_groups

    filler_items: list[str] | None
    included_locations: list[str]
    murond_fights: list[str]
    starting_pass: str
    zodiac_stones_required: int
    zodiac_stones_in_pool: int
    enemy_rando_mapping: dict[EventCode, list[RandomizedMapping]]
    poach_enemy_rando_mapping: dict[EventCode, list[RandomizedMapping]]
    poach_locations: dict[MonsterNames, list[RegionAccessRequirement]]
    poach_hints: dict[MonsterNames, list[PoachHintLocation]]
    excluded_monster_locations: list[str]

    mfi_rewards: dict[int, list[tuple[int, int]]]

    version = "0.4.0"
    debug = False
    topology_present = debug

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_items = None
        self.included_locations = list()
        self.murond_fights = list()
        self.starting_pass = "Gallione Pass"
        self.zodiac_stones_required = 0
        self.poach_locations = dict()
        self.poach_hints = dict()
        self.poach_database: dict[MonsterNames, list[RegionAccessRequirement]] = dict()
        self.excluded_monster_locations = []

        self.mfi_rewards = dict()
        self.poach_rewards = list()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        logging.info(f"Final Fantasy Tactics Ivalice Island APWorld v{cls.version} used for generation.")

    @classmethod
    def stage_write_spoiler_header(cls, _multiworld: MultiWorld, spoiler_handle: TextIO):
        spoiler_handle.write(f"\nFinal Fantasy Tactics Ivalice Island APWorld version: v{cls.version}\n")

    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
        if FinalFantasyTacticsIvaliceIslandWorld.debug:
            spoiler_handle.write("\n")
            for event_id, mapping_list in self.enemy_rando_mapping.items():
                spoiler_handle.write("\n")
                spoiler_handle.write(EventCode(event_id).name)
                spoiler_handle.write("\n")
                for mapping in mapping_list:
                    spoiler_handle.write(f"- {mapping}\n")
            spoiler_handle.write("\n")

    def create_item(self, name: str) -> "FinalFantasyTacticsIIItem":
        return FinalFantasyTacticsIIItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> "FinalFantasyTacticsIIItem":
        return FinalFantasyTacticsIIItem(name, ItemClassification.progression, None, self.player)

    def create_enemy_rando_mapping(self):
        # Switch modes based on settings

        # if unique enemy shuffle
        if (self.options.enemy_randomizer == self.options.enemy_randomizer.option_boss_shuffle
                or self.options.enemy_randomizer == self.options.enemy_randomizer.option_boss_shuffle_randomized):
            source_units: list[SourceUnit] = valid_shuffle_source_units.copy()
            destination_units = base_shuffle_list.copy()
            if self.options.lucavi_randomizer >= self.options.lucavi_randomizer.option_lucavi: # if Zodiac bosses are in
                source_units.extend(zodiac_shuffle_source_units)
                destination_units.extend(zodiac_story_shuffle_list)
                if self.options.sidequest_battles: # if sidequest zodiac bosses are in
                    source_units.extend(zodiac_sidequest_source_units)
                    destination_units.extend(sidequest_zodiac_shuffle_list)
                if self.options.lucavi_randomizer == self.options.lucavi_randomizer.option_include_altima:
                    source_units.extend(altima_source_units)
                    destination_units.extend(altima_story_shuffle_list)
            if self.options.sidequest_battles: # if sidequest bosses are in
                source_units.extend(sidequest_shuffle_source_units)
                destination_units.extend(sidequest_boss_shuffle_list)
            # for each souorce unit, get a unit factory
            assert len(source_units) == len(destination_units), (len(source_units), len(destination_units))
            destination_unit_jobs = [unit.job for unit in destination_units]
            unit_factories: dict[Job, RandomizedUnitFactory] = {
                job.job: RandomizedUnitFactory({job: 1}, self.random) for job in destination_units
            }
            for source_unit in source_units:
                assert source_unit.job in destination_unit_jobs, Job(source_unit.job).name
            mapping_dict: dict[EventCode, list[RandomizedMapping]] = {}
            for fight in BattleMappingLists.all_fights:
                mapping_dict[fight.battle_id] = list()
                for fight_source_unit in fight.source_units:
                    if fight_source_unit in source_units:
                        new_randomized_mapping = RandomizedMapping()
                        new_randomized_mapping.source_unit = fight_source_unit
                        logical_difficulty = self.options.logical_difficulty.value
                        adjusted_battle_level = get_logic_adjusted_fight_level(fight.battle_level, logical_difficulty)
                        new_randomized_mapping.battle_level = adjusted_battle_level
                        new_randomized_mapping.boss_unit = fight_source_unit.immortal
                        mapping_dict[fight.battle_id].append(new_randomized_mapping)
            refined_dict = {key: value for key, value in mapping_dict.items() if len(value) > 0}
            for battle_id, battle_mapping_list in refined_dict.items():
                for mapping in battle_mapping_list:
                    factory_options = {
                        job: factory for job, factory in unit_factories.items()
                        if factory.get_lowest_difficulty() <= mapping.battle_level
                           and job in destination_unit_jobs
                    }
                    if len(factory_options) == 0:
                        mapping.battle_level = 14
                        factory_options = {
                            job: factory for job, factory in unit_factories.items()
                            if factory.get_lowest_difficulty() <= mapping.battle_level
                               and job in destination_unit_jobs
                        }
                    destination_job = self.random.choice(sorted(list(factory_options.keys())))
                    destination_factory = factory_options[destination_job]
                    destination_unit_job = destination_factory.get_unit(mapping.battle_level).job
                    destination_unit_key = FactoryKey[destination_unit_job.name]
                    mapping.destination_unit = destination_unit_job
                    destination_unit_jobs.remove(destination_job)
            self.enemy_rando_mapping = {}
            for key, value in refined_dict.items():
                self.enemy_rando_mapping[key] = value
        if self.options.enemy_randomizer >= self.options.enemy_randomizer.option_randomized: # Randomized enemies
            randomized_factories: dict[FactoryKey, RandomizedUnitFactory] = {
                job: RandomizedUnitFactory(mapping, self.random) for job, mapping in factory_mappings.items()
            }
            if self.options.enemy_randomizer_locality == self.options.enemy_randomizer_locality.option_battle:
                if self.options.randomize_story_fights_only:
                    fight_list = BattleMappingLists.all_story_fights
                else:
                    fight_list = BattleMappingLists.all_fights
                for fight in fight_list:
                    fight_mapping_list = []
                    fight_difficulty = get_logic_adjusted_fight_level(
                        fight.battle_level, self.options.logical_difficulty.value)
                    working_factories = randomized_factories.copy()
                    for source_unit in fight.source_units:
                        skip = False
                        found_mapping = None
                        if fight.battle_id in self.enemy_rando_mapping.keys():
                            for mapping in self.enemy_rando_mapping[fight.battle_id]:
                                if source_unit == mapping.source_unit:
                                    skip = True
                                    found_mapping = mapping
                        if not skip and check_if_source_unit_randomized(source_unit, self.options):
                            randomized_mapping, destination_factory_key = get_randomized_mapping(
                                working_factories,
                                randomized_factories,
                                fight_difficulty,
                                source_unit,
                                self
                            )
                            fight_mapping_list.append(randomized_mapping)
                            if self.options.enemy_randomizer_method == self.options.enemy_randomizer_method.option_shuffle:
                                if destination_factory_key in working_factories:
                                    working_factories.pop(destination_factory_key)
                        elif skip:
                            fight_mapping_list.append(found_mapping)
                    self.enemy_rando_mapping[fight.battle_id] = fight_mapping_list
            if self.options.enemy_randomizer_locality == self.options.enemy_randomizer_locality.option_region:
                if self.options.randomize_story_fights_only:
                    region_fight_list = BattleMappingLists.story_fights_by_region
                else:
                    region_fight_list = BattleMappingLists.all_fights_by_region
                for region in region_fight_list:
                    region_source_units = set()
                    region_mappings = []
                    source_unit_difficulty: dict[SourceUnit, int] = {}
                    for fight in region:
                        fight_difficulty = get_logic_adjusted_fight_level(
                            fight.battle_level, self.options.logical_difficulty.value)
                        region_source_units.update(fight.source_units)
                        if fight.battle_id in self.enemy_rando_mapping.keys():
                            for mapping in self.enemy_rando_mapping[fight.battle_id]:
                                region_source_units.remove(mapping.source_unit)
                        for source_unit in fight.source_units:
                            if source_unit in source_unit_difficulty.keys():
                                source_unit_difficulty[source_unit] = min(
                                    fight_difficulty, source_unit_difficulty[source_unit])
                            else:
                                source_unit_difficulty[source_unit] = fight_difficulty
                    working_factories = randomized_factories.copy()
                    for source_unit in sorted(list(region_source_units)):
                        if check_if_source_unit_randomized(source_unit, self.options):
                            randomized_mapping, destination_job_key = get_randomized_mapping(
                                working_factories,
                                randomized_factories,
                                source_unit_difficulty[source_unit],
                                source_unit,
                                self
                            )
                            region_mappings.append(randomized_mapping)
                            if self.options.enemy_randomizer_method == self.options.enemy_randomizer_method.option_shuffle:
                                if destination_job_key in working_factories:
                                    working_factories.pop(destination_job_key)
                    for fight in region:
                        if fight.battle_id in self.enemy_rando_mapping.keys():
                            self.enemy_rando_mapping[fight.battle_id].extend(region_mappings)
                        else:
                            self.enemy_rando_mapping[fight.battle_id] = region_mappings
            if self.options.enemy_randomizer_locality == self.options.enemy_randomizer_locality.option_global:
                if self.options.randomize_story_fights_only:
                    fight_list = BattleMappingLists.all_story_fights
                else:
                    fight_list = BattleMappingLists.all_fights
                all_source_units: set[SourceUnit] = set()
                all_mappings = []
                source_unit_difficulty: dict[SourceUnit, int] = {}
                for fight in fight_list:  # for each fight
                    fight_difficulty = get_logic_adjusted_fight_level(
                        fight.battle_level, self.options.logical_difficulty.value)
                    all_source_units.update(fight.source_units)
                    if fight.battle_id in self.enemy_rando_mapping.keys():
                        for mapping in self.enemy_rando_mapping[fight.battle_id]:
                            all_source_units.remove(mapping.source_unit)
                    for source_unit in fight.source_units:
                        if source_unit in source_unit_difficulty.keys():
                            source_unit_difficulty[source_unit] = min(
                                fight_difficulty, source_unit_difficulty[source_unit])
                        else:
                            source_unit_difficulty[source_unit] = fight_difficulty
                working_factories = randomized_factories.copy()
                for source_unit in sorted(list(all_source_units)):
                    if check_if_source_unit_randomized(source_unit, self.options):
                        randomized_mapping, destination_job_key = get_randomized_mapping(
                            working_factories,
                            randomized_factories,
                            source_unit_difficulty[source_unit],
                            source_unit,
                            self
                        )
                        all_mappings.append(randomized_mapping)
                        if self.options.enemy_randomizer_method == self.options.enemy_randomizer_method.option_shuffle:
                            if destination_job_key in working_factories:
                                working_factories.pop(destination_job_key)
                for fight in fight_list:
                    if fight.battle_id in self.enemy_rando_mapping.keys():
                        self.enemy_rando_mapping[fight.battle_id].extend(all_mappings)
                    else:
                        self.enemy_rando_mapping[fight.battle_id] = all_mappings
            mapping_dict: dict[EventCode, list[RandomizedMapping]] = {}
            for fight in BattleMappingLists.all_fights:
                mapping_dict[fight.battle_id] = list()
                for fight_source_unit in fight.source_units:
                    new_mapping = RandomizedMapping()
                    new_mapping.source_unit = fight_source_unit
                    new_mapping.destination_unit = None
                    mapping_dict[fight.battle_id].append(new_mapping)
            self.poach_enemy_rando_mapping = self.enemy_rando_mapping.copy()
            for key, value in mapping_dict.items():
                if key not in self.poach_enemy_rando_mapping.keys():
                    self.poach_enemy_rando_mapping[key] = value

    def apply_enemy_rando(self):
        self.enemy_rando_mapping: dict[EventCode, list[RandomizedMapping]] = {}
        if self.options.enemy_randomizer > self.options.enemy_randomizer.option_disabled:
            self.poach_enemy_rando_mapping = dict()
            self.create_enemy_rando_mapping()
            if len(self.poach_enemy_rando_mapping) > 0:
                poach_mappings = create_poach_mappings(self.poach_enemy_rando_mapping)
            else:
                poach_mappings = create_default_poach_mappings()
        else:
            poach_mappings = create_default_poach_mappings()
        poach_locations: dict[MonsterNames, list[RegionAccessRequirement]] = dict()
        for monster_name in monster_family_lookup.keys():
            self.poach_hints[monster_name] = list()
            self.poach_database[monster_name] = list()
            poach_locations[monster_name] = []
            for region, battle_sources in poach_mappings.items():
                for battle_source in battle_sources:
                    if monster_name == battle_source.monster_name:
                        battle_region_mapping = [
                            mapping for mapping in all_battle_region_mappings
                            if battle_source.fight_id in mapping.battle_ids
                        ].pop()
                        story_battle = battle_source.fight_id > 0x100
                        requirement = RegionAccessRequirement(
                            battle_region_mapping.regions,
                            battle_source.battle_level,
                            story=story_battle
                        )
                        requirement.battle_id = battle_source.fight_id
                        poach_locations[monster_name].append(requirement)
                        poach_hint = PoachHintLocation(
                            battle_region_mapping.name,
                            battle_source.battle_level,
                            battle_source.fight_id)
                        self.poach_hints[monster_name].append(poach_hint)
                        self.poach_database[monster_name].append(requirement)
            self.poach_locations = poach_locations

    def generate_early(self) -> None:
        self.apply_enemy_rando()

        all_items = set(gear_item_names)
        rare_items = set(rare_item_names)
        common_items = all_items - rare_items
        all_items = sorted(list(all_items))
        rare_items = sorted(list(rare_items))
        common_items = sorted(list(common_items))
        filler_lists = []
        normal_weight = self.options.normal_item_weight.value
        rare_weight = self.options.rare_item_weight.value
        if normal_weight == rare_weight:
            filler_lists = [shop_item_names, rare_item_names]
        else:
            # One instance of a list per weight value
            for i in range(normal_weight):
                filler_lists.append(shop_item_names)
            for i in range(rare_weight):
                filler_lists.append(rare_item_names)

        # Move-Find Item randomization
        if self.options.randomize_move_find_item_rewards > self.options.randomize_move_find_item_rewards.option_off:
            for map_id, map_name in mfi_location_id_to_name.items():
                self.mfi_rewards[map_id] = []
                for i in range(4):
                    if self.options.randomize_move_find_item_rewards == self.options.randomize_move_find_item_rewards.option_on:
                        common_item = item_data_lookup[self.random.choice(all_items)].game_id
                        rare_item = item_data_lookup[self.random.choice(all_items)].game_id
                    elif self.options.randomize_move_find_item_rewards == self.options.randomize_move_find_item_rewards.option_split:
                        common_item = item_data_lookup[self.random.choice(common_items)].game_id
                        rare_item = item_data_lookup[self.random.choice(rare_items)].game_id
                    elif self.options.randomize_move_find_item_rewards == self.options.randomize_move_find_item_rewards.option_weighted:
                        chosen_weighted_list = self.random.choice(filler_lists)
                        common_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                        rare_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                    else: # weighted split
                        chosen_weighted_list = self.random.choice(filler_lists)
                        common_item = item_data_lookup[self.random.choice(common_items)].game_id
                        rare_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                    self.mfi_rewards[map_id].append((common_item, rare_item))

        if self.options.randomize_poach_rewards > self.options.randomize_poach_rewards.option_off:
            for i in range(len(monster_location_names)):
                if self.options.randomize_poach_rewards == self.options.randomize_poach_rewards.option_on:
                    common_item = item_data_lookup[self.random.choice(all_items)].game_id
                    rare_item = item_data_lookup[self.random.choice(all_items)].game_id
                elif self.options.randomize_poach_rewards == self.options.randomize_poach_rewards.option_split:
                    common_item = item_data_lookup[self.random.choice(common_items)].game_id
                    rare_item = item_data_lookup[self.random.choice(rare_items)].game_id
                elif self.options.randomize_poach_rewards == self.options.randomize_poach_rewards.option_weighted:
                    chosen_weighted_list = self.random.choice(filler_lists)
                    common_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                    rare_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                else: # weighted split
                    chosen_weighted_list = self.random.choice(filler_lists)
                    common_item = item_data_lookup[self.random.choice(common_items)].game_id
                    rare_item = item_data_lookup[self.random.choice(chosen_weighted_list)].game_id
                self.poach_rewards.append({"Common": common_item, "Rare": rare_item})

        # Story battles are always in
        included_locations: list[LocationNames] = []
        included_locations.extend(story_battle_locations)
        included_locations.extend(story_stone_locations)
        included_locations.extend(altima_only_stone_locations)

        # Character recruitment locations are always in if not tied to a sidequest
        if self.options.sidequest_battles:
            character_recruitments = character_recruit_locations
        else:
            character_recruitments = [
                character for character in character_recruit_locations if character not in sidequest_battle_locations
            ]
        included_locations.extend(character_recruitments)

        # Shop unlocks are always in
        included_locations.extend(shop_unlock_locations)

        # Ramza form unlocks are always in
        included_locations.extend(ramza_job_unlock_locations)

        # Optional locations
        if self.options.sidequest_battles:
            included_locations.extend(sidequest_battle_locations)
            included_locations.extend(sidequest_stone_locations)
        if self.options.job_unlocks:
            included_locations.extend(job_unlock_locations)
        if self.options.rare_battles:
            included_locations.extend(rare_battle_locations)
        if self.options.move_find_item_locations:
            included_locations.extend(main_mfi_locations)
            if self.options.sidequest_battles:
                included_locations.extend(sidequest_mfi_locations)
            if self.options.move_find_item_location_logic == self.options.move_find_item_location_logic.option_vanilla:
                included_locations.remove(LocationNames.BERVENIA_VOLCANO_MFI_2)


        if self.options.final_battles == self.options.final_battles.option_vanilla:
            self.murond_fights.extend([fight.value for fight in default_murond_fights])

        self.included_locations = [location.value for location in included_locations]

        if self.options.poach_locations:
            if (self.options.enemy_randomizer == self.options.enemy_randomizer.option_randomized
                    or self.options.enemy_randomizer == self.options.enemy_randomizer.option_boss_shuffle_randomized):
                for monster_location in monster_locations:
                    monster_name = monster_location.monster_name
                    monster_family = monster_family_lookup[monster_name]
                    total_requirements = []
                    for monster in monster_families[monster_family]:
                        total_requirements.extend(self.poach_locations[monster])
                    if len(total_requirements) > 0:
                        self.included_locations.append(f"Poach {monster_name.value}")
            else:
                self.included_locations.extend(monster_location_names)

        # Make Zodiac Stones local if option is set
        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_anywhere_local:
            self.options.local_items.value |= set(zodiac_stone_names)

        self.zodiac_stones_required = self.options.zodiac_stones_required.value
        self.zodiac_stones_in_pool = self.options.zodiac_stones_in_pool.value
        # Determine number of zodiac stones based on options
        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_vanilla_stones:
            max_stones = len(story_stone_locations)
            if self.options.final_battles == self.options.final_battles.option_altima_only:
                max_stones += len(altima_only_stone_locations)
            if self.options.sidequest_battles:
                max_stones += len(sidequest_stone_locations)
            self.zodiac_stones_required = min(self.zodiac_stones_required, max_stones)
            self.zodiac_stones_in_pool = min(self.zodiac_stones_in_pool, max_stones)
        if self.zodiac_stones_in_pool < self.zodiac_stones_required:
            self.zodiac_stones_in_pool = self.zodiac_stones_required

        early_items_dict = {}
        if self.options.early_pass:
            early_pass = self.random.choice(["Fovoham Pass", "Lesalia Pass", "Murond Pass"])
            early_items_dict.update({early_pass: 1})
        if self.options.chemist_placement == self.options.chemist_placement.option_early:
            early_items_dict["Chemist"] = 1
        self.multiworld.early_items[self.player].update(early_items_dict)

        if (self.options.chemist_placement == self.options.chemist_placement.option_starting
                and self.options.job_unlocks == self.options.job_unlocks.option_true):
            self.options.start_inventory_from_pool.value.update({"Chemist": 1})
            #self.push_precollected(self.create_item("Chemist"))

        if self.options.starting_shop_level > 0:
            shop_level = self.options.starting_shop_level.value
            self.options.start_inventory_from_pool.value.update({"Progressive Shop Level": shop_level})
            #for i in range(shop_level):
            #    self.push_precollected(self.create_item("Progressive Shop Level"))

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region_data in all_regions:
            region = Region(region_data.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Will be adjusted for different starting regions.
        starting_region = self.get_region("Gariland")
        menu.connect(starting_region)
        self.options.start_inventory.value[self.starting_pass] = 1

        # Debug lists
        gallione_locations = []
        fovoham_locations = []
        lesalia_locations = []
        lionel_locations = []
        zeltennia_locations = []
        limberry_locations = []
        murond_locations = []

        # Define connections
        locations_to_add = []
        for origin_region_data in all_regions:
            origin_region = self.get_region(origin_region_data.name)
            for connection in origin_region_data.connections:
                connecting_region = self.get_region(connection.destination.name)
                logic_object = LogicObject(self.player, self.options, 0, self.zodiac_stones_required)
                if self.debug:
                    print(f"Connection: {origin_region.name} to {connecting_region.name}")
                logic_object.requirements = create_logic_rule_for_list(
                    connection.requirements,
                    self.options,
                    self.debug)
                connection_name = f"{origin_region.name} to {connecting_region.name}"
                self.create_entrance(origin_region, connecting_region, logic_object.get_logic_rule(), connection_name)
            for location in origin_region_data.locations:
                if origin_region_data in gallione_regions:
                    gallione_locations.append(location)
                if origin_region_data in fovoham_regions:
                    fovoham_locations.append(location)
                if origin_region_data in lesalia_regions:
                    lesalia_locations.append(location)
                if origin_region_data in lionel_regions:
                    lionel_locations.append(location)
                if origin_region_data in zeltennia_regions:
                    zeltennia_locations.append(location)
                if origin_region_data in limberry_regions:
                    limberry_locations.append(location)
                if origin_region_data in murond_regions:
                    murond_locations.append(location)
                if not location.check_enabled(self.options):
                    if self.debug:
                        print(f"Excluding {location}")
                    continue
                new_location = FinalFantasyTacticsIILocation(
                    self.player,
                    location.name,
                    self.location_name_to_id[location.name],
                    origin_region
                )
                locations_to_add.append(new_location)
        locations_to_add.sort(key=lambda loc: location_sort_list_names.index(loc.name))
        for location in locations_to_add:
            if location.name in self.included_locations:
                location.parent_region.locations.append(location)
        for region in jobs_regions:
            menu.connect(self.get_region(region.name))

        poach_region = Region("Poaching", self.player, self.multiworld)
        self.multiworld.regions.append(poach_region)
        menu.connect(poach_region)
        if self.options.poach_locations:
            for poach_location in monster_location_names:
                new_location = FinalFantasyTacticsIILocation(
                    self.player, poach_location, self.location_name_to_id[poach_location], poach_region
                )
                if new_location.name in self.included_locations:
                    poach_region.locations.append(new_location)
                else:
                    self.excluded_monster_locations.append(poach_location)

        victory_location = self.get_location(LocationNames.AIRSHIPS_2_STORY.value)
        victory_location.place_locked_item(self.create_item("Farlem"))

        # Debug print list and number of locations for analysis purposes
        if self.debug:
            all_region_locations = {
                "Gallione": gallione_locations,
                "Fovoham": fovoham_locations,
                "Lesalia": lesalia_locations,
                "Lionel": lionel_locations,
                "Zeltennia": zeltennia_locations,
                "Limberry": limberry_locations,
                "Murond": murond_locations
            }
            with open("fftlocations.txt", "w") as file:
                for key, value in all_region_locations.items():
                    locations = [location.name for location in value if location.name in self.included_locations]
                    file.write(f"{key} Locations ({len(locations)}):\n")
                    for location in locations:
                        file.write(f"{location}\n")
                    file.write("\n")

        if self.debug:
            from Utils import visualize_regions
            visualize_regions(self.get_region("Menu"), f"fftdiagram{self.player}.puml")

    def create_items(self):

        # Get all world map passes we don't start with
        world_map_passes = [item for item in world_map_pass_names if item != self.starting_pass]
        self.push_precollected(self.create_item(self.starting_pass))

        # Squire is always unlocked
        self.options.start_inventory.value["Squire"] = 1
        self.push_precollected(self.create_item("Squire"))

        # If we don't have jobs in the pool, we "start" with them all
        if not self.options.job_unlocks:
            for job_name in earned_job_names:
                self.options.start_inventory.value[job_name] = 1
                self.push_precollected(self.create_item(job_name))

        # Pick Zodiac Stones to place ingame
        zodiac_stones_in_game = self.random.sample(zodiac_stone_names, k=self.zodiac_stones_in_pool)

        # Handle major items
        major_items = [
           *world_map_passes, *shop_levels, *special_character_names, *ramza_job_levels
        ]

        # Place Zodiac Stones if stones are in vanilla spots. Otherwise, add them to itempool.
        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_vanilla_stones:
            stone_locations = [location.value for location in story_stone_locations]
            if self.options.sidequest_battles:
                stone_locations.extend([location.value for location in sidequest_stone_locations])
            if self.options.final_battles == self.options.final_battles.option_altima_only:
                stone_locations.extend([location.value for location in altima_only_stone_locations])
            stone_locations_pruned = self.random.sample(stone_locations, k=self.zodiac_stones_in_pool)
            self.random.shuffle(stone_locations)
            for stone in zodiac_stones_in_game:
                self.get_location(stone_locations_pruned.pop()).place_locked_item(self.create_item(stone))
        else:
            major_items.extend(zodiac_stones_in_game)

        # Add jobs if they're items
        if self.options.job_unlocks:
            major_items.extend(earned_job_names)

        # Get unfilled location count.
        world_locations = self.multiworld.get_unfilled_locations(self.player)
        location_count = len(world_locations)

        # Get filler item count and determine filler pool
        filler_item_count = location_count - len(major_items)
        filler_items = self.determine_filler_item_pool(filler_item_count)

        # Create items
        itempool = [*major_items, *filler_items]
        for item in map(self.create_item, itempool):
            self.multiworld.itempool.append(item)

    def determine_filler_item_pool(self, filler_item_count: int) -> list[str]:
        filler_lists = []
        normal_weight = self.options.normal_item_weight.value
        rare_weight = self.options.rare_item_weight.value
        gil_weight = self.options.bonus_gil_item_weight.value
        jp_weight = self.options.jp_boon_item_weight.value

        # Shortcut if everything's the same weight (or if someone gets funny and sets them all to zero)
        if normal_weight == rare_weight == gil_weight == jp_weight:
            filler_lists = [shop_item_names, rare_item_names, gil_item_names_weighted, jp_item_names_weighted]
        else:
            # One instance of a list per weight value
            for i in range(normal_weight):
                filler_lists.append(shop_item_names)
            for i in range(rare_weight):
                filler_lists.append(rare_item_names)
            for i in range(gil_weight):
                filler_lists.append(gil_item_names_weighted)
            for i in range(jp_weight):
                filler_lists.append(jp_item_names_weighted)
        all_filler = []
        for filler_list in filler_lists:
            all_filler.extend(filler_list)
        filler_set = set(all_filler)
        self.filler_items = sorted(list(filler_set))

        return_list = []
        # For every itempool slot, just pull a random item from each pool in order based on weight
        # Could change this if we want the weights to be random and not static
        for i in range(filler_item_count):
            chosen_list = filler_lists[i % len(filler_lists)]
            chosen_item = self.random.choice(chosen_list)
            return_list.append(chosen_item)
        return return_list

    def set_rules(self):
        monster_family_logic_rules: dict[MonsterFamilies, Rule["FinalFantasyTacticsIvaliceIslandWorld"]] = dict()
        for location in all_locations:
            # Handle MFI in a little bit
            if location.name in mfi_location_names:
                continue
            # Locations that aren't real don't get rules set, of course
            if location.name not in self.included_locations:
                ap_location = None
            else:
                ap_location = self.get_location(location.name)
            if location.name in monster_location_names:
                # Poach locations rules
                if self.options.enemy_randomizer == self.options.enemy_randomizer.option_randomized:
                    # Enemy rando logic
                    monster_object = monster_locations_lookup[location.name[6:]]
                    monster_family_name = monster_family_lookup[monster_object.monster_name]
                    monster_family = [
                        monster_locations_lookup[monster_name.value] for monster_name in
                        monster_families[monster_family_name]
                    ]
                    breed_logic_object = PoachLogicObject(self.player, self.options)
                    breed_logic_object.requirements = []
                    for monster in monster_family:
                        breed_logic_object.requirements.extend(self.poach_locations[monster.monster_name])
                    breed_access_rule = breed_logic_object.get_poach_logic_rule()
                    full_access_rule = breed_access_rule & Has("Thief") & Has("Mediator")
                    monster_family_logic_rules[MonsterFamilies(monster_family_name)] = breed_access_rule
                    # Locations that aren't real don't get rules set, of course
                    if location.name not in self.included_locations:
                        continue
                    self.set_rule(ap_location, full_access_rule)
                else:
                    # Normal poach logic
                    monster_object = monster_locations_lookup[location.name[6:]]
                    monster_family_name = monster_family_lookup[monster_object.monster_name]
                    monster_family = [
                        monster_locations_lookup[monster_name.value] for monster_name in
                        monster_families[monster_family_name]
                    ]
                    poach_logic_object = PoachLogicObject(self.player, self.options)
                    poach_logic_object.requirements = monster_object.compiled_requirements
                    breed_logic_object = PoachLogicObject(self.player, self.options)
                    breed_logic_object.requirements = []
                    for monster in monster_family:
                        breed_logic_object.requirements.extend(monster.compiled_requirements)
                    poach_access_rule = poach_logic_object.get_poach_logic_rule()
                    breed_access_rule = breed_logic_object.get_poach_logic_rule()
                    full_access_rule = (poach_access_rule | (breed_access_rule & Has("Mediator"))) & Has("Thief")
                    monster_family_logic_rules[MonsterFamilies(monster_family_name)] = breed_access_rule
                    # Locations that aren't real don't get rules set, of course
                    if location.name not in self.included_locations:
                        continue
                    self.set_rule(ap_location, full_access_rule)
            else:
                # Locations that aren't real don't get rules set, of course
                if location.name not in self.included_locations:
                    continue
                # Regular location rules
                logic_object = LogicObject(self.player, self.options, location.battle_level, self.zodiac_stones_required)
                if self.debug:
                    print(f"\n{location.name} requirements (Battle level {location.battle_level}):")
                logic_object.requirements = create_logic_rule_for_list(
                    location.requirements, self.options, self.debug)
                access_rule = logic_object.get_logic_rule()
                if location.name in rare_battle_location_names:
                    access_rule &= Has("Progressive Shop Level", count=8)
                self.set_rule(ap_location, access_rule)
        four_jump_jobs = ["Monk", "Thief", "Lancer", "Ninja"]
        # Teleport, Ignore Height, and Fly all ignore jump requirements.
        movement_ability_jobs = ["Time Mage", "Lancer", "Bard", "Dancer"]
        # Rule only applies when logic is set to not default.
        mfinotdefaultfilter = [OptionFilter(MoveFindItemLocationLogic, 0, operator="ne")]
        # Rule only applies when logic is set to blue team innate
        mfiblueteaminnatefilter = [OptionFilter(MoveFindItemLocationLogic, 2, operator="eq")]
        # Rule only applies when logic is set to default or chemist innate
        mfinotblueteaminnatefilter = [OptionFilter(MoveFindItemLocationLogic, 2, operator="ne")]

        mediator_rule = Has("Mediator")

        # Can we refcruit a large monster?
        large_monster_rule = False_()
        large_monster_present = False
        for family in large_monster_families:
            large_monster_present = True
            large_monster_rule |= monster_family_logic_rules[family]
        if large_monster_present:
            large_monster_rule &= mediator_rule

        # Can we recruit a flying monster on Blue Team Innate?
        flying_monster_rule = False_()
        flying_monster_present = False
        for family in flying_monster_families:
            flying_monster_present = True
            flying_monster_rule |= monster_family_logic_rules[family]
        if flying_monster_present:
            flying_monster_rule &= mediator_rule
            flying_monster_rule = Filtered(flying_monster_rule, options=mfiblueteaminnatefilter)

        # Can we recruit a monster that can move on lava on Blue Team Innate?
        lava_monster_rule = False_()
        lava_monster_present = False
        for family in lava_monster_families:
            lava_monster_present = True
            lava_monster_rule |= monster_family_logic_rules[family]
        if lava_monster_present:
            lava_monster_rule &= mediator_rule
            lava_monster_rule = Filtered(lava_monster_rule, options=mfiblueteaminnatefilter)

        # Foundational rules
        spike_shoes_rule = Has("Progressive Shop Level", count=4)
        four_jump_jobs_rule = HasAny(*four_jump_jobs)
        filtered_four_jump_jobs_rule = Filtered(four_jump_jobs_rule, options=mfiblueteaminnatefilter)
        movement_ability_rule = Filtered(HasAny(*movement_ability_jobs), options=mfinotdefaultfilter)
        movement_ability_rule |= flying_monster_rule

        # Archer on not default can boost Jump by 1, but can't boost Jump to 5 unless we're on Blue Team Innate
        archer_rule = Filtered(Has("Archer", options=mfinotdefaultfilter))
        archer_innate_rule = Filtered(Has("Archer", options=mfiblueteaminnatefilter))

        four_jump_job_plus_one_rule = four_jump_jobs_rule & (spike_shoes_rule | archer_innate_rule)
        three_jump_job_plus_two_rule = spike_shoes_rule & archer_rule

        four_jump_rule = spike_shoes_rule | four_jump_jobs_rule | archer_rule | movement_ability_rule
        five_jump_rule = four_jump_job_plus_one_rule | three_jump_job_plus_two_rule | movement_ability_rule

        dancer_rule = Filtered(Has("Dancer") & (filtered_four_jump_jobs_rule | spike_shoes_rule), options=mfinotdefaultfilter)

        lava_movement_rule = HasAny("Geomancer", "Time Mage")

        # Can we recruit a Chocobo to jump us close enough to where we need to be?
        chocobo_ferry_rule = monster_family_logic_rules[MonsterFamilies.CHOCOBO] & mediator_rule

        for location in all_locations:
            # Locations that aren't real don't get rules set, of course
            if location.name not in self.included_locations:
                continue
            if location.name not in mfi_location_names:
                continue
            logic_object = LogicObject(self.player, self.options, location.battle_level, self.zodiac_stones_required)
            logic_object.requirements = create_logic_rule_for_list(location.requirements, self.options, self.debug)
            access_rule = logic_object.get_logic_rule()
            access_rule &= Has("Chemist", options=mfinotblueteaminnatefilter, filtered_resolution=True)
            if location.name in four_jump_mfi_locations:
                if location.name in chocobo_ferry_exclusion_locations:
                    access_rule &= four_jump_rule | large_monster_rule
                else:
                    access_rule &= four_jump_rule | large_monster_rule | chocobo_ferry_rule
            if location.name in five_jump_mfi_locations:
                if location.name in chocobo_ferry_exclusion_locations:
                    access_rule &= five_jump_rule | large_monster_rule
                else:
                    access_rule &= five_jump_rule | large_monster_rule | chocobo_ferry_rule
            if location.name in lava_mfi_locations:
                access_rule &= lava_movement_rule | lava_monster_rule
            if location.name in [LocationNames.NELVESKA_MFI_1.value, LocationNames.NELVESKA_MFI_4.value]:
                 access_rule &= (four_jump_rule & large_monster_rule) | movement_ability_rule | dancer_rule
            self.set_rule(self.get_location(location.name), access_rule)


        # Victory condition
        self.set_completion_rule(Has("Farlem"))

    def pre_fill(self) -> None:
        pass

    def generate_basic(self):
        pass

    def generate_output(self, output_directory: str) -> None:
        patch_dict: dict[str, Any] = dict()
        # Hash of the MW seed to associate with save file
        patch_dict["SeedHash"] = self.multiworld.seed % 0x7FFF
        patch_dict["Seed"] = self.multiworld.seed + self.player
        patch_dict["APJobs"] = self.options.job_unlocks.value
        patch_dict["RareBattles"] = self.options.rare_battles.value
        patch_dict["Sidequests"] = self.options.sidequest_battles.value
        patch_dict["FinalBattles"] = self.options.final_battles.value
        patch_dict["RequiredStones"] = self.zodiac_stones_required
        patch_dict["EXPMultiplier"] = self.options.exp_gain_multiplier.value
        patch_dict["JPMultiplier"] = self.options.jp_gain_multiplier.value
        patch_dict["RandomizeGariland"] = self.options.randomize_gariland.value
        patch_dict["BossShuffle"] = self.options.enemy_randomizer.value
        patch_dict["MFILogic"] = self.options.move_find_item_location_logic.value
        patch_dict["VanillaChanges"] = list(self.options.vanilla_changes.value)
        patch_dict["Transmooglifier"] = []
        if self.options.enable_transmooglifier:
            transmooglifier_option_count = len(self.options.transmooglifier_options.value)
            chosen_options = self.random.sample(sorted(list(self.options.transmooglifier_options.value)),
                                                min(3, transmooglifier_option_count))
            if len(chosen_options) < 3:
                remaining_options = sorted(
                    [key for key in self.options.transmooglifier_options.valid_keys if key not in chosen_options])
                chosen_options.extend(self.random.sample(remaining_options, 3 - len(chosen_options)))
            patch_dict["Transmooglifier"] = chosen_options

        patch_dict["LocationDict"] = self.create_location_dict()
        patch_dict["SlotData"] = self.fill_slot_data()

        new_enemy_rando_dict = {}
        for key, value in self.enemy_rando_mapping.items():
            new_list = []
            for mapping in value:
                new_list.append(mapping.to_json())
            new_enemy_rando_dict[key.value] = new_list
        patch_dict["EnemyRandoMapping"] = new_enemy_rando_dict

        if self.options.randomize_move_find_item_rewards > self.options.randomize_move_find_item_rewards.option_off:
            mfi_rando_dict = {}
            for map_id in self.mfi_rewards.keys():
                mfi_list = []
                for i in range(4):
                    map_dict = {
                        "Common": self.mfi_rewards[map_id][i][0],
                        "Rare": self.mfi_rewards[map_id][i][1]
                    }
                    mfi_list.append(map_dict)
                mfi_rando_dict[map_id] = mfi_list
            patch_dict["MFIRandoMapping"] = mfi_rando_dict

        if self.options.randomize_poach_rewards > self.options.randomize_poach_rewards.option_off:
            patch_dict["PoachRewards"] = self.poach_rewards

        rom_name_text = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        patch_dict["RomName"] = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'

        patch_dict["OutputFile"] = f'{self.multiworld.get_out_file_name_base(self.player)}'

        patch = FinalFantasyTacticsIIProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_file.json", json.dumps(patch_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def create_location_dict(self):
        locations = self.get_locations()
        location_dict = dict()
        for location in locations:
            if location.name not in locations_with_text:
                continue
            item_locations = [location.name]
            if location.name in linked_reward_names.keys():
                for linked_location in linked_reward_names[location.name]:
                    item_locations.append(linked_location)
            item_strings = []
            is_any_progression: bool = False
            for location_name in item_locations:
                ap_location = self.get_location(location_name)
                item = ap_location.item
                if item.classification & ItemClassification.progression:
                    is_any_progression = True
                    classification = ItemClassification.progression
                elif item.classification & ItemClassification.useful:
                    classification = ItemClassification.useful
                elif item.classification & ItemClassification.trap:
                    classification = ItemClassification.trap
                else:
                    classification = ItemClassification.filler
                player = item.player
                if player == self.player:
                    text = create_text_for_own_item(item.name, classification)
                else:
                    other_game = self.multiworld.game[player]
                    other_player_name = (self.multiworld.player_name[player]
                                         .replace("{", "")
                                         .replace("}", ""))
                    is_fft = other_game == "Final Fantasy Tactics Ivalice Island"
                    text = create_text_for_offworld_item(other_player_name,
                                                         item.name,
                                                         classification,
                                                         is_fft)
                item_strings.append(text)
            if len(item_strings) > 1:
                if len(item_strings) == 2:
                    item_strings[-1] = " and " + item_strings[-1]
                else:
                    for index, string in enumerate(item_strings[0:-1]):
                        item_strings[index] = string + ", "
                    item_strings[-1] = "and " + item_strings[-1]
            terminator = "!" if is_any_progression else "."
            final_item_string = (f"{self.player_name.replace("{", "").replace("}", "")}'s party found "
                                 + "".join(item_strings) + terminator)
            location_dict[location.name] = final_item_string
        location_dict["Dev Battle"] = (f"{self.player_name.replace("{", "").replace("}", "")}'s party "
                                       f"found their own Farlem!")
        return location_dict

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name_text = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        if self.filler_items is None:
            self.filler_items = ["Potion"]
        return self.random.choice(self.filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        return_dict = self.options.as_dict(
            "bonus_gil_item_size",
            "jp_boon_size",
            "sidequest_battles",
            "rare_battles",
            "final_battles",
            "poach_locations",
            "job_unlocks",
            "logical_difficulty",
            "enemy_randomizer",
            "move_find_item_locations",
            "move_find_item_location_logic",
            "vanilla_changes"
        )
        return_dict["zodiac_stones_required"] = self.zodiac_stones_required
        poach_hints = {}
        for monster_name, hints in self.poach_hints.items():
            hint_list = [hint.get_text() for hint in hints]
            poach_hints[monster_name.value] = hint_list
        return_dict["poach_hints"] = poach_hints
        poach_database = {}
        for monster_name, requirements in self.poach_database.items():
            requirement_list = []
            for requirement in requirements:
                requirement_list.append(requirement.to_json())
            poach_database[monster_name.value] = requirement_list
        return_dict["poach_database"] = poach_database
        return_dict["excluded_monster_locations"] = self.excluded_monster_locations

        return return_dict


class FinalFantasyTacticsIIItem(Item):
    game = "Final Fantasy Tactics Ivalice Island"
