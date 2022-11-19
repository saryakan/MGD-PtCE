init python:
    def getSpeaker(speakerNumber, EventDatabase, MonsterDatabase):
        while len(actorNames) <= speakerNumber:
            actorNames.append("")

        characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[speakerNumber].name, MonsterDatabase)
        actorNames[speakerNumber] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[speakerNumber].postName

        if EventDatabase[DataLocation].Speakers[speakerNumber].SpeakerType == "?":
            actorNames[speakerNumber] = EventDatabase[DataLocation].Speakers[speakerNumber].name

        return Character(_(actorNames[speakerNumber] +attackTitle), what_prefix='"', what_suffix='"')

    def SceneRequiresCheck():
        global displayingScene, lineOfScene, ProgressEvent, display, DataLocation, finalOption, eventMenuJumps, finalOptionEvent, finalOptionEventScene, ShuffleMenuOptions

        whatStatisIt = ""
        whatItemIsIt = ""
        whatSkillIsIt = ""
        whatPerkIsIt = ""
        statToCheck = 0
        needsStat = 0
        eAmount = ""
        vAmount = ""
        hasVirilityCheck = 0
        hasEnergyCheck = 0
        hasStatCheck = 0

        passcheck = 0

        passStatcheck = 1


        passItemCheck = 0
        passItemChecks = 0
        passEquipmentCheck = 0
        passEquipmentChecks = 0
        passSkillCheck = 0
        passSkillChecks = 0
        passPerkCheck = 0
        passPerkChecks = 0
        passEnergyCheck = 1
        passVirilityCheck = 1
        passLocalProgressCheck = 0
        passLocalProgressChecks = 0
        passFetCheck = 0
        passFetChecks = 0
        passProgressCheck = 0
        passProgressChecks = 0
        passLocalChoiceCheck = 0
        passLocalChoiceChecks = 0
        passTimeCheck = 0
        passTimeChecks = 0
        passChoiceCheck = 0
        passChoiceChecks = 0
        hideFailedMenuChoice = 0
        isFinalOption = 0
        inverseRequirement = 0
        failedItemChecked = 0
        failedEquipmentChecked = 0
        failedSkillChecked = 0
        failedPerkChecked = 0
        Overriding = 0
        global override

        checkPreFuncs = 0
        while checkPreFuncs == 0:
            if displayingScene.theScene[lineOfScene] == "HideOptionOnRequirementFail" and hideFailedMenuChoice == 0:
                hideFailedMenuChoice = 1
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "InverseRequirement":
                inverseRequirement = 1
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "ShuffleMenu":
                ShuffleMenuOptions = 1
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "OverrideOption":
                Overriding = 1
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "FinalOption":
                #REMEMBER U NEED TO CALL THIS LAST OUT OF THE FUNCTIONS
                lineOfScene += 1
                finalOption = copy.deepcopy(displayingScene.theScene[lineOfScene])
                #lineOfScene += 1

                isFinalOption = 1
                finalOptionEvent = copy.deepcopy(eventMenuJumps[-1])
                finalOptionEventScene = copy.deepcopy(eventMenuSceneJumps[-1])


            elif displayingScene.theScene[lineOfScene] == "EventJump":
                lineOfScene += 1
                eventMenuJumps[-1] = copy.deepcopy(displayingScene.theScene[lineOfScene])
                lineOfScene += 1
                if isFinalOption == 1:
                    finalOptionEvent = copy.deepcopy(eventMenuJumps[-1])

                if displayingScene.theScene[lineOfScene] ==  "ThenJumpToScene":
                    lineOfScene += 1
                    eventMenuSceneJumps[-1] = copy.deepcopy(displayingScene.theScene[lineOfScene])
                    lineOfScene += 1
                    if isFinalOption == 1:
                        finalOptionEventScene = copy.deepcopy(eventMenuSceneJumps[-1])


            elif displayingScene.theScene[lineOfScene] == "RequiresMinimumProgress":
                passLocalProgressChecks += 1
                lineOfScene += 1
                DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
                if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
                    passLocalProgressCheck += 1

                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresMinimumProgressFromEvent":
                passProgressChecks += 1
                lineOfScene += 1
                CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                lineOfScene += 1
                if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
                    passProgressCheck += 1

                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresLessProgress":
                passLocalProgressChecks += 1
                lineOfScene += 1
                DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
                if int(displayingScene.theScene[lineOfScene]) > ProgressEvent[DataLocation].eventProgress:
                    passLocalProgressCheck += 1

                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresLessProgressFromEvent":
                passProgressChecks += 1
                lineOfScene += 1
                CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                lineOfScene += 1
                if int(displayingScene.theScene[lineOfScene]) > ProgressEvent[CheckEvent].eventProgress:
                    passProgressCheck += 1

                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresChoice":
                passLocalChoiceChecks += 1
                lineOfScene += 1
                choiceToCheck = int(displayingScene.theScene[lineOfScene])
                lineOfScene += 1
                DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

                while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                    ProgressEvent[DataLocation].choices.append("")

                if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
                    passLocalChoiceCheck += 1
                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresChoiceFromEvent":
                passChoiceChecks += 1
                lineOfScene += 1
                CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                lineOfScene += 1
                choiceToCheck = int(displayingScene.theScene[lineOfScene])

                while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                    ProgressEvent[CheckEvent].choices.append("")

                lineOfScene += 1
                if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
                    passChoiceCheck += 1
                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresTime":
                passTimeChecks += 1
                lineOfScene += 1
                if IfTime(displayingScene.theScene[lineOfScene]) == 1:
                    passTimeCheck += 1
                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresStat":
                passStatcheck = 0
                lineOfScene += 1
                whatStatisIt = displayingScene.theScene[lineOfScene]
                statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
                lineOfScene += 1
                needsStat = int(displayingScene.theScene[lineOfScene])
                if needsStat <= statToCheck:
                    passStatcheck = 1
                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresFetishLevelEqualOrGreater":
                passFetCheck += 1
                lineOfScene += 1
                fetchFetish = displayingScene.theScene[lineOfScene]
                lineOfScene += 1
                fetishLvl = int(displayingScene.theScene[lineOfScene])

                if player.getFetish(fetchFetish) >= fetishLvl:
                    passFetChecks += 1

                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresFetishLevelEqualOrLess":
                passFetCheck += 1
                lineOfScene += 1
                fetchFetish = displayingScene.theScene[lineOfScene]
                lineOfScene += 1
                fetishLvl = int(displayingScene.theScene[lineOfScene])

                if player.getFetish(fetchFetish) <= fetishLvl:
                    passFetChecks += 1

                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresItem":
                passItemCheck += 1
                lineOfScene += 1

                if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                    passItemChecks += 1
                elif player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                    passItemChecks += 1
                elif player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                    passItemChecks += 1
                elif player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                    passItemChecks += 1
                else:
                    for each in player.inventory.items:
                        if each.name == displayingScene.theScene[lineOfScene]:
                            passItemChecks += 1
                if passItemCheck != passItemChecks and failedItemChecked == 0:
                    failedItemChecked = 1
                    whatItemIsIt = displayingScene.theScene[lineOfScene]
                elif inverseRequirement == 1:
                    whatItemIsIt = displayingScene.theScene[lineOfScene]
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresItemEquipped":
                passEquipmentCheck += 1
                lineOfScene += 1

                if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                    passEquipmentChecks += 1
                elif player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                    passEquipmentChecks += 1
                elif player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                    passEquipmentChecks += 1
                elif player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                    passEquipmentChecks += 1
                if passEquipmentCheck != passEquipmentChecks and failedEquipmentChecked == 0:
                    failedEquipmentChecked = 1
                    whatEquipmentIsIt = displayingScene.theScene[lineOfScene]
                elif inverseRequirement == 1:
                    whatEquipmentIsIt = displayingScene.theScene[lineOfScene]
                lineOfScene += 1

            elif displayingScene.theScene[lineOfScene] == "RequiresSkill":
                passSkillCheck += 1
                lineOfScene += 1

                for each in player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passSkillChecks += 1
                if passSkillCheck != passSkillChecks and failedSkillChecked == 0:
                    failedSkillChecked = 1
                    whatSkillIsIt = displayingScene.theScene[lineOfScene]
                elif inverseRequirement == 1:
                    whatSkillIsIt = displayingScene.theScene[lineOfScene]

                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresPerk":
                passPerkCheck += 1
                lineOfScene += 1

                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passPerkChecks += 1
                if passPerkCheck != passPerkChecks and failedPerkChecked == 0:
                    failedPerkChecked = 1
                    whatPerkIsIt = displayingScene.theScene[lineOfScene]
                elif inverseRequirement == 1:
                    whatPerkIsIt = displayingScene.theScene[lineOfScene]
                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresEnergy":
                passEnergyCheck = 0
                hasEnergyCheck = 1
                lineOfScene += 1
                eAmount = displayingScene.theScene[lineOfScene]

                if player.stats.ep >= int(eAmount):
                    passEnergyCheck = 1

                lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "RequiresVirility":
                passVirilityCheck = 0
                hasVirilityCheck = 1
                lineOfScene += 1
                vAmount = displayingScene.theScene[lineOfScene]

                if getVirility(player) >= int(vAmount):
                    passVirilityCheck = 1

                lineOfScene += 1
            else:
                if Overriding == 1:
                    override = copy.deepcopy(displayingScene.theScene[lineOfScene])
                checkPreFuncs += 1


        if inverseRequirement == 0:
            if passStatcheck == 1 and passFetCheck == passFetChecks and passItemCheck == passItemChecks and passEquipmentCheck == passEquipmentChecks and passSkillCheck == passSkillChecks and passPerkCheck == passPerkChecks and passEnergyCheck == 1 and passVirilityCheck == 1 and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passLocalChoiceCheck == passLocalChoiceChecks and passChoiceCheck == passChoiceChecks and passTimeCheck == passTimeChecks:
                passcheck = 1
            else:
                if hideFailedMenuChoice == 0:
                    if passLocalChoiceCheck == passLocalChoiceChecks and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passChoiceCheck == passChoiceChecks:
                        if passStatcheck == 0:
                            display = "Requires " + str(needsStat) + " " + whatStatisIt + "."
                        elif passItemCheck != passItemChecks:
                            display = "Requires a " + whatItemIsIt + " in your inventory."
                        elif passEquipmentCheck != passEquipmentChecks:
                            display = "Must not have " + whatEquipmentIsIt + " equipped."
                        elif passSkillCheck != passSkillChecks and failedSkillChecked == 1:
                            display = "Requires you to know the " + whatSkillIsIt + " skill."
                        elif passPerkCheck != passPerkChecks:
                            display = "Requires you to have the " + whatPerkIsIt + " perk."
                        elif passEnergyCheck == 0:
                            display = "Requires " + eAmount + " energy."
                        elif passVirilityCheck == 0:
                            display = "Requires " + vAmount + " virility."
        elif inverseRequirement == 1:
            if passStatcheck == 1 and passFetCheck == passFetChecks and passItemCheck == passItemChecks and passEquipmentCheck == passEquipmentChecks and passSkillCheck == passSkillChecks and passPerkCheck == passPerkChecks and passEnergyCheck == 1 and passVirilityCheck == 1 and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passLocalChoiceCheck == passLocalChoiceChecks and passChoiceCheck == passChoiceChecks and passTimeCheck == passTimeChecks:
                if hideFailedMenuChoice == 0:
                    if passLocalChoiceCheck == passLocalChoiceChecks and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passChoiceCheck == passChoiceChecks:
                        if passVirilityCheck == 1 and hasVirilityCheck == 1:
                            display = "Must have less than " + vAmount + " virility."
                        if passEnergyCheck == 1 and hasEnergyCheck == 1:
                            display = "Must have less than " + eAmount + " energy."
                        if passPerkCheck == passPerkChecks and passPerkCheck == 1:
                            display = "Must not have the " + whatPerkIsIt + " perk."
                        if passSkillCheck == passSkillChecks and passSkillCheck == 1:
                            display = "Must not know the " + whatSkillIsIt + " skill."
                        if passItemCheck == passItemChecks and passItemCheck == 1:
                            display = "Must not have " + whatItemIsIt + " in your inventory."
                        if passEquipmentCheck == passEquipmentChecks and passEquipmentCheck == 1:
                            display = "Must not have " + whatEquipmentIsIt + " equipped."
                        if passStatcheck == 1 and hasStatCheck == 1:
                            display = "Must have less than " + str(needsStat) + " " + whatStatisIt + "."

            else:
                passcheck = 1
        return passcheck

label displayScene:
    if SceneBookMarkRead == 1:
        $ displayingScene = copy.deepcopy(HoldingScene)
        $ lineOfScene = copy.deepcopy(HoldingLine)
        $ DataLocation = copy.deepcopy(HoldingDataLoc)
        $ HoldingDataLoc = -1
        $ HoldingLine =-1
        $ HoldingScene = LossScene()
        $ SceneBookMarkRead = 2
    else:
        $ lineOfScene = 0

