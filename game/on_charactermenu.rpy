
screen ON_UseItemConfirm:
    if equippingItem == 1:
        if player.inventory.items[inventoryETarget].itemType == "Rune" or player.inventory.items[inventoryETarget].itemType == "Accessory":
            $ display = "Equip " + player.inventory.items[inventoryETarget].name + "?"
            if player.inventory.items[inventoryETarget].itemType == "Rune":
                $ display += " Where?"
            frame:
                xpadding theXpadding
                ypadding theYpadding
                xpos 190
                yalign 0.5
                xminimum 825
                xmaximum 825
                ymaximum 202
                yminimum 202
                text "[display]":
                    xalign 0.5
                    yalign 0.2
                if player.inventory.items[inventoryETarget].itemType == "Rune":
                    textbutton "Slot 1":
                        xalign 0.125
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0), SetVariable ("TargetingEquipSlot", 1), Jump("EquipItem")]
                    textbutton "Slot 2":
                        xalign 0.375
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0), SetVariable ("TargetingEquipSlot", 2), Jump("EquipItem")]
                    textbutton "Slot 3":
                        xalign 0.625
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0), SetVariable ("TargetingEquipSlot", 3), Jump("EquipItem")]
                    textbutton "Back":
                        xalign 0.875
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0)]

                else:
                    textbutton "Yes":
                        xalign 0.25
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0),  SetVariable ("TargetingEquipSlot", 4), Jump("EquipItem")]
                    textbutton "No":
                        xalign 0.75
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("equippingItem", 0)]

    if unequippingItem >= 1:
        $ TargetEquippedItem =  Item("Empty", "Rune", "0")
        if unequippingItem == 1:
            $ TargetEquippedItem = player.inventory.RuneSlotOne
        if unequippingItem == 2:
            $ TargetEquippedItem = player.inventory.RuneSlotTwo
        if unequippingItem == 3:
            $ TargetEquippedItem = player.inventory.RuneSlotThree
        if unequippingItem == 4:
            $ TargetEquippedItem = player.inventory.AccessorySlot

        $ display = "Unequip " + TargetEquippedItem.name + "?"

        frame:
            xpadding theXpadding
            ypadding theYpadding
            xpos 300
            yalign 0.5
            xminimum 525
            xmaximum 525
            ymaximum 187
            yminimum 187
            text "[display]":
                xalign 0.5
                yalign 0.2
            textbutton "Yes":
                xalign 0.25
                yalign 0.95
                action [SelectedIf(False), SetVariable ("RemovingEquipment", unequippingItem),  SetVariable ("TargetingEquipSlot", 0), SetVariable ("unequippingItem", 0), Jump("EquipItem")]
            textbutton "No":
                xalign 0.75
                yalign 0.95
                action [SelectedIf(False), SetVariable ("unequippingItem", 0)]

    if useItem == 1:
        if player.inventory.items[inventoryTarget].itemType == "Consumable" or player.inventory.items[inventoryTarget].itemType == "DissonantConsumable" or player.inventory.items[inventoryTarget].itemType == "NotCombatConsumable":
            $ display = "Use a " + player.inventory.items[inventoryTarget].name + "?"
            frame:
                xpadding theXpadding
                ypadding theYpadding
                xpos 300
                yalign 0.5
                xminimum 525
                xmaximum 525
                ymaximum 187
                yminimum 187
                text "[display]":
                    xalign 0.5
                    yalign 0.2
                textbutton "Yes":
                    xalign 0.25
                    yalign 0.95
                    action [SelectedIf(False), SetVariable ("useItem", 0), Jump("useInventoryItem")]
                textbutton "No":
                    xalign 0.75
                    yalign 0.95
                    action [SelectedIf(False), SetVariable ("useItem", 0)]

    if useSkill == 1:
        if(player.skillList[skillTarget].skillType == "Healing" or player.skillList[skillTarget].skillType == "HealingEP" or player.skillList[skillTarget].skillType == "HealingSP" or player.skillList[skillTarget].skillType == "StatusHeal"):
            if player.skillList[skillTarget].statusOutcome != "CombatOnly":
                $ display = "Use " + player.skillList[skillTarget].name + "?"
                frame:
                    xpadding theXpadding
                    ypadding theYpadding
                    xpos 300
                    yalign 0.5
                    xminimum 525
                    xmaximum 525
                    ymaximum 187
                    yminimum 187
                    text "[display]":
                        xalign 0.5
                        yalign 0.2
                    textbutton "Yes":
                        xalign 0.25
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("useSkill", 0), Jump("useSkillFromMenu")]
                    textbutton "No":
                        xalign 0.75
                        yalign 0.95
                        action [SelectedIf(False), SetVariable ("useSkill", 0)]





screen ON_EquipSlot(itemSlot, slotName, slotID):
    hbox:
        textbutton slotName:
            text_color "#fff"
            #action [SetVariable ("unequippingItem", 0)]
            text_size on_listTextSize
            ysize on_listEntryHeight

        #text " " ysize on_listEntryHeight

        if itemSlot.name == "Empty":
            textbutton "Empty":
                text_color "#fff"
                text_size on_listTextSize
                ysize on_listEntryHeight

        else:
            textbutton itemSlot.name:
                hovered SetScreenVariable("characterMenuTooltip", itemSlot.descrips + " Value: " + str(itemSlot.cost) + " eros.")
                if renpy.variant("touch"):
                    unhovered SetScreenVariable("characterMenuTooltip", itemSlot.descrips + " Value: " + str(itemSlot.cost) + " eros.")
                else:
                    unhovered SetScreenVariable("characterMenuTooltip", "")
                action [SelectedIf(False), SensitiveIf(InventoryAvailable), SetVariable ("unequippingItem", slotID)]
                text_insensitive_color "#fff"
                text_size on_listTextSize
                ysize on_listEntryHeight




