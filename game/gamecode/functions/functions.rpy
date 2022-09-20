label Functions:
    python:
        def play_sfx(soundEffect): #WAS FOR EXPERIMENTAL FEATURE IGNORE THIS
            psfx = ""
            usingBank = 0
            if soundEffect == "QuickKiss":
                soundList = copy.deepcopy(kissQuickSoundBank)
                usingBank = 1
            elif soundEffect == "LongKiss":
                soundList = copy.deepcopy(kissLongSoundBank)
                usingBank = 1
            elif soundEffect == "MakeOut":
                soundList = copy.deepcopy(kissMakeOutSoundBank)
                usingBank = 1
            if usingBank == 0:
                psfx = copy.deepcopy(displayingScene.theScene[lineOfScene])
            else:
                renpy.random.shuffle(soundList)
                psfx = soundList[0]
            renpy.play(psfx, channel="sound")
        def play_effect(trans, st, at): #WAS FOR EXPERIMENTAL FEATURE IGNORE THIS
            renpy.play("sfx/Erotic/KissQuick/kiss1.wav", channel="sound")
        #the above is here just in case I wanna look at it again for reference or whatever.

        ###This is used to check requires items and event progress for unlocking items, events, and locations.

        def weightedChoice(choices):
            totalweight = 0.0
            for choice, weight in choices:
                totalweight += weight
            randval = renpy.random.random() * totalweight
            for choice, weight in choices:
                if randval <= weight:
                    return choice
                else:
                    randval -= weight
            return

        def changeBG(bg):
            bg = checkBGTime(bg)
            return bg

        def checkBGTime(bg):
            global TimeOfDay, Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight
            if TimeOfDay == Dusk or TimeOfDay == Evening or TimeOfDay == Midnight or TimeOfDay == MorningNight or TimeOfDay == NoonNight or TimeOfDay == AfternoonNight:
                bg =  bgToNightDay(bg, ".png", "Night.png")
            return bg

        def perkDurationDisplay(description, duration, timeType):

            perkStatusDescrip = description

            parsed = description.partition("|perkDuration|")
            if parsed[1] == "|perkDuration|":
                timeDura = ""
                if timeType == "TurnDuration":
                    timeDura = "Lasts " + str(duration) + " more turns."
                elif timeType == "TimeDuration":
                    if duration > 6:
                        timeDura = "Lasts " + str(duration/6) + " more days."
                    else:
                        timeDura = "Lasts " + str(duration) + " more time increments."
                perkStatusDescrip = parsed[0] + timeDura + parsed[2]


            return perkStatusDescrip

        def changePerkDuration(character, perkToChange, amount):
            global timeNotify
            perkFound = 0
            displayList = []
            for perk in character.perks:
                p = 0
                if perk.name == perkToChange and perkFound == 0:
                    perkFound = 1

                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "TimeDuration" or perk.PerkType[p] == "TurnDuration":
                            perk.duration += amount

                            if perk.duration <= 0 and timeNotify == 0:
                                character.giveOrTakePerk(perk.name, -1)
                        if perk.PerkType[p] == "EndMessage" and perk.duration == 0 and timeNotify == 0:
                            displayList.append(perk.EffectPower[p])
                        p += 1


            return [character, displayList]

        def bgToNightDay(bg, parse, addIn):
            parsed = bg.partition(parse)
            bgCheck = parsed[0] + addIn
            if renpy.loadable(bgCheck):
                bg = copy.deepcopy(bgCheck)
            return bg


        def IfTime(LookingForTime):
            global TimeOfDay, Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight
            passCheck = 0
            if LookingForTime == "Day":
                if (TimeOfDay == Morning or TimeOfDay == Noon or TimeOfDay == Afternoon or TimeOfDay == DuskDay or TimeOfDay == EveningDay or TimeOfDay == MidnightDay):
                    passCheck = 1
            elif LookingForTime == "Night":
                if (TimeOfDay == Dusk or TimeOfDay == Evening or TimeOfDay == Midnight or TimeOfDay == MorningNight or TimeOfDay == NoonNight or TimeOfDay == AfternoonNight):
                    passCheck = 1
            elif LookingForTime == "DayFaked":
                if (TimeOfDay == DuskDay or TimeOfDay == EveningDay or TimeOfDay == MidnightDay):
                    passCheck = 1
            elif LookingForTime == "NightFaked":
                if (TimeOfDay == MorningNight or TimeOfDay == NoonNight or TimeOfDay == AfternoonNight):
                    passCheck = 1
            elif LookingForTime == "NightTrue":
                if (TimeOfDay == Dusk or TimeOfDay == Evening or TimeOfDay == Midnight):
                    passCheck = 1
            elif LookingForTime == "DayTrue":
                if (TimeOfDay == Morning or TimeOfDay == Noon or TimeOfDay == Afternoon):
                    passCheck = 1
            elif LookingForTime == "Morning":
                if (TimeOfDay == Morning or TimeOfDay == MorningNight):
                    passCheck = 1
            elif LookingForTime == "Noon":
                if (TimeOfDay == Noon or TimeOfDay == NoonNight):
                    passCheck = 1
            elif LookingForTime == "Afternoon":
                if (TimeOfDay == Afternoon or TimeOfDay == AfternoonNight):
                    passCheck = 1
            elif LookingForTime == "Dusk":
                if (TimeOfDay == Dusk):
                    passCheck = 1
            elif LookingForTime == "Evening":
                if  (TimeOfDay == Evening):
                    passCheck = 1
            elif LookingForTime == "Midnight":
                if (TimeOfDay == Midnight):
                    passCheck = 1
            return passCheck



        def requiresCheck(requiresItem, requiresEvent, player, EventDatabase):
            hasReq = 0
            for required in requiresItem:
                if required == "" or required == "None":
                    hasReq += 1
                else:
                    for keyItem in player.inventory.items:
                        if keyItem.name == required:
                            hasReq += 1

            for required in requiresEvent:

                if required.NameOfEvent == "":
                    hasReq += 1
                else:
                    passChecks = 1
                    if required.Progress > EventDatabase[getFromName(required.NameOfEvent, EventDatabase)].eventProgress:
                        passChecks = 0

                    if passChecks != 0 and required.ChoiceNumber != -1:
                        while required.ChoiceNumber-1 >= len(EventDatabase[getFromName(required.NameOfEvent, EventDatabase)].choices):
                            EventDatabase[getFromName(required.NameOfEvent, EventDatabase)].choices.append("")

                        if required.Choice != EventDatabase[getFromName(required.NameOfEvent, EventDatabase)].choices[required.ChoiceNumber-1]:
                            passChecks = 0
                    if passChecks == 1:
                        hasReq += 1
            return hasReq

        def getFromName(theName, searchThis):
            i = 0
            for x in searchThis:
                try:
                    searchThis[i].IDname
                except:
                    if searchThis[i].name == theName:
                        return i
                else:
                    if searchThis[i].IDname == theName:
                        return i
                i += 1
            return -1

        def getFromNameOfScene(theNameOfScene, searchThis):
            i = 0
            for x in searchThis:
                if searchThis[i].NameOfScene == theNameOfScene:
                    return i
                i += 1
            return -1

        def getDialogueTriggerName(theName, searchThis):
            i = 0
            for x in searchThis:
                if searchThis[i].lineTrigger == theName:
                    return i
                i += 1
            return -1