label resumeSceneAfterCombat:

    $ showOnSide = 0
    $ showSpeakers = 1
    $ display1 = ""
    $ display2 = ""
    $ display3 = ""
    $ display4 = ""
    $ display5 = ""
    $ display6 = ""

    if len(actorNames) < 12:
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")
        $ actorNames.append("")


    python:
        try:
            displayingScene.theScene
        except:
            displayingScene = Dialogue()

    while lineOfScene < len(displayingScene.theScene):
        $ readLine = 0
        $ notFunction = 0

        #if DialogueIsFrom == "Event" or DialogueIsFrom == "Monster":
        #    if displayHealthInEvent == 1:
        #        show screen ON_HealthDisplayBacking
        #        show screen ON_HealthDisplay
        #    else:
        #        hide screen ON_HealthDisplayBacking
        #        hide screen ON_HealthDisplay
        #$ showTheLine = displayingScene.theScene[lineOfScene]
        #"[showTheLine]"
        if showSpeakers == 1:
            show screen ON_CharacterDialogueScreen (_layer="master")
            if len(monsterEncounter) > 0:
                show screen ON_EnemyCardScreen (_layer="master")
        else:
            hide screen ON_CharacterDialogueScreen

        $ dialogueFunction = additionalDialogueFunctions.get(displayingScene.theScene[lineOfScene])
        if dialogueFunction != None:
            $ dialogueFunction.execute()

        elif displayingScene.theScene[lineOfScene] == "PlayerSpeaks":
            $ Speaker = Character(_(player.name+attackTitle),
                                    what_prefix='"',
                                    what_suffix='"')
            $ lineOfScene += 1
            $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "PlayerSpeaksSkill":
            if len(monsterEncounter) >= 1:
                $ Speaker = Character(_(player.name+attackTitle) )
                $ lineOfScene += 1
                $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "SetFlexibleSpeaker":
            $ lineOfScene += 1
            $ FlexibleSpeaker = int(displayingScene.theScene[lineOfScene])-1

        elif displayingScene.theScene[lineOfScene] == "FlexibleSpeaks":

            if len(monsterEncounter) >= 2:
                $ Speaker = monsterEncounter[FlexibleSpeaker].name+attackTitle
            else:
                $ Speaker = getSpeaker(FlexibleSpeaker, EventDatabase, MonsterDatabase)

            $ lineOfScene += 1
            $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "Speak":
            $ lineOfScene += 1
            $ Speaker = Character(_(displayingScene.theScene[lineOfScene]),
                                    what_prefix='"',
                                    what_suffix='"')
            $ lineOfScene += 1
            $ readLine = 1

        elif displayingScene.theScene[lineOfScene] == "Speaks":

            if len(monsterEncounter) >= 1:
                $ actorNames[0] = monsterEncounter[0].name
            $ Speaker = Character(_(actorNames[0])+attackTitle,
                                    what_prefix='"',
                                    what_suffix='"')
            $ lineOfScene += 1
            $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "Speaks2" or displayingScene.theScene[lineOfScene] == "Speaks3"  or  displayingScene.theScene[lineOfScene] == "Speaks4" or displayingScene.theScene[lineOfScene] == "Speaks5" or displayingScene.theScene[lineOfScene] == "Speaks6" or  displayingScene.theScene[lineOfScene] == "Speaks7" or displayingScene.theScene[lineOfScene] == "Speaks8" or displayingScene.theScene[lineOfScene] == "Speaks9" or displayingScene.theScene[lineOfScene] == "Speaks10" or displayingScene.theScene[lineOfScene] == "Speaks11" or displayingScene.theScene[lineOfScene] == "Speaks12":

            $ SpeakerNum = 0
            if displayingScene.theScene[lineOfScene] == "Speaks":
                $ SpeakerNum = 0
            elif displayingScene.theScene[lineOfScene] == "Speaks2":
                $ SpeakerNum = 1
            elif displayingScene.theScene[lineOfScene] == "Speaks3":
                $ SpeakerNum = 2
            elif displayingScene.theScene[lineOfScene] == "Speaks4":
                $ SpeakerNum = 3
            elif displayingScene.theScene[lineOfScene] == "Speaks5":
                $ SpeakerNum = 4
            elif displayingScene.theScene[lineOfScene] == "Speaks6":
                $ SpeakerNum = 5
            elif displayingScene.theScene[lineOfScene] == "Speaks7":
                $ SpeakerNum = 6
            elif displayingScene.theScene[lineOfScene] == "Speaks8":
                $ SpeakerNum = 7
            elif displayingScene.theScene[lineOfScene] == "Speaks9":
                $ SpeakerNum = 8
            elif displayingScene.theScene[lineOfScene] == "Speaks10":
                $ SpeakerNum = 9
            elif displayingScene.theScene[lineOfScene] == "Speaks11":
                $ SpeakerNum = 10
            elif displayingScene.theScene[lineOfScene] == "Speaks12":
                $ SpeakerNum = 11


            if len(monsterEncounter) >= SpeakerNum+1:
                $ Speaker = monsterEncounter[SpeakerNum].name+attackTitle
            else:
                $ Speaker = getSpeaker(SpeakerNum, EventDatabase, MonsterDatabase)

            $ lineOfScene += 1
            $ readLine = 1


        elif displayingScene.theScene[lineOfScene] == "DisplayCharacters":
            $ showSpeakers = 1
            $ lineOfScene += 1
            $ SceneCharacters = []
            if len(monsterEncounter) == 0:
                $ hidingCombatEncounter = 0

            if hidingCombatEncounter == 0:
                $ monsterEncounter = []
                $ DefeatedEncounterMonsters = []
                $ trueMonsterEncounter = []
            while displayingScene.theScene[lineOfScene] != "EndLoop":

                python:
                    try:
                        targetChar = int(displayingScene.theScene[lineOfScene]) - 1
                    except:
                        targetChar = getFromName(displayingScene.theScene[lineOfScene], SceneCharacters)


                $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[targetChar].name, MonsterDatabase)
                if characterDataLocation != -1:
                    $ SceneCharacters.append(copy.deepcopy(MonsterDatabase[characterDataLocation]))
                if EventDatabase[DataLocation].Speakers[targetChar].SpeakerType == "?":
                    $ SceneCharacters.append(copy.deepcopy(Monster(Stats(),0,  "?", "?")))

                $ lineOfScene += 1
            python:
                for each in SceneCharacters:
                    each = initiateImageLayers(each)

                    for SetData in persistantMonSetData:
                        if SetData.name == each.IDname:
                            each.currentSet = getFromName(SetData.startingSet, each.ImageSets)



            #if hidingCombatEncounter == 0:
            #    hide screen ON_HealthDisplayBacking
            #    hide screen ON_HealthDisplay
            show screen ON_CharacterDialogueScreen (_layer="master")
            #if hidingCombatEncounter == 0:
            #    if displayHealthInEvent == 1:
            #        hide screen ON_HealthDisplayBacking
            #        hide screen ON_HealthDisplay
            #    else:
            #        hide screen ON_HealthDisplayBacking
            #        hide screen ON_HealthDisplay
        elif displayingScene.theScene[lineOfScene] == "ChangeImageFor":
            if DialogueIsFrom == "Monster":
                $ lineOfScene += 1
                python:
                    try:
                        settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                        lineOfScene += 1
                        settingToImage = displayingScene.theScene[lineOfScene]
                    except:
                        settingToImage = displayingScene.theScene[lineOfScene]
                        settingCharcter = CombatFunctionEnemytarget

                $ imgI = 0
                python:
                    for each in monsterEncounter:
                        if imgI == settingCharcter:
                            each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                            if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                                each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                        imgI += 1
                    imgI = 0
                    for each in DefeatedEncounterMonsters:
                        if imgI == settingCharcter:
                            each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                            if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                                each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                        imgI += 1

            else:

                if len(monsterEncounter) == 0 or hidingCombatEncounter == 1:
                    $ lineOfScene += 1
                    $ settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1

                $ lineOfScene += 1
                $ settingToImage = displayingScene.theScene[lineOfScene]
                $ imgI = 0
                python:
                    if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                        for each in monsterEncounter:
                            if imgI == CombatFunctionEnemytarget:
                                each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                                if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                                    each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                            imgI += 1

                    else:
                        imgI = 0
                        for each in SceneCharacters:
                            if imgI == settingCharcter:
                                each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                                if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                                    each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                            imgI += 1
            hide screen ON_CharacterDialogueScreen





        elif displayingScene.theScene[lineOfScene] == "AnimateImageLayer":
            $ lineOfScene += 1
            $ settingToImage = displayingScene.theScene[lineOfScene]

            $ lineOfScene += 1
            $ layerToChange = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1

            python:
                try:
                    settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1

                except:
                    ifIsInScene = 0
                    if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                        searchingCharacters = monsterEncounter
                    else:
                        searchingCharacters = SceneCharacters
                    if len(searchingCharacters) > 0 and hidingCombatEncounter == 0:
                        #during combat layer change
                        if getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)!= -1:
                            ifIsInScene = 1
                            settingCharcter = getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)

                    if ifIsInScene == 0:
                        settingCharcter = CombatFunctionEnemytarget
            if settingToImage == "Animation":
                $ animationList = []
                $ animationChoice = ""
                $ currentAnimationImg = 0
            elif settingToImage == "Animation2":
                $ animationList2 = []
                $ animationChoice2 = ""
                $ currentAnimationImg2 = 0
            elif settingToImage == "Animation3":
                $ animationList3 = []
                $ animationChoice3 = ""
                $ currentAnimationImg3 = 0

            $ lineOfScene += 1
            if settingToImage == "Animation":
                $ animationSpeed = float(displayingScene.theScene[lineOfScene])
                $ animationTime = float(displayingScene.theScene[lineOfScene])
            elif settingToImage == "Animation2":
                $ animationSpeed2 = float(displayingScene.theScene[lineOfScene])
                $ animationTime2 = float(displayingScene.theScene[lineOfScene])
            elif settingToImage == "Animation3":
                $ animationSpeed3 = float(displayingScene.theScene[lineOfScene])
                $ animationTime3 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1


            if settingToImage == "Animation":
                $ animationList = []
            elif settingToImage == "Animation2":
                $ animationList2 = []
            elif settingToImage == "Animation3":
                $ animationList3 = []
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        if settingToImage == "Animation":
                            $ animationList.append(displayingScene.theScene[lineOfScene])
                        elif settingToImage == "Animation2":
                            $ animationList2.append(displayingScene.theScene[lineOfScene])
                        elif settingToImage == "Animation3":
                            $ animationList3.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            if settingToImage == "Animation":
                if len(animationList) > 0:
                    $ animationChoice = animationList[0]
            elif settingToImage == "Animation2":
                if len(animationList2) > 0:
                    $ animationChoice2 = animationList2[0]
            elif settingToImage == "Animation3":
                if len(animationList3) > 0:
                    $ animationChoice3 = animationList3[0]

            $ searchingCharacters = AnimateImgLayer(searchingCharacters, settingCharcter, layerToChange, settingToImage)



        elif  displayingScene.theScene[lineOfScene] == "ChangeImageLayer":

            $ lineOfScene += 1
            $ layerToChange = displayingScene.theScene[lineOfScene]

            if DialogueIsFrom == "Monster":

                $ lineOfScene += 1
                python:
                    try:
                        settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                        lineOfScene += 1
                        settingToImage = displayingScene.theScene[lineOfScene]
                    except:
                        ifIsInScene = 0

                        if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                            #during combat layer change
                            if getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)!= -1:
                                ifIsInScene = 1
                                settingCharcter = getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)
                                lineOfScene += 1
                                settingToImage = displayingScene.theScene[lineOfScene]
                        if ifIsInScene == 0:
                            settingToImage = displayingScene.theScene[lineOfScene]
                            settingCharcter = CombatFunctionEnemytarget

                #change the image layers for monsters post combat, I need to really condense all the image card stuff into one single thing, but condensing the change image layer crap into one is a start.
                if layerToChange == "ImageSet" or  layerToChange == "ImageSetDontCarryOver" or layerToChange == "ImageSetPersist":
                    $ monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                    $ DefeatedEncounterMonsters = changeImgSet(DefeatedEncounterMonsters, settingCharcter, layerToChange, settingToImage)
                    #$ monsterEncounter[settingCharcter] = initiateOverlays(monsterEncounter[settingCharcter])
                    #$ DefeatedEncounterMonsters[settingCharcter] = initiateOverlays(DefeatedEncounterMonsters[settingCharcter])
                else:
                    $ monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                    $ DefeatedEncounterMonsters = changeImgLayer(DefeatedEncounterMonsters, settingCharcter, layerToChange, settingToImage)

            else:
                if len(monsterEncounter) == 0 or hidingCombatEncounter == 1:
                    python:
                        try:
                            lineOfScene += 1
                            settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                        except:
                            ifIsInScene = 0
                            if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                                #during combat layer change
                                if getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)!= -1:

                                    ifIsInScene = 1#CombatFunctionEnemytarget
                                    settingCharcter = getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)
                            else:
                                #out of combat layer change
                                if getFromName(displayingScene.theScene[lineOfScene], SceneCharacters)!= -1:
                                    ifIsInScene = 1
                                    settingCharcter = getFromName(displayingScene.theScene[lineOfScene], SceneCharacters)

                            if ifIsInScene == 0:
                                lineOfScene -= 1
                                settingCharcter = 0
                else:
                    $ settingCharcter = CombatFunctionEnemytarget


                $ lineOfScene += 1
                $ settingToImage = displayingScene.theScene[lineOfScene]
                $ imgI = 0

                if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                    #during combat layer change
                    if settingCharcter == -1:
                        $ settingCharcter = len(monsterEncounter) - 1
                    if layerToChange == "ImageSet" or layerToChange == "ImageSetPersist"  or  layerToChange == "ImageSetDontCarryOver":
                        $ monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                        #$ monsterEncounter[settingCharcter] = initiateOverlays(monsterEncounter[settingCharcter])
                    else:

                        $ monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                else:
                    #out of combat layer change
                    if layerToChange == "ImageSet" or layerToChange == "ImageSetPersist"  or  layerToChange == "ImageSetDontCarryOver":
                        $ SceneCharacters = changeImgSet(SceneCharacters, settingCharcter, layerToChange, settingToImage)
                        #$ SceneCharacters[settingCharcter] = initiateOverlays(SceneCharacters[settingCharcter])
                    else:
                        $ SceneCharacters = changeImgLayer(SceneCharacters, settingCharcter, layerToChange, settingToImage)

            hide screen ON_CharacterDialogueScreen



        elif  displayingScene.theScene[lineOfScene] == "HideHealth":
            $ displayHealthInEvent = 0


        elif displayingScene.theScene[lineOfScene] == "SetProgress":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeProgress":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress += int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "ChangeProgressBasedOnVirility":
            $ lineOfScene += 1
            $ multiplier = float(displayingScene.theScene[lineOfScene])

            $ virilityProg = getVirility(player)*0.1
            #if getVirility(player) < 350:
            #    $ virilityProg = 0.5 + ( getVirility(player)/(50-( getVirility(player)*0.1259)))
            #else:
            #    $ virilityProg = getVirility(player)-290.5
            $ virilityProg *= multiplier


            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress += virilityProg
        elif displayingScene.theScene[lineOfScene] == "HoldCurrentVirility":
            $ heldVirility = copy.deepcopy(getVirility(player))
        elif displayingScene.theScene[lineOfScene] == "HoldCurrentVirilityEnd":
            $ heldVirility = 0


        elif displayingScene.theScene[lineOfScene] == "GetEventAndSetProgress":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1

            $ ProgressEvent[CheckEvent].eventProgress = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "GetEventAndChangeProgress":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1

            $ ProgressEvent[CheckEvent].eventProgress += int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "ProgressEquals":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            if int(displayingScene.theScene[lineOfScene]) == ProgressEvent[DataLocation].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_1
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "ProgressEqualsOrGreater":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_2
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "ProgressEqualsOrLess":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            if int(displayingScene.theScene[lineOfScene]) >= ProgressEvent[DataLocation].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_58
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "GetAnEventsProgressThenIfEquals":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) == ProgressEvent[CheckEvent].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_26
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "GetAnEventsProgressThenIfEqualsOrGreater":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_27
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "GetAnEventsProgressThenIfEqualsOrLess":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) >= ProgressEvent[CheckEvent].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_65
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "EventsProgressEqualsOtherEventsProgress":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

            if ProgressEvent[CheckEvent].eventProgress == ProgressEvent[CheckEvent2].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_66
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "EventsProgressEqualsOrGreaterThanOtherEventsProgress":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

            if ProgressEvent[CheckEvent].eventProgress >= ProgressEvent[CheckEvent2].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_67
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfEventsProgressEqualsOrLessThanOtherEventsProgress":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

            if ProgressEvent[CheckEvent].eventProgress <= ProgressEvent[CheckEvent2].eventProgress:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_68
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "VirilityEqualsOrGreater":
            $ lineOfScene += 1

            if int(displayingScene.theScene[lineOfScene]) <= getVirility(player) :
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_71
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfRanAway":
            if RanAway == "True":
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]

                call sortMenuD from _call_sortMenuD_86
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

            $ runAndStayInEvent = 0
            $ RanAway = "False"
        elif displayingScene.theScene[lineOfScene] == "IfChoice":
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")


            if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]

                call sortMenuD from _call_sortMenuD_4
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "SetChoice":
            $ lineOfScene += 1
            $ HoldChoiceNumber = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1

            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while HoldChoiceNumber-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")
            $ ProgressEvent[DataLocation].choices[HoldChoiceNumber-1] = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "GetEventAndIfChoice":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                $ ProgressEvent[CheckEvent].choices.append("")


            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_8
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "GetEventAndSetChoice":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1

            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                $ ProgressEvent[CheckEvent].choices.append("")
            $ ProgressEvent[CheckEvent].choices[choiceToCheck-1] = displayingScene.theScene[lineOfScene]



        elif displayingScene.theScene[lineOfScene] == "SetChoiceToPlayerName":
            $ lineOfScene += 1
            $ HoldChoiceNumber = int(displayingScene.theScene[lineOfScene])

            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while HoldChoiceNumber-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")

            $ ProgressEvent[DataLocation].choices[HoldChoiceNumber-1] = player.name

        elif displayingScene.theScene[lineOfScene] == "SetChoiceTo PlayerName":
            $ lineOfScene += 1
            $ HoldChoiceNumber = int(displayingScene.theScene[lineOfScene])

            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while HoldChoiceNumber-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")

            $ ProgressEvent[DataLocation].choices[HoldChoiceNumber-1] = " " + player.name

        elif displayingScene.theScene[lineOfScene] == "SetChoiceToPlayerNameFromOtherEvent":
                $ lineOfScene += 1
                $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                $ lineOfScene += 1
                $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

                while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                    $ ProgressEvent[CheckEvent].choices.append("")

                $ ProgressEvent[CheckEvent].choices[choiceToCheck-1] = player.name


        elif displayingScene.theScene[lineOfScene] == "ChoiceToDisplayPlayer":
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")

            $ PlayerChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
        elif displayingScene.theScene[lineOfScene] == "ChoiceToDisplayMonster":
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")

            $ MonsterChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]

        elif displayingScene.theScene[lineOfScene] == "ChoiceToDisplayPlayerFromOtherEvent":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                $ ProgressEvent[CheckEvent].choices.append("")

            $ PlayerChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
        elif displayingScene.theScene[lineOfScene] == "ChoiceToDisplayMonsterFromOtherEvent":
            $ lineOfScene += 1
            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
            $ lineOfScene += 1
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                $ ProgressEvent[CheckEvent].choices.append("")

            $ MonsterChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]

        elif displayingScene.theScene[lineOfScene] == "HealingSickness":
            $ HealingSickness = 6
        elif displayingScene.theScene[lineOfScene] == "IfHealingSickness":
            if HealingSickness > 0:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]

                call sortMenuD from _call_sortMenuD_54
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfDelayingNotifications":
            $ lineOfScene += 1
            if timeNotify == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_72
            if len(monsterEncounter) > 0:
                return
        elif displayingScene.theScene[lineOfScene] == "AdvanceTime":
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) > 0:
                $ number = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
                python:
                    try:
                        if displayingScene.theScene[lineOfScene] == "DelayNotifications":
                            timeNotify = 1
                        else:
                            lineOfScene -= 1
                    except:
                        lineOfScene -= 1

                call advanceTime(number) from _call_advanceTime_4
        elif displayingScene.theScene[lineOfScene] == "RestPlayer":
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "DelayNotifications":
                $ timeNotify = 1
            else:
                $ lineOfScene -= 1
            call advanceTime(TimeIncrease=1) from _call_advanceTime_1
            $ player = Resting(player)
            $ notFunction = 0

        elif displayingScene.theScene[lineOfScene] == "SleepPlayer":
            $ lineOfScene += 1
            $ delayCheck = displayingScene.theScene[lineOfScene]
            $ player = player.statusEffects.refresh(player)
            $ player.stats.refresh()
            $ dreaming = 1
            if delayCheck == "DelayNotifications":
                $ timeNotify = 1
            else:
                $ lineOfScene -= 1

            call advanceTime(TimeIncrease=1) from _call_advanceTime_2
            if delayCheck == "DelayNotifications":
                $ timeNotify = 1
            if timeNotify == 0:
                $ shuffledDream = copy.deepcopy(DreamList)
                $ renpy.random.shuffle(shuffledDream)
                $ showingDream = []
                $ showingDream.append(copy.deepcopy(shuffledDream[0]))
                call TimeEvent(CardType="Dream", LoopedList=showingDream) from _call_TimeEvent_3
                $ timeNotify = 0

            if TimeOfDay != Morning:
                while TimeOfDay != Morning:
                    if TimeOfDay != Morning:
                        if delayCheck == "DelayNotifications":
                            $ timeNotify = 1
                        call advanceTime(TimeIncrease=1) from _call_advanceTime_3
            $ notFunction = 0




        elif displayingScene.theScene[lineOfScene] == "RefreshPlayer":
            $ player = player.statusEffects.refresh(player)
            $ player.stats.refresh()
        elif displayingScene.theScene[lineOfScene] == "ClearPlayerStatusEffects":
            $ player = player.statusEffects.refresh(player)
        elif displayingScene.theScene[lineOfScene] == "RemoveStatusEffect":
            $ lineOfScene += 1
            $ player = removeThisStatusEffect(displayingScene.theScene[lineOfScene], player)




        elif displayingScene.theScene[lineOfScene] == "ChangeArousal":
            $ lineOfScene += 1
            $ player.stats.hp += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) > 0):
                $ display = "You were aroused by " + displayingScene.theScene[lineOfScene] + "!"
            else:
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You calmed down by " + str(amountLost) + "!"

            if player.stats.hp <= 0:
                $ player.stats.hp = 0
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                call read from _call_read_19

        elif displayingScene.theScene[lineOfScene] == "ChangeArousalQuietly":
            $ lineOfScene += 1
            $ player.stats.hp += int(displayingScene.theScene[lineOfScene])
            if player.stats.hp <= 0:
                $ player.stats.hp = 0

        elif displayingScene.theScene[lineOfScene] == "ChangeArousalByPercent":
            $ lineOfScene += 1
            $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.stats.max_true_hp
            $ check = math.floor(check)
            $ check = int(check)
            $ player.stats.hp += check

            if player.stats.hp <= 0:
                $ player.stats.hp = 0

        elif displayingScene.theScene[lineOfScene] == "SetArousalToMax":
            $ player.stats.hp = player.stats.max_true_hp

        elif displayingScene.theScene[lineOfScene] == "SetArousalToXUnlessHigherThanX":
            $ lineOfScene += 1
            $ TheX = int(displayingScene.theScene[lineOfScene])

            if TheX <= player.stats.hp:
                $ player.stats.hp = TheX
        elif displayingScene.theScene[lineOfScene] == "SetArousalToXUnlessHigherThanXThenAddY":
            $ lineOfScene += 1
            $ TheX = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ TheY = int(displayingScene.theScene[lineOfScene])

            if TheX >= player.stats.hp:
                $ player.stats.hp = TheX
            else:
                $ player.stats.hp += TheY

        elif displayingScene.theScene[lineOfScene] == "ChangeEnergy":
            $ lineOfScene += 1
            $ player.stats.ep += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You lost " + str(amountLost) + " energy!"
            else:
                $ display = "You gain " + displayingScene.theScene[lineOfScene] + " energy!"
            if player.stats.ep <= 0:
                $ player.stats.ep = 0
            if player.stats.ep > player.stats.max_true_ep:
                $ player.stats.ep = player.stats.max_true_ep
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "ChangeEnergyQuietly":
            $ lineOfScene += 1
            $ player.stats.ep += int(displayingScene.theScene[lineOfScene])
            if player.stats.ep <= 0:
                $ player.stats.ep = 0
            if player.stats.ep > player.stats.max_true_ep:
                $ player.stats.ep = player.stats.max_true_ep
        elif displayingScene.theScene[lineOfScene] == "ChangeEnergyByPercent":
            $ lineOfScene += 1
            $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.stats.max_true_ep
            $ check = math.floor(check)
            $ check = int(check)
            $ player.stats.ep += check

            if player.stats.ep <= 0:
                $ player.stats.ep = 0
            if player.stats.ep > player.stats.max_true_ep:
                $ player.stats.ep = player.stats.max_true_ep
        elif displayingScene.theScene[lineOfScene] == "PlayerCurrentEnergyCost":
            $ player.stats.ep -= combatChoice.cost
        elif displayingScene.theScene[lineOfScene] == "ChangeSpirit":
            $ lineOfScene += 1
            $ player.stats.sp += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You lost " + str(amountLost) + " spirit!"
            else:
                $ display = "You gain " + displayingScene.theScene[lineOfScene] + " spirit!"
            if player.stats.sp <= 0:
                $ player.stats.sp = 0
            if player.stats.sp > player.stats.max_true_sp:
                $ player.stats.sp = player.stats.max_true_sp
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeSpiritQuietly":
            $ lineOfScene += 1
            $ player.stats.sp += int(displayingScene.theScene[lineOfScene])
            if player.stats.sp <= 0:
                $ player.stats.sp = 0
            if player.stats.sp > player.stats.max_true_sp:
                $ player.stats.sp = player.stats.max_true_sp

        elif displayingScene.theScene[lineOfScene] == "SetSpirit":
            $ lineOfScene += 1
            $ player.stats.sp = int(displayingScene.theScene[lineOfScene])

            if player.stats.sp <= 0:
                $ player.stats.sp = 0
            if player.stats.sp > player.stats.max_true_sp:
                $ player.stats.sp = player.stats.max_true_sp


        elif displayingScene.theScene[lineOfScene] == "ChangeMaxArousal":
            $ lineOfScene += 1

            $ player.stats.max_hp += int(displayingScene.theScene[lineOfScene])
            $ player.CalculateStatBoost()

            if (int(displayingScene.theScene[lineOfScene]) > 0):
                $ display = "You gained " + displayingScene.theScene[lineOfScene] + " maximum arousal!"
            else:
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You lost " + str(amountLost) + " maximum arousal!"

            if player.stats.hp <= 0:
                $ player.stats.hp = 0
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeMaxEnergy":
            $ lineOfScene += 1

            $ player.stats.max_ep += int(displayingScene.theScene[lineOfScene])
            $ player.CalculateStatBoost()

            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You lost " + str(amountLost) + " maximum energy!"
            else:
                $ display = "You gain " + displayingScene.theScene[lineOfScene] + " maximum energy!"
            if player.stats.ep <= 0:
                $ player.stats.ep = 0
            if player.stats.ep > player.stats.max_true_ep:
                $ player.stats.ep = player.stats.max_true_ep
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "ChangeMaxSpirit":
            $ lineOfScene += 1
            $ player.stats.max_sp += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You lost " + str(amountLost) + " maximum spirit!"
            else:
                $ display = "You gain " + displayingScene.theScene[lineOfScene] + " maximum spirit!"
            if player.stats.sp <= 0:
                $ player.stats.sp = 0
            if player.stats.sp > player.stats.max_true_sp:
                $ player.stats.sp = player.stats.max_true_sp
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "ChangePower":
            $ lineOfScene += 1
            $ player.stats.Power += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " power!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " power!"
            $ player.CalculateStatBoost()
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeWill":
            $ lineOfScene += 1
            $ player.stats.Willpower += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " willpower!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " willpower!"
            $ player.CalculateStatBoost()
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeInt":
            $ lineOfScene += 1
            $ player.stats.Int += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " intelligence!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " intelligence!"
            $ player.CalculateStatBoost()
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeTech":
            $ lineOfScene += 1
            $ player.stats.Tech += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " technique!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " technique!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeAllure":
            $ lineOfScene += 1
            $ player.stats.Allure += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " allure!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " allure!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "ChangeLuck":
            $ lineOfScene += 1
            $ player.stats.Luck += int(displayingScene.theScene[lineOfScene])
            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
                $ display = "You permanently lost " + str(amountLost) + " luck!"
            else:
                $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " luck!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"


        elif displayingScene.theScene[lineOfScene] == "ChangeSensitivity":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ player.BodySensitivity.changeRes (resTarget, resAmount)

            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = resAmount*-1
                if resTarget == "Breasts":
                    $ resTarget = "Nipple"
                if resTarget == "Sex":
                    $ resTarget = "Cock"
                $ display = "You lost " + str(amountLost) + " " + resTarget +  " sensitivity!"
            else:
                $ TempSensitivity.changeRes (resTarget, resAmount)
                if resTarget == "Breasts":
                    $ resTarget = "Nipple"
                if resTarget == "Sex":
                    $ resTarget = "Cock"
                $ display = "You gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " sensitivity!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "PermanentlyChangeSensitivity":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ player.BodySensitivity.changeRes (resTarget, resAmount)

            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = resAmount*-1
                if resTarget == "Breasts":
                    $ resTarget = "Nipple"
                if resTarget == "Sex":
                    $ resTarget = "Cock"
                $ display = "You {i}permanently{/i} lost " + str(amountLost) + " " + resTarget +  " sensitivity!"
            else:
                if resTarget == "Breasts":
                    $ resTarget = "Nipple"
                if resTarget == "Sex":
                    $ resTarget = "Cock"
                $ display = "You {i}permanently{/i} gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " sensitivity!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "PermanentChangeStatusEffectResistances":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ player.resistancesStatusEffects.changeRes (resTarget, resAmount)

            if (int(displayingScene.theScene[lineOfScene]) < 0):
                $ amountLost = resAmount*-1

                $ display = "You lost " + str(amountLost) + " " + resTarget +  " resistance!"
            else:
                $ display = "You gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " resistance!"
            if (int(displayingScene.theScene[lineOfScene]) != 0):
                "[display]"

        elif displayingScene.theScene[lineOfScene] == "ChangeFetish":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])


            $ baseFetish = player.getFetish(resTarget)

            $ fetchFetish = getFromName(resTarget, player.FetishList)
            if player.FetishList[fetchFetish].Type == "Fetish":
                while resAmount + baseFetish > 100 and resAmount > 0:
                    $ resAmount-=1

                    if resAmount < 0:
                        $ resAmount = 0


            $ baseFetish += resAmount

            $ player.setFetish(resTarget, baseFetish)

            if (resAmount > 0):
                $ L = 0
                python:
                    for fet in TempFetishes:
                        if fet.name == resTarget and player.FetishList[L].Type == "Fetish":

                            TempFetishes[L].Level += resAmount

                            if TempFetishes[L].Level > 100 - baseFetish + TempFetishes[L].Level and baseFetish <100:
                                TempFetishes[L].Level = 100 - baseFetish + TempFetishes[L].Level
                        L += 1

            if player.FetishList[fetchFetish].Type == "Fetish":

                if baseFetish < 100:
                    if (resAmount > 0):
                        if baseFetish - resAmount == 0:
                            $ display = "You have started getting a fetish for " + resTarget +  "..."
                        elif baseFetish - resAmount < 25 and baseFetish >= 25:
                            $ display = "You have acquired a fetish for " + resTarget +  "."
                        else:
                            $ display = "Your fetish for " + resTarget +  " has intensified!"

                    elif (resAmount < 0):
                        if baseFetish <= 0:
                            $ display = "You have lost your fetish for " + resTarget +  "."
                        else:
                            $ display = "Your fetish for " + resTarget +  " has receded."
                if baseFetish >= 100:
                    if baseFetish >= 100:
                        $ display = "Your fetish for " + resTarget +  " has become a complete and total obsession, but it can't get any worse than it is now...."
                    #elif baseFetish > 10:
                        #$ display = "Fantasies of " + resTarget +  " swirl through your mind as your heart pounds in your chest... You have {i}permanently{/i} gained a fetish level for " + resTarget + ", temporarily bringing your obsessive fetish of " + resTarget +  " to level " + str(fetchFetish) + "..."
                if (int(displayingScene.theScene[lineOfScene]) != 0):
                    "[display]"



        elif displayingScene.theScene[lineOfScene] == "PermanentlyChangeFetish":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ baseFetish = player.getFetish(resTarget)
            $ baseFetish += resAmount

            $ player.setFetish(resTarget, baseFetish)

            $ fetchFetish = getFromName(resTarget, player.FetishList)
            if player.FetishList[fetchFetish].Type == "Fetish":

                if baseFetish < 100:
                    if (int(displayingScene.theScene[lineOfScene]) >= 1):
                        if resAmount > 1:
                            $ display = "You {i}permanently{/i} gained " + str(resAmount) + " fetish levels for " + resTarget +  "..."
                        else:
                            $ display = "You have {i}permanently{/i} gained a fetish level for " + resTarget +  "."

                    elif (int(displayingScene.theScene[lineOfScene]) < 0):
                        $ resAmount *= -1
                        if resAmount > 1:
                            $ display = "You have {i}permanently{/i} lost " + str(resAmount) +" fetish levels for " + resTarget +  "."
                        else:
                            $ display = "You have {i}permanently{/i} lost a fetish level for " + resTarget +  "."
                if baseFetish > 100 and resAmount >= 1:
                    $ display = "Fantasies of " + resTarget +  " swirl through your mind, and your heart beats faster, you have {i}permanently{/i} gained a fetish level for " + resTarget + ", exceeding your normal obsession..."

                if (resAmount != 0):
                    "[display]"
        elif displayingScene.theScene[lineOfScene] == "SetFetish":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ baseFetish = player.getFetish(resTarget)
            $ baseFetish = resAmount

            $ player.setFetish(resTarget, baseFetish)



        elif displayingScene.theScene[lineOfScene] == "IfPlayerOrgasm":
            $ lineOfScene += 1
            if player.stats.hp >= player.stats.max_true_hp:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_5
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "IfPlayerArousalOverPercentOfMax":
            $ lineOfScene += 1
            $ Percentage = float(displayingScene.theScene[lineOfScene])*0.01
            $ lineOfScene += 1
            if player.stats.hp >= player.stats.max_true_hp*Percentage:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_56
                if len(monsterEncounter) > 0:
                    return

        elif displayingScene.theScene[lineOfScene] == "PlayerOrgasm":
            $ lineOfScene += 1
            $ player.stats.hp = 0
            $ spiritLostO = SpiritCalulation(player, int(displayingScene.theScene[lineOfScene]))
            $ player.stats.sp -= spiritLostO
            $ spiritLost += spiritLostO
            call TimeEvent(CardType="PlayerOrgasm", LoopedList=OnPlayerClimaxList) from _call_TimeEvent_4
            #$ spiritLost += int(displayingScene.theScene[lineOfScene])
            #"[spiritLost]"

            if player.stats.sp <= 0:
                $ player.stats.sp = 0
            if player.stats.sp > player.stats.max_true_sp:
                $ player.stats.sp = player.stats.max_true_sp

        elif displayingScene.theScene[lineOfScene] == "EmptySpiritCounter":
            $ spiritLost0 = 0

        elif displayingScene.theScene[lineOfScene] == "PlayerOrgasmNoSpiritLoss":
            $ player.stats.hp = 0
            $ spiritLost0 = SpiritCalulation(player, 0)

            call TimeEvent(CardType="PlayerOrgasm", LoopedList=OnPlayerClimaxList) from _call_TimeEvent_5


        elif displayingScene.theScene[lineOfScene] == "IfPlayerEnergyLessThanPercent":
            $ lineOfScene += 1
            $ percentCheck = (int(displayingScene.theScene[lineOfScene]))*0.01
            $ lineOfScene += 1

            if player.stats.ep <= player.stats.max_true_ep*percentCheck:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_59
                if len(monsterEncounter) > 0:
                    return

        elif displayingScene.theScene[lineOfScene] == "IfPlayerEnergyGone":
            $ lineOfScene += 1
            if player.stats.ep <= 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_60
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "IfPlayerSpiritGone":
            $ lineOfScene += 1
            if player.stats.sp <= 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_6
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "IfHasItem":
            $ lineOfScene += 1
            $ hasThing = 0
            python:
                if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                for each in player.inventory.items:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        hasThing = 1
            if hasThing == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_24
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfHasItemInInventory":
            $ lineOfScene += 1
            $ ItemName = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ hasThing = 0
            python:
                for each in player.inventory.items:
                    if each.name == ItemName:
                        if each.NumberHeld >= int(displayingScene.theScene[lineOfScene]):
                            hasThing = 1

            if hasThing == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_23
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfDoesntHaveItem":
            $ lineOfScene += 1
            $ hasThing = 0
            python:
                if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                for each in player.inventory.items:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        hasThing = 1
            if hasThing == 0:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_63
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfHasItemEquipped":
            $ lineOfScene += 1
            $ hasThing = 0
            python:
                if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1
                if player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                    hasThing = 1

            if hasThing == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_69
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "IfHasSkill":
            $ lineOfScene += 1
            $ passSkillCheck = 0
            python:
                for each in  player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passSkillCheck = 1
            $ lineOfScene += 1

            if passSkillCheck == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD
                if len(monsterEncounter) > 0:
                    return

        elif displayingScene.theScene[lineOfScene] == "IfHasPerk":
            $ lineOfScene += 1
            $ hasThing = 0
            python:
                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        hasThing = 1
            if hasThing == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_25
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfSensitivityEqualOrGreater":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            if player.BodySensitivity.getRes(resTarget) >= resAmount:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_57
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfHasFetish":
            $ lineOfScene += 1
            if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_13
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfFetishLevelEqualOrGreater":
            $ lineOfScene += 1
            $ fetchFetish = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ fetishLvl = int(displayingScene.theScene[lineOfScene])

            if player.getFetish(fetchFetish) >= fetishLvl:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_28
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1


        elif displayingScene.theScene[lineOfScene] == "Menu":
            $ index = 0
            $ lineOfScene += 1
            $ MenuLineSceneCheckMark = copy.deepcopy(lineOfScene)

            #$ check = ProgressEvent[DataLocation].choices[1]
            #"[check]"

            label recheckMenu:
                $ ind = index
                $ lineOfScene = copy.deepcopy(MenuLineSceneCheckMark)
                $ menuArray = []
                $ passedArray = []


            $ MaxMenuSlots = 6
            if displayingScene.theScene[lineOfScene] == "MaxMenuSlots":
                $ lineOfScene += 1
                $ MaxMenuSlots = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

            $ eventMenuJumps = []
            $ eventMenuSceneJumps = []
            $clear1 = 0
            $clear2 = 0
            $clear3 = 0
            $clear4 = 0
            $clear5 = 0
            $clear6 = 0

            $ display1 = ""
            $ display2 = ""
            $ display3 = ""
            $ display4 = ""
            $ display5 = ""
            $ display6 = ""

            $ finalOption = ""
            $ finalOptionEvent = ""
            $ finalOptionEventScene = ""
            $ finalSet = 0

            $ ShuffleMenuOptions = 0
            #$ showOnSide = 1
            while displayingScene.theScene[lineOfScene] != "EndLoop":

                $ passcheck = 0
                $ override = ""
                $ display = ""
                $ eventMenuJumps.append("")
                $ eventMenuSceneJumps.append("")

                $ passcheck = SceneRequiresCheck()

                #"[override]"

                if override != "":
                    python:
                        ova = 0
                        for each in menuArray:
                            if each == override:
                                del menuArray[ova]
                                del passedArray[ova]
                                del eventMenuJumps[ova]
                                del eventMenuSceneJumps[ova]
                                ova -= 1
                            ova +=1

                if displayingScene.theScene[lineOfScene] != "EndLoop":

                    if passcheck == 1 :
                        $ display = ""
                        $ display = displayingScene.theScene[lineOfScene]
                        $ passedArray.append(1)

                    else:
                        if display != "":
                            $ passedArray.append(0)
                if display != "":
                    $ menuArray.append(copy.deepcopy(display))
                else:
                    $ del eventMenuJumps[-1]
                    $ del eventMenuSceneJumps[-1]


                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    $ lineOfScene += 1

            if ShuffleMenuOptions == 1:
                $ menuArrays = list(zip(menuArray, passedArray, eventMenuJumps, eventMenuSceneJumps))
                $ random.shuffle(menuArrays)
                $ menuArray, passedArray, eventMenuJumps, eventMenuSceneJumps = zip(*menuArrays)


            $ choiceName = ""

            $ exist1 = 0
            $ exist2 = 0
            $ exist3 = 0
            $ exist4 = 0
            $ exist5 = 0
            $ exist6 = 0

            $ setEventJump1 = ""
            $ setEventJump2 = ""
            $ setEventJump3 = ""
            $ setEventJump4 = ""
            $ setEventJump5 = ""
            $ setEventJump6 = ""

            $ setEventSceneJump1 = ""
            $ setEventSceneJump2 = ""
            $ setEventSceneJump3 = ""
            $ setEventSceneJump4 = ""
            $ setEventSceneJump5 = ""
            $ setEventSceneJump6 = ""



            if finalOption != "" and finalSet == 0:
                python:
                    ova = 0
                    for each in menuArray:
                        if each == finalOption:
                            del menuArray[ova]
                            del passedArray[ova]
                            del eventMenuJumps[ova]
                            del eventMenuSceneJumps[ova]
                            ova -= 1
                        ova +=1

                if MaxMenuSlots == 6:
                    $ MaxMenuSlots = 5

            if len(menuArray) > MaxMenuSlots:
                show screen MenuPageButtons
            else:
                hide screen MenuPageButtons

            while ind < len(menuArray):
                if display1 == ""and MaxMenuSlots >= 1:
                    $ display1 = menuArray[ind]
                    $ clear1 = passedArray[ind]
                    $ setEventJump1 = eventMenuJumps[ind]
                    $ setEventSceneJump1 = eventMenuSceneJumps[ind]
                elif display2 == "" and MaxMenuSlots >= 2:
                    $ display2 = menuArray[ind]
                    $ clear2 = passedArray[ind]
                    $ setEventJump2 = eventMenuJumps[ind]
                    $ setEventSceneJump2 = eventMenuSceneJumps[ind]
                elif display3 == "" and MaxMenuSlots >= 3:
                    $ display3 = menuArray[ind]
                    $ clear3 = passedArray[ind]
                    $ setEventJump3 = eventMenuJumps[ind]
                    $ setEventSceneJump3 = eventMenuSceneJumps[ind]
                elif display4 == "" and MaxMenuSlots >= 4:
                    $ display4 = menuArray[ind]
                    $ clear4 = passedArray[ind]
                    $ setEventJump4 = eventMenuJumps[ind]
                    $ setEventSceneJump4 = eventMenuSceneJumps[ind]
                elif display5 == "" and MaxMenuSlots >= 5:
                    $ display5 = menuArray[ind]
                    $ clear5 = passedArray[ind]
                    $ setEventJump5 = eventMenuJumps[ind]
                    $ setEventSceneJump5 = eventMenuSceneJumps[ind]
                elif display6 == "" and finalOption == "" and MaxMenuSlots >= 6:
                    $ display6 = menuArray[ind]
                    $ clear6 = passedArray[ind]
                    $ setEventJump6 = eventMenuJumps[ind]
                    $ setEventSceneJump6 = eventMenuSceneJumps[ind]
                $ ind +=1


            if display1 != "":
                $ exist1 = 1
            if display2 != "":
                $ exist2 = 1
            if display3 != "":
                $ exist3 = 1
            if display4 != "":
                $ exist4 = 1
            if display5 != "":
                $ exist5 = 1
            if finalOption != "" and finalSet == 0:
                $ finalSet =1
            elif display6 != "":
                $ exist6 = 1



            $ damageToPlayer =" {i}" + critText +  effectiveText+ "{/i}You gain " + str(finalDamage) + " arousal."
            if len(monsterEncounter) > 0 and CombatFunctionEnemytarget < len(monsterEncounter):
                $ damageToEnemy = " {i}" + critText +  effectiveText +"{/i}" + monsterEncounter[CombatFunctionEnemytarget].name + " gains " + str(finalDamage) + " arousal."
            else:
                $ damageToEnemy = ""

            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ progressDisplay = copy.deepcopy(ProgressEvent[DataLocation].eventProgress)

            if savedLine != "" and savedLineInMenu == 1:
                $ LastLine = copy.deepcopy(savedLine)
                $ savedLine = ""
                $ savedLineInMenu = 0
            elif LastLine != "StartCombat" and LastLine != "EndLoop" and LastLine != "end":
                $ LastLine = returnReaderDiction(LastLine)
            else:
                $ LastLine = ""


            call playSpecialEffects(VisualEffect, 1) from _call_playSpecialEffects
            call playSpecialEffects(VisualEffect2, 2) from _call_playSpecialEffects_1
            call playSpecialEffects(VisualEffect3, 3) from _call_playSpecialEffects_2

            show screen fakeTextBox
            window hide

            menu menuList:
                "[display1]" if exist1 == 1:
                    if clear1 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump1 == "":
                            $ display = display1
                            $ choiceName = display1
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_9
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump1, EventDatabase)
                            if setEventSceneJump1 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump1, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu
                        if len(monsterEncounter) > 0:
                            return
                "[display2]" if exist2 == 1 :
                    if clear2 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump2 == "":
                            $ display = display2
                            $ choiceName = display2
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_10
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump2, EventDatabase)
                            if setEventSceneJump2 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump2, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu_1
                        if len(monsterEncounter) > 0:
                            return
                "[display3]" if exist3 == 1:
                    if clear3 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump3 == "":
                            $ display = display3
                            $ choiceName = display3
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_14
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump3, EventDatabase)
                            if setEventSceneJump3 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump3, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu_2
                        if len(monsterEncounter) > 0:
                            return
                "[display4]" if exist4 == 1:
                    if clear4 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump4 == "":
                            $ display = display4
                            $ choiceName = display4
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_16
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump4, EventDatabase)
                            if setEventSceneJump4 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump4, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu_3
                        if len(monsterEncounter) > 0:
                            return
                "[display5]" if exist5 == 1:
                    if clear5 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump5 == "":
                            $ display = display5
                            $ choiceName = display5
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_18
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump5, EventDatabase)
                            if setEventSceneJump5 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump5, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu_4
                        if len(monsterEncounter) > 0:
                            return
                "[display6]" if exist6 == 1 :
                    if clear6 == 1:
                        hide screen MenuPageButtons
                        hide screen fakeTextBox
                        if setEventJump6 == "":
                            $ display = display6
                            $ choiceName = display6
                            $ MenuLineSceneCheckMark = -1
                            call sortMenuD from _call_sortMenuD_19
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ isEventNow = 1
                            $ currentChoice = 0
                            $ DataLocation = getFromName(setEventJump6, EventDatabase)
                            if setEventSceneJump6 != "":
                                $ currentChoice = getFromNameOfScene(setEventSceneJump6, EventDatabase[DataLocation].theEvents)
                            jump sortMenuD
                    else:
                        call recheckMenu from _call_recheckMenu_5
                        if len(monsterEncounter) > 0:
                            return
                "[finalOption]" if hasattr(store, "finalSet") and finalSet == 1:
                    hide screen MenuPageButtons
                    hide screen fakeTextBox
                    if finalOptionEvent == "":
                        $ display = finalOption
                        $ choiceName = finalOption
                        $ MenuLineSceneCheckMark = -1
                        call sortMenuD from _call_sortMenuD_82
                        if len(monsterEncounter) > 0:
                            return
                    else:
                        $ isEventNow = 1
                        $ currentChoice = 0
                        $ DataLocation = getFromName(finalOptionEvent, EventDatabase)
                        if finalOptionEventScene != "":
                            $ currentChoice = getFromNameOfScene(finalOptionEventScene, EventDatabase[DataLocation].theEvents)
                        jump sortMenuD



        elif displayingScene.theScene[lineOfScene] == "StatCheck":
                $ checkStat = 0
                $ lineOfScene += 1

                $ checkPreFuncs = 0
                while checkPreFuncs == 0:
                    if displayingScene.theScene[lineOfScene] == "ChangeStatCheckDifficulty":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] == "IfEncounterSizeGreaterOrEqualTo":
                            if len(monsterEncounter) > 0:
                                $ lineOfScene += 1
                                if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
                                    $ lineOfScene += 1
                                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                                else:
                                    $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfEncounterSizeLessOrEqualTo":
                            if len(monsterEncounter) > 0:
                                $ lineOfScene += 1
                                if len(monsterEncounter) <= int(displayingScene.theScene[lineOfScene]):
                                    $ lineOfScene += 1
                                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                                else:
                                    $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffect":
                            if len(monsterEncounter) > 0:
                                $ lineOfScene += 1
                                if player.statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                                    $ lineOfScene += 1
                                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                                else:
                                    $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffectWithPotencyEqualOrGreater":
                            if len(monsterEncounter) > 0:
                                $ lineOfScene += 1
                                $ statusEffectChek = displayingScene.theScene[lineOfScene]
                                $ lineOfScene += 1
                                $ potencyChek = int(displayingScene.theScene[lineOfScene])

                                $ TheCheck = player.statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek)

                                if TheCheck == True:
                                    $ lineOfScene += 1
                                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                                else:
                                    $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfHasFetish":
                            $ lineOfScene += 1
                            if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfFetishLevelEqualOrGreater":
                            $ lineOfScene += 1
                            $ fetchFetish = displayingScene.theScene[lineOfScene]
                            $ lineOfScene += 1
                            $ fetishLvl = int(displayingScene.theScene[lineOfScene])

                            if player.getFetish(fetchFetish) >= fetishLvl:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfVirilityEqualsOrGreater":
                            $ lineOfScene += 1

                            if int(displayingScene.theScene[lineOfScene]) <= getVirility(player) :
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfMonsterLevelGreaterThan":
                            $ lineOfScene += 1
                            if monsterEncounter[CombatFunctionEnemytarget].stats.lvl >= int(displayingScene.theScene[lineOfScene]):
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfProgressEqualsOrGreater":
                            $ lineOfScene += 1
                            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
                            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfHasPerk":
                            $ lineOfScene += 1
                            $ hasThing = 0
                            python:
                                for each in player.perks:
                                    if each.name == displayingScene.theScene[lineOfScene]:
                                        hasThing = 1
                            if hasThing == 1:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "GetAnEventsProgressThenIfEqualsOrGreater":
                            $ lineOfScene += 1
                            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                            $ lineOfScene += 1
                            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "IfChoice":
                            $ lineOfScene += 1
                            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
                            $ lineOfScene += 1
                            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

                            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                                $ ProgressEvent[DataLocation].choices.append("")

                            if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "GetEventAndIfChoice":
                            $ lineOfScene += 1
                            $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                            $ lineOfScene += 1
                            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

                            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                                $ ProgressEvent[CheckEvent].choices.append("")

                            $ lineOfScene += 1
                            if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
                                $ lineOfScene += 1
                                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                            else:
                                $ lineOfScene += 1
                        else:
                            $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                    else:
                        $ checkPreFuncs += 1

                $ statType = displayingScene.theScene[lineOfScene]
                $ maxStatDisplay = ""
                if statType == "Temptation":
                    $ statToCheck = int(math.floor(  (player.stats.Int-5)*0.1 + (player.stats.Willpower-5)*0.2 + (player.stats.Allure-5)*0.1  ))
                    if statToCheck >= 15:
                        $ statToCheck = 15
                        $ maxStatDisplay = "(Max)"
                else:
                    $ statToCheck = int(math.floor((player.stats.getStat(displayingScene.theScene[lineOfScene])-5)*0.15))

                $ lineOfScene += 1
                $ opposedCheck = int(displayingScene.theScene[lineOfScene]) + increaseStatCheck

                #luck part
                $ luckDie = int(math.floor(player.stats.getStat("Luck")*0.20))

                if luckDie == 0:
                    $ luckDie = 1
                if luckDie < 1:
                    $ luckAddition = renpy.random.randint(luckDie,1)
                else:
                    $ luckAddition = renpy.random.randint(1,luckDie)

                #perk application
                $ minDie = 1
                python:
                    for perk in player.perks:
                        p = 0
                        while  p < len(perk.PerkType):
                            if perk.PerkType[p] == "MinStatCheckDie":
                                minDie += perk.EffectPower[p]
                            p += 1

                #roll!
                $ randomRoll = renpy.random.randint(minDie,20)

                $ defenceBonus = 0
                #defence bonus for stat check!
                if statType == "Technique" or statType == "Power" or statType == "Willpower" or statType == "Intelligence" or statType == "Temptation":
                    if (player.statusEffects.defend.duration > 0):
                        if player.statusEffects.defend.potency == 0:
                            $ defenceBonus = 5
                        elif player.statusEffects.defend.potency == 1:
                            $ defenceBonus = 3
                        else:
                            $ defenceBonus = 1
                $ defLine = ""
                if defenceBonus != 0:
                    $ defLine = " + Defend Bonus: +" + str(defenceBonus)

                #defence bonus for stat check!
                if statType == "Temptation":
                    if (player.statusEffects.charmed.duration > 0):
                        $ opposedCheck += 1

                #add it all together then make the display line
                $ combinedCheck = statToCheck + randomRoll + luckAddition + defenceBonus
                if statType == "Temptation":
                    $ showing = "Temptation Check!\nRoll d20: " + str(randomRoll) + " + Will*0.2 + Int*0.1 + Allure*0.1 - 2: " + str(statToCheck) + maxStatDisplay + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."
                else:
                    $ showing = statType + " Stat Check!\nRoll d20: " + str(randomRoll) + " + (" + statType + "-5)*0.15: " + str(statToCheck) + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."

                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                if combinedCheck >= opposedCheck and player.statusEffects.hasThisStatusEffect("Surrender") == False:
                    $ checkStat = 1
                    $ showing += "  PASS!"
                    "[showing]"
                    $ increaseStatCheck = 0
                    call sortMenuD from _call_sortMenuD_12
                    if len(monsterEncounter) > 0:
                        return
                else:
                    $ lineOfScene += 1
                    $ showing += "  FAILED!"
                    #"[showing]"
                    $ OpposingCost = ((int(math.floor(opposedCheck / 5)))*20) -10
                    $ DefendingCost = ((int(math.floor(statToCheck*0.75)))*5)
                    $ surpassEnergyCost =  ((int(math.floor(opposedCheck / 5)))*20)  - ((int(math.floor(statToCheck*0.75)))*5) - 10
                    if surpassEnergyCost < 10:
                        $ surpassEnergyCost = 10
                    $ LastLine =  showing + " Surpass your failure for " + str(surpassEnergyCost) + " Energy?"

                    if statType == "Temptation":
                        $ LastLine += "\n\n"  + "Check(" + str(opposedCheck) + "): " + str(OpposingCost) + "EP - " + "Temptation Res" + "(" + str(statToCheck) + "): " + str(DefendingCost) + "EP = " + str(surpassEnergyCost) + "EP Cost. (Min 10)"
                    else:
                        $ LastLine += "\n\n"  + "Check(" + str(opposedCheck) + "): " + str(OpposingCost) + "EP - " + statType + "(" + str(statToCheck) + "): " + str(DefendingCost) + "EP = " + str(surpassEnergyCost) + "EP Cost. (Min 10)"

                    if player.statusEffects.hasThisStatusEffect("Surrender") == True:
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ checkStat = 1
                        $ increaseStatCheck = 0
                        call sortMenuD from _call_sortMenuD_85
                        if len(monsterEncounter) > 0:
                            return
                    else:

                        show screen fakeTextBox
                        window hide
                        label surpassMenuBlip:
                        menu surpassMenu:
                            "Surpass Failure for [surpassEnergyCost] Energy." if player.stats.ep >= surpassEnergyCost:
                                $ player.stats.ep -= surpassEnergyCost
                                $ increaseStatCheck = 0
                                hide screen fakeTextBox
                                call sortMenuD from _call_sortMenuD_29
                                if len(monsterEncounter) > 0:
                                    return

                            "You don't have the Energy to resist." if player.stats.ep < surpassEnergyCost:
                                #jump surpassMenuBlip
                                hide screen fakeTextBox
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                                $ checkStat = 1
                                $ increaseStatCheck = 0
                                call sortMenuD from _call_sortMenuD_84
                                if len(monsterEncounter) > 0:
                                    return

                            "Give up." if player.stats.ep >= surpassEnergyCost:

                                hide screen fakeTextBox
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                                $ checkStat = 1
                                $ increaseStatCheck = 0
                                call sortMenuD from _call_sortMenuD_11
                                if len(monsterEncounter) > 0:
                                    return






                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "StatCheckRollUnder":
                $checkStat = 0
                while checkStat != 1:
                    $ lineOfScene += 1
                    if(displayingScene.theScene[lineOfScene] == "Fail"):
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ checkStat = 1
                        call sortMenuD from _call_sortMenuD_52
                        if len(monsterEncounter) > 0:
                            return
                    else:
                        $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
                        $ statType = displayingScene.theScene[lineOfScene]
                        $ lineOfScene += 1
                        $ randomRoll = renpy.random.randint(0,20)
                        $ combinedCheck = statToCheck + randomRoll
                        $ showing = statType + " Stat Check, roll under the value! Rolled: " + str(randomRoll) + " + Stat: " + str(statToCheck) + ".\n" + str(combinedCheck) + " vs " + displayingScene.theScene[lineOfScene] + "."
                        if combinedCheck >= int(displayingScene.theScene[lineOfScene]):
                            $ lineOfScene += 1
                            $ display = displayingScene.theScene[lineOfScene]
                            $ checkStat = 1
                            $ showing += "\nFAILED!"
                            "[showing]"
                            call sortMenuD from _call_sortMenuD_53
                            if len(monsterEncounter) > 0:
                                return
                        else:
                            $ lineOfScene += 1
                            $ showing += "\nPASS!"
                            "[showing]"
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "StatEqualsOrMore":
            $ lineOfScene += 1
            $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if statToCheck >= int(displayingScene.theScene[lineOfScene]):
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                $ checkStat = 1
                call sortMenuD from _call_sortMenuD_21
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "ClearNonPersistentStatusEffects":
            $ player = ClearNonPersistentEffects(player)


        elif displayingScene.theScene[lineOfScene] == "ApplyStatusEffect":
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ statusSkill = SkillsDatabase[skillAt]

            if statusSkill.statusEffect != "Damage" and statusSkill.statusEffect != "Defence" and statusSkill.statusEffect != "Power" and statusSkill.statusEffect != "Technique" and statusSkill.statusEffect != "Willpower" and statusSkill.statusEffect != "Intelligence" and statusSkill.statusEffect != "Allure" and statusSkill.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and statusSkill.statusEffect != "Escape" and statusSkill.statusEffect != "Crit":
                if len(monsterEncounter) > 0:
                    $ player = statusAfflict(player, statusSkill, monsterEncounter[CombatFunctionEnemytarget])
                else:
                    $ player = statusAfflict(player, statusSkill)
            else:
                if len(monsterEncounter) > 0:
                    $ holder = statusBuff(player, monsterEncounter[CombatFunctionEnemytarget], statusSkill, 1)
                else:
                    $ holder = statusBuff(player, player, statusSkill, 1)

                $ player = holder[0]

            if statusSkill.statusEffect == "Restrain":
                $ player.restraintStruggle = copy.deepcopy(statusSkill.restraintStruggle)
                $ player.restraintStruggleCharmed = copy.deepcopy(statusSkill.restraintStruggleCharmed)
                $ player.restraintEscaped = copy.deepcopy(statusSkill.restraintEscaped)
                $ player.restraintEscapedFail = copy.deepcopy(statusSkill.restraintEscapedFail)
                if len(monsterEncounter) >= 1:
                    $ player.restrainer = monsterEncounter[CombatFunctionEnemytarget]


        elif displayingScene.theScene[lineOfScene] == "CombatEncounter":

            $ lineOfScene += 1
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ monNum = 0
            $ runBG = ""
            $ runAndStayInEvent = 0
            $ checkPreFuncs = 0
            $ combatItems = 0

            while checkPreFuncs == 0:
                if displayingScene.theScene[lineOfScene] == "NoRunning":
                    $ canRun = False
                    $ lineOfScene += 1

                elif displayingScene.theScene[lineOfScene] == "SetBGOnRun":
                    $ lineOfScene += 1
                    $ runBG = changeBG(displayingScene.theScene[lineOfScene])
                    $ lineOfScene += 1
                elif displayingScene.theScene[lineOfScene] == "DenyInventory":
                    $ combatItems = 1
                    $ lineOfScene += 1
                elif displayingScene.theScene[lineOfScene] == "RunningWontSkipEvent":
                    $ runAndStayInEvent = 1
                    $ lineOfScene += 1
                else:
                    $ checkPreFuncs += 1


            while displayingScene.theScene[lineOfScene] != "StartCombat":
                $ insertToLocation = len(monsterEncounter)
                $ addMonsterTo(displayingScene.theScene[lineOfScene], monsterEncounter, insertToLocation)
                #$ monsterEncounter[monNum] = monsterEncounter[monNum].statusEffects.refresh( monsterEncounter[monNum])
                $ addMonsterTo(displayingScene.theScene[lineOfScene], trueMonsterEncounter, insertToLocation)
                #$ trueMonsterEncounter[monNum] = trueMonsterEncounter[monNum].statusEffects.refresh(trueMonsterEncounter[monNum])
                $ lineOfScene += 1
                $ checkPreFuncs = 0
                while checkPreFuncs == 0:
                    if displayingScene.theScene[lineOfScene] == "ApplyStance":
                        $ lastAttack = Skill()
                        $ lineOfScene += 1
                        $ givingStance = displayingScene.theScene[lineOfScene]
                        $ lineOfScene += 1
                        python:
                            try:
                                if displayingScene.theScene[lineOfScene] == "SetAttack":
                                    lineOfScene += 1
                                    lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                                else:
                                    lineOfScene -= 1
                            except:
                                lineOfScene -= 1
                        $ monsterEncounter[monNum].giveStance(givingStance, player, lastAttack)
                        $ player.giveStance(givingStance, monsterEncounter[monNum], lastAttack)
                        $ lineOfScene += 1
                    elif displayingScene.theScene[lineOfScene] == "Restrainer":
                        $ player.restrainer = monsterEncounter[monNum]
                        $ lineOfScene += 1
                    else:
                        $ checkPreFuncs += 1
                $ monNum += 1
            $ monsterEncounter = NumberMonsters(monsterEncounter)
            $ SceneCharacters = []
            if len(monsterEncounter) > 0:
                $ HoldingSceneForCombat = copy.deepcopy(displayingScene)
                $ HoldingLineForCombat = copy.deepcopy(lineOfScene)
                $ HoldingDataLocForCombat = copy.deepcopy(DataLocation)
                call combat from _call_combat_1
                label endCombatCalled:
                if HoldingSceneForCombat != Dialogue():
                    #$ test = HoldingSceneForCombat[HoldingLineForCombat].NameOfScene
                    $ displayingScene = copy.deepcopy(HoldingSceneForCombat)
                    $ lineOfScene = copy.deepcopy(HoldingLineForCombat)
                    $ DataLocation = copy.deepcopy(HoldingDataLocForCombat)
                    $ HoldingSceneForCombat = Dialogue()
                    $ HoldingLineForCombat = 0
                    $ HoldingDataLocForCombat = 0

            $ stunnedGridPlayer = 0


        elif displayingScene.theScene[lineOfScene] == "IfInExploration":
            $ lineOfScene += 1
            if onAdventure == 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_61
                if len(monsterEncounter) > 0:
                    return

        elif displayingScene.theScene[lineOfScene] == "JumpToScene":
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]

            call sortMenuD from _call_sortMenuD_20

            if len(monsterEncounter) > 0:
                return
        elif displayingScene.theScene[lineOfScene] == "JumpToRandomScene":
            $ lineOfScene += 1

            $ randomSelection = []

            while displayingScene.theScene[lineOfScene] != "EndLoop":
                $ passcheck = 0
                $ display = ""
                $ passcheck = SceneRequiresCheck()

                if passcheck == 1:
                    $ randomSelection.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

            $ renpy.random.shuffle(randomSelection)
            $ display = randomSelection[0]
            $ randomSelection = []
            call sortMenuD from _call_sortMenuD_22
            if len(monsterEncounter) > 0:
                return
        elif displayingScene.theScene[lineOfScene] == "JumpToEvent":
            $ lineOfScene += 1
            $ DialogueIsFrom = "Event"
            $ isEventNow = 1
            $ currentChoice = 0
            $ Speaker = Character(_(''))
            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)

            jump sortMenuD
        elif displayingScene.theScene[lineOfScene] == "JumpToEventThenScene":
            $ lineOfScene += 1
            $ DialogueIsFrom = "Event"
            $ isEventNow = 1
            $ currentChoice = 0
            $ Speaker = Character(_(''))
            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
            $ lineOfScene += 1
            $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

            jump sortMenuD

        elif displayingScene.theScene[lineOfScene] == "CallNextSceneJumpThenReturn":
            $ callNextJump = 2
            $ inCalledSceneJump = 2

            $ specifyCurrentChoice = 0
            $ showingDream = []

            label playSceneJump:
                if callNextJump == 1:
                    $ specifyCurrentChoice = getFromNameOfScene(display, EventDatabase[DataLocation].theEvents)
                    $ showingDream.append(copy.deepcopy(EventDatabase[DataLocation]))
                    $ callNextJump = 0
                    $ inCalledSceneJump = 0
                    call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_17
                    return

        elif displayingScene.theScene[lineOfScene] == "CallSceneThenReturn":
            $ lineOfScene += 1
            $ specifyCurrentChoice = 0
            $ specifyCurrentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

            $ showingDream = []
            $ showingDream.append(copy.deepcopy(EventDatabase[DataLocation]))
            call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_8


        elif displayingScene.theScene[lineOfScene] == "CallEventAndSceneThenReturn":
            $ lineOfScene += 1

            $ specifyDataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)

            $ lineOfScene += 1
            $ specifyCurrentChoice = 0
            $ specifyCurrentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[specifyDataLocation].theEvents)

            $ showingDream = []
            $ showingDream.append(copy.deepcopy(EventDatabase[specifyDataLocation]))

            call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_9


        elif displayingScene.theScene[lineOfScene] == "CallCombatEventAndScene":
            $ lineOfScene += 1
            $ DialogueIsFrom = "Event"
            $ isEventNow = 1
            $ currentChoice = 0
            $ HideOrgasmLine = 1

            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
            $ lineOfScene += 1
            $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

            call sortMenuD from _call_sortMenuD_30
            return
        elif displayingScene.theScene[lineOfScene] == "JumpToNPCEvent":
            $ lineOfScene += 1
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ EnteringLocationCheck = 0
            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
            jump sortMenuD
        elif displayingScene.theScene[lineOfScene] == "JumpToNPCEventThenScene":
            $ lineOfScene += 1
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0

            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
            $ lineOfScene += 1
            $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)
            $ EnteringLocationCheck = 0
            jump sortMenuD
        elif displayingScene.theScene[lineOfScene] == "JumpToLossEvent":
            hide screen ON_EnemyCardScreen
            $ lineOfScene += 1
            $ DialogueIsFrom = "LossEvent"
            $ isEventNow = 1
            $ currentChoice = 0

            $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
            jump sortMenuD

