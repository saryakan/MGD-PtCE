init python:
    def GetTreasureRarity(player, ChestRates = 0):
        treasureRarity = renpy.random.randint(0, 100)
        treasureRarity += player.stats.Luck*0.5

        bonusChance = 1

        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "TreasureFindChance":
                    bonusChance += (perk.EffectPower[p]*0.01)
                p += 1
        treasureRarity *= bonusChance

        if (treasureRarity <= 65-ChestRates):
            Rarity = "Common"
        elif (treasureRarity > 65-ChestRates and treasureRarity < 95-ChestRates):
            Rarity = "Uncommon"
        elif (treasureRarity >= 95-ChestRates):
            Rarity = "Rare"

        return Rarity

    def Resting(player):
        spiritRegained = 1
        energyRegained = 0.5
        arousalRegained = 0.5

        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "RestSpiritRestored":
                    spiritRegained += perk.EffectPower[p]
                if perk.PerkType[p] == "RestEnergyRestored":
                    energyRegained += (perk.EffectPower[p])*0.01
                if perk.PerkType[p] == "RestArousalRestored":
                    arousalRegained += (perk.EffectPower[p])*0.01
                p += 1
        player.stats.sp += spiritRegained
        player.stats.ep += int(math.floor(player.stats.max_true_ep*energyRegained))
        player.stats.hp -= int(math.floor(player.stats.max_true_hp*arousalRegained))
        player.stats.BarMinMax()

        return player

label Adventure:
    $ explorationDeck = []
    $ monsterDeck = []
    $ eventDeck = []
    $ QuestSlot = Event()
    $ index = 0
    $ tabToggle = 1
    $ questTaken = 0
    $ mapInteractable = True # Make sure the map works when it's added to the screen

    $ guaranteedEvents = {}

    show screen ON_MapMenu (_layer="master")
    hide screen ON_AdventureSetupMenu
    hide screen ON_HealthDisplayBacking
    hide screen ON_HealthDisplay
    #hide screen ON_MapMenu

    window hide dissolve
    #scene bg town
    pause
    jump Adventure


label RandomizeAdventure:

    $ explorationDeck = []
    $ monsterDeck = []
    $ eventDeck = []

    $ maxDeckSize = LocationDatabase[targetLocation].MaximumEventDeck + LocationDatabase[targetLocation].MaximumMonsterDeck
    $ minDeckSize = LocationDatabase[targetLocation].MinimumDeckSize
    $ MakeDeckSize = renpy.random.randint(minDeckSize, maxDeckSize)
    $ cardCycle = 1

    while MakeDeckSize > len(monsterDeck) + len(eventDeck):
        $ number = 0
        $ getCurrentCard = 0
        $ currentCard = 0
        $ cardSel = []



        if cardCycle == 1:
            $ cardSel = LocationDatabase[targetLocation].Monsters
            $ currentDeck = monsterDeck
            $ getCurrentCard = getFromName(cardSel[renpy.random.randint(0, len(cardSel)-1)], MonsterDatabase)
            $ currentCard = MonsterDatabase[getCurrentCard]
            $ currentMax = LocationDatabase[targetLocation].MaximumMonsterDeck
        if cardCycle == 2:
            $ cardSel = LocationDatabase[targetLocation].Events
            $ currentDeck = eventDeck
            $ getCurrentCard = getFromName(cardSel[renpy.random.randint(0, len(cardSel)-1)], EventDatabase)
            $ currentCard = EventDatabase[getCurrentCard]
            $ currentMax = LocationDatabase[targetLocation].MaximumEventDeck

        if (len(currentDeck) < currentMax):
            python:
                hasReq = 0
                hasReq = requiresCheck(currentCard.requires, currentCard.requiresEvent, player, ProgressEvent)

                if cardCycle == 2:
                    numberInDeck = 0
                    for cycle in currentDeck:
                        if cycle.name == currentCard.name:
                            numberInDeck += 1
                    if currentCard.CardLimit <= numberInDeck:
                        hasReq = 0
                    if ProgressEvent[getFromName(currentCard.name, EventDatabase)].questComplete == 1:
                        hasReq = 0

            if hasReq >= len(currentCard.requires) + len(currentCard.requiresEvent):
                $ i = 0
                $ currentDeck.append(currentCard)
                $ i+=1

        $ cardCycle +=1
        if cardCycle >= 3:
            $ cardCycle = 1


    jump AdventureSetUp

