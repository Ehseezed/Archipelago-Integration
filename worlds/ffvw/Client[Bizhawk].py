
from NetUtils import ClientStatus, color
#from worlds.AutoSNIClient import SNIClient
#from .Regions import offset
import logging

from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


snes_logger = logging.getLogger("SNES")

ROM_NAME = (0xe72f4a, 4)

READ_DATA_START = 0x207f20
READ_DATA_END = 0x207f3f + 1

WRITE_DATA_START = 0x207f40
WRITE_DATA_END = 0x207f5f + 1

COMPLETED_GAME = (0x7e1f21, 1)

READABLE_DATA = (0x207f20, 32)
WRITABLE_DATA = (0x207f40, 32)

ITEM_CODE_START = 0x6900

IN_GAME_FLAG = (4 * 8) + 2

LOCATION_CHECKS = {
    6901: ((3 * 8) + 6, False),
    6902: ((25 * 8) + 1, False),
    6903: ((26 * 8) + 0, False),
    6904: ((29 * 8) + 2, False),
    6905: ((25 * 8) + 6, False),
    6906: ((29 * 8) + 3, False),
    6907: ((29 * 8) + 7, False),
    6908: ((29 * 8) + 6, False),
    6909: ((29 * 8) + 1, False),
    6910: ((26 * 8) + 1, False),
    6911: ((14 * 8) + 4, False),
    6912: ((29 * 8) + 5, False),
}


class FFVWClient(BizHawkClient):
    game = "Final Fantasy V: Whirlwind"
    system = "SFC"
    patch_suffix = ".apffvw"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True

        return True


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read save data
            save_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x3000100, 20, "System Bus")]
            )[0]

            # Check locations
            if save_data[2] & 0x04:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [23]
                }])

            # Send game clear
            if not ctx.finished_game and (save_data[5] & 0x01):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass


def get_flag(data, flag):
    byte = int(flag / 8)
    bit = int(0x80 / (2 ** (flag % 8)))
    return (data[byte] & bit) > 0

def validate_read_state(data1, data2):
    validation_array = bytes([0x01, 0x46, 0x46, 0x4D, 0x51, 0x52])

    if data1 is None or data2 is None:
        return False
    for i in range(6):
        if data1[i] != validation_array[i] or data2[i] != validation_array[i]:
            return False;
    return True
    

        
        
"""from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

check_1 = await snes_read(ctx, 0x207f20, 32)
received = await snes_read(ctx, READABLE_DATA[0], READABLE_DATA[1])
data = await snes_read(ctx, READ_DATA_START, READ_DATA_END - READ_DATA_START)
check_2 = await snes_read(ctx, 0x207f20, 32)
if not validate_read_state(check_1, check_2):
    return

def get_range(data_range):
    return data[data_range[0] - READ_DATA_START:data_range[0] + data_range[1] - READ_DATA_START]
completed_game = get_range(COMPLETED_GAME)

if not ctx.finished_game:
    if completed_game[0] == 1:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True

old_locations_checked = ctx.locations_checked.copy()

for container in range(256):
    if get_flag(game_flags, (0x20 * 8) + container):
        ctx.locations_checked.add(offset["Chest"] + container)

for location, data in NPC_CHECKS.items():
    if get_flag(game_flags, data[0]) is data[1]:
        ctx.locations_checked.add(location)

if old_locations_checked != ctx.locations_checked:
    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

if received[0] == 0:
    received_index = int.from_bytes(received[1:], "big")
    if received_index < len(ctx.items_received):
        item = ctx.items_received[received_index]
        received_index += 1
        code = (item.item - ITEM_CODE_START) + 1
        if code > 256:
            code -= 256
        snes_buffered_write(ctx, WRITABLE_DATA[0], bytes([0xa1, code, *received_index.to_bytes(2, "big")]))
await snes_flush_writes(ctx)"""
