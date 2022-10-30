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

    
    registerDialogueFunction("ptce", "SaveMenu", ptceOpenSaveMenu)
    registerDialogueFunction("ptce", "GivePerkFromInput", ptceGivePerkFromInput)
    registerDialogueFunction("ptce", "GiveExpFromInput", ptceGiveExpFromInput)
    registerDialogueFunction("ptce", "GiveErosFromInput", ptceGiveErosFromInput)