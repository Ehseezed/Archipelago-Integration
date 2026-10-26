from copy import copy
from typing import TYPE_CHECKING

from rule_builder.rules import True_, Rule, HasGroupUnique, HasAll, Has, False_, CanReachRegion
from .data.logic.Monsters import RegionAccessRequirement
from .data.logic.Requirement import Requirement
from .Items import valid_item_names
from .Options import FinalFantasyTacticsIIOptions

if TYPE_CHECKING:
    from worlds.fftii import FinalFantasyTacticsIvaliceIslandWorld

# Number of shop progression unlocks needed to logically access a battle
easy_battle_levels =      [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 14]
normal_battle_levels =    [0, 1, 2, 3, 4, 5, 6, 7,  8,  9, 10, 11, 12, 13, 14]
difficult_battle_levels = [0, 1, 1, 2, 3, 4, 5, 5,  6,  6,  7,  8,  9, 10, 11]
extreme_battle_levels =   [0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0]
battle_levels = [easy_battle_levels, normal_battle_levels, difficult_battle_levels, extreme_battle_levels]

# 0, 2, 5, 8, and 9 correspond to formations 1, 2, 3, 4, and the rare respectively. These are hard requirements.
# Others are for story/sidequest battles. These are soft requirements.
easy_poach_battle_levels =      [0, None, 2, None, None, 5, 8, None, 8, 8, 10, None, 14, None, 14]
normal_poach_battle_levels =    [0, None, 2, None, None, 5, 6, None, 8, 8,  8, None, 12, None, 14]
difficult_poach_battle_levels = [0, None, 2, None, None, 5, 5, None, 8, 8,  6, None,  8, None, 11]
extreme_poach_battle_levels =   [0, None, 2, None, None, 5, 0, None, 8, 8,  0, None,  0, None,  0]

poach_battle_levels = [
    easy_poach_battle_levels, normal_poach_battle_levels,
    difficult_poach_battle_levels, extreme_poach_battle_levels
]

# Number of jobs required to logically access a battle
easy_job_battle_levels =      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
normal_job_battle_levels =    [1, 1, 2, 3, 3, 4, 4, 5, 6,  7,  7,  8,  9, 10, 10]
difficult_job_battle_levels = [1, 1, 1, 2, 2, 3, 3, 4, 4,  5,  5,  6,  6,  7,  7]
extreme_job_battle_levels =   [0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0]
job_battle_levels = [
    easy_job_battle_levels, normal_job_battle_levels,
    difficult_job_battle_levels, extreme_job_battle_levels
]

easy_poach_job_battle_levels =      [0, None, 2, None, None, 5, 6, None, 8, 8, 10, None, 12, None, 14]
normal_poach_job_battle_levels =    [0, None, 2, None, None, 4, 4, None, 5, 5,  7, None,  8, None, 10]
difficult_poach_job_battle_levels = [0, None, 2, None, None, 3, 3, None, 4, 4,  5, None,  6, None,  7]
extreme_poach_job_battle_levels =   [0, None, 1, None, None, 1, 1, None, 1, 1,  1, None,  1, None,  0]
poach_job_battle_levels = [
    easy_poach_job_battle_levels, normal_poach_job_battle_levels,
    difficult_poach_job_battle_levels, extreme_poach_job_battle_levels
]

class LogicObject:
    requirements: list[list[str]] = []
    player: int
    options: "FinalFantasyTacticsIIOptions"
    battle_level: int
    zodiac_stones_required: int

    def __init__(self, player: int, options: "FinalFantasyTacticsIIOptions", battle_level: int, zodiac_stones_required: int):
        self.player = player
        self.options = options
        self.battle_level = battle_level
        self.zodiac_stones_required = zodiac_stones_required

    def get_logic_rule(self) -> Rule["FinalFantasyTacticsIvaliceIslandWorld"]:
        if len(self.requirements) == 0 and self.battle_level < 1:
            return True_()
        expression: Rule | None = None
        for requirement_list in self.requirements:
            if "Zodiac Stones" in requirement_list:
                expression = HasGroupUnique("Zodiac Stones", count=self.zodiac_stones_required)
            elif expression is None:
                expression = HasAll(*requirement_list)
            else:
                expression = expression | HasAll(*requirement_list)
        if self.battle_level > 0:
            shop_level_count = battle_levels[self.options.logical_difficulty.value][self.battle_level]
            job_count = job_battle_levels[self.options.logical_difficulty.value][self.battle_level]
            shop_level_expression: Rule = Has("Progressive Shop Level", count=shop_level_count)
            job_count_expression: Rule = HasGroupUnique("Jobs", count=job_count)
            battle_level_expression: Rule = shop_level_expression & job_count_expression
            if expression is None:
                expression = battle_level_expression
            else:
                expression = expression & battle_level_expression
        if expression is None:
            return True_()
        return expression

def create_logic_rule_for_list(
        requirements: list[Requirement],
        options: "FinalFantasyTacticsIIOptions",
        debug: bool = False) -> list:
    requirements_list = []
    for requirement in requirements:
        new_rule = create_logic_rule(requirement, options, debug)
        for requirement2 in new_rule:
            requirements_list.append(requirement2)
        continue
    if debug:
        print("Create logic rule for list...")
        for requirement in requirements_list:
            print("Logic rule:")
            print(f"Requirements: {requirement}")
        print("===\n")
    return requirements_list

def create_logic_rule(
        requirement: Requirement,
        options: "FinalFantasyTacticsIIOptions",
        debug: bool = False) -> list[str]:
    if requirement.check_option_enabled(options):
        requirements_list = []
        unpack_requirement(
            requirement,
            requirements_list,
            [],
            options,
            debug)
        if debug:
            print("Create logic rule...")
            print(f"Requirement: {requirement}")
            print(f"Requirements List: [")
            for requirement in requirements_list:
                print(f"  {requirement}")
            print(f"]")
        return requirements_list
    else:
        if debug:
            print(f"Requirement {requirement.name} disabled due to options.")
        return []

def unpack_requirement(
        requirement: Requirement,
        possibilities: list[list[str]],
        parent_items: list[str],
        options: "FinalFantasyTacticsIIOptions",
        debug = False) -> None:
    if requirement.check_option_enabled(options):
        if len(requirement.other_requirements) > 0:
            for nested_requirement in requirement.other_requirements:
                current_parent_items = copy(parent_items)
                for item_needed in requirement.items_needed:
                    assert item_needed in valid_item_names, (item_needed, requirement)
                parent_items.extend(requirement.items_needed)
                unpack_requirement(
                    nested_requirement,
                    possibilities,
                    parent_items,
                    options,
                    debug
                )
                parent_items = copy(current_parent_items)
        elif len(requirement.items_needed) > 0:
            items_needed = copy(requirement.items_needed)
            for item_needed in items_needed:
                assert item_needed in valid_item_names, (item_needed, requirement)
            items_needed.extend(parent_items)
            possibilities.append(items_needed)
    else:
        if debug:
            print(f"Requirement {requirement.name} disabled due to options.")

class PoachLogicObject:
    requirements: list[RegionAccessRequirement] = []
    player: int
    options: "FinalFantasyTacticsIIOptions"

    def __init__(self, player: int, options: "FinalFantasyTacticsIIOptions"):
        self.player = player
        self.options = options

    def get_poach_logic_rule(self) -> Rule["FinalFantasyTacticsIvaliceIslandWorld"]:
        expression: Rule | None = None
        if len(self.requirements) == 0:
            return False_()
        for requirement in self.requirements:
            region_list = requirement.access_regions
            battle_level = requirement.battle_level
            region_expression: Rule | None = None
            for region in region_list:
                if region_expression is None:
                    region_expression = CanReachRegion(region.name)
                else:
                    region_expression = region_expression & CanReachRegion(region.name)
            battle_level_list = battle_levels if requirement.story else poach_battle_levels
            job_level_list = job_battle_levels if requirement.story else poach_job_battle_levels
            poach_shop_level = battle_level_list[self.options.logical_difficulty.value][battle_level]
            poach_job_count = job_level_list[self.options.logical_difficulty.value][battle_level]
            shop_level_expression: Rule = Has("Progressive Shop Level", count=poach_shop_level)
            job_count_expression: Rule = HasGroupUnique("Jobs", count=poach_job_count)
            battle_level_expression: Rule = shop_level_expression & job_count_expression
            if expression is None:
                expression = region_expression & battle_level_expression
            else:
                expression = expression | (region_expression & battle_level_expression)
        return expression