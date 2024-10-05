from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item
from BaseClasses import CollectionState
from .options import AM2ROptions
from math import ceil

if TYPE_CHECKING:
    from . import AM2RWorld


# use only to make breakables, red door and missile block checks easier
def has_missiles(state: CollectionState, player: int, options: AM2ROptions, packs: int) -> bool:
    if options.ammo_logic == 1:
        packs = ceil(
            packs * 2.5)  # on hard/fusion mode, missile packs give 2 missiles instead of 5 this value is rounded up

    if options.missile_launcher == 0:
        return True
    elif options.missile_launcher == 1:
        return state.has("Missile", player, packs)
    elif options.missile_launcher == 2:
        packs -= 1  # launcher counts as 1 pack
        return state.has("Missile Launcher", player) and state.has("Missile", player, packs)


# for super blocks and Metroid logic
def has_supers(state: CollectionState, player: int, options: AM2ROptions, packs: int) -> bool:
    if options.ammo_logic == 1:
        packs *= 2  # on hard/fusion mode, super missile packs give 1 super missile instead of 2

    if options.missile_launcher:
        packs -= 1  # launcher counts as 1 pack
        return state.has("Super Missile Launcher", player) and state.has("Super Missile", player, packs)
    else:
        return state.has("Super Missile", player, packs)


