
init python:
    mapInteractable = True # Used to turn the map off when bringing up a choice menu


# World map screen - draws a map with selectable icons for locations. Replaces locationMenu.
screen ON_MapMenu:
    add "map/map.png"

    $ locationsWithoutIcons = []
    $ mapIconIndices = [] # array of tuples - (index, zorder, hasReq)
    default tooltip = "" # display names of locations when icon is hovered

    $ ignorebuttons = 0
    if renpy.variant("touch"):
        $ ignorebuttons = 1
        for i, loc in enumerate(LocationDatabase):
            $ locationsWithoutIcons.append(i)
            $ sortedIndices = sorted(mapIconIndices, key = lambda x: x[1])

    # Determine whether each location has a map icon

    for i, loc in enumerate(LocationDatabase):
        $ hasReq = 0
        $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)

        $ available = hasReq >=  len(loc.requires) + len(loc.requiresEvent)

        if loc.mapIcon == "" or loc.mapIcon == "None":
            if available:
                $ locationsWithoutIcons.append(i)
        else:
            $ mapIconIndices.append((i, loc.mapIconZorder, available))

    # Sort icons by zorder (e.g. draw mountain icon before forest)
    $ sortedIndices = sorted(mapIconIndices, key = lambda x: x[1])
    if ignorebuttons == 0:
        # Draw all icons in order
        for i in sortedIndices:
            $ loc = LocationDatabase[i[0]]
            imagebutton:
                focus_mask True
                xpos int(loc.mapIconXpos)
                ypos int(loc.mapIconYpos)
                idle "map/" + loc.mapIcon + ".png"
                hover "map/" + loc.mapIcon + "_Hover.png"
                insensitive "map/" + loc.mapIcon + ".png"
                hovered [SetScreenVariable("tooltip", loc.exploreTitle)]
                unhovered [SetScreenVariable("tooltip", "")]
                action [SensitiveIf(mapInteractable and i[2]), SetVariable("targetLocation", i[0]), Jump("ON_ChooseAdventure")]

        # Draw the town icon
        imagebutton:
            focus_mask True
            xpos 0
            ypos 0
            idle "map/MGD_Map_Icon_Town.png"
            hover "map/MGD_Map_Icon_Town_Hover.png"
            insensitive "map/MGD_Map_Icon_Town.png"
            hovered [SetScreenVariable("tooltip", "Back to town")]
            unhovered [SetScreenVariable("tooltip", "")]
            action [SensitiveIf(mapInteractable), Jump("Town")]

    # Draw generic cloud cover
    add "map/map_clouds.png"



    # Draw cloud cover for each location with an icon that CAN'T be visited
    for each in reversed(LocationDatabase):
        if each.mapIcon != "" and each.mapIcon != "None":
            $ hasReq = 0
            $ hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

            $ available = hasReq >=  len(each.requires) + len(each.requiresEvent)


            if not available and each.mapClouds != "":
                add "map/" + each.mapClouds:
                    xpos int(each.mapCloudsXpos)
                    ypos int(each.mapCloudsYpos)

    # in front of clouds, draw classic list of any locations that don't have icons
    if mapInteractable:
        $ yal = 0.1
        for i in locationsWithoutIcons:


            $ loc = LocationDatabase[i]

            $ hasReq = 0
            $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)

            $ available = hasReq >=  len(loc.requires) + len(loc.requiresEvent)

            if available:
                fixed:
                    yalign yal
                    xalign 0.5
                    xsize 324
                    ysize 81
                    use ON_TextButton(text=loc.exploreTitle, action=[SetVariable("targetLocation", i), Jump("ON_ChooseAdventure")])
                $ yal += 0.15

        if renpy.variant("touch"):
            fixed:
                yalign yal
                xalign 0.5
                xsize 324
                ysize 81
                use ON_TextButton(text="Return to Town", action=[Jump("Town")])

    # tooltip displays name of hovered location
    text tooltip xalign 0.5 yalign 0.075 size fontsize


