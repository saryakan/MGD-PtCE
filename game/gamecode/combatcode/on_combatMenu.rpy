
# WOOOOO COMPLETELY REDONE COMBAT MENU
# looks like some shit you'd find in RPGmaker tbh lmao
# No more pagination - everything is in a hierarchical scrollbox-based view
init python:

    topRowAlignmentY = 0.78
    bottomRowAlignmentY = 0.890
    buttonWidth = 360

    tt = Tooltip("")
    currentButtonX = -1.5
    currentButtonY = -1.5
    targeting = 0
    target = 0
    xMonAdjust = 0.3
    xMonPos = 0
    skillToolTip = ""
    charmIcon = "StatusIcons/charmIcon.png"
    defendIcon = "StatusIcons/defendIcon.png"
    defendIcon2 = "StatusIcons/defendIcon2.png"
    defendIcon3 = "StatusIcons/defendIcon3.png"
    poisonIcon = "StatusIcons/poisonIcon.png"
    restrainedIcon = "StatusIcons/restrainedIcon.png"
    stunnedIcon = "StatusIcons/stunedIcon.png"
    surrenderIcon = "StatusIcons/SurrenderIcon.png"

    sleepIcon0 = "StatusIcons/Sleep0Icon.png"
    sleepIcon1 = "StatusIcons/Sleep1Icon.png"
    sleepIcon2 = "StatusIcons/Sleep2Icon.png"
    sleepIcon3 = "StatusIcons/Sleep3Icon.png"

    tranceIcon10 = "StatusIcons/trance10Icon.png"
    tranceIcon9 = "StatusIcons/trance9Icon.png"
    tranceIcon8 = "StatusIcons/trance8Icon.png"
    tranceIcon7 = "StatusIcons/trance7Icon.png"
    tranceIcon6 = "StatusIcons/trance6Icon.png"
    tranceIcon5 = "StatusIcons/trance5Icon.png"
    tranceIcon4 = "StatusIcons/trance4Icon.png"
    tranceIcon3 = "StatusIcons/trance3Icon.png"
    tranceIcon2 = "StatusIcons/trance2Icon.png"
    tranceIcon1 = "StatusIcons/trance1Icon.png"
    tranceIcon0 = "StatusIcons/trance0Icon.png"

    paralysisIcon10 = "StatusIcons/paralysis10Icon.png"
    paralysisIcon9 = "StatusIcons/paralysis9Icon.png"
    paralysisIcon8 = "StatusIcons/paralysis8Icon.png"
    paralysisIcon7 = "StatusIcons/paralysis7Icon.png"
    paralysisIcon6 = "StatusIcons/paralysis6Icon.png"
    paralysisIcon5 = "StatusIcons/paralysis5Icon.png"
    paralysisIcon4 = "StatusIcons/paralysis4Icon.png"
    paralysisIcon3 = "StatusIcons/paralysis3Icon.png"
    paralysisIcon2 = "StatusIcons/paralysis2Icon.png"
    paralysisIcon1 = "StatusIcons/paralysis1Icon.png"

    atkUpIcon = "StatusIcons/AtkUpIcon.png"
    atkDownIcon = "StatusIcons/AtkDownIcon.png"
    defUpIcon = "StatusIcons/DefenceUpIcon.png"
    defDownIcon = "StatusIcons/DefenceDownIcon.png"

    powUpIcon = "StatusIcons/PowUpIcon.png"
    powDownIcon = "StatusIcons/PowDownIcon.png"
    techUpIcon = "StatusIcons/TechUpIcon.png"
    techDownIcon = "StatusIcons/TechDownIcon.png"
    intUpIcon = "StatusIcons/IntUpIcon.png"
    intDownIcon = "StatusIcons/IntDownIcon.png"
    allureUpIcon = "StatusIcons/AllureUpIcon.png"
    allureDownIcon = "StatusIcons/AllureDownIcon.png"
    willUpIcon = "StatusIcons/WillUpIcon.png"
    willDownIcon = "StatusIcons/WillDownIcon.png"
    luckUpIcon = "StatusIcons/LuckUpIcon.png"
    luckDownIcon = "StatusIcons/LuckDownIcon.png"

    critIcon = "StatusIcons/CritChanceIcon.png"

    stanceBreaking = 0

    # All menu items are based on this class
    # Menu columns are lists of MenuItemDefs, either generated dynamically or predefined
    class MenuItemDef():
        def __init__(self, name="NAME", tooltip="", showIf="True", sensitiveIf="True", openSubMenu="", jumpTo="", setVar="", setValue="", usedFilterType="", rawName=None):
            self.name = name # the displayed name of the item
            self.tooltip = tooltip # Any tooltip it shows, "" for none
            self.showIf = showIf # condition (Python expr in a string) for hiding/showing the item
            self.sensitiveIf = sensitiveIf # condition (Python expr in a string) for using the item
            self.openSubMenu = openSubMenu # name of submenu opened by this item, handled by cmenu_setColumn()
            self.jumpTo = jumpTo # label to jump to when clicked
            self.setVar = setVar # var to set when clicked
            self.setValue = setValue # value to set var to
            self.usedFilterType = usedFilterType # what to do when adding this to recently used list - "Basic", "Item", "Skill", or ""
            if rawName is None:
                self.rawName = name
            else:
                self.rawName = rawName

    # Convenience function - show option to run?
    def cmenu_showRunOpt():
        for stance in player.combatStance:
            if stance.Stance != "None":
                return False
        return True

    # convenience functions - which of the three mutually exclusive push away options to show
    # if there are multiple enemies, show mon list
    def cmenu_showMonList():
        return len(monsterEncounter) > 1

    # else if there are multiple stances with the target, show stance list
    def cmenu_showPushList():
        return len(monsterEncounter[target].combatStance) > 1 and not cmenu_showMonList()

    # else, show single opt
    def cmenu_showSinglePushOption():
        return not cmenu_showPushList() and not cmenu_showMonList()

    # Convenience function - show escape option?
    def cmenu_hasEscapeSkills():
        for skill in player.skillList:
            if skill.statusEffect == "Escape":
                return True
        return False


    # Top-level menu
    cmenu_main = [
        MenuItemDef(name="Caress", tooltip="Gently caress your opponent. The most basic of skills, is unaffected by the target's sensitivities.\n{color=#F7B}Estimated Arousal: [caressEstimate]{/color}", jumpTo="combatBasicAttack", usedFilterType="Basic"),
        MenuItemDef(name="Skills", openSubMenu="Skills"),
        MenuItemDef(name="Items", tooltip="Use an item.", openSubMenu="Items", sensitiveIf="combatItems == 0"),
        MenuItemDef(name="Defend", tooltip="Increase your defence, dodge chance, and get a bonus against stat checks.", jumpTo="combatDefend", sensitiveIf="player.statusEffects.charmed.duration <= 0", usedFilterType="Basic"),
        MenuItemDef(name="Run", tooltip="Attempt to run!", jumpTo="combatRun", showIf="cmenu_showRunOpt()", sensitiveIf="player.statusEffects.charmed.duration <= 0 and canRun == True and Rut == False"),
        MenuItemDef(name="Push Away", tooltip="Attempt to get out of a stance! Usable for free once per turn!", setVar="stanceBreaking", setValue=1, jumpTo="pushaway", showIf="not cmenu_showRunOpt() and cmenu_showSinglePushOption()", sensitiveIf="player.statusEffects.charmed.duration <= 0 and pushAwayAttempt == 0"),
        MenuItemDef(name="Push Away", tooltip="Attempt to get out of a stance! Usable for free once per turn!", openSubMenu="Push", showIf="not cmenu_showRunOpt() and cmenu_showPushList()", sensitiveIf="player.statusEffects.charmed.duration <= 0 and pushAwayAttempt == 0"),
        MenuItemDef(name="Push Away", tooltip="Attempt to get out of a stance! Usable for free once per turn!", openSubMenu="PushMon", showIf="not cmenu_showRunOpt() and cmenu_showMonList()", sensitiveIf="player.statusEffects.charmed.duration <= 0 and pushAwayAttempt == 0"),
        MenuItemDef(name="Other", tooltip="Like waiting to take a breather, or giving up, but you wouldn't do those things... Right?", openSubMenu="Surrender")
        ]

    # Skill subcategories
    cmenu_skills = [
        MenuItemDef(name="Sex", openSubMenu="SkillList", setVar="moveFilter", setValue="Sex"),
        MenuItemDef(name="Ass", openSubMenu="SkillList", setVar="moveFilter", setValue="Ass"),
        MenuItemDef(name="Breasts", openSubMenu="SkillList", setVar="moveFilter", setValue="Breasts"),
        MenuItemDef(name="Mouth", openSubMenu="SkillList", setVar="moveFilter", setValue="Mouth"),
        MenuItemDef(name="Seduction", openSubMenu="SkillList", setVar="moveFilter", setValue="Seduction"),
        MenuItemDef(name="Magic", openSubMenu="SkillList", setVar="moveFilter", setValue="Magic"),
        MenuItemDef(name="Pain", openSubMenu="SkillList", setVar="moveFilter", setValue="Pain"),
        MenuItemDef(name="Buffs", openSubMenu="SkillList", setVar="moveFilter", setValue="Buffs"),
        MenuItemDef(name="Afflictions", openSubMenu="SkillList", setVar="moveFilter", setValue="Afflictions"),
        MenuItemDef(name="Holy", openSubMenu="SkillList", setVar="moveFilter", setValue="Holy")
        ]


    # Surrender options ( ͡° ͜ʖ ͡°)
    cmenu_surrender = [
        MenuItemDef(name="Wait", tooltip="Just wait, and restore 5% of your energy.", jumpTo="combatWait", usedFilterType="Basic"),
        MenuItemDef(name="Surrender", tooltip="Let the monsters have their way with you...", jumpTo="combatGiveUp"),
        MenuItemDef(name="Super Surrender", tooltip="You give up so hard that you skip combat.", jumpTo="combatSurrender")
        ]

    # Struggle options
    cmenu_struggle = [
        MenuItemDef(name="Struggle", tooltip="Try to get free!", jumpTo="combatStruggle"),
        MenuItemDef(name="Struggle!!!", tooltip="Costs 10 energy. Desperately try to get free! About twice as effective as normal struggle.", setVar="desperateStruggle", setValue=1,  jumpTo="combatStruggle", sensitiveIf="player.stats.ep >= 10"),
        MenuItemDef(name="Defend", tooltip="Increase your defence, and get a bonus against stat checks!", jumpTo="combatDefend", sensitiveIf="player.statusEffects.charmed.duration <= 0"),
        MenuItemDef(name="Esc Skills", openSubMenu="SkillList", setVar="moveFilter", setValue="Escape", showIf="cmenu_hasEscapeSkills()"),
        MenuItemDef(name="Other", tooltip="Like waiting and giving up, but you wouldn't do those things... Right?", openSubMenu="Surrender")
        ]

    # Big array of columns, used for displaying the menu
    # This is shared between the combat menu and the skills list in the character screen
    # So it needs to be reset with cmenu_resetMenu() whenever either screen is brought up
    cmenu_columns = []

    # List of names - parent options for currently-open submenus
    # Names are checked against this and highlighted/disabled if they're part of the breadcrumb
    cmenu_breadcrumb = []


    # Sets a given column index to a given column, and removes any columns of higher depth.
    def cmenu_setColumn(depth, name, bcrumb_name):
        del cmenu_columns[depth:]
        del cmenu_breadcrumb[depth:]

        # If we're opening a submenu, add its parent to the breadcrumb
        if depth > 0:
            cmenu_breadcrumb.insert(depth-1, bcrumb_name)

        # Add main column
        if name == "Main":
            cmenu_columns.insert(depth, cmenu_main)

        # Add list of skill categories
        elif name == "Skills":
            cmenu_columns.insert(depth, cmenu_skills)

        # Add surrender menu
        elif name == "Surrender":
            cmenu_columns.insert(depth, cmenu_surrender)

        # Add generated list of kills based on moveFilter
        elif name == "SkillList":
            cmenu_columns.insert(depth, cmenu_getSkillList())

        # Add list of usable items
        elif name == "Items":
            cmenu_columns.insert(depth, cmenu_getItemList())

        # Add list of monsters to try to push away
        elif name == "PushMon":
            cmenu_columns.insert(depth, cmenu_getPushMonList())

        # Add list of stances to try to get out of
        elif name == "Push":
            cmenu_columns.insert(depth, cmenu_getPushList())

        else: #Given name doesn't match a defined column - assume it's something like "None"
            # We've already removed columns[depth:] so just get rid of the parent breadcrumb too
            del cmenu_breadcrumb[depth-1:]


    # System for equivalent stances, so we're not putting if statements about this everywhere
    # Each entry in the dict is equivalent to each entry in the matching array
    # but items in the arrays are NOT equivalent to each other
    # (so in math terms this does not actually represent an equivalence relation... go figure :P)
    stanceEquivalences = {"Penetration": ["Sex", "Anal"]}

    # Check for stance equivalence using the dict
    def StanceEquals(stance1, stance2):
        # duh
        if stance1 == stance2:
            return True

        # But also check the array
        elif stance1 in stanceEquivalences:
            if stance2 in stanceEquivalences[stance1]:
                return True

        # Do this both ways so it doesn't matter which stance is 1 or 2 (symmetric)
        elif stance2 in stanceEquivalences:
            if stance1 in stanceEquivalences[stance2]:
                return True

        return False



    # Logic for skill being visible in the list
    def skillIsVisible(skill):
        visible = False

        for tag in skill.skillTags:
            if moveFilter == tag:
                visible = True
            elif tag == "Penetration":
                for stanceCheck in player.combatStance:
                    if stanceCheck.Stance == "Sex" and moveFilter == "Sex":
                        visible = True
                    elif stanceCheck.Stance == "Anal" and moveFilter == "Ass":
                        visible = True
                if len(monsterEncounter) == 0 and (moveFilter == "Ass" or moveFilter == "Sex"):
                    visible = True


        for tag in skill.skillTags:
            if tag == "displayPain" and moveFilter == "Pain":
                visible = True
            if tag == "displayMagic" and moveFilter == "Magic":
                visible = True
            if tag == "displaySeduction" and moveFilter == "Seduction":
                visible = True
            if tag == "displayMouth" and moveFilter == "Mouth":
                visible = True
            if tag == "displayBreasts" and moveFilter == "Breasts":
                visible = True
            if tag == "displayAss" and moveFilter == "Ass":
                visible = True
            if tag == "displaySex" and moveFilter == "Sex":
                visible = True
            if tag == "displayPenetration":
                for stanceCheck in player.combatStance:
                    if stanceCheck.Stance == "Sex" and moveFilter == "Sex":
                        visible = True
                    elif stanceCheck.Stance == "Anal" and moveFilter == "Ass":
                        visible = True
                if len(monsterEncounter) == 0 and (moveFilter == "Ass" or moveFilter == "Sex"):
                    visible = True




        if not visible:
            return False

        visible = False

        if skill.requiresStance == "Any":
            visible = True
        else:
            for stanceCheck in player.combatStance:
                if StanceEquals(stanceCheck.Stance, skill.requiresStance):
                    visible = True

        for stanceCheck in player.combatStance:
            for stances in skill.startsStance:
                if stanceCheck.Stance == stances: # restrict stance we're already in - no equivalence
                    visible = False

        if len(monsterEncounter) == 1:

            i = 0
            for perk in monsterEncounter[0].perks:
                p = 0
                while  p < len(perk.PerkType):
                    for stances in skill.startsStance:
                        if perk.PerkType[p] == "NoAnus" and stances == "Anal":
                            visible = False

                        if perk.PerkType[p] == "NoPussy":

                            if stances == "Sex":
                                visible = False
                            for each in skill.skillTags:
                                if each == "Sex":
                                    visible = False

                    if perk.PerkType[p] == "NoChest":
                        for each in skill.skillTags:
                            if each == "Breasts":
                                visible = False

                    if perk.PerkType[p] == "NoMouth":
                        for fetishE in theTarget.FetishList:
                            if fetishE == "Kissing":
                                visible = False
                    p += 1
        if len(monsterEncounter) == 0:
            visible = True

        return visible



    # logic for skill being usable (clickable)
    def skillIsUsable(skill):

        if skill.costType == "ep":
            if player.stats.ep < skill.cost:
                return False
        elif skill.costType == "sp":
            if player.stats.sp < skill.cost:
                return False


        noGo = False
        canGo = False
        for Pstance in player.combatStance:
            for stances in skill.startsStance:
                if Pstance.Stance == stances: # restrict stance we're already in - no equivalence
                    noGo = True

            if "Any" != skill.requiresStance:
                if StanceEquals(Pstance.Stance, skill.requiresStance):
                    canGo = True
            else:
                canGo = True

            for pick in skill.unusableIfStance:
                if StanceEquals(Pstance.Stance, pick):
                    noGo = True
                if Pstance.Stance != "None" and pick == "Any":
                    noGo = True

        try:
            skill.requiresStatusEffectSelf
        except:
            skill.requiresStatusEffectSelf = ""

        if skill.requiresStatusEffectSelf != "" and skill.requiresStatusEffectSelf != "None":
            if player.statusEffects.hasThisStatusEffect(skill.requiresStatusEffectSelf) == False:
                noGo = True

        try:
            skill.requiresStatusPotencySelf
        except:
            skill.requiresStatusPotencySelf = 0

        if skill.requiresStatusPotencySelf > 0:
            if player.statusEffects.hasThisStatusEffectPotency(skill.requiresStatusEffectSelf, skill.requiresStatusPotencySelf) == False:
                noGo = True

        try:
            skill.unusableIfStatusEffectSelf
        except:
            skill.unusableIfStatusEffectSelf = [""]

        for skillStatus in skill.unusableIfStatusEffectSelf:
            if player.statusEffects.hasThisStatusEffect(skillStatus) == True:
                noGo = True

        try:
            skill.requiresPerkSelf
        except:
            skill.requiresPerkSelf = []

        reqMet = 0
        for eachReq in skill.requiresPerkSelf:
            if eachReq != "" and eachReq != "None":
                for perk in player.perks:
                    if perk.name == eachReq:
                        reqMet += 1
                        break
            else:
                reqMet += 1
        if reqMet != len(skill.requiresPerkSelf):
            noGo = True

        try:
            skill.unusableIfPerkSelf
        except:
            skill.unusableIfPerkSelf = []

        reqMet = 0
        for eachReq in skill.unusableIfPerkSelf:
            if eachReq != "" and eachReq != "None":
                for perk in player.perks:
                    if perk.name == eachReq:
                        noGo = True
                        break


        try:
            skill.requiresOnePerkSelf
        except:
            skill.requiresOnePerkSelf = []

        reqMet = 0
        if len (skill.requiresOnePerkSelf) == 0:
            reqMet = 1
        for eachReq in skill.requiresOnePerkSelf:
            if eachReq != "" and eachReq != "None":
                for perk in player.perks:
                    if perk.name == eachReq:
                        reqMet += 1
                        break
        if reqMet == 0:
            noGo = True

        if len(monsterEncounter) == 1:
            canGo = skillIsUsableForTarget(skill, monsterEncounter[0])

        if len(monsterEncounter) == 0:
            canGo = True
            noGo = False

        return (canGo and not noGo)



    # Logic for skill being clickable against a specific target
    def skillIsUsableForTarget(skill, target):
        noGo = False
        canGo = False

        for pick in skill.requiresTargetStance:
            if "Any" != pick:
                if target.combatStance[0].Stance != "None":
                    for monStance in target.combatStance:
                        if StanceEquals(monStance.Stance, pick):
                            canGo = True
            else:
                canGo = True

        for pick in skill.unusableIfTarget:
            for monStance in target.combatStance:
                if StanceEquals(monStance.Stance, pick):
                    noGo = True
                if monStance.Stance != "None" and pick == "Any":
                    noGo = True


        isunusable = getUnviableSets(skill, target)
        if isunusable == True:
            noGo = True


        if skill.requiresStatusEffect != "" and skill.requiresStatusEffect != "None":
            if target.statusEffects.hasThisStatusEffect(skill.requiresStatusEffect) == False:
                noGo = True

        if skill.requiresStatusPotency > 0:
            if target.statusEffects.hasThisStatusEffectPotency(skill.requiresStatusEffect, skill.requiresStatusPotency) == False:
                noGo = True

        for skillStatus in skill.unusableIfStatusEffect:
            if target.statusEffects.hasThisStatusEffect(skillStatus) == True:
                noGo = True

        try:
            skill.requiresPerk
        except:
            skill.requiresPerk = []

        reqMet = 0
        for eachReq in skill.requiresPerk:
            if eachReq != "" and eachReq != "None":
                for perk in target.perks:
                    if perk.name == eachReq:
                        reqMet += 1
                        break
            else:
                reqMet += 1
        if reqMet != len(skill.requiresPerk):
            noGo = True

        try:
            skill.unusableIfPerk
        except:
            skill.unusableIfPerk = []

        for eachReq in skill.unusableIfPerk:
            if eachReq != "" and eachReq != "None":
                for perk in target.perks:
                    if perk.name == eachReq:
                        noGo = True
                        break

        try:
            skill.requiresOnePerk
        except:
            skill.requiresOnePerk = []
        reqMet = 0
        if len (skill.requiresOnePerk) == 0:
            reqMet = 1
        for eachReq in skill.requiresOnePerk:
            if eachReq != "" and eachReq != "None":
                for perk in target.perks:
                    if perk.name == eachReq:
                        reqMet += 1
                        break
        if reqMet == 0:
            noGo = True



        for perk in target.perks:
            p = 0
            while  p < len(perk.PerkType):
                for stances in skill.startsStance:
                    if perk.PerkType[p] == "NoAnus" and stances == "Anal":
                        canGo = False

                    if perk.PerkType[p] == "NoPussy":
                        if stances == "Sex":
                            canGo = False
                        for each in skill.skillTags:
                            if each == "Sex":
                                canGo = False

                if perk.PerkType[p] == "NoChest":
                    for each in skill.skillTags:
                        if each == "Breasts":
                            canGo = False

                if perk.PerkType[p] == "NoMouth":
                    for fetishE in theTarget.FetishList:
                        if fetishE == "Kissing":
                            canGo = False
                p += 1

        return (canGo and not noGo)



    # Build a list of MenuItemDefs for skills based on moveFilter
    def cmenu_getSkillList():
        arr = []

        for skill in player.skillList:
            if skillIsVisible(skill):
                usable = skillIsUsable(skill)

                skillToolTip = getSkillToolTip(skill, player, skill.descrips)

                skillID = getFromName(skill.name, player.skillList)

                arr.append(MenuItemDef(name=skill.name, tooltip=skillToolTip, setVar="SkillNumber", setValue=skillID, jumpTo="combatMoveChoice", sensitiveIf=usable, usedFilterType="Skill"))
        return arr


    # Build a list of MenuItemDefs for usable items
    def getSkillToolTip(skill, player, skillDes):
        skillToolTip = ""
        if skill.cost != 0:
            costDisplay = skill.costType
            actualCost = skill.cost
            if skill.costType == "hp":
                actualCost = skill.cost + (player.stats.max_true_hp-100)*0.15
                actualCost = math.floor(actualCost)
                actualCost = int(actualCost)
            skillToolTip += "Costs " + str(actualCost) + " " + costDisplay + ". "
        if skill.statType != "" and skill.statType != "None" and skill.statType != "PercentMaxArousal":
            skillToolTip += "Uses " + skill.statType + ". "
        if skill.requiresStance != "Any":
            skillToolTip += " Requires the " + skill.requiresStance + " stance."

        try:
            skill.startsStance[0]
        except:
            skill.startsStance = [""]
        if skill.startsStance[0] != "":
            if len(skill.startsStance) == 1:
                skillToolTip += "\nStarts the " + skill.startsStance[0] + " stance."
            else:
                skillToolTip += "\nStarts the " + skill.startsStance[0] + " and " + skill.startsStance[1] + " stances."
        if skill.statType != "" or skill.cost != 0:
            if skillToolTip != "":
                skillToolTip += "\n"

        skillToolTip += skillDes

        if skill.skillType == "Healing" or skill.skillType == "HealingEP" or skill.skillType == "HealingSP":
            damageEstimate = getHealingEstimate(player, skill)
            if damageEstimate != 0:
                skillToolTip += "\n{color=#7DF}Estimated Healing: " + str(damageEstimate) + "{/color}"

        wasattack = 0
        if skill.skillType == "attack":
            wasattack = 1
            damageEstimate = getDamageEstimate(player, skill)
            for each in player.statusEffects.tempAtk:
                if each.duration > 0:
                    damageEstimate *= (each.potency*0.01) + 1
            damageEstimate *= getTotalBoost(player, skill)
            damageEstimate = math.floor(damageEstimate)
            damageEstimate = int(damageEstimate)

            skillToolTip += "\n{color=#F7B}Estimated Arousal: " + str(damageEstimate) + "{/color}"


        if skill.statusEffect == "Damage" or skill.statusEffect == "Defence" or skill.statusEffect == "Crit" or skill.statusEffect == "Power" or skill.statusEffect == "Technique" or skill.statusEffect == "Intelligence" or skill.statusEffect == "Willpower" or skill.statusEffect == "Allure" or skill.statusEffect == "Luck" or skill.statusEffect == "%Power" or skill.statusEffect == "%Technique" or skill.statusEffect == "%Intelligence" or skill.statusEffect == "%Willpower" or skill.statusEffect == "%Allure" or skill.statusEffect == "%Luck":
            global buff
            buff = ""
            global postNote
            postNote =""

            damageEstimate = getBuffEstimate(player, skill)
            if skill.statusEffect == "Defence" or skill.statusEffect == "Damage"  or skill.statusEffect == "Crit"  or skill.statusEffect[0] == "%":
                postNote = "%"
            if skill.statusPotency >= 0:
                buff = "Buff: "
                wasattack = 2
            else:
                buff = "Debuff: "
                wasattack = 1
            if buff == "Buff: ":
                if postNote =="":
                    skillToolTip += "\n{color=#7DF}Estimated " + skill.statusEffect +" Buff: " + str(damageEstimate) + "{/color}"
                else:
                    skillToolTip += "\n{color=#7DF}Estimated " + skill.statusEffect +" Buff: " + str(damageEstimate) + "[postNote]{/color}"
            else:
                if postNote =="":
                    skillToolTip += "\n{color=#F7B}Estimated " + skill.statusEffect +" [buff]" + str(damageEstimate) + "{/color}"
                else:
                    skillToolTip += "\n{color=#F7B}Estimated " + skill.statusEffect +" [buff]" + str(damageEstimate) + "[postNote]{/color}"

        if skill.statusEffect != "" and skill.statusEffect != "none" and skill.statusEffect != "None" and skill.statusEffect != "Analyze":
            damageEstimate = 0
            relatedStat = player.stats.getStat(skill.statType)
            try:
                scaling = skill.statusEffectScaling*0.01
            except:
                scaling = 1

            damageEstimate = getStatusEffectChance(skill.statusChance, player, player, skill)
            damageEstimate = math.floor(damageEstimate)
            damageEstimate = int(damageEstimate)
            if damageEstimate != 0:
                if wasattack == 1:
                    skillToolTip += "\n{color=#F7B}Status Effect Chance: " + str(damageEstimate) + "%{/color}"
                elif wasattack == 0:
                    skillToolTip += "\n{color=#F7B}Status Effect Chance: " + str(damageEstimate) + "%{/color}"
            if skill.statusEffect == "Aphrodisiac":
                damageEstimate = 0
                damageEstimate = skill.statusPotency
                damageEstimate = math.floor(damageEstimate)
                damageEstimate = int(damageEstimate)
                if damageEstimate != 0:
                    skillToolTip += "\n{color=#F7B}Aphrodisiac Potency: " + str(damageEstimate) + "{/color}"
            if skill.statusEffect == "Aphrodisiac" or skill.statusEffect == "Charm" or skill.statusEffect == "Stun" or skill.statusEffect == "Damage" or skill.statusEffect == "Defence" or skill.statusEffect == "Crit" or skill.statusEffect == "Power" or skill.statusEffect == "Technique" or skill.statusEffect == "Intelligence" or skill.statusEffect == "Willpower" or skill.statusEffect == "Allure" or skill.statusEffect == "Luck" or skill.statusEffect == "%Power" or skill.statusEffect == "%Technique" or skill.statusEffect == "%Intelligence" or skill.statusEffect == "%Willpower" or skill.statusEffect == "%Allure" or skill.statusEffect == "%Luck":
                estimatedDuration = statusEffectDuration(skill.statusDuration, player)-1
                if damageEstimate != 0:
                    skillToolTip += "  Effect Duration: " + str(estimatedDuration) + " turns."
            if skill.statusEffect == "Restrain":
                damageEstimate = 0
                restraintBoost = 1.0
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "RestraintBoost":
                            restraintBoost += perk.EffectPower[p]*0.01
                        p += 1
                damageEstimate = (statusEffectDuration(skill.statusPotency, player, 1) + (relatedStat*scaling))*restraintBoost
                damageEstimate = math.floor(damageEstimate)
                damageEstimate = int(damageEstimate)
                if damageEstimate != 0:
                    skillToolTip += "\n{color=#F7B}Restraint Potency: " + str(damageEstimate) + "{/color} (5 = one turn on avg.)"
            if skill.statusEffect == "Sleep":
                damageEstimate = 0
                damageEstimate = skill.statusPotency
                damageEstimate = math.floor(damageEstimate)
                damageEstimate = int(damageEstimate)
                if damageEstimate != 0:
                    skillToolTip += "\n{color=#F7B}Sleep Potency: " + str(damageEstimate) + "{/color} (Drains this much energy per turn from the monster.)"

        return skillToolTip



    # Build a list of MenuItemDefs for usable items
    def cmenu_getItemList():
        arr = []

        for i, item in enumerate(player.inventory.items):
            if item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable":
                display = item.name + " (" + str(item.NumberHeld) + ")"

                if len(item.skills) > 0:
                    fetchSkill = getFromName(item.skills[0], SkillsDatabase)
                    skillToCheck = copy.deepcopy(SkillsDatabase[fetchSkill])
                    usable = skillIsUsable(skillToCheck)

                    itemToolTip = getSkillToolTip(skillToCheck, player, item.descrips)
                else:
                    usable = True
                    itemToolTip = item.descrips


                arr.append(MenuItemDef(name=display, tooltip=itemToolTip, setVar="ItemNumber", setValue=i+1, jumpTo="combatItemChoice", sensitiveIf=usable, usedFilterType="Item", rawName=item.name))

        return arr



    # Build a list of MenuItemDefs for monsters in the encounter
    def cmenu_getPushMonList():
        arr = []

        for i, mon in enumerate(monsterEncounter):
            name = mon.name

            if len(mon.combatStance) == 1 and mon.combatStance[0].Stance != "None":
                stanceName = mon.combatStance[0].Stance
                arr.append(MenuItemDef(name=name, tooltip="Try to remove the " + stanceName + " stance with " + name + ".", setVar="target", setValue=i, jumpTo="combatPushAway", sensitiveIf="player.statusEffects.charmed.duration <= 0"))

            elif len(mon.combatStance) > 1:
                arr.append(MenuItemDef(name=name, tooltip="Try to remove stances with " + name + ".", setVar="target", setValue=i, openSubMenu="Push", sensitiveIf="player.statusEffects.charmed.duration <= 0"))

            else:
                arr.append(MenuItemDef(name=name, tooltip="No stances with " + name + ".", sensitiveIf=False))
        return arr



    # Build a list of MenuItemDefs to stances to break out of
    def cmenu_getPushList():
        arr = []

        for sti, stance in enumerate(monsterEncounter[target].combatStance):
            name = stance.Stance
            arr.append(MenuItemDef(name=name, tooltip="Try to remove the " + name + " stance with the target.", setVar="tryRemoveThisStance", setValue=sti, jumpTo="removeThisStanceStances"))

        arr.append(MenuItemDef(name="All stances", tooltip="Try to remove all stances with target.", jumpTo="removeAllStances"))
        return arr



    # Reset the menu to a blank state
    def cmenu_resetMenu():
        del cmenu_columns[:]
        del cmenu_breadcrumb[:]
        cmenu_tooltip = ""

    def cmenu_refreshMenu():
        if len(cmenu_columns) >= 3:
            for each in cmenu_columns[1]:
                breadcrumb = 1 < len(cmenu_breadcrumb) and cmenu_breadcrumb[1] == each.name

            cmenu_setColumn(2, "SkillList", breadcrumb)
        elif len(cmenu_columns) == 2 and cmenu_breadcrumb[0] == "Other":
            breadcrumb = "Other"
            cmenu_setColumn(1, "Surrender", breadcrumb)
        elif len(cmenu_columns) == 2 and cmenu_breadcrumb[0] == "Items":
            breadcrumb = "Items"
            cmenu_setColumn(1, "Items", breadcrumb)

        else:
            cmenu_resetMenu()

    def cmenu_refreshSwapMenu():
        if len(cmenu_columns) >= 2:
            for each in cmenu_columns[0]:
                breadcrumb = 0 < len(cmenu_breadcrumb) and cmenu_breadcrumb[0] == each.name

            cmenu_setColumn(1, "SkillList", breadcrumb)

    # Handle a condition that can either be a string containing Python code or an actual boolean (durrr)
    def cmenu_eval(foo):
        try:
            return renpy.python.py_eval(foo)
        except:
            if (foo):
                return True;
            else:
                return False;



    # GUI stuff
    if renpy.variant("touch"):
        cmenu_col_width = 260
    else:
        cmenu_col_width = 220
    cmenu_col_height = 235
    if renpy.variant("touch"):
        cmenu_xpos = gui.dialogue_xpos - 10
    else:
        cmenu_xpos = gui.dialogue_xpos - 2
    cmenu_ypos = 825

    cmenu_tooltip = ""
    cmenu_showHealthTooltip = False


