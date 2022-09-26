#this rpy handles all combat turn and action selection stuff, as well as any hard coded menu actions like running. It also has the spots used for winning and losing fights.
init python:
    def getInit(target):
        roll = getInitStats(target) + renpy.random.randint(0,100)

        if target.statusEffects.paralysis.duration >= 1:
            roll -= target.statusEffects.paralysis.potency*5

        return roll

    def getInitStats(target):
        roll = (target.stats.Tech  + (target.stats.Int)*0.5  + (target.stats.Luck)*0.5)
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "InitiativeBonus":
                    roll += perk.EffectPower[p]
                p += 1
        return int(math.floor(roll))

    def getParalysisBoost(char): #this thing is for figuring out if the player is stunned by paralysis, which occurs in this area
        global turnsStunnedByParalysis
        Paraboost = 0
        Parabase = char.statusEffects.paralysis.potency*char.statusEffects.paralysis.potency + 24
        if Parabase > 95:
            Parabase = 95
        ParaPerkboost = 0
        for perk in char.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "ParalysisAmp":
                    ParaPerkboost -= perk.EffectPower[p]
                p += 1

        Paraboost = Parabase - (char.stats.Power*0.25 + (char.stats.Willpower)*0.1 + (char.stats.Luck)*0.1 + turnsStunnedByParalysis*(10 + char.stats.Power*0.1)) - ParaPerkboost
        Paraboost = math.floor(Paraboost)
        Paraboost = int(Paraboost)
        if Paraboost < 0:
            Paraboost = 0
        return Paraboost

    def getSleepingStruggle(target):

        SleepAmp = 1
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "SleepAmp":
                    SleepAmp += (perk.EffectPower[p])*0.01
                p += 1

        target.statusEffects.sleep.duration -= (target.stats.Willpower*0.25 + (target.stats.Int)*0.1 + (target.stats.Luck)*0.1 + 2.25 )*SleepAmp

        return target.statusEffects.sleep.duration

    def getSleepingDuration(target):

        target.statusEffects.sleep.duration = target.statusEffects.sleep.duration*1.5 + 10
        target.statusEffects.sleep.duration += target.statusEffects.sleep.potency*0.5
        target.statusEffects.sleep.duration *= (renpy.random.randint(85, 125)*0.01)

        return target.statusEffects.sleep.duration

    def getRestrainStruggle(target, restraintEscapeBoost, charmMod, despMod):
        roll = ((3 + (despMod*9) + (target.stats.Power*(0.25+despMod) + target.stats.Tech*(0.1+(despMod*0.35)) + (target.stats.Luck*0.05))) * ((renpy.random.randint(90, 110)+restraintEscapeBoost)*0.01))*charmMod
        return roll

    def getStanceHoldRoll(target):
        stanceBoost = 1.0
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "StanceBoost":
                    stanceBoost += perk.EffectPower[p]*0.01

                p += 1
        roll = ((target.stats.Power*1.0 + target.stats.Tech*0.5)  * ((renpy.random.randint(90, 110))*0.01))*stanceBoost
        return roll

    def getStanceStruggleRoll(target):
        stanceStuck = 1.0
        stanceEscapeBoost = 1.0
        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "StanceStuck":
                    stanceStuck -= perk.EffectPower[p]*0.01

                if perk.PerkType[p] == "GetOutOfStance":
                    stanceEscapeBoost += perk.EffectPower[p]*0.01

                p += 1
        roll = (((target.stats.Power*0.5 + target.stats.Tech*0.25 + (target.stats.Luck*0.10))* stanceEscapeBoost)*stanceStuck)* ((renpy.random.randint(90, 110))*0.01)

        if roll == 0:
            roll = 1

        return roll

    def NumberMonsters(array):
        idBit = 0

        for each in array:
            idC = 0
            multipleOf = 2
            for compare in array:
                if idBit != idC:
                    if each.name == compare.name:
                        compare.name = compare.name + " " + str(multipleOf)
                        multipleOf +=1
                idC +=1
            if multipleOf > 2:
                each.name = each.name + " 1"

            idBit+=1
        return array

    def getUnviableSets(picked, player):#makes sure skill can actually be used with stances that have been added
        usability = 0
        try:
            for pick in picked.unusableIfTargetHasTheseSets:
                passesUsable = 0
                checked = []

                for unusableSet in pick:
                    s = 0
                    matchFound = 0
                    while s < len(player.combatStance):
                        ignoreThis = 0
                        for used in checked:
                            if used == s:
                                ignoreThis = 1
                        if StanceEquals(player.combatStance[s].Stance, unusableSet) and ignoreThis != 1 and matchFound != 1:
                            checked.append(s)
                            matchFound = 1
                        s+=1
                if len(checked) == len(pick):
                    return True
        except:
            setattr(picked, 'unusableIfTargetHasTheseSets', [])

        return False

    def getTheEndScene(Scenes, Monster, monsterEncounter, trueMonsterEncounter, lastAttack):
        chosenScene = -5
        scenesPool = []
        sceneNumbers  = []
        howFar = 0

        for each in Scenes:
            charsRequired = 0
            moveRequired = 0
            stanceRequired = 0
            foundMatch = 0
            inUse = []

            if len(each.includes) > 1:
                if len(monsterEncounter) > 1:
                    requirementsMet = 0
                    mc = 0
                    for monReq in each.includes:
                        mc = 0
                        foundMatch = 0
                        for monsAvalible in trueMonsterEncounter:
                            if monReq == monsAvalible.IDname and foundMatch == 0:
                                canUseMon = 1

                                if len(inUse) >= 1:
                                    for unusable in inUse:
                                        if unusable == mc:
                                            canUseMon = 0
                                if canUseMon == 1:
                                    howFar = 1
                                    requirementsMet += 1
                                    foundMatch = 1
                                    inUse.append(mc)
                            mc += 1
                    if requirementsMet == len(each.includes):
                        charsRequired = 1
            else:
                charsRequired = 1

            if each.move != "":
                if each.move == lastAttack.name:
                    moveRequired = 1
            else:
                moveRequired = 1

            if each.stance == "" or each.stance == "None":
                stanceRequired = 1
            else:
                for pStance in Monster.combatStance:
                    if pStance.Stance != "None":
                        if pStance.Stance == each.stance:

                            stanceRequired = 1

            if stanceRequired == 1 and moveRequired == 1 and charsRequired == 1:
                scenesPool.append(copy.deepcopy(each))
                sceneNumbers.append(copy.deepcopy(getFromNameOfScene(each.NameOfScene, Scenes)))


        largestScene = 0
        oneHasAMove = 0
        oneHasAStance = 0

        if len(scenesPool) == 1:
            chosenScene = sceneNumbers[0]

        if chosenScene == -5:
            for each in scenesPool:
                if largestScene < len(each.includes):
                    largestScene = len(each.includes)

            clearList = 0
            while clearList < len(scenesPool):
                if len(scenesPool[clearList].includes) < largestScene:

                    del scenesPool[clearList]
                    del sceneNumbers[clearList]
                    clearList -= 1
                clearList += 1

            if len(scenesPool) == 1:
                chosenScene = sceneNumbers[0]

        if chosenScene == -5:
            for each in scenesPool:
                if each.move != "":
                    oneHasAMove = 1
            clearList = 0
            if oneHasAMove == 1:
                while clearList < len(scenesPool):
                    if scenesPool[clearList].move == "":
                        del scenesPool[clearList]
                        del sceneNumbers[clearList]
                        clearList -= 1
                    clearList += 1

            if len(scenesPool) == 1:
                chosenScene = sceneNumbers[0]

        if chosenScene == -5:
            for each in scenesPool:
                if each.stance != "":
                    oneHasAStance = 1
            clearList = 0
            if oneHasAStance == 1:
                while clearList < len(scenesPool):
                    if scenesPool[clearList].stance == "":
                        del scenesPool[clearList]
                        del sceneNumbers[clearList]
                        clearList -= 1
                    clearList += 1

            if len(scenesPool) == 1:
                chosenScene = sceneNumbers[0]
        if chosenScene == -5:
            chosenScene = sceneNumbers[renpy.random.randint(0, len(scenesPool)-1)]
        return chosenScene

    def addMonsterTo(theName, addTo, inserted=-1):#technically used in dialogue system and adventuing, but this spot makes more sense I think
        global PerkDatabase
        dataTarget = getFromName(theName, MonsterDatabase)
        blankMon =  copy.deepcopy(MonsterDatabase[dataTarget])
        if IfTime("Night") == 1:
            blankMon.giveOrTakePerk("Moonlit Allure", 1)
        addTo.insert(inserted, copy.deepcopy(blankMon))



