
# Function and transforms for the random cloud gfx on the corners
init python:
    import random
    def getRandomCornerDeco():
        if random.randint(0, 100) > 50:
            return "None"
        else:
            return "gui/enemycardcorner" + str(random.randint(0, 9)) + ".png"

transform CardTopLeft:
    ypos -50
    xpos -50

transform CardBottomLeft:
    xpos -50
    yalign 1.0
    ypos 450
    yzoom -1.0

transform CardTopRight:
    ypos -50
    xalign 1.0
    xpos 330
    xzoom -1.0

transform CardBottomRight:
    xalign 1.0
    xpos 330
    yalign 1.0
    ypos 450
    zoom -1.0



# Unified screen for any NPC (both dialogue and combat use this)
screen NPCCard(name, description, mC, seed=None):

    python:
        if seed is None:
            random.seed(name + str(mC))
        else:
            random.seed(str(seed) + str(mC))

    default topLeft = getRandomCornerDeco()
    default topRight = getRandomCornerDeco()
    default bottomLeft = getRandomCornerDeco()
    default bottomRight = getRandomCornerDeco()

    if persistent.showCardBubbles == True:
        # Display cloud gfx
        if topLeft != "None":
            add topLeft at CardTopLeft
        if topRight != "None":
            add topRight at CardTopRight
        if bottomLeft != "None":
            add bottomLeft at CardBottomLeft
        if bottomRight != "None":
            add bottomRight at CardBottomRight

    # Backdrop img
    add "gui/enemycard.png" xalign 0.5 ypos 0

    # NPC name at top
    fixed:
        xsize 324
        xalign 0.5
        ypos 2
        use ON_TextButtonBackgroundNoClouds(name, seed=seed)

    # Scrollbox with description text
    $ theMonID = "comScroll " + str(mC)
    fixed:
        xalign 0.5
        ypos 95
        xsize 330
        ysize 350

        viewport id theMonID:
            #scrollbars "vertical"
            mousewheel True
            draggable True
            side_yfill True
            vbox:
                xalign 0.5
                text description size 23
        vbar value YScrollValue(theMonID) xpos 330 ysize 350-16 yoffset 8 unscrollable "hide"