# Rotate the HP bar after cropping
transform rotateHP:
    xanchor 0.0
    yanchor 0.0
    rotate -32
    zoom 0.8

# Rotate the MP bar after cropping
transform rotateMP:
    xanchor 0.0
    yanchor 0.0
    rotate -148
    zoom 0.8

# Rotate the AP text to fit against the bar
transform rotateAPText:
    xanchor 0.0
    yanchor 0.0
    rotate 8

# Rotate the EP text to fit against the bar
transform rotateEPText:
    xanchor 0.0
    yanchor 0.0
    rotate -8

# Rotate the EP text to fit against the bar
transform rotateSPText:
    xanchor 0.0
    yanchor 0.0
    rotate -17

# Health display! Replaces the health bar, uses cropped/rotated HP bars in addition to a text readout
screen ON_HealthDisplay(mainMenu=False):
    zorder 100

    fixed:
        ypos 670
        use ON_HealthDisplayInner(mainMenu, xOffset=961)
        #700 is ypos

    # Add status effects over player icon
    use StatusBar(player) #it's in on_enemyCardScreen.rpy
    use ON_CombatMenuTooltip

screen ON_HealthDisplayBacking():
    zorder 0
    add "gui/playerbackUnderSide.png" xpos 0 ypos 660-10 # Add a second bg img in case textbox.png gets hidden