screen ON_SingleFetishDisplay(name, fetish, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight
        $ value = fetish.Level
        if name == "Sex:":
            $ tooltipDisplay = "How much you love sex and your sexual fascination with pussies.\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with pussies and sex. You have a hard time focusing on anything else, and can't even think of resisting temptations of fucking..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for pussies and sex. Your thoughts are often drifting towards them, leaving you achingly horny..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for pussies and sex. Just thinking about it gets you a little aroused..."
            elif value >= 25:
                $ tooltipDisplay += "You have a fetish for pussies and sex."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for pussies and sex."
        elif name == "Oral:":
            $ tooltipDisplay = "How much you love getting blowjobs.\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with blowjobs. You're having a hard time not fantasizing about a woman sucking you off right now, and couldn't possibly resist the temptation if the temptation were to arise..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for women giving you blowjobs. Your thoughts often fantasizing about a warm pair of lips teasing your cock, leaving you eager to get sucked dry..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for women giving you blowjobs. Just thinking a warm mouth wrapped around your cock gets you hard..."
            elif value >= 25:
                $ tooltipDisplay += "You have a fetish for blowjobs."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for oral."
        elif name == "Breasts:":
            $ tooltipDisplay = "How much you love breasts. Big or small!\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with tits. You can't help but fantasize about women shaking their breasts for you, seducing you into a horny mess, and you definitely can't stop yourself from staring at a woman's cleavage..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for women's soft tits. You have a hard time not thinking about swaying breasts, bouncing and jiggling, their deep cleavage tempting you to give in..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for women's soft tits. Just thinking about a girl's bouncy chest, or looking at a woman's deep cleavage gets you hard..."
            elif value >= 25:
                $ tooltipDisplay += "You have a fetish for tits."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for tits."
        elif name == "Ass:":
            $ tooltipDisplay = "How much you love butts!\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with curvy asses. You're can't help but fantasize on occasion about woman shaking her ass for you, and you definitely can't stop yourself from watching a woman walk while her hips sway with her step, your thoughts and resistance draining down into your cock..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for curvy asses. You have a hard time stopping yourself from thinking about a nice ass, and pulling your eyes away from a woman's swaying hips as she walks, each swing making your cock twitch..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for curvy asses. Just thinking about a nice ass, or watching a woman's hips swing as she walks gets you hard..."
            elif value >= 25:
                $ tooltipDisplay += "You have an ass fetish."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for butts."
        elif name == "Kissing:":
            $ tooltipDisplay = "How much you love to make out! Probably lipstick too...\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with kissing and plump lips. You're can't help but fantasize about getting covered in lipstick marks, thoughtlessly making out, letting a woman kiss you into pleasure drunk stupor. Even just getting a kiss blown your way could make you fall to temptation..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for kissing and plump lips. Fantasies of making out and getting coated in lipstick marks flit through your thoughts, and a single smooch could probably get you wrapped around a womans finger, even just looking at her soft lips would make your cock ache..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for kissing and plump lips. Just thinking about kissing, or just looking a woman's soft lips gets you hard..."
            elif value >= 25:
                $ tooltipDisplay += "You have a kissing fetish."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for kissing."
        elif name == "Legs:":
            $ tooltipDisplay = "How much you love legs and thighs!\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with legs and thighs. You're can't help but fantasize on occasion about humping women's soft legs, thinking about teasing thigh highs and sexy stockings, leaving you staring at their tempting thighs unconsciously, making you space out and wonderfully vulnerable..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for legs and thighs. Your thoughts drift to fantasizing about women's long, seductive legs, leaving you aching to rub your cock against them, tempting you to let your eyes linger on their smooth skin..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for legs and thighs. Just thinking about a womens long legs and firm thighs makes your cock twitch, tempting you to let your eyes linger on their smooth skin..."
            elif value >= 25:
                $ tooltipDisplay += "You have a fetish for legs and thighs."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for legs or thighs."
        elif name == "Feet:":
            $ tooltipDisplay = "How much you love feet!\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with feet. You're can't help but fantasize on occasion about getting stepped on by a woman, worshipping her foot, just hearing a woman walk in heels makes your cock twitch, and you staring at women's feet unconsciously, leaving you spacing out and vulnerable..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish for feet. Your thoughts drift to worshipping women feet on occasion, aching for them to tease your cock, and your eyes linger on women's feet unconsciously..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for feet. Just thinking about worshipping a woman's foot gets you hard, and your eyes dart down to women's feet unconsciously..."
            elif value >= 25:
                $ tooltipDisplay += "You have a foot fetish."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for feet."
        elif name == "Monstrous:":
            $ tooltipDisplay = "How much you love tails, wings, fangs, tentacles, slimy bodies, tail pussies, and more!\n\nVerdict: "
            if value >= 100:
                $ tooltipDisplay += "You are completely obsessed with the monstrous aspects of monster girls. You're can't help but fantasize about any and every kind of monster girl and the things they could do to you, and it's very noticeable when you stare at a girl's tail pussy or fluffy wings, leaving you wonderfully vulnerable..."
            elif value >= 75:
                $ tooltipDisplay += "You have a very strong fetish the monstrous aspects of monster girls. Your thoughts often drifting to fantasies of monster girls teasing you with their tails, wings, and unique orifices. You often stare at monster girls spacing out with naughty thoughts, leaving your atttration rather apparent..."
            elif value >= 50:
                $ tooltipDisplay += "You have a strong fetish for monstrous body bits. Just thinking about a tail teasing your dick gets you hard, and your eyes linger on monster girls longer than they should..."
            elif value >= 25:
                $ tooltipDisplay += "You have a fetish for monstrous body parts."
            else:
                $ tooltipDisplay += "You have yet to acquire a fetish for monster girls more monstrous parts."
        else:
            $ tooltipDisplay = "This is a custom fetish."


        $ value = "Lvl " + str(value) + " / " + str(fetish.LevelPerm)

        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            if tooltipDisplay != "":
                action [ SetVariable("characterMenuTooltip", tooltipDisplay)] #make hoverable
                hovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                if renpy.variant("touch"):
                    unhovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                else:
                    unhovered SetScreenVariable("characterMenuTooltip", "")

            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleDisplay(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight
        if duration >= 0:
            $ tooltipDisplay = perkDurationDisplay( tooltipDisplay, duration, timeType)
        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            if tooltipDisplay != "":
                action [ SetVariable("characterMenuTooltip", tooltipDisplay)] #make hoverable
                hovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                if renpy.variant("touch"):
                    unhovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                else:
                    unhovered SetScreenVariable("characterMenuTooltip", "")
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleStatDisplay(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight

        if "Virility: ":
            $ Virility = getVirility(player)

        if "Initiative: ":
            $ InititiveBonus = getInitStats(player)

        if "Reduction: ":
            $ damageReduction = (getDamageReduction(player, 100) -100)*-1

        if "Evade: ":
            $ InStanceEvade = getBaseEvade(player, 10, 1)
            $ OutOfStanceEvade = getBaseEvade(player, 0, 1)
        if "Acc: ":
            $ AccuracyBonus = getBaseAccuracy(player, 0)
            $ InStanceAccuracyBonus = getBaseAccuracy(player, 10)

        if "Effect Duration: ":
            $ statusDuration = statusEffectBaseDuration(player)
        if "Effect Chance: ":
            $ statusAccuracyBonus = getStatusEffectBaseAccuracy(player)
        if "Status Res: ":
            $ statusEvadeBonus = getStatusEffectEvade(player)

        if "Allure Bonus:  ":
            $ allureFlatScaling = 0.10
            python:
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "BaselineAllureFlatBuff":
                            allureFlatScaling += perk.EffectPower[p]*0.01
                        p += 1
            $ flatAllureBonus = (player.stats.Allure-5)*allureFlatScaling
        if "Allure Bonus%:  ":
            $ allureFlatPercentBoost = 0
            python:
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):

                        if perk.PerkType[p] == "BaselineAllureFlatPercentBoost":
                            allureFlatPercentBoost += perk.EffectPower[p]*0.01
                        p += 1
            $ percentAllureBonus = 100*((player.stats.Allure-5)*0.002 + allureFlatPercentBoost)


        if name == "Crit Chance: " or name == "Crit Damage: ":
            $ critChance = getCritChance(player)
            $ critDamage = getCritDamage(player)

        if name == "Crit Reduction: ":
            $ critReduction = getCritReduction(player)

        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            if tooltipDisplay != "":
                action [ SetVariable("characterMenuTooltip", tooltipDisplay)] #make hoverable
                hovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                if renpy.variant("touch"):
                    unhovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                else:
                    unhovered SetScreenVariable("characterMenuTooltip", "")
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleStatDisplayNoVar(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight
        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            if tooltipDisplay != "":
                action [ SetVariable("characterMenuTooltip", tooltipDisplay)] #make hoverable
                hovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                if renpy.variant("touch"):
                    unhovered SetScreenVariable("characterMenuTooltip", tooltipDisplay)
                else:
                    unhovered SetScreenVariable("characterMenuTooltip", "")
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleItemDisplay(item, spaceNextOne=0):
    $ invIndex =  getFromName(item.name, player.inventory.items)
    $ display = item.name

    if player.inventory.items[invIndex].NumberHeld > 1:
        $ display += " (" + str(player.inventory.items[invIndex].NumberHeld) + ")"

    $ twolayered = 0

    if spaceNextOne == 1:
        #$ twolayered += 15
        $ spaceNext = 0

    if len(display) > 28:
        $ twolayered += 24
        $ spaceNextOne = 1

    $ itemsToolTip = item.descrips + " Value: " + str(item.cost) + " eros."
    if item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable"  or item.itemType == "CombatConsumable":
        if len(item.skills) > 0:
            $ fetchSkill = getFromName(item.skills[0], SkillsDatabase)
            $ skillToCheck = copy.deepcopy(SkillsDatabase[fetchSkill])
            $ itemsToolTip = getSkillToolTip(skillToCheck, player, itemsToolTip)

    button:
        ysize on_listEntryHeight + twolayered
        hovered SetScreenVariable("characterMenuTooltip", itemsToolTip)
        if renpy.variant("touch"):
            unhovered SetScreenVariable("characterMenuTooltip", itemsToolTip)
        else:
            unhovered SetScreenVariable("characterMenuTooltip", "")

        text display:
            size on_listTextSize
            #xsize 700
            if item.itemType == "Loot" or item.itemType == "CombatConsumable":
                idle_color gui.insensitive_color
                hover_color gui.insensitive_color
                insensitive_color gui.insensitive_color
            else:
                idle_color gui.idle_color
                hover_color gui.hover_color
                insensitive_color gui.insensitive_color
        if (item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "NotCombatConsumable") and useItem == 0:
            action [SelectedIf(False), SetVariable ("useItem", 1), SetVariable("inventoryTarget", invIndex)]
        elif (item.itemType == "Rune" or item.itemType == "Accessory" and useItem == 0) and useItem == 0:
            action [SelectedIf(False), SetVariable ("equippingItem", 1), SetVariable ("inventoryETarget", invIndex) ]
        else:
            action [SelectedIf(False), NullAction()] # make hoverable

screen ON_EquipmentListDisplay:
    use ON_Scrollbox(""):
        use ON_EquipSlot(player.inventory.RuneSlotOne, "Rune Slot 1 -", 1)
        use ON_EquipSlot(player.inventory.RuneSlotTwo, "Rune Slot 2 -", 2)
        use ON_EquipSlot(player.inventory.RuneSlotThree, "Rune Slot 3 -", 3)
        use ON_EquipSlot(player.inventory.AccessorySlot, "Accessory -", 4)

screen ON_StatsListDisplay(showMainStats=False):
    $ damageBoost = 0
    use ON_Scrollbox("Stats"):

        #if showMainStats:
        use ON_SingleStatDisplayNoVar("Arousal:","[player.stats.hp]/[player.stats.max_true_hp]", color="#FB97A3", tooltipDisplay="The amount of sexual stimulation you can take! When it hits its max, you lose spirit.")
        use ON_SingleStatDisplayNoVar("Energy:", "[player.stats.ep]/[player.stats.max_true_ep]", color="#BCC9F0", tooltipDisplay="Your personal reserves of energy, or mana as some like to call it, it's used for skills and magic!")
        use ON_SingleStatDisplayNoVar("Spirit:", "[player.stats.sp]/[player.stats.max_true_sp]", tooltipDisplay="Your life energy! If this runs out, you won't be able to fight back. You lose at least one per orgasm, so really, it's just a measurement of how many times you can cum normally.")
        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5


        use ON_SingleStatDisplayNoVar("Power:", "[player.stats.Power]", tooltipDisplay="Escape restraints, 'punish' your foes, maintain or get out of sexual positions, and deal increased critical arousal! Every 5 points naturally gained increases your max arousal by 10. Boosts how much damage you do with core skills!\nYou have [powerDisplay] base power out of 100. Power skills deal [powerBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [powerPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Technique:", "[player.stats.Tech]", tooltipDisplay="Used for evading, acting faster, running away, and sexual finesse! It also helps you get out of stances and restraints, but it is not as effective as power. Boosts how much damage you do with core skills!\nYou have [techDisplay] base technique out of 100. Tech skills deal [techBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [techPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Intelligence:", "[player.stats.Int]", tooltipDisplay="Cast magic, resist some temptations, increase your chance to apply status effects, and increase the duration of your status effect! Every 5 points gained naturally increases your max energy by 10. Boosts how much damage you do with core skills!\nYou have [intDisplay] base intelligence out of 100. Intelligence skills deal [intBoost] extra arousal based on the (square root of the stat*4)-5. Said skills also get an increase of [intPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Allure:", "[player.stats.Allure]", tooltipDisplay="Seduce and charm your foes! It increases how much arousal you deal with all skills, including increased critical arousal, and boosts how much damage you do with core skills! Also increases the recoil damage your opponent takes, from sex skills for example!\nYou have [allureDisplay] base allure out of 100. Allure skills deal [allureBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [allurePerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Willpower:", "[player.stats.Willpower]", tooltipDisplay="Greatly resist temptation, status effects, and reduces how much arousal you take! Every 5 points increases your max arousal and max energy by 5.\nYou have [willDisplay] base willpower out of 100. Willpower skills deal [willBoost] extra arousal based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [willPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Luck:", "[player.stats.Luck]", tooltipDisplay="Helps a little bit across the board. Such as acting before others, getting out of restraints, running away, hitting or dodging attacks, and improves your critical chance! But best of all it helps you find more treasure!\nYou have [luckDisplay] base luck out of 100. Luck skills(?) deal [luckBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [luckPerBoost]% to their base power!")

        use ON_MoreStatsListDisplay


screen ON_MoreStatsListDisplay:
        textbutton "---More Stats---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5

        use ON_SingleStatDisplay("Core Skills Bonus", "", tooltipDisplay="Your core skills deal [flatCore] bonus arousal and a bonus of [percentCore]% to the base power of core skills!\nCore skills are based on 50% of your highest stat out of Power, Tech, Int, and Allure, plus the average of the four stats added together. Then the (square root of that times 3)-5 is your flat bonus.")
        use ON_SingleStatDisplay("Initiative: ", "[InititiveBonus]", tooltipDisplay="Initiative determines combatant turn order, with the highest acting first. All combatants add a d100 roll to their base Initiative to determine their total Initiative that turn. Turn order then proceeds from highest total Initiative to lowest.\nYou gain a +75 bonus to Initiative when attempting to use an item.\nInitiative is equal to your Tech + Int/2 + Luck/2 + possible bonuses from perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Crit Chance: ", "[critChance]%", tooltipDisplay="Your percent chance to land a critical hit when attacking.\nIt is equal to your Tech*0.10 + Luck*0.25 + 3.25 + possible bonuses from perks.")
        use ON_SingleStatDisplay("Crit Damage: ", "[critDamage]x", tooltipDisplay="Your arousal modifier when you land a critical!\nIt is equal to your (Power*0.525-2.5) +  (Allure*0.525-2.5) + 200% + possible bonuses from perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        #use ON_SingleStatDisplay("Crit Reduction: ", "[critReduction]%", tooltipDisplay="How much you reduce your opponent's chance to critted you! If it's negative, it's increasing your chance to be crit.\nIt is equal to your Luck*0.2 + perks - 1. When you would be crit and your crit chance reduction saves you 'Passion Endured' will be displayed.")
        use ON_SingleStatDisplay("Evade: ", "[OutOfStanceEvade]%/"+ "[InStanceEvade]%", tooltipDisplay="Chance to Evade attacks out of stance/Chance to evade in stance. Out of stance evade is based on tech-5(0.3% per point) + luck-5(0.15% per point), while In stance evade is based on power-5(0.3% per point) + tech-5(0.15% per point). Both are effected by any respective perks. Defending increases your total evade chance by 50%.\nFetishes, status effects, and attacker accuracy make it harder to evade.")
        use ON_SingleStatDisplay("Acc: ", "[AccuracyBonus]%/"+ "[InStanceAccuracyBonus]%", tooltipDisplay="Attack accuracy bonus out of stances/Accuracy bonus in stance. Out of stance accuracy is based on tech-5(0.3% per point) + luck-5(0.15% per point), while In stance accuracy is based on power-5(0.3% per point) + tech-5(0.15% per point) + 10. Both are effected by any respective perks and get a random roll(d100) added, that are added together to decide if the skill hits vs the targets evade.")
        use ON_SingleStatDisplay("Reduction: ", "[damageReduction]%", tooltipDisplay="Your % damage reduction to arousal, calculated from your willpower and relevant perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Effect Duration: ", "[statusDuration]%", tooltipDisplay="The bonus duration of your own status effects, base duration of a skill is increased by this percentage. Which is calculated by (int*0.5)% + perks. So at 100 int, skills would last 50% longer. Keep in mind skills that last 1 turn will be increased to 2, as all effects also last the turn they are cast. The turn count is always rounded down. This also boosts restraints and sleep effects by the same amount.")
        use ON_SingleStatDisplay("Effect Chance: ", "[statusAccuracyBonus]%", tooltipDisplay="Your base status effect accuracy is derived by the the individual skills stat used, its base chance, and this stat. Which is calculated from int-5(0.25% per point) + luck-5(0.1% per point) + perks. There's also a random roll(d100) added, that are then all added together to decide if the skill applies its status effect.")
        use ON_SingleStatDisplay("Status Res: ", "[statusEvadeBonus]%", tooltipDisplay="Your base status effect resistance based on your stats, this isn't counting any res to specific effects you might have, or any of the multiple other factors in combat that can increase your chance to be effected, such as being restrained, the attacks innate res stat, or its fetishes. This is calculated via will-5(0.25% per point) + luck-5(0.1% per point) + perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Allure Bonus: ", "[flatAllureBonus]", tooltipDisplay="The flat boost to arousal dealt gained from your allure. Calculated by 10% of (Your total allure - 5), the 10% scaling can be increased by perks.")
        use ON_SingleStatDisplay("Allure Bonus%: ", "[percentAllureBonus]%", tooltipDisplay="The percentage here is the bonus arousal that will be added to your skill's base power from your allure. (Your Allure-5)*0.002*(multiplied by 100 to show the percent increase. Normally base skill power.) + Perk Bonus.")






screen ON_SensitivityListDisplay:
    use ON_Scrollbox("Sensitivity"):
        use ON_SingleDisplay("Cock: ", "[player.BodySensitivity.Sex]%", tooltipDisplay="How sensitive your penis is.")
        use ON_SingleDisplay("Ass: ", "[player.BodySensitivity.Ass]%", tooltipDisplay="How sensitive your ass is. But I'm sure no monsters will actually go for your ass... R-Right?")
        use ON_SingleDisplay("Nipples: ", "[player.BodySensitivity.Breasts]%", tooltipDisplay="How sensitive your nipples are! Bit of an odd thing for a guy to think about isn't it?")
        use ON_SingleDisplay("Mouth: ", "[player.BodySensitivity.Mouth]%", tooltipDisplay="Are romantic kisses your weakness? Or maybe having a girl sit on your face?")
        use ON_SingleDisplay("Seduction: ", "[player.BodySensitivity.Seduction]%", tooltipDisplay="Try not to stare too much at erotic displays, listen to honeyed words, okay?")
        use ON_SingleDisplay("Magic: ", "[player.BodySensitivity.Magic]%", tooltipDisplay="Your body's innate ability to resist magical attacks!")
        use ON_SingleDisplay("Pain: ", "[player.BodySensitivity.Pain]%", tooltipDisplay="Do you like getting punished?")

screen ON_FetishListDisplay:
    use ON_Scrollbox("Fetishes"):
        for fetish in player.FetishList:
            if fetish.Type == "Fetish":
                use ON_SingleFetishDisplay(str(fetish.name + ":"), fetish)

screen ON_PerkListDisplay:
    use ON_Scrollbox("Perks"):
        for perk in player.perks:
            if perk.PlayerCanPurchase != "HiddenCompletelyFromPlayer":
                $ theTimeType = ""
                for y in perk.PerkType:
                    if y == "TimeDuration" or y == "TurnDuration":
                        $ theTimeType = y
                use ON_SingleDisplay(perk.name, "", tooltipDisplay=perk.description, duration=perk.duration, timeType=theTimeType)

        if len(player.perks) == 0:
            use ON_SingleDisplay("None... yet!", "")

screen ON_ResistanceListDisplay:
    use ON_Scrollbox("Resistances"):
        use ON_SingleStatDisplay("Stun:", "[player.resistancesStatusEffects.Stun]%")
        use ON_SingleStatDisplay("Charm:", "[player.resistancesStatusEffects.Charm]%")
        use ON_SingleStatDisplay("Aphrodisiac:", "[player.resistancesStatusEffects.Aphrodisiac]%")
        use ON_SingleStatDisplay("Restraints:", "[player.resistancesStatusEffects.Restraints]%")
        use ON_SingleStatDisplay("Sleep:", "[player.resistancesStatusEffects.Sleep]%")
        use ON_SingleStatDisplay("Trance:", "[player.resistancesStatusEffects.Trance]%")
        use ON_SingleStatDisplay("Paralysis:", "[player.resistancesStatusEffects.Paralysis]%")
        use ON_SingleStatDisplay("Debuff:", "[player.resistancesStatusEffects.Debuff]%")

screen ON_InventoryDisplay(inventoryType, columns=1):
    $ items = []
    $ spaceNext = 0
    for item in player.inventory.items:
        if (inventoryType == 1 and (item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable" or item.itemType == "NotCombatConsumable" or item.itemType == "Loot") or
            inventoryType == 2 and (item.itemType == "Rune" and RuneOrAccessory == 0) or
            inventoryType == 2 and (item.itemType == "Accessory"  and RuneOrAccessory == 1) or
            inventoryType == 3 and (item.itemType == "Key")):
                $ items.append(item)
    use ON_Scrollbox(""):
        fixed ysize 4 # spacing
        grid columns 1:
            xfill True
            for c in range(0, columns):
                vbox:
                    xfill True
                    for i in range(c, len(items), columns):
                        use ON_SingleItemDisplay(items[i], spaceNext)

    for c in range(0, columns-1):
        $ pct = (1.0+c)/columns
        add "gui/framedivider211partial.png" xalign pct




init python:
    characterMenuTab = "Stats"
    inventoryTab = 1
    characterMenuTooltip = ""

screen ON_CharacterDisplayScreen:
    $ _game_menu_screen = "ON_CharacterDisplayScreen"

    tag menu

    use game_menu(_("Character")):
        fixed:
            xpos 60
            ysize 900
            xsize 1500
            frame:
                xpos 0
                ypos 50
                xsize 1289
                ysize 222

                text "[player.name]" size fontsize xpos 400 xalign 1.0 ypos 40
                # if this is from the character menu, also show XP until next level, and button to level up
                $ exp = player.stats.ExpNeeded - player.stats.Exp
                $ showLevelUp = InventoryAvailable and (player.perkPoints >= 1 or player.SensitivityPoints >=1 or player.statPoints >= 1)

                vbox:
                    ypos 90
                    textbutton "Level [player.stats.lvl]" text_size 24 xpos 404 ysize 25 xalign 1.0 text_color "#fff"
                    textbutton "[exp] XP to next level" text_size 24 xpos 404 ysize 25 xalign 1.0 text_color "#fff"

                    if showLevelUp:
                        textbutton "Spend Unused stat points!" text_size 24 action SetVariable ("shifting", 1), Jump("spendLvlUpPoints") xpos 424 ysize 25 xalign 1.0

                fixed:
                    xpos 500
                    xsize 200
                    ypos 100
                    use ON_SingleStatDisplay("Virility: ", "[Virility]%", tooltipDisplay="Measures the fertility of a man, as well as his semen's thickness, flavour, and nutritional value to monster girls. Increases the effectiveness of holy skills, and increases the effectiveness of monster girl's energy draining and semen eating abilities on you. Equal to your (level-1)*0.5 + spirit*5 + 10 + any perks you have!")


                fixed:
                    xpos 800
                    xsize 675
                    ypos 45
                    use ON_EquipmentListDisplay

            fixed:
                ypos -10
                use ON_HealthDisplayInner(True, xOffset=615, menuCall=1)

            hbox:
                xpos 0
                ypos 285
                fixed xsize 10 ysize 30 # spacing

                if InventoryAvailable:
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_selected.png"
                            action [SensitiveIf(characterMenuTab != "Stats"), SetVariable ("characterMenuTab", "Stats")]
                        text "Stats" xalign 0.5 yalign 0.5
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_selected.png"
                            action [SensitiveIf(characterMenuTab != "Skills"), SetVariable ("characterMenuTab", "Skills")]
                        text "Skills" xalign 0.5 yalign 0.5
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_selected.png"
                            action [SensitiveIf(characterMenuTab != "Inventory"), SetVariable ("characterMenuTab", "Inventory")]
                        text "Inventory" xalign 0.5 yalign 0.5
                    fixed:
                        frame:
                            xalign 1.0
                            xoffset -260
                            ysize 51
                            xsize 275
                            text "  Eros: ξ [player.inventory.money]" size on_listTitleSize yalign 0.5 xalign 0.25
                else:
                    $ characterMenuTab = "Stats"
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_selected.png"
                            action [SensitiveIf(characterMenuTab != "Stats"), SetVariable ("characterMenuTab", "Stats")]
                        text "Stats" xalign 0.5 yalign 0.5
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_insensitive.png"
                        text "Skills" xalign 0.5 yalign 0.5
                    fixed:
                        xsize 240
                        ysize 45
                        imagebutton:
                            idle "gui/tab_idle.png"
                            hover "gui/tab_hover.png"
                            insensitive "gui/tab_insensitive.png"
                        text "Inventory" xalign 0.5 yalign 0.5
                    fixed:
                        frame:
                            xalign 1.0
                            xoffset -300
                            ysize 51
                            xsize 240
                            text "Eros:  ξ [player.inventory.money]" size on_listTitleSize yalign 0.5 xalign 0.3


            frame:
                ypos 330
                ysize 367
                xsize 1289

                if characterMenuTab == "Stats":
                    hbox:
                        #if name == "Allure:" or name == "Technique:" or name == "Power:" or name == "Luck:" or name == "Willpower:":
                        $ relatedStat = player.stats.getStat("Power")
                        $ powerBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ powerPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
                        $ relatedStat = player.stats.getStat("Intelligence")
                        $ intBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ intPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
                        $ relatedStat = player.stats.getStat("Technique")
                        $ techBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ techPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
                        $ relatedStat = player.stats.getStat("Allure")
                        $ allureBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ allurePerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
                        $ relatedStat = player.stats.getStat("Willpower")
                        $ willBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ willPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
                        $ relatedStat = player.stats.getStat("Luck")
                        $ luckBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
                        $ luckPerBoost =  float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))

                        $ powerDisplay = player.stats.Power-player.getStatBonusReduction("Power")
                        $ techDisplay = player.stats.Tech-player.getStatBonusReduction("Technique")
                        $ intDisplay = player.stats.Int-player.getStatBonusReduction("Intelligence")
                        $ allureDisplay = player.stats.Allure-player.getStatBonusReduction("Allure")
                        $ willDisplay = player.stats.Willpower-player.getStatBonusReduction("Willpower")
                        $ luckDisplay = player.stats.Luck-player.getStatBonusReduction("Luck")

                        $ coreStatsList = []
                        $ coreStatsList.append(player.stats.Power)
                        $ coreStatsList.append(player.stats.Tech)
                        $ coreStatsList.append(player.stats.Allure)
                        $ coreStatsList.append(player.stats.Int)
                        $ biggestStat = max(coreStatsList)*0.5
                        $ statDamMod = biggestStat + (player.stats.Allure + player.stats.Tech + player.stats.Int +  player.stats.Power)/4

                        $ flatCore = float("{0:.2f}".format(getCoreStatFlatBonus(statDamMod)))
                        $ percentCore = float("{0:.2f}".format(getCoreStatPercentBonus(statDamMod, 100)))


                        fixed:
                            xsize 300
                            ysize 352
                            use ON_StatsListDisplay(True)

                        if renpy.variant("touch"):
                            fixed xsize 16 #spacing
                        else:
                            fixed xsize 4 #spacing
                            add "gui/framedivider235.png"

                        fixed:
                            xsize 298
                            ysize 352
                            use ON_SensitivityListDisplay

                        if renpy.variant("touch"):
                            fixed xsize 5 #spacing
                            add "gui/framedivider235.png"
                        else:
                            fixed xsize 4 #spacing
                            add "gui/framedivider235.png"



                        fixed:
                            xsize 298
                            ysize 352
                            use ON_FetishListDisplay

                        if renpy.variant("touch"):
                            fixed xsize 5 #spacing
                            add "gui/framedivider235.png"
                        else:
                            fixed xsize 4 #spacing
                            add "gui/framedivider235.png"



                        fixed:
                            xsize 348
                            ysize 352
                            use ON_PerkListDisplay

                elif characterMenuTab == "Inventory":
                    hbox:
                        vbox:
                            hbox:
                                fixed xsize 6 ysize 24 # spacing
                                fixed:
                                    xsize 192
                                    ysize 36
                                    imagebutton:
                                        idle "gui/smalltab_idle.png"
                                        hover "gui/smalltab_hover.png"
                                        insensitive "gui/smalltab_selected.png"
                                        action [SensitiveIf(inventoryTab != 1), SetVariable ("inventoryTab", 1)]
                                    text "Consumables" xalign 0.5 yalign 0.5 size 22
                                fixed:
                                    xsize 192
                                    ysize 36
                                    imagebutton:
                                        idle "gui/smalltab_idle.png"
                                        hover "gui/smalltab_hover.png"
                                        insensitive "gui/smalltab_selected.png"
                                        action [SensitiveIf(inventoryTab != 2), SetVariable ("inventoryTab", 2), SetVariable ("RuneOrAccessory", 0)]
                                    text "Equipment" xalign 0.5 yalign 0.5 size 22
                                fixed:
                                    xsize 192
                                    ysize 36
                                    imagebutton:
                                        idle "gui/smalltab_idle.png"
                                        hover "gui/smalltab_hover.png"
                                        insensitive "gui/smalltab_selected.png"
                                        action [SensitiveIf(inventoryTab != 3), SetVariable ("inventoryTab", 3)]
                                    text "Key Items" xalign 0.5 yalign 0.5 size 22
                                if inventoryTab == 2:
                                    fixed:
                                        xsize 162
                                        ysize 36
                                        imagebutton:
                                            idle "gui/smallertab_idle_outline.png"
                                            hover "gui/smallertab_hover_outline.png"
                                            insensitive "gui/smallertab_selected.png"
                                            action [SensitiveIf(RuneOrAccessory != 0), SetVariable ("RuneOrAccessory", 0)]
                                        text "Runes" xalign 0.5 yalign 0.5 size 22

                                    fixed:
                                        xsize 162
                                        ysize 36
                                        imagebutton:
                                            idle "gui/smallertab_idle_outline.png"
                                            hover "gui/smallertab_hover_outline.png"
                                            insensitive "gui/smallertab_selected.png"
                                            action [SensitiveIf(RuneOrAccessory == 0), SetVariable ("RuneOrAccessory", 1)]
                                        text "Accessories" xalign 0.5 yalign 0.5 size 22

                            add "gui/framedividerhoriz619.png"

                            fixed:
                                xsize 915
                                ysize 306
                                use ON_InventoryDisplay(inventoryTab, 2)

                        add "gui/framedivider235.png"

                        fixed:
                            xsize 301
                            ysize 352
                            use ON_ResistanceListDisplay

                else:
                    use ON_MenuSkillsList(height=357)
                    fixed:
                        xpos 870
                        xsize 915
                        ysize 306
                        add "gui/framedivider235.png"
                    vbox:
                        xpos 920
                        text "Re-Organize!" xalign 0.5
                        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
                        textbutton "Alphebetical" text_size on_listTextSize action [Jump("SortSkillsByAlphebet")] xalign 0.5
                        textbutton "Reverse Alphebetical" text_size on_listTextSize action [Jump("SortSkillsByReverseAlphebet")] xalign 0.5
                        textbutton "Lowest Energy Cost" text_size on_listTextSize action [Jump("SortSkillsByEnergyCost")] xalign 0.5
                        textbutton "Highest Energy Cost" text_size on_listTextSize action [Jump("SortSkillsByReverseEnergyCost")] xalign 0.5
                        textbutton "Lowest Damage" text_size on_listTextSize action [Jump("SortSkillsByDamage")] xalign 0.5
                        textbutton "Highest Damage" text_size on_listTextSize action [Jump("SortSkillsByReverseDamage")] xalign 0.5
                        if manualSort == 0:
                            textbutton "Manual Sorting" text_size on_listTextSize action [Jump("ActivateManualSorting")] xalign 0.5
                        else:
                            textbutton "End Manual Sorting" text_size on_listTextSize action [Jump("DeactivateManualSorting")] xalign 0.5
                            if swappingSkill != -1:
                                $ showText = player.skillList[swappingSkill].name
                                textbutton "[showText]" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5

            frame:
                ypos 705
                xpadding 12
                ypadding 10
                ysize 262
                xsize 1289
                text characterMenuTooltip size 30


            use ON_UseItemConfirm



label SortSkillsByAlphebet:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.name)
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label SortSkillsByReverseAlphebet:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.name, reverse=True)
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label SortSkillsByEnergyCost:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.cost )
    $ characterMenuTooltip = ""
    $ cmenu_refreshSwapMenu()

    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label SortSkillsByReverseEnergyCost:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.cost , reverse=True)
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label SortSkillsByDamage:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.power + (player.stats.getStat(x.statType)-5)*0.3)
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label SortSkillsByReverseDamage:
    $ renpy.retain_after_load()
    $ player.skillList = sorted(player.skillList, key = lambda x: x.power + (player.stats.getStat(x.statType)-5)*0.3, reverse=True)
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction


label ActivateManualSorting:
    $ manualSort = 1
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction
label DeactivateManualSorting:
    $ manualSort = 0
    $ cmenu_refreshSwapMenu()
    $ characterMenuTooltip = ""
    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction


label EquipItem:
    $ renpy.retain_after_load()

    $ itemChoice = Item("Empty", "", "0")
    $ removingItem = Item("Empty", "", "0")
    if RemovingEquipment == 0:
        $ itemChoice = player.inventory.items[inventoryETarget]

    #if RemovingEquipment != 0: #Unequip line implementation for Equipment, doesn't really work given it has the same pitfalls as item use events, except stopping equipping during events would be a big hassle, so im shelfing this for now
    #    if RemovingEquipment == 1:
    #        $ removingItem = copy.deepcopy(player.inventory.RuneSlotOne)
    #    if RemovingEquipment == 2:
    #        $ removingItem = copy.deepcopy(player.inventory.RuneSlotTwo)
    #    if RemovingEquipment == 3:
    #        $ removingItem = copy.deepcopy(player.inventory.RuneSlotThree)
    #    if RemovingEquipment == 4:
    #        $ removingItem = copy.deepcopy(player.inventory.AccessorySlot)
    #    if removingItem.onUnequip != "":
    #        $ display = removingItem.onUnequip
    #        $ config.keymap['game_menu'].remove('mouseup_3')
    #        $ config.keymap['game_menu'].remove('K_ESCAPE')
    #        $ config.keymap['game_menu'].remove('K_MENU')
    #        $ renpy.clear_keymap_cache()
    #        call read
    #        $ config.keymap['game_menu'].append('mouseup_3')
    #        $ config.keymap['game_menu'].append('K_ESCAPE')
    #        $ config.keymap['game_menu'].append('K_MENU')
    #        $ renpy.clear_keymap_cache()

    if itemChoice.itemType == "Rune" or RemovingEquipment <=3:
        if TargetingEquipSlot == 1 or RemovingEquipment == 1:
            if player.inventory.RuneSlotOne.name != "Empty":
                $ player.inventory.give(player.inventory.RuneSlotOne.name, 1)
            $ player.inventory.equip(1, player, -1)
            if RemovingEquipment == 0:
                $ player.inventory.RuneSlotOne = itemChoice
                $ player.inventory.equip(1, player, 1)
            else:
                $ player.inventory.RuneSlotOne = Item("Empty", "Rune", "0")
        if TargetingEquipSlot == 2 or RemovingEquipment == 2:
            if player.inventory.RuneSlotTwo.name != "Empty":
                $ player.inventory.give(player.inventory.RuneSlotTwo.name, 1)
            $ player.inventory.equip(2, player, -1)
            if RemovingEquipment == 0:
                $ player.inventory.RuneSlotTwo = itemChoice
                $ player.inventory.equip(2, player, 1)
            else:
                $ player.inventory.RuneSlotTwo = Item("Empty", "Rune", "0")
        if TargetingEquipSlot == 3 or RemovingEquipment == 3:
            if player.inventory.RuneSlotThree.name != "Empty":
                $ player.inventory.give(player.inventory.RuneSlotThree.name, 1)
            $ player.inventory.equip(3, player, -1)
            if RemovingEquipment == 0:
                $ player.inventory.RuneSlotThree = itemChoice
                $ player.inventory.equip(3, player, 1)
            else:
                $ player.inventory.RuneSlotThree = Item("Empty", "Rune", "0")

    if itemChoice.itemType == "Accessory" or RemovingEquipment == 4:
        if player.inventory.AccessorySlot.name != "Empty":
            $ player.inventory.give(player.inventory.AccessorySlot.name, 1)
        $ player.inventory.equip(4, player, -1)
        if RemovingEquipment == 0:
            $ player.inventory.AccessorySlot = itemChoice
            $ player.inventory.equip(4, player, 1)
        else:
            $ player.inventory.AccessorySlot = Item("Empty", "Accessory", "0")

    if RemovingEquipment == 0:
        if itemChoice.itemType == "Rune":
            if TargetingEquipSlot == 1:
                $ player.inventory.useItem( player.inventory.RuneSlotOne.name)
            if TargetingEquipSlot == 2:
                $ player.inventory.useItem( player.inventory.RuneSlotTwo.name)
            if TargetingEquipSlot == 3:
                $ player.inventory.useItem( player.inventory.RuneSlotThree.name)
        else:
            $ player.inventory.useItem( player.inventory.AccessorySlot.name)
    $ player.CalculateStatBoost()


    if player.stats.hp <= 0:
        $ player.stats.hp = 0
    if player.stats.ep >= player.stats.max_true_ep:
        $ player.stats.ep = player.stats.max_true_ep
    if player.stats.ep <= 0:
        $ player.stats.ep = 0
    if player.stats.sp >= player.stats.max_true_sp:
        $ player.stats.sp = player.stats.max_true_sp
    if player.stats.sp <= 0:
        $ player.stats.sp = 0


    #if RemovingEquipment == 0: #Equip line implementation for Equipment, doesn't really work given it has the same pitfalls as item use events, except stopping equipping during events would be a big hassle, so im shelfing this for now
    #    if itemChoice.onEquip != "":
    #        $ display = itemChoice.onEquip
    #        $ config.keymap['game_menu'].remove('mouseup_3')
    #        $ config.keymap['game_menu'].remove('K_ESCAPE')
    #        $ config.keymap['game_menu'].remove('K_MENU')
    #        $renpy.clear_keymap_cache()
    #        call read
    #        $ config.keymap['game_menu'].append('mouseup_3')
    #        $ config.keymap['game_menu'].append('K_ESCAPE')
    #        $ config.keymap['game_menu'].append('K_MENU')
    #        $renpy.clear_keymap_cache()



    $ RemovingEquipment = 0
    $ unequippingItem = 0


    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu
    python:
        renpy.call_in_new_context('_game_menu')


    jump exitCombatFunction