def red_door(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return has_missiles(state, player, options, 1) or has_supers(state, player, options, 1)


def has_ammo(state: CollectionState, player: int, options: AM2ROptions, health: int) -> bool:
    #  calculate by number of missiles NOT MISSILE PACKS required to kill a metroid
    m_packs = state.count("Missile", player)
    s_packs = state.count("Super Missile", player)
    m_count = 0
    s_count = 0
    health = ceil(health * (options.expected_ammo_multiplier / 100))

    if options.missile_launcher == 0:  # default starting 30 missiles
        m_count += 30

    if options.missile_launcher == 2:  # missile launcher in item pool counts as 30 missiles
        if state.has("Missile Launcher", player):
            m_count += 30
        else:  # if no launcher, then you cant fire missiles and they should not be counted towards damage total
            m_packs = 0

    if options.super_launcher:
        if state.has("Super Missile Launcher", player):  # Super Launcher counts as 1 pack
            s_packs += 1
        else:  # if no launcher, then you cant fire supers and they should not be counted towards damage total
            s_packs = 0

    if options.ammo_logic == 0:
        m_count += 5 * m_packs  # 5 missiles per pack
        s_count += 2 * s_packs  # 2 supers per pack
    else:
        m_count += 2 * m_packs  # 2 missiles per pack
        s_count += 1 * s_packs  # 1 super per pack

    damage = m_count + (s_count * 5)  # supers are worth 5 missiles of damage

    if damage >= health:
        return True
    else:
        return False


def has_powerbombs(state: CollectionState, player: int, options: AM2ROptions, packs: int) -> bool:
    if options.ammo_logic == 1:
        packs *= 2

    if not can_morph(state, player, options):
        return False

    if options.missile_launcher:
        packs -= 1  # launcher counts as 1 pack
        return state.has("Power Bomb Launcher", player) and state.has("Power Bomb", player, packs)
    else:
        return state.has("Power Bomb", player, packs)


def has_energy(state: CollectionState, player: int, options: AM2ROptions, required: int) -> bool:
    num = required
    if options.logic_dificulty == 0:  # literally baby mode
        num *= 2

    if state.has("Varia Suit", player) and state.has("Gravity Suit", player):
        num = ceil(num / 4)
    elif state.has("Varia Suit", player) or state.has("Gravity Suit", player):
        num = ceil(num / 2)

    return state.has("Energy Tank", player, num)


def can_morph(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    if options.remove_morph_ball:
        return state.has("Morph Ball", player)
    else:
        return True


def has_grip(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    if options.remove_power_grip:
        return state.has("Power Grip", player)
    else:
        return True


# a surprisingly common check because of the number of 2-3 block vertical morph tunnels
def can_morph_uppies(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return can_morph(state, player, options) and \
        (has_grip(state, player, options) or state.has("Bombs", player) or state.has("Spider Ball", player)
         or state.has("Spring Ball", player))


def can_bomb(state: CollectionState, player: int, options: AM2ROptions, packs: int) -> bool:
    return (can_morph(state, player, options) and
            (state.has("Bombs", player) or has_powerbombs(state, player, options, packs)))


def can_ibj(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    if options.logic_dificulty != 0:
        return state.has("Bombs", player) and can_morph(state, player, options)
    else:
        return False


def can_fly(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return state.has("Space Jump", player) or can_ibj(state, player, options)


def can_hi(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return state.has("Hi Jump", player) or can_fly(state, player, options)


def has_spider(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return state.has("Spider Ball", player) and can_morph(state, player, options)


def has_spring(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return state.has("Spring Ball", player) and can_morph(state, player, options)


def can_ballspark(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return state.has("Speed Booster", player) and has_spring(state, player, options)


def can_schmove(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return has_spider(state, player, options) or can_fly(state, player, options) or state.has("Hi Jump", player)


def can_spider(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return has_spider(state, player, options) or can_fly(state, player, options)


def has_metroids(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    required = options.metroids_required
    return state.has("Metroid", player, required)


def can_ouch_jump(state: CollectionState, player: int, options: AM2ROptions, energy: int) -> bool:
    if options.logic_dificulty != 0 and has_energy(state, player, options, energy):
        return True
    else:
        return False


def can_wall_jump(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    if options.logic_dificulty != 0:
        return can_schmove(state, player, options)
    else:
        return True


def can_ball(state: CollectionState, player: int, options: AM2ROptions) -> bool:
    return can_bomb(state, player, options, 1) or has_missiles(state, player, options, 2) or has_supers(state, player,
                                                                                                        options, 3)


def set_region_rules(world: "AM2RWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Main Caves -> First Alpha").access_rule = \
        lambda state: True

    world.get_entrance("Main Caves -> Guardian").access_rule = \
        lambda state: True

    world.get_entrance("Main Caves -> Hydro Station").access_rule = \
        lambda state: can_morph(state, player, options)

    world.get_entrance("Main Caves -> Mines").access_rule = \
        lambda state: has_supers(state, player, options, 1) and can_morph(state, player, options)

    world.get_entrance("Main Caves -> Industrial Complex Nest").access_rule = \
        lambda state: can_morph(state, player, options)

    world.get_entrance("Main Caves -> GFS Thoth").access_rule = \
        lambda state: True

    world.get_entrance("Main Caves -> Lower Main Caves").access_rule = \
        lambda state: can_morph_uppies(state, player, options)

    world.get_entrance("Lower Main Caves -> The Tower").access_rule = \
        lambda state: True

    world.get_entrance("Lower Main Caves -> Underwater Distribution Center").access_rule = \
        lambda state: ((can_morph(state, player, options) and has_powerbombs(state, player, options, 1)
                        or has_supers(state, player, options, 1)) and
                       (state.has("Ice Beam", player) and has_ammo(state, player, options, 1)))

    world.get_entrance("Lower Main Caves -> Deep Caves").access_rule = \
        lambda state: (can_morph(state, player, options) and has_powerbombs(state, player, options, 1) or
                       has_supers(state, player, options, 1))

    world.get_entrance("GFS Thoth -> Genesis").access_rule = \
        lambda state: can_morph(state, player, options) and has_powerbombs(state, player, options, 2)

    world.get_entrance("Guardian -> After Guardian").access_rule = \
        lambda state: True

    world.get_entrance("After Guardian -> Golden Temple").access_rule = \
        lambda state: True

    world.get_entrance("After Guardian -> Golden Temple Nest").access_rule = \
        lambda state: True

    world.get_entrance("Hydro Station -> Hydro Nest").access_rule = \
        lambda state: (can_morph(state, player, options) and
                       (state.has("Hi Jump", player) and has_grip(state, player, options)) or
                       can_fly(state, player, options) or (can_ouch_jump(state, player, options, 0)) and has_grip(state,
                                                                                                                  player,
                                                                                                                  options))

    world.get_entrance("Hydro Station -> Arachnus").access_rule = \
        lambda state: (can_morph(state, player, options) and red_door(state, player, options) and
                       can_bomb(state, player, options, 1) and can_morph_uppies(state, player, options))

    world.get_entrance("Hydro Station -> Inner Hydro Station").access_rule = \
        lambda state: can_bomb(state, player, options, 1) or state.has("Screw Attack", player)

    world.get_entrance("Hydro Station -> The Tower").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Screw Attack", player)

    world.get_entrance("Hydro Station -> The Lab").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Screw Attack", player) and has_metroids(state,
                                                                                                               player,
                                                                                                               options)

    world.get_entrance("Industrial Complex Nest -> Pre Industrial Complex").access_rule = \
        lambda state: ((can_bomb(state, player, options, 1) and can_morph_uppies(state, player, options)) or
                       (state.has("Hi Jump", player) and state.has("Speed Booster", player)))

    world.get_entrance("Pre Industrial Complex -> Complex Sand").access_rule = \
        lambda state: (can_morph(state, player, options) and (
                    (can_spider(state, player, options) or can_fly(state, player, options) or
                     (can_ouch_jump(state, player, options, 1) and state.has("Hi Jump", player))) and
                    has_ammo(state, player, options, 1) or can_morph(state, player, options) and state.has("Bombs",
                                                                                                           player)))

    world.get_entrance("Pre Industrial Complex -> Torizo Ascended").access_rule = \
        lambda state: (can_schmove(state, player, options) and red_door(state, player, options))

    world.get_entrance("Complex Sand -> Speed Industrial Complex").access_rule = \
        lambda state: can_schmove(state, player, options)

    world.get_entrance("Speed Industrial Complex -> Industrial Complex").access_rule = \
        lambda state: state.has("Speed Booster", player)

    world.get_entrance("The Tower -> Tester Lower").access_rule = \
        lambda state: can_bomb(state, player, options, 2) and can_wall_jump(state, player, options)

    world.get_entrance("The Tower -> Tester Upper").access_rule = \
        lambda state: can_bomb(state, player, options, 2) and can_wall_jump(state, player, options)

    world.get_entrance("The Tower -> Geothermal").access_rule = \
        lambda state: True

    world.get_entrance("Tester Lower -> Tester").access_rule = \
        lambda state: True

    world.get_entrance("Tester Upper -> Tester").access_rule = \
        lambda state: True

    world.get_entrance("Underwater Distribution Center -> Underwater Distro Connection").access_rule = \
        lambda state: (state.has("Gravity Suit", player) and state.has("Speed Booster", player) or
                       state.has("Ice Beam", player) and has_ammo(state, player, options, 1) and
                       (state.has("Gravity Suit", player) and state.has("Speed Booster", player) or
                        has_supers(state, player, options, 1)))

    world.get_entrance("Underwater Distribution Center -> EMP").access_rule = \
        lambda state: True

    world.get_entrance("Underwater Distribution Center -> Serris").access_rule = \
        lambda state: True

    world.get_entrance("EMP -> Post EMP").access_rule = \
        lambda state: (can_bomb(state, player, options, 2) and state.has("Speed Booster", player) and
                       state.has("EMP", player) and can_ball(state, player, options))

    world.get_entrance("Post EMP -> Pipe Hell BL").access_rule = \
        lambda state: can_bomb(state, player, options, 2)

    world.get_entrance("Pipe Hell BL -> Pipe Hell L").access_rule = \
        lambda state: state.has("Screw Attack", player)

    world.get_entrance("Pipe Hell BR -> Pipe Hell R").access_rule = \
        lambda state: state.has("Screw Attack", player)

    world.get_entrance("Pipe Hell BR -> Pipe Hell L").access_rule = \
        lambda state: can_morph(state, player, options)

    world.get_entrance("Pipe Hell L -> Pipe Hell R").access_rule = \
        lambda state: can_bomb(state, player, options, 1)

    world.get_entrance("Pipe Hell R -> Screw Attack").access_rule = \
        lambda state: (state.has("Screw Attack", player) and
                       can_schmove(state, player, options) and can_ball(state, player, options))

    world.get_entrance("Pipe Hell R -> Underwater Distro Connection").access_rule = \
        lambda state: can_morph_uppies(state, player, options)

    world.get_entrance("Serris -> Ice Beam").access_rule = \
        lambda state: (state.has("Ice Beam", player) and has_ammo(state, player, options, 1) and
                       can_morph(state, player, options))

    world.get_entrance("Fast Travel -> Golden Temple").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Screw Attack", player)

    world.get_entrance("Fast Travel -> Complex Sand").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Screw Attack", player)

    world.get_entrance("Fast Travel -> The Tower").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Screw Attack", player)

    world.get_entrance("Fast Travel -> Gravity").access_rule = \
        lambda state: can_morph(state, player, options) and (
                    state.has("Gravity Suit", player) and state.has("Space Jump", player))

    world.get_entrance("Pipe Hell L -> Fast Travel").access_rule = \
        lambda state: state.has("Screw Attack", player)

    world.get_entrance("Fast Travel -> Underwater Distribution Center").access_rule = \
        lambda state: can_ball(state, player, options)

    world.get_entrance("Gravity -> Pipe Hell Outside").access_rule = \
        lambda state: can_morph(state, player, options) and state.has("Gravity Suit", player) and state.has(
            "Space Jump", player)

    world.get_entrance("Pipe Hell Outside -> Pipe Hell R").access_rule = \
        lambda state: can_ball(state, player, options)

    world.get_entrance("Deep Caves -> Omega Nest").access_rule = \
        lambda state: ((has_powerbombs(state, player, options, 1) or state.has("Screw Attack", player)) and
                       (state.has("Ice Beam", player) and has_ammo(state, player, options, 1)) and
                       (can_morph_uppies(state, player, options) and can_bomb(state, player, options, 1)))

    world.get_entrance("Omega Nest -> The Lab").access_rule = \
        lambda state: ((can_wall_jump(state, player, options) or state.has("Speed Booster", player)) and
                       can_bomb(state, player, options, 1) and can_fly(state, player, options) and
                       has_metroids(state, player, options))

    world.get_entrance("The Lab -> Research Station").access_rule = \
        lambda state: (state.has("Ice Beam", player) and has_ammo(state, player, options, 10) and
                       state.has("Space Jump", player) and can_bomb(state, player, options, 1))

# todo: Have someone other than me verify this @Everyone
def set_location_rules_easy(world: AM2RWorld) -> None:  # currently every location is in a reachable state
    multiworld = world.multiworld
    player = world.player
    options = world.options

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Upper", player),
             lambda state: (can_bomb(state, player, options, 2) and
                           (can_fly(state, player, options) or
                            has_spider(state, player, options) and state.has("Bombs", player))))

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Lower", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Main Caves: Hi-Jump Challenge", player),
             lambda state: can_bomb(state, player, options, 1) and can_hi(state, player, options))

    set_rule(multiworld.get_location("Main Caves: Spiky Maze", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Main Caves: Shinespark Before The Pit", player),
             lambda state: state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Main Caves: Shinespark After The Pit", player),
             lambda state: state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Golden Temple: Bombs", player),
             lambda state: red_door(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Below Bombs", player),
             lambda state: can_bomb(state, player, options, 1) and red_door(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Hidden Energy Tank", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Golden Temple: Charge Beam", player),
             lambda state: red_door(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Armory Left", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory Upper", player),
             lambda state: can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Armory Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory False Wall", player),
             lambda state: can_bomb(state, player, options, 2) and can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Left", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Middle", player),
             lambda state: can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Right", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Spider Ball", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Exterior Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Guardian: Up Above", player),
             lambda state: True)

    set_rule(multiworld.get_location("Guardian: Behind The Door", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Cliff", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Side Morph Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Turbine Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Not so Secret Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Water Pressure Pre-Varia", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Varia Suit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Arachnus: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Wave Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Dead End", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Hi-Jump Boots", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Below the Walkway", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Speed Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Behind The Wall", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Above Save", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex Nest: Nest Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: In the Sand", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Side After Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Side Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Behind the Green Door", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Save Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Spazer Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus Spark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Speed Booster", player),
             lambda state: True)

    set_rule(multiworld.get_location("Torizo Ascended: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Conveyor Belt Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Doom Treadmill", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub in the Floor", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Skippy Reward", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Research Camp", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Hornoad Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Outside the Front of the Ship", player),
             lambda state: True)

    set_rule(multiworld.get_location("Genesis: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Beside Hydro Pipe", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Right Side of Tower", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: In the Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Plasma Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Tester", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Outside Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Geothermal Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Chozo", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Main Room Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Underwater Speed Hallway", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After EMP Activation", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spider Ball Crumble Spiky \"Maze\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spiky Trial Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Screw Attack", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Exterior Post-Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spectator Jail", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Gravity Suit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Serris: Ice Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Drivel Ballspark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Ramulken Lava Pool", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: After Omega", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Forgotten Alpha", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Friendly Spider", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Moe", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Larry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Curly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Freddy Fazbear", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Turbine Terror", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: The Lookout", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Recent Guardian", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: EnderMahan", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Carnage Awful", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Venom Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Something More, Something Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mimolette", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Big Cheese", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mohwir", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Chirn", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: BHHarbinger", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Abyssal Creature", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: And then there\'s this Asshole", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Guardian of Doom Treadmill", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Rawsome1234 by the Lava Lake", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Marco", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Polo", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Unga", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Gunga", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Patricia", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Variable \"GUH\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Ruler of The Tower: Slagathor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Mr.Sandman", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Anakin", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Xander", player),
             lambda state: True)

    set_rule(multiworld.get_location("EMP: Sir Zeta Commander of the Alpha Squadron", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Timmy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Tommy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Terry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Telly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Martin", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Mario", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Luigi", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Lil\' Bro", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Big Sis", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Lucina", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Epsilon", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Druid", player),
             lambda state: True)


def set_location_rules_normal(world: AM2RWorld) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Upper", player),
             lambda state: can_fly(state, player, options) and can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Lower", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Main Caves: Hi-Jump Challenge", player),
             lambda state: can_bomb(state, player, options, 1) and can_hi(state, player, options))

    set_rule(multiworld.get_location("Main Caves: Spiky Maze", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Main Caves: Shinespark Before The Pit", player),
             lambda state: state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Main Caves: Shinespark After The Pit", player),
             lambda state: state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Golden Temple: Bombs", player),
             lambda state: red_door(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Below Bombs", player),
             lambda state: red_door(state, player, options) and can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Golden Temple: Hidden Energy Tank", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Golden Temple: Charge Beam", player),
             lambda state: red_door(state, player, options) and can_morph(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Armory Left", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory Upper", player),
             lambda state: can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Armory Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory False Wall", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Left", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Middle", player),
             lambda state: can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Right", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Spider Ball", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: Exterior Ceiling", player),
             lambda state: can_spider(state, player, options) or can_fly(state, player, options))

    set_rule(multiworld.get_location("Golden Temple: EMP Room", player),
             lambda state: (state.has("EMP", player) and can_ball(state, player, options) and
             can_ballspark(state, player, options) and state.has("Screw Attack", player) and
             has_supers(state, player, options, 1) and can_bomb(state, player, options, 2)))

    set_rule(multiworld.get_location("Guardian: Up Above", player),
             lambda state: (can_spider(state, player, options) or can_fly(state, player, options)) and can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Guardian: Behind The Door", player),
             lambda state: (can_spider(state, player, options) or can_fly(state, player, options)) and has_powerbombs(state, player, options, 1))

    set_rule(multiworld.get_location("Hydro Station: Cliff", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: Side Morph Tunnel", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: Turbine Room", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Hydro Station: Not so Secret Tunnel", player),
             lambda state: (can_spider(state, player, options) or can_fly(state, player, options)) and
                           can_morph(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: Water Pressure Pre-Varia", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Hydro Station: Varia Suit", player),
             lambda state: can_bomb(state, player, options, 2) and red_door(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: EMP Room", player),
             lambda state: state.has("EMP", player) and can_ball(state, player, options) and
                           state.has("Speed Booster", player) and has_supers(state, player, options, 1))

    set_rule(multiworld.get_location("Arachnus: Boss", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Hydro Station: Wave Beam", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Upper", player),
             lambda state: can_bomb(state, player, options, 1) and can_schmove(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Lower", player),
             lambda state: can_bomb(state, player, options, 2))

    set_rule(multiworld.get_location("Hydro Station: Dead End", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Hydro Station: Hi-Jump Boots", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Upper", player),
             lambda state: can_bomb(state, player, options, 2) and can_schmove(state, player, options))

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Lower", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Hydro Nest: Below the Walkway", player),
             lambda state: can_bomb(state, player, options, 2) and
                           (has_energy(state, player, options, 1) or state.has("Gravity Suit", player)))

    set_rule(multiworld.get_location("Hydro Nest: Speed Ceiling", player),
             lambda state: state.has("Speed Booster", player) and
                           (has_energy(state, player, options, 1) or state.has("Gravity Suit", player)))

    set_rule(multiworld.get_location("Hydro Nest: Behind The Wall", player),
             lambda state: state.has("Speed Booster", player) and has_powerbombs(state, player, options, 1) and
                           (has_energy(state, player, options, 1) or state.has("Gravity Suit", player)))

    set_rule(multiworld.get_location("Industrial Complex: Above Save", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: EMP Room", player),
             lambda state: state.has("EMP", player) and
                           has_powerbombs(state, player, options, 1) and has_supers(state, player, options, 1))

    set_rule(multiworld.get_location("Industrial Complex Nest: Nest Shinespark", player),
             lambda state: state.has("Speed Booster", player) and can_bomb(state, player, options, 1) and
                           can_schmove(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: In the Sand", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Side After Tunnel", player),
             lambda state: can_schmove(state, player, options) and can_morph(state, player, options) and
                           red_door(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Complex Side Tunnel", player),
             lambda state: can_schmove(state, player, options) and can_bomb(state, player, options, 1) and
                           red_door(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Behind the Green Door", player),
             lambda state: has_supers(state, player, options, 1) and
                           has_powerbombs(state, player, options, 1) and state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Industrial Complex: Save Room", player),
             lambda state: can_schmove(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Spazer Beam", player),
             lambda state: red_door(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus Spark", player),
             lambda state: state.has("Speed Booster", player))

    set_rule(multiworld.get_location("Industrial Complex: Speed Booster", player),
             lambda state: red_door(state, player, options) and (state.has("Speed Booster", player) or can_bomb(state, player, options, 2)))

    set_rule(multiworld.get_location("Torizo Ascended: Boss", player),
             lambda state: can_schmove(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Conveyor Belt Room", player),
             lambda state: can_morph(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Doom Treadmill", player),
             lambda state: can_bomb(state, player, options, 1))

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub Shinespark", player),
             lambda state: can_bomb(state, player, options, 1) and can_morph_uppies(state, player, options))

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub in the Floor", player),
             lambda state: can_bomb(state, player, options, 1) and can_morph_uppies(state, player, options) and
             has_supers(state, player, options, 1))

    set_rule(multiworld.get_location("Industrial Complex: Skippy Reward", player),
             lambda state: can_bomb(state, player, options, 1) and can_morph_uppies(state, player, options) and
             has_supers(state, player, options, 4))

    set_rule(multiworld.get_location("GFS Thoth: Research Camp", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Hornoad Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Outside the Front of the Ship", player),
             lambda state: True)

    set_rule(multiworld.get_location("Genesis: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Beside Hydro Pipe", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Right Side of Tower", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: In the Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Plasma Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Tester", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Outside Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Geothermal Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Chozo", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Main Room Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Underwater Speed Hallway", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After EMP Activation", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spider Ball Crumble Spiky \"Maze\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spiky Trial Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Screw Attack", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Exterior Post-Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spectator Jail", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Gravity Suit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Serris: Ice Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Drivel Ballspark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Ramulken Lava Pool", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: After Omega", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Forgotten Alpha", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Friendly Spider", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Moe", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Larry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Curly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Freddy Fazbear", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Turbine Terror", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: The Lookout", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Recent Guardian", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: EnderMahan", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Carnage Awful", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Venom Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Something More, Something Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mimolette", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Big Cheese", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mohwir", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Chirn", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: BHHarbinger", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Abyssal Creature", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: And then there\'s this Asshole", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Guardian of Doom Treadmill", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Rawsome1234 by the Lava Lake", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Marco", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Polo", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Unga", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Gunga", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Patricia", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Variable \"GUH\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Ruler of The Tower: Slagathor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Mr.Sandman", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Anakin", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Xander", player),
             lambda state: True)

    set_rule(multiworld.get_location("EMP: Sir Zeta Commander of the Alpha Squadron", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Timmy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Tommy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Terry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Telly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Martin", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Mario", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Luigi", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Lil\' Bro", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Big Sis", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Lucina", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Epsilon", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Druid", player),
             lambda state: True)


def set_location_rules_hard(world: AM2RWorld) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Spider Ball Challenge Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Hi-Jump Challenge", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Spiky Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Shinespark Before The Pit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Shinespark After The Pit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Bombs", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Below Bombs", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Hidden Energy Tank", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Charge Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory Left", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Armory False Wall", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Left", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Middle", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: 3-Orb Hallway Right", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Spider Ball", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Exterior Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Guardian: Up Above", player),
             lambda state: True)

    set_rule(multiworld.get_location("Guardian: Behind The Door", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Cliff", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Side Morph Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Turbine Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Not so Secret Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Water Pressure Pre-Varia", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Varia Suit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Arachnus: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Wave Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Below Tower Pipe Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Dead End", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Hi-Jump Boots", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Upper", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Behind Hi-Jump Boots Lower", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Below the Walkway", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Speed Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Behind The Wall", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Above Save", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: EMP Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex Nest: Nest Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: In the Sand", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Side After Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Side Tunnel", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Behind the Green Door", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Save Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Spazer Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus Spark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Speed Booster", player),
             lambda state: True)

    set_rule(multiworld.get_location("Torizo Ascended: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Conveyor Belt Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Doom Treadmill", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Complex Hub in the Floor", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Skippy Reward", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Research Camp", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Hornoad Room", player),
             lambda state: True)

    set_rule(multiworld.get_location("GFS Thoth: Outside the Front of the Ship", player),
             lambda state: True)

    set_rule(multiworld.get_location("Genesis: Boss", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Beside Hydro Pipe", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Right Side of Tower", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: In the Ceiling", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Dark Maze", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Plasma Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: After Tester", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Outside Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Geothermal Reactor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Chozo", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Post Reactor Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Main Room Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Underwater Speed Hallway", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After EMP Activation", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spider Ball Crumble Spiky \"Maze\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spiky Trial Shinespark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: After Spiky Trial", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Screw Attack", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Exterior Post-Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Spectator Jail", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Before Gravity", player),
             lambda state: True)

    set_rule(multiworld.get_location("Distribution Center: Gravity Suit", player),
             lambda state: True)

    set_rule(multiworld.get_location("Serris: Ice Beam", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Drivel Ballspark", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Ramulken Lava Pool", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: After Omega", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Forgotten Alpha", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple: Friendly Spider", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Moe", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Larry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Golden Temple Nest: Curly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Main Caves: Freddy Fazbear", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Turbine Terror", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: The Lookout", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Station: Recent Guardian", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: EnderMahan", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Carnage Awful", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Venom Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Hydro Nest: Something More, Something Awesome", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mimolette", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Big Cheese", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Mohwir", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: Chirn", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: BHHarbinger", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Nest: The Abyssal Creature", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: Sisyphus", player),
             lambda state: True)

    set_rule(multiworld.get_location("Industrial Complex: And then there\'s this Asshole", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Guardian of Doom Treadmill", player),
             lambda state: True)

    set_rule(multiworld.get_location("Inside Industrial: Rawsome1234 by the Lava Lake", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Marco", player),
             lambda state: True)

    set_rule(multiworld.get_location("Dual Alphas: Polo", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Unga", player),
             lambda state: True)

    set_rule(multiworld.get_location("Mines: Gunga", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Patricia", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Variable \"GUH\"", player),
             lambda state: True)

    set_rule(multiworld.get_location("Ruler of The Tower: Slagathor", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Mr.Sandman", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Anakin", player),
             lambda state: True)

    set_rule(multiworld.get_location("The Tower: Xander", player),
             lambda state: True)

    set_rule(multiworld.get_location("EMP: Sir Zeta Commander of the Alpha Squadron", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Timmy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Tommy", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Terry", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Telly", player),
             lambda state: True)

    set_rule(multiworld.get_location("Alpha Squadron: Martin", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Mario", player),
             lambda state: True)

    set_rule(multiworld.get_location("Underwater: Gamma Bros Luigi", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Lil\' Bro", player),
             lambda state: True)

    set_rule(multiworld.get_location("Deep Caves: Big Sis", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Lucina", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Epsilon", player),
             lambda state: True)

    set_rule(multiworld.get_location("Omega Nest: Druid", player),
             lambda state: True)