screen ON_HealthDisplayInner(mainMenu=False, xOffset=0, menuCall = 0):
    zorder 100
    if not mainMenu:
        add "gui/playerback.png" xpos xOffset-960 ypos -15 # Add a second bg img in case textbox.png gets hidden
    else:
        add "gui/healthBackTotal.png" xpos xOffset-960 ypos -15
    # Calculate AP and EP percents for cropping
    $ player.stats.Update()
    $ AP_Pct = max(0, float(player.stats.hp)/player.stats.max_true_hp)
    $ EP_Pct = max(0, float(player.stats.ep)/player.stats.max_true_ep)

    $ AP_crop = int(37 + (AP_Pct*225))
    $ EP_crop = int(37 + (EP_Pct*225))

    #default showHealthTooltip = False

    # Add AP and EP bars and overlays
    fixed:
        xsize 270
        ysize 270
        add "gui/HP.png" crop (270-AP_crop, 0, AP_crop, 270) xpos 270-AP_crop
        add "gui/HPBar.png"
        at rotateHP
        xpos xOffset-280
        ypos -85
    fixed:
        xsize 270
        ysize 270
        add "gui/MP.png" crop (270-EP_crop, 0, EP_crop, 270) xpos 270-EP_crop
        add "gui/MPBar.png"
        at rotateMP
        xpos xOffset-28
        ypos -85

    fixed:
        xsize 200
        ysize 24
        text "{color=#ff587d}[player.stats.hp]/[player.stats.max_true_hp]{/color}" size 28 xalign 1.0
        at rotateAPText
        xpos xOffset-284
        ypos -75
    fixed:
        xsize 200
        ysize 24
        text "{color=#4BF}[player.stats.ep]/[player.stats.max_true_ep]{/color}" size 28
        at rotateEPText
        xpos xOffset+84
        ypos -75

    $ spiritHeight = 16
    if player.stats.max_true_sp > 0:
        $ spiritPct = player.stats.sp/(player.stats.max_true_sp+0.0)
    else:
        $ spiritPct = 0
    $ SPCropHeight = int(spiritPct*67)
    $ SPCropStart = 79 - SPCropHeight

    imagebutton:
        idle "gui/SpiritBack.png"
        hover "gui/SpiritBack.png"
        xcenter xOffset
        ypos spiritHeight
        hovered SetVariable("cmenu_showHealthTooltip", True)
        unhovered SetVariable("cmenu_showHealthTooltip", False)
        if MenuLineSceneCheckMark == -1 and mainMenu == False and inTownMenu == 0 and npcCount == 0  and senCount == 0 and fetCount == 0:
            action renpy.curry(renpy.end_interaction)(True)
        else:
            action [SelectedIf(False), NullAction()] #make hoverable
    add "gui/SpiritFill.png" crop(0, SPCropStart, 96, SPCropHeight+12) xcenter xOffset ypos spiritHeight+SPCropStart


    if cmenu_showHealthTooltip:
        text "{color=#DFD}[player.stats.sp]/[player.stats.max_true_sp]{/color}" size 25 xcenter xOffset ypos spiritHeight+30
    else:
        text "{color=#DFD}[player.stats.sp]{/color}" size 27 xcenter xOffset ypos spiritHeight+30

    # Add status effects over player icon
    use StatusBar(player, 1, menuCall) #it's in on_enemyCardScreen.rpy




# Screen containing list of enemy cards
screen ON_EnemyCardScreen:

    $ alternating = 1
    $ xAdjustBase = -0.22
    if len(monsterEncounter) == 2:
        $ xAdjustBase = 0.15
    elif len(monsterEncounter) > 3:
        $ xAdjustBase =-0.27

    if hidingCombatEncounter == 0:
        for mC, mon in reversed(list(enumerate(monsterEncounter))):
            $ placement = PlacementFunction(mC, monsterEncounter, xAdjustBase, alternating)

            use EnemyCard(mC, mon, placement[0], placement[1])


# Tooltip screen for combat menu - not based on tt, but its own variable
screen ON_CombatMenuTooltip:
    zorder 100
    if cmenu_tooltip != "":
        $ combatChoice = getSkill("Caress", SkillsDatabase)
        $ caressEstimate = combatChoice.power + 1
        $ allureFlatScaling = 0.10
        $ allureFlatPercentBoost = 0

        python:
            for perk in player.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "BaselineAllureFlatBuff":
                        allureFlatScaling += perk.EffectPower[p]*0.01

                    if perk.PerkType[p] == "BaselineAllureFlatPercentBoost":
                        allureFlatScaling += perk.EffectPower[p]*0.01
                    p += 1
        $ caressEstimate += (combatChoice.power*((player.stats.Allure-5)*0.003 + allureFlatPercentBoost)) + ((player.stats.Allure-5)*allureFlatScaling)
        $ statDamMod = player.stats.lvl
        $ caressEstimate += ((statDamMod)*0.3)
        $ caressEstimate = math.floor(caressEstimate)
        $ caressEstimate = int(caressEstimate)
        frame:
            xpadding 11
            ypadding 6
            xpos 1110
            xsize 490
            ypos 818
            ysize 300
            xmaximum 600
            text cmenu_tooltip xsize 470 size 26


