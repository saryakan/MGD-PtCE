label playerClass:
    python:
        #should prolly be directly integrated into the player.
        def getVirility(player, forceCurrentVirile = 0):
            global heldVirility
            Virility = 0
            if heldVirility == 0 or forceCurrentVirile == 1:
                Virility = 0
                Vmod = 0
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "VirilityBoost":
                            Vmod += perk.EffectPower[p]
                        p += 1

                Virility = (player.stats.lvl -1)*0.5 + player.stats.max_sp*5 + Vmod + 10
                Virility = math.floor(Virility)
                Virility = int(Virility)
            else:
                Virility = copy.deepcopy(heldVirility)

            return Virility

        class LvlChoice:
            def __init__(self, statUp="", ResUp="None"):
                self.statUp = statUp
                self.ResUp = ResUp

        class Player:
            def __init__(self, name="", gender="male", skillList=[], perks=[], stats=Stats(), inventory=Inventory(), statPoints = 5,
                        BodySensitivity=BodySensitivity(), statusEffects=StatusEffects(), species="Player",
                        FetishList = [Fetish("Sex", 0), Fetish("Oral", 0), Fetish("Breasts", 0), Fetish("Ass", 0)],
                        combatStance=[CombatStance()], lvlUps=[], resistancesStatusEffects=ResistancesStatusEffects(),
                        restraintStruggle=[""], restraintStruggleCharmed=[""], restraintEscaped=[""], restraintEscapedFail=[""], restrainer=Stats(), perkPoints=0):
                self.name=name
                self.gender=gender
                self.skillList = skillList
                self.stats = stats
                self.inventory = inventory
                self.statPoints = statPoints
                self.BodySensitivity = BodySensitivity
                self.statusEffects = StatusEffects()
                self.species = species
                self.BodySensitivity = BodySensitivity
                self.SensitivityPoints = 3
                self.FetishList = FetishList
                self.combatStance = combatStance
                self.pastLevelUps = [[]]
                self.pastLevelUpSens = []
                self.lvlUps = lvlUps
                self.resistancesStatusEffects = resistancesStatusEffects

                self.perks = perks
                self.perkPoints = perkPoints

                self.BodySensitivity.Sex=100
                self.BodySensitivity.Ass=100
                self.BodySensitivity.Breasts=100
                self.BodySensitivity.Mouth=100
                self.BodySensitivity.Seduction=100
                self.BodySensitivity.Magic=100
                self.BodySensitivity.Pain=100

                self.BodySensitivity.Holy=100
                self.BodySensitivity.Unholy=100

                self.restraintStruggle=restraintStruggle
                self.restraintStruggleCharmed=restraintStruggleCharmed
                self.restraintEscaped=restraintEscaped
                self.restraintEscapedFail=restraintEscapedFail
                self.restraintOnLoss = [""]
                self.restrainer=restrainer


            def respec(self):
                global difficulty#, easyCoreStat, easyHp, easyEp, easySp, normalCoreStat, normalHp, normalEp, normalSp, hardCoreStat, hardHp, hardEp, hardSp
                tempPerksList = copy.deepcopy(self.perks)
                for each in tempPerksList:
                    if each.PlayerCanPurchase == "Yes":
                        self.giveOrTakePerk(each.name, -1)
                        self.perkPoints += 1
                tempPerksList = copy.deepcopy(self.perks)
                for each in tempPerksList:
                    self.giveOrTakePerk(each.name, -1)

                #if difficulty == "Easy":
                #    coreStatBase = easyCoreStat
                #    HpBase = easyHp
                #    EpBase = easyEp
                #    SpBase = easySp
                #if difficulty == "Normal":
                #    coreStatBase = normalCoreStat
                #    HpBase = normalHp
                #    EpBase = normalEp
                #    SpBase = normalSp
                #if difficulty == "Hard":
                #    coreStatBase = hardCoreStat
                #    HpBase = hardHp
                #    EpBase = hardEp
                #    SpBase = hardSp
                self.pastLevelUps = [[]]
                self.pastLevelUpSens = []

                self.stats.bonus_hp = 0
                self.stats.bonus_ep = 0
                self.stats.max_true_hp = self.stats.max_hp + self.stats.bonus_hp
                self.stats.max_true_ep = self.stats.max_ep + self.stats.bonus_ep
                self.stats.max_true_sp = self.stats.max_sp

                if difficulty == "Normal":
                    self.resetStat("Arousal", 45)
                    self.resetStat("Energy", 25)
                else:
                    self.resetStat("Arousal", 40)
                    self.resetStat("Energy", 20)
                #self.resetStat("Spirit", SpBase)


                self.resetStat("Power", 1)
                self.resetStat("Technique", 1)
                self.resetStat("Intelligence", 1)
                self.resetStat("Willpower", 1)
                self.resetStat("Allure", 1)
                self.resetStat("Luck", 1)


                self.BodySensitivity.resetSens("Sex", self)
                self.BodySensitivity.resetSens("Ass", self)
                self.BodySensitivity.resetSens("Breasts", self)
                self.BodySensitivity.resetSens("Mouth", self)
                self.BodySensitivity.resetSens("Seduction", self)
                self.BodySensitivity.resetSens("Magic", self)
                self.BodySensitivity.resetSens("Pain", self)

                self.CalculateStatBoost()
                self.stats.BarMinMax()

                for each in tempPerksList:
                    self.giveOrTakePerk(each.name, 1)

                return

            def resetStat(self, statToChange, statBase):

                actualStat = self.stats.getStat(statToChange) - self.getStatBonusReduction(statToChange)
                actualStat -= statBase

                if statToChange == "Arousal":
                    self.statPoints += actualStat/10
                    self.stats.max_hp -= actualStat
                elif statToChange == "Energy":
                    self.statPoints += actualStat/10
                    self.stats.max_ep -= actualStat
                elif statToChange == "Spirit":
                    self.statPoints += actualStat*3
                    self.stats.max_sp -= actualStat
                else:
                    self.statPoints += actualStat
                if statToChange == "Power":
                    self.stats.Power -= actualStat
                if statToChange == "Technique":
                    self.stats.Tech -= actualStat
                if statToChange == "Intelligence":
                    self.stats.Int -= actualStat
                if statToChange == "Willpower":
                    self.stats.Willpower -= actualStat
                if statToChange == "Allure":
                    self.stats.Allure -= actualStat
                if statToChange == "Luck":
                    self.stats.Luck -= actualStat
                return

            def setNewPlayerVariables(self, restrainer=Stats(), restraintStruggle=[""], restraintStruggleCharmed=[""], restraintEscaped=[""], restraintEscapedFail=[""] ):

                self.restraintStruggle=restraintStruggle
                self.restraintStruggleCharmed=restraintStruggleCharmed
                self.restraintEscaped=restraintEscaped
                self.restraintEscapedFail=restraintEscapedFail
                self.restrainer=restrainer

                try:
                    self.perks
                except AttributeError:
                    self.perks = []

                try:
                    self.perkPoints
                except AttributeError:
                    self.perkPoints = 0

                    p = 1
                    while p < player.stats.lvl:
                        if p % 5 == 0:
                            self.perkPoints += 1

                        p+=1


            def _resetPlayerAtStart(self, theFetishList):

                self.stats.Exp = 0
                self.stats.ExpNeeded = 10
                self.stats.lvl=1
                self.stats.max_hp=normalHp
                self.stats.hp=0
                self.stats.max_ep=normalEp
                self.stats.ep=normalEp*2
                self.stats.max_sp=normalSp
                self.stats.sp=normalSp
                self.stats.Power = 5
                self.stats.Tech = 5
                self.stats.Int = 5
                self.stats.Allure = 5
                self.stats.Willpower = 5
                self.stats.Luck = 5
                self.pastLevelUps = [[]]
                self.pastLevelUpSens = []

                self.perks = []

                self.skillList = []
                self.lvlUps = []

                self.inventory=Inventory()
                self.combatStance=[CombatStance()]

                self.statPoints = 5
                self.perkPoints = 0

                self.SensitivityPoints = 3
                self.FetishList = theFetishList

                self.resistancesStatusEffects.Stun = 0
                self.resistancesStatusEffects.Charm = 0
                self.resistancesStatusEffects.Aphrodisiac = 0
                self.resistancesStatusEffects.Restraints = 0
                self.resistancesStatusEffects.Sleep = 0
                self.resistancesStatusEffects.Trance = 0
                self.resistancesStatusEffects.Paralysis = 0
                self.resistancesStatusEffects.Debuff = 0

                self.statusEffects.defend.duration = -1
                self.statusEffects.stunned.duration = -1
                self.statusEffects.charmed.duration = -1
                self.statusEffects.aphrodisiac.duration = -1
                self.statusEffects.aphrodisiac.potency = 0
                self.statusEffects.restrained.duration = 0
                self.statusEffects.surrender.duration = 0

                self.statusEffects.tempAtk = [StatusEffect()]
                self.statusEffects.tempDefence = [StatusEffect()]
                self.statusEffects.tempCrit = [StatusEffect()]
                self.statusEffects.tempPower = [StatusEffect()]
                self.statusEffects.tempTech = [StatusEffect()]
                self.statusEffects.tempInt = [StatusEffect()]
                self.statusEffects.tempWillpower = [StatusEffect()]
                self.statusEffects.tempAllure = [StatusEffect()]
                self.statusEffects.tempLuck = [StatusEffect()]


                self.BodySensitivity.Sex=100
                self.BodySensitivity.Ass=100
                self.BodySensitivity.Breasts=100
                self.BodySensitivity.Mouth=100
                self.BodySensitivity.Seduction=100
                self.BodySensitivity.Magic=100
                self.BodySensitivity.Pain=100
                self.BodySensitivity.Holy=100
                self.BodySensitivity.Unholy=100

                self.restraintStruggle=[""]
                self.restraintStruggleCharmed=[""]
                self.restraintEscaped=[""]
                self.restraintEscapedFail=[""]
                self.restrainer=Monster(Stats())


            def giveStance(self, name, target, skill=Skill(), holdoverDura=0):
                if name != "":
                    i = 0
                    for each in self.combatStance:
                        if each.Stance == "None":
                            del self.combatStance[i]
                        i+=1
                    durability = getStanceHoldRoll(self)
                    if skill.name != "blank":
                        fetishMod = 0
                        for each in skill.fetishTags:
                            for fetishE in target.FetishList:
                                checkTag = each
                                if checkTag == "Penetration":
                                    for stanceChek in self.combatStance:
                                        if stanceChek.Stance == "Sex":
                                            checkTag = "Sex"
                                        elif stanceChek.Stance == "Anal":
                                            checkTag = "Ass"
                                if checkTag == fetishE.name:
                                    fetishMod += (fetishE.Level)
                        durability += durability*(fetishMod*0.005) + (fetishMod*0.1)
                    self.combatStance.append(CombatStance(name, durability+holdoverDura))

            def getStanceDurability(self, theName):
                i = 0
                durability = 0
                stanceRemoved = 0
                for x in self.combatStance:
                    if (x.Stance == theName and stanceRemoved == 0) or theName == "All":
                        durability = self.combatStance[i].potency
                        stanceRemoved = 1
                    i += 1
                return durability

            def clearStance(self):
                numberOStance = len(self.combatStance)
                i = 0
                while i < numberOStance:
                    del self.combatStance[0]
                    i += 1
                self.combatStance.append(CombatStance("None"))


            def removeStanceByName(self, theName):
                i = 0
                stanceRemoved = 0
                for x in self.combatStance:
                    if (x.Stance == theName and stanceRemoved == 0) or theName == "All":
                        del self.combatStance[i]
                        stanceRemoved = 1
                    i += 1
                if len(self.combatStance) <= 0:
                    self.combatStance.append(CombatStance("None"))

            def learnSkill(self, skill):
                self.skillList.append(skill)

            def removeSkill(self, skill):
                fetchSkill = getFromName(skill, self.skillList)
                del self.skillList[fetchSkill]

            def has_skill(self, aSkill):
                    if getFromName(aSkill, self.skillList) != -1:
                        return True
                    else:
                        return False

            def getStatBonusReduction(self, stat):

                TemporaryStatCheck = self.inventory.RuneSlotOne.getStat(stat) + self.inventory.RuneSlotTwo.getStat(stat) + self.inventory.RuneSlotThree.getStat(stat) + self.inventory.AccessorySlot.getStat(stat)

                if stat == "Arousal" or stat == "Energy" or stat == "Spirit":
                    stat = "Gain" + stat

                if stat == "Arousal":
                    TemporaryStatCheck -= self.stats.bonus_hp
                if stat == "Energy":
                    TemporaryStatCheck -= self.stats.bonus_ep

                if stat == "Power":
                    for each in self.statusEffects.tempPower:
                        TemporaryStatCheck += each.potency
                if stat == "Willpower":
                    for each in self.statusEffects.tempWillpower:
                        TemporaryStatCheck += each.potency
                if stat == "Intelligence":
                    for each in self.statusEffects.tempInt:
                        TemporaryStatCheck += each.potency

                for perk in self.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == stat:
                            TemporaryStatCheck += perk.EffectPower[p]
                        p += 1

                return TemporaryStatCheck


            def creatorLvlStat(self, stat, amount, mini, maxi, cost=1, statToChange="", tempStat=0):
                go = 0

                if stat+amount-tempStat <= maxi and amount > 0:
                    if self.statPoints >= cost:
                        self.statPoints -= cost
                        stat += amount
                        go = 1

                if respeccing == 0:
                    tempStat = 0
                if stat+amount >= mini+tempStat and amount < 0:
                    self.statPoints += cost
                    stat += amount
                    go = 1

                if statToChange == "Arousal":
                    self.stats.max_hp = stat
                if statToChange == "Energy":
                    self.stats.ep += amount
                    self.stats.max_ep = stat
                if statToChange == "Spirit":
                    self.stats.max_sp = stat
                if statToChange == "Power":
                    self.stats.Power = stat
                if statToChange == "Technique":
                    self.stats.Tech = stat
                if statToChange == "Intelligence":
                    self.stats.Int = stat
                if statToChange == "Willpower":
                    self.stats.Willpower = stat
                if statToChange == "Allure":
                    self.stats.Allure = stat
                if statToChange == "Luck":
                    self.stats.Luck = stat



                if go == 1:
                    if amount > 0:
                        if len(self.pastLevelUps[-1]) >= 2:
                            self.pastLevelUps.append([])
                        self.pastLevelUps[-1].append(copy.deepcopy(statToChange))
                    else:
                        lvledStack = []
                        foundRemoved = 0
                        tracker = len(self.pastLevelUps) -1
                        tempList = copy.deepcopy(self.pastLevelUps)
                        for each in tempList[::-1]:
                            if foundRemoved == 1:
                                break
                            for lvl in each:
                                if lvl == statToChange:
                                    del self.pastLevelUps[tracker][0]
                                    foundRemoved = 1
                                    break
                                else:
                                    lvledStack.append(self.pastLevelUps[tracker][0])
                                    del self.pastLevelUps[tracker][0]

                            if len(self.pastLevelUps[tracker]) == 0:
                                del self.pastLevelUps[tracker]
                                if len(self.pastLevelUps) == 0:
                                    self.pastLevelUps.append([])
                            tracker -= 1
                        for each in lvledStack:
                            if len(self.pastLevelUps[-1]) >= 2:
                                self.pastLevelUps.append([])
                            self.pastLevelUps[-1].append(each)

                return

            def CalculateStatBoost(self):

                global hpDeficit
                if hpDeficit < 0:
                        self.stats.max_true_hp = copy.deepcopy(hpDeficit)
                        hpDeficit = 0
                global epDeficit
                if epDeficit < 0:
                        self.stats.max_true_ep = copy.deepcopy(epDeficit)
                        epDeficit = 0



                truePower = self.stats.Power - self.getStatBonusReduction("Power")
                trueWillpower = self.stats.Willpower - self.getStatBonusReduction("Willpower")
                trueInt = self.stats.Int  - self.getStatBonusReduction("Intelligence")

                excessEnergy = copy.deepcopy(self.stats.bonus_ep)

                self.stats.bonus_hp = 0
                self.stats.bonus_ep = 0

                self.stats.bonus_hp = ((int(math.floor(truePower / 5)))*10)
                self.stats.bonus_ep = ((int(math.floor(trueInt / 5)))*10)

                self.stats.bonus_hp += ((int(math.floor(trueWillpower / 5)))*5)
                self.stats.bonus_ep += ((int(math.floor(trueWillpower / 5)))*5)


                self.stats.ep += self.stats.bonus_ep - excessEnergy

                self.stats.max_true_hp = self.stats.max_hp + self.stats.bonus_hp
                self.stats.max_true_ep = self.stats.max_ep + self.stats.bonus_ep
                self.stats.max_true_sp = self.stats.max_sp


                if self.stats.max_true_hp < 1:
                        hpDeficit = copy.deepcopy(self.stats.max_true_hp)
                        self.stats.max_true_hp = 1
                if self.stats.max_true_ep < 1:
                        epDeficit = copy.deepcopy(self.stats.max_true_ep)
                        self.stats.max_true_ep = 1



                return


            def getFetish(self, name):
                for each in self.FetishList:
                    if each.name == name:
                        return each.Level

                return 0

            def setFetish(self, name, number):
                L = 0
                for each in self.FetishList:
                    if each.name == name:
                        self.FetishList[L].Level = number
                    L += 1

                return

            def giveOrTakePerk(self, perkName, GiveOrTake, duration= -2):

                if GiveOrTake == 1:
                    fetchPerk = getFromName(perkName, PerkDatabase)
                    aquiredPerk = PerkDatabase[fetchPerk]
                else:
                    fetchPerk = getFromName(perkName, self.perks)
                    aquiredPerk = self.perks[fetchPerk]

                p = 0
                while  p < len(aquiredPerk.PerkType):
                    if aquiredPerk.PerkType[p] == "GainSpirit" or aquiredPerk.PerkType[p] == "Gain Spirit":
                        self.stats.max_sp += aquiredPerk.EffectPower[p] * GiveOrTake
                        self.stats.sp += aquiredPerk.EffectPower[p] * GiveOrTake

                    if aquiredPerk.PerkType[p] == "GainEnergy" or aquiredPerk.PerkType[p] == "Gain Energy":
                        global epDeficit
                        if epDeficit < 0:
                                self.stats.max_true_ep = copy.deepcopy(epDeficit)
                                hpDeficit = 0
                        self.stats.max_ep += aquiredPerk.EffectPower[p] * GiveOrTake
                        player.CalculateStatBoost()
                        if GiveOrTake > 0:
                            self.stats.ep += aquiredPerk.EffectPower[p] * GiveOrTake
                        if self.stats.max_true_ep < 1:
                                hpDeficit = copy.deepcopy(self.stats.max_true_ep)
                                self.stats.max_true_ep = 1
                    if aquiredPerk.PerkType[p] == "GainArousal" or aquiredPerk.PerkType[p] == "Gain Arousal":
                        global hpDeficit
                        if hpDeficit < 0:
                                self.stats.max_true_hp = copy.deepcopy(hpDeficit)
                                hpDeficit = 0
                        self.stats.max_hp += aquiredPerk.EffectPower[p] * GiveOrTake
                        player.CalculateStatBoost()
                        if self.stats.max_true_hp < 1:
                                hpDeficit = copy.deepcopy(self.stats.max_true_hp)
                                self.stats.max_true_hp = 1

                    if aquiredPerk.PerkType[p] == "GiveSensitivityPoints" or aquiredPerk.PerkType[p] == "Give Sensitivity Points":
                        self.SensitivityPoints += aquiredPerk.EffectPower[p] * GiveOrTake

                    if aquiredPerk.PerkType[p] == "Power":
                        self.stats.Power += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "Technique":
                        self.stats.Tech += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "Intelligence":
                        self.stats.Int += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "Allure":
                        self.stats.Allure += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "Willpower":
                        self.stats.Willpower += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "Luck":
                        self.stats.Luck += aquiredPerk.EffectPower[p] * GiveOrTake

                    if aquiredPerk.PerkType[p] == "StunRes" or aquiredPerk.PerkType[p] == "Stun Res":
                        self.resistancesStatusEffects.Stun += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "CharmRes" or aquiredPerk.PerkType[p] == "CharmRes":
                        self.resistancesStatusEffects.Charm += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "AphrodisiacRes" or aquiredPerk.PerkType[p] == "Aphrodisiac Res":
                        self.resistancesStatusEffects.Aphrodisiac += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "RestraintsRes" or aquiredPerk.PerkType[p] == "Restraints Res":
                        self.resistancesStatusEffects.Restraints += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "SleepRes" or aquiredPerk.PerkType[p] == "Sleep Res":
                        self.resistancesStatusEffects.Sleep += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "TranceRes" or aquiredPerk.PerkType[p] == "Trance Res":
                        self.resistancesStatusEffects.Trance += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "ParalysisRes" or aquiredPerk.PerkType[p] == "Paralysis Res":
                        self.resistancesStatusEffects.Paralysis += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "DebuffRes" or aquiredPerk.PerkType[p] == "Debuff Res":
                        self.resistancesStatusEffects.Debuff += aquiredPerk.EffectPower[p] * GiveOrTake

                    if aquiredPerk.PerkType[p] == "SexSensitivity" or aquiredPerk.PerkType[p] == "Sex Sensitivity":
                        self.BodySensitivity.Sex += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "AssSensitivity" or aquiredPerk.PerkType[p] == "Ass Sensitivity":
                        self.BodySensitivity.Ass += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "BreastsSensitivity" or aquiredPerk.PerkType[p] == "Breasts Sensitivity":
                        self.BodySensitivity.Breasts += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "MouthSensitivity" or aquiredPerk.PerkType[p] == "Mouth Sensitivity":
                        self.BodySensitivity.Mouth += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "SeductionSensitivity" or aquiredPerk.PerkType[p] == "Seduction Sensitivity":
                        self.BodySensitivity.Seduction += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "MagicSensitivity" or aquiredPerk.PerkType[p] == "Magic Sensitivity":
                        self.BodySensitivity.Magic += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "PainSensitivity" or aquiredPerk.PerkType[p] == "Pain Sensitivity":
                        self.BodySensitivity.Pain += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "HolySensitivity" or aquiredPerk.PerkType[p] == "Holy Sensitivity":
                        self.BodySensitivity.Holy += aquiredPerk.EffectPower[p] * GiveOrTake
                    if aquiredPerk.PerkType[p] == "UnholySensitivity" or aquiredPerk.PerkType[p] == "Unholy Sensitivity":
                        self.BodySensitivity.Unholy += aquiredPerk.EffectPower[p] * GiveOrTake

                    if aquiredPerk.PerkType[p] == "IncreaseFetish" or aquiredPerk.PerkType[p] == "DecreaseFetish" or aquiredPerk.PerkType[p] == "Increase Fetish" or aquiredPerk.PerkType[p] == "Decrease Fetish":
                        resTarget = aquiredPerk.EffectPower[p]

                        parsed = aquiredPerk.EffectPower[p].partition("|/|")
                        baseFetish = self.getFetishObject(parsed[0])

                        if parsed[2] == "":
                            multi = 1
                        else:
                            multi = int(parsed[2])

                        if aquiredPerk.PerkType[p] == "IncreaseFetish" or aquiredPerk.PerkType[p] == "Increase Fetish":
                            baseFetish.increaseMin(multi * GiveOrTake)
                        else:
                            baseFetish.increaseMin(-multi * GiveOrTake)

                    p += 1

                if GiveOrTake == 1:
                    self.perks.append(copy.deepcopy(PerkDatabase[fetchPerk]))


                    if duration != -2:
                        self.perks[-1].duration = duration


                else:
                    del self.perks[fetchPerk]

                self.CalculateStatBoost()

                return
            
            def getFetishObject(self, name):
                for fetish in self.FetishList:
                    if fetish.name == name:
                        return fetish

            def fetishTotal(self):
                total = 0
                for each in self.FetishList:
                    total += each.Level
                return total

            def getAllFetishes(self):
                return self.getFetishByType("Fetish")

            def getAllAddictions(self):
                return self.getFetishByType("Addiction")

            def getFetishByType(self, type):
                return filter(lambda f: f.Type == type, self.FetishList)

            def Update(self):

                self.stats.Update()
                self.resistancesStatusEffects.Update()
                self.inventory.Update()
                self.statusEffects.Update()

                try:
                    len(self.pastLevelUps[0])
                except:
                    setattr(self, 'pastLevelUps', [[]])
                    setattr(self, 'pastLevelUpSens', [])
                    self.pastLevelUpSens = []

                    setattr(self.combatStance, 'potency', 0)

                return
