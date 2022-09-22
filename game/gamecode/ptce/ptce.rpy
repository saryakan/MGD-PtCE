init -1 python:

    import json

    ##################### CONFIG #####################
    PTCE_CONFIG_PATH = renpy.loader.transfn("gamecode/ptce/config.json")

    global ptceConfig

    ptceConfig = {
        "fetishMaxLevel": 10000,
        "stancesByFetish": {
            "Feet": ["Footjob", "Feet Pussy", "Behind Footjob", "Electric Massage"],
            "Legs": ["Thighjob", "Kneejob"],
            "Monstrous": ["Tail Fuck", "Slimed", "Slimed 50%", "Slimed 100%", "Tailjob"],
            "Ass": ["Anal", "Face Sit"],
            "Oral": ["Blowjob"],
            "Breasts": ["Titfuck", "Breast Smother", "Nursing"],
            "Sex": ["Sex"],
            "Kissing": ["Making Out"]
        },
        "useVanillaExpMod": False,
        "useVanillaErosMod": False,
        "bannedFetishes": [],
        "enemiesLearnWeaknesses": True,
        "ptceTempFetishCost": 5,
        "hardcoreMode": False
    }
    
    def loadPtCEConfigs():
        global ptceConfig
        try:
            file = open(PTCE_CONFIG_PATH, "r")
            ptceConfig = json.load(file)
            file.close()
            
        except:
            pass
    ##################### CONFIG #####################

init 1 python:
    ## used to adjust exp gain based on level difference.
    def getExpModForLvlDiff(targetLvl, playerLvl, difficulty):
        if ptceConfig["useVanillaExpMod"]:
            return getVanillaExpModForLevelDiff(targetLvl, playerLvl)

        if targetLvl >= playerLvl:
            return 1

        lvlDifference = math.fabs(targetLvl - playerLvl)
        difficultyMod = 0.03 if difficulty == "Hard" else 0.01 if difficulty == "Easy" else 0.021
        expMod = 1 - difficultyMod * math.pow(lvlDifference, 2)
        return max(0, min(1, expMod))

    def getVanillaExpModForLevelDiff(targetLvl, playerLvl):
        lvlDifference = math.fabs(targetLvl - playerLvl)
        expMod = 1 - lvlDifference * 0.05 + playerLvl * 0.01
        return max(0.7, min(1, expMod))

    ## used to adjust eros gain based on level difference.
    def getErosModForLvlDiff(targetLvl, playerLvl, difficulty):
        if ptceConfig["useVanillaErosMod"] or targetLvl >= playerLvl:
            return 1

        lvlDifference = math.fabs(targetLvl - playerLvl)
        difficultyMod = 0.1 if difficulty == "Hard" else 0.025 if difficulty == "Easy" else 0.05
        difficultyMin = 0.25 if difficulty == "Hard" else 0.75 if difficulty == "Easy" else 0.5
        erosMod = 1 - difficultyMod * lvlDifference
        return max(difficultyMin, min(1, erosMod))

    ## increase Fetish for various occasions
    def increaseFetishOnBeingHit(lastAttack, attacker):
        fetishGain = attacker.stats.Allure
        fetishTags = getUnbannedFetishTagsOnly(lastAttack.getActualFetishes())
        difficultyMod = 0.2 if difficulty == "Hard" else 0.05 if difficulty == "Easy" else 0.1
        for f in getPlayerFetishes(fetishTags):
            f.increaseTemp(attacker.stats.Allure * difficultyMod)

    def increaseFetishOnOrgasm(lastAttack, attacker, spiritLost = 1):
        fetishGain = attacker.stats.Allure
        fetishTags = getUnbannedFetishTagsOnly(lastAttack.getActualFetishes())
        difficultyMod = 1.25 if difficulty == "Hard" else 0.75 if difficulty == "Easy" else 1
        for f in getPlayerFetishes(fetishTags):
            f.increasePerm(attacker.stats.Allure * difficultyMod * max(1, spiritLost))

    def increaseFetishOnOrgasmForFetishes(fetish, attacker, spiritLost = 1):
        if fetish not in ptceConfig["bannedFetishes"]:
            fetishGain = attacker.stats.Allure
            difficultyMod = 1.25 if difficulty == "Hard" else 0.75 if difficulty == "Easy" else 1
            for f in getPlayerFetishes([fetish]):
                f.increasePerm(attacker.stats.Allure * difficultyMod * max(1, spiritLost))

    def increaseFetishOnLoss(lastAttack, attacker):
        fetishGain = attacker.stats.Allure
        fetishTags = getUnbannedFetishTagsOnly(lastAttack.getActualFetishes())
        difficultyMod = 2 if difficulty == "Hard" else 1 if difficulty == "Easy" else 1.5
        for f in getPlayerFetishes(fetishTags):
            f.increasePerm(max(10, attacker.stats.Allure * difficultyMod))

    def getUnbannedFetishTagsOnly(fetishTags):
        if len(ptceConfig["bannedFetishes"]) <= 0:
            return fetishTags

        return filter(lambda f: f not in ptceConfig["bannedFetishes"], fetishTags)

    ## utility functions
    def getPlayerFetishes(fetishes):
        return filter(lambda f: f.name in fetishes, player.FetishList)

