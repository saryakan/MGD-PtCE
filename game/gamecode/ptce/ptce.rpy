init 1 python:

    def ptceCalculate(calculation, value):
        if calculation.get("calculationType") == "quadratic":
            return calculateQuadratic(calculation, value)
        elif calculation.get("calculationType") == "squareRoot":
            return calculateRoot(calculation, value)
        elif calculation.get("calculationType") == "inverseQuadratic":
            return calculateInverseQuadratic(calculation, value)
        elif calculation.get("calculationType") == "inverseSquareRoot":
            return calculateInverseRoot(calculation, value)
        else:
            raise Exception("Can't determine calculation for value '{0}' and calculation '{1}'".format(value, calculation))

    def calculateQuadratic(calculation, value):
        return calculation.get("quadraticMultiplier") * math.pow(value, 2) + calculation.get("flatMultiplier") * value + calculation.get("flatBonus")

    def calculateRoot(calculation, value):
        return calculation.get("rootMultiplier") * math.sqrt(value) + calculation.get("flatMultiplier") * value + calculation.get("flatBonus")

    def calculateInverseQuadratic(calculation, value):
        return (calculation.get("dividend") / calculateQuadratic(calculation, value)) + calculation.get("flatOverallBonus")

    def calculateInverseRoot(calculation, value):
        return (calculation.get("dividend") / calculateRoot(calculation, value)) + calculation.get("flatOverallBonus")

    ## used to adjust exp gain based on level difference.
    def getExpModForLvlDiff(targetLvl, playerLvl):
        expConfig = ptceConfig.get("expGain")

        if expConfig.get("useVanilla"):
            return getVanillaExpModForLevelDiff(targetLvl, playerLvl)

        if targetLvl >= playerLvl:
            return 1

        lvlDifference = math.fabs(targetLvl - playerLvl)
        difficultyMod = expConfig.get("multiplier").get(difficulty)
        lvlMod = ptceCalculate(expConfig.get("calculation"), lvlDifference)
        floor = expConfig.get("floor").get(difficulty)

        expMod = 1 + difficultyMod * lvlMod
        return round(max(floor, min(1, expMod)), 0)

    def getVanillaExpModForLevelDiff(targetLvl, playerLvl):
        lvlDifference = math.fabs(targetLvl - playerLvl)
        expMod = 1 - lvlDifference * 0.05 + playerLvl * 0.01
        return max(0.7, min(1, expMod))

    ## used to adjust eros gain based on level difference.
    def getErosModForLvlDiff(targetLvl, playerLvl):
        erosConfig = ptceConfig.get("erosGain")

        if erosConfig.get("useVanilla") or targetLvl >= playerLvl:
            return 1

        lvlDifference = math.fabs(targetLvl - playerLvl)
        difficultyMod = erosConfig.get("multiplier").get(difficulty)
        lvlMod = ptceCalculate(erosConfig.get("calculation"), lvlDifference)
        floor = erosConfig.get("floor").get(difficulty)

        erosMod = 1 + difficultyMod * lvlDifference
        return round(max(floor, min(1, erosMod)), 0)
    
    def getPurgeCost(fetish):
        purgeConfig = ptceConfig.get("fetishPurge")
        purgeableAmount = fetish.getPurgeableAmount()
        if purgeConfig.get("useVanilla"):
            return purgeableAmount * 25
        
        return round(ptceCalculate(purgeConfig.get("calculation"), purgeableAmount), 0)

    ## increase Fetish for various occasions
    def increaseFetishOnBeingHit(lastAttack, attacker):
        fetishConfig = ptceConfig.get("fetishGain")
        handleFetishGain(lastAttack, attacker, ["onHitTemp", "onHitPerm"], fetishConfig)

    def increaseFetishOnOrgasm(lastAttack, attacker, spiritLost = 1):
        fetishConfig = ptceConfig.get("fetishGain")
        handleFetishGain(lastAttack, attacker, ["onSpiritLossTemp", "onSpiritLossPerm"], fetishConfig, spiritLost)

    def increaseFetishOnLoss(lastAttack, attacker):
        fetishConfig = ptceConfig.get("fetishGain")
        handleFetishGain(lastAttack, attacker, ["onSpiritLossTemp", "onSpiritLossPerm"], fetishConfig, spiritLost)

    def handleFetishGain(lastAttack, attacker, applyMultipliers, fetishConfig, spiritLost = 1):
        if not fetishConfig.get("useVanilla"):
            fetishTags = getUnbannedFetishTagsOnly(lastAttack.getActualFetishes(attacker), fetishConfig)
            distributionDivisor = 1 if fetishConfig.get("fullFetishGainForMultiFetishSkills") else len(fetishTags)
            effectiveAllure = ptceCalculate(fetishConfig.get("calculation"), attacker.stats.Allure)
            for f in getPlayerFetishes(fetishTags):
                for multiplierName in applyMultipliers:
                    difficultyMod = fetishConfig.get("multipliers").get(multiplierName).get(difficulty)
                    finalGain = round(effectiveAllure * difficultyMod * max(1, spiritLost) / distributionDivisor, 2)
                    if "Perm" in multiplierName:
                        f.increasePerm(finalGain)
                    else:
                        f.increaseTemp(finalGain)

    def getUnbannedFetishTagsOnly(fetishTags, fetishConfig):
        bannedFetishes = fetishConfig.get("bannedFetishes")
        if len(bannedFetishes) <= 0:
            return fetishTags

        return filter(lambda f: f not in bannedFetishes, fetishTags)

    def getPlayerFetishes(fetishes):
        return filter(lambda f: f.name in fetishes, player.FetishList)

