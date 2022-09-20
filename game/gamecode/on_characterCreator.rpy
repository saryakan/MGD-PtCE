# Crop transforms for the perk menu
transform pmenu_crop(start, height, xpos, ypos):
    crop (0, start, 519, height)
    xanchor 0.0
    yanchor 0.0
    xpos xpos-259
    ypos ypos-259+start

transform pmenu_crop2(start, height, ypos):
    crop (0, start, 900, height)
    xanchor 0.0
    yanchor 0.0
    ypos ypos+start

# Function for getting xpos on a circle based on the ypos and radius
# used for positioning all the options
init python:
    import math

    def on_getXPosOnCircle(radius, ypos):
        if ypos >= radius or ypos <= -radius:
            return 0
        else:
            return int(math.sqrt(radius*radius - ypos*ypos))
    sens_arr = []

    vp_position = 0

    changingStat = 0
    statCost = 0
    theStatFloor = 0
    theStatCap = 0
    perkText = ""
    typeText = ""
    ChangeThisStat = 0

    hardHp = 100
    hardEp = 30
    hardSp = 1
    hardCoreStat = 1
    easyHp = 170
    easyEp = 70
    easySp = 3
    easyCoreStat = 10
    normalHp = 85
    normalEp = 35
    normalSp = 3
    normalCoreStat = 5

    header_color = "#fff"
    entry_color = "#fff"


    def on_getPerkEntries():
        perkEntries = []

        for perk in PerkDatabaseLVLDisplay:
            # If it's buyable and we don't already have it, display it
            if perk.PlayerCanPurchase == "Yes":
                HasPerk = False
                for existingPerk in tentativeStats.perks:
                    if existingPerk.name == perk.name:
                        HasPerk = True
                filterOut = False

                if PerkFilter != perk.StatReq[0] and PerkFilter != "None":
                    filterOut = True

                if HasPerk == False and filterOut == False:
                    # Check for requirements
                    Usable = True

                    if player.stats.lvl < perk.LevelReq:
                        Usable = False


                    hasPerkReq = 0
                    if perk.PerkReq[0] != "":
                        for each in player.perks:
                            for perkNeed in perk.PerkReq:
                                if each.name == perkNeed:
                                    hasPerkReq += 1
                    else:
                        hasPerkReq += 1

                    if hasPerkReq != len(perk.PerkReq):
                        Usable = False


                    hasStatReq = 0
                    if perk.StatReq[0] != "":
                        p = 0
                        for perkNeed in perk.StatReq:
                            TemporaryStatCheck = player.getStatBonusReduction(perk.StatReq[p])
                            if player.stats.getStat(perk.StatReq[p])-TemporaryStatCheck >= perk.StatReqAmount[p]:
                                hasStatReq += 1
                    else:
                        hasStatReq += 1

                    if hasStatReq != len(perk.StatReq):
                        Usable = False


                    # Build tooltip
                    tooltip = perk.description

                    if perk.PerkReq[0] != "":
                        tooltip += "\nRequires the following perks: "
                        loopCount = 1
                        for perkNeed in perk.PerkReq:
                            if loopCount == len(perk.PerkReq):
                                if loopCount >= 2:
                                    tooltip += " and "

                            tooltip += perkNeed

                            if loopCount == len(perk.PerkReq):
                                tooltip += "."
                            else:
                                tooltip += ","

                            loopCount += 1

                    if perk.StatReqAmount[0] > 0:
                        hasStatReq = 0
                        for perkNeed in perk.StatReq:
                            pstat = player.stats.getStat(perkNeed)
                            tooltip += "\nYou need " + str(perk.StatReqAmount[p]) + " " + perk.StatReq[p] + " to learn this perk."
                            hasStatReq += 1

                    if perk.LevelReq > 1:
                        tooltip += "\nRequires level to learn this perk: " + str(perk.LevelReq) + "."

                    perkEntries.append((perk, Usable, tooltip))

        return perkEntries
        #return sorted(perkEntries, key = lambda x: x[0].name)