# EnemyCard for combat - uses NPCCard
screen EnemyCard(mC, mon, xMonPos,yMonpos):
    $ picCheck = 0
    python:
        try:
            if mon.ImageSets[mon.currentSet].ImageSet[0].name != "" and  mon.ImageSets[mon.currentSet].ImageSet[0].name != "None":
                picCheck = 1
        except:
            pass

    if picCheck == 0 or persistent.showCharacterImages == False:

        fixed:
            xalign 0.5 +xMonPos*1.25
            #xpos
            yalign yMonpos + 0.34
            xsize 378
            ysize 540

            use NPCCard(mon.name, mon.description, mC)

            if targeting == 0:
                use stanceList(mon, 1.0, mC)

            else:
                if stanceBreaking == 0:
                    $ canUse = skillIsUsableForTarget(combatChoice, mon)
                    fixed: ##istargeting
                        xalign 0.5
                        yalign 1.0
                        xsize 324
                        ysize 81
                        use ON_TextButton(text="Target", action=[SensitiveIf(canUse), SetVariable ("target", mC), Jump("combatEnemies")])

                else:
                    use stanceList(mon, 1.0, mC)
            use StatusBar(mon)

    else:
        #if has picture
        $ bodyX = 0
        $ bodyY = 0
        for layers in mon.ImageSets[mon.currentSet].ImageSet:
            if layers.currentImage == 0 and len(layers.Images) >= 1 and layers.AlwaysOn == 1:
                $ layers.currentImage = 1

            if layers.Overlay != "No" and layers.Overlay != "":
                if len(layers.Images) >= 1 and layers.currentImage == 0:
                        $ overlaying = getFromName(settingToImage, mon.ImageSets[mon.currentSet].ImageSet)
                        $ layers.currentImage = getFromName(mon.ImageSets[mon.currentSet].ImageSet[overlaying].Images[mon.ImageSets[mon.currentSet].ImageSet[overlaying].currentImage].name, layers.Images)
                        $ layers.overlayOn = 1
            if layers.TheBody == 1:
                $ bodyX = layers.setXalign
                $ bodyY = layers.setYalign
        #fixed:
            #xalign 0.5
            #yalign yMonpos

            #ypos bodyY
            #xpos bodyX + xMonPos

        # TODO: remove debug sout
        #$ monsterToolTip = mon.name
        $ monsterMovesWithPrio = getMonsterKnownMovesWithPrio(mon)
        $ monsterKnownBadMoves = getMonsterKnownBadMoveNames(mon)
        $ monsterToolTip = mon.name + "\n{" + str(monsterMovesWithPrio) + "\nbad: [" + str(monsterKnownBadMoves)
        if target == -1:
            imagebutton:
                hovered SetVariable("cmenu_tooltip", monsterToolTip)
                unhovered SetVariable("cmenu_tooltip", "")
                idle "blankButton.png"
                hover "blankButton.png"
                insensitive "blankButton.png"
                xalign 0.5
                yalign -0.3
                xsize 235
                ysize 300
                action SetVariable("cmenu_tooltip", ""), renpy.curry(renpy.end_interaction)(True)
                at characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)
                #yalign mon.pictures[mon.currentPicture].setYalign
                #at CharacterZoom
        for layers in mon.ImageSets[mon.currentSet].ImageSet:
            $ showimage = 1

            if layers.overlayOn == 0 and layers.Overlay != "No" and layers.Overlay != "":
                $ showimage = 0
            if layers.player == "Yes":
               if PlayerDisplay == "Silhouette":
                    $ showimage = 0
            elif layers.player == "Silhouette":
                if PlayerDisplay == "Body":
                    $ showimage = 0

            if layers.currentImage > 0 and showimage == 1 and layers.IsScene == 0:
                if layers.animating == "Animation":
                    $ imageShown = "animatingLayer"
                elif layers.animating == "Animation2":
                    $ imageShown = "animatingLayer2"
                elif layers.animating == "Animation3":
                    $ imageShown = "animatingLayer3"
                else:
                    $ imageShown = layers.Images[layers.currentImage].file

                $ transformsList = [characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)]
                if layers.player == "Yes" or layers.player == "Silhouette":
                    if PlayerDisplay == "Body":
                        $ transformsList = [characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos), CharacterBrightness, CharacterColor, CharacterOpacity, CharacterTint, CharacterSaturation]
                    else:
                        $ transformsList = [characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos), CharacterSilBrightness, CharacterSilColor, CharacterSilOpacity, CharacterSilTint,  CharacterSilSaturation]

                if GlobalMotion != "" or layers.motion != "":
                    if GlobalMotion == "Bounce" or layers.motion == "Bounce":
                        $ transformsList.append(Bounce)
                    elif GlobalMotion == "BounceSlow" or layers.motion == "BounceSlow":
                        $ transformsList.append(BounceSlow)
                    elif GlobalMotion == "BounceFast" or layers.motion == "BounceFast":
                        $ transformsList.append(BounceFast)
                    elif GlobalMotion == "BounceOnce" or layers.motion == "BounceOnce":
                        $ transformsList.append(BounceOnce)
                    elif GlobalMotion == "BounceCustom" or layers.motion == "BounceCustom":
                        $ transformsList.append(BounceCustom)
                    elif GlobalMotion == "Sway" or layers.motion == "Sway":
                        $ transformsList.append(Sway)
                    elif GlobalMotion == "SwaySlow" or layers.motion == "SwaySlow":
                        $ transformsList.append(SwaySlow)
                    elif GlobalMotion == "SwayFast" or layers.motion == "SwayFast":
                        $ transformsList.append(SwayFast)
                    elif GlobalMotion == "SwayOnce" or layers.motion == "SwayOnce":
                        $ transformsList.append(SwayOnce)
                    elif GlobalMotion == "SwayCustom" or layers.motion == "SwayCustom":
                        $ transformsList.append(SwayCustom)
                    elif GlobalMotion == "Pump" or layers.motion == "Pump":
                        $ transformsList.append(Pump)
                    elif GlobalMotion == "PumpSlow" or layers.motion == "PumpSlow":
                        $ transformsList.append(PumpSlow)
                    elif GlobalMotion == "PumpFast" or layers.motion == "PumpFast":
                        $ transformsList.append(PumpFast)
                    elif GlobalMotion == "PumpCustom" or layers.motion == "PumpCustom":
                        $ transformsList.append(PumpCustom)
                    elif GlobalMotion == "Ride" or layers.motion == "Ride":
                        $ transformsList.append(Ride)
                    elif GlobalMotion == "RideSlow" or layers.motion == "RideSlow":
                        $ transformsList.append(RideSlow)
                    elif GlobalMotion == "RideFast" or layers.motion == "RideFast":
                        $ transformsList.append(RideFast)
                    elif GlobalMotion == "RideCustom" or layers.motion == "RideCustom":
                        $ transformsList.append(RideCustom)
                    elif GlobalMotion == "Vibrate" or layers.motion == "Vibrate":
                        $ transformsList.append(Vibrate)
                    elif GlobalMotion == "VibrateCustom" or layers.motion == "VibrateCustom":
                        $ transformsList.append(VibrateCustom)
                    elif GlobalMotion == "Realign" or layers.motion == "Realign":
                        $ transformsList.append(Realign)
                    #$ transformsList.append(shakeTest)

                imagebutton:
                    idle imageShown
                    hover imageShown
                    insensitive imageShown
                    if layers.TheBody == 0:
                        xalign 0.5 + layers.setXalign
                        ypos layers.setYalign
                    else:
                        xalign 0.5
                    if len(transformsList) > 0:
                        at transformsList
        for layers in mon.ImageSets[mon.currentSet].ImageSet:
            if layers.IsScene == 1:
                if layers.currentImage > 0:
                    $ showimage = 1
                    if layers.overlayOn == 0 and layers.Overlay != "No" and layers.Overlay != "":
                        $ showimage = 0
                    if layers.player == "Yes":
                       if PlayerDisplay == "Silhouette":
                            $ showimage = 0
                    elif layers.player == "Silhouette":
                        if PlayerDisplay == "Body":
                            $ showimage = 0
                    if showimage == 1:
                        if layers.animating == "Animation":
                            $ imageShown = "animatingLayer"
                        elif layers.animating == "Animation2":
                            $ imageShown = "animatingLayer2"
                        elif layers.animating == "Animation3":
                            $ imageShown = "animatingLayer3"
                        else:
                            $ imageShown = layers.Images[layers.currentImage].file

                        $ transformsList = [truecenter]
                        if layers.player == "Yes" or layers.player == "Silhouette":
                            if PlayerDisplay == "Body":
                                $ transformsList = [truecenter, CharacterBrightness, CharacterColor, CharacterOpacity, CharacterTint, CharacterSaturation]
                            else:
                                $ transformsList = [truecenter, CharacterSilBrightness, CharacterSilColor, CharacterSilOpacity, CharacterSilTint,  CharacterSilSaturation]

                        if GlobalMotion != "" or layers.motion != "":
                            if GlobalMotion == "Bounce" or layers.motion == "Bounce":
                                $ transformsList.append(Bounce)
                            elif GlobalMotion == "BounceSlow" or layers.motion == "BounceSlow":
                                $ transformsList.append(BounceSlow)
                            elif GlobalMotion == "BounceFast" or layers.motion == "BounceFast":
                                $ transformsList.append(BounceFast)
                            elif GlobalMotion == "BounceOnce" or layers.motion == "BounceOnce":
                                $ transformsList.append(BounceOnce)
                            elif GlobalMotion == "BounceCustom" or layers.motion == "BounceCustom":
                                $ transformsList.append(BounceCustom)
                            elif GlobalMotion == "Sway" or layers.motion == "Sway":
                                $ transformsList.append(Sway)
                            elif GlobalMotion == "SwaySlow" or layers.motion == "SwaySlow":
                                $ transformsList.append(SwaySlow)
                            elif GlobalMotion == "SwayFast" or layers.motion == "SwayFast":
                                $ transformsList.append(SwayFast)
                            elif GlobalMotion == "SwayOnce" or layers.motion == "SwayOnce":
                                $ transformsList.append(SwayOnce)
                            elif GlobalMotion == "SwayCustom" or layers.motion == "SwayCustom":
                                $ transformsList.append(SwayCustom)
                            elif GlobalMotion == "Pump" or layers.motion == "Pump":
                                $ transformsList.append(Pump)
                            elif GlobalMotion == "PumpSlow" or layers.motion == "PumpSlow":
                                $ transformsList.append(PumpSlow)
                            elif GlobalMotion == "PumpFast" or layers.motion == "PumpFast":
                                $ transformsList.append(PumpFast)
                            elif GlobalMotion == "PumpCustom" or layers.motion == "PumpCustom":
                                $ transformsList.append(PumpCustom)
                            elif GlobalMotion == "Ride" or layers.motion == "Ride":
                                $ transformsList.append(Ride)
                            elif GlobalMotion == "RideSlow" or layers.motion == "RideSlow":
                                $ transformsList.append(RideSlow)
                            elif GlobalMotion == "RideFast" or layers.motion == "RideFast":
                                $ transformsList.append(RideFast)
                            elif GlobalMotion == "RideCustom" or layers.motion == "RideCustom":
                                $ transformsList.append(RideCustom)
                            elif GlobalMotion == "Vibrate" or layers.motion == "Vibrate":
                                $ transformsList.append(Vibrate)
                            elif GlobalMotion == "VibrateCustom" or layers.motion == "VibrateCustom":
                                $ transformsList.append(VibrateCustom)
                            elif GlobalMotion == "Realign" or layers.motion == "Realign":
                                $ transformsList.append(Realign)
                            #$ transformsList.append(shakeTest)
                        imagebutton:
                            idle imageShown
                            hover imageShown
                            insensitive imageShown
                            xpos layers.setXalign + layers.Images[layers.currentImage].setXalign
                            ypos layers.setYalign + layers.Images[layers.currentImage].setYalign
                            at transformsList

        if _windows_hidden == False:
            fixed:
                #xalign 0.5
                yalign 0.16
                ypos 160
                xpos xMonPos
                fixed:
                    xalign 0.5
                    xsize 500
                    ysize 1100

                    $ layerY = 0
                    if ((mC == 1 or mC == 2) and len(monsterEncounter) > 10):
                        $ layerY += yMonpos*1.15
                    if mC > 8 and len(monsterEncounter) > 10:
                        $ layerY = yMonpos*1.15
                    elif mC > 6 and len(monsterEncounter) <= 10:
                        $ layerY = yMonpos*1.15
                    elif (mC > 4 and len(monsterEncounter) > 10):
                        $ layerY = yMonpos*0.4
                    elif (mC > 2 and len(monsterEncounter) <= 10):
                        $ layerY = yMonpos*0.4

                    if targeting == 1 and stanceBreaking == 0:
                        $ canUse = skillIsUsableForTarget(combatChoice, mon)

                        fixed: ##istargeting
                            xalign 0.5
                            yalign 0.605 + layerY
                            xsize 324
                            ysize 81
                            use ON_TextButton(text="Target", action=[SensitiveIf(canUse), SetVariable ("target", mC), Jump("combatEnemies")])
                    else:
                        if mon.combatStance[0].Stance != "None":
                            use stanceList(mon, 0.605+ layerY, mC)

                    $ layerYmul = 1
                    if mC > 8 and len(monsterEncounter) > 10:
                        $ layerYmul = 0.75
                    elif mC > 6 and len(monsterEncounter) <= 10:
                        $ layerYmul = 0.75

                    use StatusBar(mon, yalign=0.550+ layerY*layerYmul)





