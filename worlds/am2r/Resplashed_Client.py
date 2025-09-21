import asyncio
import copy
import json
import time
import random
import datetime
from asyncio import StreamReader, StreamWriter
from random import randint
from typing import List
from unittest import case

from worlds.am2r.items import item_table
from worlds.am2r.locations import get_location_datas
from .options import AM2ROptions as options

import Utils
from Utils import async_start
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser

CONNECTION_TIMING_OUT_STATUS = "Connection timing out"
CONNECTION_REFUSED_STATUS = "Connection Refused"
CONNECTION_RESET_STATUS = "Connection was reset"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"
item_location_scouts = {}
item_id_to_game_id: dict = {item.code: item.game_id for item in item_table.values()}
location_id_to_game_id: dict = {location.code: location.game_id for location in get_location_datas(None, None)}
game_id_to_location_id: dict = {location.game_id: location.code for location in get_location_datas(None, None) if location.code != None}
players = []

class AM2RCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_am2r(self):
        """Check AM2R Connection State"""
        if isinstance(self.ctx, AM2RContext):
            logger.info(f"Connection Status: {self.ctx.am2r_status}")

    def _cmd_septoggs(self):
        """Septogg information"""
        logger.info("Hi, messenger for the co-creator of the Septoggs here. The Septoggs were creatures found in the \
original MII as platforms to help samus with Space Jumping, we wanted to include them along with the Blob Throwers to \
complete the enemy roster from the original game, but had to come up with another purpose for them to work besides \
floating platforms. They do help the player, which is most noticeable in randomizer modes, but they also act as \
environmental story telling, akin to the Zebesian Roaches and Tatori from Super Metroid. This can be seen with the Baby \
Septoggs randomly appearing in certain areas with camouflage of that environment, more and more babies appearing by \
Metroid husks in the breeding grounds after more Metroids are killed in the area (to show how much damage the Metroids \
can cause to the ecosystem and establish that Septoggs are scavengers), and Baby Septoggs staying close to Elder \
Septoggs (as they feel safe next to the durable Elders)")

    def _cmd_credits(self):
        """Huge thanks to all the people listed here"""
        logger.info("AM2R Multiworld Randomizer brought to you by:")
        logger.info("Programmers: Ehseezed and DodoBirb")
        logger.info("Additional help by: Scungip")
        logger.info("Initial Multiworld Mod by: DodoBirb")
        logger.info("Resplashed Mod by: Abyssal Creature, Mystical")
        logger.info("Multisquared Mod by: Steele")
        logger.info("Sprite Artists: Abyssal Creature, Mimolette")
        logger.info("New Trap Sprites by: Mystical")
        logger.info("Special Thanks to all the beta testers and the AM2R Community Updates Team")
        logger.info("And Variable who was conned into becoming a programmer to fix issues he found")

    def _cmd_deathlink(self):
        """Toggles deathlink"""
        if isinstance(self.ctx, AM2RContext):
            self.ctx.set_deathLink = not self.ctx.set_deathLink
            if self.ctx.set_deathLink:
                self.output(f"Deathlink enabled.")
            else:
                self.output(f"Deathlink disabled.")


class AM2RContext(CommonContext):
    command_processor = AM2RCommandProcessor
    game = 'AM2R'
    items_handling = 0b111 # full remote
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.error = 0
        self.waiting_for_client = False
        self.am2r_streams: (StreamReader, StreamWriter) = None
        self.am2r_sync_task = None
        self.am2r_status = CONNECTION_INITIAL_STATUS
        self.received_locscouts = False
        self.metroids_required = 41
        self.client_requesting_scouts = False
        self.TrapSprites = 0
        self.Tozos = False
        self.deathlink_pending = None
        self.set_deathLink = False

    
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            self.waiting_for_client = True
            logger.info('No AM2R details found. Reconnect to MW server after AM2R is connected.')
            return
        
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class AM2RManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "AM2R Multiworld Client"

        self.ui = AM2RManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        global players
        if cmd == "Connected":
            players = list(self.player_names.values())
            print(players)
            self.metroids_required = args["slot_data"]["MetroidsRequired"]
            try:
                self.Tozos = args["slot_data"]["Tozos"]
                self.TrapSprites = args["slot_data"]["TrapSprites"]
            except KeyError:
                self.Tozos = False
                self.TrapSprites = 5
                self.error += 10
            try:
                if args["slot_data"]["DeathLink"]:
                    self.set_deathLink = True
            except KeyError:
                self.set_deathLink = False
                self.error += 1
        elif cmd == "LocationInfo":
            logger.info("Received Location Info")
            if self.error // 10 == 1:
                self.ui.print_json([{"text": "Seed rolled on version without Tozos or Trap Sprites options, defaulting to old behavior", "type": "color", "color": "salmon"}])
                self.ui.print_json([{"text": "Everything is fine just convince the host to update their AM2R for next time", "type": "color", "color": "salmon"}])
            if self.error % 10 == 1:
                self.ui.print_json([{"text": "Seed rolled on version without DeathLink option, defaulting to DeathLink on", "type": "color", "color": "salmon"}])
                self.ui.print_json([{"text": "Everything is fine just convince the host to update their AM2R for next time", "type": "color", "color": "salmon"}])

    def on_deathlink(self, data: dict):
        self.deathlink_pending = "whatkillsyou"
        super().on_deathlink(data)



def get_payload(ctx: AM2RContext):
    global upper, lower

    items_to_give = [item_id_to_game_id[item.item] for item in ctx.items_received if item.item in item_id_to_game_id]
    if not ctx.locations_info:
        locations = [location.code for location in get_location_datas(None, None) if location.code is not None]
        async_start(ctx.send_msgs([{"cmd": "LocationScouts", "locations": locations, "create_as_hint": 0}]))
        return json.dumps({
            "cmd": "items", "items": items_to_give 
        })

    match ctx.TrapSprites:
        case 0:
            upper = 82
            lower = 20
        case 2:
            upper = 38
            lower = 20
        case 1:
            upper = 47
            lower = 40
        case 3:
            upper = 62
            lower = 50
        case 4:
            upper = 82
            lower = 70
        case 5:
            upper = 15
            lower = 0
        case _:
            upper = 15
            lower = 0

    non_ids = [48,49,63,64,65,66,67,68,69]

    # 0b111 = full remote
    # 0b000 = bad
    # 0b001 = progression
    # 0b010 = good
    # 0b100 = trap
    if ctx.deathlink_pending == "whatkillsyou":
        return json.dumps({
            "cmd": "whatkillsyou",
        })

    if ctx.client_requesting_scouts:
        itemdict = {}
        for locationid, netitem in ctx.locations_info.items():
            itemid = randint(lower, upper)
            while itemid in non_ids:
                print("extremely loud incorrect buzzer")
                itemid = randint(lower, upper)
            gamelocation = location_id_to_game_id[locationid]
            if ctx.Tozos:
                if netitem.item in item_id_to_game_id:
                    if netitem.flags & 0b100 != 0:
                        gameitem = random.randint(lower, upper)
                    else:
                        gameitem = item_id_to_game_id[netitem.item] + 20
                elif netitem.flags & 0b001 == 1:
                    gameitem = 102 #
                else:
                    gameitem = 103
            else:
                if netitem.item in item_id_to_game_id:
                    if netitem.flags & 0b100 != 0:
                        gameitem = random.randint(lower, upper)
                    else:
                        gameitem = item_id_to_game_id[netitem.item]
                elif netitem.flags & 0b001 == 1:
                    gameitem = 100
                else:
                    gameitem = 101
            itemdict[gamelocation] = gameitem
        ret = json.dumps(
            {
                'cmd':"locations",
                'items': itemdict,
                'metroids': ctx.metroids_required
            }
        )
        return ret
    ret_payload = json.dumps(
        {
           "cmd": "items",
           "items": items_to_give,
        }
    )
    ctx.deathlink_pending = None
    return ret_payload

async def parse_payload(ctx: AM2RContext, data_decoded):
    item_list = [game_id_to_location_id[int(location)] for location in data_decoded["Items"]]
    game_finished = bool(int(data_decoded["GameCompleted"]))
    item_set = set(item_list)
    ctx.locations_checked = item_list
    new_locations = [location for location in ctx.missing_locations if location in item_set]
    if new_locations:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_locations}])
    if game_finished and not ctx.finished_game:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
        ctx.finished_game = True

async def am2r_sync_task(ctx: AM2RContext):
    global players
    logger.info("Starting AM2R connector, use /am2r for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.am2r_streams:
            (reader, writer) = ctx.am2r_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=5)
                    data_decoded = json.loads(data.decode())
                    ctx.auth = data_decoded["SlotName"]
                    ctx.password = data_decoded["SlotPass"]
                    ctx.client_requesting_scouts = not bool(int(data_decoded["SeedReceived"]))
                    await parse_payload(ctx, data_decoded)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.am2r_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.am2r_streams = None


                await ctx.update_death_link(ctx.set_deathLink)

                # if data_decoded["Deathlinked"] == True and ctx.set_deathLink:
                if True:
                    print(players)
                    rand = datetime.datetime.now().microsecond

                    if players == []:
                        players = ["Ehseezed"]

                    if ctx.auth in players:
                        players.remove(ctx.auth)
                    if "Archipelago" in players:
                        players.remove("Archipelago")

                    rand_player = random.choice(players)
                    player = ctx.auth
                    enemy = ""

                    match rand:
                        case 0:
                            reason = f"{player} was killed"
                        case 1:
                            reason = f"{player} forgot their X-Vaccine"
                        case 2:
                            reason = f"Omega Metroid landed the 0 to death on {player}"
                        case 3:
                            reason = f"{player} ran out of Energy"
                        case 4:
                            reason = f"{player}\'s controller disconnected"
                        case 5:
                            reason = f"{player} bid farewell, cruel world"
                        case 6:
                            reason = f"{player} has turned you into a tombstone"
                        case 7:
                            reason = f"What?\nKills you"
                        case 8:
                            reason = f"{player} is not feeling good...\nThey are feeling evil"
                        case 9:
                            reason = f"{player} and their friends suffered the consequences of {player}\'s actions"
                        case 10:
                            reason = f"{player} wants you to know it was a rollback hit"
                        case 11:
                            if datetime.datetime.now().weekday() != 3:
                                reason = f"{player} remembered it isn\'t Thursday yet"
                            else:
                                reason = f"{player} realized \"Thursday\" is not this Thursday"
                        case 12:
                            reason = f"{player} was slain by a Chiny Tozo"
                        case 13:
                            reason = f"Which one of you idiots decided that {player} sends DeathLinks?"
                        case 14:
                            reason = f"{player} received a DMCA takedown notice from Nintendo"
                        case 15:
                            reason = f"{player} ran out of memory"
                        case 16:
                            reason = f"{player}\'s level was divisible by 5"
                        case 17:
                            reason = f"{player} was brutally murdered by hammers and whatnot"
                        case 18:
                            reason = f"{player} is wondering if there is a better way"
                        case 19:
                            reason = f"{player} was found by the SA-X"
                        case 20:
                            reason = f"{player} just simply wanted to kill you"
                        case 21:
                            reason = f"{player}\'s power bomb did not scare the metroid"
                        case 22:
                            reason = f"{player} was not authorised by Adam"
                        case 23:
                            reason = f"{player} calls it \"Wide Beam\" and was promptly killed for it"
                        case 24:
                            reason = f"{player} has always been a bit clumsy"
                        case 25:
                            reason = f"{player} couldn\'t escape mines"
                        case 26:
                            reason = f"{player} has a modern Android device"
                        case 27:
                            reason = f"{player} was silenced for asking for a Mac port"
                        case 28:
                            reason = (f"{player} is prohibited to speak for the next 12 hours and by law has to "
                                      f"stand up for the next 4")
                        case 29:
                            reason = f"Fatal Memory Error\nOut of memory!"
                        case 30:
                            consoles = ["Color TV-Game", "NES/Famicom", "Super Famicom/SNES", "Nintendo 64", "GameCube",
                                        "Wii", "Wii U", "Nintendo Switch", "Nintendo Switch 2", "Game & Watch", "Game Boy",
                                        "Game Boy Advance", "Nintendo DS", "Nintendo 3DS", "Pokemon Mini"
                                        "Virtual Boy"]
                            reason = f"{player} was trying to port AM2R to the {random.choice(consoles)}"
                        case 31:
                            reason = f"{player}\'s blunder will be added to the skullboard"
                        case 32:
                            reason = f"{player} wants you to immagine this (https://www.youtube.com/watch?v=Ad87SqVYizA) any time they die"
                        case 33:
                            reason = f"{player} wants you to know that they are not a gamer"
                        case 34:
                            reason = f"{player} wants you to know that stick drift is real and its really annoying"
                        case 35:
                            reason = f"The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start."
                        case 36:
                            reason = f"Your honor {player} is innocent, the real criminal is the one who decided that {player} should send DeathLinks"
                        case 37:
                            reason = f"{player} was killed by a horde of angry Archipelago players for sending DeathLinks"
                        case 38:
                            reason = (f"{player}, you little fucker.  You made a shit of piece with your trash Isaac. "
                                      f"It\'s fucking bad, this trash game. I will become back my money. "
                                      f"I hope you will in your next time a cow on a trash farm you sucker.")
                        case 39:
                            reason = f"{player} has been suspended for 50 days."
                        case 40:
                            reason = f"That gameplay was ass: Multiworld Terminated"
                        case 41:
                            reason = f"For whom the wombat malls"
                        case 42:
                            reason = f"{player} insists its but a scratch"
                        case 43:
                            reason = f"{player} experienced the killer rabbit"
                        case 44:
                            reason = (f"In front of you are 2 doors. Due to budget cuts only {player} stand in front of "
                                      f"them and {player} lies 50% of the time.")
                        case 45:
                            reason = f"In front of {player} there are 2 doors. Due to budget cuts, only Ehseezed stands in front of them, and Ehseezed lies 50% of the time."
                        case 46:
                            reason = f"{player} saved the animals"
                        case 47:
                            reason = f"In front of {player} there are 2 doors. Due to budget cuts, only {rand_player} stands in front of them, and {rand_player} lies 50% of the time."
                        case 48:
                            reason = f"{player} touched the sand map"
                        case 49:
                            reason = f"Unlike the Gatordile algorithm, {player} does not stay winning"
                        case 50:
                            reason = f"{player} could not stop gambling"
                        case 51:
                            reason = f"{player} got everyone else killed making them tonight's biggest loser"
                        case 52:
                            reason = f"{player} had a bad time"
                        case 53:
                            reason = f"{player} dies a slightly embarrassing death"
                        case 54:
                            reason = f"{player} votes to lower the difficulty"
                        case 55:
                            reason = f"Not a trace of {player} will be found"
                        case 56:
                            reason = f"The planet has killed {player}"
                        case 57:
                            reason = f"That was absolutely {player}\'s fault"
                        case 58:
                            reason = f"That was definitely not {player}\'s fault"
                        case 59:
                            reason = f"Beep.. beep.. beeeeeeeeeeeeeeeee"
                        case 60:
                            reason = f"{player} was styled uppon"
                        case 61:
                            reason = f"{player} has shattered into innumerable pieces"
                        case 62:
                            reason = f"{player} fell for it"
                        case 63:
                            reason = f"{player} pixel bonked"
                        case 64:
                            reason = f"{player} was sent to the crystal"
                        case 65:
                            reason = f"{player} pulled a lever, it was the wrong one"
                        case 66:
                            reason = f"{rand_player} had the controller"
                        case 67:
                            reason = f"Mom said it was {rand_player}\'s turn on the Game Boy"
                        case 68:
                            reason = f"{player} did that to mess with {rand_player}"
                        case 69:
                            reason = f"{player} has released all the remaining hate from their world"
                        case 70:
                            reason = f"And Yet."
                        case _:
                            reason = f"Ehseezed has made an error in their code\nyou should never see this one"

                    match rand:
                        case 1:
                            reason = f"{player} was killed by {enemy}"
                        case 2:
                            reason = f"{enemy} will be celebrated for this one"
                        case 3:
                            reason = f"{player}: \"What?\"\n{enemy}: \"Kills you\""
                        case 4:
                            reason = f"{enemy} did not like the way {player} looked at them"
                        case 5:
                            reason = f"{enemy} was defending their honor"
                        case 6:
                            reason = f"{enemy} asked"

                        case _:
                            reason = f"Ehseezed has made an error in their code\nyou should never see this one"


                    await ctx.send_death(f"{reason}")



            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.am2r_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.am2r_streams = None

            if ctx.am2r_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to AM2R")
                    ctx.am2r_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.am2r_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.am2r_status = error_status
                logger.info("Lost connection to AM2R and attempting to reconnect. Use /am2r for status updates")
        else:
            try:
                logger.debug("Attempting to connect to AM2R")
                ctx.am2r_streams = await asyncio.wait_for(asyncio.open_connection("127.0.0.1", 64197), timeout=10)
                ctx.am2r_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.am2r_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.am2r_status = CONNECTION_REFUSED_STATUS
                continue


def launch():
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("AM2RClient")

    options = Utils.get_options()

    async def main(args):
        random.seed()
        ctx = AM2RContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.am2r_sync_task = asyncio.create_task(am2r_sync_task(ctx), name="AM2R Sync")
        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama

    parser = get_base_parser()
    args = parser.parse_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()