label useInventoryItem:
    $ renpy.retain_after_load()
    $ itemChoice = player.inventory.items[inventoryTarget]

    $ _game_menu_screen = None

    $ attackerName = player.name
    $ attackerHeOrShe = getHeOrShe(player)
    $ attackerHisOrHer = getHisOrHer(player)
    $ attackerHimOrHer = getHimOrHer(player)
    $ attackerYouOrMonsterName = getYouOrMonsterName(player)
    python:
        try:
            displayingScene.theScene
        except:
            displayingScene = Dialogue()


    $ display = ""
    if len(itemChoice.skills) > 0 and itemChoice.itemType != "DissonantConsumable":
        $ player.inventory.useItem(itemChoice.name)
        $ fetchSkill = getFromName(itemChoice.skills[0], SkillsDatabase)
        $ menuItemChoice = copy.deepcopy(SkillsDatabase[fetchSkill])
        $ menuItemChoice.isSkill = itemChoice.itemType

        $ holder = HealCalc(player, menuItemChoice)
        $ player = holder[0]
        $ display += holder[1]



        $ display = returnReaderDiction(display)
        $ characterMenuTooltip = display
        $ tt = Tooltip(display)

        if player.stats.Exp >= player.stats.ExpNeeded:

            $ culmitiveLeveling = 0
            $ hpIncreases = 0
            $ statPointIncreases = 0
            $ sensitivityIncreases = 0
            $ perkIncreases = 0
            call levelUpSpot from _call_levelUpSpot_3

    elif lineOfScene < len(displayingScene.theScene):
        $ display = "You can't use that right now."
        $ characterMenuTooltip = display
        $ tt = Tooltip(display)
    else:
        #$ renpy.curry(renpy.end_interaction)(True) # thought this might be able to close the menu before instigating an event to make shit work better. But it either crashes, or does nothing, seems to only work with a button, even if it did, im pretty sure it'd end the event before it started.
        $ player.inventory.useItem(itemChoice.name)
        $ display = itemChoice.useOutcome
        $ config.keymap['game_menu'].remove('mouseup_3')
        $ config.keymap['game_menu'].remove('K_ESCAPE')
        $ config.keymap['game_menu'].remove('K_MENU')
        $renpy.clear_keymap_cache()
        $ itemEvent = 1
        call read from _call_read_1
        $ itemEvent = 0
        $ config.keymap['game_menu'].append('mouseup_3')
        $ config.keymap['game_menu'].append('K_ESCAPE')
        $ config.keymap['game_menu'].append('K_MENU')
        $renpy.clear_keymap_cache()

    $ _game_menu_screen="ON_CharacterDisplayScreen"
    #call _game_menu from _call__game_menu
    python:
        renpy.call_in_new_context('_game_menu')


    jump exitCombatFunction

