init 1 python:
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

    def ptceChangeFetish():
        global lineOfScene, displayingScene, player
        FETISH_MAX_LEVEL = ptceConfig.get("fetishGain").get("fetishMaxLevel")
        lineOfScene += 1
        fetishName = displayingScene.theScene[lineOfScene]
        lineOfScene += 1
        amount = int(displayingScene.theScene[lineOfScene])
        fetish = player.getFetishObject(fetishName)
        fetish.increaseTemp(amount)
        level = fetish.Level
        if fetish.Type == "Fetish":
            if level >= FETISH_MAX_LEVEL:
                display = "Your fetish for " + fetishName +  " has become a complete and total obsession, but it can't get any worse than it is now...."
            else level < FETISH_MAX_LEVEL:
                if amount > 0:
                    if level - amount == 0:
                        display = "You have started getting a fetish for " + fetishName +  "..."
                    elif level - amount < 25 and level >= 25:
                        display = "You have acquired a fetish for " + fetishName +  "."
                    else:
                        display = "Your fetish for " + fetishName +  " has intensified!"
                elif amount < 0:
                    if level <= 0:
                        display = "You have lost your fetish for " + fetishName +  "."
                    else:
                        display = "Your fetish for " + fetishName +  " has receded."
            if amount != 0:
                renpy.say(None, display)
    
    def ptcePermanentlyChangeFetish():
        global lineOfScene, displayingScene, player
        FETISH_MAX_LEVEL = ptceConfig.get("fetishGain").get("fetishMaxLevel")
        lineOfScene += 1
        fetishName = displayingScene.theScene[lineOfScene]
        lineOfScene += 1
        amount = int(displayingScene.theScene[lineOfScene])
        fetish = player.getFetishObject(fetishName)
        fetish.increasePerm(amount)
        level = fetish.Level
        if fetish.Type == "Fetish":
            if level < FETISH_MAX_LEVEL:
                if amount >= 1:
                    if amount > 1:
                        display = "You {i}permanently{/i} gained " + str(amount) + " fetish levels for " + fetishName +  "..."
                    else:
                        display = "You have {i}permanently{/i} gained a fetish level for " + fetishName +  "."

                elif amount < 0:
                    amountLost = -amount
                    if amountLost > 1:
                        display = "You have {i}permanently{/i} lost " + str(amountLost) +" fetish levels for " + fetishName +  "."
                    else:
                        display = "You have {i}permanently{/i} lost a fetish level for " + fetishName +  "."
            if baseFetish > FETISH_MAX_LEVEL and amount >= 1:
                display = "Fantasies of " + fetishName +  " swirl through your mind, and your heart beats faster, you have {i}permanently{/i} gained a fetish level for " + fetishName + ", exceeding your normal obsession..."

            if (amount != 0):
                renpy.say(None, display)
    
    registerDialogueFunction("ptce", "SaveMenu", ptceOpenSaveMenu)
    registerDialogueFunction("ptce", "GivePerkFromInput", ptceGivePerkFromInput)
    registerDialogueFunction("ptce", "GiveExpFromInput", ptceGiveExpFromInput)
    registerDialogueFunction("ptce", "GiveErosFromInput", ptceGiveErosFromInput)
    registerDialogueFunction("ptce", "ChangeFetish", ptceChangeFetish)
    registerDialogueFunction("ptce", "PermanentlyChangeFetish", ptceChangeFetish)