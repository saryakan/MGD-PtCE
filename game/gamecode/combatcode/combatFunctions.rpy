#this .rpy handles all combat action results, such as trying to hit with a skill, and the effects of hitting.
#I really need to re-orginize everything in here at some point.
init python:
    def GetFetishCount(FetishList):
        numberOfFetishes = 0
        for each in FetishList:
            if each.Type == "Fetish":
                numberOfFetishes += 1

        return numberOfFetishes

    def ClearNonPersistentEffects(player):
        player = player.statusEffects.refreshNonPersistant(player)
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "NonPersistentEffect":
                    player.giveOrTakePerk(perk.name, -1)
                p += 1

        return player

    def statusEffectDuration(skillDuration, user, restrain=0):
        effectDuration = float(skillDuration)


        effectDuration = effectDuration*((statusEffectBaseDuration(user, restrain))*0.01 + 1)
        if effectDuration <=2:
            effectDuration = 2
        effectDuration = int(math.floor(effectDuration))
        return effectDuration

    def statusEffectBaseDuration(user, restrain=0):
        effectPerkDuration = 0
        bonus = 0
        if restrain == 0:
            for perk in user.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "StatusEffectDuration":
                        effectPerkDuration += perk.EffectPower[p]
                    p += 1
            bonus = ((float(user.stats.Int)*0.5) + effectPerkDuration)
        return bonus

    def getCritChance(target):
        critMod = 0
        for each in target.statusEffects.tempCrit:
            critMod += each.potency
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "CritChanceBoost":
                    critMod += perk.EffectPower[p]
                p += 1
        critChance = target.stats.Tech*0.10 + target.stats.Luck*0.25 + critMod + 3.25
        critChance = float("{0:.2f}".format(critChance))
        return critChance

    def getCritDamage(target):
        critDamage = 200
        critDamMod = 0
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "CritDamageBoost":
                    critDamMod += perk.EffectPower[p]
                p += 1
        critDamage += target.stats.Allure*0.525 + target.stats.Power*0.525 + critDamMod

        critDamage = float("{0:.2f}".format(critDamage*0.01))
        return critDamage

    def getCritReduction(target):
        critRedMod = 0
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "CritChanceBoostSelf":
                    critRedMod += perk.EffectPower[p]
                p += 1
        #critRedMod += target.stats.Luck*0.2 - 1
        return critRedMod

    def getTotalBoost(attacker, move): #should be a way to cut down this function i think. Will keep in mind for later.
        Boost = 1
        PreventDoubleBoost = 0
        for perk in attacker.perks:
            p = 0
            while  p < len(perk.PerkType):
                PreventDoubleBoost = 0
                if perk.PerkType[p] == "DamageBoost":
                    Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "BreastBoost":
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Breasts":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "AssBoost":
                    for each in move.skillTags:
                        canGo = 0
                        checkTag = each
                        for monStance in attacker.combatStance:
                            if monStance.Stance != "None":
                                if checkTag == "Penetration":
                                    if monStance.Stance == "Anal":
                                        canGo = 1

                        if checkTag == "Ass":
                            canGo = 1
                        if canGo == 1 and PreventDoubleBoost == 0:
                            PreventDoubleBoost = 1
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "NonPenAssBoost":
                    checkPen = 0
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Penetration":
                            checkPen = 1
                    if checkPen == 0:
                        for each in move.skillTags:
                            checkTag = each
                            if checkTag == "Ass":
                                Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "SexBoost":
                    for each in move.skillTags:
                        canGo = 0
                        checkTag = each
                        for monStance in attacker.combatStance:
                            if monStance.Stance != "None":
                                if checkTag == "Penetration":
                                    if monStance.Stance == "Sex":
                                        canGo = 1
                        if checkTag == "Sex":
                            canGo = 1
                        if canGo == 1 and PreventDoubleBoost == 0:
                            PreventDoubleBoost = 1
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "NonPenSexBoost":
                    checkPen = 0
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Penetration":
                            checkPen = 1
                    if checkPen == 0:
                        for each in move.skillTags:
                            checkTag = each
                            if checkTag == "Sex":
                                Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "PainBoost":
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Pain":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "SeductionBoost":
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Seduction":
                            Boost += perk.EffectPower[p]*0.01
                if perk.PerkType[p] == "NonPenSeductionBoost":
                    checkPen = 0
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Penetration":
                            checkPen = 1
                    if checkPen == 0:
                        for each in move.skillTags:
                            checkTag = each
                            if checkTag == "Seduction":
                                Boost +=  perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "MagicBoost":
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Magic":
                            Boost +=  perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "NonPenMagicBoost":
                    checkPen = 0
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Penetration":
                            checkPen = 1
                    if checkPen == 0:
                        for each in move.skillTags:
                            checkTag = each
                            if checkTag == "Magic":
                                Boost +=  perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "PenetrationBoost":
                    for each in move.skillTags:
                        checkTag = each
                        if checkTag == "Penetration":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "OralBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Oral":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "MonstrousBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Monstrous":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "FeetUseBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Feet":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "BreastUseBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Breasts":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "AssUseBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Ass":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "KissBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Kissing":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "ForeplayBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Foreplay":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "SexToyBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Sex Toy":
                            Boost += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "IndulgentBoost":
                    for fetishE in move.fetishTags:
                        checkTag = fetishE
                        if checkTag == "Indulgent":
                            Boost += perk.EffectPower[p]*0.01
                p += 1
        return Boost

    def getBaseEvade(evader, StanceAccuaracyMod, defenceMod):
        EvadeDamageMod = 0
        evadeTotal = 0
        statEvade = 0
        if StanceAccuaracyMod == 0:
            statEvade = ((evader.stats.Tech-5)*0.3) + (evader.stats.Luck-5)*0.15
        else:
            statEvade = ((evader.stats.Power-5)*0.3) + ((evader.stats.Tech-5)*0.15)

        for perk in evader.perks:
            if StanceAccuaracyMod == 0:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "OutOfStanceEvade":
                        EvadeDamageMod += perk.EffectPower[p]
                    p += 1


        evadeTotal = (statEvade + EvadeDamageMod)*defenceMod
        return evadeTotal

    def getBaseAccuracy(attacker, StanceAccuaracyMod):
        accuracyTotal = 0
        if StanceAccuaracyMod == 0:
            accuracyTotal = ((attacker.stats.Tech-5)*0.3) + (attacker.stats.Luck-5)*0.15
        else:
            accuracyTotal = ((attacker.stats.Power-5)*0.3) + ((attacker.stats.Tech-5)*0.15) + StanceAccuaracyMod
        return accuracyTotal

    def getStatusEffectAccuracy(attacker, move):
        accuracyTotal = 0

        relatedStat = attacker.stats.getStat(move.statType)

        accuracyTotal =  relatedStat*0.25 +  getStatusEffectBaseAccuracy(attacker)
        return accuracyTotal

    def getStatusEffectBaseAccuracy(attacker):
        accuracyTotal = 0
        chanceBoost = 0
        for perk in attacker.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "StatusChanceBoost":
                    chanceBoost += perk.EffectPower[p]
                p += 1
        accuracyTotal += ((attacker.stats.Int-5)*0.25) + ((attacker.stats.Luck-5)*0.1)  + chanceBoost
        return accuracyTotal

    def getStatusEffectEvade(theTarget):
        evadeTotal = 0
        evadeTotal += ((theTarget.stats.Willpower-5)*0.25) + ((theTarget.stats.Luck-5)*0.1)
        return evadeTotal


    def getStatusEffectRes(theTarget, move, autoHits=0):
        accuracyTotal = 0

        if (theTarget.statusEffects.surrender.duration > 0):
            surrenderMod = 1000
        else:
            surrenderMod = 0

        restrainedMod = 0
        if (theTarget.statusEffects.restrained.duration > 0 ):
            restrainedMod = 10

        if (theTarget.statusEffects.sleep.potency == -99 or theTarget.statusEffects.trance.potency >= 11)  or autoHits == 1:
            restrainedMod += 1000

        if (theTarget.statusEffects.paralysis.duration > 0):
            restrainedMod += theTarget.statusEffects.paralysis.potency*3


        defenceMod = 0
        if (theTarget.statusEffects.defend.duration > 0):
            defenceMod += 25


        StanceAccuaracyMod = 0
        EvadeDamageMod = 0
        fetishMod = 0
        if move.statusEffect != "Escape" and move.statusEffect != "TargetStances":
            for each in theTarget.combatStance:
                if each.Stance != "None":
                    StanceAccuaracyMod += 3
                else:

                    for perk in theTarget.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "OutOfStanceEvade":
                                EvadeDamageMod += perk.EffectPower[p]
                            p += 1


            for each in move.fetishTags:
                for fetishE in theTarget.FetishList:
                    checkTag = each
                    if checkTag == "Penetration":
                        for stanceChek in theTarget.combatStance:
                            if stanceChek.Stance == "Sex":
                                checkTag = "Sex"
                            elif stanceChek.Stance == "Anal":
                                checkTag = "Ass"
                    if checkTag == fetishE.name:
                        fetishMod += fetishE.Level*0.1

        CharmMod = 1


        EffectRes = 0
        if theTarget.resistancesStatusEffects.getRes(move.statusEffect) != -999:
            EffectRes += (theTarget.resistancesStatusEffects.getRes(move.statusEffect))

        relatedReisitStat = 0
        baseStatusEvade = 0
        if move.statusEffect != "Escape" and move.statusEffect != "TargetStances":
            baseStatusEvade = getStatusEffectEvade(theTarget)
            relatedReisitStat = theTarget.stats.getStat(move.statusResistedBy)

        accuracyTotal =  (baseStatusEvade + defenceMod + relatedReisitStat*0.25 - fetishMod + EvadeDamageMod - restrainedMod - surrenderMod  + StanceAccuaracyMod + EffectRes)*CharmMod
        return accuracyTotal


    def getStatusEffectChance(statusChance, attacker, theTarget, move, autoHits=0):
        total = 0

        CharmMod = 1
        TranceMod = 0
        if move.statusEffect == "Escape" or move.statusEffect == "TargetStances":
            if  attacker.statusEffects.trance.potency >= 0:
                TranceMod += attacker.statusEffects.trance.potency*2

            if (attacker.statusEffects.charmed.duration > 0):
                CharmMod = 0.5

        if attacker.species == "Player" and theTarget.species == "Player":
            total = (statusChance + getStatusEffectAccuracy(attacker, move))*CharmMod - TranceMod
        else:
            total = (statusChance + getStatusEffectAccuracy(attacker, move))*CharmMod - TranceMod - getStatusEffectRes(theTarget, move, autoHits)

        return total



    def getDamageReduction(defender, Damage):
        damageReturn = 200.0/(200.0 + float(defender.stats.Willpower) - 5.0)
        extraReduction = 0
        for perk in defender.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "DamageReduction":
                    extraReduction += (perk.EffectPower[p]*0.01)
                p += 1
        damageReturn = Damage*(damageReturn-extraReduction)
        damageReturn = float("{0:.2f}".format(damageReturn))
        return damageReturn


    def getCoreStatFlatBonus(statDamMod):
        Mod = 0
        if statDamMod >= 0:
            Mod = math.sqrt(statDamMod*3)-5
        else:
            statDamMod = statDamMod*-1
            Mod = -(math.sqrt(statDamMod*3))-5
        return Mod
    def getCoreStatPercentBonus(statDamMod, power):
        Mod = 0
        if statDamMod >= 0:
            Mod += power*(math.sqrt(statDamMod*0.002)-0.1)
        else:
            statDamMod = statDamMod*-1
            Mod += power*(-(math.sqrt(statDamMod*0.002))-0.1)
        return Mod

    def getStatFlatBonus(statDamMod):
        Mod = 0
        if statDamMod >= 0:
            Mod = math.sqrt(statDamMod*4)-5
        else:
            statDamMod = statDamMod*-1
            Mod = -(math.sqrt(statDamMod*4))-5
        return Mod
    def getStatPercentBonus(statDamMod, power):
        Mod = 0
        if statDamMod >= 0:
            Mod += power*(math.sqrt(statDamMod*0.003)-0.1)
        else:
            statDamMod = statDamMod*-1
            Mod += power*(-(math.sqrt(statDamMod*0.003))-0.1)
        return Mod

    def getDamageEstimate(player, skill):

        damageEstimate = skill.power + 1
        allureFlatScaling = 0.05
        allureFlatPercentBoost = 0
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BaselineAllureFlatBuff":
                    allureFlatScaling += perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "BaselineAllureFlatPercentBoost":
                    allureFlatPercentBoost += perk.EffectPower[p]*0.01
                p += 1

        flatDamageBonus = 0
        for each in skill.fetishTags:
            if each == "Foreplay":
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "ForeplayFlatDamage":
                            flatDamageBonus += perk.EffectPower[p]
                        p += 1

        if skill.statType != "None" and skill.statType != "HeadPat":
            if skill.statType == "Level":
                statDamMod = player.stats.lvl
                damageEstimate += ((statDamMod)*0.3)
            if skill.statType == "Core":
                coreStatsList = []
                coreStatsList.append(player.stats.Power)
                coreStatsList.append(player.stats.Tech)
                coreStatsList.append(player.stats.Int)
                coreStatsList.append(player.stats.Allure)
                biggestStat = max(coreStatsList)*0.5

                statDamMod = biggestStat + (player.stats.Allure + player.stats.Tech + player.stats.Int + player.stats.Power)/4
                damageEstimate += getCoreStatFlatBonus(statDamMod)
                damageEstimate += getCoreStatPercentBonus(statDamMod, skill.power)

            else:
                relatedStat = player.stats.getStat(skill.statType)
                statDamMod = relatedStat
                damageEstimate += getStatFlatBonus(statDamMod)
                damageEstimate += getStatPercentBonus(statDamMod, skill.power)

        else:
            relatedStat = 0
        damageEstimate += (skill.power*((player.stats.Allure-5)*0.002 + allureFlatPercentBoost)) + ((player.stats.Allure-5)*allureFlatScaling) + flatDamageBonus
        for each in skill.skillTags:
            if each == "Holy" and skill.statType != "HeadPat":
                damageEstimate *= getVirility(player)*0.01


        damageEstimate = math.floor(damageEstimate)
        damageEstimate = int(damageEstimate)

        return damageEstimate

    def getBuffEstimate(user, skill):
        damageEstimate = 0
        relatedStat = user.stats.getStat(skill.statType)
        try:
            scaling = skill.statusEffectScaling*0.01
        except:
            scaling = 1

        flipper = 1
        if skill.statusPotency < 0:
            flipper = -1

        if skill.statusEffect == "Defence" or skill.statusEffect == "Damage":
            relatedStat = user.stats.getStat(skill.statType)
            damageEstimate = skill.statusPotency + (relatedStat*scaling)*flipper
            damageEstimate = math.floor(damageEstimate)
            damageEstimate = int(damageEstimate)
        else:
            damageEstimate = skill.statusPotency + (relatedStat*scaling)*flipper

            damageEstimate = math.floor(damageEstimate)
            damageEstimate = int(damageEstimate)
        return damageEstimate