# New label so you don't go into the setup screen if you're just going to do an adventure anyway
# when a location is chosen and it has adventures available, bring up a choice menu
# Option to explore (using cards), do any adventures, or return to the map
label ON_ChooseAdventure:

    # reset the hovered var from the setup menu since it might still be set
    $ hoveredCard = None

    # disable the map and show the location's BG
    $ mapInteractable = False
    $ bg = changeBG(LocationDatabase[targetLocation].picture)
    if bg != "":
        show screen DisplayBG (_layer="master")
    window hide dissolve

    python:
        loc = LocationDatabase[targetLocation]

        hasReq = 0
        hasReq = requiresCheck(loc.FullyUnlockedBy, loc.FullyUnlockedByEvent, player, ProgressEvent)

        availableAdventures = GetAdventureNames(loc)

    if hasReq < len(loc.FullyUnlockedBy) + len(loc.FullyUnlockedByEvent):
        # if there are any adventures for this location, give the list, sans "Explore" option
        if len(availableAdventures) > 0:
            python:
                menuItems = []

                for adventureName in availableAdventures:
                    menuItems.append((adventureName, adventureName))

                menuItems.append(("Return", "__Return"))

                selection = renpy.display_menu(menuItems) # equivalent to "menu:" statement

            if selection == "__Return":
                jump Adventure # Back to map
            else:
                hide screen ON_MapMenu
                python:
                    renpy.hide_screen("ON_MapMenu", 'master')
                $ currentCardName = selection # Set adventure name
                jump AdventureEmbark

        else: # not fully unlocked but no adventures to go on?! Just go back to map
            jump Adventure

    else:
        # If there are any adventures to choose, use a choice menu
        if len(availableAdventures) > 0:

            python:
                menuItems = []
                menuItems.append(("Explore the " + loc.name, "__Explore"))

                for adventureName in availableAdventures:
                    menuItems.append((adventureName, adventureName))

                menuItems.append(("Return", "__Return"))

                selection = renpy.display_menu(menuItems) # equivalent to "menu:" statement

            if selection == "__Explore":
                jump AdventureSetUp
            elif selection == "__Return":
                jump Adventure # Back to map
            else:
                hide screen ON_MapMenu
                python:
                    renpy.hide_screen("ON_MapMenu", 'master')
                $ currentCardName = selection # Set adventure name
                jump AdventureEmbark

        # If no adventures to pick from, just go straight to the setup menu
        else:
            jump AdventureSetUp

init python:
    hoveredCard = None

    # get all available adventures for a location
    def GetAdventureNames(loc):
        availableAdventures = []

        for adventureName in loc.Adventures:
            adventureIndex = getFromName(adventureName, AdventureDatabase)

            if adventureIndex >= 0:

                adventure = AdventureDatabase[adventureIndex]
                questProgress = ProgressAdventure[adventureIndex]

                hasReq = 0

                hasReq = requiresCheck(adventure.requires, adventure.requiresEvent, player, ProgressEvent)


                if questProgress.questComplete == 1:
                    hasReq = 0

                if hasReq >= len(adventure.requires) + len(adventure.requiresEvent):
                    availableAdventures.append(adventureName)

        return availableAdventures


