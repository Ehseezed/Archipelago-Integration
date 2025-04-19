from typing import Dict, Set


am2r_regions: Dict[str, Set[str]] = {
    "Menu": {"A0E01_M"}, # Menu to landing site
    "A0E01_M": {"A0E01_R", "A0E01_L"},

    "A0E02_M": {"A0E02_TR", "A0E02_BR", "A0E02_L"},

    "A0E03_M": {"A0E03_TL", "A0E03_BL", "A0E03_B"},

    "A0M01_M": {"A0M01_T", "A0M01_L", "A0M01_R"},

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

    "A0M20_M": {"A0M20_BR", "A0M20_TR", "A0M20_T"},

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




    "Research Station": set()
}
# todo: Have someone other than me verify this @(V)ariable
