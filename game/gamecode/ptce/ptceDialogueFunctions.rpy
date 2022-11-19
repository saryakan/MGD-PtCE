init 1 python:
    PTCE_PREFIX = "ptce"

    def ptceOpenSaveMenu():
        _game_menu_screen = "save"
        renpy.call_in_new_context("_game_menu")
        _game_menu_screen = "ON_CharacterDisplayScreen" if ptceConfig.get("hardcoreMode") else "save"
    
    def ptceGivePerkFromInput():
        debugInput = renpy.input("Which Perk do you want?", length=30) or ("None")
        if debugInput != "None":
            playerHasPerk = debugInput in (perk.name for perk in player.perks)
            if playerHasPerk:
                display = "You already have the perk \"" + debugInput + "\"."
            else:
                player.giveOrTakePerk(debugInput, 1)
                display = "Got the perk \"" + debugInput + "\"."
            
            renpy.say(None, "[display]")
    
    def ptceGiveExpFromInput():
        debugInput = renpy.input("How many Exp do you want?", length=20) or ("0")
        player.stats.Exp += int(debugInput)
                
        if int(debugInput) > 0:
            renpy.say(None, "Gained " + debugInput + " exp!")
        else:
            amountLost = moneyEarned*-1
            renpy.say(None, "Lost " + debugInput + " exp!")
        
        expGiven = 1
        renpy.call("refreshLevelVar")
        renpy.call("levelUpSpot")
        expGiven = 0

    def ptceGiveErosFromInput():
        debugInput = renpy.input(_("How much Eros do you want?"), length=20) or _("0")
        player.inventory.money += int(debugInput)

    def ptceChangeFetishOverride():
        global ptceConfig, lineOfScene, displayingScene

        FETISH_MAX_LEVEL = ptceConfig.get("fetishGain").get("fetishMaxLevel")
        lineOfScene += 1
        resTarget = displayingScene.theScene[lineOfScene]
        lineOfScene += 1
        resAmount = int(displayingScene.theScene[lineOfScene])
        playersFetish = player.getFetishObject(resTarget)
        playerFetish.increaseTemp(resAmount)

        if playersFetish.Type == "Fetish" and resAmount != 0:
            if playersFetish.Level < FETISH_MAX_LEVEL:
                if (resAmount > 0):
                    if playersFetish.Level - resAmount == 0:
                        display = "You have started getting a fetish for " + resTarget +  "..."
                    elif playersFetish.Level - resAmount < 25 and playersFetish.Level >= 25:
                        display = "You have acquired a fetish for " + resTarget +  "."
                    else:
                        display = "Your fetish for " + resTarget +  " has intensified!"

                elif (resAmount < 0):
                    if playersFetish.Level <= 0:
                        display = "You have lost your fetish for " + resTarget +  "."
                    else:
                        display = "Your fetish for " + resTarget +  " has receded."
            
            else:
                display = "Your fetish for " + resTarget +  " has become a complete and total obsession, but it can't get any worse than it is now...."
            
            renpy.say(None, "[display]")
        
    def ptcePermanentlyChangeFetishOverride():
        global lineOfScene, displayingScene, ptceConfig

        FETISH_MAX_LEVEL = ptceConfig.get("fetishGain").get("fetishMaxLevel")
        lineOfScene += 1
        resTarget = displayingScene.theScene[lineOfScene]
        lineOfScene += 1
        resAmount = int(displayingScene.theScene[lineOfScene])

        playersFetish = player.getFetishObject(resTarget)
        playersFetish.increasePerm(resAmount)

        baseFetish = playersFetish.Level

        if playersFetish.Type == "Fetish":
            if baseFetish < FETISH_MAX_LEVEL:
                if (int(displayingScene.theScene[lineOfScene]) >= 1):
                    if resAmount > 1:
                        display = "You {i}permanently{/i} gained " + str(resAmount) + " fetish levels for " + resTarget +  "..."
                    else:
                        display = "You have {i}permanently{/i} gained a fetish level for " + resTarget +  "."

                elif (int(displayingScene.theScene[lineOfScene]) < 0):
                    resAmount *= -1
                    if resAmount > 1:
                        display = "You have {i}permanently{/i} lost " + str(resAmount) +" fetish levels for " + resTarget +  "."
                    else:
                        display = "You have {i}permanently{/i} lost a fetish level for " + resTarget +  "."
            if baseFetish > FETISH_MAX_LEVEL and resAmount >= 1:
                display = "Fantasies of " + resTarget +  " swirl through your mind, and your heart beats faster, you have {i}permanently{/i} gained a fetish level for " + resTarget + ", exceeding your normal obsession..."

            if (resAmount != 0):
                renpy.say(None, "[display]")
    
    def ptceHitPlayerWithOverride():
        global lineOfScene, displayingScene

        recoil = 0
        lineOfScene += 1
        skillAt = getFromName(displayingScene.theScene[lineOfScene],
        SkillsDatabase)
        holder = AttackCalc(monsterEncounter[CombatFunctionEnemytarget], player,  SkillsDatabase[skillAt], 1, True)
        finalDamage = holder[0]
        critText = holder[2]
        effectiveText = holder[5]
        recoil = holder[4]
        recoil =  int(math.floor(recoil))
        monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil
        player.stats.hp += holder[0]

    registerDialogueFunction(PTCE_PREFIX, "SaveMenu", ptceOpenSaveMenu)
    registerDialogueFunction(PTCE_PREFIX, "GivePerkFromInput", ptceGivePerkFromInput)
    registerDialogueFunction(PTCE_PREFIX, "GiveExpFromInput", ptceGiveExpFromInput)
    registerDialogueFunction(PTCE_PREFIX, "GiveErosFromInput", ptceGiveErosFromInput)
    registerDialogueFunction(PTCE_PREFIX, "ChangeFetish", ptceChangeFetishOverride, overrideVanilla=True)
    registerDialogueFunction(PTCE_PREFIX, "PermanentlyChangeFetish", ptcePermanentlyChangeFetishOverride, overrideVanilla=True)
    registerDialogueFunction(PTCE_PREFIX, "HitPlayerWith", ptceHitPlayerWithOverride, overrideVanilla=True)