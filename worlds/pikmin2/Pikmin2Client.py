import asyncio
import psutil
import sys
import subprocess
import os
import json
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start
from NetUtils import ClientStatus
from settings import get_settings
import dolphin_memory_engine
from .watchdog import events
from .watchdog import observers

class Pikmin2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_force_relink(self):
        """Try to relink to the game if linking fails. Use with caution!"""
        try:
            f = open(self.ctx.src_path + "\\01-GPVE-Pikmin2_SaveData.gci", "rb")
            b = f.read()
            ba = bytearray(b)
            offset = 24640
            if (b[offset + 2] == ord("I")): # fake file is here, must read from second file slot instead
                offset = 73792
            # link to game
            logger.info("Linking to Pikmin 2")
            if (ba[offset + 44] == 0xBE and ba[offset + 45] == 0xEF and ba[offset + 46] == 0xCA and ba[offset + 47] == 0xFE):
                self.ctx.recv_addr = (ba[offset + 48] << 24) + (ba[offset + 49] << 16) + (ba[offset + 50] << 8) + (ba[offset + 51])
                logger.info("Found pointer at " + hex(self.ctx.recv_addr))
                # check that pointer has correct value
                # print(id, result)
                result = dolphin_memory_engine.read_bytes(self.ctx.recv_addr, 4)
                if (result == b'\xde\xad\xc0\xde'): # make sure pointer has correct value
                    # add day 1 location check
                    logger.info("Granting Day 1 check")
                    self.ctx.locations_checked.add(1)
                    # if (len(self.ctx.locations_checked) != set_len and self.ctx.mapping["VoR Courage Reactor"] != "Remote"): # if this actually changed something, move the item index. item also must be from Pikmin 2
                    #     self.ctx.recv_item_index += 1
                    logger.info("Linking successful.")
                    self.ctx.linked = True
                else:
                    logger.info(f"Linking failed. Pointer value was {result}, which is incorrect. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
            else:
                logger.info("Linking failed. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
        except Exception as e:
            logger.info(e)
    
    def _cmd_status(self):
        """Get the current game status."""
        if (self.ctx.win_condition == 0):
            logger.info(f"Goal: Collect Louie")
        elif (self.ctx.win_condition == 1):
            logger.info(f"Goal: Collect {self.ctx.poko_amount} Pokos")
        elif (self.ctx.win_condition == 2):
            logger.info(f"Goal: Collect {self.ctx.treasure_amount} Treasures")
        logger.info(f"Current Pokos (does not include enemy corpses): {calculate_pokos(self.ctx)}")
        logger.info(f"Current Treasure Count: {len(self.ctx.items_received)}")
        
    
    # def _cmd_reset_game(self):
    #     """Reset the game if you delete your save file or start a new game."""
    #     self.ctx.recv_item_index = 0
    #     logger.info("Please restart client to save changes.")
    
    # def _cmd_save_config(self):
    #     """Manually save paths to config file."""
    #     data = {}
    #     data["dolphin_executable_path"] = str(self.ctx.dolphin_executable_path)
    #     data["game_path"] = str(self.ctx.game_path)
    #     data["mapping_path"] = str(self.ctx.mapping_path)
    #     data["src_path"] = str(self.ctx.src_path)
    #     f = open("pikmin2_client_config.json", "w")
    #     json.dump(data, f)
    #     f.close()
    #     logger.info("Saved paths to config file.")

class Pikmin2Context(CommonContext):
    tags = {"AP"}
    game = "Pikmin 2"
    command_processor = Pikmin2CommandProcessor
    items_handling = 0b111
    connected = False
    linked = False
    collected = []
    recv_addr = None
    recv_item_index = 0
    game_end = False
    victory = False
    dolphin_executable_path = None
    game_path = None
    mapping_path = None
    src_path = None
    seed = None
    win_condition = None
    poko_amount = None
    treasure_amount = None
    slot_number = 0
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.pieces_needed = 0
        self.finished_game = False
        self.game = "Pikmin 2"
        self.slot_number = 0
        self.connected = False
        self.linked = False
        self.collected = []
        self.recv_addr = None
        self.game_end = False
        self.victory = False
        self.seed = None
        self.recv_item_index = 0
        self.win_condition = None
        self.poko_amount = None
        self.treasure_amount = None
        # if (os.path.exists("pikmin2_client_config.json")):
        #     f = open("pikmin2_client_config.json")
        #     data = json.load(f)
        #     self.dolphin_executable_path = Path(data["dolphin_executable_path"])
        #     self.game_path = Path(data["game_path"])
        #     self.mapping_path = Path(data["mapping_path"])
        #     self.src_path = Path(data["src_path"])
        #     f.close()

    
    def run_gui(self):
        from kvui import GameManager

        class Pikmin2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pikmin 2 Client"

        self.ui = Pikmin2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def shutdown(self):
        f = open(str("pikmin2_game_" + self.seed + ".txt"), "w")
        f.write(str(self.recv_item_index) + "\n")
        f.close()
        await super().shutdown()
    # def on_package(self, cmd: str, args: dict):
    #     if (cmd == "Connected"):
    #         print("he")
    #         connected = True
locations = [
    ("VoR Courage Reactor", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 296, "overworld", [], 0, 0),
    ("VoR Utter Scrap", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 379, "overworld", [], 0, 1),
    ("VoR Pink Menace", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 360, "overworld", ["blue"], 0, 2),
    ("VoR Spiny Alien Treat", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 277, "overworld", ["blue"], 0, 3),
    ("VoR Temporal Mechanism", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 336, "overworld_enemy", ["blue"], 0, 4),
    ("VoR Unspeakable Wonder", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 315, "overworld", ["blue"], 0, 5),
    ("VoR Fossilized Ursidae", "files\\user\\Abe\\map\\tutorial\\initgen.txt", 258, "overworld", ["blue", "yellow"], 0, 6),
    ("EC Citrus Lump", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_1.txt", 38, "cave", [], 1, 26),
    ("EC Quenching Emblem", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_1.txt", 37, "cave", [], 1, 27),
    ("EC Spherical Atlas", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_1.txt", 87, "cave", [], 2, 26),
    ("SC Exhausted Superstick", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 55, "cave", ["blue", "white"], 1, 26),
    ("SC Nouveau Table", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 56, "cave", ["blue", "white"], 1, 27),
    ("SC Network Mainbrain", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 120, "cave", ["blue", "white"], 2, 26),
    ("SC Spirit Flogger", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 121, "cave", ["blue", "white"], 2, 27),
    ("SC Coiled Launcher", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 183, "cave", ["blue", "white"], 3, 26),
    ("SC Omega Flywheel", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 182, "cave", ["blue", "white"], 3, 27),
    ("SC Superstrong Stabilizer", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 162, "cave_enemy", ["blue", "white"], 3, 28),
    ("SC Adamantine Girdle", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 312, "cave", ["blue", "white"], 5, 26),
    ("SC Mystical Disc", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 311, "cave", ["blue", "white"], 5, 27),
    ("SC Repair Juggernaut", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 376, "cave", ["blue", "white"], 6, 26),
    ("SC Space Wave Receiver", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 375, "cave", ["blue", "white"], 6, 27),
    ("SC Vacuum Processor", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 374, "cave", ["blue", "white"], 6, 28),
    ("SC Furious Adhesive", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 445, "cave", ["blue", "white"], 7, 26),
    ("SC Indomitable CPU", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 414, "cave_enemy", ["blue", "white"], 7, 27),
    ("SC Thirst Activator", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 444, "cave", ["blue", "white"], 7, 28),
    ("SC Stellar Orb", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_2.txt", 539, "cave_enemy", ["blue", "white"], 9, 26),
    ("FC Essence of Rage", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 62, "cave", ["blue"], 1, 26),
    ("FC Essential Furnishing", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 61, "cave", ["blue"], 1, 27),
    ("FC Icon of Progress", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 122, "cave", ["blue"], 2, 26),
    ("FC Joy Receptacle", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 121, "cave", ["blue"], 2, 27),
    ("FC Danger Chime", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 159, "cave_enemy", ["blue"], 3, 26),
    ("FC Fleeting Art Form", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 182, "cave", ["blue"], 3, 27),
    ("FC Gemstar Husband", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 181, "cave", ["blue"], 3, 28),
    ("FC Innocence Lost", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 255, "cave", ["blue"], 4, 26),
    ("FC Omniscient Sphere", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 256, "cave", ["blue"], 4, 27),
    ("FC Brute Knuckles", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 309, "cave_enemy", ["blue"], 5, 26),
    ("FC Priceless Statue", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 402, "cave", ["blue"], 6, 26),
    ("FC Worthless Statue", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 401, "cave", ["blue"], 6, 27),
    ("FC Flame Tiller", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 462, "cave", ["blue"], 7, 26),
    ("FC Spouse Alert", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 463, "cave", ["blue"], 7, 27),
    ("FC Repugnant Appendage", "files\\user\\Mukki\\mapunits\\caveinfo\\tutorial_3.txt", 504, "cave_enemy", ["blue"], 8, 26),
    ("AW Sunseed Berry", "files\\user\\Abe\\map\\forest\\initgen.txt", 346, "overworld", [], 0, 7),
    ("AW Chance Totem", "files\\user\\Abe\\map\\forest\\initgen.txt", 365, "overworld", ["white"], 0, 8),
    ("AW Pilgrim Bulb", "files\\user\\Abe\\map\\forest\\initgen.txt", 441, "overworld", [], 0, 9),
    ("AW Geographic Projection", "files\\user\\Abe\\map\\forest\\initgen.txt", 327, "overworld", ["white"], 0, 10),
    ("AW Healing Cask", "files\\user\\Abe\\map\\forest\\initgen.txt", 422, "overworld", ["yellow"], 0, 11),
    ("AW Decorative Goo", "files\\user\\Abe\\map\\forest\\initgen.txt", 403, "overworld", ["yellow", "blue"], 0, 12),
    ("AW Air Brake", "files\\user\\Abe\\map\\forest\\initgen.txt", 384, "overworld", ["blue"], 0, 13),
    ("HoB Stone of Glory", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 50, "cave", [], 1, 26),
    ("HoB Cosmic Archive", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 144, "cave", [], 3, 26),
    ("HoB Strife Monolith", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 145, "cave", [], 3, 27),
    ("HoB Dream Architect", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 181, "cave_enemy", [], 4, 26),
    ("HoB Luck Wafer", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 193, "cave", [], 4, 27),
    ("HoB Prototype Detector", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_1.txt", 235, "cave_enemy", [], 5, 26),
    ("WFG Alien Billboard", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 43, "cave", ["purple"], 1, 26),
    ("WFG Drought Ender", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 84, "cave", ["purple"], 2, 26),
    ("WFG Petrified Heart", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 85, "cave", ["purple"], 2, 27),
    ("WFG Superstick Textile", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 136, "cave", ["purple"], 3, 26),
    ("WFG Survival Ointment", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 177, "cave", ["purple"], 4, 26),
    ("WFG Toxic Toadstool", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 178, "cave", ["purple"], 4, 27),
    ("WFG Five-man Napsack", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_2.txt", 213, "cave_enemy", ["purple"], 5, 26),
    ("BK Crystal Clover", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 31, "cave_enemy", ["white", "yellow"], 1, 26),
    ("BK Tear Stone", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 95, "cave", ["white", "yellow"], 2, 26),
    ("BK Olimarnite Shell", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 148, "cave", ["white", "yellow"], 3, 26),
    ("BK Crystal King", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 186, "cave_enemy", ["white", "yellow"], 4, 26),
    ("BK Unknown Merit", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 188, "cave_enemy", ["white", "yellow"], 4, 27),
    ("BK Anxious Sprout", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 267, "cave", ["white", "yellow"], 5, 26),
    ("BK Colossal Fossil", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 330, "cave", ["white", "yellow"], 6, 26),
    ("BK Eternal Emerald Eye", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 308, "cave_enemy", ["white", "yellow"], 6, 27),
    ("BK Forged Courage", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 389, "cave_enemy", ["white", "yellow"], 7, 26),
    ("BK Gyroid Bust", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_3.txt", 401, "cave", ["white", "yellow"], 7, 27),
    ("SH Crystallized Telekinesis", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 32, "cave_enemy", ["blue", "white"], 1, 26),
    ("SH Leviathan Feather", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 40, "cave", ["blue", "white"], 1, 27),
    ("SH Combustion Berry", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 96, "cave", ["blue", "white"], 2, 26),
    ("SH Taste Sensation", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 97, "cave", ["blue", "white"], 2, 27),
    ("SH Meat Satchel", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 139, "cave_enemy", ["blue", "white"], 3, 26),
    ("SH Crystallized Telepathy", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 220, "cave", ["blue", "white"], 4, 26),
    ("SH Cupid's Grenade", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 219, "cave", ["blue", "white"], 4, 27),
    ("SH Heavy-duty Magnetizer", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 201, "cave_enemy", ["blue", "white"], 4, 28),
    ("SH Crystallized Clairvoyance", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 261, "cave_enemy", ["blue", "white"], 5, 26),
    ("SH Emperor Whistle", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 259, "cave_enemy", ["blue", "white"], 5, 27),
    ("SH Salivatrix", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 333, "cave", ["blue", "white"], 6, 26),
    ("SH Science Project", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 332, "cave", ["blue", "white"], 6, 27),
    ("SH Stupendous Lens", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 316, "cave_enemy", ["blue", "white"], 6, 28),
    ("SH Triple Sugar Threat", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 314, "cave_enemy", ["blue", "white"], 6, 29),
    ("SH Justice Alloy", "files\\user\\Mukki\\mapunits\\caveinfo\\forest_4.txt", 383, "cave_enemy", ["blue", "white"], 7, 26),
    ("PP Gherkin Gate", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 382, "overworld", ["yellow"], 0, 14),
    ("PP Impediment Scourge", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 420, "overworld", ["yellow"], 0, 15),
    ("PP Aquatic Mine", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 338, "overworld_enemy", ["blue"], 0, 16),
    ("PP Fortified Delicacy", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 439, "overworld", ["blue"], 0, 17),
    ("PP Onion Replica", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 458, "overworld", ["blue"], 0, 18),
    ("PP Optical Illustration", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 401, "overworld", ["blue", "yellow"], 0, 19),
    ("PP Massage Girdle", "files\\user\\Abe\\map\\yakushima\\initgen.txt", 363, "overworld", ["blue"], 0, 20),
    ("CoS Love Nugget", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 48, "cave", [], 1, 26),
    ("CoS Creative Inspiration", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 90, "cave_enemy", [], 2, 26),
    ("CoS Lip Service", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 111, "cave", [], 2, 27),
    ("CoS Paradoxical Enigma", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 110, "cave", [], 2, 28),
    ("CoS Memorial Shell", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 169, "cave", [], 3, 26),
    ("CoS Patience Tester", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 170, "cave", [], 3, 27),
    ("CoS Flame of Tomorrow", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 234, "cave", [], 4, 26),
    ("CoS King of Sweets", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 217, "cave_enemy", [], 4, 27),
    ("CoS Time Capsule", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 233, "cave", [], 4, 28),
    ("CoS Regal Diamond", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 292, "cave", [], 5, 26),
    ("CoS The Key", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_1.txt", 278, "cave_enemy", [], 5, 27),
    ("GK Master's Instrument", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 42, "cave", ["yellow"], 1, 26),
    ("GK Massive Lid", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 98, "cave", ["yellow"], 2, 26),
    ("GK Imperative Cookie", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 99, "cave", ["yellow"], 2, 27),
    ("GK Director of Destiny", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 151, "cave", ["yellow"], 3, 26),
    ("GK Harmonic Synthesizer", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 152, "cave", ["yellow"], 3, 27),
    ("GK Invigorator", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 210, "cave", ["yellow"], 4, 26),
    ("GK Happiness Emblem", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 197, "cave_enemy", ["yellow"], 4, 27),
    ("GK White Goodness", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 209, "cave", ["yellow"], 4, 28),
    ("GK Boom Cone", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 260, "cave", ["yellow"], 5, 26),
    ("GK Sulking Antenna", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 261, "cave", ["yellow"], 5, 27),
    ("GK Dream Material", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 306, "cave_enemy", ["yellow"], 6, 26),
    ("GK Hideous Victual", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 323, "cave", ["yellow"], 6, 27),
    ("GK Meat of Champions", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 322, "cave", ["yellow"], 6, 28),
    ("GK Sweet Dreamer", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_2.txt", 324, "cave", ["yellow"], 6, 29),
    ("SR Merciless Extractor", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 48, "cave", ["yellow", "blue"], 1, 26),
    ("SR Durable Energy Cell", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 115, "cave", ["yellow", "blue"], 2, 26),
    ("SR Sud Generator", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 114, "cave", ["yellow", "blue"], 2, 27),
    ("SR Mirrored Stage", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 162, "cave_enemy", ["yellow", "blue"], 3, 26),
    ("SR Scrumptious Shell", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 177, "cave", ["yellow", "blue"], 3, 27),
    ("SR Vorpal Platter", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 176, "cave", ["yellow", "blue"], 3, 28),
    ("SR Arboreal Frippery", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 245, "cave", ["yellow", "blue"], 4, 26),
    ("SR Broken Food Master", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 299, "cave", ["yellow", "blue"], 5, 26),
    ("SR Endless Repository", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 300, "cave", ["yellow", "blue"], 5, 27),
    ("SR Pondering Emblem", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 301, "cave", ["yellow", "blue"], 5, 28),
    ("SR Abstract Masterpiece", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 373, "cave", ["yellow", "blue"], 6, 26),
    ("SR Behemoth Jaw", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 372, "cave", ["yellow", "blue"], 6, 27),
    ("SR Rubber Ugly", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 371, "cave", ["yellow", "blue"], 6, 28),
    ("SR Amplified Amplifier", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_3.txt", 423, "cave_enemy", ["yellow", "blue"], 7, 26),
    ("SMGC Bug Bait", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 34, "cave_enemy", ["blue"], 1, 26),
    ("SMGC Diet Doomer", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 53, "cave", ["blue"], 1, 27),
    ("SMGC Pastry Wheel", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 52, "cave", ["blue"], 1, 28),
    ("SMGC Chocolate Cushion", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 115, "cave", ["blue"], 2, 26),
    ("SMGC Comfort Cookie", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 99, "cave_enemy", ["blue"], 2, 27),
    ("SMGC Confection Hoop", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 116, "cave", ["blue"], 2, 28),
    ("SMGC Activity Arouser", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 156, "cave_enemy", ["blue"], 3, 26),
    ("SMGC Compelling Cookie", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 176, "cave", ["blue"], 3, 27),
    ("SMGC Succulent Mattress", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 177, "cave", ["blue"], 3, 28),
    ("SMGC Drone Supplies", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 249, "cave", ["blue"], 4, 26),
    ("SMGC Pale Passion", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 239, "cave_enemy", ["blue"], 4, 27),
    ("SMGC Proton AA", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 250, "cave", ["blue"], 4, 28),
    ("SMGC Professional Noisemaker", "files\\user\\Mukki\\mapunits\\caveinfo\\yakushima_4.txt", 291, "cave_enemy", ["blue", "purple"], 5, 26),
    ("WW Doomsday Apparatus", "files\\user\\Abe\\map\\last\\initgen.txt", 221, "overworld", [], 0, 21),
    ("WW Seed of Greed", "files\\user\\Abe\\map\\last\\initgen.txt", 288, "overworld_enemy", ["blue"], 0, 22),
    ("WW Anti-hiccup Fungus", "files\\user\\Abe\\map\\last\\initgen.txt", 313, "overworld", ["blue", "white"], 0, 23),
    ("WW Armored Nut", "files\\user\\Abe\\map\\last\\initgen.txt", 261, "overworld_enemy", ["blue"], 0, 24),
    ("WW Conifer Spire", "files\\user\\Abe\\map\\last\\initgen.txt", 240, "overworld", ["yellow"], 0, 25),
    ("CoC Enamel Buster", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 56, "cave", [], 1, 26),
    ("CoC Mirth Sphere", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 55, "cave", [], 1, 27),
    ("CoC Essence of Despair", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 98, "cave_enemy", [], 2, 26),
    ("CoC Frosty Bauble", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 96, "cave_enemy", [], 2, 27),
    ("CoC Gemstar Wife", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 94, "cave_enemy", [], 2, 28),
    ("CoC Child of the Earth", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 171, "cave", [], 3, 26),
    ("CoC Infernal Vegetable", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 170, "cave", [], 3, 27),
    ("CoC Milk Tub", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 231, "cave", [], 4, 26),
    ("CoC Mysterious Remains", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 211, "cave_enemy", [], 4, 27),
    ("CoC Growshroom", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 347, "cave", [], 6, 26),
    ("CoC Princess Pearl", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 331, "cave_enemy", [], 6, 27),
    ("CoC Fuel Reservoir", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 404, "cave", [], 7, 26),
    ("CoC Impenetrable Cookie", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 382, "cave_enemy", [], 7, 27),
    ("CoC Fruit Guard", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 468, "cave", [], 8, 26),
    ("CoC Maternal Sculpture", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 522, "cave", [], 9, 26),
    ("CoC Wiggle Noggin", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 523, "cave", [], 9, 27),
    ("CoC Silencer", "files\\user\\Mukki\\mapunits\\caveinfo\\last_1.txt", 558, "cave_enemy", [], 10, 26),
    ("HoH Corpulent Nut", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 55, "cave", ["yellow"], 1, 26),
    ("HoH Essence of True Love", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 116, "cave", ["yellow"], 2, 26),
    ("HoH Love Sphere", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 177, "cave", ["yellow"], 3, 26),
    ("HoH Lustrous Element", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 217, "cave_enemy", ["yellow"], 4, 26),
    ("HoH Nutrient Silo", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 337, "cave", ["yellow", "blue"], 6, 26),
    ("HoH Joyless Jewel", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 378, "cave_enemy", ["yellow"], 7, 26),
    ("HoH Dimensional Slicer", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 476, "cave_enemy", ["yellow"], 9, 26),
    ("HoH Treasured Gyro Block", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 534, "cave_enemy", ["yellow"], 10, 26),
    ("HoH Favorite Gyro Block", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 584, "cave_enemy", ["yellow"], 11, 26),
    ("HoH Lost Gyro Block", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 628, "cave_enemy", ["yellow"], 12, 26),
    ("HoH Memorable Gyro Block", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 681, "cave_enemy", ["yellow", "blue"], 13, 26),
    ("HoH Fond Gyro Block", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 721, "cave_enemy", ["yellow", "blue"], 14, 26),
    ("HoH Remembered Old Buddy", "files\\user\\Mukki\\mapunits\\caveinfo\\last_2.txt", 785, "cave_enemy", ["yellow"], 15, 26),
    ("DD Disguised Delicacy", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 48, "cave", ["blue", "white"], 1, 26),
    ("DD Implement of Toil", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 94, "cave", ["blue", "white"], 2, 26),
    ("DD Manual Honer", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 84, "cave_enemy", ["blue", "white"], 2, 27),
    ("DD Glee Spinner", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 130, "cave_enemy", ["blue", "white"], 3, 26),
    ("DD Mirrored Element", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 203, "cave", ["blue", "white"], 4, 26),
    ("DD Insect Condo", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 239, "cave_enemy", ["blue", "white"], 5, 26),
    ("DD Future Orb", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 294, "cave_enemy", ["blue", "white"], 6, 26),
    ("DD Essence of Desire", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 346, "cave_enemy", ["blue", "white"], 7, 26),
    ("DD Extreme Perspirator", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 430, "cave", ["blue", "white"], 8, 26),
    ("DD Possessed Squash", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 429, "cave", ["blue", "white"], 8, 27),
    ("DD Talisman of Life", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 517, "cave_enemy", ["blue", "white"], 10, 26),
    ("DD Boss Stone", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 598, "cave", ["blue", "white"], 11, 26),
    ("DD Yellow Taste Tyrant", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 599, "cave", ["blue", "white"], 11, 27),
    ("DD Stringent Container", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 635, "cave_enemy", ["blue", "white"], 12, 26),
    ("DD Universal Com", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 655, "cave", ["blue", "white"], 12, 27),
    ("DD Hypnotic Platter", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", 693, "cave_enemy", ["blue", "white"], 13, 26),
    ("DD Comedy Bomb", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", -1, "cave", ["blue", "white"], 14, 26),
    ("DD Flare Cannon", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", -1, "cave", ["blue", "white"], 14, 27),
    ("DD Monster Pump", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", -1, "cave", ["blue", "white"], 14, 28),
    ("DD Shock Therapist", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", -1, "cave", ["blue", "white"], 14, 29),
    ("DD King of Bugs", "files\\user\\Mukki\\mapunits\\caveinfo\\last_3.txt", -1, "cave", ["blue", "white"], 14, 30)
]

caves = {
    0x745F3031: "EC",
    0x745F3032: "SC",
    0x745F3033: "FC",
    0x665F3031: "HoB",
    0x665F3032: "WFG",
    0x665F3033: "BK",
    0x665F3034: "SH",
    0x795F3031: "CoS",
    0x795F3032: "GK",
    0x795F3033: "SR",
    0x795F3034: "SMGC",
    0x6C5F3031: "CoC",
    0x6C5F3032: "HoH",
    0x6C5F3033: "DD"
}

items = [
    ("Rubber Ugly", "ahiru", 0, 0, 90, 8),
    ("Insect Condo", "apple", 1, 0, 40, 15),
    ("Meat Satchel", "apple_blue", 2, 0, 40, 5),
    ("Coiled Launcher", "bane", 3, 0, 70, 15),
    ("Confection Hoop", "baum_kuchen", 4, 0, 60, 20),
    ("Omniscient Sphere", "be_dama_red", 5, 0, 85, 1),
    ("Love Sphere", "be_dama_yellow", 6, 0, 85, 1),
    ("Mirth Sphere", "be_dama_blue", 7, 0, 85, 1),
    ("Maternal Sculpture", "bell", 8, 0, 55, 15),
    ("Stupendous Lens", "bey_goma", 9, 0, 120, 10),
    ("Leviathan Feather", "bird_hane", 10, 0, 10, 1),
    ("Superstrong Stabilizer", "bolt", 11, 0, 60, 10),
    ("Space Wave Receiver", "channel", 12, 0, 80, 10),
    ("Joy Receptacle", "chess_king_black", 13, 0, 60, 15),
    ("Worthless Statue", "chess_king_white", 14, 0, 80, 10),
    ("Priceless Statue", "chess_queen_black", 15, 0, 80, 10),
    ("Triple Sugar Threat", "chess_queen_white", 16, 0, 60, 6),
    ("King of Sweets", "chocolate", 17, 0, 15, 5),
    ("Diet Doomer", "chocoichigo", 18, 0, 25, 5),
    ("Pale Passion", "chocowhite", 19, 0, 25, 5),
    ("Boom Cone", "compact", 20, 0, 100, 10),
    ("Bug Bait", "cookie", 21, 0, 15, 5),
    ("Milk Tub", "creap", 22, 0, 60, 5),
    ("Petrified Heart", "diamond_red", 23, 0, 100, 5),
    ("Regal Diamond", "diamond_blue", 24, 0, 100, 5),
    ("Princess Pearl", "diamond_green", 25, 0, 100, 5),
    ("Silencer", "doll", 26, 0, 670, 20),
    ("Armored Nut", "donguri", 27, 0, 60, 4),
    ("Chocolate Cushion", "donutschoco", 28, 0, 40, 10),
    ("Sweet Dreamer", "donutsichigo", 29, 0, 40, 10),
    ("Cosmic Archive", "donutswhite", 30, 0, 230, 15),
    ("Cupid's Grenade", "flower_red", 31, 0, 20, 3),
    ("Science Project", "flower_blue", 32, 0, 20, 1),
    ("Manual Honer", "toy_gentle", 33, 0, 130, 10),
    ("Broken Food Master", "toy_lady", 34, 0, 90, 20),
    ("Sud Generator", "toy_dog", 35, 0, 60, 20),
    ("Wiggle Noggin", "toy_cat", 36, 0, 85, 15),
    ("Omega Flywheel", "gear", 37, 0, 60, 20),
    ("Lustrous Element", "gold_medal", 38, 0, 1000, 10),
    ("Superstick Textile", "gum_tape", 39, 0, 80, 30),
    ("Possessed Squash", "halloween", 40, 0, 180, 30),
    ("Gyroid Bust", "haniwa", 41, 0, 250, 10),
    ("Sunseed Berry", "ichigo", 42, 0, 170, 5),
    ("Glee Spinner", "juji_key", 43, 0, 140, 6),
    ("Decorative Goo", "kan", 44, 0, 80, 10),
    ("Anti-hiccup Fungus", "kinoko", 45, 0, 30, 5),
    ("Crystal King", "kouseki_suisyou", 46, 0, 110, 10),
    ("Fossilized Ursidae", "kumakibori", 47, 0, 160, 25),
    ("Time Capsule", "locket", 48, 0, 70, 7),
    ("Olimarnite Shell", "makigai", 49, 0, 40, 15),
    ("Conifer Spire", "matu_bokkuri", 50, 0, 15, 7),
    ("Abstract Masterpiece", "milk_cap", 51, 0, 30, 6),
    ("Arboreal Frippery", "momiji_normal", 52, 0, 10, 1),
    ("Onion Replica", "momiji_kare", 53, 0, 30, 20),
    ("Infernal Vegetable", "momiji_red", 54, 0, 30, 12),
    ("Adamantine Girdle", "nut", 55, 0, 70, 12),
    ("Director of Destiny", "tatebue", 56, 0, 100, 20),
    ("Colossal Fossil", "saru_head", 57, 0, 140, 20),
    ("Invigorator", "sensya", 58, 0, 130, 20),
    ("Vacuum Processor", "sinkukan", 59, 0, 100, 10),
    ("Mirrored Element", "silver_medal", 60, 0, 300, 10),
    ("Nouveau Table", "tel_dial", 61, 0, 100, 25),
    ("Pink Menace", "toy_ring_a_red", 62, 0, 100, 5),
    ("Frosty Bauble", "toy_ring_a_blue", 63, 0, 100, 5),
    ("Gemstar Husband", "toy_ring_a_green", 64, 0, 100, 5),
    ("Gemstar Wife", "toy_ring_b_red", 65, 0, 100, 5),
    ("Universal Com", "toy_ring_b_blue", 66, 0, 100, 5),
    ("Joyless Jewel", "toy_ring_b_green", 67, 0, 100, 5),
    ("Fleeting Art Form", "toy_ring_c_red", 68, 0, 75, 2),
    ("Innocence Lost", "toy_ring_c_green", 69, 0, 100, 15),
    ("Icon of Progress", "toy_ring_c_blue", 70, 0, 85, 15),
    ("Unspeakable Wonder", "toy_teala", 71, 0, 120, 30),
    ("Aquatic Mine", "turi_uki", 72, 0, 80, 3),
    ("Temporal Mechanism", "watch", 73, 0, 110, 30),
    ("Essential Furnishing", "Xmas_item", 74, 0, 100, 5),
    ("Flame Tiller", "yoyo_red", 75, 0, 120, 20),
    ("Doomsday Apparatus", "yoyo_yellow", 76, 0, 3000, 1000),
    ("Impediment Scourge", "yoyo_blue", 77, 0, 50, 10),
    ("Future Orb", "flask", 78, 0, 200, 25),
    ("Shock Therapist", "elec", 79, 0, 1000, 30),
    ("Flare Cannon", "fire", 80, 0, 1000, 30),
    ("Comedy Bomb", "gas", 81, 0, 1000, 30),
    ("Monster Pump", "water", 82, 0, 1000, 30),
    ("Mystical Disc", "mojiban", 83, 0, 75, 6),
    ("Vorpal Platter", "futa_a_gold", 84, 0, 60, 12),
    ("Taste Sensation", "futa_a_silver", 85, 0, 40, 15),
    ("Lip Service", "kan_b_gold", 86, 0, 50, 4),
    ("Utter Scrap", "kan_b_silver", 87, 0, 170, 35),
    ("Paradoxical Enigma", "ahiru_head", 88, 0, 80, 4),
    ("King of Bugs", "loozy", 89, 0, 10, 1),
    ("Essence of Rage", "teala_dia_a", 90, 0, 70, 8),
    ("Essence of Despair", "teala_dia_b", 91, 0, 80, 6),
    ("Essence of True Love", "teala_dia_c", 92, 0, 60, 5),
    ("Essence of Desire", "teala_dia_d", 93, 0, 90, 8),
    ("Citrus Lump", "dia_a_red", 94, 0, 180, 15),
    ("Behemoth Jaw", "dia_a_blue", 95, 0, 100, 20),
    ("Anxious Sprout", "dia_a_green", 96, 0, 50, 15),
    ("Implement of Toil", "dia_b_red", 97, 0, 55, 2),
    ("Luck Wafer", "dia_b_blue", 98, 0, 140, 1),
    ("Meat of Champions", "dia_b_green", 99, 0, 35, 10),
    ("Talisman of Life", "dia_c_red", 100, 0, 90, 15),
    ("Strife Monolith", "dia_c_green", 101, 0, 150, 12),
    ("Boss Stone", "dia_c_blue", 102, 0, 110, 8),
    ("Toxic Toadstool", "kinoko_doku", 103, 0, 30, 5),
    ("Growshroom", "kinoko_tubu", 104, 0, 50, 5),
    ("Indomitable CPU", "sinkukan_b", 105, 0, 100, 10),
    ("Network Mainbrain", "sinkukan_c", 106, 0, 100, 10),
    ("Repair Juggernaut", "bolt_l", 107, 0, 85, 20),
    ("Exhausted Superstick", "gum_tape_s", 108, 0, 50, 12),
    ("Pastry Wheel", "baum_kuchen_s", 109, 0, 35, 10),
    ("Combustion Berry", "ichigo_l", 110, 0, 190, 12),
    ("Imperative Cookie", "cookie_m_l", 111, 0, 25, 5),
    ("Compelling Cookie", "cookie_u", 112, 0, 10, 3),
    ("Impenetrable Cookie", "cookie_u_l", 113, 0, 25, 8),
    ("Comfort Cookie", "cookie_s", 114, 0, 10, 4),
    ("Succulent Mattress", "cookie_s_l", 115, 0, 50, 8),
    ("Corpulent Nut", "donguri_l", 116, 0, 80, 8),
    ("Alien Billboard", "fire_helmet", 117, 0, 80, 15),
    ("Massage Girdle", "nut_l", 118, 0, 100, 20),
    ("Crystallized Telepathy", "be_dama_red_l", 119, 0, 120, 10),
    ("Crystallized Telekinesis", "be_dama_yellow_l", 120, 0, 120, 10),
    ("Crystallized Clairvoyance", "be_dama_blue_l", 121, 0, 120, 10),
    ("Eternal Emerald Eye", "diamond_red_l", 122, 0, 150, 20),
    ("Tear Stone", "diamond_blue_l", 123, 0, 150, 5),
    ("Crystal Clover", "diamond_green_l", 124, 0, 150, 20),
    ("Danger Chime", "bell_red", 125, 0, 120, 10),
    ("Sulking Antenna", "bell_blue", 126, 0, 150, 35),
    ("Spouse Alert", "bell_yellow", 127, 0, 120, 10),
    ("Master's Instrument", "bane_red", 128, 0, 30, 4),
    ("Extreme Perspirator", "bane_blue", 129, 0, 150, 15),
    ("Pilgrim Bulb", "bane_yellow", 130, 0, 55, 10),
    ("Stone of Glory", "juji_key_fc", 131, 0, 100, 5),
    ("Furious Adhesive", "tape_red", 132, 0, 60, 10),
    ("Quenching Emblem", "tape_yellow", 133, 0, 100, 4),
    ("Flame of Tomorrow", "tape_blue", 134, 0, 10, 10),
    ("Love Nugget", "leaf_normal", 135, 0, 40, 20),
    ("Child of the Earth", "leaf_yellow", 136, 0, 40, 15),
    ("Disguised Delicacy", "leaf_kare", 137, 0, 40, 15),
    ("Proton AA", "denchi_3_red", 138, 0, 90, 6),
    ("Fuel Reservoir", "denchi_3_black", 139, 0, 120, 8),
    ("Optical Illustration", "denchi_2_red", 140, 0, 140, 15),
    ("Durable Energy Cell", "denchi_2_black", 141, 0, 160, 15),
    ("Courage Reactor", "denchi_1_red", 142, 0, 280, 20),
    ("Thirst Activator", "denchi_1_black", 143, 0, 300, 20),
    ("Harmonic Synthesizer", "castanets", 144, 0, 120, 10),
    ("Merciless Extractor", "otama", 145, 0, 90, 20),
    ("Remembered Old Buddy", "robot_head", 146, 0, 250, 30),
    ("Fond Gyro Block", "j_block_red", 147, 0, 80, 5),
    ("Memorable Gyro Block", "j_block_yellow", 148, 0, 80, 5),
    ("Lost Gyro Block", "j_block_green", 149, 0, 80, 5),
    ("Favorite Gyro Block", "j_block_blue", 150, 0, 80, 5),
    ("Treasured Gyro Block", "j_block_white", 151, 0, 80, 5),
    ("Fortified Delicacy", "akagai", 152, 0, 60, 20),
    ("Scrumptious Shell", "hotate", 153, 0, 60, 10),
    ("Memorial Shell", "sinjyu", 154, 0, 100, 10),
    ("Chance Totem", "donutschoco_s", 155, 0, 100, 15),
    ("Dream Architect", "donutsichigo_s", 156, 0, 280, 20),
    ("Spiny Alien Treat", "donutswhite_s", 157, 0, 50, 4),
    ("Spirit Flogger", "gear_silver", 158, 0, 70, 20),
    ("Mirrored Stage", "compact_make", 159, 0, 140, 15),
    ("Enamel Buster", "chocolate_l", 160, 0, 60, 8),
    ("Drought Ender", "chocoichigo_l", 161, 0, 100, 4),
    ("White Goodness", "chocowhite_l", 162, 0, 60, 8),
    ("Salivatrix", "g_futa_kyodo", 163, 0, 30, 20),
    ("Creative Inspiration", "g_futa_titiyas", 164, 0, 100, 4),
    ("Massive Lid", "g_futa_kyusyu", 165, 0, 100, 4),
    ("Happiness Emblem", "g_futa_sikoku", 166, 0, 100, 4),
    ("Survival Ointment", "g_futa_kajiwara", 167, 0, 90, 6),
    ("Mysterious Remains", "g_futa_koiwai", 168, 0, 150, 8),
    ("Dimensional Slicer", "g_futa_hirosima", 169, 0, 100, 8),
    ("Yellow Taste Tyrant", "g_futa_kyosin", 170, 0, 100, 15),
    ("Hypnotic Platter", "g_futa_sakotani", 171, 0, 100, 4),
    ("Gherkin Gate", "g_futa_daisen", 172, 0, 100, 15),
    ("Healing Cask", "g_futa_hiruzen", 173, 0, 60, 6),
    ("Pondering Emblem", "g_futa_kitaama", 174, 0, 100, 4),
    ("Activity Arouser", "g_futa_nihonraku", 175, 0,100, 4),
    ("Stringent Container", "kan_maruha", 176, 0, 130, 10),
    ("Patience Tester", "kan_nichiro", 177, 0, 130, 20),
    ("Endless Repository", "kan_iwate", 178, 0, 130, 20),
    ("Fruit Guard", "kan_kyokuyo", 179, 0, 130, 15),
    ("Nutrient Silo", "kan_meidiya", 180, 0, 130, 15),
    ("Drone Supplies", "kan_imuraya", 181, 0, 130, 15),
    ("Unknown Merit", "wadou_kaichin", 182, 0,100,5),
    ("Seed of Greed", "kuri", 183, 0, 70, 10),
    ("Heavy-Duty Magnetizer", "uji_jisyaku", 184, 0,150, 10),
    ("Air Brake", "badminton", 185, 0,100, 15),
    ("Hideous Victual", "medama_yaki", 186, 0,100, 10),
    ("Emperor Whistle", "whistle", 187, 0,75, 15),
    ("Brute Knuckles", "fue_a", 0, 1,100, 15),
    ("Dream Material", "fue_b", 1, 1,100, 10),
    ("Amplified Amplifier", "fue_wide", 2, 1,100, 20),
    ("Professional Noisemaker", "fue_pullout", 3, 1,100,15),
    ("Stellar Orb", "light_a", 4, 1,100,5),
    ("Justice Alloy", "suit_powerup", 5, 1,100,20),
    ("Forged Courage", "suit_fire", 6, 1,100,20),
    ("Repugnant Appendage", "dashboots", 7, 1,100,20),
    ("Prototype Detector", "radar_a", 8, 1,200,35),
    ("Five-man Napsack", "radar_b", 9, 1,100,15),
    ("Spherical Atlas", "map01", 10, 1,200,101),
    ("Geographic Projection", "map02", 11, 1,200,101),
    ("The Key", "key", 12, 1,100,1)
] # (name, text_id, num_id, item_type, value, weight)

class Handler(events.PatternMatchingEventHandler):
    def __init__(self, ctx):
        # Set the patterns for PatternMatchingEventHandler
        events.PatternMatchingEventHandler.__init__(self, patterns=['*GPVE*.gci'],
                                                             ignore_directories=True, case_sensitive=True)
        self.ctx = ctx

    def on_modified(self, event):
        error = True
        while error:
            error = False
            try:
                print("Attempting file open")
                f = open(self.ctx.src_path + "\\01-GPVE-Pikmin2_SaveData.gci", "rb")
                b = f.read()
                ba = bytearray(b)
                offset = 24640
                if (b[offset + 2] == ord("I")): # fake file is here, must read from second file slot instead
                    offset = 73792
                if not self.ctx.linked:
                    # link to game
                    logger.info("Linking to Pikmin 2")
                    if (ba[offset + 44] == 0xBE and ba[offset + 45] == 0xEF and ba[offset + 46] == 0xCA and ba[offset + 47] == 0xFE):
                        self.ctx.recv_addr = (ba[offset + 48] << 24) + (ba[offset + 49] << 16) + (ba[offset + 50] << 8) + (ba[offset + 51])
                        logger.info("Found pointer at " + hex(self.ctx.recv_addr))
                        # check that pointer has correct value
                        # print(id, result)
                        result = dolphin_memory_engine.read_bytes(self.ctx.recv_addr, 4)
                        if (result == b'\xde\xad\xc0\xde'): # make sure pointer has correct value
                            # add day 1 location check
                            logger.info("Granting Day 1 check")
                            self.ctx.locations_checked.add(1)
                            # if (len(self.ctx.locations_checked) != set_len and self.ctx.mapping["VoR Courage Reactor"] != "Remote"): # if this actually changed something, move the item index. item also must be from Pikmin 2
                            #     self.ctx.recv_item_index += 1
                            logger.info("Linking successful.")
                            self.ctx.linked = True
                        else:
                            logger.info(f"Linking failed. Pointer value was {result}, which is incorrect. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
                    else:
                        logger.info("Linking failed. Make sure you're in the overworld or a cave and you are on Day 2 or beyond.")
                if (self.ctx.linked):
                    if ((b[offset + 60] & 128) != 0): # leftmost bit is set == logged item, NOT "normal" playtime (I would hope)
                        itemID = (b[offset + 62] << 8) + b[offset + 63]
                        checksum = ((b[offset + 60] - 128) << 8) + b[offset + 61]
                        cave = (b[offset + 52] << 24) + (b[offset + 53] << 16) + (b[offset + 54] << 8) + (b[offset + 55])
                        sublevel = (b[offset + 56] << 24) + (b[offset + 57] << 16) + (b[offset + 58] << 8) + (b[offset + 59])
                        if not cave in caves.keys():
                            cave = 0
                            sublevel = 0
                        print(hex(cave))
                        print(sublevel)
                        print(itemID)
                        print(checksum)
                        if (itemID != checksum):
                            print("Error (probably not a logged item)")
                            break
                        if ((cave, sublevel, itemID) in self.ctx.collected):
                            print("Already collected, ignoring.")
                            break

                        if (itemID == 89 and self.ctx.win_condition == 0): # louie
                            self.ctx.victory = True

                        self.ctx.collected.append((cave, sublevel, itemID))
                        # print(read_received_item(itemID, cave, sublevel, self.ctx.mapping))
                        self.ctx.locations_checked.add(read_received_item(itemID, cave, sublevel, self.ctx.mapping))
                        # print(self.ctx.locations_checked)
                        # if (not(itemID >= 188 and itemID < 500)): # only increase recv_item_index if the item is from this game
                        #     self.ctx.recv_item_index += 1

                    # # check for FFFFFFFF in treasure (indicates that treasure was read by game)
                    # # if yes, read next thing from queue
                    # # if queue is empty, set busy to false
                    # if(bytes[offset + 48] == 0 and bytes[offset + 49] == 255 and bytes[offset + 50] == 255 and bytes[offset + 51] == 255): # game read the treasure that was previously written
                    #     if (len(item_receipt_queue) > 0):
                    #         current_write = item_receipt_queue.pop(0)
                    #         write_received_item(src_path, current_write)
                    #     else:
                    #         busy = False
            except Exception as e:
                print(e)
                error = True

def calculate_pokos(ctx: Pikmin2Context):
    poko_count = 0
    for nwitem in ctx.items_received:
        itemID = nwitem.item - 1
        if (itemID >= 500):
            itemID -= 312
        poko_count += items[itemID][4]
    print(poko_count)
    return poko_count

def read_received_item(itemID, cave, sublevel, mapping):
    print(itemID)
    explorerKit = 0
    if (itemID >= 500): # it's an explorer kit treasure
        itemID -= 500
        explorerKit = 1
    elif (itemID >= 188): # it's an archipelago treasure
        itemID -= 188
        if (itemID >= 0 and itemID <= 25):
            count = 1
            for location in locations:
                if (location[5] == 0 and location[6] == itemID): # overworld treasure
                    return count
                count += 1
        else:
            count = 1
            for location in locations:
                if (location[0].startswith(caves[cave]) and location[5] == sublevel and location[6] == itemID): # cave treasure
                    return count
                count += 1
    for item in items:
        if (item[2] == itemID and item[3] == explorerKit):
            key = [loc for loc, i in mapping.items() if i == item[0]]
            key = key[0]
            count = 1
            for location in locations:
                if (location[0] == key):
                    return count
                count += 1

def write_received_item(recv_addr, id):
    if (recv_addr == None):
        return False
    print(hex(recv_addr))
    result = dolphin_memory_engine.read_bytes(recv_addr, 4)
    # print(id, result)
    if (dolphin_memory_engine.read_bytes(recv_addr, 4) != b'\xde\xad\xc0\xde'): # game not ready
        return False
    one = (id >> 24) & 0x000000FF
    two = (id >> 16) & 0x000000FF
    three = (id >> 8) & 0x000000FF
    four = id & 0x000000FF
    # print(one, two, three, four)
    # print(bytes([one, two, three, four]))
    dolphin_memory_engine.write_bytes(recv_addr, bytes([one, two, three, four]))
    print("Successfully wrote item " + str(id))
    return True     
        
async def game_watch(ctx: Pikmin2Context):
    while not ctx.exit_event.is_set():
        if (not ctx.connected):
            ctx.game_path = Path(filedialog.askopenfilename(
                initialdir="/",
                title="Select patched Pikmin 2 ROM",
                filetypes=[("Patched Pikmin 2 ROM", "*.iso")]
            ))
            ctx.mapping_path = Path(filedialog.askopenfilename(
                initialdir="/",
                title="Select Pikmin 2 setup file",
                filetypes=[("JSON file", "*.json")]
            ))
            ctx.dolphin_executable_path = get_settings().pikmin2_options.dolphin_path
            ctx.src_path = get_settings().pikmin2_options.save_folder
            print(ctx.dolphin_executable_path)
            print(ctx.src_path)
            print(ctx.mapping_path)
            print(ctx.game_path)
            f = open(ctx.mapping_path)
            data = json.load(f)
            ctx.seed = data["seed"]
            ctx.mapping = data["items"]
            ctx.win_condition = int(data["win_condition"])
            ctx.poko_amount = int(data["poko_amount"])
            ctx.treasure_amount = int(data["treasure_amount"])
            ctx.slot_number = int(data["slot_number"])
            f.close()
            if (os.path.exists(str("pikmin2_game_" + ctx.seed + ".txt"))):
                f = open(str("pikmin2_game_" + ctx.seed + ".txt"), "r")
                ctx.recv_item_index = int(f.readline())
                print(ctx.recv_item_index)
            process_obj = subprocess.Popen([ctx.dolphin_executable_path, f"--exec={ctx.game_path}", "--batch"])
            pid = process_obj.pid
            while not dolphin_memory_engine.is_hooked():
                dolphin_memory_engine.hook()
            print(dolphin_memory_engine.is_hooked())
            event_handler = Handler(ctx)
            observer = observers.Observer()
            observer.schedule(event_handler, path=ctx.src_path, recursive=True)
            observer.start()
            ctx.connected = True
        else:
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                "locations": list(ctx.locations_checked)})
            # print(ctx.locations_checked)
            async_start(ctx.send_msgs(sync_msg))
            # print(ctx.items_received, len(ctx.items_received), ctx.recv_item_index)
            if (len(ctx.items_received) > 0 and ctx.recv_item_index < len(ctx.items_received)):
                next = ctx.items_received[ctx.recv_item_index]
                # logger.info(next.player)
                if (next.player != ctx.slot_number): # item is being sent from another game and must be processed
                    next_id = next.item
                    # print(next_id)
                    # print(ctx.recv_addr)
                    result = write_received_item(ctx.recv_addr, next_id - 1)
                    if result:
                        ctx.recv_item_index += 1
                else: # item is from the game and can be ignored
                    ctx.recv_item_index += 1
            if (ctx.win_condition == 1 and calculate_pokos(ctx) >= ctx.poko_amount):
                ctx.victory = True
            if (ctx.win_condition == 2 and len(ctx.items_received) >= ctx.treasure_amount):
                ctx.victory = True
            if (ctx.victory and not ctx.game_end):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.game_end = True
        # ctx.locations_checked.add(99)
        # sync_msg = [{"cmd": "Sync"}]
        # if (ctx.locations_checked):
        #     sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        await asyncio.sleep(0.1)
def main():
    async def _main():
        ctx = Pikmin2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watch(ctx), name="Pikmin2ProgressionWatcher")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    asyncio.run(_main())

def launch():
    parser = get_base_parser(description="Pikmin 2 Client")
    args = parser.parse_args()
    main()