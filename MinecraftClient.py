from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.minecraft.MinecraftClient import launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("MinecraftClient")
    launch()