############################################### Grid map functions ########################################################

        elif displayingScene.theScene[lineOfScene] == "ExitGridmap":
            $ onGridMap = 0
            $ runAndStayInEvent = 0
            $ RanAway = "False"
            hide screen Gridmap
            hide screen GridmapPlayer
            hide screen GridmapNPCs
            hide screen GridmapObstacles
            $ TheGrid = []

        elif displayingScene.theScene[lineOfScene] == "StunGridPlayer":
            $ lineOfScene += 1
            $ stunnedGridPlayer = int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "IfGridPlayerStunned":
            $ lineOfScene += 1
            if stunnedGridPlayer > 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_87
            if len(monsterEncounter) > 0:
                return

        elif displayingScene.theScene[lineOfScene] == "RemoveGridNPC":
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "Current":
                $ del ActiveGridNPCs[currentGridNPC]
            elif displayingScene.theScene[lineOfScene] == "Specific":
                $ lineOfScene += 1
                $ passcheck = 0
                $ currentGridNPC = 0
                $ v = 0
                python:
                    for each in ActiveGridNPCs:
                        if each.name == displayingScene.theScene[lineOfScene]:
                            currentGridNPC = copy.deepcopy(v)
                            passcheck = 1
                        v += 1
                $ del ActiveGridNPCs[currentGridNPC]

            $ currentGridNPC -= 1

        elif displayingScene.theScene[lineOfScene] == "SetPlayerGridPosition":
            $ lineOfScene += 1
            $ startplayerpos[0] = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ startplayerpos[1] = int(displayingScene.theScene[lineOfScene])
            $ playerCoord = startplayerpos
            $ GridPXpos = GridMovement*playerCoord[0]
            $ GridPYpos = GridMovement*playerCoord[1]
            $ GridPXposPrior = GridPXpos
            $ GridPYposPrior = GridPYpos

        elif displayingScene.theScene[lineOfScene] == "ChangeGridNPCMovement":
            $ lineOfScene += 1
            $ ActiveGridNPCs[currentGridNPC].Movement = displayingScene.theScene[lineOfScene]
            if ActiveGridNPCs[currentGridNPC].Movement != "Wander":
                $ lineOfScene += 1
                if  displayingScene.theScene[lineOfScene] == "Coord":
                    $ ActiveGridNPCs[currentGridNPC].MovementTarget = "TargetSet"
                    $ lineOfScene += 1
                    $ ActiveGridNPCs[currentGridNPC].TargetCoords[0]
                    $ lineOfScene += 1
                    $ ActiveGridNPCs[currentGridNPC].TargetCoords[1]
                else:
                    $ ActiveGridNPCs[currentGridNPC].MovementTarget = displayingScene.theScene[lineOfScene]

                    if ActiveGridNPCs[currentGridNPC].Movement == "Whimsical":
                        $ lineOfScene += 1
                        $ ActiveGridNPCs[currentGridNPC].WhimsyRange = int(displayingScene.theScene[lineOfScene])
                        $ ActiveGridNPCs[currentGridNPC].MovementVector=[-1,-1]

        elif displayingScene.theScene[lineOfScene] == "IfGridNPCSeesPlayer":
            $ lineOfScene += 1
            $ passcheck = 1
            $ NPCSeeRange = -1
            $ walls= 1
            if displayingScene.theScene[lineOfScene] == "IgnoreWalls":
                $ lineOfScene += 1
                $ walls= 0
            $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), (playerCoord[0], playerCoord[1]), tileset, ActiveGridNPCs, walls )
            if displayingScene.theScene[lineOfScene] == "Range":
                $ lineOfScene += 1
                $ NPCSeeRange = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

            if NPCSeeRange > 0:
                if len(Path) > NPCSeeRange + 1:
                    $ passcheck = 0

            if walls == 1:
                python:
                    for each in Path:
                        if  tileset[FindTileType(TheGrid[each[1]][each[0]], tileset)][2] == "Wall":
                            passcheck = 0

            if passcheck == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_88
            if len(monsterEncounter) > 0:
                return

        elif displayingScene.theScene[lineOfScene] == "IfGridNPCThere":
            $ lineOfScene += 1
            $ passcheck = 0
            python:
                for each in ActiveGridNPCs:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passcheck = 1
            $ lineOfScene += 1
            if passcheck == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_89
            if len(monsterEncounter) > 0:
                return
        elif displayingScene.theScene[lineOfScene] == "ChangeGridVision":
            $ lineOfScene += 1
            $ PlayerGridSight = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "IfGridVisonOn":
            $ lineOfScene += 1
            if PlayerGridSight != 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_90
            if len(monsterEncounter) > 0:
                return

        elif displayingScene.theScene[lineOfScene] == "SpawnGridNPC":
            $ lineOfScene += 1
            $ newNPC = copy.deepcopy(TheGridNPCs[getFromName(displayingScene.theScene[lineOfScene], TheGridNPCs)] )
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "Here":
                $ newNPC.coord[0] = ActiveGridNPCs[currentGridNPC].coord[0]
                $ newNPC.coord[1] = ActiveGridNPCs[currentGridNPC].coord[1]
            else:
                $ newNPC.coord[0] = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
                $ newNPC.coord[1] = int(displayingScene.theScene[lineOfScene])

            $ newNPC.GridposX = GridMovement*newNPC.coord[0]
            $ newNPC.GridposY = GridMovement*newNPC.coord[1]
            $ newNPC.GridposXPrior = newNPC.GridposX
            $ newNPC.GridposYPrior = newNPC.GridposY

            $ ActiveGridNPCs.append(copy.deepcopy(newNPC))

        elif displayingScene.theScene[lineOfScene] == "ChangeMapTile":
            $ lineOfScene += 1
            $ coordX = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ coordY = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ newTile = displayingScene.theScene[lineOfScene]
            $ TheGrid[coordY][coordX] = newTile

        elif displayingScene.theScene[lineOfScene] == "GoToMap":
            $ startplayerpos = [0,0]
            $ onGridMap = 1
            $ tileset = []
            $ TheGrid = []
            $ TheGridNPCs = []
            $ ActiveGridNPCs = []
            $ gridStepLine = ""
            $ PlayerGridSight = 0
            $ stunnedGridPlayer = 0

            $ display = ""
            $ toggledGridEvent = 0
            while displayingScene.theScene[lineOfScene] != "StartMap":
                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "StartMap":
                    if displayingScene.theScene[lineOfScene] == "Tileset":
                        while displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ Tile = []
                            $ lineOfScene += 1
                            if displayingScene.theScene[lineOfScene] != "EndLoop":
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ lineOfScene += 1
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ lineOfScene += 1
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ lineOfScene += 1
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ lineOfScene += 1
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ lineOfScene += 1
                                $ Tile.append(displayingScene.theScene[lineOfScene])
                                $ tileset.append(copy.deepcopy(Tile))
                    elif displayingScene.theScene[lineOfScene] == "YAdjust":
                        $ lineOfScene += 1
                        $ gridYAdjust = int(displayingScene.theScene[lineOfScene])

                    elif displayingScene.theScene[lineOfScene] == "PlayerCoord":
                        $ lineOfScene += 1
                        $ startplayerpos[0] = int(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ startplayerpos[1] = int(displayingScene.theScene[lineOfScene])
                        $ playerCoord = startplayerpos
                        $ GridPXpos = GridMovement*playerCoord[0]
                        $ GridPYpos = GridMovement*playerCoord[1]
                        $ GridPXposPrior = GridPXpos
                        $ GridPYposPrior = GridPYpos
                    elif displayingScene.theScene[lineOfScene] == "Sight":
                        $ lineOfScene += 1
                        $ PlayerGridSight = int(displayingScene.theScene[lineOfScene])

                    elif displayingScene.theScene[lineOfScene] == "NPC":
                        $ newNPC = GridNPC()
                        while displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ lineOfScene += 1
                            if displayingScene.theScene[lineOfScene] != "EndLoop":
                                if displayingScene.theScene[lineOfScene] == "Name":
                                    $ lineOfScene += 1
                                    $ newNPC.name = displayingScene.theScene[lineOfScene]
                                elif displayingScene.theScene[lineOfScene] == "Img":
                                    $ lineOfScene += 1
                                    $ newNPC.pic = displayingScene.theScene[lineOfScene]
                                elif displayingScene.theScene[lineOfScene] == "Event":
                                    $ lineOfScene += 1
                                    $ newNPC.NPCevent = [displayingScene.theScene[lineOfScene], displayingScene.theScene[lineOfScene+1], displayingScene.theScene[lineOfScene+2]]
                                    $ lineOfScene += 2
                                elif displayingScene.theScene[lineOfScene] == "TurnEvent":
                                    $ lineOfScene += 1
                                    $ newNPC.NPCMoveEvent = [displayingScene.theScene[lineOfScene], displayingScene.theScene[lineOfScene+1]]
                                    $ lineOfScene += 1
                                elif displayingScene.theScene[lineOfScene] == "Movement":
                                    $ lineOfScene += 1
                                    $ newNPC.Movement = displayingScene.theScene[lineOfScene]
                                    $ lineOfScene += 1
                                    $ newNPC.MovementTarget = displayingScene.theScene[lineOfScene]

                                    if newNPC.Movement == "Whimsical":
                                        $ lineOfScene += 1
                                        $ newNPC.WhimsyRange = int(displayingScene.theScene[lineOfScene])
                                elif displayingScene.theScene[lineOfScene] == "Obstacle":
                                    $ newNPC.Obstacle = 1
                                elif displayingScene.theScene[lineOfScene] == "Wall":
                                    $ newNPC.Wall = "Wall"
                        $ TheGridNPCs.append(copy.deepcopy(newNPC))

                    elif displayingScene.theScene[lineOfScene] == "SpawnNPC":
                        $ lineOfScene += 1
                        $ newNPC = copy.deepcopy(TheGridNPCs[getFromName(displayingScene.theScene[lineOfScene], TheGridNPCs)] )
                        $ lineOfScene += 1
                        $ newNPC.coord[0] = int(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ newNPC.coord[1] = int(displayingScene.theScene[lineOfScene])

                        $ newNPC.GridposX = GridMovement*newNPC.coord[0]
                        $ newNPC.GridposY = GridMovement*newNPC.coord[1]
                        $ newNPC.GridposXPrior = newNPC.GridposX
                        $ newNPC.GridposYPrior = newNPC.GridposY

                        $ ActiveGridNPCs.append(copy.deepcopy(newNPC))


                    elif displayingScene.theScene[lineOfScene] == "Row":
                        $ Row = []
                        while displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ lineOfScene += 1
                            if displayingScene.theScene[lineOfScene] != "EndLoop":
                                $ Row.append(displayingScene.theScene[lineOfScene])
                        $ TheGrid.append(copy.deepcopy(Row))



            call displayTileMap from _call_displayTileMap

            label postGridMap:



####################################################combat specific functions######################################################
        elif displayingScene.theScene[lineOfScene] == "LevelUpMonster":
            $ lineOfScene += 1
            $ goToLevel = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
            if displayingScene.theScene[lineOfScene] == "MatchPlayer":
                $ goToLevel = player.stats.lvl
            elif displayingScene.theScene[lineOfScene] == "GoUpByProgress":
                $ goToLevel += ProgressEvent[DataLocation].eventProgress
            elif displayingScene.theScene[lineOfScene] == "GoUpByProgressFromOtherEvent":
                $ lineOfScene += 1
                $ locOfProg = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                $ goToLevel += ProgressEvent[locOfProg].eventProgress
            else:
                $ goToLevel += int(displayingScene.theScene[lineOfScene])


            if goToLevel > monsterEncounter[CombatFunctionEnemytarget].stats.lvl:
                $ monsterEncounter[CombatFunctionEnemytarget].levelUp(goToLevel)



        elif displayingScene.theScene[lineOfScene] == "EnergyDrain":
            $ lineOfScene += 1
            $ energyLost = int(displayingScene.theScene[lineOfScene])
            $ Drain = energyLost * (1+getVirility(player)*0.01)
            $ Drain *= (renpy.random.randint(75, 125)*0.01)
            $ Drain = math.floor(Drain)
            $ Drain = int(Drain)
            $ player.stats.ep -= Drain
            $ finalDamage = Drain
        elif displayingScene.theScene[lineOfScene] == "SemenHeal":
            $ healText = 0
            $ lineOfScene += 1
            $ recoverAmount = int(displayingScene.theScene[lineOfScene]) * (1+getVirility(player)*0.01)
            $ recoverAmount *= renpy.random.randint(75, 125)*0.01
            $ recoverAmount = math.floor(recoverAmount)
            $ recoverAmount= int(recoverAmount)
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp -= recoverAmount
            $ finalDamage = recoverAmount
        elif displayingScene.theScene[lineOfScene] == "ApplyStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ givingStance = displayingScene.theScene[lineOfScene]

                $ lineOfScene += 1
                python:
                    try:
                        if displayingScene.theScene[lineOfScene] == "SetAttack":
                            lineOfScene += 1
                            lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                        else:
                            lineOfScene -= 1
                    except:
                        lineOfScene -= 1

                $ monsterEncounter[CombatFunctionEnemytarget].giveStance(givingStance, player, lastAttack, holdoverDura=stanceDurabilityHoldOverAttacker)
                $ player.giveStance(givingStance, monsterEncounter[CombatFunctionEnemytarget], lastAttack, holdoverDura=stanceDurabilityHoldOverTarget)

        elif displayingScene.theScene[lineOfScene] == "ApplyStanceToOtherMonster":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ monName = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                $ givingStance = displayingScene.theScene[lineOfScene]

                $ stancePass = 0
                $ found = -1
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        stancePass = 0
                        if C != CombatFunctionEnemytarget:
                            if each.name == monName:
                                for stance in monsterEncounter[C].combatStance:
                                    if stance.Stance == givingStance:
                                        stancePass = 2
                                if stancePass != 2:
                                    stancePass = 1
                                    found = copy.deepcopy(C)
                        C += 1
                if found != -1:
                    $ lineOfScene += 1
                    python:
                        try:
                            if displayingScene.theScene[lineOfScene] == "SetAttack":
                                lineOfScene += 1
                                lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                            else:
                                lineOfScene -= 1
                        except:
                            lineOfScene -= 1

                    $ monsterEncounter[found].giveStance(givingStance, player, lastAttack, holdoverDura=stanceDurabilityHoldOverAttacker)
                    $ player.giveStance(givingStance, monsterEncounter[found], lastAttack, holdoverDura=stanceDurabilityHoldOverTarget)
                    $ CombatFunctionEnemytarget = copy.deepcopy(found)

        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                python:
                    for stance in player.combatStance:
                        if displayingScene.theScene[lineOfScene] == "Penetration":
                            if stance.Stance == "Sex":
                                stancePass = 1
                            elif stance.Stance == "Anal":
                                stancePass = 1
                        if stance.Stance == displayingScene.theScene[lineOfScene]:
                            stancePass = 1
                        if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                            stancePass = 1

                if stancePass == 1:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_31
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStances":
            if len(monsterEncounter) > 0:
                $ stancePass = 0
                $ stanceNeeded = 0
                $ checked = []
                python:
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            stanceNeeded += 1
                            s = 0
                            for stance in player.combatStance:
                                lookthrough = 0
                                for checkee in checked:
                                    if checkee == s:
                                        lookthrough = 1

                                if lookthrough == 0:
                                    if displayingScene.theScene[lineOfScene] == "Penetration":
                                        if stance.Stance == "Sex":
                                            stancePass += 1
                                            checked.append(s)
                                        elif stance.Stance == "Anal":
                                            stancePass += 1
                                            checked.append(s)
                                    if stance.Stance == displayingScene.theScene[lineOfScene]:
                                        stancePass += 1
                                        checked.append(s)
                                    if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                                        stancePass += 1
                                        checked.append(s)
                                s +=1

                if stancePass == stanceNeeded:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_70
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerDoesntHaveStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                python:
                    for stance in player.combatStance:
                        if stance.Stance == displayingScene.theScene[lineOfScene]:
                            stancePass = 1

                if stancePass == 1:
                    $ lineOfScene += 1
                else:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]

                    call sortMenuD from _call_sortMenuD_32
                    return
        elif displayingScene.theScene[lineOfScene] == "IfMonsterHasStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                python:
                    for stance in monsterEncounter[CombatFunctionEnemytarget].combatStance:
                        if stance.Stance == displayingScene.theScene[lineOfScene]:
                            stancePass = 1
                        if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                            stancePass = 1


                if stancePass == 1:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_33
                    return
                else:

                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterDoesntHaveStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                python:
                    for stance in monsterEncounter[CombatFunctionEnemytarget].combatStance:
                        if stance.Stance == displayingScene.theScene[lineOfScene]:
                            stancePass = 1

                if stancePass == 1:
                    $ lineOfScene += 1
                else:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]

                    call sortMenuD from _call_sortMenuD_34
                    return
        elif displayingScene.theScene[lineOfScene] == "IfOtherMonsterHasStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        if C != CombatFunctionEnemytarget:
                            if each.name == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                                found = copy.deepcopy(C)
                        C += 1
                if stancePass == 1:
                    $ lineOfScene += 1
                    $ stancePass = 0
                    python:
                        for stance in monsterEncounter[found].combatStance:
                            if stance.Stance == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                    if stancePass == 1:
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_35
                        return
                    else:
                        $ lineOfScene += 1
                else:
                    $ lineOfScene += 1
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfOtherMonsterDoesntHaveStance":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        if C != CombatFunctionEnemytarget:
                            if each.name == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                                found = copy.deepcopy(C)
                        C += 1
                if stancePass == 1:
                    $ lineOfScene += 1
                    $ stancePass = 0
                    python:
                        for stance in monsterEncounter[found].combatStance:
                            if stance.Stance == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                    if stancePass == 1:
                        $ lineOfScene += 1
                    else:
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_36
                        return
                else:
                    $ lineOfScene += 1
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "EncounterSizeGreaterOrEqualTo":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_37
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "EncounterSizeLessOrEqualTo":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if len(monsterEncounter) <= int(displayingScene.theScene[lineOfScene]):
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_38
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfThisMonsterIsInEncounter":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        if C != CombatFunctionEnemytarget:
                            if each.name == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                                found = copy.deepcopy(C)
                        C += 1
                if stancePass == 1:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    $ CombatFunctionEnemytarget = copy.deepcopy(found)
                    call sortMenuD from _call_sortMenuD_39
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerIsUsingThisSkill":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] == combatChoice.name:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_64
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if player.statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_40
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerStunnedByParalysis":
            $ lineOfScene += 1
            if paralysisStunned == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_62
                return
        elif displayingScene.theScene[lineOfScene] == "IfPlayerLevelGreaterThan":
            $ lineOfScene += 1
            if player.stats.lvl >= int(displayingScene.theScene[lineOfScene]):
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_74
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterLevelGreaterThan":
            $ lineOfScene += 1
            if monsterEncounter[CombatFunctionEnemytarget].stats.lvl >= int(displayingScene.theScene[lineOfScene]):
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_75
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterHasStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                while isStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                    if monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                        while isStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                            $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        call sortMenuD from _call_sortMenuD_41
                        return
                    else:
                        $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffectWithPotencyEqualOrGreater":
            $ lineOfScene += 1
            $ statusEffectChek = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ potencyChek = int(displayingScene.theScene[lineOfScene])

            $ TheCheck = player.statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek)


            if TheCheck == True:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_50
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterHasStatusEffectWithPotencyEqualOrGreater":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ statusEffectChek = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                $ potencyChek = displayingScene.theScene[lineOfScene]

                if monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek) == True:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_51
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfOtherMonsterHasStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        if C != CombatFunctionEnemytarget:
                            if each.name == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                                found = copy.deepcopy(C)
                        C += 1

                if stancePass == 1:
                    $ lineOfScene += 1
                    if monsterEncounter[found].statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_42
                        return
                    else:
                        $ lineOfScene += 1
                else:
                    $ lineOfScene += 1
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfPlayerDoesntHaveStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if player.statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == False:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_43
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterDoesntHaveStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                if monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == False:
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_44
                    return
                else:
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfOtherMonsterDoesntHaveStatusEffect":
            if len(monsterEncounter) > 0:
                $ lineOfScene += 1
                $ stancePass = 0
                $ C = 0
                python:
                    for each in trueMonsterEncounter:
                        if C != CombatFunctionEnemytarget:
                            if each.name == displayingScene.theScene[lineOfScene]:
                                stancePass = 1
                                found = copy.deepcopy(C)
                        C += 1
                if stancePass == 1:
                    $ lineOfScene += 1
                    if monsterEncounter[found].statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                        $ lineOfScene += 1
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_45
                        return
                    else:
                        $ lineOfScene += 1
                else:
                    $ lineOfScene += 1
                    $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "ChangeNextStatCheckDifficulty":
            $ lineOfScene += 1
            $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ResetStatCheckDifficultyModifer":
            $ increaseStatCheck = 0

        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterArousal":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += int(displayingScene.theScene[lineOfScene])
            if monsterEncounter[CombatFunctionEnemytarget].stats.hp <= 0:
                $ monsterEncounter[CombatFunctionEnemytarget].stats.hp = 0
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterEnergy":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.ep += int(displayingScene.theScene[lineOfScene])
            if monsterEncounter[CombatFunctionEnemytarget].stats.ep <= 0:
                $ monsterEncounter[CombatFunctionEnemytarget].stats.ep = 0
            if monsterEncounter[CombatFunctionEnemytarget].stats.ep > monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep:
                $ monsterEncounter[CombatFunctionEnemytarget].stats.ep = monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterLevel":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.lvl += int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterSpirit":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.sp += int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterMaxArousal":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.max_hp += int(displayingScene.theScene[lineOfScene])
            $  monsterEncounter[CombatFunctionEnemytarget].stats.max_true_hp =  monsterEncounter[CombatFunctionEnemytarget].stats.max_hp
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterMaxEnergy":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.max_ep += int(displayingScene.theScene[lineOfScene])
            $  monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep =  monsterEncounter[CombatFunctionEnemytarget].stats.max_ep
            $ monsterEncounter[CombatFunctionEnemytarget].stats.ep += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterMaxSpirit":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.max_sp += int(displayingScene.theScene[lineOfScene])
            $ monsterEncounter[CombatFunctionEnemytarget].stats.sp += int(displayingScene.theScene[lineOfScene])
            $  monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp =  monsterEncounter[CombatFunctionEnemytarget].stats.max_sp
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterPower":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Power += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterWill":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Willpower += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterInt":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Int += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterTech":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Tech += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterAllure":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Allure += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterLuck":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Luck += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterSensitivity":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ monsterEncounter[CombatFunctionEnemytarget].BodySensitivity.changeRes (resTarget, resAmount)
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterStatusEffectResistances":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ monsterEncounter[CombatFunctionEnemytarget].resistancesStatusEffects.changeRes (resTarget, resAmount)
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterFetish":
            $ lineOfScene += 1
            $ resTarget = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ resAmount = int(displayingScene.theScene[lineOfScene])

            $ baseFetish = monsterEncounter[CombatFunctionEnemytarget].getFetish(resTarget)
            $ baseFetish += resAmount

            $ monsterEncounter[CombatFunctionEnemytarget].setFetish(resTarget, baseFetish)
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterErosDrop":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].moneyDropped += int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "RecalculateMonsterErosDrop":
            $ lineOfScene += 1
            $ lvlchek = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Exp = int((lvlchek)^2+(lvlchek*10)+48)
        elif displayingScene.theScene[lineOfScene] == "ChangeMonsterExpDrop":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Exp += int(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "RecalculateMonsterExpDrop":
            $ lineOfScene += 1
            $ lvlchek = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
            $ monsterEncounter[CombatFunctionEnemytarget].stats.Exp = int((0.4*(lvlchek*lvlchek))+(2*lvlchek)+(15*math.sqrt(lvlchek)-8))

        elif displayingScene.theScene[lineOfScene] == "RefreshMonster":
            $ monsterEncounter[CombatFunctionEnemytarget] = monsterEncounter[CombatFunctionEnemytarget].statusEffects.refresh(monsterEncounter[CombatFunctionEnemytarget])
            $ monsterEncounter[CombatFunctionEnemytarget].stats.refresh()

        elif displayingScene.theScene[lineOfScene] == "IfMonsterArousalGreaterThan":
            $ lineOfScene += 1
            if monsterEncounter[CombatFunctionEnemytarget].stats.hp >= int(displayingScene.theScene[lineOfScene]):
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_46
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfMonsterOrgasm":
            $ lineOfScene += 1
            if monsterEncounter[CombatFunctionEnemytarget].stats.hp >= monsterEncounter[CombatFunctionEnemytarget].stats.max_true_hp:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_47
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "IfMonsterEnergyGone":
            $ lineOfScene += 1
            if monsterEncounter[CombatFunctionEnemytarget].stats.ep <= 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_91
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "IfMonsterSpiritGone":
            $ lineOfScene += 1
            if monsterEncounter[CombatFunctionEnemytarget].stats.sp <= 0:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_55
                if len(monsterEncounter) > 0:
                    return
        elif displayingScene.theScene[lineOfScene] == "CallMonsterEncounterOrgasmCheck":
            $ orgasmTarget = monsterEncounter[CombatFunctionEnemytarget]
            $ orgasmCauser = player
            call setDefender(monsterEncounter[CombatFunctionEnemytarget]) from _call_setDefender_2

            call theOrgasmCheck from _call_theOrgasmCheck_1
            call MonsterLossCheck from _call_MonsterLossCheck_2

            if len(monsterEncounter) <= 0:
                jump combatWin
        elif displayingScene.theScene[lineOfScene] == "MonsterOrgasm":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp = 0
            $ spiritLost = SpiritCalulation(monsterEncounter[CombatFunctionEnemytarget], int(displayingScene.theScene[lineOfScene]))
            $ monsterEncounter[CombatFunctionEnemytarget].stats.sp -= spiritLost
            if monsterEncounter[CombatFunctionEnemytarget].stats.sp <= 0:
                $ monsterEncounter[CombatFunctionEnemytarget].stats.sp = 0
            if monsterEncounter[CombatFunctionEnemytarget].stats.sp > monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp:
                $ monsterEncounter[CombatFunctionEnemytarget].stats.sp = monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp
        elif displayingScene.theScene[lineOfScene] == "ApplyStatusEffectToMonster":
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ statusSkill = SkillsDatabase[skillAt]

            if statusSkill.statusEffect != "Damage" and statusSkill.statusEffect != "Defence" and statusSkill.statusEffect != "Power" and statusSkill.statusEffect != "Technique" and statusSkill.statusEffect != "Intelligence" and statusSkill.statusEffect != "Willpower" and statusSkill.statusEffect != "Allure" and statusSkill.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and statusSkill.statusEffect != "Escape" and statusSkill.statusEffect != "Crit":
                $ monsterEncounter[CombatFunctionEnemytarget] = statusAfflict(monsterEncounter[CombatFunctionEnemytarget], statusSkill)
            else:
                $ holder = statusBuff(monsterEncounter[CombatFunctionEnemytarget], monsterEncounter[CombatFunctionEnemytarget], statusSkill, 1)
                $ monsterEncounter[CombatFunctionEnemytarget] = holder[0]
            if statusSkill.statusEffect == "Restrain":
                $ monsterEncounter[CombatFunctionEnemytarget].restraintStruggle = copy.deepcopy(statusSkill.restraintStruggle)
                $ monsterEncounter[CombatFunctionEnemytarget].restraintStruggleCharmed = copy.deepcopy(statusSkill.restraintStruggleCharmed)
                $ monsterEncounter[CombatFunctionEnemytarget].restraintEscaped = copy.deepcopy(statusSkill.restraintEscaped)
                $ monsterEncounter[CombatFunctionEnemytarget].restraintEscapedFail = copy.deepcopy(statusSkill.restraintEscapedFail)
                $ monsterEncounter[CombatFunctionEnemytarget].restrainer = player

        elif displayingScene.theScene[lineOfScene] == "GiveSkillToMonster":
            $ lineOfScene += 1
            $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ monsterEncounter[CombatFunctionEnemytarget].skillList.append(SkillsDatabase[fetchSkill])
        elif displayingScene.theScene[lineOfScene] == "RemoveSkillFromPlayer":
            $ lineOfScene += 1
            $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], player.skillList)
            if fetchSkill != -1:
                $ display = "Forgot how to use " + player.skillList[fetchSkill].name + "!"
                $ del player.skillList[fetchSkill]
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "RemoveSkillFromPlayerQuietly":
            $ lineOfScene += 1
            $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], player.skillList)
            if fetchSkill != -1:
                $ del player.skillList[fetchSkill]

        elif displayingScene.theScene[lineOfScene] == "RemoveSkillFromMonster":
            $ lineOfScene += 1
            $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], monsterEncounter[CombatFunctionEnemytarget].skillList)
            if fetchSkill != -1:
                $ del monsterEncounter[CombatFunctionEnemytarget].skillList[fetchSkill]

        elif displayingScene.theScene[lineOfScene] == "GiveSkillThatWasTemporarilyRemoved":
            $ lineOfScene += 1
            $ check = 1
            python:
                for each in player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 0
            if check == 1:
                python:
                    foundS = 0
                    fetchSkill = 0
                    for each in removedSkill:
                        if each == displayingScene.theScene[lineOfScene] or foundS == 1:
                            foundS = 1
                        else:
                            fetchSkill += 1
                if foundS != 0:
                    $ player.skillList.insert(removedSkillPosition[fetchSkill], SkillsDatabase[getFromName(removedSkill[fetchSkill], SkillsDatabase)])
                    $ del removedSkillPosition[fetchSkill]
                    $ del removedSkill[fetchSkill]
        elif displayingScene.theScene[lineOfScene] == "RemoveSkillFromPlayerTemporarily":
            $ lineOfScene += 1
            $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], player.skillList)
            if fetchSkill != -1:
                $ removedSkillPosition.append(fetchSkill)
                $ removedSkill.append(displayingScene.theScene[lineOfScene])
                $ del player.skillList[fetchSkill]
        elif displayingScene.theScene[lineOfScene] == "IfMonsterHasSkill":
            $ lineOfScene += 1
            $ passSkillCheck = 0
            python:
                for each in  monsterEncounter[CombatFunctionEnemytarget].skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passSkillCheck = 1
            $ lineOfScene += 1
            if passSkillCheck == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_48
                return
        elif displayingScene.theScene[lineOfScene] == "GivePerkToMonster":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].giveOrTakePerk(displayingScene.theScene[lineOfScene], 1)

        elif displayingScene.theScene[lineOfScene] == "RemovePerkFromMonster":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget].giveOrTakePerk(displayingScene.theScene[lineOfScene], -1)

        elif displayingScene.theScene[lineOfScene] == "IfMonsterHasPerk":
            $ lineOfScene += 1
            $ passSkillCheck = 0
            python:
                for each in  monsterEncounter[CombatFunctionEnemytarget].perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        passSkillCheck = 1
            $ lineOfScene += 1
            if passSkillCheck == 1:
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_49
                return
        elif displayingScene.theScene[lineOfScene] == "ClearMonsterSkillList":
            $ monsterEncounter[CombatFunctionEnemytarget].skillList = []
        elif displayingScene.theScene[lineOfScene] == "ClearMonsterPerks":
            $ monsterEncounter[CombatFunctionEnemytarget].perks = []
        elif displayingScene.theScene[lineOfScene] == "AddMonsterToEncounter":
            $ lineOfScene += 1
            $ replacingMonster = 0
            $ insertToLocation = len(monsterEncounter)
            if displayingScene.theScene[lineOfScene] == "ChangeForm":
                $ lineOfScene += 1
                $ replacingMonster = 1
                $ insertToLocation = copy.deepcopy(CombatFunctionEnemytarget)
                $ KeepingHP = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].stats.hp)
                $ KeepingSP = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].stats.sp)
                $ KeepingStatusEffects = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].statusEffects)
                $ KeepingStances = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].combatStance)

                python:
                    del monsterEncounter[CombatFunctionEnemytarget]
                    del trueMonsterEncounter[CombatFunctionEnemytarget]


            $ addMonsterTo(displayingScene.theScene[lineOfScene], monsterEncounter, insertToLocation)
            $ monsterEncounter[insertToLocation] = monsterEncounter[insertToLocation].statusEffects.refresh(monsterEncounter[insertToLocation])
            $ addMonsterTo(displayingScene.theScene[lineOfScene], trueMonsterEncounter,insertToLocation)
            $ trueMonsterEncounter[insertToLocation] = trueMonsterEncounter[insertToLocation].statusEffects.refresh(trueMonsterEncounter[insertToLocation])

            if replacingMonster == 0:
                $ monInititive.append(-999)
                $ monSkillChoice.append( getSkill(" ", SkillsDatabase))

            else:
                $ monsterEncounter[insertToLocation].stats.hp = copy.deepcopy(KeepingHP)
                $ monsterEncounter[insertToLocation].stats.sp = copy.deepcopy(KeepingSP)
                $ monsterEncounter[insertToLocation].statusEffects = copy.deepcopy(KeepingStatusEffects)
                $ monsterEncounter[insertToLocation].combatStance = copy.deepcopy(KeepingStances)

                python:
                    del KeepingHP, KeepingStatusEffects, KeepingStances
                    try:
                        del KeepingStatusEffects
                    except:
                        pass

            $ monsterEncounter[insertToLocation] = initiateImageLayers(monsterEncounter[insertToLocation])
            python:
                for SetData in persistantMonSetData:
                    if SetData.name == monsterEncounter[insertToLocation].IDname:
                        monsterEncounter[insertToLocation].currentSet = getFromName(SetData.startingSet, monsterEncounter[insertToLocation].ImageSets)

                c = 0
                for each in monsterEncounter:
                    monsterEncounter[c].name = copy.deepcopy(trueMonsterEncounter[c].name)



                    c += 1
            $ monsterEncounter = NumberMonsters(monsterEncounter)

            $ m = -1
            $ ar = 0
            while ar < len(monsterEncounter[m].combatDialogue):
                $ specifyStance = 0
                if ar < len(monsterEncounter[m].combatDialogue):
                    if monsterEncounter[m].combatDialogue[ar].lineTrigger == "MonsterArrived":
                        $ CombatFunctionEnemytarget = m
                        $ Speaker = Character(_(monsterEncounter[m].name))
                        $ display = monsterEncounter[m].combatDialogue[ar].theText[renpy.random.randint(-1, len(monsterEncounter[m].combatDialogue[ar].theText)-1)]
                        call read from _call_read_55
                $ ar += 1


        elif displayingScene.theScene[lineOfScene] == "ShuffleMonsterEncounter":
            python:
                c = 0
                for each in monsterEncounter:
                    monsterEncounter[c].name = copy.deepcopy(trueMonsterEncounter[c].name)
                    c += 1
            $ renpy.random.shuffle(monsterEncounter)
            $ trueMonsterEncounter = copy.deepcopy(monsterEncounter)
            $ monsterEncounter = NumberMonsters(monsterEncounter)
        elif displayingScene.theScene[lineOfScene] == "RefocusOnInitialMonster":
            $ CombatFunctionEnemytarget = copy.deepcopy(CombatFunctionEnemyInitial)
        elif displayingScene.theScene[lineOfScene] == "FocusOnMonster":
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) <= len(monsterEncounter):
                $ CombatFunctionEnemytarget = int(displayingScene.theScene[lineOfScene])-1
            else:
                $ CombatFunctionEnemytarget = len(monsterEncounter)-1
        elif displayingScene.theScene[lineOfScene] == "FocusOnRandomMonster":
            if len(monsterEncounter) >= 1:
                $ CombatFunctionEnemytarget = renpy.random.randint(0, len(monsterEncounter)-1)
        elif displayingScene.theScene[lineOfScene] == "FocusedSpeaks":
            if len(monsterEncounter) >= 1:
                #$ Speaker = monsterEncounter[CombatFunctionEnemytarget].name + attackTitle

                $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name) + attackTitle,
                                        what_prefix='"',
                                        what_suffix='"')
                $ lineOfScene += 1
                $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "FocusedSpeaksSkill":
            if len(monsterEncounter) >= 1:
                #$ Speaker = monsterEncounter[CombatFunctionEnemytarget].name + attackTitle

                $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name) + attackTitle )
                $ lineOfScene += 1
                $ readLine = 1
        elif displayingScene.theScene[lineOfScene] == "CallMonsterAttack":
            if len(monsterEncounter) > 0:
                $ specified = 0
                $ lineOfScene += 1
                $ m = CombatFunctionEnemytarget
                python:
                    try:
                        if displayingScene.theScene[lineOfScene] == "SpecificAttack":
                            lineOfScene += 1
                            specified = 1
                            monSkillChoice[CombatFunctionEnemytarget] = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                        else:
                            lineOfScene -= 1
                    except:
                        lineOfScene -= 1

                $ HoldingSceneCA = copy.deepcopy(displayingScene)
                $ HoldingLineCA = copy.deepcopy(lineOfScene+1)
                $ HoldingDataLocCA = copy.deepcopy(DataLocation)

                if(monsterEncounter[CombatFunctionEnemytarget].statusEffects.stunned.duration > 0):
                    $ display = monsterEncounter[CombatFunctionEnemytarget].name + " is stunned and cannot act!"
                    "[display]"
                else:
                    if specified == 0:
                        $ pickNewSkill = 1
                        call enemySkillChoice(mSC=CombatFunctionEnemytarget) from _call_enemySkillChoice_1

                    $ skillcheck = monSkillChoice[CombatFunctionEnemytarget]
                    if player.statusEffects.sleep.potency < 5:
                        $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name + " - " + monSkillChoice[CombatFunctionEnemytarget].name))
                    else:
                        $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name))
                    $ attacker = monsterEncounter[CombatFunctionEnemytarget]
                    $ defender = player
                    $ skillChoice = monSkillChoice[CombatFunctionEnemytarget]
                    call combatActionTurn from _call_combatActionTurn_2
                    #call EnemyTurn from _call_EnemyTurn

                #$ display = ""
                $ LastDisplayOrder = []
                if HoldingSceneCA != Dialogue():
                    $ displayingScene = copy.deepcopy(HoldingSceneCA)
                    $ lineOfScene = copy.deepcopy(HoldingLineCA)
                    $ DataLocation = copy.deepcopy(HoldingDataLocCA)
                $ HoldingSceneCA = Dialogue()
                $ HoldingLineCA = 0
                $ HoldingDataLocCA = 0

                jump resumeSceneAfterCombat


        elif displayingScene.theScene[lineOfScene] == "HitMonsterWith":
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ holder = AttackCalc(player, monsterEncounter[CombatFunctionEnemytarget],  SkillsDatabase[skillAt], 1)
            $ finalDamage = holder[0]
            $ critText = holder[2]
            $ effectiveText = holder[5]
            $ recoil = holder[4]
            $ recoil =  int(math.floor(recoil))
            $ player.stats.hp += recoil
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += holder[0]
        elif displayingScene.theScene[lineOfScene] == "HitPlayerWith":
            $ recoil = 0
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ holder = AttackCalc(monsterEncounter[CombatFunctionEnemytarget], player,  SkillsDatabase[skillAt], 1)
            $ finalDamage = holder[0]
            $ critText = holder[2]
            $ effectiveText = holder[5]
            $ recoil = holder[4]
            $ recoil =  int(math.floor(recoil))
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil
            $ player.stats.hp += holder[0]
        elif displayingScene.theScene[lineOfScene] == "DamagePlayerFromMonster":
            $ recoil = 0
            $ lineOfScene += 1
            $ MonAt = getFromName(displayingScene.theScene[lineOfScene], MonsterDatabase)
            $ holder = MonsterDatabase[MonAt]
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ holder = AttackCalc(holder, player,  SkillsDatabase[skillAt], 1)
            $ finalDamage = holder[0]
            if len(monsterEncounter) >= 1:
                $ critText = holder[2]
                $ effectiveText = holder[5]
                $ recoil = holder[4]
                $ recoil =  int(math.floor(recoil))
                $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil

            $ player.stats.hp += holder[0]
            $ holder = []
        elif displayingScene.theScene[lineOfScene] == "DamageMonsterFromMonster":
            $ recoil = 0
            $ lineOfScene += 1
            $ MonAt = getFromName(displayingScene.theScene[lineOfScene], MonsterDatabase)
            $ holder = MonsterDatabase[MonAt]
            $ lineOfScene += 1
            $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ holder = AttackCalc(holder, monsterEncounter[CombatFunctionEnemytarget],  SkillsDatabase[skillAt], 1)
            $ finalDamage = holder[0]
            if len(monsterEncounter) >= 1:
                $ critText = holder[2]
                $ effectiveText = holder[5]
            #    $ recoil = holder[4]
            #    $ recoil =  int(math.floor(recoil))
                #$ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil
            $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += holder[0]
            $ holder = []
        elif displayingScene.theScene[lineOfScene] == "EndCounterChecks":
            $ canGo = 0

        elif displayingScene.theScene[lineOfScene] == "DenyPlayerOrgasm":
            $ skipPlayerOrgasm = 1
        elif displayingScene.theScene[lineOfScene] == "DenyMonsterOrgasm":
            $ skipMonsterOrgasm = 1
        elif displayingScene.theScene[lineOfScene] == "DenyTargetOrgasm":
            $ skipTargetOrgasm = 1
        elif displayingScene.theScene[lineOfScene] == "DenyAttackerOrgasm":
            $ skipAttackOrgasm = 1

        elif displayingScene.theScene[lineOfScene] == "SkipPlayerAttack":
            $ skipAttack = 1
        elif displayingScene.theScene[lineOfScene] == "SkipMonsterAttack":
            $ monsterEncounter[CombatFunctionEnemytarget].skippingAttack = 1
        elif displayingScene.theScene[lineOfScene] == "ResumeMonsterAttack":
            $ monsterEncounter[CombatFunctionEnemytarget].skippingAttack = 0
        elif displayingScene.theScene[lineOfScene] == "SkipAllMonsterAttacks":
            python:
                for each in monsterEncounter:
                    each.skippingAttack = 1
        elif displayingScene.theScene[lineOfScene] == "ResumeAllMonsterAttacks":
            python:
                for each in monsterEncounter:
                    each.skippingAttack = 0

        elif displayingScene.theScene[lineOfScene] == "PlayerLosesCombat":
            if len(monsterEncounter) >= 1:
                $ theLastAttacker = monsterEncounter[CombatFunctionEnemytarget]
                jump combatLoss
        elif displayingScene.theScene[lineOfScene] == "SetPostName":
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "None":
                $ attackTitle = ""
            else:
                $ attackTitle = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "HideMonsterEncounter":
            if len(monsterEncounter) >= 1:
                python:
                    renpy.hide_screen("ON_EnemyCardScreen", 'master')
                $ hidingCombatEncounter = 1
        elif displayingScene.theScene[lineOfScene] == "ShowMonsterEncounter":
            if len(monsterEncounter) >= 1:
                hide screen ON_CharacterDialogueScreen
                show screen ON_EnemyCardScreen (_layer="master")
                $ SceneCharacters = []
            $ hidingCombatEncounter = 0
        elif displayingScene.theScene[lineOfScene] == "ClearStances":
            $ player.clearStance()
            python:
                for each in monsterEncounter:
                    each.clearStance()
        elif displayingScene.theScene[lineOfScene] == "ClearStanceFromMonsterAndPlayer":
            $ lineOfScene += 1
            $ removeThisStance = ""
            $ stanceDurabilityHoldOverTarget = 0
            $ stanceDurabilityHoldOverAttacker = 0
            if displayingScene.theScene[lineOfScene] == "All":
                python:
                    copyStances = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].combatStance)
                    for each in copyStances:
                        stanceDurabilityHoldOverTarget += player.getStanceDurability(displayingScene.theScene[lineOfScene])
                        player.removeStanceByName(each.Stance)
                        monsterEncounter[CombatFunctionEnemytarget].removeStanceByName(each.Stance)
            else:
                $ stanceDurabilityHoldOverTarget += player.getStanceDurability(displayingScene.theScene[lineOfScene])
                $ player.removeStanceByName(displayingScene.theScene[lineOfScene])
                $ monsterEncounter[CombatFunctionEnemytarget].removeStanceByName(displayingScene.theScene[lineOfScene])



            $ stanceDurabilityHoldOverAttacker += monsterEncounter[CombatFunctionEnemytarget].getStanceDurability(displayingScene.theScene[lineOfScene])


        elif displayingScene.theScene[lineOfScene] == "RemoveStatusEffectFromMonster":
            $ lineOfScene += 1
            $ monsterEncounter[CombatFunctionEnemytarget] = removeThisStatusEffect(displayingScene.theScene[lineOfScene], monsterEncounter[CombatFunctionEnemytarget])

        elif displayingScene.theScene[lineOfScene] == "ClearMonsterEncounter":
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ DefeatedEncounterMonsters = []
            $ player.clearStance()
            $ player.restraintStruggle = [""]
            $ player.restraintStruggleCharmed = [""]
            $ player.restraintEscaped = [""]
            $ player.restraintEscapedFail = [""]
            $ canRun = True

        elif displayingScene.theScene[lineOfScene] == "ClearMonsterEncounterBossFight":
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ DefeatedEncounterMonsters = []
            $ player.clearStance()
            $ player.restraintStruggle = [""]
            $ player.restraintStruggleCharmed = [""]
            $ player.restraintEscaped = [""]
            $ player.restraintEscapedFail = [""]
        elif displayingScene.theScene[lineOfScene] == "ClearFightForVictory":
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ player.clearStance()
            $ player.restraintStruggle = [""]
            $ player.restraintStruggleCharmed = [""]
            $ player.restraintEscaped = [""]
            $ player.restraintEscapedFail = [""]
            $ canRun = True



        elif displayingScene.theScene[lineOfScene] == "EndCombat":
            jump combatWin

        elif displayingScene.theScene[lineOfScene] == "RemoveMonster":
            python:
                if monsterEncounter[CombatFunctionEnemytarget].combatStance[0].Stance != "None":
                    for monStance in monsterEncounter[CombatFunctionEnemytarget].combatStance:
                        player.removeStanceByName(monStance.Stance)

            if monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[0] != "":
                $ restrainholdyLine = copy.deepcopy(lineOfScene)
                $ restrainholdyScene = copy.deepcopy(displayingScene)
                $ restrainholdyData = copy.deepcopy(DataLocation)
                $ display = monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[renpy.random.randint(-1, len(monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss)-1)]
                call read from _call_read_40
                $ lineOfScene = copy.deepcopy(restrainholdyLine)
                $ displayingScene = copy.deepcopy(restrainholdyScene)
                $ DataLocation = copy.deepcopy(restrainholdyData)

            python:
                del monsterEncounter[CombatFunctionEnemytarget]
                del trueMonsterEncounter[CombatFunctionEnemytarget]
                del monInititive[CombatFunctionEnemytarget]
                if len(monSkillChoice) > 0 and len(monSkillChoice) > CombatFunctionEnemytarget:
                    del monSkillChoice[CombatFunctionEnemytarget]




        elif displayingScene.theScene[lineOfScene] == "DefeatMonster":

            if monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[0] != "":
                $ restrainholdyLine = copy.deepcopy(lineOfScene)
                $ restrainholdyScene= copy.deepcopy(displayingScene)
                $ restrainholdyData = copy.deepcopy(DataLocation)

                $ display = monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[renpy.random.randint(-1, len(monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss)-1)]
                call read from _call_read_41

                $ lineOfScene = copy.deepcopy(restrainholdyLine)
                $ displayingScene = copy.deepcopy(restrainholdyScene)
                $ DataLocation = copy.deepcopy(restrainholdyData)

            $ DefeatMonster(CombatFunctionEnemytarget)

            if len(monsterEncounter) <=0:
                call combatWin from _call_combatWin





##########################################Brothel specific jump functions###########################


        elif displayingScene.theScene[lineOfScene] == "GoToRandomBrothelWaiterScene":
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0

            $ LocationCurrentList = []
            python:
                for each in WaiterBrothel:

                    if each.CardType == "WaiterShift" or each.description == "WaiterShift":
                        hasReq = 0
                        hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                        if hasReq >= len(each.requires) + len(each.requiresEvent):
                            LocationCurrentList.append(copy.deepcopy(each))

            $ renpy.random.shuffle(LocationCurrentList)

            $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
            jump sortMenuD
        elif displayingScene.theScene[lineOfScene] == "GoToRandomBrothelBarScene":
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0

            $ LocationCurrentList = []
            python:
                for each in BarBrothel:
                    if each.CardType == "BarShift" or each.description == "BarShift":
                        hasReq = 0
                        hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                        if hasReq >= len(each.requires) + len(each.requiresEvent):
                            LocationCurrentList.append(copy.deepcopy(each))

            $ renpy.random.shuffle(LocationCurrentList)

            $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
            jump sortMenuD

        elif displayingScene.theScene[lineOfScene] == "GoToRandomBrothelHoleScene":
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0

            $ LocationCurrentList = []
            python:
                for each in GloryHoleBrothel:
                    if each.CardType == "GloryHoleShift" or each.description == "GloryHoleShift":
                        hasReq = 0
                        hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                        if hasReq >= len(each.requires) + len(each.requiresEvent):
                            LocationCurrentList.append(copy.deepcopy(each))

            $ renpy.random.shuffle(LocationCurrentList)

            $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
            jump sortMenuD

        elif displayingScene.theScene[lineOfScene] == "GoToRandomBrothelDayScene":
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0

            $ LocationCurrentList = []
            python:
                for each in DayBrothel:
                    if each.CardType == "DayShift" or each.description == "DayShift":
                        hasReq = 0
                        hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                        if hasReq >= len(each.requires) + len(each.requiresEvent):
                            LocationCurrentList.append(copy.deepcopy(each))

            $ renpy.random.shuffle(LocationCurrentList)

            $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
            jump sortMenuD


###########################################Assorted functions####################################################
        elif displayingScene.theScene[lineOfScene] == "StoreCurrentEventSpotSkippingLines":
            $ lineOfScene += 1

            $ StoredScene = copy.deepcopy(displayingScene)
            $ StoredLine = copy.deepcopy(lineOfScene) + int(displayingScene.theScene[lineOfScene])
            $ StoredDataLoc = copy.deepcopy(DataLocation)

        elif displayingScene.theScene[lineOfScene] == "GoBackToStoredEvent":
            $ displayingScene = StoredScene
            $ lineOfScene = StoredLine
            $ DataLocation = StoredDataLoc
            $ StoredScene = ""
            $ StoredLine = ""
            $ StoredDataLoc = ""





        elif displayingScene.theScene[lineOfScene] == "TimeBecomesNight":
            if TimeOfDay == Morning:
                $ TimeOfDay = MorningNight
            elif TimeOfDay == Noon:
                $ TimeOfDay = NoonNight
            elif TimeOfDay == Afternoon:
                $ TimeOfDay = AfternoonNight
            elif TimeOfDay == DuskDay:
                $ TimeOfDay = Dusk
            elif TimeOfDay == EveningDay:
                $ TimeOfDay = Evening
            elif TimeOfDay == MidnightDay:
                $ TimeOfDay = Midnight
            $ bg =  bgToNightDay(bg, ".png", "Night.png")
        elif displayingScene.theScene[lineOfScene] == "TimeBecomesDay":
            if TimeOfDay == MorningNight:
                $ TimeOfDay = Morning
            elif TimeOfDay == NoonNight:
                $ TimeOfDay = Noon
            elif TimeOfDay == AfternoonNight:
                $ TimeOfDay = Afternoon
            elif TimeOfDay == Dusk:
                $ TimeOfDay = DuskDay
            elif TimeOfDay == Evening:
                $ TimeOfDay = EveningDay
            elif TimeOfDay == Midnight:
                $ TimeOfDay = MidnightDay
            $ bg = bgToNightDay(bg, "Night.png", ".png")
        elif displayingScene.theScene[lineOfScene] == "TimeBecomesNormal":
            if TimeOfDay == MorningNight:
                $ TimeOfDay = Morning
                $ bg = bgToNightDay(bg, "Night.png", ".png")
            elif TimeOfDay == NoonNight:
                $ TimeOfDay = Noon
                $ bg = bgToNightDay(bg, "Night.png", ".png")
            elif TimeOfDay == AfternoonNight:
                $ TimeOfDay = Afternoon
                $ bg = bgToNightDay(bg, "Night.png", ".png")

            if TimeOfDay == DuskDay:
                $ TimeOfDay = Dusk
                $ bg =  bgToNightDay(bg, ".png", "Night.png")
            elif TimeOfDay == EveningDay:
                $ TimeOfDay = Evening
                $ bg =  bgToNightDay(bg, ".png", "Night.png")
            elif TimeOfDay == MidnightDay:
                $ TimeOfDay = Midnight
                $ bg =  bgToNightDay(bg, ".png", "Night.png")

        elif displayingScene.theScene[lineOfScene] == "IfTimeIs":
            $ lineOfScene += 1
            $ passCheck = 0

            $ passCheck = IfTime(displayingScene.theScene[lineOfScene])
            if passCheck == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_73
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "PlayerStep":
            call statusStep from _call_statusStep

        elif displayingScene.theScene[lineOfScene] == "SaveNextLine":
            $ savedLine = displayingScene.theScene[lineOfScene+1]
            $ savedLineInMenu = 0
        elif displayingScene.theScene[lineOfScene] == "DisplaySavedLine":
            $ display = savedLine
            call read from _call_read_52
        elif displayingScene.theScene[lineOfScene] == "UseSavedLineInMenu":
            $ savedLineInMenu = 1
        elif displayingScene.theScene[lineOfScene] == "CallLossLevelUp":
            $ NoGameOver = 1
            call lostExpCheck from _call_lostExpCheck
        elif displayingScene.theScene[lineOfScene] == "ChangeBG":
            $ lineOfScene += 1
            $ bg = changeBG(displayingScene.theScene[lineOfScene])

        elif displayingScene.theScene[lineOfScene] == "StoreCurrentBG":
            $ heldBG = copy.deepcopy(bg)
        elif displayingScene.theScene[lineOfScene] == "UseHeldBG":
            $ bg  = changeBG(heldBG)

        elif displayingScene.theScene[lineOfScene] == "StopBGM":
            $ overrideCombatMusic = 0
            stop music fadeout 1.0
            $ musicChanged = [""]
        elif displayingScene.theScene[lineOfScene] == "StopBGMHard":
            $ overrideCombatMusic = 0
            stop music
            $ musicChanged = [""]
        elif displayingScene.theScene[lineOfScene] == "ChangeBGM":
            $ lineOfScene += 1
            $ bgm = displayingScene.theScene[lineOfScene]
            $ BGMlist = []
            $ BGMlist.append(bgm)
            $ renpy.random.shuffle(BGMlist)
            $ overrideCombatMusic = 0
            if renpy.music.get_playing(channel='music') != bgm:
                play music BGMlist fadeout 1.0 fadein 1.0
            $ musicLastPlayed = BGMlist

        elif displayingScene.theScene[lineOfScene] == "StoreCurrentBGM":
            $ storedBGM = copy.deepcopy(BGMlist)

        elif displayingScene.theScene[lineOfScene] == "PlayStoredBGM":
            $ BGMlist = []
            $ bgm = storedBGM[0]
            $ BGMlist = copy.deepcopy(storedBGM)
            $ renpy.random.shuffle(BGMlist)
            if renpy.music.get_playing(channel='music') != bgm:
                play music BGMlist fadeout 1.0 fadein 1.0
            $ musicLastPlayed = BGMlist

        elif displayingScene.theScene[lineOfScene] == "ChangeBGM-OverrideCombatMusic":
            $ lineOfScene += 1
            $ bgm = displayingScene.theScene[lineOfScene]
            $ BGMlist = []
            $ BGMlist.append(bgm)
            $ renpy.random.shuffle(BGMlist)
            if renpy.music.get_playing(channel='music') != bgm:
                play music BGMlist fadeout 1.0 fadein 1.0
            $ musicLastPlayed = BGMlist
            $ overrideCombatMusic = 1

        elif displayingScene.theScene[lineOfScene] == "ChangeBGM-NoFade":
            $ lineOfScene += 1
            $ bgm = displayingScene.theScene[lineOfScene]
            $ BGMlist = []
            $ BGMlist.append(bgm)
            $ renpy.random.shuffle(BGMlist)
            if renpy.music.get_playing(channel='music') != bgm:
                play music BGMlist
            $ musicLastPlayed = BGMlist
        elif displayingScene.theScene[lineOfScene] == "ChangeBGM-List":
            $ BGMlist = []
            $ musicLastPlayed = BGMlist
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                $ lineOfScene += 1

                $ bgm = displayingScene.theScene[lineOfScene]
                $ BGMlist.append(bgm)

            $ renpy.random.shuffle(BGMlist)
            play music BGMlist fadeout 1.0 fadein 1.0
        elif displayingScene.theScene[lineOfScene] == "PlayThisSongAfterCombat":
            $ lineOfScene += 1
            $ SetSongAfterCombat = displayingScene.theScene[lineOfScene]


        elif displayingScene.theScene[lineOfScene] == "PlaySoundEffect":
            $ lineOfScene += 1
            $ sfx = ""
            $ usingBank = 0

            $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
            $ usingBank = sfxHolder[0]
            $ soundList = sfxHolder [1]

            if usingBank == 0:
                $ sfx = copy.deepcopy(displayingScene.theScene[lineOfScene])
            else:
                $ renpy.random.shuffle(soundList)
                $ sfx = soundList[0]
            play sound sfx fadeout 0.25 fadein 0.25
        elif displayingScene.theScene[lineOfScene] == "PlaySoundEffect2":
            $ lineOfScene += 1
            $ sfx = ""
            $ usingBank = 0

            $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
            $ usingBank = sfxHolder[0]
            $ soundList = sfxHolder [1]

            if usingBank == 0:
                $ sfx = copy.deepcopy(displayingScene.theScene[lineOfScene])
            else:
                $ renpy.random.shuffle(soundList)
                $ sfx = soundList[0]
            play soundChannel2 sfx fadeout 0.25 fadein 0.25

        elif displayingScene.theScene[lineOfScene] == "PlaySoundBankOnce":
            $ lineOfScene += 1
            $ trueSoundList = []
            $ usingBank = 0

            $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
            $ usingBank = sfxHolder[0]
            $ soundList = sfxHolder [1]

            if usingBank == 0:
                $ trueSoundList.append(copy.deepcopy(displayingScene.theScene[lineOfScene]))
            else:
                $ renpy.random.shuffle(soundList)
                python:
                    for each in soundList:
                        trueSoundList.append(each)
                        trueSoundList.append("<silence .25>")
            play sound trueSoundList fadeout 0.25 fadein 0.25

        elif displayingScene.theScene[lineOfScene] == "PlayLoopingSoundEffect":
            $ lineOfScene += 1
            $ trueSoundList = []
            $ usingBank = 0

            $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
            $ usingBank = sfxHolder[0]
            $ soundList = sfxHolder [1]

            if usingBank == 0:
                $ trueSoundList.append(copy.deepcopy(displayingScene.theScene[lineOfScene]))
            else:
                $ renpy.random.shuffle(soundList)
                python:
                    for each in soundList:
                        trueSoundList.append(each)
                        trueSoundList.append("<silence .25>")
            play loopingSound trueSoundList fadeout 0.25 fadein 0.25 loop
        elif displayingScene.theScene[lineOfScene] == "StopSoundEffectLoop":
            stop loopingSound fadeout 1.0

        elif displayingScene.theScene[lineOfScene] == "PlayLoopingSoundEffect2":
            $ lineOfScene += 1
            $ trueSoundList = []
            $ usingBank = 0

            $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
            $ usingBank = sfxHolder[0]
            $ soundList = sfxHolder [1]

            if usingBank == 0:
                $ trueSoundList.append(copy.deepcopy(displayingScene.theScene[lineOfScene]))
            else:
                $ renpy.random.shuffle(soundList)
                python:
                    for each in soundList:
                        trueSoundList.append(each)
                        trueSoundList.append("<silence .25>")
            play loopingSound2 trueSoundList fadeout 0.25 fadein 0.25 loop
        elif displayingScene.theScene[lineOfScene] == "StopSoundEffectLoop2":
            stop loopingSound2 fadeout 1.0


        elif displayingScene.theScene[lineOfScene] == "ShowTreasureChest":
            show chest:
                yalign 0
                xalign 0.35
        elif displayingScene.theScene[lineOfScene] == "HideTreasureChest":
            hide chest
        elif displayingScene.theScene[lineOfScene] == "GiveTreasure":
            $ searchHere = 0
            $ numberFound = 0
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "Common":
                $ searchHere = 0
                $ numberFound = renpy.random.randint(1, 3)
            elif displayingScene.theScene[lineOfScene] == "Uncommon":
                $ searchHere = 1
                $ numberFound = renpy.random.randint(1, 2)
            elif displayingScene.theScene[lineOfScene] == "Rare":
                $ searchHere = 2
                $ numberFound = 1
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
            $ player.inventory.earn(erosFound)
            if datahere.Treasure[searchHere][treasureFound] != "":
                $ player.inventory.give(datahere.Treasure[searchHere][treasureFound], numberFound)

        elif displayingScene.theScene[lineOfScene] == "PlayVisualEffect":
            hide displayVFX onlayer visualEffects
            $ lineOfScene += 1
            $ VisualEffect = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ vfx = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "EndVisualEffect":
            $ VisualEffect = ""
            hide displayVFX onlayer visualEffects
        elif displayingScene.theScene[lineOfScene] == "PlayVisualEffect2":
            hide displayVFX2 onlayer visualEffects
            $ lineOfScene += 1
            $ VisualEffect2 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ vfx2 = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "EndVisualEffect2":
            $ VisualEffect2 = ""
            hide displayVFX2 onlayer visualEffects
        elif displayingScene.theScene[lineOfScene] == "PlayVisualEffect3":
            hide displayVFX3 onlayer visualEffects
            $ lineOfScene += 1
            $ VisualEffect3 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ vfx3 = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "EndVisualEffect3":
            $ VisualEffect3 = ""
            hide displayVFX3 onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayImagePulseLoopingList":
            hide ImagePulseLoopingList onlayer visualEffects
            $ currentPulsingImg = 0

            $ lineOfScene += 1
            $ pulsingSpeed = float(displayingScene.theScene[lineOfScene])
            $ pulsingTime = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulseZoom = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulsingOpacity = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingList = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ pulsingList.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            $ pulsingChoice = pulsingList[0]
            if persistent.showVFX == True:
                show ImagePulseLoopingList onlayer visualEffects at truecenter, ImagePulseLoopingList

        elif displayingScene.theScene[lineOfScene] == "EndImagePulseLoopingList":
            hide ImagePulseLoopingList onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayImagePulseLoopingList2":
            hide ImagePulseLoopingList2 onlayer visualEffects
            $ currentPulsingImg2 = 0
            $ lineOfScene += 1
            $ pulsingSpeed2 = float(displayingScene.theScene[lineOfScene])
            $ pulsingTime2 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulseZoom2 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulsingOpacity2 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingList2 = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ pulsingList2.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            $ pulsingChoice2 = pulsingList2[0]
            if persistent.showVFX == True:
                show ImagePulseLoopingList2 onlayer visualEffects at truecenter, ImagePulseLoopingList2

        elif displayingScene.theScene[lineOfScene] == "EndImagePulseLoopingList2":
            hide ImagePulseLoopingList2 onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayImagePulseLoopingRandom":
            hide ImagePulseLoopingListRandom onlayer visualEffects

            $ currentPulsingImg = 0

            $ lineOfScene += 1
            $ pulsingSpeedRand = float(displayingScene.theScene[lineOfScene])
            $ pulsingTimeRand = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulseZoomRand = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pulsingOpacityRand = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingListRand = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ pulsingListRand.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            $ pulsingChoiceRand = pulsingListRand[0]

            if persistent.showVFX == True:
                show ImagePulseLoopingListRandom onlayer visualEffects at truecenter, ImagePulseLoopingListRandom

        elif displayingScene.theScene[lineOfScene] == "EndImagePulseLoopingRandom":
            hide ImagePulseLoopingListRandom onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayHypnoSpiral":
            hide hypnosisSpiral onlayer visualEffects
            hide hypnosisSpiral behind EnemyCard
            hide hypnosisSpiral behind ON_CharacterDialogueScreen
            $ lineOfScene += 1
            $ sprialSpeed = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ spiralOpacity = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ spiralVFX = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ playBehind = int(displayingScene.theScene[lineOfScene])
            if persistent.showVFX == True:
                if playBehind == 0:
                    show hypnosisSpiral onlayer visualEffects at HypnoSpiral
                else:
                    if len(monsterEncounter) >= 1:
                        show hypnosisSpiral behind EnemyCard at HypnoSpiral
                    else:
                        show hypnosisSpiral behind ON_CharacterDialogueScreen at HypnoSpiral

        elif displayingScene.theScene[lineOfScene] == "EndHypnoSpiral":
            hide hypnosisSpiral onlayer visualEffects
            hide hypnosisSpiral behind EnemyCard
            hide hypnosisSpiral behind ON_CharacterDialogueScreen

        elif displayingScene.theScene[lineOfScene] == "PlayPendulum":
            hide pendulum onlayer visualEffects
            $ lineOfScene += 1
            $ pendulumSpeed = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ pendulumSway = float(displayingScene.theScene[lineOfScene])

            $ lineOfScene += 1
            $ pendulumVFX = displayingScene.theScene[lineOfScene]

            show pendulum onlayer visualEffects at PendulumSwing

        elif displayingScene.theScene[lineOfScene] == "EndPendulum":
            hide pendulum onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayKiss":
            if persistent.showVFX == True:
                show kiss onlayer visualEffects at kiss
        elif displayingScene.theScene[lineOfScene] == "PlayKissingBarrage":
            hide kissingBarrage onlayer visualEffects
            hide kissingBarrageFade onlayer visualEffects
            if persistent.showVFX == True:
                show kissingBarrage onlayer visualEffects at kissingBarrage
                show kissingBarrageFade onlayer visualEffects at kissingBarrageFade
        elif displayingScene.theScene[lineOfScene] == "EndKissingBarrage":
            hide kissingBarrage onlayer visualEffects
            hide kissingBarrageFade onlayer visualEffects
        elif displayingScene.theScene[lineOfScene] == "PlayKissingBarrageOnce":
            if persistent.showVFX == True:
                show kissingBarrage onlayer visualEffects at kissingBarrageOnce
                show kissingBarrageFade onlayer visualEffects at kissingBarrageFadeOnce
                $ kissBarOnce = 1


        elif displayingScene.theScene[lineOfScene] == "PlayCustomBarrage":
            hide kissingBarrageCustom onlayer visualEffects
            hide kissingBarrageFadeCustom onlayer visualEffects

            $ barragefadeSkip = 0
            $ lineOfScene += 1
            $ currentBarrageImg = 0
            $ currentBarrageFadeImg = 0
            $ BarrageTime = float(displayingScene.theScene[lineOfScene])
            $ BarrageSpeed = float(displayingScene.theScene[lineOfScene])
            $ BarrageFadeSpeed = float(displayingScene.theScene[lineOfScene])
            $ BarrageFadeTime = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ BarrageOpacity = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ barrageList = []
                $ barrageFadeList = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ barrageList.append(displayingScene.theScene[lineOfScene])
                        $ barrageFadeList.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            $ barrageChoice = barrageList[0]
            $ barrageFadeChoice = barrageFadeList[0]
            if persistent.showVFX == True:
                show kissingBarrageCustom onlayer visualEffects at kissingBarrageCustom
                show kissingBarrageFadeCustom onlayer visualEffects at kissingBarrageFadeCustom
        elif displayingScene.theScene[lineOfScene] == "EndCustomBarrage":
            hide kissingBarrageCustom onlayer visualEffects
            hide kissingBarrageFadeCustom onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayCustomBarrage2":
            hide kissingBarrageCustom2 onlayer visualEffects
            hide kissingBarrageFadeCustom2 onlayer visualEffects

            $ barragefadeSkip = 0
            $ lineOfScene += 1
            $ currentBarrageImg2 = 0
            $ currentBarrageFadeImg2 = 0
            $ BarrageTime2 = float(displayingScene.theScene[lineOfScene])
            $ BarrageSpeed2 = float(displayingScene.theScene[lineOfScene])
            $ BarrageFadeSpeed2 = float(displayingScene.theScene[lineOfScene])
            $ BarrageFadeTime2 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ BarrageOpacity2 = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ barrageList = []
                $ barrageFadeList = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ barrageList2.append(displayingScene.theScene[lineOfScene])
                        $ barrageFadeList2.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

            $ barrageChoice2 = barrageList2[0]
            $ barrageFadeChoice2 = barrageFadeList2[0]
            if persistent.showVFX == True:
                show kissingBarrageCustom2 onlayer visualEffects at kissingBarrageCustom2
                show kissingBarrageFadeCustom2 onlayer visualEffects at kissingBarrageFadeCustom2
        elif displayingScene.theScene[lineOfScene] == "EndCustomBarrage2":
            hide kissingBarrageCustom2 onlayer visualEffects
            hide kissingBarrageFadeCustom2 onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "PlayBlackOut":
            hide dark onlayer visualEffects
            if persistent.showVFX == True:
                show dark onlayer visualEffects at BlackOut
        elif displayingScene.theScene[lineOfScene] == "EndBlackOut":
            hide dark onlayer visualEffects

        elif displayingScene.theScene[lineOfScene] == "EndAllVisualEffects":
            call EndAllEffects from _call_EndAllEffects_5


        elif displayingScene.theScene[lineOfScene] == "PlayMotionEffect":
            #"MotionEffect", "EffectName", "Target", "Speed", "Distance"
            #Effects: Bounce, SwayPump, Vibrate, Ride,
                #screen only effects: ScreenSway, ScreenBounce, SlowScreenBounce, Explosion, LongExplosion, Crash, Quake
            $ MotionEffectLoop = 0
            #$ GlobalMotion = ""
            $ lineOfScene += 1
            $ MotionEffect = displayingScene.theScene[lineOfScene]

            if MotionEffect != "Explosion" and MotionEffect != "LongExplosion" and MotionEffect != "Crash" and MotionEffect != "Quake" and MotionEffect != "SlowScreenBounce" and MotionEffect != "ScreenBounce" and MotionEffect != "ScreenSway":
                $ GlobalMotion = copy.deepcopy(MotionEffect)
                $ MotionEffect = ""

        elif displayingScene.theScene[lineOfScene] == "PlayMotionEffectLoop":
            #$ GlobalMotion = ""
            $ lineOfScene += 1
            $ MotionEffect = displayingScene.theScene[lineOfScene]
            if MotionEffect != "Explosion" and MotionEffect != "LongExplosion" and MotionEffect != "Crash" and MotionEffect != "Quake" and MotionEffect != "SlowScreenBounce" and MotionEffect != "ScreenBounce" and MotionEffect != "ScreenSway":
                $ GlobalMotion = copy.deepcopy(MotionEffect)
                $ MotionEffect = ""
            $ MotionEffectLoop = 1
        elif displayingScene.theScene[lineOfScene] == "EndMotionEffect":
            $ MotionEffect = ""
            $ MotionEffectLoop = 0
            $ GlobalMotion = ""


        elif displayingScene.theScene[lineOfScene] == "PlayMotionEffectCustom":
            #"MotionEffect", "EffectName", "Target", "Speed", "Distance"
            #Effects: Bounce, Sway
                #screen only effects: SlowBounce, Explosion, LongExplosion, Crash, Quake
                #non-screen only effects: Pump, Vibrate, Ride,
            #Targets: Screen, Characters, Character, Bodypart
            $ MotionEffectLoop = 1
            #$ GlobalMotion = ""
            $ lineOfScene += 1
            $ MotionEffect = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ MotionTarget = displayingScene.theScene[lineOfScene]

            if MotionEffect != "":
                $ MotionEffect+= "Custom"
            else:
                $ MotionEffect = "Realign"

            if MotionTarget == "Characters":
                $ GlobalMotion = copy.deepcopy(MotionEffect)
            elif MotionTarget == "Character" or MotionTarget == "Bodypart":
                $ lineOfScene += 1
                python:
                    try:
                        settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                    except:
                        ifIsInScene = 0
                        if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                            searchingCharacters = trueMonsterEncounter
                        else:
                            searchingCharacters = SceneCharacters
                        if len(searchingCharacters) > 0 and hidingCombatEncounter == 0:
                            #during combat layer change
                            if getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)!= -1:
                                ifIsInScene = 1
                                settingCharcter = getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)

                        if ifIsInScene == 0:
                            settingCharcter = CombatFunctionEnemytarget

                    bodypartTarget = ""
                    if MotionTarget == "Bodypart":
                        lineOfScene += 1
                        bodypartTarget = displayingScene.theScene[lineOfScene]

                    for each in searchingCharacters:
                        if searchingCharacters[settingCharcter].name == each.name:
                            for layers in each.ImageSets[each.currentSet].ImageSet:
                                if MotionTarget == "Bodypart":
                                    if bodypartTarget == layers.name:
                                        layers.motion = MotionEffect
                                else:
                                    layers.motion = MotionEffect

            $ lineOfScene += 1
            $ motionSpeed = float(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ motionDistance = float(displayingScene.theScene[lineOfScene])
            $ MotionEffect = ""
        elif displayingScene.theScene[lineOfScene] == "HasErosLessThan":
            $ lineOfScene += 1
            if int(displayingScene.theScene[lineOfScene]) > player.inventory.money:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_15
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "GiveExp":
            $ lineOfScene += 1
            $ player.stats.Exp += int(displayingScene.theScene[lineOfScene])
            if int(displayingScene.theScene[lineOfScene]) > 0:
                $ display = "Gained " + str(displayingScene.theScene[lineOfScene]) + " exp!"
            else:
                $ amountLost = moneyEarned*-1
                $ display = "Lost " + str(displayingScene.theScene[lineOfScene]) + " exp!"
            "[display]"
            $ expGiven = 1
            call refreshLevelVar from _call_refreshLevelVar_2
            call levelUpSpot from _call_levelUpSpot_1
            $ expGiven = 0

        elif displayingScene.theScene[lineOfScene] == "ChangeEros":
            $ lineOfScene += 1

            $ moneyEarned = int(displayingScene.theScene[lineOfScene])
            $ player.inventory.money += moneyEarned

            if int(displayingScene.theScene[lineOfScene]) > 0:
                $ display = "Gained " + str(moneyEarned) + " eros!"
            else:
                $ amountLost = moneyEarned*-1
                $ display = "Lost " + str(amountLost) + " eros!"
            "[display]"
        elif displayingScene.theScene[lineOfScene] == "SetEros":
            $ lineOfScene += 1
            $ player.inventory.money = int(displayingScene.theScene[lineOfScene])

            if player.inventory.money <= 0:
                $ player.inventory.money = 0

        elif displayingScene.theScene[lineOfScene] == "ChangeErosByPercent":
            $ lineOfScene += 1
            $ preChange = copy.deepcopy(player.inventory.money)
            $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.inventory.money
            $ check = math.floor(check)
            $ check = int(check)
            $ player.inventory.money = check

            if player.inventory.money <= 0:
                $ player.inventory.money = 0

            if float(displayingScene.theScene[lineOfScene]) >= 100:
                $ display = "Gained " + str(check - preChange) + " eros!"
            else:
                $ display = "Lost " + str(preChange - check) + " eros!"
            "[display]"
        elif displayingScene.theScene[lineOfScene] == "AllowInventory":
            $ InventoryAvailable = True
        elif displayingScene.theScene[lineOfScene] == "DenyInventory":
            $ InventoryAvailable = False
        elif displayingScene.theScene[lineOfScene] == "GiveItem":
            $ lineOfScene += 1
            $ amount = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1

            if amount > 0:
                $ player.inventory.give(displayingScene.theScene[lineOfScene] , amount)
                $ display = "Acquired " + str(amount) + " " + displayingScene.theScene[lineOfScene] + "!"
                "[display]"
            else:
                $ amount *= -1
                $ It = 0
                while It < amount:
                    $ player.inventory.useItem(displayingScene.theScene[lineOfScene])
                    $ It += 1

                $ display = "Lost " + str(amount) + " " + displayingScene.theScene[lineOfScene] + "!"
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "GiveItemQuietly":
            $ lineOfScene += 1
            $ amount = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1

            if amount > 0:
                $ player.inventory.give(displayingScene.theScene[lineOfScene], amount)
            else:
                $ amount *= -1
                $ It = 0
                while It < amount:
                    $ player.inventory.useItem(displayingScene.theScene[lineOfScene])
                    $ It += 1

        elif displayingScene.theScene[lineOfScene] == "GiveSkill":
            $ lineOfScene += 1
            $ check = 1
            python:
                for each in player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 0
            if check == 1:
                $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
                $ player.learnSkill(SkillsDatabase[fetchSkill])
                $ display = "Learned " + SkillsDatabase[fetchSkill].name + "!"
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "GiveSkillQuietly":
            $ lineOfScene += 1
            $ check = 1
            python:
                for each in player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 0
            if check == 1:
                $ fetchSkill = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
                $ player.learnSkill(SkillsDatabase[fetchSkill])
        elif displayingScene.theScene[lineOfScene] == "GivePerkPoint":
            $ player.perkPoints += 1

        elif displayingScene.theScene[lineOfScene] == "GivePerk":
            $ lineOfScene += 1
            $ check = 1
            python:
                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 0
            if check == 1:
                $ player.giveOrTakePerk(displayingScene.theScene[lineOfScene], 1)
                $ display = "Got the " + displayingScene.theScene[lineOfScene] + " perk!"
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "GivePerkQuietly":
            $ lineOfScene += 1
            $ check = 1
            python:
                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 0
            if check == 1:
                $ player.giveOrTakePerk(displayingScene.theScene[lineOfScene], 1)


        elif displayingScene.theScene[lineOfScene] == "RemovePerk":
            $ lineOfScene += 1
            $ check = 0
            python:
                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 1
            if check == 1:
                $ player.giveOrTakePerk(displayingScene.theScene[lineOfScene], -1)
                $ display = "Lost the " + displayingScene.theScene[lineOfScene] + " perk!"
                "[display]"
        elif displayingScene.theScene[lineOfScene] == "RemovePerkQuietly":
            $ lineOfScene += 1
            $ check = 0
            python:
                for each in player.perks:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        check = 1
            if check == 1:
                $ player.giveOrTakePerk(displayingScene.theScene[lineOfScene], -1)

        elif displayingScene.theScene[lineOfScene] == "ChangePerkDuration":
            $ lineOfScene += 1
            $ perkToChange = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            $ amountToChange = int(displayingScene.theScene[lineOfScene])
            $ displayList = []

            $ holda = changePerkDuration(player, perkToChange, amountToChange)
            $ player = holda[0]
            $ displayList = holda[1]

            $ p = 0
            while p < len(displayList):
                $ display = returnReaderDiction(displayList[p])
                "[display]"
                $ p += 1



        elif displayingScene.theScene[lineOfScene] == "GoToTown":
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ DefeatedEncounterMonsters = []
            $ SceneCharacters = []
            $ displayingScene = Dialogue()
            $ player = player.statusEffects.refresh(player)
            #$ player.stats.refresh()
            $ player.clearStance()
            $ player.restraintStruggle = [""]
            $ player.restraintStruggleCharmed = [""]
            $ player.restraintEscaped = [""]
            $ player.restraintEscapedFail = [""]
            $ explorationDeck = []
            $ deckProgress = 0
            $ InventoryAvailable = True
            $ canRun = True

            jump returnToTown

        elif displayingScene.theScene[lineOfScene] == "BumpToTown":
            jump Town

        elif displayingScene.theScene[lineOfScene] == "GoToChurch":
            $ monsterEncounter = []
            $ trueMonsterEncounter = []
            $ DefeatedEncounterMonsters = []
            $ SceneCharacters = []
            $ displayingScene = Dialogue()
            $ player = player.statusEffects.refresh(player)
            #$ player.stats.refresh()
            $ player.clearStance()
            $ player.restraintStruggle = [""]
            $ player.restraintStruggleCharmed = [""]
            $ player.restraintEscaped = [""]
            $ player.restraintEscapedFail = [""]
            $ explorationDeck = []
            $ deckProgress = 0
            $ InventoryAvailable = True
            $ canRun = True

            jump Church
        elif displayingScene.theScene[lineOfScene] == "GameOver":
            $ LostGameOver = 1
            $ NoGameOver = 0

            jump lostExpCheck
        elif displayingScene.theScene[lineOfScene] == "TrueGameOver":
            $ renpy.full_restart()
        elif displayingScene.theScene[lineOfScene] == "QuestComplete":
            if DialogueIsFrom == "Event":
                $ ProgressEvent[DataLocation].questComplete = 1
        elif displayingScene.theScene[lineOfScene] == "AdventureComplete":
            $ lineOfScene += 1
            $ AdvLocation = getFromName(displayingScene.theScene[lineOfScene], ProgressAdventure)
            $ ProgressAdventure[AdvLocation].questComplete = 1


        elif displayingScene.theScene[lineOfScene] == "SkillShoppingMenu":
            $ ShoppingSkillList = []
            $ showOnSide = 1
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    $ dataTarget = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
                    $ blankItem = SkillsDatabase[dataTarget]
                    $ ShoppingSkillList.append(blankItem)

            $ buying = 1
            $ SkillShopping = 1
            call Shopping from _call_Shopping
            $ purchasing = 0
            $ amountToBuy = 1
            $ tt.value = ""
            $ on_shoppingtooltip = ""
            show screen ON_CharacterDialogueScreen (_layer="master")
            hide screen ON_ShoppingScreen
            $ showOnSide = 0
            $ ShoppingSkillList = []

        elif displayingScene.theScene[lineOfScene] == "ShoppingMenu":
            $ ShoppingItemList = []
            $ showOnSide = 1
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    $dataTarget = getFromName(displayingScene.theScene[lineOfScene], ItemDatabase)
                    $ blankItem = ItemDatabase[dataTarget]
                    $ ShoppingItemList.append(blankItem)

            $ buying = 1
            $ SkillShopping = 0
            call Shopping from _call_Shopping_1
            $ purchasing = 0
            $ amountToBuy = 1
            $ tt.value = ""
            $ on_shoppingtooltip = ""
            show screen ON_CharacterDialogueScreen (_layer="master")
            hide screen ON_ShoppingScreen
            $ showOnSide = 0
            $ ShoppingSkillList = []


        elif displayingScene.theScene[lineOfScene] == "InputProgress":
            $ debt = 0
            call InputProgress from _call_InputProgress
        elif displayingScene.theScene[lineOfScene] == "HasErosLessThanInput":
            if debt > player.inventory.money:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_3
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfInputEquals":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            if int(displayingScene.theScene[lineOfScene]) == debt:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_7
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "IfInputEqualsOrLessThan":
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            if int(displayingScene.theScene[lineOfScene]) >= debt:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_17
                if len(monsterEncounter) > 0:
                    return
            else:
                $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "AddInputToProgress":
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress += int(math.floor(debt))

        elif displayingScene.theScene[lineOfScene] == "RemoveInputFromPlayerEros":
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ player.inventory.money -= int(math.floor(debt))

        elif displayingScene.theScene[lineOfScene] == "RemoveInputFromProgress":
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress -= int(math.floor(debt))

        elif displayingScene.theScene[lineOfScene] == "RemoveProgressFromEros":
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ player.inventory.money -= int(math.floor(ProgressEvent[DataLocation].eventProgress))
        elif displayingScene.theScene[lineOfScene] == "RespecPlayer":
            $ player.respec()
            $ sexResCap = 150
            $ assResCap = 150
            $ nipResCap = 200
            $ chuResCap = 150
            $ seducResCap = 150
            $ magResCap = 150
            $ painResCap = 150
            $ hpFloor = 50
            $ epFloor = 20
            $ spFloor = 1
            $ powFloor = 1
            $ spdFloor = 1
            $ intFloor = 1
            $ allFloor = 1
            $ wilFloor = 1
            $ lukFloor = 1
            $ respeccing = 1
            $ hasResPoints = 1
            hide screen ON_HealthDisplay
            hide screen ON_HealthDisplayBacking

            $ tentativeStats = copy.deepcopy(player)
            call characterCreation from _call_characterCreation_2
            call setStatFloors from _call_setStatFloors_5
            show screen ON_HealthDisplayBacking #(_layer="hplayer")
            show screen ON_HealthDisplay #(_layer="sayScreen")
            $ respeccing = 0
        elif displayingScene.theScene[lineOfScene] == "DonateToGoddess":
            call DonateToGoddess from _call_DonateToGoddess
        elif displayingScene.theScene[lineOfScene] == "SensitivityRestore":
            call RestoreSensitivity from _call_RestoreSensitivity
        elif displayingScene.theScene[lineOfScene] == "PurgeFetishes":
            call PurgeFetishes from _call_PurgeFetishes
        elif displayingScene.theScene[lineOfScene] == "AddTributeToProgress":
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress += int(math.floor(tribute))
            $ tribute = 0
        else:
            $ notFunction = 1

        if notFunction == 1:
            $ Speaker = Character(_(''))
            $ readLine = 1

        python:
            try:
                displayingScene.theScene
            except:
                displayingScene = Dialogue()

        #if onGridMap == 1:
        #    jump displayTileMap

        if lineOfScene < len(displayingScene.theScene):

            if displayingScene.theScene[lineOfScene] == "SwapLineIf":
                $ lineOfScene += 1
                $ checking = displayingScene.theScene[lineOfScene]
                #Virility, Progress, Choice, OtherEventsProgress, OtherEventsChoice
                $ linefound = 0
                if checking == "Stat":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
                            $ lineOfScene += 1

                            if statToCheck >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "Arousal":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.stats.hp >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "MaxArousal":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.stats.max_true_hp >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "Energy":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.stats.ep >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "MaxEnergy":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.stats.max_true_ep >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "Virility":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if getVirility(player) >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "HasFetish":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25 and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "HasFetishLevelEqualOrGreater":
                    $ lineOfScene += 1
                    $ fetchFetish = displayingScene.theScene[lineOfScene]
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop" and linefound == 0:
                            $ fetishLvl = int(displayingScene.theScene[lineOfScene])

                            if player.getFetish(fetchFetish) >= fetishLvl:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "EncounterSize":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop" and linefound == 0:
                            if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1

                elif checking == "Progress":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "Choice":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
                            $ lineOfScene += 1
                            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

                            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                                $ ProgressEvent[DataLocation].choices.append("")

                            if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1] and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "OtherEventsProgress":
                    $ lineOfScene += 1
                    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "OtherEventsChoice":
                    $ lineOfScene += 1
                    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
                            $ lineOfScene += 1
                            $ CheckEvent = getFromName(ProgressEvent[CheckEvent].name, ProgressEvent)

                            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                                $ ProgressEvent[CheckEvent].choices.append("")

                            if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1] and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "IfTimeIs":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if 1 == IfTime(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1


                elif checking == "Eros":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            if player.inventory.money >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1

                elif checking == "Item":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ hasThing = 0
                            python:
                                for item in player.inventory.items:
                                    if item.name == displayingScene.theScene[lineOfScene]:
                                        hasThing = 1

                            if hasThing == 1 and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1
                elif checking == "Perk":
                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ lineOfScene += 1
                        if displayingScene.theScene[lineOfScene] != "EndLoop":
                            $ hasThing = 0
                            python:
                                for each in player.perks:
                                    if each.name == displayingScene.theScene[lineOfScene]:
                                        hasThing = 1

                            if hasThing == 1 and linefound == 0:
                                $ linefound = 1
                                $ lineOfScene += 1
                                $ display = displayingScene.theScene[lineOfScene]
                            else:
                                $ lineOfScene += 1

                            $ hasThing = 0
                elif checking == "Random":
                    $ lineOfScene += 1
                    $ linefound = 1
                    $ randomSelection = []

                    while displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ randomSelection.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1

                    $ renpy.random.shuffle(randomSelection)
                    $ display = randomSelection[0]

                if linefound == 1:
                    $ readLine = 3
                else:
                    $ readLine = 3
                    $ display = displayingScene.theScene[lineOfScene-1]

                if display == "":
                    $ readLine = 0



        if RanAway == "True" and runAndStayInEvent == 0:
            $ RanAway = "False"
            return

        $ player.stats.BarMinMax()

        if callNextJump == 2:
            $ callNextJump = 1
        else:
            $ callNextJump = 0



        python:
            try:
                if lineOfScene < len(displayingScene.theScene) and readLine == 1:
                    readLine = 2
            except:
                readLine = -10

        if readLine == -10:
            return


        if readLine >= 2 and lineOfScene < len(displayingScene.theScene):
            if readLine == 2 :
                $ display = displayingScene.theScene[lineOfScene]

            $ LastSpeaker = Speaker
            $ LastLine = copy.deepcopy(display)
            if displayingScene.theScene[lineOfScene] != "StartCombat" and display != "EndLoop":
                call read from _call_read_11

        $ lineOfScene += 1




    if len(monsterEncounter) > 0:
        return

    if itemEvent == 1:
        return

    if onGridMap == 2:
        return
    if onGridMap == 3 and dontJumpOutOfGridEvents == 0:
        jump postGridEvent

    if HoldingLine != -1 and len(DialogueTypeHolderArray) == 0:
        $ SceneBookMarkRead = 1
        jump displayScene

    if SceneBookMarkRead == 2:
        $ SceneBookMarkRead = 0
        $ DialogueIsFrom = "Event"
        call PostCombatWin from _call_PostCombatWin


    $ displayingScene = Dialogue()


    if len(explorationDeck) >= deckProgress and len(monsterEncounter) == 0  and runAndStayInEvent == 1 and TimeAdvancedCheckArray[-1] == 0:
        $ runAndStayInEvent = 0
        $ DialogueIsFrom = "Event"
        jump PostCombatWin




    return

label sortMenuD:
    #if TimeAdvancedCheck == 1:
        #$ DialogueIsFrom = "NPC"
        #$ isEventNow = 0
    if callNextJump == 1:
        call playSceneJump from _call_playSceneJump
        if len(monsterEncounter) > 0:
            $ lineOfScene += 1
            jump resumeSceneAfterCombat
        return
    $ cmenu_tooltip = ""



    if EventDatabase[EventConsisterTarget].name != EventConsister and EventConsister != "":
        $ DataLocation = getFromName(EventConsister, EventDatabase)

    $ EventConsister = copy.deepcopy(EventDatabase[DataLocation].name)
    $ EventConsisterTarget = copy.deepcopy(DataLocation)



    if callNextJump == 99:
        $ callNextJump = 0
        $ inCalledSceneJump = 1
        $ specifyCurrentChoice = 0
        $ specifyCurrentChoice = getFromNameOfScene(display, EventDatabase[DataLocation].theEvents)

        $ showingDream = []
        $ showingDream.append(copy.deepcopy(EventDatabase[DataLocation]))
        call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_10
        #$ specifyCurrentChoice = 0

        if callLoopTei != []:
            $ del callLoopTei[-1]
            $ lineOfScene += 1
            $ isEventNow = 0
            jump resumeSceneAfterCombat
        else:
            return



    call postSpecialEffectsCall(VisualEffect, 1) from _call_postSpecialEffectsCall
    call postSpecialEffectsCall(VisualEffect2, 2) from _call_postSpecialEffectsCall_1
    call postSpecialEffectsCall(VisualEffect3, 3) from _call_postSpecialEffectsCall_2

    #if DialogueIsFrom == "NPC":
    #    call npcDialogueMenu from _call_npcDialogueMenu
    #elif DialogueIsFrom == "Monster" or DialogueIsFrom == "LossEvent":
    #    call combatDialogueMenu from _call_combatDialogueMenu
    #elif DialogueIsFrom == "Event":
    #    if InIntro == 0:
        #    call eventDialogueMenu from _call_eventDialogueMenu
        #else:
            #call InIntroDialogueMenu from _call_InIntroDialogueMenu

    if DialogueIsFrom == "Monster":
        if VicChosenScene == -5:
            $ currentChoice = getFromNameOfScene(display, theLastAttacker.lossScenes)
            if currentChoice != -1:
                $ displayingScene = theLastAttacker.lossScenes[currentChoice]
            else:
                $ currentChoice = getFromNameOfScene(display, theLastAttacker.victoryScenes)
                $ displayingScene = theLastAttacker.victoryScenes[currentChoice]
            $ actorNames[0] =  theLastAttacker.name
        else:
            $ currentChoice = getFromNameOfScene(display, DefeatedEncounterMonsters[-1].victoryScenes)
            if currentChoice != -1:
                $ displayingScene = DefeatedEncounterMonsters[-1].victoryScenes[currentChoice]
            else:
                $ currentChoice = getFromNameOfScene(display, DefeatedEncounterMonsters[-1].lossScenes)
                $ displayingScene = DefeatedEncounterMonsters[-1].lossScenes[currentChoice]
            $ actorNames[0] =  DefeatedEncounterMonsters[-1].name
    else:
        if isEventNow == 0:
            $ currentChoice = getFromNameOfScene(display, EventDatabase[DataLocation].theEvents)
        else:
            $ isEventNow = 0

        $ displayingScene = EventDatabase[DataLocation].theEvents[currentChoice]

        $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
        $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
        if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
            $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name


    #$ DialogueIsFrom = "Event"
    #$ DialogueIsFrom = "NPC"

    call displayScene from _call_displayScene_1


    if itemEvent == 1:
        return

    if len(TimeAdvancedCheckArray) > 0 and len(monsterEncounter) == 0 and dontJumpOutOfGridEvents == 0:
        if TimeAdvancedCheckArray[-1] == 1:
            jump postTimeAdvancedEvent

    if EnteringLocationCheck == 1 and len(monsterEncounter) == 0 :
        jump postEntryEvent

    if len(monsterEncounter) > 0 or LostGameOver == -1:
        $ LostGameOver = 0
        return

    if TimeAdvancedCheckArray[-1] == 1:
        return



    if InIntro == 1:
        return



    if DialogueIsFrom == "Event":
        jump postAdventureEvent


label TownLocation:
    $ LastLine = ""
    $ index = 0
    $ SceneCharacters = []

    $ timeNotify = 0
    call advanceTime(TimeIncrease=0) from _call_advanceTime_9

    label getNPCPage:
        $ i = index
        $ LocationCurrentList = []

        $ npcCount = 0
        $ displayTown1 = ""
        $ displayTown2 = ""
        $ displayTown3 = ""
        $ displayTown4 = ""
        $ displayTown5 = ""


    python:
        for each in LocationList:
            if each.CardType == currentLocation and each.description != "EnterArea":
                hasReq = 0
                hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                if hasReq >= len(each.requires) + len(each.requiresEvent):
                    LocationCurrentList.append(copy.deepcopy(each))
                    npcCount += 1

        while i < len(LocationCurrentList):
            if i < len(LocationCurrentList):
                display = LocationCurrentList[i].name

                if displayTown1 == "":
                    displayTown1 = LocationCurrentList[i].name
                elif displayTown2 == "":
                    displayTown2  = LocationCurrentList[i].name
                elif displayTown3 == "":
                    displayTown3  = LocationCurrentList[i].name
                elif displayTown4 == "":
                    displayTown4 = LocationCurrentList[i].name
                elif displayTown5 == "":
                    displayTown5 = LocationCurrentList[i].name
                i += 1

    if currentLocation == "Guild":
        $ locationDescrip = "You stand in the small guildhall, and you can see Elena standing attentively behind the front desk.  Multiple stylistic engravings decorate the stone walls, and a few wooden chairs and tables are haphazardly scattered across the floor with most seats left unoccupied. Elly sits alone in the corner reading a book."
    elif currentLocation == "Inn":
        $ locationDescrip = "You stand in the elegantly decorated entryway of the inn. Vivian stands in the center of the room behind a fancy podium, at the perfect height to show off her ample cleavage while still allowing for business transactions to occur on it. Directly behind Vivian are stairs to the bedrooms, and to your right a set of large double doors lead off to the bar and brothel."
    elif currentLocation == "Church":
        $ locationDescrip = "The church is rather spacious for how small it is, with pews lining the sides and a well kept red carpet going down the center aisle leading to a stone statue of the Goddess Venereae. The only person who never seems to leave is the cleric girl, while others drift in and out to offer prayers or give small donations."
    elif currentLocation == "Shopping":
        $ locationDescrip = "You stand in the rustic looking adventuring store in the market district of town. The walls and shelves are lined with all different kinds of gear an adventurer in Lucidia could use, ranging from potions, runes and magical artifacts, to just straight up sex toys."

    if npcCount > 5:
        show screen NPCPageButtons
    else:
        hide screen NPCPageButtons
    window hide
    $ LastLine = locationDescrip
    show screen fakeTextBox

    menu LocationList:
        "[displayTown1]" if displayTown1 != "":
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ npcCount = 0
            $ DataLocation = getFromName(displayTown1, EventDatabase)
            $ EventConsister = ""
            call sortMenuD from _call_sortMenuD_76
        "[displayTown2]" if displayTown2 != "":
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ npcCount = 0
            $ DataLocation = getFromName(displayTown2, EventDatabase)
            $ EventConsister = ""
            call sortMenuD from _call_sortMenuD_77
        "[displayTown3]" if displayTown3 != "":
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ npcCount = 0
            $ DataLocation = getFromName(displayTown3, EventDatabase)
            $ EventConsister = ""
            call sortMenuD from _call_sortMenuD_78
        "[displayTown4]" if displayTown4 != "":
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ npcCount = 0
            $ DataLocation = getFromName(displayTown4, EventDatabase)
            $ EventConsister = ""
            call sortMenuD from _call_sortMenuD_79
        "[displayTown5]" if displayTown5 != "":
            hide screen FetPageButtons
            hide screen fakeTextBox
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ npcCount = 0
            $ DataLocation = getFromName(displayTown5, EventDatabase)
            $ EventConsister = ""
            call sortMenuD from _call_sortMenuD_83
        "Leave.":
            hide screen FetPageButtons
            hide screen fakeTextBox
            jump LeaveBuilding
    jump TownLocation

label nextNPCPage:
    $ index += 5
    if index >  npcCount:
        $ index = 0
    jump getNPCPage

label lastNPCPage:
    $ index -= 5
    if index < 0:
        $ index = 0

        $ index = npcCount/5
        $ index = math.floor(index)
        $ index = index*5
        $ index = math.floor(index)
        #$ b =  fetCount - index
        #$ index = index + b
        $ index = int(index)

    jump getNPCPage


label nextMenuPage:
    $ index += MaxMenuSlots

    if index >=  len(menuArray):
        $ index = 0

    jump recheckMenu

label lastMenuPage:

    $ indent = MaxMenuSlots
    $ index -= indent
    if index < 0:
        $ index = 0

        while index < len(menuArray):
            $ index += indent
        $ index -= indent
    #    $ index = len(menuArray)/indent
        $ index = math.floor(index)
        #$ index = index*indent
        $ index = math.floor(index)
        #$ b =  fetCount - index
        #$ index = index + b
        $ index = int(index)


    jump recheckMenu



label EnterTownLocation:
    $ LastLine = ""

    $ SceneCharacters = []
    $ EnteringLocationCheck = 1
    $ etl = 0

    while etl < len(LocationList):
        $ Speaker = Character(_(''))
        $ hasReq = 0

        if LocationList[etl].CardType == currentLocation and LocationList[etl].description == "EnterArea":
            $ DialogueIsFrom = "NPC"
            $ isEventNow = 1
            $ currentChoice = 0
            $ DataLocation = getFromName(LocationList[etl].name, EventDatabase)
            call sortMenuD from _call_sortMenuD_80
        label postEntryEvent:
            $ etl += 1
    $ Speaker = Character(_(''))
    $ EnteringLocationCheck = 0
    jump TownLocation