# Character creator - completely redone!
# Still not totally sure it isn't crap
# Design is based around three circles - stats, sensitivity, and fetishes/perks
screen ON_CreatorDisplay():
    # Keep it on top of stuff but behind the Say screen
    zorder 150

    # Is this a valid character on the creation screen?
    python:
        done = False
        if (player.SensitivityPoints >= 0):
            if (player.statPoints >= 0 ):
                if (tentativeStats.fetishTotal() > 0):
                    done = True

    # Backdrop for center (behind everything)
    add "gui/levelmenu_center.png" xpos 0 ypos 0

    # Sensitivity screen to the left
    if creating == 1 or hasResPoints == 1:
        add "gui/levelmenu_left.png" xpos 0 ypos 0

        # Display text in red if less than 0
        # Doesn't really apply as of 13 but wotthehell
        frame:
            xcenter 381
            ycenter 240
            xpadding theXpadding
            ypadding theYpadding
            text "Sensitivity Points: [tentativeStats.SensitivityPoints]" xalign 0.5 yalign 0.5 color header_color size fontsize

        # All this shit is in a bigass list of tuples so it's easily extended
        # Also because I fucking love lists of tuples
        # (DisplayName, label for increase, label for decrease, number to display, tooltip)
        python:
            global sens_arr
            sens_arr = [
                ["Cock:", "SenChange", 5, -5, 2, "[tentativeStats.BodySensitivity.Sex]%", "How sensitive is your penis? Costs 2 points to change!", "SexSensitivity", tentativeStats.BodySensitivity.Sex, sexResFloor, sexResCap, "Sex"],
                ["Ass:", "SenChange", 10, -10, 1, "[tentativeStats.BodySensitivity.Ass]%", "I'm sure no monsters will actually go for your ass... R-Right?", "AssSensitivity", tentativeStats.BodySensitivity.Ass, assResFloor, assResCap, "Ass"],
                ["Nipples:", "SenChange", 25, -25, 1, "[tentativeStats.BodySensitivity.Breasts]%", "Your chest sensitivity!", "BreastsSensitivity", tentativeStats.BodySensitivity.Breasts, nipResFloor, nipResCap, "Breasts"],
                ["Mouth:", "SenChange", 10, -10, 1, "[tentativeStats.BodySensitivity.Mouth]%", "Are romantic kisses your weakness?", "MouthSensitivity", tentativeStats.BodySensitivity.Mouth, chuResFloor, chuResCap, "Mouth"],
                ["Seduction:", "SenChange", 10, -10, 1, "[tentativeStats.BodySensitivity.Seduction]%", "Try not to stare too much at erotic displays, or listen to honeyed words, okay?", "SeductionSensitivity", tentativeStats.BodySensitivity.Seduction, seducResFloor, seducResCap, "Seduction"],
                ["Magic:", "SenChange", 10, -10, 1, "[tentativeStats.BodySensitivity.Magic]%", "Your body's innate ability to resist magical attacks!", "MagicSensitivity", tentativeStats.BodySensitivity.Magic, magResFloor, magResCap, "Magic"],
                ["Pain:", "SenChange", 10, -10, 1, "[tentativeStats.BodySensitivity.Pain]%", "Do you like getting punished?", "PainSensitivity", tentativeStats.BodySensitivity.Pain, painResFloor, painResCap, "Pain"]]

            # define the menu location
            xcenter = 381
            ycenter = 475
            radius = 259
            yoffset = -140

        # Loop through each setting, positioning the display/controls on the menu
        $ i = 0
        for s in sens_arr:
            $ x = xcenter + on_getXPosOnCircle(radius, yoffset)
            $ y = ycenter + yoffset

            add "gui/circlebuttonlong.png" xcenter x ycenter y
            if renpy.variant("touch"):
                $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
                $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
                $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
                $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"
                $ xScreenPos = 90
            else:
                $ buttonIdleImgDown = "gui/Button_dec_idle.png"
                $ buttonHoverImgDown = "gui/Button_dec_hover.png"
                $ buttonIdleImgUp = "gui/Button_inc_idle.png"
                $ buttonHoverImgUp = "gui/Button_inc_hover.png"
                $ xScreenPos = 75
            imagebutton:
                idle buttonIdleImgDown
                hover buttonHoverImgDown
                xcenter x-xScreenPos
                ycenter y
                action SetVariable("changingStat", s[3]), SetVariable("statCost", s[4]), SetVariable("perkText", s[7]),  SetVariable("theStatFloor", s[9]), SetVariable("theStatCap", s[10]), SetVariable("typeText", s[11]),   SetVariable("ChangeThisStat", i), Jump(s[1])
                hovered tt.Action(s[6])
                unhovered tt.Action("")

            imagebutton:
                idle buttonIdleImgUp
                hover buttonHoverImgUp
                xcenter x+xScreenPos
                ycenter y
                action SetVariable("changingStat", s[2]), SetVariable("statCost", s[4]), SetVariable("perkText", s[7]),  SetVariable("theStatFloor", s[9]), SetVariable("theStatCap", s[10]), SetVariable("typeText", s[11]), SetVariable("ChangeThisStat", i), Jump(s[1])
                hovered tt.Action(s[6])
                unhovered tt.Action("")

            $ i += 1
            text s[5] xcenter x ycenter y
            if renpy.variant("touch"):
                text s[0] xpos x-120 xalign 1.0 ycenter y color entry_color
            else:
                text s[0] xpos x-105 xalign 1.0 ycenter y color entry_color

            $ yoffset += 61



    # define the menu location
    python:
        xcenter = 1554
        ycenter = 511
        radius = 258

        # Define the circular viewport location

        if creating == 1:
            viewportstart = 165
            viewportheight = 315
            scrollbarstart = 135
            scrollbarheight = 331
        else:
            viewportstart = 105
            viewportheight = 322
            scrollbarstart = 75
            scrollbarheight = 339

        lineheight = 48

        if creating == 1:
            fetishCount = 0
            for fetish in player.FetishList:
                if fetish.Type == "Fetish":
                    fetishCount += 1

            boxheight = fetishCount*lineheight
            excess = boxheight-viewportheight
        else:
            perkEntries = on_getPerkEntries()

            boxheight = len(perkEntries)*lineheight
            excess = boxheight-viewportheight

    # Control the circular viewport via mousewheel scroll
    key "mousedown_4" action SetVariable("vp_position", max(min(vp_position-15, excess), 0))
    key "mousedown_5" action SetVariable("vp_position", max(min(vp_position+15, excess), 0))

    key "keydown_K_RSHIFT" action SetVariable("shifting", 5)
    key "keyup_K_RSHIFT" action SetVariable("shifting", 1)
    key "keydown_K_LSHIFT" action SetVariable("shifting", 5)
    key "keyup_K_LSHIFT" action SetVariable("shifting", 1)


    # Fetishes!
    # No tuples this time since we're getting the list from player.FetishList directly
    if creating == 1:

        # Backdrop and circular viewport scrollbar
        add "gui/levelmenu_right.png" xpos 0 ypos 0

        if renpy.variant("touch"):
            $ UseFancyScrollBar = False
        else:
            fixed:
                xpos 1770
                ypos 310
                if UseFancyScrollBar == True:
                    imagebutton:
                        hovered [tt.Action("Simplify the fetish scrollbar!"), Jump("characterCreation")]
                        idle "gui/circlebuttonsmallchecked.png"
                        hover "gui/circlebuttonsmallchecked_hover.png"
                        action [ SetVariable("UseFancyScrollBar", False) ]
                else:
                    imagebutton:
                        hovered [tt.Action("Fancify the fetish scrollbar!"), Jump("characterCreation")]
                        idle "gui/circlebuttonsmall.png"
                        hover "gui/circlebuttonsmall_hover.png"
                        action [ SetVariable("UseFancyScrollBar", True) ]
        if renpy.variant("touch") or UseFancyScrollBar == False:
            $ excess = excess
        elif (excess > 0):
            add "gui/perk_circlebarback.png" at pmenu_crop(scrollbarstart, scrollbarheight-1, xcenter, ycenter)
            #add "gui/perk_circlebar.png" at pmenu_crop(scrollbarstart + int(scrollbarheight*float(vp_position)/boxheight), int(scrollbarheight*float(viewportheight)/boxheight), xcenter, ycenter)

            imagebutton:
                idle "gui/perk_circlebar.png"
                hover "gui/perk_circlebar.png"
                insensitive "gui/perk_circlebar.png"
                #hovered [SetVariable ("vp_position", max(min(renpy.get_mouse_pos()[1], excess), 0))]
                #action [SetVariable ("vp_position", max(min(vp_position+15, excess), 0))]
                #alternate [SetVariable ("vp_position", max(min(vp_position-15, excess), 0))]
                at pmenu_crop(scrollbarstart + int(scrollbarheight*float(vp_position)/boxheight), int(scrollbarheight*float(viewportheight)/boxheight), xcenter, ycenter)

        frame:
            xcenter xcenter
            ycenter 337

            xpadding 5
            ypadding 5
            vbox:
                ysize 40
                text "Fetishes are a glaring weakness." xalign 0.5 yoffset 2 color header_color size 22
                text "You need at least one.":
                    xalign 0.5
                    yoffset -1
                    size 22
                    if (tentativeStats.fetishTotal() <= 0):
                        color "#ff2200"
                    else:
                        color header_color
        frame:
            xcenter xcenter
            ycenter 273
            xpadding theXpadding
            ypadding theYpadding
            text "Fetishes" size fontsize xalign 0.5 yalign 0.5 color header_color

        if renpy.variant("touch")  or UseFancyScrollBar == False:
            $ theScrollID = "CharScroll"
            fixed:
                xalign 0.89
                yalign 0.49
                xsize 375
                ysize 290
                viewport id theScrollID:
                    mousewheel True
                    draggable True
                    side_yfill True
                    vbox:
                        for i, fetish in enumerate(tentativeStats.FetishList):
                            if fetish.Type == "Fetish":
                                hbox:
                                    if fetish.Level > 0:
                                        imagebutton:

                                            idle "gui/circlebuttonsmallchecked.png"
                                            hover "gui/circlebuttonsmallchecked_hover.png"
                                            action [
                                                SetVariable("setThisFetish", i),
                                                tt.Action(fetish.CreationOff),
                                                Jump ("setFetish")]
                                    else:
                                        imagebutton:
                                            idle "gui/circlebuttonsmall.png"
                                            hover "gui/circlebuttonsmall_hover.png"
                                            action [
                                                SetVariable("setThisFetish", i),
                                                tt.Action(fetish.CreationOn),
                                                Jump ("setFetish")]

                                    text fetish.name:
                                        yalign 0.5 xoffset 7
                                        color entry_color
                vbar value YScrollValue(theScrollID) xpos 330 ysize 290-16 yoffset 8 unscrollable "hide"
        else:
            $ _fv = 0
            vbox:
                xpos xcenter-300
                at pmenu_crop2(vp_position, viewportheight, ycenter + viewportstart - vp_position - 283)

                for i, fetish in enumerate(tentativeStats.FetishList):
                    if fetish.Type == "Fetish":
                        hbox:
                            if renpy.variant("touch") or UseFancyScrollBar == False:
                                xpos 300
                                ysize lineheight
                            else:
                                xpos 300-on_getXPosOnCircle(radius-24, _fv*lineheight - (radius-viewportstart) - vp_position)
                                ysize lineheight

                            if fetish.Level > 0:
                                imagebutton:
                                    xpos -16
                                    idle "gui/circlebuttonsmallchecked.png"
                                    hover "gui/circlebuttonsmallchecked_hover.png"
                                    action [
                                        SetVariable("setThisFetish", i),
                                        tt.Action(fetish.CreationOff),
                                        Jump ("setFetish")]
                            else:
                                imagebutton:
                                    xpos -16
                                    idle "gui/circlebuttonsmall.png"
                                    hover "gui/circlebuttonsmall_hover.png"
                                    action [
                                        SetVariable("setThisFetish", i),
                                        tt.Action(fetish.CreationOn),
                                        Jump ("setFetish")]

                            text fetish.name:
                                yalign 0.5 xoffset -7
                                color entry_color
                        $ _fv +=1
    # Perk screen
    elif tentativeStats.perkPoints > 0:

        # Backdrop and circular viewport scrollbar
        add "gui/levelmenu_right.png" xpos 0 ypos 0

        if renpy.variant("touch"):
            $ UseFancyScrollBar = False
        else:
            fixed:
                xpos 1770
                ypos 310
                if UseFancyScrollBar == True:
                    imagebutton:
                        hovered [tt.Action("Simplify the perk scrollbar!"), Jump("characterCreation")]
                        idle "gui/circlebuttonsmallchecked.png"
                        hover "gui/circlebuttonsmallchecked_hover.png"
                        action [ SetVariable("UseFancyScrollBar", False) ]
                else:
                    imagebutton:
                        hovered [tt.Action("Fancify the perk scrollbar!"), Jump("characterCreation")]
                        idle "gui/circlebuttonsmall.png"
                        hover "gui/circlebuttonsmall_hover.png"
                        action [ SetVariable("UseFancyScrollBar", True) ]

        if renpy.variant("touch") or UseFancyScrollBar == False:
            $ excess = excess
        elif (excess > 0):
            add "gui/perk_circlebarback.png" at pmenu_crop(scrollbarstart, scrollbarheight-1, xcenter, ycenter)
            #add "gui/perk_circlebar.png" at pmenu_crop(scrollbarstart + int(scrollbarheight*float(vp_position)/boxheight), int(scrollbarheight*float(viewportheight)/boxheight), xcenter, ycenter)
            imagebutton:
                idle "gui/perk_circlebar.png"
                hover "gui/perk_circlebar.png"
                insensitive "gui/perk_circlebar.png"
                #hovered [SetVariable ("vp_position", max(min(renpy.get_mouse_pos()[1], excess), 0))]
                #action [SetVariable ("vp_position", max(min(vp_position+15, excess), 0))]
                #alternate [SetVariable ("vp_position", max(min(vp_position-15, excess), 0))]
                at pmenu_crop(scrollbarstart + int(scrollbarheight*float(vp_position)/boxheight), int(scrollbarheight*float(viewportheight)/boxheight), xcenter, ycenter)

        frame:
            xcenter xcenter
            ycenter 263
            xpadding theXpadding
            ypadding theYpadding
            text "Perk points: [tentativeStats.perkPoints]" size fontsize xalign 0.5 yalign 0.5 color header_color

        fixed:
            xcenter xcenter+10
            xsize 224
            ypos 275
            if TogglePerkFilter == True:
                use ON_TextButtonSmol("Filters", action=[SetVariable("TogglePerkFilter", False)], hovered=[tt.Action("Toggle the perk filter menu."), Jump("characterCreation")])
            else:
                use ON_TextButtonSmol("Filters", action=[SetVariable("TogglePerkFilter", True)], hovered=[tt.Action("Toggle the perk filter menu."), Jump("characterCreation")])


        if TogglePerkFilter == True:
            frame:
                xcenter xcenter
                xsize 380
                ypos 14
                xpadding 8
                ypadding 12
                vbox:
                    xalign 0.5
                    text "Perk Filters" size 25 xalign 0.5
                    if PerkOrder == "None":
                        textbutton "Alphabetical Order" text_size on_listTextSize action [SetVariable ("PerkOrder", "Alphebetical"), Jump("SortPerksByAlphebet")] xalign 0.5
                    else:
                        textbutton "Normal Order" text_size on_listTextSize action [SetVariable ("PerkOrder", "None"), Jump("SortPerksByNormal")] xalign 0.5
                    hbox:
                        xalign 0.5
                        textbutton "No Filter" text_size on_listTextSize action [SetVariable ("PerkFilter", "None"), Jump("characterCreation")] xalign 0.5
                        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
                        textbutton "Neutral" text_size on_listTextSize action [SetVariable ("PerkFilter", ""), Jump("characterCreation")] xalign 0.5
                    hbox:
                        xalign 0.5
                        textbutton "Power" text_size on_listTextSize action [SetVariable ("PerkFilter", "Power"), Jump("characterCreation")] xalign 0.5
                        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
                        textbutton "Technique" text_size on_listTextSize action [SetVariable ("PerkFilter", "Technique"), Jump("characterCreation")] xalign 0.5
                    hbox:
                        xalign 0.5
                        textbutton "Intelligence" text_size on_listTextSize action [SetVariable ("PerkFilter", "Intelligence"), Jump("characterCreation")] xalign 0.5
                        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
                        textbutton "Allure" text_size on_listTextSize action [SetVariable ("PerkFilter", "Allure"), Jump("characterCreation")] xalign 0.5
                    hbox:
                        xalign 0.5
                        textbutton "Willpower" text_size on_listTextSize action [SetVariable ("PerkFilter", "Willpower"), Jump("characterCreation")] xalign 0.5
                        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
                        textbutton "Luck" text_size on_listTextSize action [SetVariable ("PerkFilter", "Luck"), Jump("characterCreation")] xalign 0.5

        # Stick everything in a vbox
        # x position is offset based on its location in the list and vp_position
        # Then the vbox is moved up by vp_position and cropped so items are in the right place
        if renpy.variant("touch") or UseFancyScrollBar == False:
            $ theScrollID = "CharScroll"
            fixed:
                xalign 0.89
                yalign 0.46
                xsize 400
                ysize 290
                viewport id theScrollID:
                    mousewheel True
                    draggable True
                    side_yfill True
                    vbox:
                        for i, entry in enumerate(perkEntries):
                            hbox:
                                if perkChosen == entry[0].name:
                                    if entry[1]:
                                        imagebutton:
                                            hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                            idle "gui/circlebuttonsmallchecked.png"
                                            hover "gui/circlebuttonsmallchecked_hover.png"
                                            insensitive "gui/circlebuttonsmallchecked_insensitive.png"
                                            action [ SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                                    else:
                                        imagebutton:
                                            hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                            idle "gui/circlebuttonsmallchecked.png"
                                            hover "gui/circlebuttonsmallchecked_hover.png"
                                            insensitive "gui/circlebuttonsmallchecked_insensitive.png"
                                            action [ SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                                else:
                                    if entry[1]:
                                        imagebutton:
                                            hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                            idle "gui/circlebuttonsmall.png"
                                            hover "gui/circlebuttonsmall_hover.png"
                                            insensitive "gui/circlebuttonsmall_insensitive.png"
                                            action [SetVariable("perkChosen", entry[0].name), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                                    else:
                                        imagebutton:
                                            hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                            idle "gui/circlebuttonsmall.png"
                                            hover "gui/circlebuttonsmall_hover.png"
                                            insensitive "gui/circlebuttonsmall_insensitive.png"
                                            action [SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]

                                text entry[0].name:
                                    yalign 0.5 xoffset 7
                                    color (entry_color if entry[1] else gui.insensitive_color)
                vbar value YScrollValue(theScrollID) xpos 405 ysize 290-16 yoffset 8 unscrollable "hide"
        else:
            vbox:
                xpos xcenter-300
                at pmenu_crop2(vp_position, viewportheight, ycenter + viewportstart - vp_position - 283)

                for i, entry in enumerate(perkEntries):
                    hbox:
                        xpos 300-on_getXPosOnCircle(radius-24, i*lineheight - (radius-viewportstart) - vp_position)
                        ysize lineheight

                        if perkChosen == entry[0].name:
                            if entry[1]:
                                imagebutton:
                                    xpos -16
                                    hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                    idle "gui/circlebuttonsmallchecked.png"
                                    hover "gui/circlebuttonsmallchecked_hover.png"
                                    insensitive "gui/circlebuttonsmallchecked_insensitive.png"
                                    action [ SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                            else:
                                imagebutton:
                                    xpos -16
                                    hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                    idle "gui/circlebuttonsmallchecked.png"
                                    hover "gui/circlebuttonsmallchecked_hover.png"
                                    insensitive "gui/circlebuttonsmallchecked_insensitive.png"
                                    action [ SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                        else:
                            if entry[1]:
                                imagebutton:
                                    xpos -16
                                    hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                    idle "gui/circlebuttonsmall.png"
                                    hover "gui/circlebuttonsmall_hover.png"
                                    insensitive "gui/circlebuttonsmall_insensitive.png"
                                    action [SetVariable("perkChosen", entry[0].name), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]
                            else:
                                imagebutton:
                                    xpos -16
                                    hovered [tt.Action(entry[2]), Jump("characterCreation")]
                                    idle "gui/circlebuttonsmall.png"
                                    hover "gui/circlebuttonsmall_hover.png"
                                    insensitive "gui/circlebuttonsmall_insensitive.png"
                                    action [SetVariable("perkChosen", ""), SetVariable("perkBuyUse", entry[1]), tt.Action(entry[2])]

                        text entry[0].name:
                            yalign 0.5 xoffset -7
                            color (entry_color if entry[1] else gui.insensitive_color)

        # Confirm button near the bottom
        if perkChosen and len(perkEntries) > 0:
            frame:
                xminimum 280
                xcenter xcenter ypos 664
                xpadding theXpadding
                ypadding theYpadding
                text "Perk chosen: [perkChosen]" xalign 0.5 yalign 0.5
                ysize 55

            fixed:
                use ON_TextButton("Confirm choice", action=[Jump("getPerk")], hovered=[tt.Action("Are you sure you want this perk?"), Jump("characterCreation")])
                xcenter xcenter
                xsize 324
                ypos 714
                # Stick everything in a vbox
                # x position is offset based on its location in the list and vp_position
                # Then the vbox is moved up by vp_position and cropped so items are in the right place


    # Center menu: Stats
    frame:
        xcenter 960
        ycenter 75
        xpadding theXpadding
        ypadding theYpadding
        text "Stat points: [tentativeStats.statPoints]" xalign 0.5 yalign 0.5 size fontsize color header_color

    # Difficulty button is just kind of sticking out to the side, maybe need to do something else with it
    if creating == 1:
        fixed:
            xpos 750
            ypos 258
            vbox:
                text "Difficulty:" xalign 0.5 yoffset 5
                use ON_TextButtonMid(text="[difficulty]", action=Jump("changeDiffuculty"))
    else:
        fixed:
            xpos 750
            ypos 258
            vbox:
                use ON_TextButtonMid(text="Confirm Stats", action=Jump("lockInStats"))

    # Stats are all in tuples again
    # same format: (DisplayName, label for increase, label for decrease, number to display, tooltip)
    python:
        powerDisplay = tentativeStats.stats.Power-tentativeStats.getStatBonusReduction("Power")
        techDisplay = tentativeStats.stats.Tech-tentativeStats.getStatBonusReduction("Technique")
        intDisplay = tentativeStats.stats.Int-tentativeStats.getStatBonusReduction("Intelligence")
        allureDisplay = tentativeStats.stats.Allure-tentativeStats.getStatBonusReduction("Allure")
        willDisplay = tentativeStats.stats.Willpower-tentativeStats.getStatBonusReduction("Willpower")
        luckDisplay = tentativeStats.stats.Luck-tentativeStats.getStatBonusReduction("Luck")
        attrs_arr = [
            ("{color=#F7B}Arousal: {/color}", "StatChange", 10, -10, 1,  "{color=#F7B}[tentativeStats.stats.max_true_hp]{/color}", "The amount of sexual stimulation you can take! When it hits its max, you lose spirit.", "Arousal", hpFloor, hpCap, tentativeStats.stats.max_hp ),
            ("{color=#7DF}Energy: {/color}", "StatChange", 10, -10, 1, "{color=#7DF}[tentativeStats.stats.max_true_ep]{/color}", "Your personal reserves of energy, or mana as some like to call it, it's used for skills and magic!", "Energy", epFloor, epCap, tentativeStats.stats.max_ep),
            ("Spirit: ", "StatChange", 1, -1, 3, "[tentativeStats.stats.max_sp]", "Your life energy! If this runs out, you won't be able to fight back. You lose at least one per orgasm. Really, it's just a measurement of how many times you can cum normally. You gain 3 stat points for each reduction at character creation, it can't be increased with stat points after character creation. Can't go higher than 3 at character creation unless you're on easy.", "Spirit", spFloor, spCap, tentativeStats.stats.max_sp)]
        stats_arr = [
            ("Power: ", "StatChange", 1, -1, 1, "[powerDisplay]", "Escape restraints, 'punish' your foes, maintain or get out of sexual positions, and deal increased critical arousal! Every 5 points naturally gained increases your max arousal by 10. Boosts how much damage you do with core skills!", "Power", powFloor, powCap, tentativeStats.stats.Power),
            ("Technique: ", "StatChange", 1, -1, 1, "[techDisplay]", "Used for evading, acting faster, running away, and sexual finesse! It also helps you get out of stances and restraints, but it is not as effective as power. Boosts how much damage you do with core skills!", "Technique", spdFloor, spdCap, tentativeStats.stats.Tech),
            ("Intelligence: ", "StatChange", 1, -1, 1, "[intDisplay]", "Cast magic, resist some temptations, increase your chance to apply status effects, and increase the duration of your status effect! Every 5 points gained naturally increases your max energy by 10. Boosts how much damage you do with core skills!", "Intelligence", intFloor, intCap, tentativeStats.stats.Int),
            ("Allure: ", "StatChange", 1, -1, 1, "[allureDisplay]", "Seduce and charm your foes! It increases how much arousal you deal with all skills, including increased critical arousal, and boosts how much damage you do with core skills! Also increases the recoil damage your opponent takes, from sex skills for example!", "Allure", allFloor, allCap, tentativeStats.stats.Allure),
            ("Willpower: ", "StatChange", 1, -1, 1, "[willDisplay]", "Greatly resist temptation, status effects, and reduces how much arousal you take! Every 5 points increases your max arousal and max energy by 5.", "Willpower", wilFloor, wilCap, tentativeStats.stats.Willpower),
            ("Luck: ", "StatChange", 1, -1, 1, "[luckDisplay]", "Helps a little bit across the board. Such as acting before others, getting out of restraints, running away, hitting or dodging attacks, and improves your critical chance! But best of all it helps you find more treasure!", "Luck", lukFloor, lukCap, tentativeStats.stats.Luck)]

        # define the menu location
        xcenter = 960
        ycenter = 349
        radius = 297
        if renpy.variant("touch"):
            theta = -0.86
        else:
            theta = -0.80

    # Loop through arousal/energy/spirit
    for s in attrs_arr:
        $ x = int(xcenter + radius*math.cos(theta))
        $ y = int(ycenter + radius*math.sin(theta))

        if s[0] == "Spirit: " and creating == 0:
            add "gui/circlebuttonlarge.png" xcenter x ycenter y
        else:
            add "gui/circlebuttonlarge.png" xcenter x ycenter y

            if renpy.variant("touch"):
                $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
                $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
                $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
                $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"
                $ xScreenPos = 65
            else:
                $ buttonIdleImgDown = "gui/Button_dec_idle.png"
                $ buttonHoverImgDown = "gui/Button_dec_hover.png"
                $ buttonIdleImgUp = "gui/Button_inc_idle.png"
                $ buttonHoverImgUp = "gui/Button_inc_hover.png"
                $ xScreenPos = 52
            imagebutton:
                idle buttonIdleImgDown
                hover buttonHoverImgDown
                xcenter x-xScreenPos
                ycenter y
                action SetVariable("changingStat", s[3]), SetVariable("statCost", s[4]), SetVariable("typeText", s[7]), SetVariable("theStatFloor", s[8]), SetVariable("theStatCap", s[9]), SetVariable("ChangeThisStat", s[10]), Jump(s[1])
                hovered tt.Action(s[6])
                unhovered tt.Action("")

            imagebutton:
                idle buttonIdleImgUp
                hover buttonHoverImgUp
                xcenter x+xScreenPos
                ycenter y
                action SetVariable("changingStat", s[2]), SetVariable("statCost", s[4]), SetVariable("typeText", s[7]),  SetVariable("theStatFloor", s[8]), SetVariable("theStatCap", s[9]), SetVariable("ChangeThisStat", s[10]),  Jump(s[1])
                hovered tt.Action(s[6])
                unhovered tt.Action("")


        text s[5] xcenter x ycenter y
        if s[0] == "Spirit: " and creating == 0:
            text s[0] xpos x-29 xalign 1.0 ycenter y color entry_color
        else:
            if renpy.variant("touch"):
                text s[0] xpos x-85 xalign 1.0 ycenter y color entry_color
            else:
                text s[0] xpos x-55 xalign 1.0 ycenter y color entry_color
        if renpy.variant("touch"):
            $ theta += 0.272
        else:
            $ theta += 0.26

    # Add a small gap between arousal/energy/spirit and the other 5 stats
    if renpy.variant("touch"):
        $ theta -= 0.001
    else:
        $ theta += 0.03

    # Loop through the other stats using a different button graphic/size
    for s in stats_arr:
        $ x = int(xcenter + radius*math.cos(theta))
        $ y = int(ycenter + radius*math.sin(theta))

        add "gui/circlebutton.png" xcenter x ycenter y

        if renpy.variant("touch"):
            $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
            $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
            $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
            $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"
            $ xScreenPos = 60
        else:
            $ buttonIdleImgDown = "gui/Button_dec_idle.png"
            $ buttonHoverImgDown = "gui/Button_dec_hover.png"
            $ buttonIdleImgUp = "gui/Button_inc_idle.png"
            $ buttonHoverImgUp = "gui/Button_inc_hover.png"
            $ xScreenPos = 45
        imagebutton:
            idle buttonIdleImgDown
            hover buttonHoverImgDown
            xcenter x-xScreenPos
            ycenter y
            action SetVariable("changingStat", s[3]), SetVariable("statCost", s[4]), SetVariable("typeText", s[7]),  SetVariable("theStatFloor", s[8]), SetVariable("theStatCap", s[9]),  SetVariable("ChangeThisStat", s[10]),    Jump(s[1])
            hovered tt.Action(s[6])
            unhovered tt.Action("")

        imagebutton:
            idle buttonIdleImgUp
            hover buttonHoverImgUp
            xcenter x+xScreenPos
            ycenter y
            action SetVariable("changingStat", s[2]), SetVariable("statCost", s[4]), SetVariable("typeText", s[7]),  SetVariable("theStatFloor", s[8]), SetVariable("theStatCap", s[9]),  SetVariable("ChangeThisStat", s[10]),    Jump(s[1])
            hovered tt.Action(s[6])
            unhovered tt.Action("")

        text s[5] xcenter x ycenter y
        if renpy.variant("touch"):
            text s[0] xpos x-85 xalign 1.0 ycenter y color entry_color
        else:
            text s[0] xpos x-50 xalign 1.0 ycenter y color entry_color
        if renpy.variant("touch"):
            $ theta += 0.23
        else:
            $ theta += 0.21

        # cheap hack: add extra space after willpower and allure to space out text
        if s[0] == "Intelligence: ":
            $ theta += 0.01
        if s[0] == "Willpower: ":
            if renpy.variant("touch"):
                $ theta += 0.17
            else:
                $ theta += 0.09
        if s[0] == "Allure: ":
            if renpy.variant("touch"):
                $ theta += 0.04
            else:
                $ theta += 0.02
        if s[0] == "Luck: ":
            $ theta += 0.01


    # Finished button - maybe needs to draw more attention?
    if creating == 1:
        textbutton "Finished!" action [SensitiveIf(done), Jump("creatorEndHideScreen")] xcenter 0.5 ycenter 705 text_size fontsize
    elif respeccing == 1:
        textbutton "Finished!" action [SensitiveIf(player.SensitivityPoints >= 0), Jump("endLvling")] xcenter 0.5 ycenter 705 text_size fontsize
    else:
        textbutton "Finished!" action [Jump("endLvling")] xcenter 0.5 ycenter 705 text_size fontsize

label StatChange:

    #"[shifting]"

    $ TemporaryStatCheck = tentativeStats.getStatBonusReduction(typeText)

    $ tentativeStats.creatorLvlStat(ChangeThisStat, changingStat*shifting, theStatFloor, theStatCap, statCost*shifting, typeText, TemporaryStatCheck)

    $ tentativeStats.CalculateStatBoost()


    if typeText == "Spirit":
        $ tentativeStats.stats.sp = tentativeStats.stats.max_true_sp
    jump characterCreation

######SensitivityFUNC###########


label lockInStats:
    $ player = copy.deepcopy(tentativeStats)
    $ tentativeStats = copy.deepcopy(player)
    call setStatFloors from _call_setStatFloors_2
    jump characterCreation

label SenChange:
    $ TemporarySensCheck = tentativeStats.BodySensitivity.getSensBonusReduction(tentativeStats, typeText)

    $ tentativeStats.BodySensitivity.creatorSetRes(sens_arr[ChangeThisStat][8], changingStat*shifting, theStatFloor, theStatCap, statCost*shifting, TemporarySensCheck, typeText)


    jump characterCreation

label getPerk:
    if tentativeStats.perkPoints >= 1 and perkChosen != "" and perkBuyUse == True:
        $ tentativeStats.perkPoints -= 1
        $ tentativeStats.giveOrTakePerk(perkChosen, 1)
        $ perktemp = perkChosen
        $ perkChosen = ""

        if (tentativeStats.SensitivityPoints > 0):
            $ hasResPoints = 1
        "You got the [perktemp] perk!"

    jump characterCreation

label SortPerksByAlphebet:
    $ PerkDatabaseLVLDisplay = copy.deepcopy(sorted(LevelingPerkDatabase, key = lambda x: x.name))
    jump characterCreation

label SortPerksByNormal:
    $ PerkDatabaseLVLDisplay = copy.deepcopy(LevelingPerkDatabase)
    jump characterCreation

# setFetish label not based on that odd 4-element array thingy
label setFetish:
    if tentativeStats.FetishList[setThisFetish].Level >= 1:
        $ tentativeStats.FetishList[setThisFetish].Level = 0
        $ tentativeStats.FetishList[setThisFetish].LevelPerm = 0
        $ tentativeStats.FetishList[setThisFetish].LevelMin = 0
    else:
        $ tentativeStats.FetishList[setThisFetish].Level = 25
        $ tentativeStats.FetishList[setThisFetish].LevelPerm = 25
        $ tentativeStats.FetishList[setThisFetish].LevelMin = 25
    jump characterCreation

label changeDiffuculty:
    if difficulty == "Normal":
        $ tt = Tooltip("Ah... Are you perhaps a masochist? Or do you just want to challenge yourself?")
        $ difficulty = "Hard"
        $ player.SensitivityPoints = 1
        $ player.BodySensitivity.resetSens("Sex", player)
        $ player.BodySensitivity.resetSens("Ass", player)
        $ player.BodySensitivity.resetSens("Breasts", player)
        $ player.BodySensitivity.resetSens("Mouth", player)
        $ player.BodySensitivity.resetSens("Seduction", player)
        $ player.BodySensitivity.resetSens("Magic", player)
        $ player.BodySensitivity.resetSens("Pain", player)
        $ player.stats.max_hp=copy.deepcopy(hardHp)
        $ player.stats.hp=0
        $ player.stats.max_ep=copy.deepcopy(hardEp)
        $ player.stats.ep=copy.deepcopy(hardEp)
        $ player.stats.max_sp=copy.deepcopy(hardSp)
        $ player.stats.sp=copy.deepcopy(hardSp)
        $ player.stats.Power = copy.deepcopy(hardCoreStat)
        $ player.stats.Tech = copy.deepcopy(hardCoreStat)
        $ player.stats.Int = copy.deepcopy(hardCoreStat)
        $ player.stats.Allure = copy.deepcopy(hardCoreStat)
        $ player.stats.Willpower = copy.deepcopy(hardCoreStat)
        $ player.stats.Luck = copy.deepcopy(hardCoreStat)

        $ player.statPoints = 20

    elif difficulty == "Hard":
        $ tt = Tooltip("Oh my, with this kind of power, it won't take long for you to beat the Demon Queen... You're just going to go 'sight seeing', aren't you?\n(Fully restore spirit on level ups in addition to higher stats.)")
        $ difficulty = "Easy"
        $ player.SensitivityPoints = 5
        $ player.BodySensitivity.resetSens("Sex", player)
        $ player.BodySensitivity.resetSens("Ass", player)
        $ player.BodySensitivity.resetSens("Breasts", player)
        $ player.BodySensitivity.resetSens("Mouth", player)
        $ player.BodySensitivity.resetSens("Seduction", player)
        $ player.BodySensitivity.resetSens("Magic", player)
        $ player.BodySensitivity.resetSens("Pain", player)
        $ player.stats.max_hp= copy.deepcopy(easyHp)
        $ player.stats.hp=0
        $ player.stats.max_ep=copy.deepcopy(easyEp)
        $ player.stats.ep=copy.deepcopy(easyHp)
        $ player.stats.max_sp= copy.deepcopy(easySp)
        $ player.stats.sp= copy.deepcopy(easySp)
        $ player.stats.Power = copy.deepcopy(easyCoreStat)
        $ player.stats.Tech = copy.deepcopy(easyCoreStat)
        $ player.stats.Int = copy.deepcopy(easyCoreStat)
        $ player.stats.Allure = copy.deepcopy(easyCoreStat)
        $ player.stats.Willpower = copy.deepcopy(easyCoreStat)
        $ player.stats.Luck = copy.deepcopy(easyCoreStat)

        $ player.statPoints = 10

        call EasyStats from _call_EasyStats

    elif difficulty == "Easy":
        $ difficulty = "Normal"
        $ tt = Tooltip("Yes, this seems about right for an adventurer.")
        $ player.SensitivityPoints = 3
        $ player.BodySensitivity.resetSens("Sex", player)
        $ player.BodySensitivity.resetSens("Ass", player)
        $ player.BodySensitivity.resetSens("Breasts", player)
        $ player.BodySensitivity.resetSens("Mouth", player)
        $ player.BodySensitivity.resetSens("Seduction", player)
        $ player.BodySensitivity.resetSens("Magic", player)
        $ player.BodySensitivity.resetSens("Pain", player)
        $ player.stats.max_hp= copy.deepcopy(normalHp)
        $ player.stats.hp=0
        $ player.stats.max_ep= copy.deepcopy(normalEp)
        $ player.stats.ep= copy.deepcopy(normalEp)
        $ player.stats.max_sp= copy.deepcopy(normalSp)
        $ player.stats.sp= copy.deepcopy(normalSp)
        $ player.stats.Power = copy.deepcopy(normalCoreStat)
        $ player.stats.Tech = copy.deepcopy(normalCoreStat)
        $ player.stats.Int = copy.deepcopy(normalCoreStat)
        $ player.stats.Allure = copy.deepcopy(normalCoreStat)
        $ player.stats.Willpower = copy.deepcopy(normalCoreStat)
        $ player.stats.Luck = copy.deepcopy(normalCoreStat)

        $ player.statPoints = 5
        call NormalStats from _call_NormalStats
    $ player.CalculateStatBoost()
    $ tentativeStats = copy.deepcopy(player)

    jump characterCreation

label spendLvlUpPoints:
    if player.SensitivityPoints > 0:
        $ hasResPoints = 1
    else:
        $ hasResPoints = 0

    hide screen ON_HealthDisplay
    $ tentativeStats = copy.deepcopy(player)
    call setStatFloors from _call_setStatFloors_1
    call characterCreation from _call_characterCreation_1
    hide screen ON_CreatorDisplay

    return

label characterCreation:
    $ player.CalculateStatBoost()
    show screen ON_CreatorDisplay
    if tt.value != "":
        Goddess "[tt.value]"
    else:
        pause
    jump characterCreation

label endLvling:
    hide screen ON_CreatorDisplay
    $ player = copy.deepcopy(tentativeStats)
    call setStatFloors from _call_setStatFloors_3
    $ tentativeStats = Player()
    show screen ON_HealthDisplayBacking #(_layer="hplayer")
    show screen ON_HealthDisplay #(_layer="sayScreen")
    return

label creatorEndHideScreen:
    hide screen ON_CreatorDisplay
    $ player = copy.deepcopy(tentativeStats)
    call setStatFloors from _call_setStatFloors_4
    $ tentativeStats = Player()
    jump creatorEnd



screen ON_AppearanceCreator():
    # Backdrop for center (behind everything)
    add "gui/adventurecards.png" xpos 150 ypos 0

    vbox:
        xpos 442
        ypos 202
        if PlayerDisplay == "Body":
            label _("Opacity")
            hbox:
                bar value VariableValue("PlayerOpacity", 1.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerOpacity]"
            label _("Brightness")
            hbox:
                bar value VariableValue("PlayerBrightness", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]

                text "[PlayerBrightness]"
            label _("Hue")
            hbox:
                bar value VariableValue("PlayerHue", 360):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerHue]"

            label _("Saturation")
            hbox:
                bar value VariableValue("PlayerSaturation", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSaturation]"
            label _("R")
            hbox:
                bar value VariableValue("PlayerSaturationR", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSaturationR]"
            label _("G")
            hbox:
                bar value VariableValue("PlayerSaturationG", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSaturationG]"
            label _("B")
            hbox:
                bar value VariableValue("PlayerSaturationB", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSaturationB]"
            #label _("Tint - [PlayerTint] - Hex Code")
            #hbox:
            #    input default "" copypaste True value VariableInputValue("currentTint", True, True) length 9
        elif PlayerDisplay == "Silhouette":
            label _("Opacity")
            hbox:
                bar value VariableValue("PlayerSilOpacity", 1.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSilOpacity]"
            label _("Brightness")
            hbox:
                bar value VariableValue("PlayerSilBrightness", 2.0):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]

                text "[PlayerSilBrightness]"
            label _("Hue")
            hbox:
                bar value VariableValue("PlayerSilHue", 360):
                    xmaximum 400
                    ymaximum 40
                    changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
                text "[PlayerSilHue]"

            #label _("Saturation")
            #hbox:
            #    bar value VariableValue("PlayerSilSaturation", 2.0):
            #        xmaximum 400
            #        ymaximum 40
            #        changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
            #    text "[PlayerSilSaturation]"
            #label _("R")
            #hbox:
            #    bar value VariableValue("PlayerSilSaturationR", 2.0):
            #        xmaximum 400
            #        ymaximum 40
            #        changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
            #    text "[PlayerSilSaturationR]"
            #label _("G")
            #hbox:
            #    bar value VariableValue("PlayerSilSaturationG", 2.0):
            #        xmaximum 400
            #        ymaximum 40
            #        changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
            #    text "[PlayerSilSaturationG]"
            #label _("B")
            #hbox:
            #    bar value VariableValue("PlayerSilSaturationB", 2.0):
            #        xmaximum 400
            #        ymaximum 40
            #        changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
            #    text "[PlayerSilSaturationB]"
            #label _("Tint - [PlayerTint] - Hex Code")
            #hbox:
                #input default "" copypaste True value VariableInputValue("currentTint", True, True) length 9

    hbox:
        xpos 1050 ycenter 320
        textbutton "Body" action [SensitiveIf(PlayerDisplay == "Silhouette"), SetVariable("PlayerDisplay", "Body")]  text_size fontsize
        text "/"
        textbutton "Silhouette" action [SensitiveIf(PlayerDisplay == "Body"), SetVariable("PlayerDisplay", "Silhouette")]  text_size fontsize

    textbutton "Reset to Defaults." action [Jump("ResetAppearanceDefaults")] xcenter 0.5 ycenter 865 text_size fontsize
    textbutton "Finished!" action [Jump("DoneAppearanceCreator")] xcenter 0.5 ycenter 950 text_size fontsize

screen ON_AppearanceCreatorShowSample():
    if PlayerDisplay == "Body":
        add "images/torsoTest.png" xpos 950 ypos 350 at CharacterBrightness, CharacterColor, CharacterOpacity, CharacterTint,  CharacterSaturation
    else:
        add "images/SilhouetteTest.png" xpos 950 ypos 350 at CharacterSilBrightness, CharacterSilColor, CharacterSilOpacity, CharacterSilTint,  CharacterSilSaturation


label AppearanceCreator:
    show screen ON_AppearanceCreator
    $ currentTint = copy.deepcopy(PlayerTint)
    jump AppearanceCreatorMenu

label AppearanceCreatorMenu:
    show screen ON_AppearanceCreatorShowSample
    pause
    hide screen ON_AppearanceCreatorShowSample
    if len(currentTint) >= 1:
        if currentTint[0] == "#" :
            if len(currentTint) == 4 or len(currentTint) == 5 or len(currentTint) == 7 or len(currentTint) == 9:
                $ PlayerTint = copy.deepcopy(currentTint)

    jump AppearanceCreatorMenu






label ResetAppearanceDefaults:
    hide screen ON_AppearanceCreator
    hide screen ON_AppearanceCreatorShowSample
    if PlayerDisplay == "Body":
        $ PlayerHue = 1.0
        $ PlayerBrightness = 1.0
        $ PlayerOpacity = 1.0
        $ PlayerSaturation = 1.0
        $ PlayerSaturationR = 0.2126
        $ PlayerSaturationG = 0.7152
        $ PlayerSaturationB = 0.0722
        $ PlayerTint = "#FFFFFF"
    else:
        $ PlayerSilHue = 1.0
        $ PlayerSilBrightness = 1.0
        $ PlayerSilOpacity = 0.9
        $ PlayerSilSaturation = 1.0
        $ PlayerSilSaturationR = 0.2126
        $ PlayerSilSaturationG = 0.7152
        $ PlayerSilSaturationB = 0.0722
        $ PlayerSilTint = "#FFFFFF"
    jump AppearanceCreator

label DoneAppearanceCreator:
    hide screen ON_AppearanceCreator
    hide screen ON_AppearanceCreatorShowSample
    return


label backToMenu:
