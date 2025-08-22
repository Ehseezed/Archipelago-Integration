import random





def generate_basic_starting_inventory() -> list:
    legal_starting_password = ["BBAAB", "BAAAB", "BABBI", "BIIIB", "BIFFB", "BFFFB", "BFIIG", "BJJJB", "BJCCB", "BCCCB",
                               "BCJJI", "BGGGB", "BGEEB", "BEEEB", "BEJJJ", "AAAAB", "AABBI", "ABBBI", "ABAAI", "AFFFB",
                               "AFIIG", "AIIIG", "AIFFG", "ACCCB", "ACJJI", "AJJJI", "AJCCI", "AEEEB", "AEJJJ", "AGJJJ",
                               "AGCCJ", "IIIIB", "IIFFB", "IFFFB", "IFIIG", "IBBBJ", "IBAAJ", "IAAAJ", "IABBG", "IGGGB",
                               "IGEEB", "IEEEB", "IEJJJ", "IJGGG", "IJEEG", "ICEEG", "ICGGJ", "FFFFB", "FFIIG", "FFIFG",
                               "FIIIG", "FAAAJ", "FABBG", "FBBBG", "FBAAG", "FEEEB", "FEJJJ", "FGJJJ", "FGCCJ", "FCEEG",
                               "FCGGJ", "FJGGJ", "FJEEJ", "JJJJB", "JJCCB", "JCCCB", "JCJJI", "JGGGB", "JGEEB", "JEEEB",
                               "JEJJJ", "JBIII", "JBFFI", "JAFFI", "JAIIB", "JIBBI", "JIAAI", "JFAAI", "JFBBJ", "CCCCB",
                               "CCJJI", "CJJJI", "CJCCI", "CEEEB", "CEJJJ", "CGJJJ", "CGCCJ", "CAFFI", "CAJFI", "CBIIB",
                               "CBFFB", "CFAAI", "CJBBJ", "CIBBJ", "CIAAJ", "GGJBI", "GGJBI", "GGEEB", "GEEEB", "GEJJJ",
                               "CJGEG", "GJEGJ", "GCEGJ", "GCGEJ", "GIBAI", "GIABJ", "GFABJ", "GFBAJ", "GBIFG", "GBFIJ",
                               "GAFIJ", "GAIFJ", "EECJJ", "BBAJI", "BAAJI", "BABCI", "BIIEB", "BIAJJ", "BFAJJ", "BFBCJ",
                               "BJGFI", "BJEIB", "BCEIB", "BCGFB", "BGJAI", "BGCBJ", "BECBJ", "BEJAJ", "AAAJI", "AABCI",
                               "ABBCI", "ABFGG", "AFAJJ", "AFBCJ", "AIBCJ", "AIAJG", "ACEIB", "ACGFB", "AJGFB", "AJEIG",
                               "AECBJ", "AEJAJ", "AGJAJ", "AGCBG", "IIIEB", "IIAJJ", "IFAJJ", "IFBCJ", "IBIEG", "IBFGJ",
                               "IAFGJ", "IAIEJ", "IGJAI", "IGCBJ", "IECBJ", "IEJAJ", "IJGFG", "IJEIJ", "ICEIJ", "ICGFJ",
                               "FFAJJ", "FFBCJ", "FIBCJ", "FIAJG", "FAFGJ", "FAIEJ", "FBIEJ", "FBFGI", "FECBJ", "FEJAJ",
                               "FGJAJ", "FGCBG", "FCEIJ", "FCGFJ", "FJGFJ", "FJAJJ", "JJGFI", "JJEIB", "JCEIB", "JCGFB",
                               "JGJAI", "JGCBJ", "JECBJ", "JEJAJ", "JBIEI", "JBFGB", "JAFGB", "JAIEB", "JIBCI", "JIEII",
                               "JFEII", "JFGFI", "CCEIB", "CCGFB", "CJGFB", "CJEIG", "CECBJ", "CEJAJ", "CGJAJ", "CGCBG",
                               "CAFGB", "CAIEB", "CBIEB", "CBCBB", "CFEII", "CFGFI", "CIGFI", "CIEIB", "GGJAI", "GGCBJ",
                               "GECBJ", "GEJAJ", "GJGBG", "GJEAG", "GCEAG", "GCBGG", "GIGBB", "GIEAB", "GFEAB", "GFGBI",
                               "GBJIB", "GBCFB", "GACFB", "GAJIG", "EECFG"]
    starting_inventory = generate_starting_inventory(random.choice(legal_starting_password))
    return starting_inventory


def generate_starting_inventory(password: str) -> list:
    starting_inventory = []
    for c in range(len(password)):
        new_item = get_position_string(c) + " " + password[c].upper()
        if not new_item in starting_inventory:
            starting_inventory.append(new_item)

    return starting_inventory


def get_position_string(location: int) -> str:
    position_string = " position"

    match location:
        case 0:
            return "First" + position_string
        case 1:
            return "Second" + position_string
        case 2:
            return "Third" + position_string
        case 3:
            return "Fourth" + position_string
        case 4:
            return "Fifth" + position_string