label AddToDeck:
    if (tabToggle == 1):
        $ monsterDeck.append(MonsterDatabase[getFromName(currentCardName, MonsterDatabase)])
    if (tabToggle == 2):
        $ eventDeck.append(EventDatabase[getFromName(currentCardName, EventDatabase)])
    if (tabToggle == 3):
        $ QuestSlot = EventDatabase[getFromName(currentCardName, EventDatabase)]

    jump AdventureSetUp

label RemoveFromDeck:
    $ i = 0
    if (tabToggle == 1):
        while i < len(monsterDeck):
            if monsterDeck[i].IDname == currentCardName:
                $ del monsterDeck[i]
                $ i = len(monsterDeck)
            $ i += 1
    if (tabToggle == 2):
        while i < len(eventDeck):
            if eventDeck[i].name == currentCardName:
                $ del eventDeck[i]
                $ i = len(eventDeck)
            $ i += 1
    if (tabToggle == 3):
        $ QuestSlot = Event()

    jump AdventureSetUp


label AdventureSetUp:
    python:
        renpy.hide_screen("ON_MapMenu", 'master')
    #hide screen ON_MapMenu

    if ptceConfig.get("adventuring").get("useVanilla"):
        show screen ON_AdventureSetupMenu
    else:
        show screen PtceAdventureSetupMenu

    $ bg = changeBG(LocationDatabase[targetLocation].picture)
    if bg != "":
        show screen DisplayBG (_layer="master")
    window hide dissolve
    pause
    jump AdventureSetUp

label AdventureEmbark:
    $ onAdventure = 1
    $ deckProgress = 0
    $ isEventNow = 0
    hide screen ON_AdventureSetupMenu
    $ explorationDeck = []
    $ AdventureHolder = []
    $ randomSelection = []

    $ getAdventure = getFromName(currentCardName, AdventureDatabase)
    $ AdventureHolder = AdventureDatabase[getAdventure]



    $ ao = 0
    while ao < len(AdventureHolder.deck):
        $ display = AdventureHolder.deck[ao]
        if AdventureHolder.deck[ao] == "Event":
            $ ao += 1
            $ explorationDeck.append(EventDatabase[getFromName(AdventureHolder.deck[ao], EventDatabase)])
        elif AdventureHolder.deck[ao] == "Monster":
            $ ao += 1
            $ treasureCard = Event("SpecificMon", "", "SpecificMon")
            $ explorationDeck.append(treasureCard)
            while AdventureHolder.deck[ao] != "EndLoop":
                $ explorationDeck.append(MonsterDatabase[getFromName(AdventureHolder.deck[ao], MonsterDatabase)])
                $ ao += 1
            $ treasureCard = Event("EndMon", "", "EndMon")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "RandomEvent":
            $ randomSelection = []
            python:
                for each in AdventureHolder.randomEvents:
                    if each != "":
                        randomSelection.append(each)
            $ renpy.random.shuffle(randomSelection)
            $ display = randomSelection[0]
            $ explorationDeck.append(EventDatabase[getFromName(display, EventDatabase)])
        elif AdventureHolder.deck[ao] == "RandomMonsters":
            $ randomSelection = []
            python:
                for each in AdventureHolder.randomMonsters:
                    if each != "":
                        randomSelection.append(each)
            $ renpy.random.shuffle(randomSelection)
            $ display = randomSelection[0]
            $ explorationDeck.append(MonsterDatabase[getFromName(display, MonsterDatabase)])
        elif AdventureHolder.deck[ao] == "RandomTreasure":
            $ Rarity = GetTreasureRarity(player)

            $ treasureCard = Event(Rarity, "", "Treasure")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "CommonTreasure":
            $ treasureCard = Event("Common", "", "Treasure")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "UncommonTreasure":
            $ treasureCard = Event("Uncommon", "", "Treasure")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "RareTreasure":
            $ treasureCard = Event("Rare", "", "Treasure")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "BreakSpot":
            $ treasureCard = Event("Break", "", "Break")
            $ explorationDeck.append(treasureCard)
        elif AdventureHolder.deck[ao] == "Unrepeatable":
            $ treasureCard = Event("Unrepeatable", "", "Unrepeatable")
            $ explorationDeck.append(treasureCard)
        $ ao += 1

    $ randomSelection = []

    $ display = len(explorationDeck)

    jump explore

label shuffleExploration:
    $ onAdventure = 0
    $ isEventNow = 0
    hide screen ON_AdventureSetupMenu
    $ explorationDeck = []
    $ i = 0
    $ deckProgress = 0
    while i < len(monsterDeck):
        $ explorationDeck.append(monsterDeck[i])
        $ i+=1
    $ i= 0
    while i < len(eventDeck):
        $ explorationDeck.append(eventDeck[i])
        $ i+=1
    $ i= 0

    $ preTreasureLength = len(explorationDeck)

    #add treasure encounters
    $ i = 0
    $ treasureCardCount = 0
    while i < 3:
        $ treasureRarity = (renpy.random.randint(0, 100) + player.stats.Luck*0.5) - (treasureCardCount)*15 + (i-treasureCardCount)*10

        $ bonusChance = 1
        python:
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "TreasureFindChance":
                        bonusChance += (perk.EffectPower[p]*0.01)
                    p += 1
        $ treasureRarity *= bonusChance

        if treasureRarity > 70:
            $ treasureCardCount += 1

        $ i+=1


    $ i = 0
    if treasureCardCount > 0:
        while i < treasureCardCount:
            $ Rarity = GetTreasureRarity(player)

            $ treasureCard = Event(Rarity, "", "Treasure")
            $ i += 1
            $ explorationDeck.append(treasureCard)

    $ renpy.random.shuffle(explorationDeck) #####################Shuffle the Deck###################

    $ e = 0
    $ placedRestSpots = 0
    $ avgRestPoints = float(preTreasureLength/3)
    $ avgRestPoints = renpy.random.randint(1, avgRestPoints)
    $ bufferRestPoint = renpy.random.randint(0, preTreasureLength/3)
    $ bufferRestPoint -= 1
    while e < len(explorationDeck):
        if e < len(explorationDeck)-1 and e > 2:
            if bufferRestPoint <= 0:
                if placedRestSpots <= avgRestPoints:
                    $ treasureCard = Event("Break", "", "Break")
                    $ explorationDeck.insert(e, treasureCard)
                    $ bufferRestPoint = renpy.random.randint(2, len(explorationDeck)/2)
            else:
                $ bufferRestPoint -= 1
        $ e += 1


    if QuestSlot.name == "": #END OF THE ADVENTURE! PUT A TREASURE CHEST THERE IF NO QUEST
        $ Rarity = GetTreasureRarity(player, 65)

        $ treasureCard = Event(Rarity, "", "Treasure")
        $ explorationDeck.append(treasureCard)
    else:
        $ treasureCard = Event("Break", "", "Break")
        $ explorationDeck.append(treasureCard)
        $ explorationDeck.append(QuestSlot)

    $ eventDeck = []

    jump explore

label eventDialogueMenu:


    $ displayingScene = EventDatabase[DataLocation].theEvents[currentChoice]

    if lineOfScene < len(displayingScene.theScene) and readLine == 1:
        $ booty = 0


    $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
    $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
    if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
        $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name

    call displayScene from _call_displayScene_2
    if len(monsterEncounter) > 0:
        return

    if TimeAdvancedCheck == 1:
        return
    jump postAdventureEvent

label explore:
    $ BGMlist = []
    python:
        for each in LocationDatabase[targetLocation].MusicList:
            BGMlist.append(each)

    if musicLastPlayed != BGMlist:
        $ musicLastPlayed = copy.deepcopy(BGMlist)
        $ renpy.random.shuffle(BGMlist)
        if renpy.music.get_playing(channel='music') != BGMlist[0]:
            play music BGMlist fadeout 1.0 fadein 1.0
    call EndAllEffects from _call_EndAllEffects_2

    $ e = 0 + deckProgress
    while e  < len(explorationDeck):


        $ breaktime = 0
        $ monsterEncounter = []
        hide screen ON_HealthDisplayBacking
        hide screen ON_HealthDisplay
        show screen ON_HealthDisplayBacking #(_layer="master")
        show screen ON_HealthDisplay #(_layer="master")
        $ RanAway = "False"
        $ SceneCharacters = []
        $ InventoryAvailable = False
        $ deckProgress += 1
        $ displayHealthInEvent = 1

        call statusStep from _call_statusStep_1
        $ renpy.set_return_stack([])

        if explorationDeck[e].CardType == "SpecificMon":
            $ HoldingSceneForCombat = ""
            $ HoldingLineForCombat = 0
            $ HoldingDataLocForCombat = ""
            $ runAndStayInEvent = 0
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            python:
                fightDeck = []
                e += 1
                deckProgress += 1
                while explorationDeck[e].CardType != "EndMon":
                    if explorationDeck[e].CardType == "Monster":
                        fightDeck.append(explorationDeck[e])
                    e += 1
                    deckProgress += 1

                renpy.random.shuffle(fightDeck)

                r = 0
                if len(fightDeck) > 0:
                    for each in fightDeck:
                        addMonsterTo(each.IDname, monsterEncounter)
                        addMonsterTo(each.IDname, trueMonsterEncounter)

                        r += 1

                    monsterEncounter = NumberMonsters(monsterEncounter)
            $ fightDeck = []
            call combat from _call_combat_2

        elif explorationDeck[e].CardType == "Monster":#IF MONSTER DRAWN
            $ HoldingSceneForCombat = ""
            $ HoldingLineForCombat = 0
            $ HoldingDataLocForCombat = ""
            $ runAndStayInEvent = 0
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            python:
                fightDeck = []
                if onAdventure == 0:
                    groupHolder = LocationDatabase[targetLocation].MonsterGroups
                    monsterEncounterList = monsterDeck
                else:
                    groupHolder = AdventureHolder.monsterGroups
                    monsterEncounterList = AdventureHolder.randomMonsters

                for each in groupHolder:
                    isActive = 0
                    isCard = 0
                    for mon in each:
                        M = 0
                        if explorationDeck[e].IDname == mon:
                            isCard = 1

                        while M < len(monsterEncounterList):
                            passing = 0
                            if onAdventure == 0:
                                if mon == monsterEncounterList[M].IDname:
                                    passing = 1
                            else:
                                if mon == monsterEncounterList[M]:
                                    passing = 1

                            if passing == 1:
                                    isActive += 1
                                    M =  len(monsterEncounterList)
                            M += 1
                    if isActive >= len(each) and isCard == 1:
                        fightDeck.append(each)

                renpy.random.shuffle(fightDeck)

                r = 0
                if len(fightDeck) > 0:
                    for each in fightDeck[0]:
                        addMonsterTo(each, monsterEncounter)
                        addMonsterTo(each, trueMonsterEncounter)

                        r += 1

                    monsterEncounter = NumberMonsters(monsterEncounter)
                else:
                    addMonsterTo(explorationDeck[e].IDname, monsterEncounter)
                    addMonsterTo(explorationDeck[e].IDname, trueMonsterEncounter)

            $ fightDeck = []
            call combat from _call_combat
        elif explorationDeck[e].CardType == "Event" or  explorationDeck[e].CardType == "Quest":
            $ currentEvent = e
            $ DialogueIsFrom= "Event"

            $ DataLocation = getFromName(explorationDeck[currentEvent].name, EventDatabase)
            $ displayingScene = explorationDeck[currentEvent].theEvents[0]
            $ actorNames[0] =  EventDatabase[DataLocation].Speakers[0].name
            $ ProgressEvent[DataLocation].timesSeen += 1
            call displayScene from _call_displayScene_3
            label postAdventureEvent:
                $ SceneCharacters = []
        elif explorationDeck[e].CardType == "Treasure":
            $ searchHere = 0
            $ numberFound = 0
            $ openable = 1
            if explorationDeck[e].name == "Common":
                show bag:
                    yalign 0.16
                    ypos 0.15
                    xalign 0.5
                $ searchHere = 0
                $ numberFound = renpy.random.randint(1, 3)
                $ openable = 0
                "You find some valuables."
            elif explorationDeck[e].name == "Uncommon":
                $ searchHere = 1
                $ numberFound = renpy.random.randint(1, 2)
                $ findChest = getFromName("Treasure Chest", MonsterDatabase)
                $ SceneCharacters.append(MonsterDatabase[findChest])

                "You find a wooden treasure chest!"

            elif explorationDeck[e].name == "Rare":
                $ searchHere = 2
                $ numberFound = 1
                $ findChest = getFromName("Treasure Chest Golden", MonsterDatabase)
                $ SceneCharacters.append(MonsterDatabase[findChest])
                "You find a large ornate golden treasure chest!"

            $ getTreasure = 1
            if openable == 1:
                menu openChest:
                    "Open the chest.":
                        $ getTreasure = 1
                        "You open the chest and..."
                        $ SceneCharacters = []
                        hide chest
                        hide bag
                    "Leave it be.":
                        $ getTreasure = 0
                        $ SceneCharacters = []
                        hide chest
                        hide bag
                        "You move on."

            if getTreasure == 1:
                if onAdventure == 0:
                    $ datahere = LocationDatabase[targetLocation]
                else:
                    $ datahere = AdventureHolder

                $ treasureFound = renpy.random.randint(0, len(datahere.Treasure[searchHere]) - 1)
                $ erosFound = datahere.Eros[searchHere]

                $ bonusMoney = 100
                python:
                    for perk in attacker.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "ErosBoost":
                                bonusMoney += perk.EffectPower[p]
                            p += 1

                $ erosFound *= (bonusMoney*0.01)
                $ erosFound *= (renpy.random.randint(75, 125)*0.01)
                $ erosFound *= (player.stats.Luck*0.01 + 1)
                $ erosFound =  int(math.floor(erosFound))

                $ numberFoundDis = ""
                $ pluralS = ""
                if numberFound > 1:
                    $ numberFoundDis = str(numberFound) + " "
                    $ pluralS = "s"
                if datahere.Treasure[searchHere][treasureFound] == "":
                    $ display = "You plunder " + str(erosFound) + " Eros!"
                else:
                    $ display = "You acquire " + numberFoundDis + datahere.Treasure[searchHere][treasureFound] + pluralS + "!"
                    $ display += "\nYou also plunder " + str(erosFound) + " Eros!"
                "[display]"
                hide bag

                $ player.inventory.earn(erosFound)
                if datahere.Treasure[searchHere][treasureFound] != "":
                    $ player.inventory.give(datahere.Treasure[searchHere][treasureFound], numberFound)
        elif explorationDeck[e].CardType == "Break":
            hide screen ON_HealthDisplayBacking
            hide screen ON_HealthDisplay
            show screen ON_HealthDisplayBacking #(_layer="master")
            show screen ON_HealthDisplay #(_layer="master")
            $ InventoryAvailable = True
            "You find a place to rest!\nDon't forget to use your inventory while you can!"

            menu AdventureMenu:
                "Continue onwards!":
                    "You press forward."
                "Rest. (Advances Time 1)":
                    "You take a moment to rest..."
                    call advanceTime(TimeIncrease=1) from _call_advanceTime
                    $ player = Resting(player)

                    "And you recover your strength!"

                "Return to town.":
                    "You return to town."
                    jump returnToTown
        elif explorationDeck[e].CardType == "Unrepeatable":
            $ ensureChange =  getFromName(AdventureHolder.name, ProgressAdventure)
            $ ProgressAdventure[ensureChange].questComplete = 1

        $ e += 1

        $ BGMlist = []
        python:
            for each in LocationDatabase[targetLocation].MusicList:
                BGMlist.append(each)
        if musicLastPlayed != BGMlist:
            $ musicLastPlayed = copy.deepcopy(BGMlist)
            $ renpy.random.shuffle(BGMlist)

            if renpy.music.get_playing(channel='music') != BGMlist[0]:
                play music BGMlist fadeout 1.0 fadein 1.0

        call EndAllEffects from _call_EndAllEffects_3





        if e > 0 and e < len(explorationDeck):
            hide screen ON_HealthDisplayBacking
            hide screen ON_HealthDisplay
            show screen ON_HealthDisplayBacking #(_layer="master")
            show screen ON_HealthDisplay #(_layer="master")
            $ InventoryAvailable = True
            "You continue on your adventure.\nYou can access your inventory!"


    "You return to town."
    jump returnToTown



