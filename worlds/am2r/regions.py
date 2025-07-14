from typing import Dict, Set

am2r_regions: Dict[str, Set[str]] = {
    "Menu": {"A0E01_M"}, # Menu to landing site
    "A0E01_M": {"A0E01_R", "A0E01_L"},

    "A0E02_M": {"A0E02_TR", "A0E02_BR", "A0E02_L"},

    "A0E03_M": {"A0E03_TL", "A0E03_BL", "A0E03_D"},

    "A0M01_M": {"A0M01_U", "A0M01_L", "A0M01_R"},

    "A0M02_M": {"A0M02_L", "A0M02_R"},

    "A0M03_M": {"A0M03_L", "A0M03_R"},

    "A0M04_M": {"A0M04_L", "A0M04_R"},

    "A0M05_M": {"A0M05_L", "A0M05_R"},

    "A0M06_M": {"A0M06_L", "A0M06_R"},

    "A0M07_M": {"A0M07_R"},

    "A0M08_M": {"A0M08_L", "A0M08_R"},

    "A0M09_M": {"A0M09_L", "A0M09_R"},

    "A0M10_M1": {"A0M10_L1", "A0M10_TR1", "A0M10_R1", "A0M10_BR1"},

    "A0M10_M2": {"A0M10_L2", "A0M10_R2"}, # This is the same room but completely separated

    "A0M11_M": {"A0M11_L"},

    "A0M12_M": {"A0M12_L", "A0M12_R"},

    "A0M13_M1": {"A0M13_TL1", "A0M13_BL1", "A0M13_R1"},

    "A0M13_M2": {"A0M13_L2", "A0M13_R2"}, # This is the same room but completely separated

    "A0M14_M": {"A0M14_L"},

    "A0M15_M": {"A0M15_L", "A0M15_R"},

    "A0M16_M": {"A0M16_TL", "A0M16_TR","A0M16_BL", "A0M16_BR"},

    "A0M17_M": {"A0M17_L", "A0M17_R"},

    "A0M18_M": {"A0M18_TR", "A0M18_BR", "A0M18_TL", "A0M18_BL"}, # techincally theres the transition to A017 but its crumble blocked

    "A0M19_M": {"A0M19_L", "A0M19_R"},

    "A0M20_M": {"A0M20_BR", "A0M20_TR", "A0M20_U"},

    "A0M21_M": {"A0M21_L", "A0M21_R"},

    "A0M22_M": {"A0M22_L"},

    "A0M23_M": {"A0M23_L", "A0M23_R"},

    "A0M24_M": {"A0M24_L", "A0M24_TR", "A0M24_BR"},

    "A0M25_M": {"A0M25_R"},

    "A0M26_M": {"A0M26_L", "A0M26_R"},

    "A0M27_M": {"A0M27_TL", "A0M27_BL"},

    "A0M28_M": {"A0M28_L", "A0M28_R"},

    "A0M29_M": {"A0M29_L", "A0M29_TR", "A0M29_BR"},

    "A0M30_M": {"A0M30_L", "A0M30_R"},

    "A0M31_M": {"A0M31_L", "A0M31_TR", "A0M31_BR"},

    "A0M32_M": {"A0M32_TL", "A0M32_BL"},

    "A0M33_M": {"A0M33_L", "A0M33_R"},

    "A0M34_M": {"A0M34_L", "A0M34_R"},

    "A0M35_M": {"A0M35_L", "A0M35_R"},

    "A1E01_M": {"A1E01_L", "A1E01_R", "A1E01_U"},

    "A1E02_M": {"A1E02_L", "A1E02_TR", "A1E02_BR"},

    "A1E03_M": {"A1E03_L", "A1E03_R"},

    "A1E04_M": {"A1E04_L", "A1E04_R"},

    "A1E05_M": {"A1E05_LL", "A1E05_LR", "A1E05_TRL", "A1E05_TRR", "A1E05_BRL", "A1E05_BRR"}, # I fucking hate this

    "A1E06_M": {"A1E06_L", "A1E06_D"},

    "A1E07_M1": {"A1E07_T1"},

    "A1E07_M2": {"A1E07_L2"},

    "A1E08_M": {"A1E08_L"},

    "A1E09_M": {"A1E09_D", "A1E09_L"},

    "A1E10_M": {"A1E10_R"},

    "A1B01_M": {"A1B01_L", "A1B01_R"},

    "A1B02_M": {"A1B02_TL", "A1B02_BL", "A1B02_TR", "A1B02_BR"},

    "A1B03_M": {"A1B03_L"},

    "A1B04_M": {"A1B04_R"},

    "A1B05_M": {"A1B05_L"},

    "A1M01_M": {"A1M01_L", "A1M01_R"},

    "A1M02_M": {"A1M02_TL", "A1M02_BL", "A1M02_R"},

    "A1M03_M": {"A1M03_L", "A1M03_R"},

    "A1M04_M": {"A1M04_R"},

    "A1M05_M": {"A1M05_L", "A1M05_R"},

    "A1M06_M": {"A1M06_TL", "A1M06_L", "A1M06_BL", "A1M06_TR", "A1M06_R", "A1M06_BR"},

    "A1M07_M": {"A1M07_L", "A1M07_R"},

    "A1M08_M": {"A1M08_L", "A1M08_R"},

    "A1M09_M": {"A1M09_R"},

    "A1M10_M": {"A1M10_L", "A1M10_R"},

    "A1M11_M": {"A1M11_P", "A1M11_R"},

    "A1M12_M": {"A1M12_L"},

    "A2E01_M": {"A2E01_L", "A2E01_R"},

    "A2E02_M": {"A2E02_RBL", "A2E02_RTL", "A2E02_D", "A2E02_LTL", "A2E02_LBL", "A2E02_LL", "A2E02_LTR", "A2E02_LR", "A2E02_LBR"},

    "A2E03_M": {"A2E03_R"},

    "A2E04_M": {"A2E04_L", "A2E04_BL", "A2E04_R", "A2E04_TR"},

    "A2E05_M": {"A2E05_R"},

    "A2B01_M": {"A2E06_L", "A2E06_R"},

    "A2B02_M": {"A2B02_L", "A2B02_TR", "A2B02_BL", "A2B02_R"},

    "A2B03_M": {"A2B03_L"},

    "A2B04_M": {"A2B04_L", "A2B04_TR", "A2B04_BR"},

    "A2B05_M": {"A2B05_U", "A2B05_R"},

    "A2B06_M": {"A2B06_L", "A2B06_R"},

    "A2B07_M": {"A2B07_L", "A2B07_R"},

    "A2B08_M": {"A2B08_D", "A2B08_R"},

    "A2M01_M": {"A2M01_L", "A2M01_R"},

    "A2M02_M": {"A2M02_L", "A2M02_R"},

    "A2M03_M": {"A2M03_L", "A2M03_R"},

    "A2M04_M": {"A2M04_L", "A2M04_R"},

    "A2M05_M": {"A2M05_L", "A2M05_R", "A2M05_U"},

    "Level_339_M": {"Level_339_U", "Level_339_D",},

    "Level_340_M1": {"Level_340_U1", "Level_340_D1",},

    "Level_340_M2": {"Level_340_U2", "Level_340_D2",},

    "A2M06_M": {"A2M06_L", "A2M06_D"},

    "A2M07_M": {"A2M07_R"},

    "A2M08_M": {"A2M08_L", "A2M08_D"},

    "A2M09_M": {"A2M09_U", "A2M09_L", "A2M09_R"},

    "A2M10_M": {"A2M10_R"},

    "A2M11_M": {"A2M11_TL", "A2M11_BL", "A2M11_R"},

    "A2M12_M": {"A2M12_TL", "A2M12_BL"},

    "A2M13_M": {"A2M13_L", "A2M13_R"},

    "A2M14_M": {"A2M14_L", "A2M14_R"},

    "A2M15_M": {"A2M15_UL", "A2M15_BL"},

    "A2M16_M1": {"A2M16_R1"},

    "A2M16_M2": {"A2M16_L2"},

    "A2M17_M": {"A2M17_L", "A2M17_U"},

    "A2M18_M": {"A2M18_R"},

    "A3E01_M": {"A3E01_L", "A3E01_R"},

    "A3E02_M": {"A3E02_BL", "A3E02_L", "A3E02_TL", "A3E02_LR", "A3E02_TR", "A3E02_D"},

    "A3E03_M": {"A3E03_L", "A3E03_D"},

    "A3E04_M": {"A3E04_L", "A3E04_R"},

    "A3E05_ML": {},
    # Semantic link between this one particularly large room
    "A3E05_MR": {},

    "Research Station": set()
}
# L = left
# R = right
# U = upwards
# D = downwards
# TL = top left
# TR = top right
# BL = bottom left
# BR = bottom right
# LL = left side leftwards
# LR = left side rightwards
# RL = right side leftwards
# ML = Main left

