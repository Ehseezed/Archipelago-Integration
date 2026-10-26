from typing import TYPE_CHECKING

from . import BattleMappingLists
from .FactoryKey import FactoryKey
from .RandomizedUnitFactory import RandomizedUnitFactory
from .SpriteSet import SpriteSet
from .. import FinalFantasyTacticsIIOptions
from .SourceUnit import SourceUnit
from .RandomizedMapping import RandomizedMapping
from .RandomizedMappings import generic_job_table, special_job_table, generic_monster_table, special_monster_table, \
    lucavi_table, altima_table
from .Job import generic_jobs, generic_monster_jobs, special_character_jobs, special_monster_jobs, lucavi_jobs, Job, \
    altima_jobs, monster_job_name_lookup
from .RandomizedPoachBattleSource import RandomizedPoachBattleSource

if TYPE_CHECKING:
    from .. import FinalFantasyTacticsIvaliceIslandWorld

battle_levels = [
    [0, 1, 1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 14],
    [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
]

def get_logic_adjusted_fight_level(fight_level: int, logical_difficulty: int):
    return battle_levels[logical_difficulty][fight_level]

def get_eligible_destination_jobs(source_unit: SourceUnit, options: "FinalFantasyTacticsIIOptions") -> dict[Job, list[FactoryKey]]:
    eligible_destination_job_table: dict[Job, list[FactoryKey]] = {}
    if source_unit.job.value in generic_jobs.keys():
        eligible_destination_job_table.update(generic_job_table)
        if options.cross_enemy_randomizer:  # if cross-class rando
            eligible_destination_job_table.update(special_job_table)
        if options.cross_species_randomizer:  # if cross-monster rando
            eligible_destination_job_table.update(generic_monster_table)
        if options.cross_enemy_randomizer and options.cross_species_randomizer:  # if both
            eligible_destination_job_table.update(special_monster_table)
            if options.lucavi_randomizer:  # if Lucavi
                eligible_destination_job_table.update(lucavi_table)
                if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
                    eligible_destination_job_table.update(altima_table)
    if source_unit.job.value in generic_monster_jobs.keys():
        eligible_destination_job_table.update(generic_monster_table)
        if options.cross_enemy_randomizer:  # if cross-class rando
            eligible_destination_job_table.update(special_monster_table)
        if options.cross_species_randomizer:  # if cross-monster rando
            eligible_destination_job_table.update(generic_job_table)
        if options.cross_enemy_randomizer and options.cross_species_randomizer:  # if both
            eligible_destination_job_table.update(special_job_table)
            if options.lucavi_randomizer:  # if Lucavi
                eligible_destination_job_table.update(lucavi_table)
                if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
                    eligible_destination_job_table.update(altima_table)
    if source_unit.job.value in special_character_jobs.keys() or source_unit.sprite_set == SpriteSet.ALGUS:
        eligible_destination_job_table.update(special_job_table)
        if options.cross_enemy_randomizer:  # if cross-class rando
            eligible_destination_job_table.update(generic_job_table)
        if options.cross_species_randomizer:  # if cross-monster rando
            eligible_destination_job_table.update(special_monster_table)
            if options.lucavi_randomizer:  # if Lucavi
                eligible_destination_job_table.update(lucavi_table)
                if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
                    eligible_destination_job_table.update(altima_table)
        if options.cross_enemy_randomizer and options.cross_species_randomizer:  # if both
            eligible_destination_job_table.update(generic_monster_table)
    if source_unit.job.value in special_monster_jobs.keys():
        eligible_destination_job_table.update(special_monster_table)
        if options.cross_enemy_randomizer:  # if cross-class rando
            eligible_destination_job_table.update(generic_monster_table)
        if options.cross_species_randomizer:  # if cross-monster rando
            eligible_destination_job_table.update(special_job_table)
        if options.cross_enemy_randomizer and options.cross_species_randomizer:  # if both
            eligible_destination_job_table.update(generic_job_table)
        if options.lucavi_randomizer:  # if Lucavi
            eligible_destination_job_table.update(lucavi_table)
            if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
                eligible_destination_job_table.update(altima_table)
    if source_unit.job.value in lucavi_jobs.keys():
        eligible_destination_job_table.update(lucavi_table)
        if options.lucavi_randomizer:  # if Lucavi
            eligible_destination_job_table.update(special_monster_table)
            if options.cross_enemy_randomizer:  # if cross-class rando
                eligible_destination_job_table.update(generic_monster_table)
            if options.cross_species_randomizer:  # if cross-monster rando
                eligible_destination_job_table.update(special_job_table)
            if options.cross_enemy_randomizer and options.cross_species_randomizer:  # if both
                eligible_destination_job_table.update(generic_job_table)
            if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
                eligible_destination_job_table.update(altima_table)
    assert len(eligible_destination_job_table) > 0, (source_unit.job.value, source_unit.job.name)
    return eligible_destination_job_table


def get_randomized_mapping(
        randomized_factories: dict[FactoryKey, RandomizedUnitFactory],
        all_factories: dict[FactoryKey, RandomizedUnitFactory],
        fight_difficulty: int,
        source_unit: SourceUnit,
        world: "FinalFantasyTacticsIvaliceIslandWorld") -> tuple[RandomizedMapping, FactoryKey]:
    eligible_factories = {
        job: factory for job, factory in randomized_factories.items()
        if factory.get_lowest_difficulty() <= fight_difficulty
    }
    eligible_destination_job_table = get_eligible_destination_jobs(source_unit, world.options)
    eligible_destination_job_table = {
        job: options for job, options in eligible_destination_job_table.items()
        if any(key in eligible_factories.keys() for key in options)
    }
    if len(eligible_destination_job_table) == 0:
        #print(f"Shuffle failed for source unit {source_unit}. Reverting to chaos for that unit.")
        eligible_factories = {
            job: factory for job, factory in all_factories.items()
            if factory.get_lowest_difficulty() <= fight_difficulty
        }
        eligible_destination_job_table = get_eligible_destination_jobs(source_unit, world.options)
        eligible_destination_job_table = {
            job: options for job, options in eligible_destination_job_table.items()
            if job in eligible_factories.keys()
        }
        if len(eligible_destination_job_table) == 0:
            eligible_factories = {
                job: factory for job, factory in all_factories.items()
                if factory.get_lowest_difficulty() <= 14
            }
            eligible_destination_job_table = get_eligible_destination_jobs(source_unit, world.options)
            eligible_destination_job_table = {
                job: options for job, options in eligible_destination_job_table.items()
                if job in eligible_factories.keys()
            }
    else:
        pass
        # print(f"Shuffle succeeded for source unit {source_unit}.")
    sorted_keys = sorted(list(eligible_destination_job_table.keys()))
    destination_job_key = world.random.choice(sorted_keys)
    destination_factory_key = world.random.choice(sorted(list(eligible_destination_job_table[destination_job_key])))
    #chosen_destination_job = world.random.choice(eligible_destination_job_table[destination_job_key])
    #chosen_factory = eligible_factories[chosen_destination_job]
    #destination_unit = chosen_factory.get_unit(fight_difficulty)
    new_mapping = RandomizedMapping(source_unit, destination_factory_key)
    new_mapping.battle_level = fight_difficulty
    new_mapping.boss_unit = source_unit.immortal
    return new_mapping, destination_factory_key

def check_if_source_unit_randomized(source_unit: SourceUnit, options: "FinalFantasyTacticsIIOptions") -> bool:
    if source_unit.job.value in altima_jobs.keys():
        if options.lucavi_randomizer == options.lucavi_randomizer.option_include_altima:
            return True
        else:
            return False
    if source_unit.job.value in lucavi_jobs.keys():
        if options.lucavi_randomizer > options.lucavi_randomizer.option_disabled:
            return True
        else:
            return False
    return True

region_lists = [
    [*BattleMappingLists.gallione_story_fights, *BattleMappingLists.gallione_only_randoms],
    BattleMappingLists.gallione_randoms_from_fovoham,
    [*BattleMappingLists.fovoham_story_fights, *BattleMappingLists.fovoham_only_randoms],
    BattleMappingLists.fovoham_randoms_from_gallione,
    BattleMappingLists.fovoham_randoms_from_lesalia,
    BattleMappingLists.fovoham_randoms_from_zeltennia,
    [*BattleMappingLists.lesalia_only_randoms, *BattleMappingLists.lesalia_story_fights],
    BattleMappingLists.lesalia_randoms_from_gallione,
    BattleMappingLists.lesalia_randoms_from_fovoham,
    BattleMappingLists.lesalia_randoms_from_lionel,
    BattleMappingLists.lesalia_randoms_from_limberry,
    [*BattleMappingLists.lionel_only_randoms, *BattleMappingLists.lionel_story_fights],
    BattleMappingLists.lionel_randoms_from_murond,
    [*BattleMappingLists.zeltennia_only_randoms, *BattleMappingLists.zeltennia_story_fights],
    BattleMappingLists.zeltennia_randoms_from_fovoham,
    BattleMappingLists.zeltennia_randoms_from_limberry,
    [*BattleMappingLists.limberry_only_randoms, *BattleMappingLists.limberry_story_fights],
    BattleMappingLists.limberry_randoms_from_zeltennia,
    BattleMappingLists.murond_story_fights,
]
region_keys = [
    "GallioneOnly",
    "GallioneFromFovoham",
    "FovohamOnly",
    "FovohamFromGallione",
    "FovohamFromLesalia",
    "FovohamFromZeltennia",
    "LesaliaOnly",
    "LesaliaFromGallione",
    "LesaliaFromFovoham",
    "LesaliaFromLionel",
    "LesaliaFromLimberry",
    "LionelOnly",
    "LionelFromMurond",
    "ZeltenniaOnly",
    "ZeltenniaFromFovoham",
    "ZeltenniaFromLimberry",
    "LimberryOnly",
    "LimberryFromZeltennia",
    "MurondOnly"
]
assert len(region_lists) == len(region_keys), (len(region_lists), len(region_keys))

def create_poach_mappings(enemy_rando_mapping):
    new_poach_locations: dict[str, set[RandomizedPoachBattleSource]] = {}
    for fight_list, region_key in zip(region_lists, region_keys):
        new_poach_locations[region_key] = set()
        for fight in fight_list:
            battle_mapping = enemy_rando_mapping[fight.battle_id]
            for source_unit in fight.source_units:
                if source_unit.immortal:
                    continue
                source_mapping = None
                for mapping in battle_mapping:
                    if mapping.source_unit == source_unit:
                        source_mapping = mapping
                        break
                if source_mapping is not None:
                    destination_job: Job = source_mapping.destination_unit
                    if destination_job is None:
                        destination_job = source_unit.job
                    if destination_job in monster_job_name_lookup.keys():
                        destination_job_name = monster_job_name_lookup[destination_job]
                        new_source = RandomizedPoachBattleSource(
                            fight.battle_level,
                            fight.battle_id.value,
                            destination_job,
                            destination_job_name)
                        new_poach_locations[region_key].add(new_source)
    return new_poach_locations

def create_default_poach_mappings():
    new_poach_locations: dict[str, set[RandomizedPoachBattleSource]] = {}
    for fight_list, region_key in zip(region_lists, region_keys):
        new_poach_locations[region_key] = set()
        for fight in fight_list:
            for source_unit in fight.source_units:
                if source_unit.immortal:
                    continue
                destination_job: Job = source_unit.job
                if destination_job in monster_job_name_lookup.keys():
                    destination_job_name = monster_job_name_lookup[destination_job]
                    new_source = RandomizedPoachBattleSource(
                        fight.battle_level,
                        fight.battle_id.value,
                        destination_job,
                        destination_job_name)
                    new_poach_locations[region_key].add(new_source)
    return new_poach_locations