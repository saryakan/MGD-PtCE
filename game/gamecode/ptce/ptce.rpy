init 1 python:

    def ptceCalculate(calculation, value):
        if calculation.get("calculationType") == "linear":
            return calculateLinear(calculation, value)
        elif calculation.get("calculationType") == "quadratic":
            return calculateQuadratic(calculation, value)
        elif calculation.get("calculationType") == "squareRoot":
            return calculateRoot(calculation, value)
        elif calculation.get("calculationType") == "inverseQuadratic":
            return calculateInverseQuadratic(calculation, value)
        elif calculation.get("calculationType") == "inverseSquareRoot":
            return calculateInverseRoot(calculation, value)
        else:
            raise Exception("Can't determine calculation for value '{0}' and calculation '{1}'".format(value, calculation))
    
    def ptceCalculateAllForTarget(calculations, target):
        results = []
        for calculation in calculations:
            if "rngType" in calculation.keys():
                results.append(calculateRng(calculation))
            else:
                stat = target.stats.__dict__.get(calculation.get("stat"))
                results.append(ptceCalculate(calculation, stat))
        
        return results

    def calculateRng(rngCalculation):
        minimum = rngCalculation.get("minimum")
        maximum = rngCalculation.get("maximum")
        if rngCalculation.get("rngType") == "integer":
            return renpy.random.randint(minimum, maximum)
        
        return renpy.random.random() * (maximum - minimum) + minimum

    def calculateLinear(calculation, value):
        return calculation.get("flatMultiplier") * value + calculation.get("flatBonus")
    
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
        handleFetishGain(lastAttack, attacker, ["onCombatLossTemp", "onCombatLossPerm"], fetishConfig, spiritLost)

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
    
    def updateMonsterLearned(monster, move):
        monster.updateLearned(move, player)

    def pickMoveWithPrio(knownMoves, moves):
        normalizedMoves = getNormalizedMoveChoices(knownMoves)
        rng = renpy.random.random()
        for (name, prio) in normalizedMoves:
            if rng <= prio:
                for move in moves:
                    if move.name == name:
                        return move
        
        raise Exception("Could not find move. rng: " + str(rng) + " normalizedMoves: " + str(normalizedMoves) + " moves: " + str(map(lambda m: m.name, moves)))

    def getNormalizedMoveChoices(knownMoves):
        if len(knownMoves.keys()) <= 0:
            return []

        normalizedMoves = []
        modifier = 1 / sum(knownMoves.values())
        runningSum = 0
        for name, prio in knownMoves.items():
            runningSum += prio * modifier
            normalizedMoves.append((name, runningSum))

        return normalizedMoves

    def getMonsterKnownMovesWithPrio(monster):
        result = {}
        for skill in monster.skillList:
            prio = monster.getKnownMovePriority(skill)
            if prio > 0:
                result.update({skill.name: prio})
        
        return result

    def getMonsterKnownBadMoveNames(monster):
        result = []
        for skill in monster.skillList:
            prio = monster.getKnownMovePriority(skill)
            if prio < 0:
                result.append(skill.name)

        return result

    def getRunningRoll(character):
        runningConfig = ptceConfig.get("combat").get("runningCalculations")
        if runningConfig.get("useVanilla"):
            if character.species == "Player":
                return character.stats.Tech*1.5 + (character.stats.Luck)*0.5  + renpy.random.randint(0,100)

            return character.stats.Tech* + (character.stats.Luck)*0.5  + renpy.random.randint(0,100)

        if character.species == "Player":
            return calculateAll(runningConfig.get("playerRunningCalculation"), character)
        
        return calculateAll(runningConfig.get("enemyRunningCalculation"), character)
    
    def getBaseInitiative(character):
        initiativeConfig = ptceConfig.get("combat").get("initiativeCalculations")
        if initiativeConfig.get("useVanilla"):
            return (target.stats.Tech  + (target.stats.Int)*0.5  + (target.stats.Luck)*0.5)
        
        return calculateAll(initiativeConfig.get("fixedCalculations"), character)
    
    def getInitiativeRandomizedBonus(character):
        baseInitiative = getBaseInitiative(character)
        initiativeConfig = ptceConfig.get("combat").get("initiativeCalculations")
        if initiativeConfig.get("useVanilla"):
            return renpy.random.randint(0,100)
        
        return calculateAll(initiativeConfig.get("randomCalculations"), character)
    
    def getMonsterTooltip(monster):
        tooltip = "{0} (Level {1}):\n\n".format(monster.name, monster.stats.lvl)
        if monster.hasBeenAnalyzed:
            tooltip += "Exp: {0}  Eros: {1}\n".format(monster.stats.Exp, monster.moneyDropped)
            tooltip += "HP: {0}/{1}  SP: {4}/{5}  EP: {2}/{3}\n".format(monster.stats.hp, monster.stats.max_true_hp, monster.stats.ep, monster.stats.max_true_ep, monster.stats.sp, monster.stats.max_true_sp)
            tooltip += "Pow | Tech |  Int  | Allu | Will | Luck\n"
            tooltip += "   {0}   |   {1}   |   {2}   |   {3}   |   {4}   |    {5}\n".format(monster.stats.Power, monster.stats.Tech, monster.stats.Int, monster.stats.Allure, monster.stats.Willpower, monster.stats.Luck)
        
        return tooltip
    
    def getSumOfPerkPower(perks, perkType):
        sum = 0
        for perk in perks:
            i = 0
            while i < len(perk.PerkType):
                if perk.PerkType[i] == perkType:
                    sum += perk.EffectPower[i]
                
                i += 1
        return sum