label combatActionTurn:
    $ Crit = 0
    $ Hit = 0
    $ recoilHit = 0
    $ critText = ""
    $ stanceGo = "False"
    $ attackHit = "False"
    $ stanceDurabilityHoldOverAttacker = 0
    $ stanceDurabilityHoldOverTarget = 0
    call setAttacker(attacker, skillChoice) from _call_setAttacker


    $ noGo = 0
    $ canGo = 0
    $ foreplayDefDown = 0

    python:
        for pick in skillChoice.requiresTargetStance:
            if "Any" != pick:
                for monStance in defender.combatStance:
                    if monStance.Stance != "None":
                        if pick == "Penetration":
                            if monStance.Stance == "Sex":
                                canGo = 1
                            elif monStance.Stance == "Anal":
                                canGo = 1
                        if monStance.Stance == pick:
                            canGo = 1
            else:
                canGo = 1

        for each in attacker.combatStance:
            for pick in skillChoice.unusableIfStance:
                if pick == "Penetration":
                    if each.Stance == "Sex":
                        noGo += 1
                    elif each.Stance == "Anal":
                        noGo += 1
                elif each.Stance == pick:
                    noGo += 1
                elif pick == "Any":
                    if each.Stance != "None":
                        noGo += 1

        for each in defender.combatStance:
            for pick in skillChoice.unusableIfTarget:
                if pick == "Penetration":
                    if each.Stance == "Sex":
                        noGo += 1
                    elif each.Stance == "Anal":
                        noGo += 1
                elif each.Stance == pick:
                    noGo += 1

        isunusable = getUnviableSets(skillChoice, defender)
        if isunusable == True:
            noGo = True

        if noGo >= 1:
            canGo = 0

    if canGo != 1:
        $ canUse = False
    else:
        $ canUse = True

    $ epOut = 0
    if skillChoice.costType == "ep" and attacker.species == "Player":
        if skillChoice.cost > attacker.stats.ep:
            $ canUse = False
            $ epOut = 1

    if skillChoice.requiresStatusEffect != "" and skillChoice.requiresStatusEffect != "None":
        if defender.statusEffects.hasThisStatusEffect(skillChoice.requiresStatusEffect) == False:
            $ canUse = False

    if canUse == True:
        $ lastAttack = skillChoice
        $ altName = ""
        if skillChoice.isSkill != "True":
            $ altName = itemChoice.name
        else:
            $ altName = skillChoice.name
        call CounterTalk(defender, attacker, skillChoice, altName) from _call_CounterTalk
        if len(counterArray) > 0:
            $ Speaker = Character(_(defender.name))
            $ x = 0
            while x < len(counterArray):
                $ display = copy.deepcopy(counterArray[x])
                call  read from _call_read_47
                $ x+=1

    if(skillChoice.name == "Run Away") and skipAttack == 0 and attacker.species == "Player":
        call combatRunAttempt from _call_combatRunAttempt

    if canUse == False:
        if epOut == 1:
            $ display = attacker.name + " no longer has the energy needed for their plan!"#add varience depending which stance inturrupted u
        else:
            $ display = attacker.name + "'s plans were interrupted!"#add varience depending which stance inturrupted u
        "[display]"
    elif (attacker.statusEffects.surrender.duration > 0):
        $ attacker.statusEffects.surrender.duration += 2

    elif attacker.statusEffects.sleep.potency == -99:
        if attacker.species != "Player":
            $ display = attacker.name + " sleeps soundly, unaware of what's happening around them..."


            $ attacker.statusEffects.sleep.duration = getSleepingStruggle(attacker)


            if attacker.statusEffects.sleep.duration <= 0:
                $ display = "With a groan, " + attacker.name +" drowsily begins to wake up!"
                $ attacker.statusEffects.sleep.potency = 0
                #$ CheckImmunity = getFromName("Sleep Immune", attacker.perks)
                #if CheckImmunity == -1:
                #    $ attacker.giveOrTakePerk("Sleep Immune", 1)
                #else:
                #    $ attacker.giveOrTakePerk("Sleep Immune", -1)
                #    $ attacker.giveOrTakePerk("Sleep Immune", 1)
                $ attacker.statusEffects.sleep.duration = 0
            "[display]"
    elif(attacker.statusEffects.stunned.duration > 0):
        $ display = attacker.name + " is stunned!"
        "[display]"
    elif attacker.statusEffects.restrained.duration > 0 and skillChoice.statusEffect != "Escape"  and skillChoice.name != " " and skillChoice.name != "Defend" and skillChoice.name != "Struggle" and skillChoice.name != "Wait":


        $ unbounded = 0
        python:
            for perk in attacker.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "Unbounded":
                        unbounded = 1
                    p += 1
        $ display = attacker.name + " is restrained!"
        if attacker.species != "Player" or unbounded == 1:

            $ attackerName = attacker.restrainer.name
            $ attackerHeOrShe = getHeOrShe(attacker.restrainer)
            $ attackerHisOrHer = getHisOrHer(attacker.restrainer)
            $ attackerHimOrHer = getHimOrHer(attacker.restrainer)
            $ attackerYouOrMonsterName = getYouOrMonsterName(attacker.restrainer)
            $ theAttacker = theForGeneric(attacker.restrainer)

            $ targetName = attacker.name
            $ targetHeOrShe = getHeOrShe(attacker)
            $ targetHisOrHer = getHisOrHer(attacker)
            $ targetHimOrHer = getHimOrHer(attacker)
            $ targetYouOrMonsterName = getYouOrMonsterName(attacker)
            $ theTarget = theForGeneric(attacker)

            $ canStruggle = 0
            if attacker.species != "Player":
                if attacker.putInRestrain == 0 or unbounded == 1:
                    $ canStruggle = 1
            else:
                if unbounded == 1:
                    $ canStruggle = 1

            if canStruggle == 1:
                call combatStruggleActivate(attacker) from _call_combatStruggleActivate

            else:
                $ attacker.putInRestrain = 0
                $ display = attacker.name + " is restrained!"

        call read from _call_read_30
        $ display = ""
    else:



        $ display = ""



        $ attackHit = "False"

        $ loop = 1
        $ hitAll = 0

        if skillChoice.isSkill != "True":
            $ nameExtra = itemChoice.name
        else:
            $ nameExtra = skillChoice.name

        $ Speaker = Character(_(attacker.name + " - " + nameExtra))
        $ goAttack = 0
        if skipAttack == 0 and attacker.species == "Player":
            $ goAttack = 1
        elif attacker.species != "Player":
            $ goAttack = 1

        if goAttack == 1:
            if attacker.species == "Player":
                if skillChoice.costType == "ep":
                    $ attacker.stats.ep -= skillChoice.cost
                elif skillChoice.costType == "hp":
                    $ actualCost = skillChoice.cost + (player.stats.max_true_hp-100)*0.15
                    $ actualCost = math.floor(actualCost)
                    $ actualCost = int(actualCost)
                    $ attacker.stats.hp += actualCost
                elif skillChoice.costType == "sp":
                    $ attacker.stats.sp -= skillChoice.cost

            if attacker.species == "Player" and itemChoice.name != "Blank":
                $ attacker.inventory.useItem(itemChoice.name)

            python:
                for each in skillChoice.fetishTags:
                    if each == "Foreplay":
                        for perk in attacker.perks:
                            p = 0
                            while  p < len(perk.PerkType):
                                if perk.PerkType[p] == "ForeplayEnergyRegen":
                                    attacker.stats.ep += int(math.floor(player.stats.max_true_ep*(perk.EffectPower[p]*0.01)))
                                if perk.PerkType[p] == "ForeplayArousalRegen":
                                    attacker.stats.hp -= int(math.floor(player.stats.max_true_hp*(perk.EffectPower[p]*0.01)))

                                p += 1
                                if player.stats.ep > player.stats.max_true_ep:
                                    player.stats.ep = player.stats.max_true_ep
                                if player.stats.hp <= 0:
                                    player.stats.hp = 0

            $ AppliedStanceThisAttack = 0
            if(skillChoice.targetType == "single"):
                $ loop = 1
            elif(skillChoice.targetType == "2Hits"):
                $ loop = 2
            elif(skillChoice.targetType == "3Hits"):
                $ loop = 3
            elif(skillChoice.targetType == "4Hits"):
                $ loop = 4
            elif(skillChoice.targetType == "5Hits"):
                $ loop = 5
            elif(skillChoice.targetType == "Escape"):
                $ loop = 1
            elif skillChoice.targetType == "all" and skillChoice.skillType != "Healing" and skillChoice.skillType != "HealingEP" and skillChoice.skillType != "HealingSP" and skillChoice.skillType != "StatusHeal" and attacker.species == "Player":
                $ loop = len(monsterEncounter)
                $ hitAll = 1

            $ atkLo = 0

            while atkLo < loop:
                $ attackHit = "False"
                if loop >= 1:
                    $ display = ""

                if hitAll == 1:
                    $ defender = monsterEncounter[atkLo]
                    $ CombatFunctionEnemytarget = atkLo

                call setDefender(defender) from _call_setDefender

                if(skillChoice.skillType == "attack"):
                    python:
                        holder = AttackCalc(attacker, defender, skillChoice, waiting, True)
                        finalDamage = holder[0]
                        defender.stats.hp += holder[0]
                        attacker.stats.hp += holder[4]
                        recoilHit = holder[4]
                        critText = holder[2]

                        attackHit = holder[3]
                        stanceGo = holder[3]
                        effectiveText = holder[5]
                        statusEffectiveText = holder[6]
                    $ foreplayDefDown = 0
                    if(stanceGo == "True"):
                        python:
                            for each in skillChoice.fetishTags:
                                if each == "Foreplay":
                                    for perk in attacker.perks:
                                        p = 0
                                        while  p < len(perk.PerkType):
                                            if perk.PerkType[p] == "ForeplayDefDown":
                                                foreplayDefDown += (perk.EffectPower[p])

                                            p += 1
                                    if foreplayDefDown > 0:
                                        defender.statusEffects.tempDefence.append(StatusEffect(4, foreplayDefDown*-1, "Foreplay"))

                        #call onHitTalk(defender, attacker, skillChoice) from _call_onHitTalk_1
                        if attacker.species != "Player":
                            call PreMonDialogueGet from _call_PreMonDialogueGet
                            call MonDialogueGet from _call_MonDialogueGet

                        if skillChoice.removesStance[0] != "" and skillChoice.removesStance[0] != "None":
                            python:
                                for removeTheStance in skillChoice.removesStance:
                                    if removeTheStance != "All" and removeTheStance != "Target":
                                        stanceDurabilityHoldOverAttacker = attacker.getStanceDurability(removeTheStance)
                                        stanceDurabilityHoldOverTarget = defender.getStanceDurability(removeTheStance)
                                        attacker.removeStanceByName(removeTheStance)
                                        defender.removeStanceByName(removeTheStance)

                                    elif removeTheStance == "Target":

                                        if attacker.species == "Player":
                                            for each in defender.combatStance:
                                                stanceDurabilityHoldOverTarget += defender.getStanceDurability(each.Stance)
                                                stanceDurabilityHoldOverAttacker += attacker.getStanceDurability(each.Stance)
                                                attacker.removeStanceByName(each.Stance)
                                            defender.clearStance()
                                        else:
                                            for each in attacker.combatStance:
                                                stanceDurabilityHoldOverTarget += defender.getStanceDurability(each.Stance)
                                                stanceDurabilityHoldOverAttacker += attacker.getStanceDurability(each.Stance)
                                                defender.removeStanceByName(each.Stance)
                                            attacker.clearStance()
                                    else:
                                        for each in player.combatStance:
                                            stanceDurabilityHoldOverTarget += defender.getStanceDurability(each.Stance)
                                            stanceDurabilityHoldOverAttacker += attacker.getStanceDurability(each.Stance)
                                        player.clearStance()
                                        atkLo = 0
                                        while atkLo < len(monsterEncounter):
                                            monsterEncounter[atkLo].clearStance()
                                            atkLo+=1

                        if AppliedStanceThisAttack == 0:
                            $ holderS = ApplyStance(attacker, defender, skillChoice, justEscapedStance, stanceDurabilityHoldOverAttacker, stanceDurabilityHoldOverTarget)
                            $ stanceDurabilityHoldOverAttacker = 0
                            $ stanceDurabilityHoldOverTarget = 0
                            $ defender = holderS[1]
                            $ attacker = holderS[0]
                            $ justEscapedStance = holderS[2]
                            $ AppliedStanceThisAttack = 1

                    $ display += holder[1]

                    $ OverrideSleeping = 0
                    if skillChoice.descrips == "PlayWhilePlayerSleeping":
                        $ OverrideSleeping = 1

                    if player.statusEffects.sleep.potency != -99 or OverrideSleeping == 1:
                        call read from _call_read_12

                    if(skillChoice.statusChance > 0 and finalDamage > 0):
                        $ hadStanceToRemove = 1
                        if skillChoice.statusEffect == "TargetStances":
                            if attacker.combatStance[0].Stance == "None" or attacker.combatStance[0].Stance == "":
                                $ hadStanceToRemove = 0
                        python:
                            if skillChoice.statusEffect != "Damage" and skillChoice.statusEffect != "Defence" and skillChoice.statusEffect != "Crit" and skillChoice.statusEffect != "Power" and skillChoice.statusEffect != "Technique" and skillChoice.statusEffect != "Intelligence" and skillChoice.statusEffect != "Willpower" and skillChoice.statusEffect != "Allure" and skillChoice.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and skillChoice.statusEffect != "Escape" and skillChoice.statusEffect != "TargetStances":
                                holder = statusCheck(attacker, defender, skillChoice, waiting)
                                defender = holder[0]
                            else:
                                if skillChoice.statusPotency > 0 or skillChoice.statusEffect == "Escape" or skillChoice.statusEffect == "TargetStances":
                                    holder = statusBuff(attacker, defender, skillChoice, waiting)
                                    attacker = holder[0]
                                    defender = holder[2]
                                    stanceGo = holder[3]
                                    statusEffectiveText = holder[4]

                                else:
                                    holder = statusBuff(defender, attacker, skillChoice, waiting)
                                    attacker = holder[2]
                                    defender = holder[0]
                                    stanceGo = holder[3]
                                    statusEffectiveText = holder[4]
                        if holder[1] != "Skip":
                            if attacker.species != "Player" and stanceGo == "True":
                                call PreMonDialogueGet from _call_PreMonDialogueGet_1
                                call MonDialogueGet from _call_MonDialogueGet_1
                            $ display = holder[1]
                            $ OverrideSleeping = 0
                            if skillChoice.descrips == "PlayWhilePlayerSleeping":
                                $ OverrideSleeping = 1

                            if player.statusEffects.sleep.potency != -99 or OverrideSleeping == 1:
                                if hadStanceToRemove == 1:
                                    call read from _call_read_13
                if(skillChoice.skillType == "statusEffect"):
                    if(skillChoice.statusChance > 0):
                        $ stanceGo = "False"

                        if skillChoice.statusEffect == "Analyze":
                            $ stanceGo = "True"
                            $ display = skillChoice.outcome
                            call read from _call_read_42
                            $ display = "Name: " + defender.name + "        Species: " + defender.species + "       Level: " + str(defender.stats.lvl) + "\n\n"
                            $ display += "Arousal: " + str(defender.stats.hp) + "/" + str(defender.stats.max_true_hp) + "      Energy: " + str(defender.stats.ep) + "/" + str(defender.stats.max_true_ep) + "      Spirit: " + str(defender.stats.sp) + "/" + str(defender.stats.max_true_sp) + "\n\n"
                            $ display += "Power: " + str(defender.stats.Power) + "     "
                            $ display += "Technique: " + str(defender.stats.Tech) + "      "
                            $ display += "Intelligence: " + str(defender.stats.Int) + "     \n"
                            $ display += "Allure: " + str(defender.stats.Allure) + "       "
                            $ display += "Willpower: " + str(defender.stats.Willpower) + "     "
                            $ display += "Luck: " + str(defender.stats.Luck) + "\n"
                            call read from _call_read_43
                            python:
                                display = "Fetishes: "
                                WeakArray = []
                                for fetishE in defender.FetishList:
                                    if fetishE.Level >= 1:
                                        WeakArray.append(fetishE.name)
                                if  len(WeakArray) > 0:
                                    ri = 0
                                    for each in WeakArray:
                                        display += each
                                        if ri + 1 < len(WeakArray):
                                            display += ", "
                                        else:
                                            display += ".\n"
                                        ri += 1

                                if display != "Fetishes: ":
                                    display += "Sensitive: "
                                else:
                                    display = "Sensitive: "

                                resArray = ["Sex", "Ass", "Breasts", "Mouth", "Seduction", "Magic", "Pain", "Holy"]
                                WeakArray = []
                                StrongArray = []
                                for res in resArray:
                                    if defender.BodySensitivity.getRes(res) >= 125:
                                        WeakArray.append(res)
                                    elif defender.BodySensitivity.getRes(res) <= 75:
                                        StrongArray.append(res)

                                if  len(WeakArray) > 0:
                                    ri = 0
                                    for each in WeakArray:
                                        display += each
                                        if ri + 1 < len(WeakArray):
                                            display += ", "
                                        else:
                                            display += ".\n"
                                        ri += 1
                                else:
                                    display += "None.\n"

                                display += "Insensitive: "
                                if  len(StrongArray) > 0:
                                    ri = 0
                                    for each in StrongArray:
                                        display += each
                                        if ri + 1 < len(StrongArray):
                                            display += ", "
                                        else:
                                            display += ".\n\n"
                                        ri += 1
                                else:
                                    display += "None.\n\n"


                                display += "Vulnerable to: "

                                effectResArray = ["Stun", "Charm", "Aphrodisiac", "Restraints", "Sleep", "Trance", "Paralysis", "Debuff"]
                                WeakArray = []
                                StrongArray = []
                                for res in effectResArray:
                                    if defender.resistancesStatusEffects.getRes(res) < 0:
                                        WeakArray.append(res)
                                    elif defender.resistancesStatusEffects.getRes(res) > 0:
                                        StrongArray.append(res)
                                if  len(WeakArray) > 0:
                                    ri = 0
                                    for each in WeakArray:
                                        display += each
                                        if ri + 1 < len(WeakArray):
                                            display += ", "
                                        else:
                                            display += ".\n"
                                        ri += 1
                                else:
                                    display += "None.\n"
                                display += "Resists: "
                                if  len(StrongArray) > 0:
                                    ri = 0
                                    for each in StrongArray:
                                        display += each
                                        if ri + 1 < len(StrongArray):
                                            display += ", "
                                        else:
                                            display += ".\n"
                                        ri += 1
                                else:
                                    display += "None.\n"

                            call read from _call_read_44
                            $ display = ""

                        elif skillChoice.statusEffect != "Damage" and skillChoice.statusEffect != "Defence" and skillChoice.statusEffect != "Crit" and skillChoice.statusEffect != "Power" and skillChoice.statusEffect != "Technique" and skillChoice.statusEffect != "Intelligence" and skillChoice.statusEffect != "Willpower" and skillChoice.statusEffect != "Allure" and skillChoice.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and skillChoice.statusEffect != "Escape" and skillChoice.statusEffect != "TargetStances":
                            python:
                                holder = statusCheck(attacker, defender, skillChoice, waiting)
                                defender = holder[0]
                                stanceGo = holder[2]
                                statusEffectiveText = holder[3]
                                if AppliedStanceThisAttack == 0:
                                    holderS = ApplyStance(attacker, defender, skillChoice, justEscapedStance, stanceDurabilityHoldOverAttacker, stanceDurabilityHoldOverTarget)
                                    AppliedStanceThisAttack = 1
                                    stanceDurabilityHoldOverAttacker = 0
                                    stanceDurabilityHoldOverTarget = 0
                                    defender = holderS[1]
                                    attacker = holderS[0]
                                    justEscapedStance = holderS[2]
                        else:
                            if skillChoice.statusPotency > 0 or skillChoice.statusEffect == "Escape" or skillChoice.statusEffect == "TargetStances":
                                python:
                                    holder = statusBuff(attacker, defender, skillChoice, waiting)
                                    attacker = holder[0]
                                    defender = holder[2]
                                    stanceGo = holder[3]
                                    statusEffectiveText = holder[4]
                            else:
                                python:
                                    holder = statusBuff(defender, attacker, skillChoice, waiting)
                                    attacker = holder[2]
                                    defender = holder[0]
                                    stanceGo = holder[3]
                                    statusEffectiveText = holder[4]


                        if(stanceGo == "True"):
                            #call onHitTalk(defender, attacker, skillChoice) from _call_onHitTalk_1
                            if attacker.species != "Player":
                                call PreMonDialogueGet from _call_PreMonDialogueGet_2
                                call MonDialogueGet from _call_MonDialogueGet_2
                            if skillChoice.removesStance[0] != "" and skillChoice.removesStance[0] != "None":
                                python:
                                    for removeTheStance in skillChoice.removesStance:
                                        if removeTheStance != "All" and removeTheStance != "Target":
                                            attacker.removeStanceByName(removeTheStance)
                                            defender.removeStanceByName(removeTheStance)
                                        elif removeTheStance == "Target":
                                            if attacker.species == "Player":
                                                for each in defender.combatStance:
                                                    attacker.removeStanceByName(each.Stance)
                                                defender.clearStance()
                                            else:
                                                for each in attacker.combatStance:
                                                    defender.removeStanceByName(each.Stance)
                                                attacker.clearStance()
                                        else:
                                            player.clearStance()
                                            atkLo = 0
                                            while atkLo < len(monsterEncounter):
                                                monsterEncounter[atkLo].clearStance()
                                                atkLo+=1

                        if skillChoice.statusEffect != "Analyze":
                            $ display += holder[1]
                            $ OverrideSleeping = 0
                            if skillChoice.descrips == "PlayWhilePlayerSleeping":
                                $ OverrideSleeping = 1

                            if player.statusEffects.sleep.potency != -99 or OverrideSleeping == 1:
                                call read from _call_read_14

                $ atkLo += 1

            if(skillChoice.skillType == "Healing" or skillChoice.skillType == "HealingEP" or skillChoice.skillType == "HealingSP" or skillChoice.skillType == "StatusHeal"):
                python:
                    holder = HealCalc(attacker, skillChoice)
                    attacker = holder[0]
                    display += holder[1]
                $ OverrideSleeping = 0
                if skillChoice.descrips == "PlayWhilePlayerSleeping":
                    $ OverrideSleeping = 1

                if player.statusEffects.sleep.potency != -99 or OverrideSleeping == 1:
                    call read from _call_read_20


    $ theLastAttacker = attacker

    $ currentTarget = defender

    if player.statusEffects.sleep.potency == -99:
        if attacker.species != "Player":
            $ display = defender.name + " has dirty dreams about " + attacker.name + "."
            call read from _call_read_23


    if(stanceGo == "True" or attackHit == "True"):
        $ display = ""


        if attacker.species != "Player":
            if skillChoice.restraintStruggle[0] != "" and defender.restrainer.name == attacker.name:

                $ defender.restraintStruggle = []
                $ defender.restraintStruggleCharmed = []
                $ defender.restraintEscaped = []
                $ defender.restraintEscapedFail = []
                $ defender.restraintOnLoss = []

                $ defender.restraintStruggle = skillChoice.restraintStruggle
                $ defender.restraintStruggleCharmed = skillChoice.restraintStruggleCharmed
                $ defender.restraintEscaped = skillChoice.restraintEscaped
                $ defender.restraintEscapedFail = skillChoice.restraintEscapedFail
                $ defender.restraintOnLoss = skillChoice.restraintOnLoss

            elif defender.restrainer.name == attacker.name:
                python:
                    foundLine = 0

                    for each in attacker.combatDialogue:
                        if each.lineTrigger == "RestraintStruggle" :
                            for possibleOptions in each.move:
                                if possibleOptions == skillChoice.name and foundLine == 0:
                                    defender.restraintStruggle = each.theText
                                    foundLine = 1

                    foundLine = 0
                    for each in attacker.combatDialogue:
                        if each.lineTrigger == "RestraintStruggleCharmed" :
                            for possibleOptions in each.move:
                                if possibleOptions == skillChoice.name and foundLine == 0:
                                    defender.restraintStruggleCharmed = each.theText
                                    foundLine = 1

                    foundLine = 0
                    for each in attacker.combatDialogue:
                        if each.lineTrigger == "RestraintEscaped" :
                            for possibleOptions in each.move:
                                if possibleOptions == skillChoice.name and foundLine == 0:
                                    defender.restraintEscaped = each.theText
                                    foundLine = 1

                    foundLine = 0
                    for each in attacker.combatDialogue:
                        if each.lineTrigger == "RestraintEscapedFail" :
                            for possibleOptions in each.move:
                                if possibleOptions == skillChoice.name and foundLine == 0:
                                    defender.restraintEscapedFail = each.theText
                                    foundLine = 1



        $ loop = 1
        if skillChoice.removesStance[0] == "All" or skillChoice.removesStance[0] == "Target":
            if attacker.species == "Player":
                $ justEscapedStance = 2
        if skillChoice.statusEffect == "Escape":
            call EndAllEffects from _call_EndAllEffects_4


        if(skillChoice.targetType == "single"):
            $ loop = 1
        elif skillChoice.targetType == "all" and skillChoice.skillType != "Healing" and skillChoice.skillType != "HealingEP" and skillChoice.skillType != "HealingSP" and skillChoice.skillType != "StatusHeal" and attacker.species == "Player":
            $ loop = len(monsterEncounter)
        $ atkLo = 0
        while atkLo < loop:
            if loop != 1:
                $ defender = monsterEncounter[atkLo]
                $ display = ""
            if hitAll == 1:
                $ CombatFunctionEnemytarget = atkLo
            $ Speaker = Character(_(defender.name))
            if(stanceGo == "True" or attackHit == "True"):
                call onRecoilTalk(defender, attacker, skillChoice) from _call_onRecoilTalk
                if display != "":
                    call read from _call_read
                $ display = ""
                call onHitPreTalk(defender, attacker, skillChoice) from _call_onHitPreTalk
                call onHitTalk(defender, attacker, skillChoice) from _call_onHitTalk
            if display != "":

                call read from _call_read_22
            $ atkLo += 1

    if stanceGo == "True" and skillChoice.outcome == "OrgasmCheck" and skillChoice.skillType == "statusEffect":
        $ attackHit = "True"

    $ orgasmTarget = currentTarget
    $ orgasmCauser = theLastAttacker
    if(attackHit == "True"):
        $ orgasmGo = 1
        if orgasmTarget.species == "Player" and skipPlayerOrgasm == 1:
            $ orgasmGo = 0
        if orgasmTarget.species != "Player" and skipMonsterOrgasm == 1:
            $ orgasmGo = 0
        if skipTargetOrgasm == 1:
            $ orgasmGo = 0

        if orgasmGo == 1:
            call theOrgasmCheck from _call_theOrgasmCheck
        else:
            call edgeCheck from _call_edgeCheck

    if recoilHit >= 1 and player.statusEffects.surrender.duration <= 0 and currentTarget.stats.sp != 0 :
        $ orgasmTarget = theLastAttacker
        $ orgasmCauser = currentTarget
        $ orgasmGo = 1

        if orgasmTarget.species == "Player" and skipPlayerOrgasm == 1:
            $ orgasmGo = 0
        if orgasmTarget.species != "Player" and skipMonsterOrgasm == 1:
            $ orgasmGo = 0
        if skipAttackOrgasm == 1:
            $ orgasmGo = 0
        if orgasmGo == 1:
            call theOrgasmCheck from _call_theOrgasmCheck_2
        else:
            call edgeCheck from _call_edgeCheck_1

    $ skipTargetOrgasm = 0
    $ skipAttackOrgasm = 0

    $ orgasmTarget = currentTarget
    $ orgasmCauser = theLastAttacker
    if attacker.species == "Player":
        call MonsterLossCheck from _call_MonsterLossCheck_1
    else:
        call PlayerLossCheck from _call_PlayerLossCheck_1

    if recoilHit >= 1 and player.statusEffects.surrender.duration <= 0:
        $ orgasmTarget = theLastAttacker
        $ orgasmCauser = currentTarget
        if orgasmCauser.species == "Player":
            call MonsterLossCheck from _call_MonsterLossCheck
        else:
            call PlayerLossCheck from _call_PlayerLossCheck

    return




label MonDialogueGet:
    python:
        playLine = 0
        if defender.stats.hp >= defender.stats.max_true_hp*0.65 and renpy.random.randint(0, 100) < 70 and playerCloseMark == 0:
            playerCloseMark = 1

            for each in attacker.combatDialogue:
                for possibleOptions in each.move:
                    if possibleOptions == monSkillChoice[m].name and foundLine == 0:
                        playLine = 1
            #if monSkillChoice.statusEffect == "" and monSkillChoice.skillType == "statusEffect":


            if playLine == 1:
                for each in attacker.combatDialogue:
                    if each.lineTrigger == "PlayerLowHealth":
                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)] + " "

        if playLine == 0:
            onlyOnce = 0
            for each in attacker.combatDialogue:
                canGo = 0
                if each.lineTrigger == "UsesMove" or each.lineTrigger == "usesMoveA":
                    for possibleOptions in each.move:
                        if  possibleOptions == monSkillChoice[m].name and onlyOnce == 0:
                            if monSkillChoice[m].requiresStance == "Penetration":
                                for stanceChek in attacker.combatStance:
                                    if stanceChek.Stance == "Sex":
                                        if each.lineTrigger == "UsesMove":
                                            canGo = 1
                                    elif stanceChek.Stance == "Anal":
                                        if each.lineTrigger == "usesMoveA":
                                            canGo = 1
                            else:
                                canGo = 1

                            if canGo == 1:
                                onlyOnce = 1
                                display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                if display[-1] != "|":
                                    display = display + " "
    return

