from typing import TYPE_CHECKING
from .options import AM2ROptions

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object


class AM2RLogic:
    player: int

    combat_logic: bool

    def __init__(self, world: AM2RWorld | object, player: int):
        self.player = player

        options = getattr(world, "options", None)
        if options is None and hasattr(world, "worlds") and player is not None:
            world_obj = getattr(world, "worlds", {}).get(player)
            options = getattr(world_obj, "options", None)

        combat_logic = getattr(options, "CombatLogic", None)
        self.combat_logic = bool(combat_logic and getattr(combat_logic, "value", combat_logic))

    def AM2R_can_bomb(self, state: CollectionState) -> bool:
        return state.has('Bombs', self.player) or state.has('Power Bomb', self.player, 2)

    def AM2R_can_jump(self, state: CollectionState) -> bool:
        return state.has_any({'Hi Jump', 'Space Jump', 'Bombs'}, self.player)

    def AM2R_can_fly(self, state: CollectionState) -> bool:
        return state.has_any({'Bombs', 'Space Jump'}, self.player)

    def AM2R_can_spider(self, state: CollectionState) -> bool:
        return state.has('Spider Ball', self.player) \
            or self.AM2R_can_fly(state)

    def AM2R_can_schmove(self, state: CollectionState) -> bool:
        return self.AM2R_can_spider(state) \
            or state.has('Hi Jump', self.player)

    def AM2R_has_ballspark(self, state: CollectionState) -> bool:
        return state.has_all({'Speed Booster', 'Spring Ball'}, self.player)

    def AM2R_has_health_and_ammo(self, state: CollectionState, required_damage: int, required_health: int) -> bool:
        damage = 30
        health = 100

        health += state.count("Energy Tank", self.player) * 100
        if state.has("Varia Suit", self.player):
            health *= 2
        if state.has("Gravity Suit", self.player):
            health *= 2

        damage += state.count("Missile", self.player) * 2  # Hard/Fusion only grants 2 missiles per missile pickup
        damage += state.count("Super Missile",
                              self.player) * 5  # Hard/Fusion only grants 1 super missile per super missile pickup and supers are worth 5 missiles

        return (health > required_health and damage > required_damage) or (self.combat_logic == False)

    def AM2R_can_down(self, state: CollectionState) -> bool:  # both of these fall to else and I really dont want to fix it until the full rewrite
        return state.has_all({"Speed Booster", "Ice Beam", "Super Missile"}, self.player) \
            and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state) and (state.has("Screw Attack", self.player) or state.has("Power Bomb", self.player))

    def AM2R_can_lab(self, state: CollectionState) -> bool:  # both of these fall to else and I really dont want to fix it until the full rewrite
        return state.has_all({"Speed Booster", "Ice Beam", "Super Missile"}, self.player) \
            and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state) and (state.has("Screw Attack", self.player) or state.has("Power Bomb", self.player))
