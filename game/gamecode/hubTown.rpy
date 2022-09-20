
label advanceTime(TimeIncrease):
    $ HealingSickness -= 1
    while TimeIncrease >= 1:

        if TimeOfDay == Morning:
            $ TimeOfDay = Noon
        elif TimeOfDay == Noon:
            $ TimeOfDay = Afternoon
        elif TimeOfDay == Afternoon:
            $ TimeOfDay = Dusk
            $ bg =  bgToNightDay(bg, ".png", "Night.png")

        #check if sudo night is happening and move forward
        elif TimeOfDay == MorningNight:
            $ TimeOfDay = NoonNight
            $ bg =  bgToNightDay(bg, ".png", "Night.png")
        elif TimeOfDay == NoonNight:
            $ TimeOfDay = AfternoonNight
            $ bg =  bgToNightDay(bg, ".png", "Night.png")
        elif TimeOfDay == AfternoonNight:
            $ TimeOfDay = Dusk
            $ bg =  bgToNightDay(bg, ".png", "Night.png")

        #move onto actual night.
        elif TimeOfDay == Dusk or TimeOfDay == DuskDay:
            $ TimeOfDay = Evening
        elif TimeOfDay == Evening or TimeOfDay == EveningDay:
            $ TimeOfDay = Midnight
        elif TimeOfDay == Midnight or TimeOfDay == MidnightDay:
            $ TimeOfDay = Morning
            $ DayNumber += 1
            $ bg = bgToNightDay(bg, "Night.png", ".png")
            call TimeEvent(CardType="EndOfDay", LoopedList=EndOfDayList) from _call_TimeEvent_6
        call TimeEvent(CardType="TimePassed", LoopedList=TimePassedList) from _call_TimeEvent_7
        call PerkTimers(TimerType="TimeDuration", targetedCharacter=player) from _call_PerkTimers_2

        $ TimeIncrease -= 1
    call PerkTimers(TimerType="TimeDuration", targetedCharacter=player, durDown=0) from _call_PerkTimers_4
    $ timeNotify = 0
    return



label PerkTimers(TimerType, targetedCharacter, durDown=1):
    $ displayList = []
    python:
        perksToCheck = copy.deepcopy(targetedCharacter.perks)
        tp = 0
        for perk in perksToCheck:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "TimeDuration" or perk.PerkType[p] == "TurnDuration":
                    if perk.PerkType[p] == TimerType:
                        if perk.duration > 0:
                            targetedCharacter.perks[tp].duration -= durDown
                            perk.duration -= durDown
                    if perk.duration <= 0 and timeNotify == 0:
                        targetedCharacter.giveOrTakePerk(perk.name, -1)
                        tp -= 1


                if perk.PerkType[p] == "EndMessage" and perk.duration == 0 and timeNotify == 0:
                    displayList.append(perk.EffectPower[p])
                p += 1
            tp +=1

    $ player.stats.BarMinMax()

    $ p = 0
    while p < len(displayList):
        $ display = returnReaderDiction(displayList[p])
        "[display]"
        $ p += 1
    return

label TimeEvent(CardType, LoopedList):
    $ TimeAdvancedCheckArray.append(1)
    $ tei = 0

    $ lastTimeReturnArray.append(copy.deepcopy(renpy.get_return_stack()))
    if DataLocation != 0:
        $ HoldingSceneForTimeArray.append(copy.deepcopy(displayingScene))
        $ HoldingLineForTimeArray.append(copy.deepcopy(lineOfScene))
        $ HoldingDataLocForTimeArray.append(copy.deepcopy(DataLocation))
    $ holdActorsArray.append(copy.deepcopy(actorNames))
    $ DialogueTypeHolderArray.append(copy.deepcopy(DialogueIsFrom))

    $ currentChoice = copy.deepcopy(specifyCurrentChoice)

    if LoopedListHolder == []:
        $ LoopedListHolder.append(copy.deepcopy(LoopedList))
        $ holdChoiceForLoop.append(copy.deepcopy(currentChoice))
    if teiHold != -1:
        $ callLoopTei.append(copy.deepcopy(teiHold))

    $ dontJumpOutOfGridEvents = 1
    if EnteringLocationCheck == 1:
        $ EnteringLocationCheck = 2

    while tei < len(LoopedList):
        $ hasReq = 0
        $ DialogueIsFrom = "NPC"
        if LoopedList[tei].CardType == CardType or CardType == "Any":
            $ isEventNow = 1
            $ currentChoice = copy.deepcopy(specifyCurrentChoice)
            $ specifyCurrentChoice = 0
            $ DataLocation = getFromName(LoopedList[tei].name, EventDatabase)
            $ teiHold = copy.deepcopy(tei)
            call sortMenuD from _call_sortMenuD_81

        label postTimeAdvancedEvent:
            $ tei += 1

    $ notFunction = 0
    $ readLine = 0

    if EnteringLocationCheck == 2:
        $ EnteringLocationCheck = 1

    if len(holdActorsArray) > 0:
        $ actorNames = copy.deepcopy(holdActorsArray[-1])
        $ del holdActorsArray[-1]
    if len(DialogueTypeHolderArray) > 0:
        $ DialogueIsFrom = copy.deepcopy(DialogueTypeHolderArray[-1])
        $ del DialogueTypeHolderArray[-1]
    if len(HoldingDataLocForTimeArray) > 0:
        if HoldingDataLocForTimeArray[-1] != 0:
            $ displayingScene = copy.deepcopy(HoldingSceneForTimeArray[-1])
            $ lineOfScene = copy.deepcopy(HoldingLineForTimeArray[-1])
            $ DataLocation = copy.deepcopy(HoldingDataLocForTimeArray[-1])
            $ del HoldingSceneForTimeArray[-1]
            $ del HoldingLineForTimeArray[-1]
            $ del HoldingDataLocForTimeArray[-1]
    if len(lastTimeReturnArray) > 0 and len(monsterEncounter) == 0:
        $ renpy.set_return_stack(copy.deepcopy(lastTimeReturnArray[-1]))
        $ del lastTimeReturnArray[-1]


    $ del TimeAdvancedCheckArray[-1]
    if len(TimeAdvancedCheckArray) <= 0:
        $ TimeAdvancedCheckArray = [0]

    if len(callLoopTei) > 0 :
        $ tei = copy.deepcopy(callLoopTei[-1])
        $ teiHold = -1
        if len(LoopedListHolder) > 0:
            $ LoopedList = copy.deepcopy(LoopedListHolder[-1])
            $ del LoopedListHolder[-1]
        if len(holdChoiceForLoop) > 0:
            $ currentChoice = copy.deepcopy(holdChoiceForLoop[-1])
            $ del holdChoiceForLoop[-1]
        $ CardType = "Any"
        #$ currentChoice =  getFromNameOfScene(displayingScene.NameOfScene, EventDatabase[DataLocation].theEvents)
        if TimeAdvancedCheckArray == [0]:
            $ dontJumpOutOfGridEvents = 0
        return

    $ dontJumpOutOfGridEvents = 0
    $ teiHold = -1
    $ LoopedListHolder = []
    $ LoopedList = []
    $ callLoopTei = []


    return

label returnToTown:
    if TimeOfDay == MorningNight:
        $ TimeOfDay = Morning
        $ bg = bgToNightDay(bg, "Night.png", ".png")
    elif TimeOfDay == NoonNight:
        $ TimeOfDay = Noon
        $ bg = bgToNightDay(bg, "Night.png", ".png")
    elif TimeOfDay == AfternoonNight:
        $ TimeOfDay = Afternoon
        $ bg = bgToNightDay(bg, "Night.png", ".png")
    elif TimeOfDay == DuskDay:
        $ TimeOfDay = Dusk
        $ bg = bgToNightDay(bg, ".png", "Night.png")
    elif TimeOfDay == EveningDay:
        $ TimeOfDay = Evening
        $ bg = bgToNightDay(bg, ".png", "Night.png")
    elif TimeOfDay == MidnightDay:
        $ TimeOfDay = Midnight
        $ bg = bgToNightDay(bg, ".png", "Night.png")

    call advanceTime(TimeIncrease=1) from _call_advanceTime_5