label combat:
    $ InventoryAvailable = False
    $ noDoubleRewards = 0
    $ DefeatedEncounterMonsters = []
    $ playerCloseMark = 0
    $ ExpPool = 0
    $ LootDrops = []
    $ MoneyDrops = 0
    $ RanAway = "False"
    $ justEscapedStance = 0
    $ tranceIgnored = 0
    $ paralysisIgnored = 0
    $ breakingFreeOfTrance = 0
    $ tt = Tooltip("") # make sure tooltip is blank when bringing up combat menu
    $ display = ""
    $ pushAwayAttempt = 0
    $ turnsStunnedByParalysis = 0
    $ refreshMenu = 1
    $ manualSort = 0
    $ swappingSkill = -1
    $ hidingCombatEncounter = 0
    $ increaseStatCheck = 0
    $ NoGameOver = 0
    $ victoryScene = 0
    $ timeNotify = 0
    $ skipPlayerOrgasm = 0
    $ skipMonsterOrgasm = 0
    $ skipTargetOrgasm = 0
    $ skipAttackOrgasm = 0
    $ m = 0
    $ monInititive = []
    $ itemChoice = Item("Blank", "Null", 0)
    while m < len(monsterEncounter):#who acts first
        $ monInititive.append(0)
        $ m += 1

    $ lastReturn = copy.deepcopy(renpy.get_return_stack())
    #"[lastReturn]"
    $ renpy.set_return_stack(copy.deepcopy(lastReturn))

    $ LostGameOver = 0

    if overrideCombatMusic == 0:
        $ BGMlist = []
        $ BGMlist.append("music/Battle/Comet_Highway.mp3")

    #window hide
    show screen ON_EnemyCardScreen (_layer="master")
    $ cmenu_resetMenu() # reset combat menu before showing ON_CombatMenu since it may have been viewed in the character menu
    #show screen ON_CombatMenu
    hide screen ON_HealthDisplayBacking
    hide screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking #(_layer="hplayer")
    show screen ON_HealthDisplay #(_layer="sayScreen")


    python:
        for each in monsterEncounter:
            each = initiateImageLayers(each)
            for SetData in persistantMonSetData:
                if SetData.name == each.IDname:
                    each.currentSet = getFromName(SetData.startingSet, each.ImageSets)
            each.stats.BarMinMax()

        player.stats.BarMinMax()



    python:
        for each in monsterEncounter[0].combatDialogue:
            specifyStance = 0
            if overrideCombatMusic == 0:
                if each.lineTrigger == "SetMusicTo":
                        bgm = each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                        BGMlist = []
                        BGMlist.append(bgm)
                        break


    if overrideCombatMusic == 0:
        if musicLastPlayed != BGMlist:
            $ musicLastPlayed = copy.deepcopy(BGMlist)
            $ renpy.random.shuffle(BGMlist)

            $ fromPos = 0
            if lastCombatSong == BGMlist[0]:
                if lastCombatSongPosition is None:
                    $ lastCombatSongPosition = ""
                elif lastCombatSongPosition != "":
                    $ fromPos = int(lastCombatSongPosition)

            if fromPos == 0:
                play music BGMlist[0] fadeout 1.0 fadein 1.0
            else:
                $ assembleBGMLine = "<from " + str(fromPos) + ">" + BGMlist[0]
                play music assembleBGMLine fadeout 1.0 fadein 1.0
                queue music BGMlist[0]
    $ lastCombatSongPosition = ""
    $ overrideCombatMusic = 0



    call TimeEvent(CardType="StartOfCombat", LoopedList=StartOfCombatList) from _call_TimeEvent_14


    $ mEA = 0
    while mEA < len(monsterEncounter):
        $ ar = 0
        $ foundLine = 0
        python:
            for each in monsterEncounter[mEA].combatDialogue:
                specifyStance = 0
                if each.lineTrigger == "MonsterArrived":
                    CombatFunctionEnemytarget = mEA
                    Speaker = Character(_(monsterEncounter[mEA].name))
                    display = each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                    foundLine = 1
                    break
        if foundLine == 1:
            call read from _call_read_39
        $ mEA+=1


    $ foundLine = 0
    python:
        for each in monsterEncounter[0].combatDialogue:
            specifyStance = 0
            if each.lineTrigger == "StartOfCombat":
                    CombatFunctionEnemytarget = 0
                    Speaker = Character(_(monsterEncounter[0].name))
                    display = each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                    foundLine = 1
                    break
    if foundLine == 1:
        call read from _call_read_48
    else:
        if len(monsterEncounter) == 1:
            if monsterEncounter[0].generic == "True":
                $ display = "You encounter a " + monsterEncounter[0].name + "!" #combat preamble if any?
            else:
                $ display = monsterEncounter[0].name + " approaches!" #combat preamble if any?
            "[display]"
        else:
            "Monster girls approach!"

    call TurnStart from _call_TurnStart
    jump combatPlayer

label combatPlayer:
    $ renpy.set_return_stack(lastReturn)
    $ index = 0
    $ stanceBreaking = 0
    $ target = -2
    $ targeting = 0

    $ skipAttack = 0
    hide kiss onlayer visualEffects
    hide displayVFX2 onlayer visualEffects
    stop sound fadeout 1.0
    stop soundChannel2 fadeout 1.0
    $ waiting = 0


    python:
        Rut = False
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "DisableRun":
                    Rut = True
                p += 1

    hide screen returnButton
    $ c = 0

    $ paralysisStunned = 0
    if player.statusEffects.paralysis.potency >= 1 and player.statusEffects.paralysis.duration >= 1 and paralysisIgnored == 0:

        if getParalysisBoost(player) >= renpy.random.randint(0, 100):
            $ paralysisStunned = 1
            $ turnsStunnedByParalysis += 1
        else:
            $ turnsStunnedByParalysis = 0
            $ paralysisIgnored = 1

            #$ display = player.name + " manages to struggle through the paralysis wracking his body, and is able to act!"
            #"[display]"
    else:
        $ turnsStunnedByParalysis = 0

    if (player.statusEffects.surrender.duration > 0):
        $ cmenu_resetMenu()
        $ player.statusEffects.surrender.duration += 2
        jump combatEnemies
    elif player.statusEffects.trance.potency >= 11 and tranceIgnored == 0:
        $ cmenu_resetMenu()

        $ hypnoTurnLoss = 0
        python:
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "TranceStunChance":
                        hypnoTurnLoss += perk.EffectPower[p]
                    p += 1

        if (60 + (player.statusEffects.trance.potency-11) - player.stats.Willpower - player.stats.Int*0.5 - (player.stats.Luck)*0.25 + hypnoTurnLoss >= renpy.random.randint(0, 100)):
            $ breakingFreeOfTrance = 0
            $ display = player.name + " is completely lost in blissful hypnotic trance..."
            "[display]"
            jump combatEnemies
        else:
            $ tranceIgnored = 1
            $ breakingFreeOfTrance += 1

            $ display = player.name + " manages to struggle through his hypnotic haze, and can focus on trying to fight!"

            python:
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "CantBreakFreeOfTranceWithoutItems":
                            breakingFreeOfTrance = 0
                        p += 1

            if breakingFreeOfTrance >= 3:
                $ player.statusEffects.trance.potency = 8
                $ display = player.name + " manages to start breaking free of the hypnotic trance!"
                $ breakingFreeOfTrance = 0

            "[display]"

    elif player.statusEffects.sleep.potency == -99:
        $ cmenu_resetMenu()
        $ display = player.name + " sleeps soundly, unaware of what's happening..."

        $ player.statusEffects.sleep.duration = getSleepingStruggle(player)
        if player.statusEffects.sleep.duration <= 0:
            $ display = "With a groan, " + player.name + " drowsily begins to wake up!"
            $ player.statusEffects.sleep.potency = 0

            #$ CheckImmunity = getFromName("Sleep Immune", player.perks)
            #if CheckImmunity == -1:
            #    $ player.giveOrTakePerk("Sleep Immune", 1)
            #else:
            #    $ player.giveOrTakePerk("Sleep Immune", -1)
            #    $ player.giveOrTakePerk("Sleep Immune", 1)
            $ player.statusEffects.sleep.duration = 0
            "[display]"
            jump combatPlayer
        "[display]"
        jump combatEnemies
    elif paralysisStunned >= 1:
        $ cmenu_resetMenu()
        $ display = player.name + "'s body is paralyzed and cannot move!"
        "[display]"
        jump combatEnemies

    elif(player.statusEffects.stunned.duration > 0):
        $ cmenu_resetMenu()
        $ display = player.name + " is stunned and cannot act!"
        "[display]"
        jump combatEnemies
    else:
        #while i < len(player.combatStance):
            #$ display = player.combatStance[i].Stance
            #"[display]"
        #$ cmenu_resetMenu() # reset combat menu before showing ON_CombatMenu since it may have been viewed in the character menu

        $ target = -1
        if refreshMenu == 1:
            $ cmenu_refreshMenu()
            $ refreshMenu = 0

        show screen ON_CombatMenu #(_layer="sayScreen")
        window hide
        pause

    #stay here till you pick something
    jump combatPlayer

label pushaway:
    $ combatChoice = copy.deepcopy(getSkill("Push Away", SkillsDatabase))

label targeting:
    if combatChoice.statusEffect == "Damage" or combatChoice.statusEffect == "Defence" or combatChoice.statusEffect == "Crit" or combatChoice.statusEffect == "Power" or combatChoice.statusEffect == "Technique" or combatChoice.statusEffect == "Intelligence" or combatChoice.statusEffect == "Willpower" or combatChoice.statusEffect == "Allure" or combatChoice.statusEffect == "Luck" or combatChoice.statusEffect == "%Power" or combatChoice.statusEffect == "%Technique" or combatChoice.statusEffect == "%Intelligence" or combatChoice.statusEffect == "%Willpower" or combatChoice.statusEffect == "%Allure" or combatChoice.statusEffect == "%Luck":
        if combatChoice.statusPotency > 0 and combatChoice.skillType == "statusEffect":
            $ target = 0
            $ targeting = 0
            jump combatEnemies

    if combatChoice.skillType == "Healing" or combatChoice.skillType == "HealingEP" or combatChoice.skillType == "HealingSP" or combatChoice.skillType == "StatusHeal":
            $ target = 0
            $ targeting = 0
            jump combatEnemies

    if len(monsterEncounter) == 1 or combatChoice.targetType == "all" or  combatChoice.targetType == "Escape":
        $ target = -1
        if stanceBreaking == 0:
            jump combatEnemies
        else:
            jump combatPushAway

    $ targeting = 1
    hide screen ON_CombatMenu
    show screen returnButton
    window hide
    pause
    #stay here till you pick something
    jump targeting

label combatEnemies:
    $ targeting = 0
    hide screen returnButton
    hide screen ON_CombatMenu
    window show
    show screen ON_CombatMenuTooltip (_layer="screens")
    jump combatDisplay

