import asyncio
import copy
import json
import time
import random
from asyncio import StreamReader, StreamWriter
from random import randint
from typing import List
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


class AM2RContext(CommonContext):
    command_processor = AM2RCommandProcessor
    game = 'AM2R'
    items_handling = 0b111 # full remote
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.error = None
        self.waiting_for_client = False
        self.am2r_streams: (StreamReader, StreamWriter) = None
        self.am2r_sync_task = None
        self.am2r_status = CONNECTION_INITIAL_STATUS
        self.received_locscouts = False
        self.metroids_required = 41
        self.client_requesting_scouts = False
        self.TrapSprites = 0
        self.Tozos = False
    
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
        if cmd == "Connected":
            self.metroids_required = args["slot_data"]["MetroidsRequired"]
            try:
                self.Tozos = args["slot_data"]["Tozos"]
                self.TrapSprites = args["slot_data"]["TrapSprites"]
            except KeyError:
                self.Tozos = False
                self.TrapSprites = 5
                self.error = True
        elif cmd == "LocationInfo":
            logger.info("Received Location Info")
            if self.error:
                self.ui.print_json([{"text": "Seed rolled on version without Tozos or Trap Sprites options, defaulting to old behavior", "type": "color", "color": "salmon"}])
                self.ui.print_json([{"text": "Everything is fine just convince the host to update their AM2R for next time", "type": "color", "color": "salmon"}])

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
        print("Sending")
        return json.dumps({
            'cmd':"locations", 'items': itemdict, 'metroids': ctx.metroids_required
    })
    return json.dumps({
        "cmd": "items", "items": items_to_give 
    })

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