label Town:
    hide screen ON_HealthDisplayBacking
    hide screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking #(_layer="hplayer")
    show screen ON_HealthDisplay #(_layer="sayScreen")

    $ InventoryAvailable = True
    $ currentLocation = "TownSquare"

    python:
        renpy.hide_screen("ON_MapMenu", 'master')

    hide screen CharacterDialogueScreen

    $ bg = changeBG("town.png")

    hide screen ON_CharacterDialogueScreen
    show screen DisplayBG (_layer="master")
    show screen ON_CharacterDialogueScreen (_layer="master")
    hide screen FetPageButtons

    #call advanceTime(TimeIncrease=1)
    python:
        try:
            difficulty = difficulty
        except:
            difficulty = "Normal"


    $ player = player.statusEffects.refresh(player)
    #$ player.stats.refresh()
    $ npcCount = 0
    $ senCount = 0
    $ fetCount = 0

    $ inventoryETarget = 0
    $ inventoryTarget = 0

    #clear out varibles
    $ EnteringLocationCheck = 0
    $ SceneCharacters = []
    $ explorationDeck = []
    $ monsterDeck = []
    $ eventDeck = []
    $ AdventureHolder = []
    $ currentDeck = []
    $ displayingScene = []
    $ callNextJump = 0
    $ inCalledSceneJump = 0
    $ LootDrops = []
    $ counterArray = []
    $ showing = ""
    $ menuArray = []
    $ monSkillChoice = []
    $ EventConsister = ""
    $ DefeatedEncounterMonsters = []
    $ player.clearStance()
    $ tt = Tooltip("")
    $ StoredScene = ""
    $ StoredLine = 0
    $ StoredDataLoc = ""
    $ hidingCombatEncounter = 0
    $ renpy.set_return_stack([])
    #$ renpy.free_memory()
    $ runAndStayInEvent = 0
    $ victoryScene = 0
    $ inChurch = 0
    $ cmenu_tooltip = ""
    $ specifyCurrentChoice = 0

    $ HoldingSceneForTimeArray = []
    $ HoldingLineForTimeArray = []
    $ HoldingDataLocForTimeArray = []
    $ HoldingSceneForCombat = []
    $ HoldingLineForCombat = []
    $ HoldingDataLocForCombat = []
    $ HoldingSceneCA = []
    $ HoldingLineCA = []
    $ HoldingDataLocCA = []
    $ TimeAdvancedCheckArray = [0]
    $ lastTimeReturnArray = []

    $ removedSkillPosition = []
    $ removedSkill = []
    $ onGridMap = 0
    hide screen Gridmap
    hide screen GridmapPlayer
    hide screen GridmapNPCs
    hide screen GridmapObstacles
    $ TheGrid = []

    $ MenuLineSceneCheckMark = -1

    $ needToUpdate = 0
    $ SkillDatabase = []

    #$ renpy.profile_memory(0.75)

    call checkData from _call_checkData

    $ BGMlist = []
    $ BGMlist.append("music/Town/mati.mp3")
    $ BGMlist.append("music/Town/village.mp3")
    $ BGMlist.append("music/Town/Walk with two people.mp3")

    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.5 fadein 1.5

    $ inTownMenu = 1
    $ isEventNow = 0
    menu townMenu:
        "You stand in the center of the town square, deciding what to do next. Humans and monster girls bustle about, minding their own business."
        "Go Adventuring!":
            $ inTownMenu = 0
            $ EventConsister = ""
            call checkData from _call_checkData_1
            jump Adventure
        "Go to the Shopping District.":
            $ inTownMenu = 0
            call checkData from _call_checkData_2
            jump Shop
        "Go to the Adventurers' Guild.":
            $ inTownMenu = 0
            call checkData from _call_checkData_3
            jump Guild
        "Go to the \"Goddess' Embrace Inn♥\".":
            $ inTownMenu = 0
            call checkData from _call_checkData_4
            jump Inn
        "Go to the Church.":
            $ inTownMenu = 0
            call checkData from _call_checkData_5
            jump Church
    jump Town


label Church:
    $ BGMlist = []
    $ BGMlist.append("music/Town/Holy night.mp3")
    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0

    $ bg = changeBG("Church.png")
    $ currentLocation = "Church"
    call EnterTownLocation from _call_EnterTownLocation
    #call NpcDisplay from _call_NpcDisplay


label Inn:
    $ BGMlist = []
    $ BGMlist.append("music/Town/casino.mp3")
    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0


    $ bg = changeBG("Inn.png")
    $ currentLocation = "Inn"


    call EnterTownLocation from _call_EnterTownLocation_1

label Guild:
    $ BGMlist = []
    $ BGMlist.append("music/Town/tea-time.mp3")
    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0

    $ bg = changeBG("Guild.png")
    $ currentLocation = "Guild"
    call EnterTownLocation from _call_EnterTownLocation_2