label enemySkillChoice(mSC):
    if mSC > len(monsterEncounter):
        jump combatEndTurn

    $ refinedSkillList = []
    $ movesWithPrio = {}
    $ knownMoves = []
    $ knownBadMoves = []

    if monsterEncounter[mSC].statusEffects.restrained.duration > 0:
        if postTurnStartSelection == 0:
            $ monSkillChoice.append( getSkill("Struggle ", SkillsDatabase))
        else:
            $ monSkillChoice[mSC] = getSkill("Struggle ", SkillsDatabase)
        return

    $ showSkill = 0
    python:
        currentEnemyChoosing = monsterEncounter[mSC]
        for eachSkillOption in monsterEncounter[mSC].skillList:
            if eachSkillOption.requiresStance == "Any":
                showSkill = 1
            else:
                if eachSkillOption.requiresStance == "Penetration":
                    for stanceChek in monsterEncounter[mSC].combatStance:
                        if stanceChek.Stance == "Sex":
                            showSkill = 1
                        elif stanceChek.Stance == "Anal":
                            showSkill = 1
                else:
                    for stanceChek in monsterEncounter[mSC].combatStance:
                        if stanceChek.Stance == eachSkillOption.requiresStance:
                            showSkill = 1

            if eachSkillOption.requiresStatusEffect != "" and eachSkillOption.requiresStatusEffect != "None":
                if player.statusEffects.hasThisStatusEffect(eachSkillOption.requiresStatusEffect) == False:
                    showSkill = 0

            if eachSkillOption.requiresStatusPotency > 0:
                if player.statusEffects.hasThisStatusEffectPotency(eachSkillOption.requiresStatusEffect, eachSkillOption.requiresStatusPotency) == False:
                    showSkill = 0

            if eachSkillOption.requiresStatusEffectSelf != "" and eachSkillOption.requiresStatusEffectSelf != "None":
                if monsterEncounter[mSC].statusEffects.hasThisStatusEffect(eachSkillOption.requiresStatusEffectSelf) == False:
                    showSkill = 0

            if eachSkillOption.requiresStatusPotencySelf > 0:
                if monsterEncounter[mSC].statusEffects.hasThisStatusEffectPotency(eachSkillOption.requiresStatusEffectSelf, eachSkillOption.requiresStatusPotencySelf) == False:
                    showSkill = 0

            reqMet = 0
            for eachReq in eachSkillOption.requiresPerk:
                if eachReq != "" and eachReq != "None":
                    for perk in player.perks:
                        if perk.name == eachReq:
                            reqMet += 1
                            break
                else:
                    reqMet += 1
            if reqMet != len(eachSkillOption.requiresPerk):
                showSkill = 0

            for eachReq in eachSkillOption.unusableIfPerk:
                if eachReq != "" and eachReq != "None":
                    for perk in player.perks:
                        if perk.name == eachReq:
                            showSkill = 0
                            break

            reqMet = 0
            if len (eachSkillOption.requiresOnePerk) == 0:
                reqMet = 1
            for eachReq in eachSkillOption.requiresOnePerk:
                if eachReq != "" and eachReq != "None":
                    for perk in player.perks:
                        if perk.name == eachReq:
                            reqMet += 1
                            break
            if reqMet == 0:
                showSkill = 0

            #self vers
            reqMet = 0
            for eachReq in eachSkillOption.requiresPerkSelf:
                if eachReq != "" and eachReq != "None":
                    for perk in monsterEncounter[mSC].perks:
                        if perk.name == eachReq:
                            reqMet += 1
                            break
                else:
                    reqMet += 1
            if reqMet != len(eachSkillOption.requiresPerkSelf):
                showSkill = 0

            for eachReq in eachSkillOption.unusableIfPerkSelf:
                if eachReq != "" and eachReq != "None":
                    for perk in monsterEncounter[mSC].perks:
                        if perk.name == eachReq:
                            showSkill = 0
                            break

            reqMet = 0
            if len (eachSkillOption.requiresOnePerkSelf) == 0:
                reqMet = 1
            for eachReq in eachSkillOption.requiresOnePerkSelf:
                if eachReq != "" and eachReq != "None":
                    for perk in monsterEncounter[mSC].perks:
                        if perk.name == eachReq:
                            reqMet += 1
                            break
            if reqMet == 0:
                showSkill = 0





            for skillStatus in eachSkillOption.unusableIfStatusEffect:
                if player.statusEffects.hasThisStatusEffect(skillStatus) == True:
                    showSkill = 0

            for skillStatus in eachSkillOption.unusableIfStatusEffectSelf:
                if monsterEncounter[mSC].statusEffects.hasThisStatusEffect(skillStatus) == True:
                    showSkill = 0

            for stanceChek in monsterEncounter[mSC].combatStance:
                for stances in eachSkillOption.startsStance:
                    if stanceChek.Stance == stances:
                        showSkill = 0


            if eachSkillOption.startsStance[0] != "":
                if justEscapedStance > 0:
                    showSkill = 0

            if eachSkillOption.statusEffect == "Restrain" or eachSkillOption.statusEffect == "EventRestrain":
                if player.statusEffects.restrained.duration >= 1 or getFromName("Restraint Immune", player.perks) != -1:
                    showSkill = 0

            if eachSkillOption.statusEffect == "Sleep":
                if eachSkillOption.skillType == "statusEffect" and getFromName("Sleep Immune", player.perks) != -1:
                    showSkill = 0

            if eachSkillOption.statusEffect == "Charm" and eachSkillOption.skillType == "statusEffect":
                if player.statusEffects.charmed.duration >= 1 or getFromName("Charm Immune", player.perks) != -1:
                    showSkill = 0

            if eachSkillOption.statusEffect == "Stun" and eachSkillOption.skillType == "statusEffect":
                if player.statusEffects.stunned.duration >= 1 or getFromName("Stun Immune", player.perks) != -1:
                    showSkill = 0


            if eachSkillOption.skillType == "statusEffect":
                if eachSkillOption.statusPotency < 0:
                    for each in player.statusEffects.tempAtk:
                        if (eachSkillOption.statusEffect == "Damage" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0

                    for each in player.statusEffects.tempDefence:
                        if (eachSkillOption.statusEffect == "Defence" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0

                    for each in player.statusEffects.tempCrit:
                        if (eachSkillOption.statusEffect == "Crit" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0

                    for each in player.statusEffects.tempPower:
                        if (eachSkillOption.statusEffect == "Power" or eachSkillOption.statusEffect == "%Power") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in player.statusEffects.tempTech:
                        if (eachSkillOption.statusEffect == "Technique" or eachSkillOption.statusEffect == "%Technique") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in player.statusEffects.tempInt:
                        if (eachSkillOption.statusEffect == "Intelligence" or eachSkillOption.statusEffect == "%Intelligence") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in player.statusEffects.tempWillpower:
                        if (eachSkillOption.statusEffect == "Willpower" or eachSkillOption.statusEffect == "%Willpower") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in player.statusEffects.tempAllure:
                        if (eachSkillOption.statusEffect == "Allure" or eachSkillOption.statusEffect == "%Allure") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in player.statusEffects.tempLuck:
                        if (eachSkillOption.statusEffect == "Luck" or eachSkillOption.statusEffect == "%Luck") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0

                elif eachSkillOption.statusPotency > 0:
                    for each in monsterEncounter[mSC].statusEffects.tempAtk:
                        if (eachSkillOption.statusEffect == "Damage" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0

                    for each in monsterEncounter[mSC].statusEffects.tempDefence:
                        if (eachSkillOption.statusEffect == "Defence" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempCrit:
                        if (eachSkillOption.statusEffect == "Crit" and eachSkillOption.statusText == each.skillText):
                            showSkill = 0

                    for each in monsterEncounter[mSC].statusEffects.tempPower:
                        if (eachSkillOption.statusEffect == "Power" or eachSkillOption.statusEffect == "%Power") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempTech:
                        if (eachSkillOption.statusEffect == "Technique" or eachSkillOption.statusEffect == "%Technique") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempInt:
                        if (eachSkillOption.statusEffect == "Intelligence" or eachSkillOption.statusEffect == "%Intelligence") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempWillpower:
                        if (eachSkillOption.statusEffect == "Willpower" or eachSkillOption.statusEffect == "%Willpower") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempAllure:
                        if (eachSkillOption.statusEffect == "Allure" or eachSkillOption.statusEffect == "%Allure") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0
                    for each in monsterEncounter[mSC].statusEffects.tempLuck:
                        if (eachSkillOption.statusEffect == "Luck" or eachSkillOption.statusEffect == "%Luck") and eachSkillOption.statusText == each.skillText:
                            showSkill = 0





            stanceCheckedList = []
            n = 0
            i = 0
            canGo = 0
            while i < len(eachSkillOption.requiresTargetStance):
                stanceFound = 0
                n = 0
                for each in player.combatStance:
                    if "Any" != eachSkillOption.requiresTargetStance[i]:
                        passSearch = 0
                        # StanceEquals has the penetration/sex/anal code
                        if StanceEquals(each.Stance, eachSkillOption.requiresTargetStance[i]) and stanceFound == 0:
                            passSearch = 1
                        if passSearch == 1:
                            viable = 1
                            for check in stanceCheckedList:
                                if check == n:
                                    viable = 0
                            if viable == 1:
                                canGo += 1
                                stanceFound = 1
                                stanceCheckedList.append(n)
                    else:
                        canGo += 1
                    n += 1
                i += 1


            if canGo < len(eachSkillOption.requiresTargetStance):
                showSkill = 0


            if showSkill == 1:
                prio = currentEnemyChoosing.getKnownMovePriority(eachSkillOption)
                if prio < 0 and ptceConfig.get("combatAI").get("enemiesLearnStrengths"):
                    knownBadMoves.append(eachSkillOption) 
                elif prio > 0 and ptceConfig.get("combatAI").get("enemiesLearnWeaknesses"):
                    movesWithPrio.update({eachSkillOption.name: prio})
                    knownMoves.append(eachSkillOption)
                    refinedSkillList.append(eachSkillOption)               
                else:
                    refinedSkillList.append(eachSkillOption)


    python:
        largestScene = 1
        for each in refinedSkillList:
            if largestScene < len(each.requiresTargetStance):
                largestScene = len(each.requiresTargetStance)

        if largestScene > 1:
            clearList = 0
            for each in refinedSkillList:
                if len(each.requiresTargetStance) < largestScene:
                    if renpy.random.randint(0,100) > 30: # prioritize multi stance skills
                        del refinedSkillList[clearList]

                clearList += 1


label enemySkillChoiceLoop:
    $ name = monsterEncounter[m].name



    $ canUseStance = 0
    if monsterEncounter[m].combatStance[0].Stance == "" or monsterEncounter[m].combatStance[0].Stance == "None":
        $ canUseStance = 1
    else:
        python:
            for skillChek in monsterEncounter[m].skillList:
                for stanceChek in  monsterEncounter[m].combatStance:
                    for stances in skillChek.startsStance:
                        if stanceChek.Stance == stances or stanceChek.Stance == skillChek.requiresStance:
                            canUseStance = 1
                    if skillChek.requiresStance == "Penetration":
                        canUseStance = 1
                        if stanceChek.Stance == "Sex":
                            for perk in monsterEncounter[m].perks:
                                p = 0
                                while  p < len(perk.PerkType):
                                    if perk.PerkType[p] == "SexAdverse":
                                        canUseStance = 0
                                    p += 1
                        elif stanceChek.Stance == "Anal":
                            for perk in monsterEncounter[m].perks:
                                p = 0
                                while  p < len(perk.PerkType):
                                    if perk.PerkType[p] == "AnalAdverse":
                                        canUseStance = 0
                                    p += 1
                    if stanceChek.Stance == "Making Out":
                        for perk in monsterEncounter[m].perks:
                            p = 0
                            while  p < len(perk.PerkType):
                                if perk.PerkType[p] == "KissingAdverse":
                                    canUseStance = 0
                                p += 1

    if canUseStance == 0 and monsterEncounter[m].statusEffects.charmed.duration <= 0 and monsterEncounter[m].statusEffects.sleep.potency != -99: #OH GOD I CANT DO ANYTHING IN THIS STANCE

        if monsterEncounter[m].statusEffects.restrained.duration > 0 or monsterEncounter[m].statusEffects.stunned.duration > 0:
            if postTurnStartSelection == 0:
                $ monSkillChoice.append( getSkill("Struggle ", SkillsDatabase))
            else:
                $ monSkillChoice[m] = getSkill("Struggle ", SkillsDatabase)
            return

        if monsterEncounter[m].putInStance == 0:
            if renpy.random.randint(0,100) > 10:
                label monStruggle:
                #AI struggles
                $ isSexStance = 0
                $ isAnalStance = 0
                $ isKissStance = 0
                python:
                    for stance in monsterEncounter[m].combatStance:
                        if stance.Stance == "Sex":
                            isSexStance = 1
                        if stance.Stance == "Anal":
                            isAnalStance = 1
                        if stance.Stance == "Making Out":
                            isKissStance = 1

                if isSexStance == 1:
                    "[name] tries to get your shaft out of her sex..."
                elif isAnalStance == 1:
                    "[name] tries to get your shaft out of her ass..."
                elif isKissStance == 1:
                    "[name] tries to break the deep kiss with you..."
                else:
                    "[name] tries to pull away from you..."


                $ stanceBroken = 0
                $ stanceHPTotal = 0
                $ stanceDamageTotal = getStanceStruggleRoll(monsterEncounter[m])
                python:
                    for stance in player.combatStance:
                        stanceHPTotal += stance.potency

                if player.statusEffects.sleep.potency == -99 or player.statusEffects.trance.potency >= 11 or player.statusEffects.stunned.duration > 0 or player.statusEffects.restrained.duration > 0:
                    $ enemyStruggle = 1000000000

                if stanceHPTotal <= stanceDamageTotal:
                    $ stanceBroken = 1
                else:
                    $ stanceDamageTotal/= len(player.combatStance)
                    python:
                        for stance in player.combatStance:
                            stance.potency -= stanceDamageTotal

                if  stanceBroken == 1:
                    if isSexStance == 1:
                        "And gets your cock out of her pussy!"
                    elif isAnalStance == 1:
                        "And gets your cock out of her rear!"
                    elif isKissStance == 1:
                        "And pulls away from the kiss!"
                    else:
                        "And pulls away!"

                    python:
                        for monStance in monsterEncounter[m].combatStance:
                            player.removeStanceByName(monStance.Stance)
                        monsterEncounter[m].clearStance()
                else:
                    if isSexStance == 1:
                        "But despite her best efforts you keep a firm hold on her hips, and continue to fuck her!"
                    elif isAnalStance == 1:
                        "But despite her best efforts you keep a firm hold on her hips, and your shaft in her rear!"
                    elif isKissStance == 1:
                        "But you keep your arms tightly wrapped around her and deepen the romantic kiss!"
                    else:
                        "But fails!"

                if postTurnStartSelection == 0:
                    $ monSkillChoice.append( getSkill(" ", SkillsDatabase))
                else:
                    $ monSkillChoice[m] = getSkill(" ", SkillsDatabase)
                return
        else:
            $ monsterEncounter[m].putInStance = 0
            if renpy.random.randint(0,100) > 40 or player.statusEffects.restrained.duration > 0:
                $ monSkillChoice.append(getSkill(" ", SkillsDatabase))
                if monsterEncounter[m].statusEffects.restrained.duration > 0 or monsterEncounter[m].statusEffects.stunned.duration > 0:
                    return
                elif monsterEncounter[m].statusEffects.sleep.potency != -99 :
                    $ display = monsterEncounter[m].name + " isn't sure what to do in this position!"#add varience depending which stance inturrupted u
                    "[display]"
                return

    if AIStruggle >= 250 or (len(refinedSkillList)-1 < 0) and len(knownBadMoves) <= 0 :
        if postTurnStartSelection == 0:
            $ monSkillChoice.append( getSkill(" ", SkillsDatabase))
        else:
            $ monSkillChoice[m] = getSkill(" ", SkillsDatabase)
        if monsterEncounter[m].statusEffects.restrained.duration > 0 or monsterEncounter[m].statusEffects.stunned.duration > 0:
            return
        elif player.statusEffects.sleep.potency != -99:
            if monsterEncounter[m].combatStance[0].Stance != "None":
                jump monStruggle
            else:
                "[name] isn't sure what to do, so she tries to pose provocatively."
        return

    $ AIStruggle +=1

    #$ monSkillChoice = Skill()

    # 40% Chance that the enemy will use a move, which it does not know effectiveness for.

    if len(movesWithPrio.keys()) > 0 and (renpy.random.randint(1, 10) > 4):
        $ picked = pickMoveWithPrio(movesWithPrio, knownMoves)
    elif len(refinedSkillList) > 0:
        $ picked = refinedSkillList[renpy.random.randint(0, len(refinedSkillList)) - 1]
    else:
        $ picked = knownBadMoves[renpy.random.randint(0, len(knownBadMoves)) - 1]



    python:
        noGo = 0

        for each in player.combatStance:
            for pick in picked.unusableIfTarget:
                #if pick == "Penetration":
                #    if each.Stance == "Sex":
                #        noGo += 1
                #    elif each.Stance == "Anal":
                #        noGo += 1
                #if each.Stance == pick:
                #    noGo += 1
                if StanceEquals(each.Stance, pick):
                    noGo += 1
                if each.Stance != "None" and pick == "Any":
                    noGo += 1

        isunusable = getUnviableSets(picked, player)
        if isunusable == True:
            noGo += 1


        canGo = 0



    python:
        for monStance in monsterEncounter[m].combatStance:
            if "Any" != picked.requiresStance:
                #if picked.requiresStance == "Penetration":
                #    if monStance.Stance == "Sex":
                #        canGo = 1
                #    elif monStance.Stance == "Anal":
                #        canGo = 1
                #if monStance.Stance == picked.requiresStance:
                #    canGo = 1
                if StanceEquals(monStance.Stance, picked.requiresStance):
                    canGo = 1
            else:
                canGo = 1

            for pick in picked.unusableIfStance:
                #if pick == "Penetration":
                #    if monStance.Stance == "Sex":
                #        noGo += 1
                #    elif monStance.Stance == "Anal":
                #        noGo += 1
                #if monStance.Stance == pick:
                #    noGo += 1
                if StanceEquals(monStance.Stance, pick):
                    noGo += 1

                if monStance.Stance != "None" and pick == "Any":
                    noGo += 1



        if canGo != 1:
            noGo +=1



    if noGo > 0:
        jump enemySkillChoiceLoop

    if player.statusEffects.restrained.duration != 0 and picked.statusEffect == "Restrain":
        jump enemySkillChoiceLoop

    if postTurnStartSelection == 0:
        $ monSkillChoice.append(picked)
    else:
        $ monSkillChoice[m] = picked



    return

label combatDisplay:

    $ TextToDisplay = []
    $ lastMonToGo = -1
    $ playerGone = 0
    $ postTurnStartSelection = 0
    $ m = 0

    $ monInititive = []
    $ playerInititive = getInit(player)

    python:
        try:
            combatChoice.initiative
        except:
            combatChoice.initiative = 0

    $ playerInititive +=  combatChoice.initiative
    if(combatChoice.skillType == "Healing" or combatChoice.skillType == "HealingEP" or combatChoice.skillType == "HealingSP" or combatChoice.skillType == "StatusHeal"):
        $ playerInititive += 75

    if(combatChoice.name == "Run Away"):
        $ playerInititive += 200


    $ holdStance = copy.deepcopy(player.combatStance)
    $ holdPlayerStatus = copy.deepcopy(player.statusEffects)
    $ holdRestrain = copy.deepcopy(player.statusEffects.restrained.duration)
    $ holdStunned = copy.deepcopy(player.statusEffects.stunned.duration)

    $ monSkillChoice = []
    while m < len(monsterEncounter):#who acts first
        $ AIStruggle = 0

        call enemySkillChoice(mSC=m) from _call_enemySkillChoice_2
        $ monInititive.append(getInit(monsterEncounter[m]) + monSkillChoice[m].initiative)
        $ m += 1

    $ postTurnStartSelection = 1

    while playerGone == 0 or lastMonToGo < 0:#who acts first
        $ m = 0
        if lastMonToGo < 0:
            python:
                try:
                    playerCheck = max(monInititive)
                except:
                    playerCheck = 150
        else:
            $ playerCheck = -9999
        if playerInititive >= playerCheck and playerGone == 0:
            if target != -2:
                if combatChoice.isSkill != "True":
                    $ nameExtra = itemChoice.name
                else:
                    $ nameExtra = combatChoice.name

                $ Speaker = Character(_(player.name + " - " + nameExtra))

                $ attacker = player
                if target < len(monsterEncounter):
                    $ defender = monsterEncounter[target]
                    $ skillChoice = combatChoice
                    $ CombatFunctionEnemytarget = target
                    $ CombatFunctionEnemyInitial = target
                    call combatActionTurn from _call_combatActionTurn
                else:
                    $ display = attacker.name + "'s plans were interrupted!"#add varience depending which stance inturrupted u
                    "[display]"
            $ playerGone = 1
            if len(monsterEncounter) == 0: #combat is over
                jump combatWin
        else:
            if m > len(monsterEncounter):
                $ AIStruggle = 0
                jump combatEndTurn

            while m < len(monsterEncounter):
                if monInititive[m] == max(monInititive):
                    if monsterEncounter[m].skippingAttack == 0 and monInititive[m] != -999:

                        $ AIStruggle = 0
                        $ pickNewSkill = 0

                        $ currentEnemy = m
                        $ CombatFunctionEnemytarget = currentEnemy
                        $ CombatFunctionEnemyInitial = currentEnemy

                        if monsterEncounter[m].statusEffects.restrained.duration > 0 and (monsterEncounter[m].statusEffects.stunned.duration <= 0 and monsterEncounter[m].statusEffects.sleep.potency != -99):
                            $ pickNewSkill = -1
                            $ attackerName = monsterEncounter[m].restrainer.name
                            $ attackerHeOrShe = getHeOrShe(monsterEncounter[m].restrainer)
                            $ attackerHisOrHer = getHisOrHer(monsterEncounter[m].restrainer)
                            $ attackerHimOrHer = getHimOrHer(monsterEncounter[m].restrainer)
                            $ attackerYouOrMonsterName = getYouOrMonsterName(monsterEncounter[m].restrainer)
                            $ targetName = monsterEncounter[m].name
                            $ targetHeOrShe = getHeOrShe(monsterEncounter[m])
                            $ targetHisOrHer = getHisOrHer(monsterEncounter[m])
                            $ targetHimOrHer = getHimOrHer(monsterEncounter[m])
                            $ targetYouOrMonsterName = getYouOrMonsterName(monsterEncounter[m])
                            $ Speaker = Character(_(''))
                            call combatStruggleActivate(monsterEncounter[m]) from _call_combatStruggleActivate_1
                            if UnshackledFreedom == 1 and monsterEncounter[m].statusEffects.restrained.duration <= 0:
                                $ pickNewSkill = 1
                        else:
                            if len(holdStance) != len(player.combatStance):
                                $ pickNewSkill = 1
                            else:
                                $ cS = 0
                                while cS < len(player.combatStance):
                                    if player.combatStance[cS].Stance != holdStance[cS].Stance:
                                        $ pickNewSkill = 1
                                    $ cS+=1
                        if pickNewSkill == 1 or player.statusEffects != holdPlayerStatus:
                            if pickNewSkill != -1 and monSkillChoice[m].name != "Struggle " and monSkillChoice[m].name != " ":
                                $ pickNewSkill = 1
                                call enemySkillChoice(mSC=m) from _call_enemySkillChoice

                        $ skillcheck = monSkillChoice[m]
                        if player.statusEffects.sleep.potency != -99:
                            $ Speaker = Character(_(monsterEncounter[m].name + " - " + monSkillChoice[m].name))
                        else:
                            $ Speaker = Character(_(monsterEncounter[m].name))


                        $ attacker = monsterEncounter[currentEnemy]
                        $ defender = player
                        $ skillChoice = monSkillChoice[m]
                        call combatActionTurn from _call_combatActionTurn_1
                        #call EnemyTurn from _call_EnemyTurn
                        if len(monsterEncounter) == 0: #combat is over
                            jump combatWin

                    if m < len(monsterEncounter) > 0:
                        $ monInititive[m] = 0
                    $ m = len(monsterEncounter) + 1
                    if len(monsterEncounter) > 0:
                        if max(monInititive) == 0:
                            $ lastMonToGo = 1
                $ m += 1
    $ Speaker = Character(_(''))
    jump combatEndTurn

label combatEndTurn:
    $ refreshMenu = 1
    $ tranceIgnored = 0
    $ pushAwayAttempt = 0
    $ paralysisIgnored = 0
    $ skipPlayerOrgasm = 0
    $ skipMonsterOrgasm = 0
    $ skipTargetOrgasm = 0
    $ skipAttackOrgasm = 0

    $ attackerName = player.name
    $ attackerHeOrShe = getHeOrShe(player)
    $ attackerHisOrHer = getHisOrHer(player)
    $ attackerHimOrHer = getHimOrHer(player)
    $ attackerYouOrMonsterName = getYouOrMonsterName(player)
    $ display = ""





    if(player.statusEffects.aphrodisiac.duration > 0):
        $ player = applyPoison(player)
        $ display = "Aphrodisiac courses through {ThePlayerName}, arousing {AttackerHimOrHer} by {FinalDamage}!"
        call read from _call_read_10
    $ display = ""
    if player.statusEffects.sleep.potency > 0:
        $ player = applySleepy(player)
        $ display = "Drowsiness slowly lulls {ThePlayerName} towards sleep, sapping {FinalDamage} energy!"
        $ player.stats.BarMinMax()
        if player.stats.ep <= 0:
            $ player.statusEffects.sleep.duration = getSleepingDuration(player)
            $ player.statusEffects.sleep.potency = -99
            $ display = "With no energy left, {ThePlayerName}'s eyes close completely as {AttackerHeOrShe} drifts off into a peaceful slumber..."
            if display != "":
                call read from _call_read_3
            $ player.stats.ep += int(math.floor(player.stats.max_true_ep*0.5))
            $ display = ""
        #$ player.statusEffects.sleep.potency += 1
        #if player.statusEffects.sleep.potency == 2:
        #    $ display = "{ThePlayerName} is starting to feel incredibly tired..."
        #if player.statusEffects.sleep.potency == 3:
        #    $ display = "{ThePlayerName} just can't shake off the creeping drowsiness spreading through {AttackerHisOrHer} body..."
        #if player.statusEffects.sleep.potency == 4:
        #    $ display = "{ThePlayerName} can't help but yawn as {AttackerHisOrHer} eye lids feel incredibly heavy, it won't be much longer until {AttackerHeOrShe} falls asleep completely!"
        #if player.statusEffects.sleep.potency == 5:
        #
        if display != "":
            call read from _call_read_45

    python:
        if (player.statusEffects.surrender.duration <= 0):
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RegenMaxArousal":
                        player.stats.hp -= int(math.floor(player.stats.max_true_hp*((perk.EffectPower[p])*0.01)))
                    if perk.PerkType[p] == "RegenMaxEnergy":
                        player.stats.ep += int(math.floor(player.stats.max_true_ep*((perk.EffectPower[p])*0.01)))
                    p += 1
        player.stats.BarMinMax()

    $ mi = 0
    while mi < len(monsterEncounter):
        $ display = ""
        $ attackerName = monsterEncounter[mi].name
        $ attackerHeOrShe = getHeOrShe(monsterEncounter[mi])
        $ attackerHisOrHer = getHisOrHer(monsterEncounter[mi])
        $ attackerHimOrHer = getHimOrHer(monsterEncounter[mi])
        $ attackerYouOrMonsterName = getYouOrMonsterName(monsterEncounter[mi])

        $ foundLine = 0
        python:
            i = 0
            for each in monsterEncounter[mi].combatDialogue:
                specifyStance = 0
                CombatFunctionEnemytarget = mi
                CombatFunctionEnemyInitial = mi
                if each.lineTrigger == "EndOfRound":
                        Speaker = Character(_(monsterEncounter[mi].name))
                        display = each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                        foundLine = 1
                        break
                if i >= 10:
                    break


        if foundLine == 1:
            call read from _call_read_49



        if(monsterEncounter[mi].statusEffects.aphrodisiac.duration > 0):
            $ monsterEncounter[mi] = applyPoison(monsterEncounter[mi])
            $ display = "Aphrodisiac courses through {AttackerName}, arousing {AttackerHimOrHer} by {FinalDamage}."
            call read from _call_read_28
        $ display = ""
        if monsterEncounter[mi].statusEffects.sleep.potency >= 1:
            $ monsterEncounter[mi] = applySleepy(monsterEncounter[mi])
            $ display = "Drowsiness slowly lulls {AttackerName} towards sleep, sapping {FinalDamage} energy!"
            $ monsterEncounter[mi].stats.BarMinMax()
            if monsterEncounter[mi].stats.ep <= 0:
                $ monsterEncounter[mi].statusEffects.sleep.duration = getSleepingDuration(monsterEncounter[mi])
                $ monsterEncounter[mi].statusEffects.sleep.potency = -99
                $ display = "With no energy left, {AttackerName}'s eyes close completely as {AttackerHeOrShe} drifts off into a peaceful slumber..."
                if display != "":
                    call read from _call_read_5
                $ monsterEncounter[mi].stats.ep += int(math.floor(monsterEncounter[mi].stats.max_true_ep))
                $ display = ""

            #$ monsterEncounter[mi].statusEffects.sleep.potency += 1
            #if monsterEncounter[mi].statusEffects.sleep.potency == 2:
            #    $ display = "{AttackerName} is starting to feel incredibly tired..."
            #if monsterEncounter[mi].statusEffects.sleep.potency == 3:
            #    $ display = "{AttackerName} just can't shake off the creeping drowsiness spreading through {AttackerHisOrHer} body..."
            #if monsterEncounter[mi].statusEffects.sleep.potency == 4:
            #    $ display = "{AttackerName} can't help but yawn as {AttackerHisOrHer} eye lids feel incredibly heavy, it won't be much longer until {AttackerHeOrShe} falls asleep completely!"
            #if monsterEncounter[mi].statusEffects.sleep.potency >= 5:
            #    $ monsterEncounter[mi].statusEffects.sleep.potency = -99
            #    $ display =  "{AttackerName}'s eyes close completely as {AttackerHeOrShe} drifts off into a peaceful slumber..."
            if display != "":
                call read from _call_read_46
        $ display = ""
        $ monsterEncounter[mi].stats.BarMinMax()
        $ monsterEncounter[mi].statusEffects.turnPass(monsterEncounter[mi])
        $ monsterEncounter[mi].putInStance = 0
        $ monsterEncounter[mi].putInRestrain = 0

        python:
            for perk in monsterEncounter[mi].perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RegenMaxArousal":
                        monsterEncounter[mi].stats.hp -= int(math.floor(monsterEncounter[mi].stats.max_true_hp*((perk.EffectPower[p])*0.01)))
                    if perk.PerkType[p] == "RegenMaxEnergy":
                        monsterEncounter[mi].stats.ep += int(math.floor(monsterEncounter[mi].stats.max_true_ep*((perk.EffectPower[p])*0.01)))
                    p += 1
            monsterEncounter[mi].stats.BarMinMax()

        $ holda = monsterEncounter[mi].statusEffects.statusEnd(monsterEncounter[mi])
        $ diaplay = holda[0]
        $ monsterEncounter[mi] = holda[1]


        if display != "":
            call read from _call_read_16
        $ display = ""

        call PerkTimers(TimerType="TurnDuration", targetedCharacter=monsterEncounter[mi]) from _call_PerkTimers_3



        $ mi += 1

    $ Speaker = Character(_(''))

    if (player.statusEffects.defend.duration > 0):
        $ player.statusEffects.defend.potency += 1
    else:
        $ player.statusEffects.defend.potency = 0


    $ player.stats.BarMinMax()
    $ player.statusEffects.turnPass(player)
    $ holda = player.statusEffects.statusEnd(player)
    $ display = holda[0]
    $ player = holda[1]


    $ combatChoice = Skill()
    $ itemChoice = Item("Blank", "Null", 0)



    if display != "":
        call read from _call_read_17
    $ display = ""
    $ justEscapedStance -= 1
    call PerkTimers(TimerType="TurnDuration", targetedCharacter=player) from _call_PerkTimers_1

    call TimeEvent(CardType="EndOfTurn", LoopedList=EndOfTurnList) from _call_TimeEvent_2

    call TurnStart from _call_TurnStart_1

    jump combatPlayer


label TurnStart:
    $ mi = 0
    while mi < len(monsterEncounter):
        $ display = ""
        $ attackerName = monsterEncounter[mi].name
        $ attackerHeOrShe = getHeOrShe(monsterEncounter[mi])
        $ attackerHisOrHer = getHisOrHer(monsterEncounter[mi])
        $ attackerHimOrHer = getHimOrHer(monsterEncounter[mi])
        $ attackerYouOrMonsterName = getYouOrMonsterName(monsterEncounter[mi])
        $ foundLine = 0
        python:
            i = 0
            for each in monsterEncounter[mi].combatDialogue:
                specifyStance = 0
                CombatFunctionEnemytarget = mi
                CombatFunctionEnemyInitial = mi
                if each.lineTrigger == "StartOfRound":
                        Speaker = Character(_(monsterEncounter[mi].name))
                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                        foundLine = 1
                        break
                if i >= 10:
                    break
        if foundLine == 1:
            call read from _call_read_54
        $ mi += 1
    call TimeEvent(CardType="StartOfTurn", LoopedList=StartOfTurnList) from _call_TimeEvent_15
    return

label combatLoss:
    $ hidingCombatEncounter = 0
    $ VicChosenScene = -5
    $ victoryScene = 0
    # play scene, go back to town or game over/badend
    $ DialogueIsFrom = "Monster"
    $ chosenScene = 0
    $ lineOfScene = 0
    $ cmenu_tooltip = ""
    $ CombatFunctionEnemytarget = 0
    $ canRun = True
    $ HoldingSceneForCombat = ""
    $ HoldingLineForCombat = 0
    $ HoldingDataLocForCombat = ""
    $ runAndStayInEvent = 0
    $ player = ClearNonPersistentEffects(player)
    hide screen ON_CombatMenuTooltip

    $ lossExpPower = 0
    $ LossExp = 0
    python:
        increaseFetishOnLoss(lastAttack, theLastAttacker)
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "LossExp":
                    lossExpPower += (perk.EffectPower[p]*0.01)
                p += 1
        if lossExpPower > 0:
            LossExp = ExpPool * lossExpPower
            for each in monsterEncounter:
                LossExp += each.stats.Exp * lossExpPower

            LossExp = math.floor(LossExp)
            LossExp = int(LossExp)

    $ chosenScene = -5
    $ runBG = ""

    call TimeEvent(CardType="EndOfCombat", LoopedList=EndOfCombatList) from _call_TimeEvent_11


    $ BGMlist = []
    $ BGMlist.append("music/Loss/Do not yarn.mp3")
    $ BGMlist.append("music/Loss/Falling Down.mp3")
    $ BGMlist.append("music/Loss/reason.mp3")

    $ renpy.random.shuffle(BGMlist)
    $ SetBGM = BGMlist[0]

    play music SetBGM fadeout 1.0 fadein 1.0

    if theLastAttacker.species == "Player":
        $ theLastAttacker = monsterEncounter[0]



    #Get loss scene
    $ chosenScene = getTheEndScene(theLastAttacker.lossScenes, theLastAttacker, monsterEncounter, trueMonsterEncounter, lastAttack)

    $ extension = ""
    if theLastAttacker.lossScenes[chosenScene].picture != "":
        $ extension = theLastAttacker.lossScenes[chosenScene].picture
        show screen DisplayLossImage
        #hide screen ON_HealthDisplayBacking
        #hide screen ON_HealthDisplay
        #$ renpy.hide_screen("ON_HealthDisplayBacking", layer="master")
        #$ renpy.hide_screen("ON_HealthDisplay", layer="master")


    $ displayingScene = theLastAttacker.lossScenes[chosenScene]
    $ actorNames[0] =  theLastAttacker.name
    call displayScene from _call_displayScene
    #^plays selected loss scene
    $ renpy.set_return_stack(lastReturn)
    jump lostExpCheck





label lostExpCheck:
    $ lvlupCheck = 0

    python:
        if LossExp > 0:
            ExpBoost = 1

            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "ExpBoost":
                        ExpBoost += ((perk.EffectPower[p])*0.01)*0.5
                    p += 1
            LossExp = int(math.floor((LossExp*ExpBoost)))

            player.stats.Exp += LossExp
            player.stats.Exp = math.floor(player.stats.Exp)
            player.stats.Exp= int(player.stats.Exp)


            display = "Defeated!\n"+"But you gained " + str(LossExp) + " Exp. "
            lvlupCheck = 1


    if lvlupCheck == 1 and LossExp != 0:
        "[display]"
        $ LossExp = 0
        call refreshLevelVar from _call_refreshLevelVar
        call levelUpSpot from _call_levelUpSpot

    if NoGameOver == 1:
        $ NoGameOver = 0
        return


label combatLossEnd:
    $ hidingCombatEncounter = 0
    $ monsterEncounter = []
    $ combatItems = 0
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ SceneCharacters = []
    $ explorationDeck = []
    $ cmenu_tooltip = ""
    $ deckProgress = 0
    $ displayingScene = Dialogue()
    $ player = player.statusEffects.refresh(player)
    $ onGridMap = 0
    hide screen Gridmap
    hide screen GridmapPlayer
    hide screen GridmapNPCs
    hide screen GridmapObstacles
    $ TheGrid = []

    #$ player.stats.refresh()
    $ player.stats.sp = 1
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    $ player.restraintOnLoss = [""]

    $ StoredScene = ""
    $ StoredLine = 0
    $ StoredDataLoc = ""
    $ isEventNow = 0
    $ runAndStayInEvent = 0
    $ inChurch = 1
    call EndAllEffects from _call_EndAllEffects

    #hide screen ON_HealthDisplayBacking
    #hide screen ON_HealthDisplay


    #some day I'll move this into an event. Some day.
    hide screen DisplayLossImage
    $ bg = changeBG("Church.png")
    show screen DisplayBG (_layer="master")
    show screen ON_CharacterDialogueScreen (_layer="master")
    stop music fadeout 1.0

    $ player = player.statusEffects.refresh(player)
    $ player.stats.refresh()
    $ timeNotify = 1
    call advanceTime(TimeIncrease=1) from _call_advanceTime_6
    $ timeNotify = 1
    if TimeOfDay != Morning:
        while TimeOfDay != Morning:
            if TimeOfDay != Morning:
                $ timeNotify = 1
                call advanceTime(TimeIncrease=1) from _call_advanceTime_7
    $ notFunction = 0

    "You wake up in the church the next day, still feeling completely exhausted and drained."
    $ findLily = getFromName("Lillian", MonsterDatabase)
    $ SceneCharacters.append(MonsterDatabase[findLily])
    $ SceneCharacters[0].ImageSets[0].ImageSet[0].currentImage = getFromName("Surprised", SceneCharacters[0].ImageSets[0].ImageSet[0].Images)
    Lily "Ah?! [player.name]!? Oh no! I'll get the holy water!"
    $ SceneCharacters[0].ImageSets[0].ImageSet[0].currentImage = getFromName("Base", SceneCharacters[0].ImageSets[0].ImageSet[0].Images)
    "Before you can answer a bucket of water is dumped on you before Lillian applies her healing magic."
    $ SceneCharacters[0].ImageSets[0].ImageSet[0].currentImage = getFromName("Happy", SceneCharacters[0].ImageSets[0].ImageSet[0].Images)
    Lily "Don't worry I'm sure you'll do it next time! I believe in you!"
    $ SceneCharacters = []
    $ InventoryAvailable = True
    $ canRun = True

    if victoryScene == 1:
        call PostCombatWin from _call_PostCombatWin_1
    $ victoryScene = 0

    $ inChurch = 0

    jump Church


label combatWin:
    #Victory Scene
    $ LostGameOver = -1
    $ hidingCombatEncounter = 0
    $ canRun = True
    $ Speaker = Character(_(""))
    $ VicChosenScene = -5
    $ victoryScene = 0
    $ player = ClearNonPersistentEffects(player)
    hide screen ON_CombatMenuTooltip

    call TimeEvent(CardType="EndOfCombat", LoopedList=EndOfCombatList) from _call_TimeEvent_12

    if (DefeatedEncounterMonsters[-1].victoryScenes[0].theScene[0] != ""):
        $ victoryScene = 1
        if displayingScene != []:
            if lineOfScene + 1 < len(displayingScene.theScene):
                $ HoldingScene = copy.deepcopy(displayingScene)
                $ HoldingLine = copy.deepcopy(lineOfScene) + 1
                $ HoldingDataLoc = copy.deepcopy(DataLocation)

        $ DialogueIsFrom = "Monster"
        #$ test = len(DefeatedEncounterMonsters[-1].victoryScenes[5].includes)
        #"[test]"

        $ displayTest = DefeatedEncounterMonsters[-1].victoryScenes
        $ VicChosenScene = getTheEndScene(DefeatedEncounterMonsters[-1].victoryScenes, DefeatedEncounterMonsters[-1], monsterEncounter, DefeatedEncounterMonsters, lastAttack)


        python:
            for each in DefeatedEncounterMonsters:
                SceneCharacters.append(each)

        $ displayingScene = DefeatedEncounterMonsters[-1].victoryScenes[VicChosenScene]
        $ actorNames[0] =  DefeatedEncounterMonsters[-1].name
        $ monsterEncounter = []
        $ lineOfScene = 0
        $ combatItems = 0
        $ runAndStayInEvent = 1
        call displayScene from _call_displayScene_8
        $ DialogueIsFrom = "Event"
        $ victoryScene = 0



label PostCombatWin:
    $ runAndStayInEvent = 0
    $ hidingCombatEncounter = 0
    if SetSongAfterCombat == "":
        python:
            BGMlist = []
            for each in LocationDatabase[targetLocation].MusicList:
                BGMlist.append(each)
        if musicLastPlayed != BGMlist:
            $ musicLastPlayed = copy.deepcopy(BGMlist)
            $ renpy.random.shuffle(BGMlist)
            if renpy.music.get_playing(channel='music') != BGMlist[0]:
                play music BGMlist fadeout 1.0 fadein 1.0
    else:
        python:
            BGMlist = []
            BGMlist.append(SetSongAfterCombat)
        if musicLastPlayed != BGMlist:
            $ musicLastPlayed = copy.deepcopy(SetSongAfterCombat)
            $ renpy.random.shuffle(BGMlist)
            if renpy.music.get_playing(channel='music') != BGMlist[0]:
                play music BGMlist fadeout 1.0 fadein 1.0
        $ SetSongAfterCombat = ""

    $ HoldingLine = -1
    $ monsterEncounter = []
    $ combatItems = 0
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ SceneCharacters = []
    $ cmenu_tooltip = ""
    #give rewards, Exp
    #end

    if noDoubleRewards == 0:
        $ runBG = ""
        $ canRun = True

        $ player.clearStance()

        $ ExpBoost = 1
        python:
            for perk in attacker.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "ExpBoost":
                        ExpBoost += (perk.EffectPower[p])*0.01
                    p += 1
        $ ExpPool = int(math.floor((ExpPool*ExpBoost)))
        $ display = "Victory!\n"+"You gained " + str(ExpPool) + " Exp. "
        $ player.stats.Exp += ExpPool
        $ player.stats.Exp = math.floor(player.stats.Exp)
        $ player.stats.Exp= int(player.stats.Exp)
        $ player.restraintStruggle = [""]
        $ player.restraintStruggleCharmed = [""]
        $ player.restraintEscaped = [""]
        $ player.restraintEscapedFail = [""]
        $ player.restraintOnLoss = [""]

        $ perkChosen = ""

        if MoneyDrops > 0:
            $ bonusMoney = 100
            python:
                for perk in attacker.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "ErosBoost":
                            bonusMoney += perk.EffectPower[p]
                        p += 1

            $ MoneyDrops = int(math.floor(((MoneyDrops*(bonusMoney*0.01)) * (renpy.random.randint(75, 125)*0.01)) * (player.stats.Luck*0.01 + 1)))


            $ display += "You gained " + str(MoneyDrops) + " Eros. "
            $ player.inventory.earn(MoneyDrops)
        "[display]"

        if len(LootDrops) > 0:
            $ c = 0
            $ collectedItems = []
            while c < len(LootDrops):
                $ alreadyCollected = 0
                python:
                    for each in collectedItems:
                        if LootDrops[c] == each:
                            alreadyCollected = 1
                if alreadyCollected == 0:
                    $ player.inventory.give(LootDrops[c], LootDrops.count(LootDrops[c]))
                    $ collectedItems.append(LootDrops[c])
                    $ addS = ""
                    if LootDrops.count(LootDrops[c]) > 1 and LootDrops[c][-1] != "s":
                        $ addS = "s"
                    $ display = "You acquired " + str(LootDrops.count(LootDrops[c])) + " " + LootDrops[c] + addS + "!"
                    "[display]"
                $ c+=1


        call refreshLevelVar from _call_refreshLevelVar_1
        call levelUpSpot from _call_levelUpSpot_2
    $ noDoubleRewards = 1

    if inChurch == 0:
        $ renpy.set_return_stack(lastReturn)

    return

label refreshLevelVar:
    $ culmitiveLeveling = 0
    $ hpIncreases = 0
    $ statPointIncreases = 0
    $ sensitivityIncreases = 0
    $ perkIncreases = 0
    return

label levelUpSpot:
    $ culmitiveLeveling += 1
    if player.stats.Exp >= player.stats.ExpNeeded:
        $ player.stats.Exp -= player.stats.ExpNeeded
        $ player.stats.lvl += 1

        python:
            player.stats.ExpNeeded = int((0.4*(player.stats.lvl*player.stats.lvl)) + (2*player.stats.lvl) + (15*math.sqrt(player.stats.lvl)-8))

        $ player.statPoints += 3
        $ statPointIncreases += 3
        #$ player.stats.refresh()
        $ player.stats.hp = 0
        $ player.stats.ep = player.stats.max_true_ep
        $ shifting = 1

        #if player.stats.lvl % 2 == 0:
            #if hpDeficit < 0:
            #        $ player.stats.max_hp = copy.deepcopy(hpDeficit)
            #        $ hpDeficit = 0
            #$ player.stats.max_hp += 5
            #if player.stats.max_hp < 1:
            #        $ hpDeficit = copy.deepcopy(player.stats.max_hp)
            #        $ player.stats.max_hp = 1
            #$ hpIncreases += 5
            #$ player.stats.refresh()

        python:
            try:
                if difficulty == "Easy":
                    player.stats.refresh()
            except:
                difficulty = "Normal"


        if player.stats.lvl % 5 == 0:
            $ player.SensitivityPoints += 1
            $ sensitivityIncreases += 1

        if player.stats.lvl % 3 == 0:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl == 5:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl == 10:
            $ player.perkPoints += 2
            $ perkIncreases += 2

        if player.stats.lvl == 20:
            $ player.perkPoints += 2
            $ perkIncreases += 2


        $ tt = Tooltip("")

        $ creating = 0

        if player.SensitivityPoints > 0:
            $ hasResPoints = 1
        else:
            $ hasResPoints = 0

        #call levelup function
        if player.stats.Exp >= player.stats.ExpNeeded:
            jump levelUpSpot

        if culmitiveLeveling == 1:
            $ display = "Level up!\n"
        else:
            $ display = "Level increased by "+str(culmitiveLeveling)+"!\n"

        #if hpIncreases > 0:
            #$ display += "Max Arousal +"+str(hpIncreases)+"!\n"

        if statPointIncreases == 2:
            $ display += "Gained two stat points!"
        else:
            $ display += "Gained " + str(statPointIncreases) + " stat points!"

        if sensitivityIncreases == 1:
            $ display += "\nGained a point to alter sensitivity!"
        elif sensitivityIncreases > 0:
            $ display += "\nGained " + str(sensitivityIncreases) + " points to alter sensitivity!"

        if perkIncreases > 0:
            $ display += "\nGained " + str(perkIncreases) + " perk point!"

        "[display]"

        call setStatFloors from _call_setStatFloors
        call spendLvlUpPoints from _call_spendLvlUpPoints
        hide screen CreatorDisplay


    $ InventoryAvailable = True
    #hide screen ON_HealthDisplayBacking
    #hide screen ON_HealthDisplay

    if NoGameOver == 1 or expGiven == 1 or LostGameOver == 1:
        return

    if runAndStayInEvent == 1:
        jump endCombatCalled

    return



label removeThisStanceStances:
    $ howManyStances = "One"
    jump StanceStruggleGo

label removeAllStances:
    $ howManyStances = "All"
    $ tryRemoveThisStance = 0
    jump StanceStruggleGo

label combatPushAway:
    # new GUI: this is only ever called from the combat menu if there's only one target and only one stance
    $ pushAwayAttempt = 1
    $ tryRemoveThisStance = 0
    $ targeting = 0
    $ howManyStances = "All"
    window hide
    hide screen returnButton
    hide screen ON_CombatMenu
    $ combatChoice = copy.deepcopy(getSkill("Push Away", SkillsDatabase))

    $ stanceNum = len(monsterEncounter[target].combatStance)

label StanceStruggleGo:
    $ pushAwayAttempt = 1
    hide screen returnButton
    hide screen ON_CombatMenu

    $ attackerName = monsterEncounter[target].name
    $ attackerHeOrShe = getHeOrShe(monsterEncounter[target])
    $ attackerHisOrHer = getHisOrHer(monsterEncounter[target])
    $ attackerHimOrHer = getHimOrHer(monsterEncounter[target])
    $ attackerYouOrMonsterName = getYouOrMonsterName(monsterEncounter[target])

    $ targetName = player.name
    $ targetHeOrShe = getHeOrShe(player)
    $ targetHisOrHer = getHisOrHer(player)
    $ targetHimOrHer = getHimOrHer(player)
    $ targetYouOrMonsterName = getYouOrMonsterName(player)
    $ Speaker = Character(_(''))

    $ display = ""
    $ foundLine = 0
    python:
        for each in monsterEncounter[target].combatDialogue:
            if each.lineTrigger == "StanceStruggle" :
                stanceChecking = copy.deepcopy(tryRemoveThisStance)
                for stance in monsterEncounter[target].combatStance:
                    if foundLine == 0 and stanceChecking < len(monsterEncounter[target].combatStance):
                        for possibleStances in each.move:
                            if possibleStances == monsterEncounter[target].combatStance[stanceChecking].Stance and foundLine == 0:
                                display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                foundLine = 1
                    if howManyStances != "One":
                        stanceChecking += 1

    if display == "":
        "You try to push away [attackerName]..."
    else:
        $ CombatFunctionEnemytarget = target
        $ CombatFunctionEnemyInitial = target
        call read from _call_read_32

    $ stanceBroken = 0
    $ stanceHPTotal = 0
    $ stanceDamageTotal = getStanceStruggleRoll(player)
    python:
        for stance in monsterEncounter[target].combatStance:
            stanceHPTotal += stance.potency

    if monsterEncounter[target].statusEffects.sleep.potency == -99 or monsterEncounter[target].statusEffects.trance.potency >= 11 or monsterEncounter[target].statusEffects.stunned.duration > 0 or monsterEncounter[target].statusEffects.restrained.duration > 0:
        $ stanceDamageTotal += 1000000000

    if stanceHPTotal <= stanceDamageTotal:
        $ stanceBroken = 1
    else:
        $ stanceDamageTotal/= len(monsterEncounter[target].combatStance)
        python:
            for stance in monsterEncounter[target].combatStance:
                stance.potency -= stanceDamageTotal

    if stanceBroken == 1:
        $ display = ""
        $ foundLine = 0
        python:
            for each in monsterEncounter[target].combatDialogue:
                if each.lineTrigger == "StanceStruggleFree":
                    stanceChecking = copy.deepcopy(tryRemoveThisStance)
                    for stance in monsterEncounter[target].combatStance:
                        if foundLine == 0 and stanceChecking < len(monsterEncounter[target].combatStance):
                            for possibleStances in each.move:
                                if possibleStances == monsterEncounter[target].combatStance[stanceChecking].Stance and foundLine == 0:
                                    display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                    foundLine = 1

        python:
            RemovedStance = []
            if howManyStances == "One":
                RemovedStance.append(copy.deepcopy(monsterEncounter[target].combatStance[tryRemoveThisStance].Stance))
                player.removeStanceByName(monsterEncounter[target].combatStance[tryRemoveThisStance].Stance)
                monsterEncounter[target].removeStanceByName(monsterEncounter[target].combatStance[tryRemoveThisStance].Stance)
            elif howManyStances == "All":

                for each in monsterEncounter[target].combatStance:
                    RemovedStance.append(copy.deepcopy(each.Stance))
                    player.removeStanceByName(each.Stance)
                monsterEncounter[target].clearStance()


        if display == "":
            "And pull away!"
        else:
            $ CombatFunctionEnemytarget = target
            $ CombatFunctionEnemyInitial = target
            call read from _call_read_33

        $ display = ""
        $ foundLine = 0

        python:
            if monsterEncounter[target].statusEffects.sleep.potency != -99:
                for each in monsterEncounter[target].combatDialogue:
                    if each.lineTrigger == "StanceStruggleFreeComment":
                        stanceChecking = copy.deepcopy(tryRemoveThisStance)
                        for possibleStances in each.move:
                            if foundLine == 0:
                                for stance in RemovedStance:
                                    if possibleStances == stance:
                                        Speaker = Character(_(monsterEncounter[target].name))
                                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                        foundLine = 1


        if display != "":
            $ CombatFunctionEnemytarget = target
            $ CombatFunctionEnemyInitial = target
            call read from _call_read_34

        $ justEscapedStance = 2


    else:
        $ display = ""
        $ foundLine = 0
        python:
            for each in monsterEncounter[target].combatDialogue:
                if each.lineTrigger == "StanceStruggleFail":
                    stanceChecking = copy.deepcopy(tryRemoveThisStance)
                    for stance in monsterEncounter[target].combatStance:
                        if foundLine == 0 and stanceChecking < len(monsterEncounter[target].combatStance):
                            for possibleStances in each.move:
                                if possibleStances == monsterEncounter[target].combatStance[stanceChecking].Stance and foundLine == 0:
                                    display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                    foundLine = 1

        if display == "":
            "But fail!"
        else:
            $ CombatFunctionEnemytarget = target
            $ CombatFunctionEnemyInitial = target
            call read from _call_read_35

        $ display = ""
        $ foundLine = 0
        python:
            if monsterEncounter[target].statusEffects.sleep.potency != -99:
                for each in monsterEncounter[target].combatDialogue:
                    if each.lineTrigger == "StanceStruggleComment":
                        stanceChecking = copy.deepcopy(tryRemoveThisStance)
                        for stance in monsterEncounter[target].combatStance:
                            if foundLine == 0 and stanceChecking < len(monsterEncounter[target].combatStance):
                                for possibleStances in each.move:
                                    if possibleStances == monsterEncounter[target].combatStance[stanceChecking].Stance and foundLine == 0:
                                        Speaker = Character(_(monsterEncounter[target].name))
                                        display += each.theText[renpy.random.randint(-1, len(each.theText)-1)]
                                        foundLine = 1

        if display != "":
            $ CombatFunctionEnemytarget = target
            $ CombatFunctionEnemyInitial = target
            call read from _call_read_36

    $ cmenu_refreshMenu()
    $ display = ""
    jump combatPlayer



label combatStruggle:
    window hide
    hide screen returnButton
    hide screen ON_CombatMenu
    $ combatChoice = copy.deepcopy(getSkill("Struggle", SkillsDatabase))
    $ target = 0
    $ attackerName = player.restrainer.name
    $ attackerHeOrShe = getHeOrShe(player.restrainer)
    $ attackerHisOrHer = getHisOrHer(player.restrainer)
    $ attackerHimOrHer = getHimOrHer(player.restrainer)
    $ attackerYouOrMonsterName = getYouOrMonsterName(player.restrainer)

    $ targetName = player.name
    $ targetHeOrShe = getHeOrShe(player)
    $ targetHisOrHer = getHisOrHer(player)
    $ targetHimOrHer = getHimOrHer(player)
    $ targetYouOrMonsterName = getYouOrMonsterName(player)
    $ Speaker = Character(_(''))
    $ despMod = 0

    call combatStruggleActivate(player) from _call_combatStruggleActivate_2

    if UnshackledFreedom == 1:
        jump combatPlayer

    $ display = ""
    jump combatEnemies


label combatStruggleActivate(Struggler):
    $ theTarget = ""

    if Struggler.species != "Player":
        $ monSkillChoice[m] = copy.deepcopy(getSkill("Struggle", SkillsDatabase))
    else:
        $ combatChoice = copy.deepcopy(getSkill("Struggle", SkillsDatabase))

    $ despMod = 0
    if desperateStruggle == 1 and Struggler.species == "Player":
        $ desperateStruggle = 0
        $ despMod = 0.35
        $ player.stats.ep -= 10

    $ charmMod = 1
    if Struggler.statusEffects.charmed.duration > 0:
        $ charmMod = 0.5
        if Struggler.restraintStruggleCharmed[0] == "" and Struggler.species == "Player":
            "You weakly struggle against your restraints..."
        elif Struggler.restraintStruggleCharmed[0] == "" and Struggler.species != "Player":
            $ display = Struggler.name + " weakly struggles..."
        else:
            $ display = Struggler.restraintStruggleCharmed[renpy.random.randint(-1, len(Struggler.restraintStruggleCharmed)-1)]

            call read from _call_read_24
    else:
        if Struggler.restraintStruggle[0] == "" and Struggler.species == "Player":
            "You struggle against your restraints..."
        elif Struggler.restraintStruggleCharmed[0] == "" and Struggler.species != "Player":
            $ display = Struggler.name + " struggles..."
        else:
            $ display = Struggler.restraintStruggle[renpy.random.randint(-1, len(Struggler.restraintStruggle)-1)]
            call read from _call_read_25

    $ restraintEscapeBoost = 0
    python:
        for perk in Struggler.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "RemoveRestraints":
                    restraintEscapeBoost += perk.EffectPower[p]
                p += 1

    $ Struggler.statusEffects.restrained.duration -= getRestrainStruggle(Struggler, restraintEscapeBoost, charmMod, despMod)

    if Struggler.statusEffects.restrained.duration <= 0:
        if Struggler.restraintEscaped[0] == "" and Struggler.species == "Player":
            "And free yourself!"
        elif Struggler.restraintStruggleCharmed[0] == "" and Struggler.species != "Player":
            $ display = "and gets free!"
        else:
            $ display = Struggler.restraintEscaped[renpy.random.randint(-1, len(Struggler.restraintEscaped)-1)]
            call read from _call_read_26

        $ justEscapedStance = 2
        $ CheckImmunity = getFromName("Restraint Immune", Struggler.perks)
        if CheckImmunity == -1:
            $ Struggler.giveOrTakePerk("Restraint Immune", 1)
        else:
            $ Struggler.giveOrTakePerk("Restraint Immune", -1)
            $ Struggler.giveOrTakePerk("Restraint Immune", 1)
        $ Struggler.statusEffects.restrained.duration = 0
    else:
        if Struggler.restraintEscapedFail[0] == "" and Struggler.species == "Player":
            "But can't get free!"
        elif Struggler.restraintStruggleCharmed[0] == "" and Struggler.species != "Player":
            $ display = "but can't get free!"
        else:
            $ display = Struggler.restraintEscapedFail[renpy.random.randint(-1, len(Struggler.restraintEscapedFail)-1)]
            call read from _call_read_27

    $ UnshackledFreedom = 0
    python:
        for perk in Struggler.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "Unshackled" and Struggler.statusEffects.restrained.duration <= 0:
                    UnshackledFreedom = 1
                p += 1

    $ display = ""
    return



label combatBasicAttack:
    window hide
    $ combatChoice = copy.deepcopy(getSkill("Caress", SkillsDatabase))


    jump targeting

label combatDefend:
    window hide
    $ combatChoice = copy.deepcopy(getSkill("Defend", SkillsDatabase))
    $ player.statusEffects.defend.duration = 1
    $ target = 0
    #add status defending
    jump combatEnemies

label combatWait:
    window hide
    $ combatChoice = copy.deepcopy(getSkill("Wait", SkillsDatabase))
    $ waiting = 1
    $ target = 0
    $ player.stats.ep += int(math.floor(player.stats.max_true_ep*0.05))
    #add status defending
    jump combatEnemies


label combatSurrender:
    window hide
    $ combatChoice = copy.deepcopy(getSkill(" ", SkillsDatabase))
    $ player.statusEffects.surrender.duration = 1
    $ player.stats.sp = 0
    $ target = 0

    hide screen ON_CombatMenu

    call onSurrenderTalk from _call_onSurrenderTalk
    $ theLastAttacker = monsterEncounter[0]
    jump combatLoss

label combatGiveUp:
    window hide
    hide screen ON_CombatMenu
    $ combatChoice = copy.deepcopy(getSkill(" ", SkillsDatabase))
    $ player.statusEffects.surrender.duration = 1
    $ target = 0
    call onSurrenderTalk from _call_onSurrenderTalk_1
    jump combatEnemies

label onSurrenderTalk:
    $ i = 0
    $ l = 0
    $ cmenu_resetMenu()
    while i < len(monsterEncounter):
        $ display = ""
        $ l = 0
        if monsterEncounter[i].statusEffects.sleep.potency != -99:
            while l < len(monsterEncounter[i].combatDialogue):
                if monsterEncounter[i].combatDialogue[l].lineTrigger == "OnSurrender":
                    $ Speaker = Character(_(monsterEncounter[i].name))
                    $ display = monsterEncounter[i].combatDialogue[l].theText[renpy.random.randint(-1, len(monsterEncounter[i].combatDialogue[l].theText)-1)]
                $ l += 1

        if display != "":
            $ CombatFunctionEnemytarget = i
            $ CombatFunctionEnemyInitial = i
            call read from _call_read_21
        $ i += 1
    return


label combatMoveChoice:
    #$ SkillNumber -= 1 #because weird reasons
    $ combatChoice = copy.deepcopy(player.skillList[SkillNumber])
    jump targeting

label combatItemChoice:
    $ ItemNumber -= 1 #because weird reasons
    $ fetchSkill = getFromName(player.inventory.items[ItemNumber].skills[0], SkillsDatabase)
    $ combatChoice = copy.deepcopy(SkillsDatabase[fetchSkill])
    $ itemChoice = copy.deepcopy(player.inventory.items[ItemNumber])
    $ combatChoice.isSkill = itemChoice.itemType

    jump targeting

label combatRun:
    window hide
    hide screen returnButton
    hide screen ON_CombatMenu
    $ target = 0
    $ combatChoice = copy.deepcopy(getSkill("Run Away", SkillsDatabase))
    jump combatEnemies


label combatRunAttempt:
    "You try to run..."
    #roll opposed check to escape
    $ failed = 0

    python:
        for each in monsterEncounter:
            monsterRoll = each.stats.Tech + (each.stats.Luck)*0.5  + renpy.random.randint(0,100)

            runBonus = 0
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RunChance":
                        runBonus += perk.EffectPower[p]
                    p += 1

            for perk in each.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "OpponentRunChance":
                        runBonus += perk.EffectPower[p]
                    p += 1

            playerRoll = player.stats.Tech*1.5 + (player.stats.Luck)*0.5  + renpy.random.randint(0,100) + runBonus

            if each.statusEffects.sleep.potency == -99 or each.statusEffects.trance.potency >= 11 or each.statusEffects.stunned.duration > 0 or each.statusEffects.restrained.duration > 0:
                playerRoll = 1000000000

            if (monsterRoll >= playerRoll):
                failed += 1
    if player.statusEffects.trance.potency >= 11:
        "But your mind is so completely enthralled, you stop yourself from running!"
        return
    elif failed >= 1: #add some effects for compounded failure
        "But you couldn't get away!"
        return

    $ monsterEncounter = []
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ hidingCombatEncounter = 0

    "And get away!"

    call TimeEvent(CardType="EndOfCombat", LoopedList=EndOfCombatList) from _call_TimeEvent_13

    if runBG != "":
        $ bg = runBG
        $ runBG = ""

    $ lastCombatSongPosition = renpy.music.get_pos(channel='music')
    $ lastCombatSong = copy.deepcopy(BGMlist[0])
    python:
        BGMlist = []
        for each in LocationDatabase[targetLocation].MusicList:
            BGMlist.append(each)
    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0


    call EndAllEffects from _call_EndAllEffects_1
    $ cmenu_tooltip = ""
    $ RanAway = "True"
    hide screen ON_CombatMenu
    #hide screen ON_HealthDisplayBacking
    #hide screen ON_HealthDisplay
    hide screen ON_CombatMenuTooltip
    $ combatItems = 0
    $ player = ClearNonPersistentEffects(player)
    $ renpy.set_return_stack(lastReturn)
    if runAndStayInEvent == 1:
        jump endCombatCalled
    return

label functionEnd:
