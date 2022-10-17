init python:
    def isMaxEventsChosen():
        global guaranteedEvents, ptceConfig
        return len(guaranteedEvents) >= ptceConfig.get("adventuring").get("maxEventsToChoose")

    def toggleQuest(card):
        global QuestSlot
        QuestSlot = Event() if QuestSlot.name == card.name else card        
        renpy.jump("AdventureSetUp")

    def toggleEvent(card):
        global guaranteedEvents, ptceConfig
        if card.name in guaranteedEvents.keys():
            guaranteedEvents.pop(card.name)
        else:
            if(not isMaxEventsChosen()):
                guaranteedEvents[card.name] = card

        renpy.jump("AdventureSetUp")
    
    def returnFromAdventureMenu():
        renpy.hide_screen("PtceAdventureSetupMenu")
        renpy.jump("Adventure")

    def embarkOnAdventure(location):
        global guaranteedEvents, explorationDeck, QuestSlot, onAdventure, isEventNow, deckProgress
        onAdventure = 0
        isEventNow = 0
        deckProgress = 0
        explorationDeck = prepareExplorationDeck(location, guaranteedEvents)
        preTreasureCount = len(explorationDeck)
        addTreasures(explorationDeck)
        renpy.random.shuffle(explorationDeck)
        placeRestPoints(explorationDeck, preTreasureCount)
        if QuestSlot == None or QuestSlot.name == "":
            explorationDeck.append(Event(GetTreasureRarity(player, 65), "", "Treasure"))
        else:
            explorationDeck.append(Event("Break", "", "Break"))
            explorationDeck.append(QuestSlot)
        
        renpy.hide_screen("PtceAdventureSetupMenu")
        renpy.jump("explore")
        

    def placeRestPoints(explorationDeck, preTreasureCount):
        avgRestPoints = renpy.random.randint(1, float(preTreasureCount/3))
        bufferRestPoint = renpy.random.randint(0, preTreasureCount/3) -1
        placedRestSpots = 0
        i = 0
        while i < len(explorationDeck):
            # only add when not first or last card
            if i < len(explorationDeck) - 1 and i > 2:
                if bufferRestPoint <= 0:
                    if placedRestSpots <= avgRestPoints:
                        explorationDeck.insert(i, Event("Break", "", "Break"))
                        bufferRestPoint = renpy.random.randint(2, len(explorationDeck)/2)
                else:
                    bufferRestPoint -= 1
            i += 1

    def addTreasures(explorationDeck):
        perkModifier = 1 + getSumOfPerkPower(player.perks, "TreasureFindChance")*0.01
        treasureCount = 0
        missedRolls = 0
        for _ in range(1, 3):
            roll = treasureCardRoll(treasureCount, missedRolls) * perkModifier
            if roll > 70:
                treasureCount += 1
                explorationDeck.append(Event(GetTreasureRarity(player), "", "Treasure"))
            else:
                missedRolls += 1
        
    def treasureCardRoll(treasureCount, missedRolls):
        return renpy.random.randint(0, 100) + player.stats.Luck*0.5 - treasureCount*15 + missedRolls*10 
    
    def prepareExplorationDeck(location, guaranteedEvents):
        eventDeck = []
        monsterDeck = []
        explorationDeck = []

        maximumDeckSize = location.MaximumEventDeck + location.MaximumMonsterDeck
        targetDeckSize = renpy.random.randint(location.MinimumDeckSize, maximumDeckSize)
        print("Min: {0}, Max: {1}, Target: {2}".format(location.MinimumDeckSize, maximumDeckSize, targetDeckSize))
        eventCards = map(lambda eventName: EventDatabase[getFromName(eventName, EventDatabase)], filter(lambda eventName: eventName not in guaranteedEvents.keys(), location.Events))
        availableEventCards = filter(hasEventAllReqsMet, eventCards)
        monsterCards = map(lambda monsterName: MonsterDatabase[getFromName(monsterName, MonsterDatabase)], location.Monsters)
        availableMonsterCards = filter(hasMonsterAllReqsMet, monsterCards)
        for card in availableEventCards:
            limit = card.CardLimit
            if card.name in guaranteedEvents.keys():
                limit -= 1
            for _ in range(limit):
                eventDeck.append(card)
        
        renpy.random.shuffle(eventDeck)
        eventDeck = eventDeck[:location.MaximumEventDeck]
        
        while len(monsterDeck) < location.MaximumMonsterDeck:
            monsterDeck.append(renpy.random.choice(availableMonsterCards))

        explorationDeck.extend(guaranteedEvents.values())

        while len(explorationDeck) < targetDeckSize:
            addMonster = renpy.random.randint(1, 100) > 50
            if len(monsterDeck) > 0 and addMonster:
                monsterCard = monsterDeck.pop(renpy.random.randint(0, len(monsterDeck)-1))
                explorationDeck.append(monsterCard)
            else:
                if len(eventDeck) > 0:
                    eventCard = eventDeck.pop(renpy.random.randint(0, len(eventDeck)-1))
                    explorationDeck.append(eventCard)
                else:
                    break
        
        return explorationDeck
    
    def hasEventAllReqsMet(eventCard):
        progress = ProgressEvent[getFromName(eventCard.name, ProgressEvent)]
        numberOfFulfilledReqs = 0 if progress.questComplete == 1 else requiresCheck(eventCard.requires, eventCard.requiresEvent, player, ProgressEvent)
        return numberOfFulfilledReqs >= len(eventCard.requires) + len(eventCard.requiresEvent)
    
    def hasMonsterAllReqsMet(monsterCard):
        numberOfFulfilledReqs = requiresCheck(monsterCard.requires, monsterCard.requiresEvent, player, ProgressEvent)
        return numberOfFulfilledReqs >= len(monsterCard.requires) + len(monsterCard.requiresEvent)

screen PtceAdventureSetupMenu:
    $ location = LocationDatabase[targetLocation]
    $ maxEventsChosen = isMaxEventsChosen()
    hbox:
        vbox:
            xsize 270
            use ON_TextButtonMid(text="Embark!", action=[Function(embarkOnAdventure, location)])
            use ON_TextButtonMid(text="Return", action=[Function(returnFromAdventureMenu)])

        fixed:
            xsize 500
            yalign 0.5
            use ON_Scrollbox("QuestList"):
                for quest in location.Quests:
                    $ questCard = EventDatabase[getFromName(quest, EventDatabase)]
                    $ questProgress = ProgressEvent[getFromName(quest, ProgressEvent)]
                    $ numberOfFulfilledReqs = 0 if questProgress.questComplete == 1 else requiresCheck(questCard.requires, questCard.requiresEvent, player, ProgressEvent)

                    if numberOfFulfilledReqs >= len(questCard.requires) + len(questCard.requiresEvent):
                        hbox:
                            fixed:
                                xsize 120
                                ysize 60

                                imagebutton:
                                        idle "gui/ListEntryBack.png"
                                        hover "gui/ListEntryBack.png"
                                        yalign 0.5
                                        action SetVariable("hoveredCard", questCard)
                                        hovered SetVariable("hoveredCard", questCard)

                                $ isSelected = QuestSlot.name == questCard.name
                                imagebutton:
                                    if isSelected:
                                        idle "gui/circlebuttonsmallchecked.png"
                                        hover "gui/circlebuttonsmallchecked_hover.png"
                                    else:
                                        idle "gui/circlebuttonsmall.png"
                                        hover "gui/circlebuttonsmall_hover.png"

                                    xalign 0.5
                                    yalign 0.5
                                    action Function(toggleQuest, questCard)

                            text questCard.name xpos -10 yalign 0.5 size 26
        
        fixed:
            xsize 500
            yalign 0.5
            use ON_Scrollbox("EventList"):
                for adventureEvent in location.Events:
                    $ eventCard = EventDatabase[getFromName(adventureEvent, EventDatabase)]
                    $ eventProgress = ProgressEvent[getFromName(adventureEvent, ProgressEvent)]
                    $ numberOfFulfilledReqs = 0 if eventProgress.questComplete == 1 else requiresCheck(eventCard.requires, eventCard.requiresEvent, player, ProgressEvent)

                    if numberOfFulfilledReqs >= len(questCard.requires) + len(questCard.requiresEvent):
                        hbox:
                            fixed:
                                xsize 120
                                ysize 60

                                imagebutton:
                                        idle "gui/ListEntryBack.png"
                                        hover "gui/ListEntryBack.png"
                                        yalign 0.5
                                        action SetVariable("hoveredCard", eventCard)
                                        hovered SetVariable("hoveredCard", eventCard)

                                $ isSelected = eventCard.name in guaranteedEvents.keys()
                                imagebutton:
                                    if isSelected:
                                        idle "gui/circlebuttonsmallchecked.png"
                                        hover "gui/circlebuttonsmallchecked_hover.png"
                                    else:
                                        idle "gui/circlebuttonsmall.png"
                                        hover "gui/circlebuttonsmall_hover.png"

                                    xalign 0.5
                                    yalign 0.5
                                    action [SensitiveIf(isSelected or not maxEventsChosen), Function(toggleEvent, eventCard)]
                            if maxEventsChosen:
                                text eventCard.name xpos -10 yalign 0.5 size 26 color "#b4b4b4"
                            else:
                                text eventCard.name xpos -10 yalign 0.5 size 26
        
        if hoveredCard is not None:
            fixed:
                xsize 510
                yalign 0.5

                text hoveredCard.name xalign 0.5

                fixed:
                    ypos 52
                    ysize 555
                    use ON_Scrollbox(""):
                        if (tabToggle == 1):
                            if hasattr(hoveredCard, 'encyclopedia'):
                                text hoveredCard.encyclopedia size 24
                            else:
                                text hoveredCard.description size 24
                        else:
                            text hoveredCard.description size 24