# Single menu item for combat menu
screen ON_MenuItem(i, depth, inMainMenu=False):

    python:
        global spaceNext
        # Is this the parent of an open submenu?
        breadcrumb = depth < len(cmenu_breadcrumb) and cmenu_breadcrumb[depth] == i.name

        # Otherwise, is this disabled (e.g. not enough EP)?
        disabled = (not cmenu_eval(i.sensitiveIf))

        skillType = player.skillList[getFromName(i.name, player.skillList)].skillType


        if (not i.openSubMenu and inMainMenu) and not (skillType == "Healing" or skillType == "HealingEP" or skillType == "HealingSP" or skillType == "StatusHeal"):
            disabled = True



        # cheap hack - if it supports a submenu, clamp it to the width
        # otherwise, give it tons of space (to support long skill/item names)
        # non-submenu options can overlap if another item in the same menu opens a submenu. May need tweaking
        width = cmenu_col_width-10 if i.openSubMenu else 500
        Sensitivechecker = skillIsUsable(player.skillList[getFromName(i.name, player.skillList)])

        OOcombatAvalible = player.skillList[getFromName(i.name, player.skillList)].statusOutcome
        if (not i.openSubMenu and inMainMenu) and OOcombatAvalible == "CombatOnly":
            disabled = True

        if manualSort == 1:
            disabled = False

    # Evaluate the showIf condition
    $ twolayeredskill = 0
    if spaceNext == 1:
        $ twolayeredskill += 27

    if len(i.name) > 28:
        $ spaceNext = 1


    if cmenu_eval(i.showIf):
        hbox:
            xsize width
            ysize on_cmenu_listEntryHeight + twolayeredskill
            button:
                hovered SetVariable("cmenu_tooltip", i.tooltip)
                if renpy.variant("touch"):
                    unhovered SetVariable("cmenu_tooltip", i.tooltip)
                else:
                    unhovered SetVariable("cmenu_tooltip", "")
                ysize on_cmenu_listEntryHeight
                text i.name:
                    size on_cmenu_listTextSize
                    ysize on_cmenu_listEntryHeight

                    # Style breadcrumb - all #fff
                    if breadcrumb:
                        idle_color "#fff"
                        hover_color "#fff"
                        insensitive_color "#fff"
                    # fake insensitivity on "disabled" buttons so tooltip is still usable
                    elif disabled:
                        idle_color gui.insensitive_color
                        hover_color gui.insensitive_color
                        insensitive_color gui.insensitive_color
                    # Style normal buttons with normal textbutton colors
                    else:
                        idle_color gui.idle_color
                        hover_color gui.hover_color
                        insensitive_color gui.insensitive_color

                    idle_color gui.idle_color
                    hover_color gui.hover_color
                    insensitive_color ("#fff" if breadcrumb else gui.insensitive_color)

                # Breadcrumb items close their submenus when clicked
                if breadcrumb:
                    action If(disabled, false=[
                        SetVariable("cmenu_tooltip", ""),
                        tt.Action(""),
                        If(i.setVar, true=SetVariable(i.setVar, i.setValue)),
                        If(i.openSubMenu, true=Function(cmenu_setColumn, depth=(depth+1), name="None", bcrumb_name=i.name)),
                        If(i.jumpTo, true=[Function(cmenu_resetMenu), Jump(i.jumpTo)])
                        ], true=NullAction())

                # Else, if we're in the combat menu, do anything the MenuItemDef has defined
                elif not inMainMenu:
                    action If(disabled, false=[
                        SetVariable("cmenu_tooltip", ""),
                        If(i.setVar, true=SetVariable(i.setVar, i.setValue)),
                        If(i.openSubMenu, true=Function(cmenu_setColumn, depth=(depth+1), name=i.openSubMenu, bcrumb_name=i.name)),
                        If(i.jumpTo, true=[ Jump(i.jumpTo)])
                        ], true=NullAction())

                # Else, show tooltips, use healing skills from menu
                else:
                    if renpy.variant("touch"):
                        hovered SetScreenVariable("characterMenuTooltip", i.tooltip)
                        unhovered SetScreenVariable("characterMenuTooltip", i.tooltip)
                    else:
                        hovered If(characterMenuCanHover, true=[SetScreenVariable("characterMenuTooltip", i.tooltip)], false=[SetScreenVariable("characterMenuCanHover", True)])
                        unhovered If(characterMenuCanHover, true=[SetScreenVariable("characterMenuTooltip", "")], false=NullAction())
                    if i.openSubMenu:
                        action [If(i.setVar, true=SetVariable(i.setVar, i.setValue)),
                            Function(cmenu_setColumn, depth=(depth+1), name=i.openSubMenu, bcrumb_name=i.name)]
                    else:
                        if manualSort == 0:
                            action [SensitiveIf(Sensitivechecker), SetVariable ("useSkill", 1), SetVariable ("skillTarget", getFromName(i.name, player.skillList))]
                        elif manualSort == 1:
                            action [SetVariable ("skillTarget", getFromName(i.name, player.skillList)), Jump("SetSkillOrder")]
                # Show arrow only when hovered or breadcrumb, if there's a submenu
                if i.openSubMenu and not disabled:
                    text "►":
                        if breadcrumb:
                            idle_color "#fff"
                            hover_color "#fff"
                            insensitive_color "#fff"
                        else:
                            idle_color "#00000000" # hide when idle
                            idle_outlines [] # hide outlines when idle
                            insensitive_color "#00000000"
                            insensitive_outlines []
                            hover_color gui.hover_color
                        size on_cmenu_listTextSize - 6
                        if renpy.variant("touch"):
                            xalign 0.9
                        else:
                            xalign 1.0
                        yoffset 2


# Master screen for combat menu
screen ON_CombatMenu:
    python:
        # make sure columns[0] is the main list
        if len(cmenu_columns) == 0:
            cmenu_columns.insert(0, cmenu_main)
        else:
            cmenu_columns[0] = cmenu_main

        # Or the struggle list if we're restrained (giggity)
        if player.statusEffects.restrained.duration > 0:
            if len(cmenu_columns) == 0:
                cmenu_columns.insert(0, cmenu_main)
            cmenu_columns[0] = cmenu_struggle

    # Add the Say textbox since we use its area for the menu
    add "gui/textbox.png" xalign 0.5 yalign 1.0

    # Display each column in a scrollbox
    $ spaceNext = 0
    for i, col in enumerate(cmenu_columns):
        $ x = cmenu_xpos + i*cmenu_col_width

        fixed:
            xpos x
            ypos cmenu_ypos
            ysize cmenu_col_height
            use ON_Scrollbox(leftBar=True, hideBar=False):
                for it in col:
                    use ON_MenuItem(it, i)

    # Display the tooltip
    #use ON_CombatMenuTooltip


screen returnButton:
    frame: ##Return button
        xpadding theXpadding
        ypadding theYpadding
        xalign 0.5
        yalign 0.82
        xminimum buttonWidth
        xmaximum buttonWidth
        ymaximum 10
        text "Pick your target.":
            xalign 0.5
            yalign 2.0
        imagebutton:
            idle "textButton.png"
            hover "textButton_hovered.png"
            insensitive "textButton_insensitive.png"
            xalign 0.5
            yalign 0.5
            action Jump("combatPlayer")
        text "Return":
            xalign 0.5
            yalign 0.5

#basically a depreciated bit of code that's still kicking around from when i was first made a weak ass image system. Need to remove it from the game at some point, and the picture bit from scenes.
screen DisplayLossImage:
    frame:
        xpadding theXpadding
        ypadding theYpadding
        xalign 0.5
        yalign 0.5
        imagebutton:
            idle extension
            hover extension
            insensitive extension
            at LossSceneZoom

# Copy of the combat menu for use in the "Skills" section of the character screen.
# The columns and breadcrumb arrays are shared with the real combat menu,
# so they should be reset whenever either menu is shown
screen ON_MenuSkillsList(height=230, xoff=0):
    # First entry is skills rather than main
    python:
        if len(cmenu_columns) == 0:
            cmenu_columns.insert(0, cmenu_skills)
        else:
            cmenu_columns[0] = cmenu_skills
    $ spaceNext = 0
    for i, col in enumerate(cmenu_columns):
        $ x = i*cmenu_col_width

        fixed:
            xoffset xoff
            xpos x
            ysize height
            use ON_Scrollbox(leftBar=True, hideBar=False):
                for it in col:
                    use ON_MenuItem(it, i, inMainMenu=True)