label PreMonDialogueGet:
    python:
        playLine = 0
        if playLine == 0:
            onlyOnce = 0
            for each in attacker.combatDialogue:
                canGo = 0
                if each.lineTrigger == "UsesMovePre":
                    for possibleOptions in each.move:
                        if  possibleOptions == monSkillChoice[m].name and onlyOnce == 0:
                            if monSkillChoice[m].requiresStance == "Penetration":
                                for stanceChek in attacker.combatStance:
                                    if stanceChek.Stance == "Sex":
                                        canGo = 1
                                    elif stanceChek.Stance == "Anal":
                                        canGo = 1
                            else:
                                canGo = 1

                            if canGo == 1:
                                onlyOnce = 1
                                display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                if display[-1] != "|":
                                    display = display + " "
    return


label theOrgasmCheck:
    $ LossCheck = 0
    $ orgasmArray = []
    $ ignoreOrgasm = 0
    $ edging = 0
    $ spiritLost = 0
    python:
        if orgasmTarget.species == "Player":
            orgasmArray.append(orgasmTarget)
        else:
            for each in monsterEncounter:
                orgasmArray.append(each)

    while LossCheck < len(orgasmArray):
        $ show = 0
        if orgasmTarget.species == "Player":
            $ Speaker = Character(orgasmCauser.name)
        else:
            $ Speaker = Character(orgasmArray[LossCheck].name)


        $ orgasmLine = ""
        $ holder = OrgasmCheck(orgasmArray[LossCheck], orgasmCauser, lastAttack)
        $ orgasmArray[LossCheck] = holder[0]
        $ orgasmCauser = holder[1]
        $ orgasmLine = holder[2]

        if orgasmTarget.species == "Player" and spiritLost > 0 and edging == 0 and ignoreOrgasm == 0:
            call TimeEvent(CardType="PlayerOrgasm", LoopedList=OnPlayerClimaxList) from _call_TimeEvent

        if orgasmLine != "":
            $ display = orgasmLine
            call read from _call_read_7


        if display != "" and edging == 0 and ignoreOrgasm == 0 and spiritLost > 0:
            $ display = ""
            python:
                lineFound = 0
                LastResortLine = ""
                if orgasmArray[LossCheck].species != "Player":
                    for orgline in orgasmArray[LossCheck].combatDialogue:
                        if orgline.lineTrigger == "PostOrgasm":
                            for monStance in orgasmArray[LossCheck].combatStance:
                                showLine = 0
                                for possibleOptions in orgline.move:
                                    if lastAttack.name == possibleOptions:
                                        showLine = 1
                                    elif monStance.Stance == possibleOptions:
                                        showLine = 1
                                    elif possibleOptions == "":
                                        LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                if lineFound == 0 and showLine == 1:
                                    display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "
                                    lineFound = 1
                                    break
                            if lineFound == 1:
                                break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine
            if display != "":
                call read from _call_read_6

            $ display = ""

            $ holder = PostOrgasmCheck(orgasmArray[LossCheck], orgasmCauser, lastAttack)
            $ orgasmArray[LossCheck] = holder[0]
            $ orgasmCauser = holder[1]
            $ display = holder[2]

            if display != "":
                $ disLineOne = "As " + orgasmCauser.name + " takes in your semen, "
                $ display = disLineOne + display
                call read from _call_read_31
        $ LossCheck += 1


        $ spiritLost = 0

    $ orgasmArray = []
    return

label edgeCheck:
    $ LossCheck = 0
    $ orgasmArray = []
    $ ignoreOrgasm = 0
    $ edging = 0
    $ spiritLost = 0
    python:
        if orgasmTarget.species == "Player":
            orgasmArray.append(orgasmTarget)
        else:
            for each in monsterEncounter:
                orgasmArray.append(each)

    while LossCheck < len(orgasmArray):
        $ show = 0
        if orgasmTarget.species == "Player":
            $ Speaker = Character(orgasmCauser.name)
        else:
            $ Speaker = Character(orgasmArray[LossCheck].name)


        $ display = ""
        if checkHPLosses(orgasmTarget, orgasmCauser, move) == "Orgasm":
            python:
                lineFound = 0
                LastResortLine = ""
                if orgasmCauser.species != "Player":
                    for orgline in orgasmCauser.combatDialogue:
                        if orgline.lineTrigger == "OnPlayerEdge":
                            for monStance in orgasmCauser.combatStance:
                                showLine = 0
                                for possibleOptions in orgline.move:
                                    if lastAttack.name == possibleOptions:
                                        showLine = 1
                                    elif monStance.Stance == possibleOptions:
                                        showLine = 1
                                    elif possibleOptions == "":
                                        LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                if lineFound == 0 and showLine == 1:
                                    display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "
                                    lineFound = 1
                                    break
                            if lineFound == 1:
                                break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine
                else:
                    CombatFunctionEnemytarget = LossCheck
                    CombatFunctionEnemyInitial = LossCheck
                    for orgline in orgasmArray[LossCheck].combatDialogue:
                        if orgline.lineTrigger == "OnEdge":
                            for monStance in orgasmArray[LossCheck].combatStance:
                                showLine = 0
                                for possibleOptions in orgline.move:
                                    if monStance.Stance == possibleOptions:
                                        showLine = 1
                                    elif possibleOptions == "":
                                        LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                if lineFound == 0 and showLine == 1:
                                    display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)]
                                    lineFound = 1
                            if lineFound == 1:
                                break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine


        if display != "":
            call read from _call_read_4
        $ LossCheck += 1

    $ orgasmArray = []
    return

label PlayerLossCheck:
    $ display = ""
    if checkSPLosses(orgasmTarget, orgasmCauser, lastAttack) == "Lost":
        $ display += player.name + ", shaking with lust, is no longer able to resist!"
        $ show = 1
        call read from _call_read_8
        jump combatLoss

    return




label MonsterLossCheck:
    $ monLossCheck = 0

    while monLossCheck < len(monsterEncounter) and player.stats.sp > 0:
        $ Speaker = Character(monsterEncounter[monLossCheck].name)
        $ out = 0
        $ show = 0
        if checkSPLosses(monsterEncounter[monLossCheck], orgasmCauser, lastAttack) == "Lost":

            #$ targetName = monsterEncounter[monLossCheck].name
            $ targetName =  monsterEncounter[monLossCheck].name
            $ targetHeOrShe = getHeOrShe( monsterEncounter[monLossCheck])
            $ targetHisOrHer = getHisOrHer( monsterEncounter[monLossCheck])
            $ targetHimOrHer = getHimOrHer(monsterEncounter[monLossCheck])
            $ targetYouOrMonsterName = getYouOrMonsterName(monsterEncounter[monLossCheck])
            $ theTarget = theForGeneric(monsterEncounter[monLossCheck])
            $ display = "Shaking with pleasure, {TargetName} is left completely helpless as {TargetHeOrShe} starts to magically fade away."
            $ show = 1
            $ out = 1

        else:
            if(show == 1):

                $ display = "But {TargetHeOrShe} seems ready to keep going!"




        if(show == 1 and display != "" and display != " " and display != "\n"):
            call read from _call_read_9

            if out == 1:
                if monsterEncounter[monLossCheck].restraintEscaped[0] != "":
                    $ display = monsterEncounter[monLossCheck].restraintOnLoss[renpy.random.randint(-1, len(monsterEncounter[monLossCheck].restraintEscaped)-1)]
                    call read from _call_read_2


        $ heldMon = Monster(Stats())
        $ display = ""
        python:
            if out == 1:
                heldMon = copy.deepcopy(monsterEncounter[monLossCheck])

                DefeatMonster(monLossCheck)
                lineFound = 0
                LastResortLine = ""
                if heldMon.species != "Player":
                    if len(monsterEncounter) > 0:
                        for orgline in heldMon.combatDialogue:
                            if orgline.lineTrigger == "OnLoss":
                                for monStance in heldMon.combatStance:
                                    showLine = 0
                                    for possibleOptions in orgline.move:
                                        if lastAttack.name == possibleOptions:
                                            showLine = 1
                                        elif monStance.Stance == possibleOptions:
                                            showLine = 1
                                        elif possibleOptions == "":
                                            LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                    if lineFound == 0 and showLine == 1:
                                        display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "
                                        lineFound = 1
                                        break
                                if lineFound == 1:
                                    break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine


            else:
                monLossCheck += 1
        if display != "":
            call read from _call_read_15
        $ heldMon = Monster(Stats())


    return





label setAttacker(attacker, skillChoice):
    $ attackerName = attacker.name
    $ attackerHeOrShe = getHeOrShe(attacker)
    $ attackerHisOrHer = getHisOrHer(attacker)
    $ attackerHimOrHer = getHimOrHer(attacker)
    $ attackerYouOrMonsterName = getYouOrMonsterName(attacker)
    $ theAttacker = theForGeneric(attacker)

    $ display = ""

    python:
        notMeStance = 1
        for each in skillChoice.requiresTargetStance:
            if skillChoice.requiresStance == each:
                notMeStance == 0

        if len(skillChoice.requiresTargetStance) > 1 or notMeStance == 1:
            mset = 0
            ignoreFirstStance = 0
            for each in skillChoice.requiresTargetStance:
                if ignoreFirstStance > 0 or skillChoice.requiresStance == "Any":
                    for monE in monsterEncounter:
                        if monE.name != attacker.name:
                            stanceFound = 0
                            for stanceChek in monE.combatStance:
                                passSearch = 0
                                if each == "Penetration" and stanceFound == 0:
                                    if stanceChek.Stance == "Sex":
                                        passSearch = 1
                                    elif stanceChek.Stance == "Anal":
                                        passSearch = 1
                                if stanceChek.Stance == each and stanceFound == 0:
                                    passSearch = 1
                                if passSearch == 1:
                                    stanceFound = 1
                                    if mset == 0:
                                        attackerNameStance2 = monE.name
                                    elif mset == 1:
                                        attackerNameStance3 = monE.name
                                    elif mset == 2:
                                        attackerNameStance4 = monE.name
                                    elif mset == 3:
                                        attackerNameStance5 = monE.name
                                    mset +=1
                ignoreFirstStance = 1

    return



label setDefender(defender):
    $ targetName = defender.name
    $ targetHeOrShe = getHeOrShe(defender)
    $ targetHisOrHer = getHisOrHer(defender)
    $ targetHimOrHer = getHimOrHer(defender)
    $ targetYouOrMonsterName = getYouOrMonsterName(defender)
    $ theTarget = theForGeneric(defender)
    return


label CounterTalk(defender, attacker, skillChoice, altName):
    $ counterArray = []
    python:
        if attacker.species == "Player":
            canGo = 0
            for each in defender.combatDialogue:
                if canGo == 0:
                    allowCheck = 0
                    if each.lineTrigger == "AutoCounter" or each.lineTrigger == "AutoCounterSkill":
                        for possibleOptions in each.move:
                            if skillChoice.name == possibleOptions or altName == possibleOptions:
                                allowCheck = 1

                    if each.lineTrigger == "AutoCounterSkillTag":
                        for sTag in skillChoice.skillTags:
                            checkTag = copy.deepcopy(sTag)
                            for possibleOptions in each.move:
                                if checkTag == possibleOptions:
                                    allowCheck = 1
                                elif checkTag == "Penetration":
                                    for stanceChek in attacker.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            checkTag = "Sex"
                                        elif stanceChek.Stance == "Anal":
                                            checkTag = "Ass"
                                    if checkTag == possibleOptions:
                                        allowCheck = 1

                    if each.lineTrigger == "AutoCounterSkillFetish":
                        for sTag in skillChoice.fetishTags:
                            checkTag = copy.deepcopy(sTag)
                            for possibleOptions in each.move:
                                if checkTag == possibleOptions:
                                    allowCheck = 1
                                elif checkTag == "Penetration":
                                    for stanceChek in attacker.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            checkTag = "Sex"
                                        elif stanceChek.Stance == "Anal":
                                            checkTag = "Ass"
                                    if checkTag == possibleOptions:
                                        allowCheck = 1

                    if allowCheck == 1:
                            counterArray.append(each.theText[renpy.random.randint(-1, len(each.theText)-1)])

                    if each.lineTrigger == "OffenceCounter":
                        counterit = 1
                        if skillChoice.skillType == "Healing" or skillChoice.skillType == "HealingEP" or skillChoice.skillType == "HealingSP" or skillChoice.skillType == "StatusHeal" or skillChoice.name == "Run Away" or skillChoice.name == " " or skillChoice.name =="Struggle"  or skillChoice.name =="Defend" or skillChoice.name =="Wait" or skillChoice.name == "Push Away":
                            counterit = 0
                        elif skillChoice.skillType == "statusEffect":
                            counterit = 0
                            if skillChoice.statusPotency <= 0:
                                counterit = 1
                            elif skillChoice.statusEffect == "Charm" or skillChoice.statusEffect == "Stun" or skillChoice.statusEffect == "Aphrodisiac" or skillChoice.statusEffect == "Restrain"  or skillChoice.statusEffect == "Sleep" or skillChoice.statusEffect == "Paralysis" or skillChoice.statusEffect == "Trance":
                                counterit = 1

                        if counterit == 1:
                            counterArray.append(each.theText[renpy.random.randint(-1, len(each.theText)-1)])


                    if each.lineTrigger == "AnyCounter":
                        counterit = 1
                        if skillChoice.name == "Run Away" or skillChoice.name == " " or skillChoice.name =="Struggle"  or skillChoice.name =="Defend" or skillChoice.name =="Wait" or skillChoice.name == "Push Away":
                            counterit = 0
                        if counterit == 1:
                            counterArray.append(each.theText[renpy.random.randint(-1, len(each.theText)-1)])

    return


label onRecoilTalk(defender, attacker, skillChoice):
    python:
        if attacker.species == "Player" and recoilHit > 0:
            if defender.statusEffects.sleep.potency != -99:
                for each in defender.combatDialogue:
                    canGo = 0
                    if (each.lineTrigger == "PlayerRecoil" or each.lineTrigger == "PlayerRecoilA") and canGo == 0:
                        for possibleOptions in each.move:
                            if skillChoice.name == possibleOptions and canGo == 0:
                                if skillChoice.requiresStance == "Penetration":
                                    for stanceChek in defender.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            if each.lineTrigger == "PlayerRecoil":
                                                canGo = 1
                                        elif stanceChek.Stance == "Anal":
                                            if each.lineTrigger == "PlayerRecoilA":
                                                canGo = 1
                                else:
                                    canGo = 1
                    if canGo == 1:
                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)] + " "

    return


label onHitTalk(defender, attacker, skillChoice):
    python:
        if attacker.species == "Player":
            if defender.statusEffects.sleep.potency != -99:

                if  defender.stats.hp >= (defender.stats.max_true_hp*0.70) and defender.lowHealthMark == "False":
                    defender.lowHealthMark = "True"
                    for each in defender.combatDialogue:
                        if each.lineTrigger == "LowHealth":
                            display += each.theText[renpy.random.randint(-1, len(each.theText)-1)] + " "

                else:
                    for each in defender.combatDialogue:
                        canGo = 0
                        if skillChoice.statusEffect == "TargetStances" or skillChoice.statusEffect == "Escape" or skillChoice.targetType == "Escape":
                            for possibleOptions in each.move:
                                if possibleOptions == "" or possibleOptions == skillChoice.name:
                                    if each.lineTrigger == "Escape" and justEscapedStance == 2:
                                        canGo = 1


                        if each.lineTrigger == "HitWith" or each.lineTrigger == "HitWithA" and canGo == 0:
                            for possibleOptions in each.move:
                                if skillChoice.name == possibleOptions and canGo == 0:
                                    if skillChoice.requiresStance == "Penetration":
                                        for stanceChek in defender.combatStance:
                                            if stanceChek.Stance == "Sex":
                                                if each.lineTrigger == "HitWith":
                                                    canGo = 1
                                            elif stanceChek.Stance == "Anal":
                                                if each.lineTrigger == "HitWithA":
                                                    canGo = 1
                                    else:
                                        canGo = 1

                        if canGo == 1:
                            display += each.theText[renpy.random.randint(-1, len(each.theText)-1)] + " "

    return

label onHitPreTalk(defender, attacker, skillChoice):
    python:
        if attacker.species == "Player":
            if defender.statusEffects.sleep.potency != -99:
                for each in defender.combatDialogue:
                    canGo = 0
                    if each.lineTrigger == "HitWithPre" and canGo == 0:
                        for possibleOptions in each.move:
                            if skillChoice.name == possibleOptions and canGo == 0:
                                if skillChoice.requiresStance == "Penetration":
                                    for stanceChek in defender.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            canGo = 1
                                        elif stanceChek.Stance == "Anal":
                                            canGo = 1
                                else:
                                    canGo = 1

                    if canGo == 1:
                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)] + " "

    return