screen ON_AdventureSetupMenu:
    add "gui/adventurecards.png" xpos 270 ypos 0

    text LocationDatabase[targetLocation].name xpos 570 ypos 60 size fontsize
    hbox:
        xpos 592
        ypos 112
        text "Pages: "
        text str(len(monsterDeck) +len(eventDeck)) + "  (minimum: " + str(LocationDatabase[targetLocation].MinimumDeckSize) + ")":
            if len(monsterDeck) + len(eventDeck) < LocationDatabase[targetLocation].MinimumDeckSize:
                color "#ff2200"

    fixed:
        xpos 255
        ypos 105
        use ON_TextButtonMid(text="Return", action=[Jump("Adventure")])

    vbox:
        xpos 250 ypos 205
        fixed:
            xsize 300
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 1), SetVariable ("tabToggle", 1), SetVariable("hoveredCard", None)]
            text "Monsters:" xpos 15 yalign 0.05
            text "Pages: " + str(len(monsterDeck)) + "/" + str(LocationDatabase[targetLocation].MaximumMonsterDeck) xpos 20 yalign 0.95 size 20
        fixed:
            xsize 250
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 2), SetVariable ("tabToggle", 2), SetVariable("hoveredCard", None)]
            text "Events:" xpos 15 yalign 0.05
            text "Pages: " + str(len(eventDeck)) + "/" + str(LocationDatabase[targetLocation].MaximumEventDeck) xpos 20 yalign 0.95 size 20
        fixed:
            xsize 250
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 3), SetVariable ("tabToggle", 3), SetVariable("hoveredCard", None)]
            text "Quest:" xpos 15 yalign 0.05
            if QuestSlot.name == "":
                $ display = "None selected!"
            else:
                $ display = QuestSlot.name
            text display xpos 30 yalign 0.90 size 20

    fixed:
        xpos 255
        ypos 442
        use ON_TextButtonMid(text="Randomize", action=[Jump("RandomizeAdventure")])

    fixed:
        xpos 255
        ypos 550
        use ON_TextButtonMid(text="Embark!", action=[SensitiveIf(len(monsterDeck) + len(eventDeck) >= LocationDatabase[targetLocation].MinimumDeckSize), Jump("shuffleExploration")])



    $ cardSel = []
    if (tabToggle == 1):
        $ cardSel = LocationDatabase[targetLocation].Monsters
        $ currentDeck = monsterDeck
    elif tabToggle == 2:
        $ cardSel = LocationDatabase[targetLocation].Events
        $ currentDeck = eventDeck
    elif tabToggle == 3:
        $ cardSel = LocationDatabase[targetLocation].Quests
        $ currentDeck = eventDeck

    fixed:
        xpos 562
        ypos 232
        xsize 510
        ysize 622

        use ON_Scrollbox(""):
            for each in cardSel:

                if (tabToggle == 1):
                    $ getCurrentCard = getFromName(each, MonsterDatabase)
                    $ currentCard = MonsterDatabase[getCurrentCard]
                    $ currentMax = 99
                elif tabToggle == 2:
                    $ getCurrentCard = getFromName(each, EventDatabase)
                    $ currentCard = EventDatabase[getCurrentCard]
                    $ getCurrentProgCard = getFromName(each, ProgressEvent)
                    $ currentProg = ProgressEvent[getCurrentProgCard]
                    $ currentMax = 99
                elif tabToggle == 3:
                    $ getCurrentCard = getFromName(each, EventDatabase)
                    $ currentCard = EventDatabase[getCurrentCard]
                    $ getCurrentProgCard = getFromName(each, ProgressEvent)
                    $ currentProg = ProgressEvent[getCurrentProgCard]

                $ hasReq = 0

                $ hasReq = requiresCheck(currentCard.requires, currentCard.requiresEvent, player, ProgressEvent)


                if tabToggle == 2 or tabToggle == 3:
                    if currentProg.questComplete == 1:
                        $ hasReq = 0

                $ numberInDeck = 0
                for cycle in currentDeck:
                    if (tabToggle == 1):
                        if cycle.IDname == currentCard.IDname:
                            $ numberInDeck += 1
                    else:
                        if cycle.name == currentCard.name:
                            $ numberInDeck += 1

                if hasReq >= len(currentCard.requires) + len(currentCard.requiresEvent):
                    hbox:
                        fixed:
                            xsize 120
                            ysize 60

                            imagebutton:
                                idle "gui/ListEntryBack.png"
                                hover "gui/ListEntryBack.png"
                                yalign 0.5
                                action SetVariable("hoveredCard", currentCard)
                                hovered SetVariable("hoveredCard", currentCard)

                            if tabToggle == 3:
                                if QuestSlot.name == currentCard.name:
                                    imagebutton:
                                        idle "gui/circlebuttonsmallchecked.png"
                                        hover "gui/circlebuttonsmallchecked_hover.png"
                                        xalign 0.5
                                        yalign 0.5
                                        action SetVariable("currentCardName", currentCard.name), Jump("RemoveFromDeck")
                                else:
                                    imagebutton:
                                        idle "gui/circlebuttonsmall.png"
                                        hover "gui/circlebuttonsmall_hover.png"
                                        xalign 0.5
                                        yalign 0.5
                                        action SetVariable("currentCardName", currentCard.name), Jump("AddToDeck")

                            else:
                                if tabToggle != 1:
                                    imagebutton:
                                        idle "gui/Button_dec_idle.png"
                                        hover "gui/Button_dec_hover.png"
                                        xalign 0.0
                                        yalign 0.5
                                        action [SensitiveIf(numberInDeck > 0), SetVariable("currentCardName", currentCard.name), Jump ("RemoveFromDeck")]
                                else:
                                    imagebutton:
                                        idle "gui/Button_dec_idle.png"
                                        hover "gui/Button_dec_hover.png"
                                        xalign 0.0
                                        yalign 0.5
                                        action [SensitiveIf(numberInDeck > 0), SetVariable("currentCardName", currentCard.IDname), Jump ("RemoveFromDeck")]

                                if tabToggle == 1:
                                    $ numText = str(numberInDeck)
                                else:
                                    $ numText = str(numberInDeck) + "/" + "99"

                                fixed:
                                    xalign 0.5
                                    yalign 0.5
                                    #add "gui/circlebuttonlarge.png"
                                    text numText xalign 0.5 yalign 0.5

                                $ addible = False
                                if currentMax > len(currentDeck):
                                    if tabToggle == 2:
                                        if numberInDeck < 99:
                                            $ addible = True
                                    else:
                                        $ addible = True

                                if tabToggle != 1:
                                    imagebutton:
                                        idle "gui/Button_inc_idle.png"
                                        hover "gui/Button_inc_hover.png"
                                        xalign 1.0
                                        yalign 0.5
                                        action [SensitiveIf(addible), SetVariable("currentCardName", currentCard.name), Jump ("AddToDeck")]
                                else:
                                    imagebutton:
                                        idle "gui/Button_inc_idle.png"
                                        hover "gui/Button_inc_hover.png"
                                        xalign 1.0
                                        yalign 0.5
                                        action [SensitiveIf(addible), SetVariable("currentCardName", currentCard.IDname), Jump ("AddToDeck")]

                        if tabToggle == 3:
                            text currentCard.name xpos -10 yalign 0.5 size 26
                        else:
                            text currentCard.name xpos 13 yalign 0.5 size 26

    if hoveredCard is not None:
        fixed:
            xpos 1090
            ypos 232
            xsize 510
            ysize 622

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
