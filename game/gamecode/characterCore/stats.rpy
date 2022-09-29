
init python:
    class CombatStance(renpy.store.object):
        def __init__(self, Stance="None", potency=0):
            self.Stance = Stance
            self.potency=potency
            self.WithWho = "None"

        def giveStance(self, Stance):
            if Stance != "":
                self.Stance = Stance

        def clearStance():
            self.Stance = "None"
            self.WithWho = "None"
            self.potency = 0


    class StatusEffect:
        def __init__(self, duration=-1, potency=0, skillText="based"):
            self.duration = duration
            self.potency = potency #when applicable
            self.skillText = skillText

    class StatusEffects:
        def __init__(self, defend=StatusEffect(), stunned=StatusEffect(), charmed=StatusEffect(),
        aphrodisiac=StatusEffect(), restrained=StatusEffect(), sleep=StatusEffect(), surrender=StatusEffect(),
        trance=StatusEffect(), fascinated=StatusEffect(), confusion=StatusEffect(), paralysis=StatusEffect(), ahegao=StatusEffect()):
            self.defend = defend
            self.stunned = stunned #stunned, unable act
            self.charmed = charmed #charmed targets take extra damage, cant defend, run or use magic or items
            self.aphrodisiac = aphrodisiac #damage per turn
            self.restrained = restrained #pinned, tied up ext, small number of actions,
            self.sleep = sleep #cant act and unaware of whats happening
            self.surrender = surrender #player gave up, lower stats and skip turn
            self.trance = trance #must obey....
            self.fascinated = fascinated #must fuck!
            self.confusion= confusion #picks random actions
            self.paralysis = paralysis #might be the same as stunned?
            self.ahegao = ahegao #fucked silly

            self.tempAtk = [StatusEffect()]
            self.tempDefence = [StatusEffect()]

            self.tempPower = [StatusEffect()]
            self.tempTech = [StatusEffect()]
            self.tempInt = [StatusEffect()]
            self.tempWillpower = [StatusEffect()]
            self.tempAllure = [StatusEffect()]
            self.tempLuck = [StatusEffect()]

            self.tempCrit = [StatusEffect()]

        def Update(self):

            try:
                self.paralysis
            except AttributeError:
                setattr(self, 'paralysis', StatusEffect())

            try:
                self.tempAtk
            except AttributeError:
                setattr(self, 'tempAtk', [StatusEffect()])
                setattr(self, 'tempDefence', [StatusEffect()])
                setattr(self, 'tempPower', [StatusEffect()])
                setattr(self, 'tempTech', [StatusEffect()])
                setattr(self, 'tempInt', [StatusEffect()])
                setattr(self, 'tempWillpower', [StatusEffect()])
                setattr(self, 'tempAllure', [StatusEffect()])
                setattr(self, 'tempLuck', [StatusEffect()])
                setattr(self, 'tempCrit', [StatusEffect()])
            try:
                self.tempInt
            except AttributeError:
                setattr(self, 'tempInt', [StatusEffect()])


            return

        def hasStatusEffect(self):
            if self.defend.duration > 0:
                return True
            if self.stunned.duration > 0:
                return True
            if self.charmed.duration > 0:
                return True
            if self.aphrodisiac.duration > 0:
                return True
            if self.restrained.duration > 0:
                return True
            if self.sleep.duration > 0:
                return True

            if self.surrender.duration > 0:
                return True
            if self.trance.duration > 0:
                return True
            if self.fascinated.duration > 0:
                return True
            if self.confusion.duration > 0:
                return True
            if self.paralysis.duration > 0:
                return True
            if self.ahegao.duration > 0:
                return True

            for each in self.tempAtk:
                if each.duration > 0:
                    return True
            for each in self.tempDefence:
                if each.duration > 0:
                    return True
            for each in self.tempPower:
                if each.duration > 0:
                    return True
            for each in self.tempTech:
                if each.duration > 0:
                    return True
            try:
                self.tempInt
            except AttributeError:
                setattr(self, 'tempInt', [StatusEffect()])
            for each in self.tempInt:
                if each.duration > 0:
                    return True
            for each in self.tempWillpower:
                if each.duration > 0:
                    return True
            for each in self.tempAllure:
                if each.duration > 0:
                    return True
            for each in self.tempLuck:
                if each.duration > 0:
                    return True
            for each in self.tempCrit:
                if each.duration > 0:
                    return True


            return False


        def hasThisStatusEffect(self, Name):
            if Name == "Surrender":
                if self.surrender.duration > 0:
                    return True

            if Name == "Defend":
                if self.defend.duration > 0:
                    return True
            if Name == "Stun":
                if self.stunned.duration > 0:
                    return True
            if Name == "Charm":
                if self.charmed.duration > 0:
                    return True
            if Name == "Aphrodisiac":
                if self.aphrodisiac.duration > 0:
                    return True
            if Name == "Restrain":
                if self.restrained.duration > 0:
                    return True
            if Name == "Drowsy":
                if self.sleep.potency != -99 and self.sleep.duration > 0:
                    return True
            if Name == "Sleep":
                if self.sleep.potency == -99:
                    return True

            if Name == "Paralysis":
                if self.paralysis.potency <= 9 and self.paralysis.duration > 0:
                    return True
            if Name == "Paralyzed":
                if self.paralysis.potency >= 10 and self.paralysis.duration > 0:
                    return True


            if Name == "Trance":
                if self.trance.potency >= 1:
                    return True
            if Name == "Hypnotized":
                if self.trance.potency >= 11:
                    return True

            if Name == "Damage":
                for each in self.tempAtk:
                    if each.duration > 0:
                        return True
            if Name == "Defence":
                for each in self.tempDefence:
                    if each.duration > 0:
                        return True
            if Name == "Power":
                for each in self.tempPower:
                    if each.duration > 0:
                        return True
            if Name == "Technique":
                for each in self.tempTech:
                    if each.duration > 0:
                        return True
            if Name == "Intelligence":
                for each in self.tempInt:
                    if each.duration > 0:
                        return True
            if Name == "Willpower":
                for each in self.tempWillpower:
                    if each.duration > 0:
                        return True
            if Name == "Allure":
                for each in self.tempAllure:
                    if each.duration > 0:
                        return True
            if Name == "Luck":
                for each in self.tempLuck:
                    if each.duration > 0:
                        return True
            if Name == "Crit":
                for each in self.tempCrit:
                    if each.duration > 0:
                        return True

            return False

        def hasThisStatusEffectPotency(self, Name, Potency):
            inverse = 1
            if Potency < 0:
                inverse = -1

            if Name == "Defend":
                if self.defend.duration > 0 and self.defend.potency >= Potency:
                    return True
            if Name == "Stun":
                if self.stunned.duration > 0  and self.stunned.potency >= Potency:
                    return True
            if Name == "Charm":
                if self.charmed.duration > 0  and self.charmed.potency >= Potency:
                    return True
            if Name == "Aphrodisiac":
                if self.aphrodisiac.duration > 0  and self.aphrodisiac.potency >= Potency:
                    return True
            if Name == "Restrain":
                if self.restrained.duration > 0 and self.restrained.potency >= Potency:
                    return True
            if Name == "Sleep":
                if self.sleep.duration > 0 and self.sleep.potency >= Potency:
                    return True

            if Name == "Trance":
                if self.trance.potency >= Potency:
                    return True

            if Name == "Paralysis":
                if self.paralysis.duration > 0 and self.paralysis.potency >= Potency:
                    return True


            if Name == "Damage":
                for each in self.tempAtk:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Defence":
                for each in self.tempDefence:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Power":
                for each in self.tempPower:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Technique":
                for each in self.tempTech:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Intelligence":
                for each in self.tempInt:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Willpower":
                for each in self.tempWillpower:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Allure":
                for each in self.tempAllure:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Luck":
                for each in self.tempLuck:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True
            if Name == "Crit":
                for each in self.tempCrit:
                    if each.duration > 0 and inverse*each.potency >= Potency:
                        return True

            return False


        def refresh(self, selfAgain):
            self.defend.duration = -1
            self.defend.potency = 0
            self.stunned.duration = -1
            self.charmed.duration = -1
            self.aphrodisiac.duration = -1
            self.aphrodisiac.potency = 0
            self.restrained.duration = 0
            self.surrender.duration = 0

            selfAgain.restraintStruggle = [""]
            selfAgain.restraintStruggleCharmed=[""]
            selfAgain.restraintEscaped = [""]
            selfAgain.restraintEscapedFail = [""]


            self.sleep.duration = -1
            self.sleep.potency = 0

            self.paralysis.duration = 0
            self.paralysis.potency = 0

            self.trance.duration = 0
            self.trance.potency = 0


            for each in self.tempPower:
                if each.potency != 0:
                    selfAgain.stats.Power -= each.potency
            for each in self.tempTech:
                if each.potency != 0:
                    selfAgain.stats.Tech -= each.potency
            for each in self.tempWillpower:
                if each.potency != 0:
                    selfAgain.stats.Willpower -= each.potency
            for each in self.tempInt:
                if each.potency != 0:
                    selfAgain.stats.Int -= each.potency
            for each in self.tempAllure:
                if each.potency != 0:
                    selfAgain.stats.Allure -= each.potency
            for each in self.tempLuck:
                if each.potency != 0:
                    selfAgain.stats.Luck -= each.potency



            self.tempAtk = [StatusEffect()]
            self.tempDefence = [StatusEffect()]

            self.tempPower= [StatusEffect()]
            self.tempTech= [StatusEffect()]
            self.tempWillpower= [StatusEffect()]
            self.tempInt= [StatusEffect()]
            self.tempAllure= [StatusEffect()]
            self.tempLuck = [StatusEffect()]

            self.tempCrit = [StatusEffect()]

            for perk in selfAgain.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RemovablePersistantEffect":
                        selfAgain.giveOrTakePerk(perk.name, -1)
                    p += 1

            return selfAgain

        def refreshNegative(self, selfAgain):
            self.stunned.duration = -1
            self.charmed.duration = -1
            self.aphrodisiac.duration = -1
            self.aphrodisiac.potency = 0
            self.sleep.duration = 0
            self.sleep.potency = 0
            self.surrender.duration = 0
            self.trance.duration = 0
            self.trance.potency = 0
            self.paralysis.duration = 0
            self.paralysis.potency = 0

            s = 0
            while s < len(self.tempAtk):
                if self.tempAtk[s].potency < 0:
                    del self.tempAtk[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempDefence):
                if self.tempDefence[s].potency < 0:
                    del self.tempDefence[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempCrit):
                if self.tempCrit[s].potency < 0:
                    del self.tempCrit[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempPower):
                if self.tempPower[s].potency < 0:
                    selfAgain.stats.Power -= self.tempPower[s].potency
                    del self.tempPower[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempTech):
                if self.tempTech[s].potency < 0:
                    selfAgain.stats.Tech -= self.tempTech[s].potency
                    del self.tempTech[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempInt):
                if self.tempInt[s].potency < 0:
                    selfAgain.stats.Int -= self.tempInt[s].potency
                    del self.tempInt[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempWillpower):
                if self.tempWillpower[s].potency < 0:
                    selfAgain.stats.Willpower -= self.tempWillpower[s].potency
                    del self.tempWillpower[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempAllure):
                if self.tempAllure[s].potency < 0:
                    selfAgain.stats.Allure -= self.tempAllure[s].potency
                    del self.tempAllure[s]
                    s -= 1
                s += 1
            s = 0
            while s < len(self.tempLuck):
                if self.tempLuck[s].potency < 0:
                    selfAgain.stats.Luck -= self.tempLuck[s].potency
                    del self.tempLuck[s]
                    s -= 1
                s += 1


            for perk in selfAgain.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RemovableEffect":
                        selfAgain.giveOrTakePerk(perk.name, -1)
                    p += 1


            return selfAgain

        def refreshNonPersistant(self, selfAgain):
            self.defend.duration = -1
            self.defend.potency = 0
            self.stunned.duration = -1
            self.charmed.duration = -1
            self.restrained.duration = 0
            self.surrender.duration = 0
            self.sleep.duration = -1
            self.sleep.potency = 0


            selfAgain.restraintStruggle = [""]
            selfAgain.restraintStruggleCharmed= [""]
            selfAgain.restraintEscaped = [""]
            selfAgain.restraintEscapedFail = [""]

            self.tempAtk = [StatusEffect()]
            self.tempDefence = [StatusEffect()]

            self.tempCrit = [StatusEffect()]

            for each in self.tempPower:
                if each.potency != 0:
                    selfAgain.stats.Power -= each.potency
            for each in self.tempTech:
                if each.potency != 0:
                    selfAgain.stats.Tech -= each.potency
            for each in self.tempInt:
                if each.potency != 0:
                    selfAgain.stats.Int -= each.potency
            for each in self.tempWillpower:
                if each.potency != 0:
                    selfAgain.stats.Willpower -= each.potency
            for each in self.tempAllure:
                if each.potency != 0:
                    selfAgain.stats.Allure -= each.potency
            for each in self.tempLuck:
                if each.potency != 0:
                    selfAgain.stats.Luck -= each.potency

            self.tempPower = [StatusEffect()]
            self.tempTech = [StatusEffect()]
            self.tempInt = [StatusEffect()]
            self.tempWillpower = [StatusEffect()]
            self.tempAllure = [StatusEffect()]
            self.tempLuck = [StatusEffect()]

            for perk in selfAgain.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "RemovableEffect":
                        selfAgain.giveOrTakePerk(perk.name, -1)
                    p += 1

            return selfAgain

        def turnPass(self, being):
            self.defend.duration -= 1
            if self.stunned.duration > 0:
                self.stunned.duration -= 1
            elif self.stunned.duration <=-2:
                self.stunned.duration += 1
            if self.charmed.duration > 0:
                self.charmed.duration -= 1
            elif self.charmed.duration <=-2:
                self.charmed.duration += 1

            if self.restrained.duration < 0:
                self.restrained.duration += 1

            self.aphrodisiac.duration -= 1


            for perk in being.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "AphrodisiacTurnCure":
                        if being.statusEffects.aphrodisiac.potency > 0:
                            being.statusEffects.aphrodisiac.potency -= perk.EffectPower[p]
                            if being.statusEffects.aphrodisiac.potency <= 0:
                                being.statusEffects.aphrodisiac.potency = 0
                                being.statusEffects.aphrodisiac.duration = 0
                    p += 1

            #self.restrained.duration += 0

            if self.sleep.duration < -1:
                self.sleep.duration += 1
            elif self.sleep.duration > 0 and self.sleep.potency != -99:
                self.sleep.duration -= 1

            for each in self.tempAtk:
                each.duration -= 1
            for each in self.tempDefence:
                each.duration -= 1
            for each in self.tempCrit:
                each.duration -= 1


            for each in self.tempPower:
                each.duration -= 1
            for each in self.tempTech:
                each.duration -= 1
            for each in self.tempWillpower:
                each.duration -= 1
            for each in self.tempInt:
                each.duration -= 1
            for each in self.tempAllure:
                each.duration -= 1
            for each in self.tempLuck:
                each.duration -= 1

        def statusEnd(self, activePerson):
            displaying = ""
            if self.stunned.duration == 0:
                self.stunned.duration = -1
                CheckImmunity = getFromName("Stun Immune", activePerson.perks)
                if CheckImmunity == -1:
                    activePerson.giveOrTakePerk("Stun Immune", 1)
                else:
                    activePerson.giveOrTakePerk("Stun Immune", -1)
                    activePerson.giveOrTakePerk("Stun Immune", 1)
                for perkSI in activePerson.perks:
                    p = 0
                    while  p < len(perkSI.PerkType):
                        if perkSI.PerkType[p] == "StunDelay":
                            holda = changePerkDuration(activePerson, "Stun Immune", perkSI.EffectPower[p])
                            activePerson = holda[0]
                        p += 1
                displaying += activePerson.name + " is no longer stunned! "
            if self.charmed.duration == 0:
                self.charmed.duration = -1
                CheckImmunity = getFromName("Charm Immune", activePerson.perks)
                if CheckImmunity == -1:
                    activePerson.giveOrTakePerk("Charm Immune", 1)
                else:
                    activePerson.giveOrTakePerk("Charm Immune", -1)
                    activePerson.giveOrTakePerk("Charm Immune", 1)
                displaying += activePerson.name + " is no longer charmed! "
            if self.aphrodisiac.duration == 0:
                displaying += "The " + self.aphrodisiac.skillText + " running through " + activePerson.name + " wears off! "
            if self.aphrodisiac.duration <= 0:
                self.aphrodisiac.potency = 0

            if self.sleep.duration == 0 and self.sleep.potency != -99 and self.sleep.potency > 0:
                displaying += activePerson.name + " shakes off their drowsiness! "
                self.sleep.potency = 0
            if self.sleep.duration == 0 and self.sleep.potency == -99:
                displaying += activePerson.name + " wakes up! "
                self.sleep.potency = 0
                self.sleep.duration = -1
                #CheckImmunity = getFromName("Sleep Immune", activePerson.perks)
                #if CheckImmunity == -1:
                #    activePerson.giveOrTakePerk("Sleep Immune", 1)
                #else:
                #    activePerson.giveOrTakePerk("Sleep Immune", -1)
                #    activePerson.giveOrTakePerk("Sleep Immune", 1)
            s = 0
            for each in self.tempAtk:
                if each.duration <= 0:
                    del self.tempAtk[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempDefence:
                if each.duration <= 0:
                    del self.tempDefence[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempCrit:
                if each.duration <= 0:
                    del self.tempCrit[s]
                    s -= 1
                s += 1
            s = 0



            for each in self.tempPower:
                if each.duration <= 0:
                    activePerson.stats.Power -= each.potency
                    del self.tempPower[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempTech:
                if each.duration <= 0:
                    activePerson.stats.Tech -= each.potency
                    del self.tempTech[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempInt:
                if each.duration <= 0:
                    activePerson.stats.Int -= each.potency
                    del self.tempInt[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempWillpower:
                if each.duration <= 0:
                    activePerson.stats.Willpower -= each.potency
                    del self.tempWillpower[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempAllure:
                if each.duration <= 0:
                    activePerson.stats.Allure -= each.potency
                    del self.tempAllure[s]
                    s -= 1
                s += 1
            s = 0
            for each in self.tempLuck:
                if each.duration <= 0:
                    activePerson.stats.Luck -= each.potency
                    del self.tempLuck[s]
                    s -= 1
                s += 1
            return [displaying, activePerson]


    ####should prolly be moved into status effects class directly.###
    def removeThisStatusEffect(effect, character):
        if effect == "All":
            character = character.statusEffects.refreshNegative(character)
        if effect == "Aphrodisiac":
            character.statusEffects.aphrodisiac.duration = -1
            character.statusEffects.aphrodisiac.potency = 0
        if effect == "Charm":
            character.statusEffects.charmed.duration = -1
        if effect == "Sleep":
            character.statusEffects.sleep.duration = 0
            character.statusEffects.sleep.potency = 0
        if effect == "Trance":
            character.statusEffects.trance.potency = 0
            character.statusEffects.trance.duration = 0
        if effect == "Paralysis":
            character.statusEffects.paralysis.potency = 0
            character.statusEffects.paralysis.duration = 0
        if effect == "Stun":
            character.statusEffects.stunned.potency = 0
            character.statusEffects.stunned.duration = -1
        if effect == "Restrain":
            character.statusEffects.restrained.potency = 0
            character.statusEffects.restrained.duration = 0
        if effect == "Defend":
            character.statusEffects.defend.potency = 0
            character.statusEffects.defend.duration = -1
        if effect == "Surrender":
            character.statusEffects.surrender.potency = 0
            character.statusEffects.surrender.duration = 0


        if effect == "Damage":
            character.statusEffects.tempAtk = [StatusEffect()]
        if effect == "Defence":
            character.statusEffects.tempDefence = [StatusEffect()]
        if effect == "Power":
            for each in self.tempPower:
                if each.potency != 0:
                    selfAgain.stats.Power -= each.potency
            character.statusEffects.tempPower= [StatusEffect()]
        if effect == "Technique":
            for each in self.tempTech:
                if each.potency != 0:
                    selfAgain.stats.Tech -= each.potency
            character.statusEffects.tempTech= [StatusEffect()]
        if effect == "Intelligence":
            for each in self.tempInt:
                if each.potency != 0:
                    selfAgain.stats.Int -= each.potency
            character.statusEffects.tempInt= [StatusEffect()]
        if effect == "Willpower":
            for each in self.tempWillpower:
                if each.potency != 0:
                    selfAgain.stats.Willpower -= each.potency
            character.statusEffects.tempWillpower= [StatusEffect()]
        if effect == "Allure":
            for each in self.tempAllure:
                if each.potency != 0:
                    selfAgain.stats.Allure -= each.potency
            character.statusEffects.tempAllure= [StatusEffect()]
        if effect == "Luck":
            for each in self.tempLuck:
                if each.potency != 0:
                    selfAgain.stats.Luck -= each.potency
            character.statusEffects.tempLuck = [StatusEffect()]
        if effect == "Crit":
            character.statusEffects.tempCrit = [StatusEffect()]

        return character

    def isStatusEffect(Name):
        if Name == "Surrender":
            return True

        if Name == "Defend":
            return True
        if Name == "Stun":
            return True
        if Name == "Charm":
            return True
        if Name == "Aphrodisiac":
            return True
        if Name == "Restrain":
            return True
        if Name == "Drowsy":
            return True
        if Name == "Sleep":
            return True
        if Name == "Paralysis":
            return True
        if Name == "Paralyzed":
            return True


        if Name == "Trance":
            return True
        if Name == "Hypnotized":
            return True

        if Name == "Damage":
            return True
        if Name == "Defence":
            return True
        if Name == "Power":
            return True
        if Name == "Technique":
            return True
        if Name == "Intelligence":
            return True
        if Name == "Willpower":
            return True
        if Name == "Allure":
            return True
        if Name == "Luck":
            return True
        if Name == "Crit":
            return True

        return False

    class Skill:
        def __init__(self, name="blank", costDisplay="0",  costType="ep", skillType="attack", statType="", skillTags=[], fetishTags=[],
                        startsStance=[""], requiresStance="", unusableIfStance="", requiresTargetStance=[], unusableIfTarget=[], removesStance=[""], requiresStatusEffect="", requiresStatusPotency=0, unusableIfStatusEffect=[], requiresStatusEffectSelf="", requiresStatusPotencySelf=0, unusableIfStatusEffectSelf=[],
                        requiresPerk=[], requiresOnePerk=[], unusableIfPerk=[], requiresPerkSelf=[], requiresOnePerkSelf=[], unusableIfPerkSelf=[],
                        power=1, minRange=0, maxRange=0, recoil=0, critChance=0, critDamage=0,
                        targetType="single",  accuracy=0, initiative=0,
                        statusEffect="none", statusChance=0, statusDuration=0, statusPotency=0, statusResistedBy="", statusText= "",
                        descrips="", outcome="", miss="", statusOutcome="", statusMiss="", restraintStruggle=[""],  restraintStruggleCharmed=[""], restraintEscaped=[""], restraintEscapedFail=[""], restraintOnLoss=[""],
                        learningCost=0, requiredStat=0, requiredLevel=1, statusEffectScaling=100, scalesWithStatusScale="", flatSFFlatScaling=0, flatSFPercentScaling=0, totalSFPercentScaling=0, unusableIfTargetHasTheseSets=[], cost=0, isSkill="True"):
            self.name = name
            self.costDisplay = costDisplay
            self.cost = int(costDisplay) #energyCost
            self.costType = costType
            self.skillType = skillType
            self.statType = statType
            self.skillTags = skillTags
            self.fetishTags = fetishTags
            self.startsStance = startsStance
            self.requiresStance = requiresStance
            self.unusableIfStance = unusableIfStance
            self.requiresTargetStance = requiresTargetStance
            self.unusableIfTarget = unusableIfTarget
            self.removesStance = removesStance
            self.requiresStatusEffect = requiresStatusEffect
            self.requiresStatusPotency = requiresStatusPotency
            self.unusableIfStatusEffect = unusableIfStatusEffect
            self.requiresStatusEffectSelf = requiresStatusEffectSelf
            self.requiresStatusPotencySelf = requiresStatusPotencySelf
            self.unusableIfStatusEffectSelf = unusableIfStatusEffectSelf

            self.requiresPerk=requiresPerk
            self.requiresOnePerk=requiresOnePerk
            self.unusableIfPerk=unusableIfPerk
            self.requiresPerkSelf=requiresPerkSelf
            self.requiresOnePerkSelf=requiresOnePerkSelf
            self.unusableIfPerkSelf=unusableIfPerkSelf

            self.power = power
            self.minRange = minRange #0.7
            self.maxRange = maxRange #1.3
            self.critChance = critChance
            self.critDamage = critDamage
            self.targetType = targetType # "single"
            self.accuracy = accuracy
            self.initiative = initiative
            self.statusEffect = statusEffect
            self.statusChance = statusChance
            self.statusDuration = statusDuration
            self.statusPotency = statusPotency
            self.statusResistedBy = statusResistedBy
            self.statusText = statusText
            self.descrips = descrips #text
            self.outcome = outcome #text
            self.miss = miss #text
            self.statusOutcome = statusOutcome #text
            self.statusMiss = statusMiss #text
            self.isSkill = isSkill
            self.learningCost = learningCost
            self.requiredStat = requiredStat
            self.requiredLevel = requiredLevel
            self.recoil = recoil
            self.restraintStruggle = restraintStruggle
            self.restraintStruggleCharmed = restraintStruggleCharmed
            self.restraintEscaped = restraintEscaped
            self.restraintEscapedFail = restraintEscapedFail
            self.restraintOnLoss = restraintOnLoss
            self.statusEffectScaling = statusEffectScaling


            self.scalesWithStatusScale = scalesWithStatusScale
            self.flatSFFlatScaling = flatSFFlatScaling
            self.flatSFPercentScaling = flatSFPercentScaling
            self.totalSFPercentScaling = totalSFPercentScaling

            self.unusableIfTargetHasTheseSets =unusableIfTargetHasTheseSets


        def __ne__(self, other):
            equal = 1
            equal = self.Compare(self.costDisplay, other.costDisplay, equal)
            equal = self.Compare(self.cost, other.cost, equal)
            equal = self.Compare(self.costType, other.costType, equal)
            equal = self.Compare(self.statType, other.statType, equal)
            equal = self.CompareArray(self.skillTags, other.skillTags, equal)
            equal = self.CompareArray(self.fetishTags, other.fetishTags, equal)
            equal = self.Compare(self.startsStance, other.startsStance, equal)
            equal = self.Compare(self.requiresStance, other.requiresStance, equal)
            equal = self.CompareArray(self.unusableIfStance, other.unusableIfStance, equal)
            equal = self.CompareArray(self.requiresTargetStance, other.requiresTargetStance, equal)
            equal = self.CompareArray(self.unusableIfTarget, other.unusableIfTarget, equal)
            equal = self.Compare(self.removesStance, other.removesStance, equal)
            equal = self.Compare(self.requiresStatusEffect, other.requiresStatusEffect, equal)
            equal = self.Compare(self.requiresStatusPotency, other.requiresStatusPotency, equal)
            equal = self.CompareArray(self.unusableIfStatusEffect, other.unusableIfStatusEffect, equal)
            equal = self.Compare(self.requiresStatusEffectSelf, other.requiresStatusEffectSelf, equal)
            equal = self.Compare(self.requiresStatusPotencySelf, other.requiresStatusPotencySelf, equal)
            equal = self.CompareArray(self.unusableIfStatusEffectSelf, other.unusableIfStatusEffectSelf, equal)

            equal = self.CompareArray(self.requiresPerk, other.requiresPerk, equal)
            equal = self.CompareArray(self.requiresOnePerk, other.requiresOnePerk, equal)
            equal = self.CompareArray(self.unusableIfPerk, other.unusableIfPerk, equal)
            equal = self.CompareArray(self.requiresPerkSelf, other.requiresPerkSelf, equal)
            equal = self.CompareArray(self.requiresOnePerkSelf, other.requiresOnePerkSelf, equal)
            equal = self.CompareArray(self.unusableIfPerkSelf, other.unusableIfPerkSelf, equal)

            equal = self.Compare(self.power, other.power, equal)
            equal = self.Compare(self.minRange, other.minRange, equal)
            equal = self.Compare(self.maxRange, other.maxRange, equal)
            equal = self.Compare(self.targetType, other.targetType, equal)
            equal = self.Compare(self.statusEffect, other.statusEffect, equal)
            equal = self.Compare(self.statusChance, other.statusChance, equal)
            equal = self.Compare(self.statusDuration, other.statusDuration, equal)
            equal = self.Compare(self.statusPotency, other.statusPotency, equal)
            equal = self.Compare(self.statusResistedBy, other.statusResistedBy, equal)
            equal = self.Compare(self.statusText, other.statusText, equal)
            equal = self.Compare(self.descrips, other.descrips, equal)
            equal = self.Compare(self.outcome, other.outcome, equal)
            equal = self.Compare(self.miss, other.miss, equal)
            equal = self.Compare(self.statusOutcome, other.statusOutcome, equal)
            equal = self.Compare(self.statusMiss, other.statusMiss, equal)
            equal = self.Compare(self.isSkill, other.isSkill, equal)
            equal = self.Compare(self.learningCost, other.learningCost, equal)
            equal = self.Compare(self.requiredStat, other.requiredStat, equal)
            equal = self.Compare(self.requiredLevel, other.requiredLevel, equal)
            equal = self.Compare(self.recoil, other.recoil, equal)
            equal = self.Compare(self.restraintStruggle, other.restraintStruggle, equal)
            equal = self.Compare(self.restraintStruggleCharmed, other.restraintStruggleCharmed, equal)
            equal = self.Compare(self.restraintEscaped, other.restraintEscaped, equal)
            equal = self.Compare(self.restraintEscapedFail, other.restraintEscapedFail, equal)
            equal = self.Compare(self.statusEffectScaling, other.statusEffectScaling, equal)
            equal = self.Compare(self.scalesWithStatusScale, other.scalesWithStatusScale, equal)
            equal = self.Compare(self.flatSFFlatScaling, other.flatSFFlatScaling, equal)
            equal = self.Compare(self.flatSFPercentScaling, other.flatSFPercentScaling, equal)
            equal = self.Compare(self.totalSFPercentScaling, other.totalSFPercentScaling, equal)
            equal = self.CompareArray(self.unusableIfTargetHasTheseSets, other.unusableIfTargetHasTheseSets, equal)

            if equal == 0:
                return True
            else:
                return False
        def Compare(self, own, other, equal):
            if own != other or equal == 0:
                return 0
            return 1
        def CompareArray(self, own, other, equal):
            if len(own) != len(other) or equal == 0:
                return 0
            else:
                n = 0
                while n < len(own):
                    if own[n] != other[n] or equal == 0:
                        return 0
                    n += 1
            return 1
        
        def getActualFetishes(self, attacker):
            stancesByFetish = ptceConfig.get("fetishGain").get("stancesByFetish")
            fetishes = filter(lambda f: f != "Penetration", self.fetishTags)
            for fetish, stances in stancesByFetish.items():
                if self.requiresStance in stances or self.startsStance in stances:
                    if fetish not in fetishes:
                        fetishes.append(fetish)

            if attacker.getCurrentStanceNames() == None:
                return fetishes
            if "Penetration" in self.fetishTags:
                if "Sex" in attacker.getCurrentStanceNames():
                    if "Sex" not in fetishes:
                        fetishes.append("Sex")
                if "Anal" in attacker.getCurrentStanceNames():
                        fetish.append("Anal")
            return fetishes


    ####Should proly be in the actual skill class?####
    def addSkillTo(theName, addTo):
        dataTarget = getFromName(theName, SkillsDatabase)
        blankSkill = copy.deepcopy(SkillsDatabase[dataTarget])
        addTo.skillList.append(blankSkill)
    ####Should proly be in the actual skill class?####

    def getSkill(theName, fromTarget):
        dataTarget = getFromName(theName, fromTarget)
        blankSkill = SkillsDatabase[dataTarget]
        return blankSkill


    class Stats(renpy.store.object):
        def __init__(self, lvl=1, Exp=0, ExpNeeded=10,
                    max_hp=100, max_ep=50, max_sp=3,
                    Power=5, Tech=5, Int=5, Allure=5, Willpower=5, Luck=5, isPlayer="False"):
            self.Exp = Exp
            self.ExpNeeded = ExpNeeded
            self.lvl=lvl
            self.max_hp=max_hp
            self.hp=0
            self.max_ep=max_ep
            self.ep=max_ep
            self.max_sp=max_sp
            self.sp=max_sp
            self.Power = Power
            self.Tech = Tech
            self.Int = Int
            self.Allure = Allure
            self.Willpower = Willpower
            self.Luck = Luck
            self.isPlayer = isPlayer

            self.bonus_hp = 0
            self.bonus_ep = 0
            self.bonus_sp = 0

            self.max_true_hp = max_hp
            self.max_true_ep = max_ep
            self.max_true_sp = max_sp


        def getStat(self, statName):
            if statName == "Arousal":
                return self.max_true_hp
            if statName == "Energy":
                return self.max_true_ep
            if statName == "Spirit":
                return self.max_true_sp

            if statName == "CurrentArousal":
                return self.hp
            if statName == "CurrentEnergy":
                return self.ep
            if statName == "CurrentSpirit":
                return self.sp

            if statName == "Power":
                return self.Power
            if statName == "Technique":
                return self.Tech
            if statName == "Intelligence":
                return self.Int
            if statName == "Allure":
                return self.Allure
            if statName == "Willpower":
                return self.Willpower
            if statName == "Luck":
                return self.Luck

            return 0


        def refresh(self):
            self.sp = self.max_true_sp
            self.ep = self.max_true_ep
            self.hp = 0

        def increaseStat(self, stat):
            self.stat +=1

        def BarMinMax(self):
            #if self.hp >= self.max_hp:
                #self.hp = self.max_hp
            if self.hp <= 0:
                self.hp = 0
            if self.ep >= self.max_true_ep:
                self.ep = self.max_true_ep
            if self.ep <= 0:
                self.ep = 0
            if self.sp >= self.max_true_sp:
                self.sp = self.max_true_sp
            if self.sp <= 0:
                self.sp = 0

        def Update(self):
            try:
                self.Int
            except:
                setattr(self, 'Int', 5)
                setattr(self, 'bonus_hp', 0)
                setattr(self, 'bonus_ep', 0)
                setattr(self, 'bonus_sp', 0)
                setattr(self, 'max_true_hp', self.max_hp)
                setattr(self, 'max_true_ep', self.max_ep)
                setattr(self, 'max_true_sp', self.max_sp)

            return

    class BodySensitivity(renpy.store.object):
        def __init__(self, Sex=0, Ass=0, Breasts=0, Mouth=0, Seduction=0, Magic=0, Pain=0, Holy=0, Unholy=0):
            self.Sex = Sex
            self.Ass = Ass
            self.Breasts = Breasts
            self.Mouth = Mouth
            self.Seduction = Seduction
            self.Magic = Magic
            self.Pain = Pain
            self.Holy = Holy
            self.Unholy = Unholy


        def getRes(self, tagName):
            if tagName == "Sex":
                return self.Sex
            if tagName == "Ass":
                return self.Ass
            if tagName == "Breasts":
                return self.Breasts
            if tagName == "Mouth":
                return self.Mouth
            if tagName == "Seduction":
                return self.Seduction
            if tagName == "Magic":
                return self.Magic
            if tagName == "Pain":
                return self.Pain
            if tagName == "Holy":
                return self.Holy
            if tagName == "Unholy":
                return self.Unholy
            return -999

        def getResPName(self, tagName):
            if tagName == "Sex":
                return "Cock"
            if tagName == "Breasts":
                return "Nipple"
            return tagName

        def changeRes(self, tagName, amount):
            if tagName == "Sex":
                self.Sex += amount
            if tagName == "Ass":
                self.Ass += amount
            if tagName == "Breasts":
                self.Breasts += amount
            if tagName == "Mouth":
                self.Mouth += amount
            if tagName == "Seduction":
                self.Seduction += amount
            if tagName == "Magic":
                self.Magic += amount
            if tagName == "Pain":
                self.Pain += amount
            if tagName == "Holy":
                self.Holy += amount
            if tagName == "Unholy":
                self.Unholy += amount
            return

        def setRes(self, tagName, amount):
            if tagName == "Sex":
                self.Sex = amount
            if tagName == "Ass":
                self.Ass = amount
            if tagName == "Breasts":
                self.Breasts = amount
            if tagName == "Mouth":
                self.Mouth = amount
            if tagName == "Seduction":
                self.Seduction = amount
            if tagName == "Magic":
                self.Magic = amount
            if tagName == "Pain":
                self.Pain = amount
            if tagName == "Holy":
                self.Holy = amount
            if tagName == "Unholy":
                self.Unholy = amount
            return

        def getSensBonusReduction(self, target, typeText):
            global TempSensitivity
            TemporarySensCheck = target.inventory.RuneSlotOne.BodySensitivity.getRes(typeText) + target.inventory.RuneSlotTwo.BodySensitivity.getRes(typeText) + target.inventory.RuneSlotThree.BodySensitivity.getRes(typeText) + target.inventory.AccessorySlot.BodySensitivity.getRes(typeText) + TempSensitivity.getRes(typeText)

            typeText += "Sensitivity"
            for perk in target.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == typeText:
                        TemporarySensCheck += perk.EffectPower[p]
                    p += 1

            return TemporarySensCheck

        def resetSens(self, statToChange, target, statBase=100):

            actualStat = self.getRes(statToChange) - self.getSensBonusReduction(target, statToChange )
            statBase -= actualStat


            if statToChange == "Sex":
                target.SensitivityPoints += (statBase/5)*2
                self.Sex += statBase
            if statToChange == "Ass":
                target.SensitivityPoints += statBase/10
                self.Ass += statBase
            if statToChange == "Breasts":
                target.SensitivityPoints += statBase/25
                self.Breasts += statBase
            if statToChange == "Mouth":
                target.SensitivityPoints += statBase /10
                self.Mouth += statBase
            if statToChange == "Seduction":
                target.SensitivityPoints += statBase/10
                self.Seduction += statBase
            if statToChange == "Magic":
                target.SensitivityPoints += statBase/10
                self.Magic += statBase
            if statToChange == "Pain":
                target.SensitivityPoints += statBase/10
                self.Pain += statBase
            if statToChange == "Holy":
                target.SensitivityPoints += statBase/10
                self.Holy += statBase
            if statToChange == "Unholy":
                target.SensitivityPoints += statBase/10
                self.Unholy += statBase

            return

        def resetTempRes(self):
            self.Sex = 0
            self.Ass = 0
            self.Breasts = 0
            self.Mouth = 0
            self.Seduction = 0
            self.Magic = 0
            self.Pain = 0
            self.Holy = 0
            self.Unholy = 0
            return

        def creatorSetRes(self, stat, amount, mini, maxi, cost=1, tempRes=0, sensType=""):
            global tentativeStats, creating
            go = 0
            if stat-tempRes+amount >= mini and amount < 0:
                if tentativeStats.SensitivityPoints >= cost:
                    tentativeStats.SensitivityPoints -= cost
                    stat += amount
                    go = 1

            if respeccing == 0:
                tempRes = 0

            if stat+amount <= maxi+tempRes and amount > 0:
                tentativeStats.SensitivityPoints += cost
                stat += amount
                go = 1

            if sensType == "Sex":
                self.Sex = stat
            if sensType == "Ass":
                self.Ass = stat
            if sensType == "Breasts":
                self.Breasts = stat
            if sensType == "Mouth":
                self.Mouth = stat
            if sensType == "Seduction":
                self.Seduction = stat
            if sensType == "Magic":
                self.Magic = stat
            if sensType == "Pain":
                self.Pain = stat

            if go == 1:
                if amount < 0:
                    tentativeStats.pastLevelUpSens.append(copy.deepcopy(sensType))
                else:
                    foundRemoved = 0
                    tracker = len(tentativeStats.pastLevelUpSens) -1
                    tempList = copy.deepcopy(tentativeStats.pastLevelUpSens)
                    for each in tempList[::-1]:
                        if foundRemoved == 1:
                            break

                        if each == sensType:
                            del tentativeStats.pastLevelUpSens[tracker]
                            foundRemoved = 1
                            break

                        tracker -= 1

            return

    class ResistancesStatusEffects(renpy.store.object):
        def __init__(self, Stun=0, Charm=0, Aphrodisiac=0, Restraints=0, Sleep=0, Trance=0, Paralysis=0, Debuff=0):
            self.Stun = Stun
            self.Charm = Charm
            self.Aphrodisiac = Aphrodisiac
            self.Restraints = Restraints
            self.Sleep = Sleep
            self.Trance = Trance
            self.Paralysis = Paralysis
            self.Debuff = Debuff

        def getRes(self, tagName):
            if tagName == "Stun":
                return self.Stun
            if tagName == "Charm":
                return self.Charm
            if tagName == "Aphrodisiac":
                return self.Aphrodisiac
            if tagName == "Restraints" or tagName == "Restrain":
                return self.Restraints
            if tagName == "Sleep":
                return self.Sleep
            if tagName == "Trance":
                return self.Trance
            if tagName == "Paralysis":
                return self.Paralysis
            if tagName == "Debuff" or tagName == "Damage" or tagName == "Defence" or tagName == "Crit" or tagName == "Power" or tagName == "Technique" or tagName == "Willpower" or tagName == "Allure" or tagName == "Luck":
                return self.Debuff

            return 0

        def changeRes(self, tagName, amount):
            if tagName == "Stun":
                self.Stun += amount
            if tagName == "Charm":
                self.Charm += amount
            if tagName == "Aphrodisiac":
                self.Aphrodisiac += amount
            if tagName == "Sleep":
                self.Sleep += amount
            if tagName == "Restraints":
                self.Restraints += amount
            if tagName == "Trance":
                self.Trance += amount
            if tagName == "Paralysis":
                self.Paralysis += amount
            if tagName == "Debuff":
                self.Debuff += amount

            return 0

        def Update(self):
            try:
                self.Trance
            except AttributeError:
                setattr(self, 'Trance', 0)
            try:
                self.Paralysis
            except AttributeError:
                setattr(self, 'Paralysis', 0)
            try:
                self.Debuff
            except AttributeError:
                setattr(self, 'Debuff', 0)

            return


    class Fetish(renpy.store.object):
        def __init__(self, name = "", Level=0, Type = "", CreationOn = "", CreationOff = ""):
            self.name = name
            self.Level = Level
            self.Type = Type
            self.CreationOn = CreationOn
            self.CreationOff = CreationOff
            self.LevelMin = 0
            self.LevelPerm = 0
        
        def increaseMin(self, increase, enqueue=True):
            self.LevelMin = max(0, min(ptceConfig.get("fetishGain").get("fetishMaxLevel"), self.LevelMin + increase))
            if self.Type == "Fetish" and increase != 0 and enqueue and ptceConfig.get("fetishGain").get("displayFetishGainPopup"):
                enqueueFetishGain(self.name, increase, "m")

            self.increasePerm(increase, False)
        
        def increasePerm(self, increase, enqueue=True):
            self.LevelPerm = max(0, min(ptceConfig.get("fetishGain").get("fetishMaxLevel"), self.LevelPerm + increase))
            if self.Type == "Fetish" and increase != 0 and enqueue and ptceConfig.get("fetishGain").get("displayFetishGainPopup"):
                enqueueFetishGain(self.name, increase, "p")

            self.increaseTemp(increase, False)

        def increaseTemp(self, increase, enqueue=True):
            self.Level = max(0, min(ptceConfig.get("fetishGain").get("fetishMaxLevel"), self.Level + increase))
            if self.Type == "Fetish" and increase != 0 and enqueue and ptceConfig.get("fetishGain").get("displayFetishGainPopup"):
                enqueueFetishGain(self.name, increase, "t")
        
        def resetTemp(self):
            self.Level = min(ptceConfig.get("fetishGain").get("fetishMaxLevel"), self.LevelPerm)
        

        def resetPerm(self):
            self.LevelPerm = min(ptceConfig.get("fetishGain").get("fetishMaxLevel"), self.LevelMin)
        
        def getPurgeableAmount(self):
            return self.Level - self.LevelPerm


    class Perk(renpy.store.object):
        def __init__(self, name = "", description="", LevelReq=0, PerkReq = [""], StatReq=[""], StatReqAmount=[0], PerkType=[""], EffectPower=[0], PlayerCanPurchase="" ):
            self.name = name
            self.description = description
            self.LevelReq = LevelReq
            self.PerkReq = PerkReq
            self.StatReq = StatReq
            self.StatReqAmount = StatReqAmount
            self.PerkType = PerkType
            self.EffectPower = EffectPower
            self.PlayerCanPurchase = PlayerCanPurchase
            self.duration = -1

        def Update(self):
            try:
                self.duration
            except AttributeError:
                setattr(self, 'duration', -1)
            return