label combatFunctions:
    python:
        def OrgasmCheck(theTarget, attacker, move):
            global HideOrgasmLine, ignoreOrgasm, edging, spiritLost
            HideOrgasmLine = 0
            display = ""
            if checkHPLosses(theTarget, attacker, move) == "Orgasm":

                spiritLost = 1

                ignoreOrgasm = 0
                edging = 0
                edgingBaseChance = 0

                for perk in theTarget.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "Edging":
                            edgingBaseChance += perk.EffectPower[p]

                        if perk.PerkType[p] == "ResistFinalOrgasm":
                            if theTarget.stats.sp == 1 and (theTarget.statusEffects.surrender.duration <= 0) and edging == 0:
                                passChance = perk.EffectPower[p] + theTarget.stats.Luck*0.5 + theTarget.stats.Willpower*0.5
                                passChance += getVirility(theTarget)*0.1
                                randomRoll = renpy.random.randint(0, 100)
                                if passChance >= 60:
                                    passChance = 60
                                if randomRoll < passChance:
                                    ignoreOrgasm = 1
                        p += 1

                if edgingBaseChance > 0 :
                    if theTarget.stats.hp < theTarget.stats.max_true_hp*3:
                        passChance =  edgingBaseChance + theTarget.stats.Willpower*0.5 + theTarget.stats.Power*0.5 + theTarget.stats.Luck*0.5
                        randomRoll = renpy.random.randint(0, 100)
                        if randomRoll < passChance:
                            edging = 1
                        elif theTarget.stats.hp > theTarget.stats.max_true_hp*1.5:
                            spiritLost += 1
                    else:
                        showWake = theTarget.name + " can't take any more of this mind-blanking edging and an explosive orgasm starts to tear through " + getHisOrHer(theTarget) + " shivering body!|n|"
                        spiritLost += 2
                        display =  showWake + display

                spiritLost = SpiritCalulation(theTarget, spiritLost, 1)

                if ignoreOrgasm == 0 and edging == 0:


                    if theTarget.species == "Player":
                        actualAmountLost = spiritLost if theTarget.stats.sp >= spiritLost else theTarget.stats.sp 
                        increaseFetishOnOrgasm(lastAttack, attacker, actualAmountLost)

                    theTarget.stats.sp -= spiritLost

                    theTarget.stats.hp = 0
                elif ignoreOrgasm == 1 and edging == 0:
                    showWake = "Sensing the cumming end, " + theTarget.name + " prepares to endure the final orgasm!|n|"
                    display =  showWake + display

                if theTarget.statusEffects.sleep.potency == -99:
                    showWake = "With a moan, " + theTarget.name + " awakens at the edge of a blissful orgasm!|n|"
                    display =  showWake + display
                    if theTarget.species == "Player":
                        spiritLost += int(math.floor(theTarget.stats.max_true_sp*0.25))
                        theTarget.stats.sp -= int(math.floor(theTarget.stats.max_true_sp*0.25))

                    theTarget.statusEffects.sleep.potency = 0
                    #CheckImmunity = getFromName("Sleep Immune", theTarget.perks)
                    #if CheckImmunity == -1:
                    #    theTarget.giveOrTakePerk("Sleep Immune", 1)
                    #else:
                    #    theTarget.giveOrTakePerk("Sleep Immune", -1)
                    #    theTarget.giveOrTakePerk("Sleep Immune", 1)
                    theTarget.statusEffects.sleep.duration = 0

                lineFound = 0
                LastResortLine = ""
                if attacker.species != "Player":
                    for orgline in attacker.combatDialogue:
                        if orgline.lineTrigger == "OnPlayerOrgasm":
                            for monStance in attacker.combatStance:
                                showLine = 0
                                for possibleOptions in orgline.move:
                                    if lastAttack.name == possibleOptions:
                                        showLine = 1
                                    elif monStance.Stance == possibleOptions:
                                        showLine = 1
                                    elif possibleOptions == "":
                                        LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                if lineFound == 0 and showLine == 1:
                                    display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "
                                    lineFound = 1
                                    break
                            if lineFound == 1:
                                break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine
                else:
                    global CombatFunctionEnemytarget, CombatFunctionEnemyInitial, LossCheck
                    CombatFunctionEnemytarget = LossCheck
                    CombatFunctionEnemyInitial = LossCheck
                    for orgline in theTarget.combatDialogue:
                        if orgline.lineTrigger == "OnOrgasm":
                            for monStance in theTarget.combatStance:
                                showLine = 0
                                for possibleOptions in orgline.move:
                                    if monStance.Stance == possibleOptions:
                                        showLine = 1
                                    elif possibleOptions == "":
                                        LastResortLine = orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)] + " "

                                if lineFound == 0 and showLine == 1:
                                    display += orgline.theText[renpy.random.randint(-1, len(orgline.theText)-1)]
                                    lineFound = 1
                            if lineFound == 1:
                                break
                    if lineFound == 0 and LastResortLine != "":
                        display += LastResortLine
                if ignoreOrgasm == 0 and edging == 0:
                    if lineFound == 1 and HideOrgasmLine == 0 and theTarget.species == "Player":
                        display += " " + theTarget.name + " loses {SpiritLost} spirit.\n"
                    else:
                        the = theForGeneric(theTarget)
                        display += " " + the + theTarget.name + " cries out with ecstasy as " + getHeOrShe(theTarget) + " orgasms and loses " + str(spiritLost) +" spirit!\n"
                elif edging == 1:
                    passChance =  10 + theTarget.stats.Willpower + theTarget.stats.Power + theTarget.stats.Luck*0.5 + theTarget.resistancesStatusEffects.Stun
                    randomRoll = renpy.random.randint(0, 100)
                    if randomRoll > passChance:
                        theTarget.statusEffects.stunned.duration = 2
                        display = "Despite the intense arousal, " + theTarget.name + " manages to stay on the edge of orgasm, but is shivering in so much ecstasy " + getHeOrShe(theTarget) + " can't act!\n"
                    else:
                        display = "Despite the intense arousal, " + theTarget.name + " manages to stay on the edge of orgasm, shuddering with bliss!\n"

                if theTarget.species == "Player":
                    global playerCloseMark
                    playerCloseMark = 0

            return [theTarget, attacker, display]


        def PostOrgasmCheck(theTarget, attacker, move):
            display = ""

            recoverAmount = 0
            buffPower = 0
            DrainEP = 0

            for perk in attacker.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "SemenHeal":
                        for each in attacker.combatStance:
                            if each.Stance == "Sex" or each.Stance == "Anal" or each.Stance == "Blowjob" or each.Stance == "Titfuck" or each.Stance == "Tail Fuck":
                                recoverAmount = perk.EffectPower[p] * (0.5+getVirility(theTarget)*0.01)

                    if perk.PerkType[p] == "SemenAttackBoost":
                        for each in attacker.combatStance:
                            if each.Stance == "Sex" or each.Stance == "Anal" or each.Stance == "Blowjob" or each.Stance == "Titfuck" or each.Stance == "Tail Fuck":
                                buffPower += perk.EffectPower[p]

                    if perk.PerkType[p] == "OrgasmEnergyDrain":
                        DrainEP += perk.EffectPower[p]

                    if perk.PerkType[p] == "SemenEnergyDrain":
                        for each in attacker.combatStance:
                            if each.Stance == "Sex" or each.Stance == "Anal" or each.Stance == "Blowjob" or each.Stance == "Titfuck" or each.Stance == "Tail Fuck":
                                DrainEP += perk.EffectPower[p]
                    p += 1

            if recoverAmount > 0:
                recoverAmount *= renpy.random.randint(75, 125)*0.01
                recoverAmount = math.floor(recoverAmount)
                recoverAmount= int(recoverAmount)
                attacker.stats.hp -= recoverAmount
                display += attacker.name + " seems filled with renewed energy! " + attacker.name + " calms down " + str(recoverAmount) + " arousal!\n"

            if buffPower > 0:
                    canGetBuff = 1
                    for each in attacker.statusEffects.tempAtk:
                        if each.skillText == "Semen Boost":
                            canGetBuff = 0
                            each.duration = 10
                    if canGetBuff == 1 and buffPower * (0.5+getVirility(theTarget)*0.01) > 0:
                        attacker.statusEffects.tempAtk.append(StatusEffect(10, buffPower* (0.5+getVirility(theTarget)*0.01), "Semen Boost"))

                    if display == "":
                        display += "A lustfully manic expression spreads over "+ attacker.name + "'s face!\n"
                    else:
                        display += "A lustfully manic expression spreads over "+ attacker.name + "'s face!\n"

            if DrainEP > 0:
                if attacker.species == "Player":
                    attacker.stats.ep += DrainEP
                    if attacker.stats.ep >= attacker.stats.max_true_ep:
                        attacker.stats.ep = attacker.stats.max_true_ep
                else:
                    if 0.5 < (0.5+getVirility(theTarget)*0.01):
                        DrainEP = DrainEP * (0.5+getVirility(theTarget)*0.01)
                    else:
                        DrainEP = DrainEP * (0.5)
                    DrainEP *= (renpy.random.randint(75, 125)*0.01)
                    DrainEP = math.floor(DrainEP)
                    DrainEP = int(DrainEP)
                    theTarget.stats.ep -= DrainEP
                    if theTarget.stats.ep <= 0:
                        theTarget.stats.ep = 0
                    if display == "":
                        display += "A magical glow flows from you to "+ attacker.name + "! You lost " + str(DrainEP) +" energy!\n"
                    else:
                        display += "A magical glow flows from you to "+ attacker.name + "! You lost " + str(DrainEP) +" energy!\n"



            return [theTarget, attacker, display]


        def SpiritCalulation(theTarget, SpiritLoss=1, eventapplicable=0):
            for perk in theTarget.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "MultiplySpirit Loss":
                        SpiritLoss *= perk.EffectPower[p]

                    if perk.PerkType[p] == "RemovedOnOrgasm":
                        player.giveOrTakePerk(perk.name, -1)
                        break
                    p += 1



            #if eventapplicable == 1:
                #if theTarget.stats.hp > theTarget.stats.max_hp*2:
                    #SpiritLoss += 1

                #if theTarget.stats.hp > theTarget.stats.max_hp*2.5:
                    #SpiritLoss += 1

                #if theTarget.stats.hp > theTarget.stats.max_hp*3:
                    #SpiritLoss += 1

            return SpiritLoss

        def DefeatMonster( monLossCheck):
            global monsterEncounter, trueMonsterEncounter, monInititive, player, ExpPool, MoneyDrops, LootDrops, target, monSkillChoice, DefeatedEncounterMonsters
            monsterLvl = monsterEncounter[monLossCheck].stats.lvl 
            playerLvl = player.stats.lvl

            ## Handle EXPERIENCE
            expLvlMod = getExpModForLvlDiff(monsterLvl, playerLvl, difficulty);
            monsExp = monsterEncounter[monLossCheck].stats.Exp
            ExpBoost = 1
            for perk in monsterEncounter[monLossCheck].perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "ExpBoost":
                        ExpBoost += (perk.EffectPower[p])*0.01
                    p += 1
            ExpPool += monsExp*ExpBoost*expLvlMod

            ## Handle EROS
            monsEro = monsterEncounter[monLossCheck].moneyDropped
            eroLvlMod = getErosModForLvlDiff(monsterLvl, playerLvl, difficulty)

            EroBoost = 1
            for perk in monsterEncounter[monLossCheck].perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "ErosBoost":
                        EroBoost += (perk.EffectPower[p])*0.01
                    p += 1
            MoneyDrops += monsEro*EroBoost*eroLvlMod

            ## Handle ITEM DROPS
            for each in monsterEncounter[monLossCheck].ItemDropList:
                bonusChance = 1
                for perk in monsterEncounter[monLossCheck].perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] ==  "ItemDropChance":
                            bonusChance += (perk.EffectPower[p])*0.01
                        p += 1

                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "ItemDropChance":
                            bonusChance += (perk.EffectPower[p])*0.01
                        p += 1

                if renpy.random.randint(0,100) < (each.dropChance + player.stats.Luck*0.5)* bonusChance  :
                    LootDrops.append(each.name)

            trueMonsterEncounter[monLossCheck].combatStance = monsterEncounter[monLossCheck].combatStance
            DefeatedEncounterMonsters.append(copy.deepcopy(trueMonsterEncounter[monLossCheck]))

            if monsterEncounter[monLossCheck].combatStance[0].Stance != "None":
                for monStance in monsterEncounter[monLossCheck].combatStance:
                    player.removeStanceByName(monStance.Stance)

            if target == monLossCheck:
                target = 99
            elif target > monLossCheck:
                target -= 1


            del monsterEncounter[monLossCheck]
            del trueMonsterEncounter[monLossCheck]
            del monInititive[monLossCheck]
            if len(monSkillChoice) > 0 and len(monSkillChoice) > monLossCheck:
                del monSkillChoice[monLossCheck]

            return


        def ApplyStance(attacker, theTarget, move, justEscapedStance, stanceDurabilityHoldOverAttacker, stanceDurabilityHoldOverTarget):
            if move.startsStance[0] != "" and move.startsStance[0] != "None":
                if(stanceGo == "True"):
                    for stances in move.startsStance:
                        attacker.giveStance(stances, theTarget, move, stanceDurabilityHoldOverAttacker)

                        theTarget.giveStance(stances, attacker, move, stanceDurabilityHoldOverTarget)

                    if theTarget.species != "Player":
                        theTarget.putInStance = 1
                    else:
                        justEscapedStance = 1

            return [attacker, theTarget, justEscapedStance]

        def AttackCalc(attacker, theTarget, move, autoHits=0, increaseFetishOnHit = False):

            defenceMod = 1
            stanceApply = "False"
            effectiveText = ""
            damageMod = 1
            recoil = 0

            if (theTarget.statusEffects.surrender.duration > 0):
                surrenderMod = 1000
                damageMod += 1
            else:
                surrenderMod = 0




            if (theTarget.statusEffects.restrained.duration > 0 or theTarget.statusEffects.sleep.potency == -99 or  theTarget.statusEffects.trance.potency >= 11 or theTarget.statusEffects.stunned.duration >= 1 or autoHits == 1):
                restrainedMod = 1000
            else:
                restrainedMod = 0

            if (theTarget.statusEffects.paralysis.duration > 0):
                restrainedMod += theTarget.statusEffects.paralysis.potency*3

            if (theTarget.statusEffects.defend.duration > 0):
                defenceMod + 0.5

            fetishMod = 0
            for each in move.fetishTags:
                for fetishE in theTarget.FetishList:
                    checkTag = each
                    if checkTag == "Penetration":
                        for stanceChek in theTarget.combatStance:
                            if stanceChek.Stance == "Sex":
                                checkTag = "Sex"
                            elif stanceChek.Stance == "Anal":
                                checkTag = "Ass"
                    if checkTag == fetishE.name:
                        fetishMod += fetishE.Level*0.1

            StanceAccuaracyMod = 0

            for each in theTarget.combatStance:
                if each.Stance != "None":
                    StanceAccuaracyMod += 10

            critText = ""
            TargetsEvade = getBaseEvade(theTarget, StanceAccuaracyMod, defenceMod)
            attackerAcc = getBaseAccuracy(attacker, StanceAccuaracyMod)

            try:
                move.accuracy
            except:
                move.accuracy = 0


            allureFlatScaling = 0.10
            allureFlatPercentBoost = 0
            for perk in attacker.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "BaselineAllureFlatBuff":
                        allureFlatScaling += perk.EffectPower[p]*0.01

                    if perk.PerkType[p] == "BaselineAllureFlatPercentBoost":
                        allureFlatPercentBoost += perk.EffectPower[p]*0.01
                    p += 1

            if move.recoil > 0:
                recoilPercentBoost = 100
                recoilPercentDecreace = 100
                recoilAllureBoost = 100

                for perk in attacker.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "RecoilDamageTaken":
                            recoilPercentDecreace += perk.EffectPower[p]
                        p += 1

                for perk in defender.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "RecoilBoost":
                            recoilPercentBoost += perk.EffectPower[p]
                        if perk.PerkType[p] == "AllureRecoilBoost":
                            recoilAllureBoost += perk.EffectPower[p]
                        p += 1

                fetishMod = 100
                for each in move.fetishTags:
                    for fetishE in attacker.FetishList:
                        checkTag = each
                        if checkTag == "Penetration":
                            for stanceChek in attacker.combatStance:
                                if stanceChek.Stance == "Sex":
                                    checkTag = "Sex"
                                elif stanceChek.Stance == "Anal":
                                    checkTag = "Ass"
                        if checkTag == fetishE.name:
                            #if fetishE.Level >= 3:
                            #    fetishMod += 5
                            #if fetishE.Level >= 5:
                            #    fetishMod += 20
                            #if fetishE.Level >= 10:
                            #    fetishMod += 25
                            fetishMod += (fetishE.Level)

                recoilpercent = ((move.recoil*0.01 + ((theTarget.stats.Allure*0.25 + allureFlatPercentBoost)*0.01)*recoilAllureBoost*0.01)*(recoilPercentBoost*0.01))*(recoilPercentDecreace*0.01)
                recoil = (getDamageEstimate(attacker, move)*recoilpercent + (theTarget.stats.Allure*allureFlatScaling)*recoilAllureBoost*0.01)*(fetishMod*0.01)
                recoil *= getTotalBoost(theTarget, move)
                recoil *= (renpy.random.randint(90, 110)*0.01)
                recoil =  int(math.floor(recoil))


            if renpy.random.randint(0,100) + attackerAcc + move.accuracy >= TargetsEvade - surrenderMod - restrainedMod - fetishMod:
                Hit = 1
                stanceApply = "True"
                if theTarget.species == "Player" and increaseFetishOnHit:
                    increaseFetishOnBeingHit(move, attacker)

                if move.statusOutcome != "IgnoreAttack":
                    finalDamage = getDamageEstimate(attacker, move)

                    if move.scalesWithStatusScale != "":
                        if defender.statusEffects.hasThisStatusEffect("Defend") == True and move.scalesWithStatusScale == "Defend":
                            finalDamage += defender.statusEffects.defend.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.defend.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Stun") == True and move.scalesWithStatusScale == "Stun":
                            finalDamage += defender.statusEffects.stunned.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.stunned.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Charm") == True and move.scalesWithStatusScale == "Charm":
                            finalDamage += defender.statusEffects.charmed.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.charmed.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Aphrodisiac") == True and move.scalesWithStatusScale == "Aphrodisiac":
                            finalDamage += defender.statusEffects.aphrodisiac.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.aphrodisiac.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffectPotency("Sleep", 0) == True and move.scalesWithStatusScale == "Sleep":
                            finalDamage += defender.statusEffects.sleep.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.sleep.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Trance") == True and move.scalesWithStatusScale == "Trance":
                            finalDamage += defender.statusEffects.trance.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.trance.potency*move.flatSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Paralysis") == True and move.scalesWithStatusScale == "Paralysis":
                            finalDamage += defender.statusEffects.paralysis.potency*move.flatSFFlatScaling
                            finalDamage += move.power*((defender.statusEffects.paralysis.potency*move.flatSFPercentScaling)*0.01+1)



                    fetishMod = 1
                    for each in move.fetishTags:
                        for fetishE in theTarget.FetishList:
                            checkTag = each
                            if checkTag == "Penetration":
                                for stanceChek in theTarget.combatStance:
                                    if stanceChek.Stance == "Sex":
                                        checkTag = "Sex"
                                    elif stanceChek.Stance == "Anal":
                                        checkTag = "Ass"
                            if checkTag == fetishE.name:
                                fetishMod += (fetishE.Level)*0.01

                    #status effect bonuses
                    #if (theTarget.statusEffects.charmed.duration > 0):
                    #    finalDamage *= 1.20

                    finalDamage*=damageMod

                    for each in attacker.statusEffects.tempAtk:
                        if each.duration > 0:
                            finalDamage *= (each.potency*0.01) + 1

                    for each in theTarget.statusEffects.tempDefence:
                        if each.duration > 0:
                            finalDamage *= 1 - (each.potency*0.01)



                    #weak or resistant
                    effectiveText = ""
                    rescount = 0
                    resTotal = 0
                    if move.skillTags[0] != "":
                        for each in move.skillTags:
                            checkTag = each
                            if checkTag == "Penetration":
                                for stanceChek in theTarget.combatStance:
                                    if stanceChek.Stance == "Sex":
                                        checkTag = "Sex"
                                    elif stanceChek.Stance == "Anal":
                                        checkTag = "Ass"
                            if theTarget.BodySensitivity.getRes(checkTag) != -999:
                                resTotal +=  theTarget.BodySensitivity.getRes(checkTag)
                                rescount += 1

                        if rescount >= 1:
                            resTotal /= rescount

                            finalDamage *= resTotal*0.01
                    else:
                        resTotal = 100

                    resTotal = resTotal*0.01

                    effectivenessTotal = resTotal + fetishMod - 1

                    if effectivenessTotal >= 1.25:
                        effectiveText = "{color=#ff587d}Weakspot!{/color} "
                        if theTarget.species != "Player":
                            try:
                                attacker.addLearnedWeakness(move)
                            except:
                                pass
                    elif effectivenessTotal <= 0.75:
                        effectiveText = "{color=#535F98}Frigid!{/color} "


                    finalDamage *= getTotalBoost(attacker, move)

                    if fetishMod <= 0:
                        fetishMod = 1


                    finalDamage*= fetishMod



                    critMod = 0
                    critRedMod = 0
                    critDamage = 2

                    try:
                        move.critChance
                    except:
                        move.critChance = 0
                    try:
                        move.critDamage
                    except:
                        move.critDamage = 0
                    critChance = getCritChance(attacker) + move.critChance
                    critDamage = getCritDamage(attacker) + move.critDamage*0.01

                    for perk in theTarget.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "CritChanceBoostSelf":
                                critMod += perk.EffectPower[p]
                            p += 1
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "CritDamageBoostSelf":
                                critDamage += perk.EffectPower[p]*0.01
                            p += 1


                    critChance -=  getCritReduction(theTarget)

                    critRoll = renpy.random.randint(0,100)

                    if critChance >= critRoll:
                        finalDamage *= critDamage
                        Crit = 1
                        critText = "{color=#ff587d}Passionate!{/color} "
                    #elif critChance + getCritReduction(theTarget) >= critRoll:
                    #    critText = "{color=#535F98}Passion Endured!{/color} "



                    #willDefence = 1.0
                    #willDefence = (155+theTarget.stats.Willpower)
                    #finalDamage *= 155.0/willDefence

                    finalDamage = getDamageReduction(theTarget, finalDamage)

                    finalDamage *= (renpy.random.randint(move.minRange, move.maxRange)*0.01) #random modifyer to damage

                    if (theTarget.statusEffects.defend.duration > 0):
                        if theTarget.statusEffects.defend.potency == 0:
                            finalDamage *= 0.25
                        elif theTarget.statusEffects.defend.potency == 1:
                            finalDamage *= 0.50
                        else:
                            finalDamage *= 0.75

                    if move.scalesWithStatusScale != "":
                        if defender.statusEffects.hasThisStatusEffect("Defend") == True and move.scalesWithStatusScale == "Defend":
                            finalDamage = finalDamage*((1*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Stun") == True and move.scalesWithStatusScale == "Stun":
                            finalDamage = finalDamage*((1*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Charm") == True and move.scalesWithStatusScale == "Charm":
                            finalDamage = finalDamage*((1*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Restrain") == True and move.scalesWithStatusScale == "Restrain":
                            finalDamage = finalDamage*((1*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Aphrodisiac") == True and move.scalesWithStatusScale == "Aphrodisiac":
                            finalDamage = finalDamage*((defender.statusEffects.aphrodisiac.potency*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffectPotency("Sleep", 0) == True and move.scalesWithStatusScale == "Sleep":
                            finalDamage = finalDamage*((defender.statusEffects.sleep.potency*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Trance") == True and move.scalesWithStatusScale == "Trance":
                            finalDamage = finalDamage*((defender.statusEffects.trance.potency*move.totalSFPercentScaling)*0.01+1)
                        if defender.statusEffects.hasThisStatusEffect("Paralysis") == True and move.scalesWithStatusScale == "Paralysis":
                            finalDamage = finalDamage*((defender.statusEffects.paralysis.potency*move.totalSFPercentScaling)*0.01+1)

                    finalDamage = math.floor(finalDamage)
                    finalDamage = int(finalDamage)

                    if finalDamage <= 0:
                        finalDamage = 1


                    statusEffectiveText = ""
                    if skillChoice.statusChance > 0 and theTarget.species != "Player":
                        if (theTarget.statusEffects.restrained.duration > 0 ):
                            restrainedMod = 10
                        else:
                            restrainedMod = 0

                        if (theTarget.statusEffects.paralysis.duration > 0):
                            restrainedMod += theTarget.statusEffects.paralysis.potency*3

                        defenceMod = 0
                        if (theTarget.statusEffects.defend.duration > 0):
                            defenceMod += 25

                        relatedStat = attacker.stats.getStat(move.statType)
                        relatedReisitStat = theTarget.stats.getStat(move.statusResistedBy)


                        StanceAccuaracyMod = 0
                        EvadeDamageMod = 0
                        for each in theTarget.combatStance:
                            if each.Stance != "None":
                                StanceAccuaracyMod += 3
                            else:

                                for perk in theTarget.perks:
                                    p = 0
                                    while  p < len(perk.PerkType):
                                        if perk.PerkType[p] == "OutOfStanceEvade":
                                            EvadeDamageMod += perk.EffectPower[p]
                                        p += 1

                        fetishMod = 0
                        for each in move.fetishTags:
                            for fetishE in theTarget.FetishList:
                                checkTag = each
                                if checkTag == "Penetration":
                                    for stanceChek in theTarget.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            checkTag = "Sex"
                                        elif stanceChek.Stance == "Anal":
                                            checkTag = "Ass"
                                if checkTag == fetishE.name:
                                    fetishMod += fetishE.Level*0.1

                        if 100 <= getStatusEffectRes(theTarget, move, autoHits) - getStatusEffectAccuracy(attacker, move):
                            statusEffectiveText = "{b}{color=#535F98}Effect Immune!{/color}{/b}"
                        elif 0 < (theTarget.resistancesStatusEffects.getRes(move.statusEffect)):
                            statusEffectiveText = "{color=#535F98}Effect Resistant!{/color}"
                        elif 0 > (theTarget.resistancesStatusEffects.getRes(move.statusEffect)):
                            statusEffectiveText = "{color=#ff587d}Effect Weak!{/color}"


                    display = move.outcome + " " + "{i}{EffectiveText}{/i}" + "{i}{CritText}{/i}" + "{TargetName} is aroused by " + "{FinalDamage}!" + " {i}{StatusEffectiveText}{/i}"

                    if move.recoil > 0:
                        display += " " + "{AttackerName} is also aroused by " + str(recoil) +"!"

                else:
                    display = move.outcome
                    finalDamage = 0
                    critText = ""
                    stanceApply = "True"
                    recoil = 0
                    effectiveText = ""
                    statusEffectiveText = ""

                attacker.stats.BarMinMax()
                theTarget.stats.BarMinMax()
                return [finalDamage, display, critText, stanceApply, recoil, effectiveText, statusEffectiveText]
            else:
                #missed


                Hit = 0
                display = move.miss
                if recoil >= 0:
                    if move.requiresStance == "Any":
                        recoil = 0
                if recoil > 0:
                    display += " " + "{AttackerName} is aroused by " + str(recoil) +"!"
                statusEffectiveText = ""

                return [0, display, critText, stanceApply,recoil, effectiveText, statusEffectiveText]
            attacker.stats.BarMinMax()
            theTarget.stats.BarMinMax()
            return [0, display, critText, stanceApply, recoil]

        def applyPoison(afflicted):
            posionDamage = afflicted.statusEffects.aphrodisiac.potency
            posionAmp = 1
            global finalDamage
            for perk in afflicted.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "AphrodisiacAmp":
                        posionAmp += (perk.EffectPower[p])*0.01
                    p += 1
            posionDamage *= posionAmp

            finalDamage = int(math.floor(posionDamage * (renpy.random.randint(80, 120)*0.01)))
            afflicted.stats.hp += finalDamage
            return afflicted

        def applySleepy(afflicted):
            posionDamage = afflicted.statusEffects.sleep.potency
            posionAmp = 1
            global finalDamage
            for perk in afflicted.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "SleepAmp":
                        posionAmp += (perk.EffectPower[p])*0.01
                    p += 1
            posionDamage *= posionAmp

            finalDamage = int(math.floor(posionDamage))
            afflicted.stats.ep -= finalDamage
            return afflicted

        def statusCheck(attacker, theTarget, move, autoHits=0):
            statusEffectiveText = ""


            EffectRoll = renpy.random.randint(0,100)

            EffectChance = getStatusEffectChance(move.statusChance, attacker, theTarget, move, autoHits)


            stanceApply = "False"

            display = ""
            if( EffectRoll < EffectChance):
                #apply status effects
                stanceApply = "True"
                effect = move
                theTarget = statusAfflict(theTarget, move, attacker)
                if 0 > (theTarget.resistancesStatusEffects.getRes(move.statusEffect))  and theTarget.species != "Player":
                    statusEffectiveText = "{color=#ff587d}Effect Weak!{/color}"
                if statusEffectiveText != "" and effect.statusOutcome[0] != "|"  and move.skillType != "attack":
                    display += effect.statusOutcome  + "\n{i}{StatusEffectiveText}{/i}"
                else:
                    display += effect.statusOutcome

                if move.statusEffect == "Sleep":
                    if theTarget.statusEffects.sleep.potency == -99:
                        display += " " + theTarget.name + " has fallen asleep!"
            else:
                effect =  move

                if theTarget.resistancesStatusEffects.getRes(move.statusEffect) != -999 and theTarget.species != "Player":
                    if 100 <= getStatusEffectRes(theTarget, move, autoHits) - getStatusEffectAccuracy(attacker, move):
                        statusEffectiveText = "{b}{color=#535F98}Effect Immune!{/color}{/b}"
                    elif 0 < (theTarget.resistancesStatusEffects.getRes(move.statusEffect)):
                        statusEffectiveText = "{color=#535F98}Effect Resistant!{/color}"


                if effect.statusMiss != "":
                    if statusEffectiveText != "" and effect.statusOutcome[0] != "|":
                        display += effect.statusMiss  + "\n{i}{StatusEffectiveText}{/i}"
                    else:
                        display += effect.statusMiss
                else:
                    display = "Skip"
            #display = "EffectChance: " + str(EffectChance) + " EffectRoll: "  +  str(EffectRoll) + " Monster res: " + str(theTarget.resistancesStatusEffects.getRes(move.statusEffect))
            return [theTarget, display, stanceApply, statusEffectiveText]

        def statusBuff(user, attacker, move, autoHits= 0): #user is the target, attacker is the one using the ability.
            statusEffectiveText = ""
            passes = 0
            canGetBuff = 1
            display = ""
            surrenderMod = 0
            StanceAccuaracyMod = 0
            EvadeDamageMod = 0

            applier = attacker



            if move.statusPotency >= 0 and move.statusEffect != "Escape" and move.statusEffect != "TargetStances":
                passes = 1
                applier = user

            else:
                defend = user
                attk = attacker
                if move.statusEffect != "Escape" and move.statusEffect != "TargetStances":
                    defend = attacker
                    attk = user


                EffectRoll = renpy.random.randint(0,100)
                EffectChance = getStatusEffectChance(move.statusChance, attacker, user, move, autoHits)

                #for each in move.skillTags:
                #    checkTag = each
                #    if checkTag == "Penetration":
                #        for stanceChek in defend.combatStance:
                #            if stanceChek.Stance == "Sex":
                #                checkTag = "Sex"
                #            elif stanceChek.Stance == "Anal":
                #                checkTag = "Ass"
                #    if defend.BodySensitivity.getRes(checkTag) != -999:
                #        EffectChance *= defend.BodySensitivity.getRes(checkTag)*0.01

                if(EffectRoll < EffectChance):
                    passes = 1


            if passes == 1:

                if move.statusEffect == "Escape":
                    global justEscapedStance
                    if user.statusEffects.restrained.duration > 0:
                        CheckImmunity = getFromName("Restraint Immune", user.perks)
                        if CheckImmunity == -1:
                            user.giveOrTakePerk("Restraint Immune", 1)
                        else:
                            user.giveOrTakePerk("Restraint Immune", -1)
                            user.giveOrTakePerk("Restraint Immune", 1)

                        user.statusEffects.restrained.duration = 0
                        user.restraintStruggle = [""]
                        user.restraintStruggleCharmed = [""]
                        user.restraintEscaped = [""]
                        user.restraintEscapedFail = [""]
                        user.restraintOnLoss = [""]

                        justEscapedStance = 2


                    if user.species != "Player":
                        user.putInRestrain = 1
                    else:
                        if user.combatStance[0].Stance != "None":
                            justEscapedStance = 2
                            user.clearStance()
                            for each in monsterEncounter:
                                each.clearStance()


                if move.statusEffect == "TargetStances":
                    global justEscapedStance


                    if user.species == "Player":
                        for each in attacker.combatStance:
                            if each.Stance != "None":
                                justEscapedStance = 2
                                user.removeStanceByName(each.Stance)
                        attacker.clearStance()
                    else:
                        for each in user.combatStance:
                            attacker.removeStanceByName(each.Stance)
                        user.clearStance()

                try:
                    scaling = move.statusEffectScaling*0.01
                except:
                    scaling = 1

                flipper = 1
                if move.statusPotency < 0:
                    flipper = -1

                if move.statusEffect == "Damage":
                    relatedStat = applier.stats.getStat(move.statType)
                    canGetBuff = 1
                    for each in user.statusEffects.tempAtk:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        user.statusEffects.tempAtk.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), move.statusPotency + (relatedStat*scaling)*flipper, move.statusText))
                elif move.statusEffect == "Defence":
                    relatedStat = applier.stats.getStat(move.statType)
                    canGetBuff = 1
                    for each in user.statusEffects.tempDefence:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        user.statusEffects.tempDefence.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), move.statusPotency + (relatedStat*scaling)*flipper, move.statusText))
                elif move.statusEffect == "Crit":
                    relatedStat = applier.stats.getStat(move.statType)
                    canGetBuff = 1
                    for each in user.statusEffects.tempCrit:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        user.statusEffects.tempCrit.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), move.statusPotency + (relatedStat*scaling)*flipper, move.statusText))
                elif move.statusEffect == "Power" or move.statusEffect == "%Power":
                    canGetBuff = 1
                    for each in user.statusEffects.tempPower:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Power*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)

                        user.statusEffects.tempPower.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Power += potentChange
                elif move.statusEffect == "Technique"  or move.statusEffect == "%Technique":
                    canGetBuff = 1
                    for each in user.statusEffects.tempTech:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Tech*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)
                        user.statusEffects.tempTech.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Tech += potentChange
                elif move.statusEffect == "Intelligence" or move.statusEffect == "%Intelligence":
                    canGetBuff = 1
                    for each in user.statusEffects.tempInt:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Int*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)
                        user.statusEffects.tempInt.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Int += potentChange
                elif move.statusEffect == "Willpower" or move.statusEffect == "%Willpower":
                    canGetBuff = 1
                    for each in user.statusEffects.tempWillpower:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Willpower*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)

                        user.statusEffects.tempWillpower.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Willpower += potentChange
                elif move.statusEffect == "Allure" or move.statusEffect == "%Allure":
                    canGetBuff = 1
                    for each in user.statusEffects.tempAllure:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Allure*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)

                        user.statusEffects.tempAllure.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Allure += potentChange
                elif move.statusEffect == "Luck" or move.statusEffect == "%Luck":
                    canGetBuff = 1
                    for each in user.statusEffects.tempLuck:
                        if each.skillText == move.statusText:
                            each.duration = statusEffectDuration(move.statusDuration, applier)
                            canGetBuff = 0
                    if canGetBuff == 1:
                        relatedStat = applier.stats.getStat(move.statType)
                        potentChange = move.statusPotency + (relatedStat*scaling)*flipper
                        if move.statusEffect[0] == "%":
                            potentChange = applier.stats.Luck*(potentChange*0.01)
                        potentChange = math.floor(potentChange)
                        potentChange = int(potentChange)

                        user.statusEffects.tempLuck.append(StatusEffect(statusEffectDuration(move.statusDuration, applier), potentChange, move.statusText))
                        user.stats.Luck += potentChange

            if passes == 1:
                if 0 > (user.resistancesStatusEffects.getRes(move.statusEffect)) and move.statusPotency < 0 and move.skillType != "attack" and user.species != "Player":
                    statusEffectiveText = "{color=#ff587d}Effect Weak!{/color}"
                if statusEffectiveText != "" and move.statusOutcome[0] != "|":
                    display = move.statusOutcome  + "\n{i}{StatusEffectiveText}{/i}"
                else:
                    display = move.statusOutcome
                stanceGo = "True"
                #if canGetBuff == 0:
                    #if move.statusPotency > 0:
                        #display = user.name + " uses " + move.name +  ", but " + user.name +  " already has that buff!"
                    #else:
                        #display = attacker.name + " uses " + move.name +  ", but " + user.name +  " already has that debuff!"
            else:
                if move.statusMiss != "":

                    if attk.resistancesStatusEffects.getRes(move.statusEffect) != -999 and user.species != "Player":
                        if 100 <= getStatusEffectRes(user, move, autoHits) - getStatusEffectAccuracy(attacker, move):
                            statusEffectiveText = "{b}{color=#535F98}Effect Immune!{/color}{/b}"
                        elif 0 < (user.resistancesStatusEffects.getRes(move.statusEffect)):
                            statusEffectiveText = "{color=#535F98}Effect Resistant!{/color}"

                    if statusEffectiveText != "" and move.statusOutcome[0] != "|":
                        display = move.statusMiss  + "\n{i}{StatusEffectiveText}{/i}"
                    else:
                        display = move.statusMiss
                else:
                    display = "Skip"
                stanceGo = "False"


            return [user, display, attacker, stanceGo, statusEffectiveText]

        def statusAfflict(theTarget, move, attacker=Monster(Stats(), 0, "FAKEtARGET")):
            try:
                scaling = move.statusEffectScaling*0.01
            except:
                scaling = 1
            relatedStat = attacker.stats.getStat(move.statType)

            if move.statusEffect == "Charm":
                if theTarget.statusEffects.charmed.duration >= -1:
                    theTarget.statusEffects.charmed.duration = statusEffectDuration(move.statusDuration, attacker)
                    theTarget.statusEffects.charmed.potency = 1
            if move.statusEffect == "Stun":
                if theTarget.statusEffects.stunned.duration >= -1 and theTarget.statusEffects.stunned.duration < 1:
                    theTarget.statusEffects.stunned.duration = statusEffectDuration(move.statusDuration, attacker)
                    theTarget.statusEffects.stunned.potency = 1
            if move.statusEffect == "Aphrodisiac":
                if theTarget.statusEffects.aphrodisiac.duration < 0:
                    theTarget.statusEffects.aphrodisiac.duration = 0
                theTarget.statusEffects.aphrodisiac.duration += statusEffectDuration(move.statusDuration, attacker)
                theTarget.statusEffects.aphrodisiac.potency += move.statusPotency
                theTarget.statusEffects.aphrodisiac.skillText = move.statusText

            if move.statusEffect == "Restrain":
                restraintBoost = 1.0
                for perk in theTarget.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "RestraintBoost":
                            restraintBoost += perk.EffectPower[p]*0.01
                        p += 1
                theTarget.statusEffects.restrained.duration = (statusEffectDuration(move.statusPotency, attacker, 1) + (relatedStat*scaling))*restraintBoost
                theTarget.statusEffects.restrained.potency = 1
                theTarget.statusEffects.restrained.skillText = move.statusText
                if theTarget.species != "Player":
                    theTarget.putInRestrain = 1
                else:
                    cmenu_resetMenu()

                theTarget.restraintStruggle = []
                theTarget.restraintStruggleCharmed = []
                theTarget.restraintEscaped = []
                theTarget.restraintEscapedFail = []
                theTarget.restraintOnLoss = []

                theTarget.restraintStruggle = move.restraintStruggle
                theTarget.restraintStruggleCharmed = move.restraintStruggleCharmed
                theTarget.restraintEscaped = move.restraintEscaped
                theTarget.restraintEscapedFail = move.restraintEscapedFail
                try:
                    move.restraintOnLoss
                except:
                    move.restraintOnLoss = [""]
                theTarget.restraintOnLoss = move.restraintOnLoss

                if attacker != "FAKEtARGET":
                    theTarget.restrainer = attacker

            if move.statusEffect == "Sleep":
                if theTarget.statusEffects.sleep.duration == 0 or theTarget.statusEffects.sleep.duration == -1:
                    theTarget.statusEffects.sleep.duration = statusEffectDuration(move.statusDuration, attacker) + (relatedStat*scaling)
                if theTarget.statusEffects.sleep.potency != -99:
                    theTarget.statusEffects.sleep.potency += move.statusPotency

            if move.statusEffect == "Trance":
                if theTarget.statusEffects.trance.duration == 0:
                    theTarget.statusEffects.trance.duration = 1
                    theTarget.statusEffects.trance.potency = 1
                    for perk in theTarget.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "StartDeeperInTrance":
                                theTarget.statusEffects.trance.potency += perk.EffectPower[p]
                            p += 1
                    if move.statusPotency > 1:
                        theTarget.statusEffects.trance.potency += move.statusPotency-1
                else:
                    accumulatedTrance = 1
                    for perk in theTarget.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "StartDeeperInTrance":
                                if theTarget.statusEffects.trance.potency < perk.EffectPower[p] + accumulatedTrance:
                                    accumulatedTrance += perk.EffectPower[p]
                            p += 1
                    if accumulatedTrance > 1:
                        theTarget.statusEffects.trance.potency = accumulatedTrance
                    else:
                        theTarget.statusEffects.trance.potency += move.statusPotency
            if move.statusEffect == "Paralysis":
                if theTarget.statusEffects.paralysis.duration != 1:
                    theTarget.statusEffects.paralysis.duration = 1
                theTarget.statusEffects.paralysis.potency += move.statusPotency
                if theTarget.statusEffects.paralysis.potency >= 10:
                    theTarget.statusEffects.paralysis.potency = 10

            return theTarget

        def getHealingEstimate(healer, move):
            finalDamage = move.power

            #if(move.skillType == "HealingEP"):
            #    finalDamage *= ((attacker.stats.max_true_ep-50)*0.01)*scaling + 1
            try:
                scaling = skill.statusEffectScaling*0.01
            except:
                scaling = 1

            if move.statType == "PercentMaxEnergy":
                finalDamage = healer.stats.max_true_ep*(finalDamage*0.01)

            elif move.statType == "PercentMaxArousal":
                finalDamage = healer.stats.max_true_hp*(finalDamage*0.01)

            elif move.statType == "Max Arousal":
                finalDamage += ((healer.stats.max_true_hp-100)*0.1)*scaling
                finalDamage *= ((healer.stats.max_true_hp-100)*0.001)*scaling + 1
            elif move.statType != "None":
                relatedStat = healer.stats.getStat(move.statType)*scaling
                finalDamage += int(relatedStat)



            finalDamage = math.floor(finalDamage)
            finalDamage = int(finalDamage)

            return finalDamage


        def HealCalc(attacker, move):
            global itemChoice
            healingArousal = 0
            healingEnergy = 0
            healingSpirit = 0
            ExpGained = 0



            try:
                scaling = move.statusEffectScaling*0.01
            except:
                scaling = 1

            if move.outcome != "":
                display = move.outcome
            elif move.isSkill != "True":
                display = itemChoice.useOutcome
            else:
                display = ""

            if(move.skillType != "StatusHeal"):
                Hit = 1
                finalDamage = getHealingEstimate(player, move)
                finalDamage *= (renpy.random.randint(move.minRange, move.maxRange)*0.01) #random modifyer to damage
                finalDamage = math.floor(finalDamage)
                finalDamage = int(finalDamage)

                if move.isSkill != "True":
                    if itemChoice.hp != 0:
                        healingArousal += itemChoice.hp
                    if itemChoice.ep != 0:
                        healingEnergy += itemChoice.ep
                    if itemChoice.sp != 0:
                        healingSpirit += itemChoice.sp
                    if itemChoice.Exp != 0:
                        ExpGained += itemChoice.Exp

                if(move.skillType == "Healing"):
                    healingArousal += finalDamage
                if(move.skillType == "HealingEP"):
                    healingEnergy += finalDamage
                if(move.skillType == "HealingSP"):
                    healingSpirit += finalDamage

            if(healingArousal != 0):
                attacker.stats.hp -= healingArousal
                if healingArousal > 0:
                    display += " Arousal lowered by " + str(healingArousal) + "! "
                else:
                    display += " Arousal increased by " + str(healingArousal) + "! "
            if(healingEnergy != 0):
                attacker.stats.ep += healingEnergy
                if healingEnergy > 0:
                    display += " Recovered " + str(healingEnergy) + " energy! "
                else:
                    display += " Lost " + str(healingEnergy) + " energy! "
            if(healingSpirit != 0):
                attacker.stats.sp += healingSpirit
                if healingSpirit > 0:
                    display += " Recovered " + str(healingSpirit) + " spirit! "
                else:
                    display += " Lost " + str(healingSpirit) + " spirit! "
            if(ExpGained != 0):
                attacker.stats.Exp += ExpGained
                if healingSpirit > 0:
                    display += " Gained " + str(ExpGained) + " exp! "
                else:
                    display += " Lost " + str(ExpGained) + " exp! "
            if move.skillType == "Afflict":
                attacker = statusAfflict(attacker, move)
            else:
                if move.statusEffect != "None"  or (move.isSkill != "True" and itemChoice.statusEffect != "None") :
                    if move.statusEffect == "All" or (move.isSkill != "True" and itemChoice.statusEffect == "All"):
                        attacker = attacker.statusEffects.refreshNegative(attacker)
                        display += "You are no longer afflicted by any negative status effects!"
                    if move.statusEffect == "Aphrodisiac" or (move.isSkill != "True" and itemChoice.statusEffect == "Aphrodisiac"):
                        if attacker.statusEffects.aphrodisiac.duration > 0:
                            attacker.statusEffects.aphrodisiac.duration = -1
                            attacker.statusEffects.aphrodisiac.potency = 0
                            display += "You are no longer afflicted by an aphrodisiac!"
                        elif move.isSkill != "True":
                            display += "You feel exactly the same as before. You may have wasted that."
                    if move.statusEffect == "Charm"  or (move.isSkill != "True" and itemChoice.statusEffect == "Charm"):
                        if attacker.statusEffects.charmed.duration > 0:
                            CheckImmunity = getFromName("Charm Immune", attacker.perks)
                            if CheckImmunity == -1:
                                attacker.giveOrTakePerk("Charm Immune", 1)
                            else:
                                attacker.giveOrTakePerk("Charm Immune", -1)
                                attacker.giveOrTakePerk("Charm Immune", 1)
                            attacker.statusEffects.charmed.duration = -1
                            display += "You are no longer charmed!"
                        elif move.isSkill != "True":
                            display += "You feel exactly the same as before. You may have wasted that."
                    if move.statusEffect == "Sleep" or (move.isSkill != "True" and itemChoice.statusEffect == "Sleep"):
                        if attacker.statusEffects.sleep.duration > 0:
                            #CheckImmunity = getFromName("Sleep Immune", attacker.perks)
                            #if CheckImmunity == -1:
                            #    attacker.giveOrTakePerk("Sleep Immune", 1)
                            #else:
                            #    attacker.giveOrTakePerk("Sleep Immune", -1)
                            #    attacker.giveOrTakePerk("Sleep Immune", 1)
                            attacker.statusEffects.sleep.duration = 0
                            attacker.statusEffects.sleep.potency = 0
                            display += "You perk up, your drowsiness quickly washing away!"
                        elif move.isSkill != "True":
                            display += "You feel exactly the same as before. You may have wasted that."
                    if move.statusEffect == "Paralysis" or (move.isSkill != "True" and itemChoice.statusEffect == "Paralysis"):
                        if attacker.statusEffects.paralysis.duration > 0:
                            attacker.statusEffects.paralysis.duration = 0
                            attacker.statusEffects.paralysis.potency = 0
                            display += "You shiver a little, and the paralysis quickly fades away!"
                        elif move.isSkill != "True":
                            display += "You feel exactly the same as before. You may have wasted that."
                    if move.statusEffect == "Trance" or (move.isSkill != "True" and itemChoice.statusEffect == "Trance"):
                        if attacker.statusEffects.trance.duration > 0:
                            if move.isSkill != "True":
                                attacker.statusEffects.trance.potency -= itemChoice.statusPotency
                            else:
                                attacker.statusEffects.trance.potency -= move.statusPotency
                            if attacker.statusEffects.trance.potency <= 0:
                                attacker.statusEffects.trance.duration = 0
                                display += "You snap out of the hypnotic trance you were falling into!"
                            else:
                                display += "You start to come out of hypnotic trance!"
                        elif move.isSkill != "True":
                            display += "You feel exactly the same as before. You may have wasted that."


            attacker.stats.BarMinMax()
            return [attacker, display]


        def checkHPLosses(theTarget, lastAttacker, lastMove):
            if theTarget.stats.hp >= theTarget.stats.max_true_hp:
                return "Orgasm"
            else:
                return ""

        def checkSPLosses(theTarget, lastAttacker, lastMove):
            if theTarget.stats.sp <= 0:
                #loses text
                if(theTarget.stats.isPlayer == "True"):
                    return "Lost"#lastAttacker.lossScenes[0]
                else:
                    return "Lost"
            return ""




label exitCombatFunction:
