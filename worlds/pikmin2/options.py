from dataclasses import dataclass
from Options import Range, Choice, PerGameCommonOptions

class WinCondition(Choice):
    """
    Collect Louie: Beat the Titan Dweevil and collect the King of Bugs
    Collect Pokos: Collect a certain number of Pokos, defined by the poko_amount value. Logic and the client do not account for Pokos obtained from enemy corpses.
    Collect Treasure: Collect a certain number of treasures, defined by the treasure_amount value.
    """
    display_name = "Win Condition"
    option_collect_louie = 0
    option_collect_pokos = 1
    option_collect_treasure = 2
    default = 0

class PokoAmount(Range):
    """
    When Collect Pokos is selected as the goal, this will control how many Pokos are needed to beat the game. Does nothing in other goals.
    """
    display_name = "Poko Amount"
    range_start = 0
    range_end = 26985
    default = 10000

class TreasureAmount(Range):
    """
    When Collect Treasures is selected as the goal, this will control how many treasures are needed to beat the game. Does nothing in other goals.
    """
    display_name = "Treasure Amount"
    range_start = 0
    range_end = 201
    default = 201

@dataclass
class Pikmin2Options(PerGameCommonOptions):
    win_condition: WinCondition
    poko_amount: PokoAmount
    treasure_amount: TreasureAmount