label Shop:
    $ BGMlist = []
    $ BGMlist.append("music/Town/unknown.mp3")
    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0

    $ currentLocation = "Shopping"
    call EnterTownLocation from _call_EnterTownLocation_3

label LeaveBuilding:
    $ LocationCurrentList = []
    jump Town




label RestoreSensitivity:
    $ index = 0
    $ costPerSensitivity = 20

    label getSensPage:
        $ theCost =0

        $ sensList = []

        $ i = index
        $ display1 = ""
        $ display2 = ""
        $ display3 = ""
        $ display4 = ""

        $ d1Cost = 0
        $ d2Cost = 0
        $ d3Cost = 0
        $ d4Cost = 0

        $ d1Name = ""
        $ d2Name = ""
        $ d3Name = ""
        $ d4Name = ""


        $ sensList = ["Sex", "Ass", "Breasts", "Mouth", "Seduction", "Magic", "Pain", "Holy", "Unholy"]
        $ senCount = 0
        python:
            for each in sensList:
                if TempSensitivity.getRes(each)*costPerSensitivity > 0:
                    senCount += 1
                    theCost += TempSensitivity.getRes(each)*costPerSensitivity


        while  len(sensList) > i:
            if TempSensitivity.getRes(sensList[i])*costPerSensitivity > 0:

                $ display = TempSensitivity.getResPName(sensList[i]) + ": " + str(TempSensitivity.getRes(sensList[i])*costPerSensitivity) + " eros."

                if display1 == "" and TempSensitivity.getRes(sensList[i]) > 0:
                    $ display1 = display
                    $ d1Name = copy.deepcopy(sensList[i])
                    $ d1Cost = TempSensitivity.getRes(sensList[i])*costPerSensitivity
                elif display2 == "" and TempSensitivity.getRes(sensList[i]) > 0:
                    $ display2 = display
                    $ d2Name = copy.deepcopy(sensList[i])
                    $ d2Cost = TempSensitivity.getRes(sensList[i])*costPerSensitivity
                elif display3 == "" and TempSensitivity.getRes(sensList[i]) > 0:
                    $ display3 = display
                    $ d3Name = copy.deepcopy(sensList[i])
                    $ d3Cost = TempSensitivity.getRes(sensList[i])*costPerSensitivity
                elif display4 == "" and TempSensitivity.getRes(sensList[i]) > 0:
                    $ display4 = display
                    $ d4Name = copy.deepcopy(sensList[i])
                    $ d4Cost = TempSensitivity.getRes(sensList[i])*costPerSensitivity
            $ i+= 1



    if theCost > 0:
        if senCount > 4:
            show screen SenPageButtons
        else:
            hide screen SenPageButtons
        window hide
        $ Speaker = Goddess
        $ LastLine = "Oh, chosen hero... What do you need restored? With a donation of eros, I can remove the effects on your body from your losses."
        show screen fakeTextBox

        menu resPicker:
            "[display1]" if display1 != "":
                if player.inventory.money >= d1Cost:
                    $ senCount = 0
                    $ theCost = d1Cost
                    $ player.BodySensitivity.changeRes(d1Name, -TempSensitivity.getRes(d1Name))
                    $ TempSensitivity.setRes(d1Name, 0)
                    jump payRes
                else:
                    jump lackOfMoneyGoddess
            "[display2]" if display2 != "":
                if player.inventory.money >= d2Cost:
                    $ senCount = 0
                    $ theCost = d2Cost
                    $ player.BodySensitivity.changeRes(d2Name, -TempSensitivity.getRes(d2Name))
                    $ TempSensitivity.setRes(d2Name, 0)
                    jump payRes
                else:
                    jump lackOfMoneyGoddess
            "[display3]" if display3 != "":
                if player.inventory.money >= d3Cost:
                    $ senCount = 0
                    $ theCost = d3Cost
                    $ player.BodySensitivity.changeRes(d3Name, -TempSensitivity.getRes(d3Name))
                    $ TempSensitivity.setRes(d3Name, 0)
                    jump payRes
                else:
                    jump lackOfMoneyGoddess
            "[display4]" if display4 != "":
                if player.inventory.money >= d4Cost:
                    $ senCount = 0
                    $ theCost = d4Cost
                    $ player.BodySensitivity.changeRes(d4Name, -TempSensitivity.getRes(d4Name))
                    $ TempSensitivity.setRes(d4Name, 0)
                    jump payRes
                else:
                    jump lackOfMoneyGoddess
            "All: [theCost] eros.":
                $ senCount = 0
                if  player.inventory.money >= theCost:
                    jump payAllRes
                else:
                    jump lackOfMoneyGoddess
            "Done.":
                $ senCount = 0
                hide screen SenPageButtons
                hide screen fakeTextBox
                return

        label payAllRes:
            $ player.BodySensitivity.changeRes("Sex", -TempSensitivity.Sex)
            $ player.BodySensitivity.changeRes ("Ass", -TempSensitivity.Ass)
            $ player.BodySensitivity.changeRes ("Breasts", -TempSensitivity.Breasts)
            $ player.BodySensitivity.changeRes ("Mouth", -TempSensitivity.Mouth)
            $ player.BodySensitivity.changeRes ("Seduction", -TempSensitivity.Seduction)
            $ player.BodySensitivity.changeRes ("Magic", -TempSensitivity.Magic)
            $ player.BodySensitivity.changeRes ("Pain", -TempSensitivity.Pain)
            $ player.BodySensitivity.changeRes ("Holy", -TempSensitivity.Holy)
            $ player.BodySensitivity.changeRes ("Unholy", -TempSensitivity.Unholy)

            $ TempSensitivity.resetTempRes ()

        label payRes:
            $ player.inventory.money -= theCost
            $ tribute += theCost*0.1
            hide screen SenPageButtons
            hide screen fakeTextBox
            $ theCost = 0
            "You dump eros into the donation cup and they disappear instantly."
            "A chill runs through your body as it returns to its normal sensitivity."

    else:
        Goddess "Oh, chosen hero... Your body is not in need of restoration, but you may still donate if you wish."
        return

    jump RestoreSensitivity