# StanceList - displayed in each EnemyCard
screen stanceList(mon, yalign, mC):

    # pushing away implemented in combat menu
    #$ canBreakFree = targeting != 0 and stanceBreaking != 0 and mon.combatStance[0].Stance != "None"

    fixed: ##istargeting
        xalign 0.5
        yalign yalign # 0.885 or 0.075
        xsize 324
        ysize 81
        #if canBreakFree:
        #    use ON_TextButton(action=[SetVariable("target", mC), Jump("combatPushAway")])
        fixed: ##istargeting
            xalign 0.5
            yalign 0.98
            xsize 324
            ysize 81
            use ON_TextButtonBackground(seed=mon.name + str(mC))

        if mon.combatStance[0].Stance == "None":
            text "":
                xalign 0.5
                yalign 0.5
        else:
            $ stances = ""
            for i, monStance in enumerate(mon.combatStance):

                if i > 0:
                    $ stances += ",  "

                $ stances += monStance.Stance

            text stances:
                xalign 0.5
                yalign 0.5

                if len(mon.combatStance) == 2:
                    size 20
                elif len(mon.combatStance) > 2:
                    size 16



# StatusBar is a wrapper for StatusIcons that just includes an hbox or vbox
# Will automatically use a vbox positioned over the health display if char == player
# Otherwise, will just add an hbox to be positioned in the EnemyCard
screen StatusBar(char, yalign=1.06, menuCall=0):
    zorder 201
    $ statusPerk = 0
    for perk in char.perks:
        $ p = 0
        for x in perk.PerkType:
            if perk.PerkType[p] == "StatusIcon":
                $ statusPerk = 1

    if char.statusEffects.hasStatusEffect() == True or statusPerk == 1 :
        if menuCall==1:
            frame:
                xpos 615
                xanchor 0.5
                ycenter 140
                hbox:
                    use StatusIcons(char)
        elif (char == player):
            frame:
                xpos 1372
                xanchor 0.5
                ycenter 784
                hbox:
                    use StatusIcons(char)
        else:
            frame:
                xalign 0.5
                yalign yalign
                hbox:
                    use StatusIcons(char)


screen statusEffectIcon(statusText, Icon):
    imagebutton:
        if renpy.variant("touch"):
            if cmenu_tooltip == statusText:
                action SetVariable("cmenu_tooltip", "")
            else:
                action SetVariable("cmenu_tooltip", statusText )
        else:
            hovered SetVariable("cmenu_tooltip", statusText )
            unhovered SetVariable("cmenu_tooltip", "")
            action SetVariable("cmenu_tooltip", "")
        idle Icon
        insensitive Icon
        hover Icon
        at statusIconZoom

# StatusIcons just adds the whole list of status icons with no positioning/containers. Used by StatusBar
# This is just so we don't have the same massive list multiple places in the code
screen StatusIcons(char):
    if char.statusEffects.defend.duration > 0:
        if char.statusEffects.defend.potency == 0:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by 75%, increases evade stat by 50%, and increase int, will, power, and tech stat checks by +5.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon)
        elif char.statusEffects.defend.potency == 1:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by 50% and increases evade stat by 50%, and increase int, will, power, and tech stat checks by +3.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon2)
        else:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by 25% and increases evade stat by 50%, and increase int, will, power, and tech stat checks by +1.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon3)
    if char.statusEffects.surrender.duration > 0:
        use statusEffectIcon("You gave up and can no longer act!", surrenderIcon)
    if char.statusEffects.charmed.duration > 0:
        use statusEffectIcon("Charmed! Stops attempts from escaping stances and running, weakens attempts to break restraints, lowers escape and stance removal skills chance of working by half, and increases the difficulty of temptation checks by 1!\nLasts " + str(char.statusEffects.charmed.duration) + " more turns.", charmIcon)
    if char.statusEffects.restrained.duration > 0:
        use statusEffectIcon("Restrained! Lasts until escaped!", restrainedIcon)
    if char.statusEffects.aphrodisiac.duration > 0:
        use statusEffectIcon("Affected by an aphrodisiac!\nPotency: " + str( int(math.floor(char.statusEffects.aphrodisiac.potency))) + "!\nLasts " + str(char.statusEffects.aphrodisiac.duration) + " more turns.", poisonIcon)
    if char.statusEffects.stunned.duration > 0:
        use statusEffectIcon("Stunned and unable to act!\nLasts " + str(char.statusEffects.stunned.duration) + " more turns.", stunnedIcon)
    if char.statusEffects.sleep.duration > 0:
        if char.species == "Player":
            if char.statusEffects.sleep.potency >= 1 :
                use statusEffectIcon("You're losing " + str(int(math.floor(char.statusEffects.sleep.potency))) + " energy every turn, and will fall asleep at 0 energy.\nLasts " + str(int(math.floor(char.statusEffects.sleep.duration))) + " more turns.\nYou regain 50% of max energy if you fall asleep, but lose 25% of spirit on orgasm if you're sleeping when you cum.", sleepIcon0)
            else:
                use statusEffectIcon("Fast asleep...", sleepIcon3)
        else:
            if char.statusEffects.sleep.potency >= 1 :
                use statusEffectIcon("Is losing " + str(int(math.floor(char.statusEffects.sleep.potency))) + " energy every turn, and will fall asleep at 0 energy.\nLasts " + str(int(math.floor(char.statusEffects.sleep.duration))) + " more turns.\n" + str(char.stats.ep) + "/" + str(char.stats.max_true_ep) +" energy remaining.", sleepIcon0)
            else:
                use statusEffectIcon("Fast asleep...", sleepIcon3)


    if char.statusEffects.trance.duration > 0:
        if char.statusEffects.trance.potency == 1:
            use statusEffectIcon("Drifting into trance...", tranceIcon10)
        elif char.statusEffects.trance.potency == 2:
            use statusEffectIcon("Drifting into trance...", tranceIcon9)
        elif char.statusEffects.trance.potency == 3:
            use statusEffectIcon("Falling into trance...", tranceIcon8)
        elif char.statusEffects.trance.potency == 4:
            use statusEffectIcon("Falling into trance...", tranceIcon7)
        elif char.statusEffects.trance.potency == 5:
            use statusEffectIcon("Falling into trance...", tranceIcon6)
        elif char.statusEffects.trance.potency == 6:
            use statusEffectIcon("Falling into trance...", tranceIcon5)
        elif char.statusEffects.trance.potency == 7:
            use statusEffectIcon("Falling into trance...", tranceIcon4)
        elif char.statusEffects.trance.potency == 8:
            use statusEffectIcon("Falling into deep trance...", tranceIcon3)
        elif char.statusEffects.trance.potency == 9:
            use statusEffectIcon("Falling into deep trance...", tranceIcon2)
        elif char.statusEffects.trance.potency == 10:
            use statusEffectIcon("Falling into deep trance...", tranceIcon1)
        else:
            use statusEffectIcon("Completely entranced, may not be able to act...", tranceIcon0)

    if char.statusEffects.paralysis.duration > 0:
        $ Paraboost = getParalysisBoost(player)
        $ initLoss = int(math.floor(char.statusEffects.paralysis.potency*5))

        if char.statusEffects.paralysis.potency == 1:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon1)
        elif char.statusEffects.paralysis.potency == 2:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon2)
        elif char.statusEffects.paralysis.potency == 3:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon3)
        elif char.statusEffects.paralysis.potency == 4:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon4)
        elif char.statusEffects.paralysis.potency == 5:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon5)
        elif char.statusEffects.paralysis.potency == 6:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon6)
        elif char.statusEffects.paralysis.potency == 7:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon7)
        elif char.statusEffects.paralysis.potency == 8:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon8)
        elif char.statusEffects.paralysis.potency == 9:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon9)
        else:
            use statusEffectIcon("Paralysis lowers your initiative by " + str(initLoss) + ", and gives you a " + str(Paraboost) +"% chance to be stunned!\nEffects increase drastically with every stack, but lowers every turn you've been stunned by it. Lasts until removed with items, or dissipates slowly out of combat.", paralysisIcon10)


    for each in char.statusEffects.tempAtk:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases arousal dealt by " + str(each.potency) + "%!\nLasts " + str(each.duration) + " more turns.", atkUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases arousal dealt by " + str(each.potency*-1) + "%!\nLasts " + str(each.duration) + " more turns.", atkDownIcon)
    for each in char.statusEffects.tempDefence:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases arousal taken by " + str(each.potency) + "%!\nLasts " + str(each.duration) + " more turns.", defUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases arousal taken by " + str(each.potency*-1) + "%!\nLasts " + str(each.duration) + " more turns.", defDownIcon)
    for each in char.statusEffects.tempPower:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Power by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", powUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Power by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", powDownIcon)
    for each in char.statusEffects.tempTech:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Technique by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", techUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Technique by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", techDownIcon)
    for each in char.statusEffects.tempWillpower:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Willpower by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", willUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Willpower by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", willDownIcon)
    for each in char.statusEffects.tempInt:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Intelligence by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", intUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Intelligence by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", intDownIcon)
    for each in char.statusEffects.tempAllure:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Allure by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", allureUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Allure by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", allureDownIcon)
    for each in char.statusEffects.tempLuck:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases Luck by " + str(each.potency) + "!\nLasts " + str(each.duration) + " more turns.", luckUpIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases Luck by " + str(each.potency*-1) + "!\nLasts " + str(each.duration) + " more turns.", luckDownIcon)

    for each in char.statusEffects.tempCrit:
        if each.duration > 0:
            if each.potency > 0:
                use statusEffectIcon("Source: " + each.skillText + "\nIncreases crit chance by " + str(each.potency) + "%!\nLasts " + str(each.duration) + " more turns.", critIcon)
            else:
                use statusEffectIcon("Source: " + each.skillText + "\nDecreases crit chance by " + str(each.potency*-1) + "%!\nLasts " + str(each.duration) + " more turns.", critIcon)


    for perk in char.perks:
        $ p = 0
        for x in perk.PerkType:
            if perk.PerkType[p] == "StatusIcon":
                $ timeType = ""
                for y in perk.PerkType:
                    if y == "TimeDuration" or y == "TurnDuration":
                        $ timeType = y
                $ perkDescrip = perkDurationDisplay( perk.description, perk.duration, timeType)
                use statusEffectIcon("Source: " + perk.name + "\n" + perkDescrip, perk.EffectPower[p])

            $ p += 1