label SetSkillOrder:
    $ renpy.retain_after_load()
    if swappingSkill == -1:
        $ swappingSkill = skillTarget
    else:
        $ xS = copy.deepcopy(player.skillList[swappingSkill])
        $ yS = copy.deepcopy(player.skillList[skillTarget])

        $ player.skillList[swappingSkill] = yS
        $ player.skillList[skillTarget] = xS
        $ cmenu_refreshSwapMenu()
        $ swappingSkill = -1

    $ _game_menu_screen="ON_CharacterDisplayScreen" # replaces SkillsDisplayScreen
    #call _game_menu from _call__game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction

label useSkillFromMenu:
    $ renpy.retain_after_load()
    $ itemChoice = Item("Blank", "Null", 0)
    $ finalDamage = 0
    $ skillChoice = player.skillList[skillTarget]

    $ attackerName = player.name
    $ attackerHeOrShe = getHeOrShe(player)
    $ attackerHisOrHer = getHisOrHer(player)
    $ attackerHimOrHer = getHimOrHer(player)
    $ attackerYouOrMonsterName = getYouOrMonsterName(player)

    $ holder = HealCalc(player, skillChoice)
    $ player = holder[0]
    $ display += holder[1]

    if skillChoice.costType == "ep":
        $ player.stats.ep -= skillChoice.cost
    elif skillChoice.costType == "hp":
        $ actualCost = skillChoice.cost + (player.stats.max_true_hp-100)*0.15
        $ actualCost = math.floor(actualCost)
        $ actualCost = int(actualCost)
        $ player.stats.hp += actualCost
    elif skillChoice.costType == "sp":
        $ player.stats.sp -= skillChoice.cost

    $ display = returnReaderDiction(display)
    $ characterMenuTooltip = display

    $ tt = Tooltip(display)

    $ _game_menu_screen="ON_CharacterDisplayScreen" # replaces SkillsDisplayScreen
    #call _game_menu from _call__game_menu
    python:
        renpy.call_in_new_context('_game_menu')

    jump exitCombatFunction