label PurgeFetishes:

    $ index = 0

    $ costPerFetish = ptceConfig["ptceTempFetishCost"]
    $ playerFetishes = player.getAllFetishes()
    $ purgeableFetishes = filter(lambda f: f.getPurgeableAmount > 0, playerFetishes)

    label getFetPage:
        $ theTotalCost = 0
        $ i = index
        $ display1 = ""
        $ display2 = ""
        $ display3 = ""
        $ display4 = ""

        $ d1Cost = 0
        $ d2Cost = 0
        $ d3Cost = 0
        $ d4Cost = 0

        $ d1Name = ""
        $ d2Name = ""
        $ d3Name = ""
        $ d4Name = ""

        $ theCost = 0
        
        $ playerFetishes = player.getAllFetishes()
        $ purgeableFetishes = filter(lambda f: f.getPurgeableAmount > 0, playerFetishes)

        $ fetCount = len(purgeableFetishes)

    $ c = 0
    while c < len(purgeableFetishes):
        if c < len(purgeableFetishes):
            $ theTotalCost += purgeableFetishes[c].getPurgeableAmount()*costPerFetish
        $ c += 1


    while i < len(purgeableFetishes):
        if i < len(purgeableFetishes):
            $ theCost += purgeableFetishes[i].getPurgeableAmount()*costPerFetish

            $ display = purgeableFetishes[i].name + ": " + str(purgeableFetishes[i].getPurgeableAmount()*costPerFetish) + " eros."

            if display1 == "" and purgeableFetishes[i].getPurgeableAmount()*costPerFetish > 0:
                $ display1 = display
                $ d1Name = purgeableFetishes[i].name
                $ d1Cost = purgeableFetishes[i].getPurgeableAmount()*costPerFetish
            elif display2 == "" and purgeableFetishes[i].getPurgeableAmount()*costPerFetish > 0:
                $ display2 = display
                $ d2Name = purgeableFetishes[i].name
                $ d2Cost = purgeableFetishes[i].getPurgeableAmount()*costPerFetish
            elif display3 == "" and purgeableFetishes[i].getPurgeableAmount()*costPerFetish > 0:
                $ display3 = display
                $ d3Name = purgeableFetishes[i].name
                $ d3Cost = purgeableFetishes[i].getPurgeableAmount()*costPerFetish
            elif display4 == "" and purgeableFetishes[i].getPurgeableAmount()*costPerFetish > 0:
                $ display4 = display
                $ d4Name = purgeableFetishes[i].name
                $ d4Cost = purgeableFetishes[i].getPurgeableAmount()*costPerFetish
        $ i += 1

    if theCost > 0:
        if fetCount > 4:
            show screen FetPageButtons
        else:
            hide screen FetPageButtons
        window hide
        $ Speaker = Goddess
        $ LastLine = "Oh chosen hero... If you donate enough eros, I can remove the fetishes you have gained from your trials."
        show screen fakeTextBox

        menu fetPicker:
            "[display1]" if display1 != "":
                if player.inventory.money >= d1Cost:
                    $ theCost = d1Cost
                    $ player.getFetishObject(d1Name).resetTemp()
                    $ fetCount = 0
                    jump payFet
                else:
                    jump lackOfMoneyGoddess
            "[display2]" if display2 != "":
                if player.inventory.money >= d2Cost:
                    $ theCost = d2Cost
                    $ player.getFetishObject(d2Name).resetTemp()
                    $ fetCount = 0
                    jump payFet
                else:
                    jump lackOfMoneyGoddess
            "[display3]" if display3 != "":
                if player.inventory.money >= d3Cost:
                    $ theCost = d3Cost
                    $ player.getFetishObject(d3Name).resetTemp()
                    $ fetCount = 0
                    jump payFet
                else:
                    jump lackOfMoneyGoddess
            "[display4]" if display4 != "":
                if player.inventory.money >= d4Cost:
                    $ theCost = d4Cost
                    $ player.getFetishObject(d4Name).resetTemp()
                    $ fetCount = 0
                    jump payFet
                else:
                    jump lackOfMoneyGoddess

            "All: [theTotalCost] eros.":
                $ fetCount = 0
                if  player.inventory.money >= theTotalCost:
                    jump payAllFet
                else:
                    jump lackOfMoneyGoddess
            "Leave":
                $ fetCount = 0
                hide screen FetPageButtons
                hide screen fakeTextBox
                "You change your mind and leave."
                return

        label payAllFet:
            $ i = 0
            while i < len(player.FetishList):
                $ player.FetishList[i].resetTemp()
                $ i += 1
            $ theCost = theTotalCost

        label payFet:
            $ player.inventory.money -= theCost
            $ tribute += theCost*0.1
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ theCost =0
            "You dump eros into the donation cup and they disappear instantly."
            "A chill runs through your skull as your fantasies return to normal."

            $ i = 0

    else:
        Goddess "Oh, chosen hero... Your mind is as pure as it can be, but you may still donate if you wish."
        return

    $ i = 0
    while i < len(player.FetishList):
        if  player.FetishList[i].Level < 0:
            $ player.FetishList[i].Level = 0
        $ i += 1

    jump PurgeFetishes

label lackOfMoneyGoddess:
    hide screen FetPageButtons
    hide screen SenPageButtons
    hide screen fakeTextBox
    $ fetCount = 0
    $ senCount = 0
    Goddess "Oh, chosen hero... It seems you don't have enough eros. I believe in you to get some so I may aid you."
    return

label nextFetPage:
    $ index += 4
    if index >=  fetCount:
        $ index = 0
    jump getFetPage

label lastFetPage:
    $ index -= 4
    if index < 0:
        $ index = 0

        $ index = fetCount/4
        $ index = math.floor(index)
        $ index = index*4
        $ index = math.floor(index)
        #$ b =  fetCount - index
        #$ index = index + b
        $ index = int(index)

    jump getFetPage

label nextSenPage:
    $ index += 4
    if index >=  senCount:
        $ index = 0
    jump getSensPage

label lastSenPage:
    $ index -= 4
    if index < 0:
        $ index = 0

        $ index = senCount/4
        $ index = math.floor(index)
        $ index = index*4
        $ index = math.floor(index)
        #$ b =  fetCount - index
        #$ index = index + b
        $ index = int(index)

    jump getSensPage

label DonateToGoddess:
    $ donateStr = renpy.input(_("How much do you want to donate?"), length=20) or _("0")
    python:
        try:
            DonatePayment = int(donateStr)
        except ValueError:
            DonatePayment = 0

    if DonatePayment <= 0:
        "You change your mind about the donation."
    elif DonatePayment > player.inventory.money:
        "You don't have that many eros."
    else:
        $ player.inventory.money -= DonatePayment
        $ tribute += DonatePayment
        "You donate [DonatePayment] eros."

    return

label InputProgress:
    $ LastLine = returnReaderDiction(LastLine)

    $ DebtString = renpy.input(_(LastLine), length=20) or _("0")
    python:
        try:
            debt = int(DebtString)
        except ValueError:
            debt = 0
    return