label statusStep:
    #$ test = len(renpy.get_return_stack())
    #$ testList = renpy.get_return_stack()
    #$ test = testList[-1]
    #"[test]"
    if(player.statusEffects.aphrodisiac.duration > 0):
        $ player = applyPoison(player)
        $ Speaker = Character(_(''))
        if onGridMap == 0:
            $ display = "Aphrodisiac courses through {ThePlayerName}, {ThePlayerName} was aroused by {FinalDamage}!"
            call read from _call_read_18
        else:
            $ gridStepLine +="Aphrodisiac courses through {ThePlayerName}, {ThePlayerName} was aroused by {FinalDamage}!"
        $ player.statusEffects.turnPass(player)
        $ holda = player.statusEffects.statusEnd(player)
        $ display = holda[0]
        $ player = holda[1]
        python:
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "AphrodisiacTurnCure":
                        player.statusEffects.aphrodisiac.potency -= perk.EffectPower[p]
                        if player.statusEffects.aphrodisiac.potency <= 0:
                            player.statusEffects.aphrodisiac.potency = 0
                    p += 1

    if(player.statusEffects.trance.duration > 0):
        $ player.statusEffects.trance.potency -= 1
        if player.statusEffects.trance.potency <= 0:
            $ player.statusEffects.trance.duration = 0
            if onGridMap == 0:
                $ display = "The hypnotic effects on {ThePlayerName} have worn off!"
                call read from _call_read_51
            else:
                if gridStepLine != "":
                    $ gridStepLine += " "
                $ gridStepLine +="The hypnotic effects on {ThePlayerName} have worn off!"


    if(player.statusEffects.paralysis.duration > 0):
        $ player.statusEffects.paralysis.potency -= 1
        if player.statusEffects.paralysis.potency <= 0:
            $ player.statusEffects.paralysis.duration = 0
            if onGridMap == 0:
                $ display = "The paralysis effecting {ThePlayerName} has faded away!"
                call read from _call_read_53
            else:
                if gridStepLine != "":
                    $ gridStepLine += " "
                $ gridStepLine +="The paralysis effecting {ThePlayerName} has faded away!"


    $ DialogueIsFrom = "Event"
    call PerkTimers(TimerType="TurnDuration", targetedCharacter=player) from _call_PerkTimers
    call TimeEvent(CardType="StepTaken", LoopedList=StepTakenList) from _call_TimeEvent_1

    $ timeNotify = 0
    call advanceTime(TimeIncrease=0) from _call_advanceTime_8


    return
