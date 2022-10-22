label monsterClass:
    python:

        class ItemDrop:
            def __init__(self, name="", dropChance=0):
                self.name = name
                self.dropChance = dropChance

        class LossScene:
            def __init__(self, NameOfScene="", move=Skill(), stance="", includes=[], theScene=[], picture=""):
                self.NameOfScene = NameOfScene,
                self.move = move #name of move that triggers the scene
                self.stance = stance
                self.includes =  includes
                self.theScene = theScene #full scene text
                self.picture = picture

        class CombatDialogue:
            def __init__(self, lineTrigger="UsesMove", move=Skill(), theText=[]):
                self.lineTrigger = lineTrigger #the kind of trigger, usesMove, OpponentHpLow, OwnHpLow, Onloss,
                self.move = move #name of move that triggers the line
                self.theText = theText #full scene text

        class Dialogue:
            def __init__(self, NameOfScene="", DialogueType="",  Repeatable="False", theScene=[], played="False"):
                self.NameOfScene = NameOfScene #the kind of trigger, usesMove, OpponentHpLow, OwnHpLow, Onloss,
                self.DialogueType = DialogueType
                self.Repeatable = Repeatable
                self.theScene = theScene #full scene text
                self.played = played

        class Requirements:
            def __init__(self, NameOfEvent="", Progress=-99,  ChoiceNumber=-1,  Choice=""):
                self.NameOfEvent = NameOfEvent
                self.Progress = Progress
                self.ChoiceNumber = ChoiceNumber
                self.Choice = Choice

        class Picture:
            def __init__(self, name="", file="", setXalign = 0.5, setYalign = 0.25):
                self.name = name
                self.file = file
                self.setXalign = setXalign
                self.setYalign = setYalign

        class PictureSet:
            def __init__(self, name="", ImageSet=[]):
                self.name = name
                self.ImageSet = ImageSet

        class PersistantImgSetData:
            def __init__(self, name="", startingSet=""):
                self.name = name
                self.startingSet = startingSet


        class ImageLayer:
            def __init__(self, name="", Overlay="", StartOn = 0, AlwaysOn = 0, IsScene = 0, TheBody = 0, Images=[], setXalign = 0.5, setYalign = 0.25, currentImage=0, overlayOn=0, player="No", animating="", motion=""):
                self.name = name
                self.StartOn = StartOn
                self.AlwaysOn = AlwaysOn
                self.Overlay = Overlay
                self.IsScene = IsScene
                self.TheBody = TheBody
                self.Images = Images
                self.setXalign = setXalign
                self.setYalign = setYalign
                self.currentImage = currentImage
                self.overlayOn = overlayOn
                self.player = player
                self.animating = animating
                self.motion = motion


        class Monster:
            def __init__(self, stats, moneyDropped=0, name="", IDname="", species="", gender="female", description="", encyclopedia= "", tags="none",
                        skillList=[], perks=[],
                        lossScenes=[], victoryScenes=[], combatDialogue=[], BodySensitivity=BodySensitivity(),
                        ItemDropList=[], resistancesStatusEffects=ResistancesStatusEffects(),
                        requires=[""],
                        requiresEvent=[],
                        generic="True",
                        FetishList=[],
                        ImageSets=[],
                        statusEffects=StatusEffects(), lowHealthMark="False", combatStance=[CombatStance()], CardType="Monster",
                        restraintStruggle=[""],restraintStruggleCharmed=[""], restraintEscaped=[""], restraintEscapedFail=[""], restrainer=Player(), skippingAttack = 0):
                self.name=name
                self.IDname=IDname
                self.moneyDropped = moneyDropped
                self.species=species
                self.gender=gender
                self.description = description
                self.tags = tags
                self.skillList = skillList
                self.perks = perks
                self.stats = stats
                self.lossScenes = lossScenes
                self.victoryScenes = victoryScenes
                self.combatDialogue = combatDialogue
                self.statusEffects = StatusEffects()
                self.lowHealthMark = lowHealthMark
                self.BodySensitivity = BodySensitivity
                self.FetishList = FetishList
                self.ItemDropList = ItemDropList
                self.combatStance = combatStance
                self.CardType = CardType
                self.resistancesStatusEffects = resistancesStatusEffects
                self.requires = requires

                self.requiresEvent = requiresEvent

                self.generic = generic
                self.encyclopedia = encyclopedia

                self.restraintStruggle=restraintStruggle
                self.restraintStruggleCharmed=restraintStruggleCharmed
                self.restraintEscaped=restraintEscaped
                self.restraintEscapedFail=restraintEscapedFail
                self.restraintOnLoss = [""]
                self.restrainer=restrainer

                self.putInStance = 0
                self.putInRestrain = 0

                self.ImageSets = ImageSets
                self.currentSet = 0

                self.skippingAttack = skippingAttack
                self.learnedFetishStrength = {}
                self.learnedSensitivities = {}
                self.hasBeenAnalyzed = False

            def giveStance(self, name, target, skill=Skill(),  holdoverDura=0):
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

            def clearStance(self):
                numberOStance = len(self.combatStance)
                i = 0
                while i < numberOStance:
                    del self.combatStance[0]
                    i += 1
                self.combatStance.append(CombatStance("None"))

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


            def removeStanceByName(self, theName):
                i = 0
                for x in self.combatStance:
                    if x.Stance == theName  or theName == "All":
                        del self.combatStance[i]
                    i += 1
                if len(self.combatStance) <= 0:
                    self.combatStance.append(CombatStance("None"))

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
                        self.stats.max_true_sp = self.max_sp

                    if aquiredPerk.PerkType[p] == "GainEnergy" or aquiredPerk.PerkType[p] == "Gain Energy":

                        self.stats.max_ep += aquiredPerk.EffectPower[p] * GiveOrTake
                        self.stats.max_true_ep = self.stats.max_ep
                    if aquiredPerk.PerkType[p] == "GainArousal" or aquiredPerk.PerkType[p] == "Gain Arousal":

                        self.stats.max_hp += aquiredPerk.EffectPower[p] * GiveOrTake
                        self.stats.max_true_hp = self.stats.max_hp

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
                        baseFetish = self.getFetish(parsed[0])

                        if parsed[2] == "":
                            multi = 1
                        else:
                            multi = int(parsed[2])

                        if aquiredPerk.PerkType[p] == "IncreaseFetish" or aquiredPerk.PerkType[p] == "Increase Fetish":
                            baseFetish += multi * GiveOrTake
                        else:
                            baseFetish -= multi * GiveOrTake
                        self.setFetish(parsed[0], baseFetish)
                    p += 1

                if GiveOrTake == 1:
                    self.perks.append(copy.deepcopy(PerkDatabase[fetchPerk]))


                    if duration != -2:
                        self.perks[-1].duration = duration


                else:
                    del self.perks[fetchPerk]

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

            def fetishTotal(self):
                total = 0
                for each in self.FetishList:
                    total += each.Level
                return total
            
            def updateLearned(self, skillOption, player):
                fetishes = skillOption.getActualFetishes(self)
                playerFetishes = getPlayerFetishes(fetishes)
                for f in playerFetishes:
                    value = round(f.Level * 0.01, 2)
                    self.learnedFetishStrength.update({f.name: value})
                
                for sens in skillOption.skillTags:
                    if not (sens == "" or sens == " "):
                        value = round((player.BodySensitivity.getRes(sens) - 100) * 0.01, 2)
                        self.learnedSensitivities.update({sens: value})

            def clearLearned(self):
                self.learnedWeaknesses = {}
            
            def getCurrentStanceNames(self):
                map(lambda s: s.Stance, self.combatStance)
            
            def getKnownMovePriority(self, skillOption):
                skillFetishTags = skillOption.getActualFetishes(self)
                finalValue = 0
                for f, v in self.learnedFetishStrength.items():
                    if f in skillFetishTags:
                        finalValue += v

                for s, v in self.learnedSensitivities.items():
                    if s in skillOption.skillTags:
                        finalValue += v
                
                return finalValue

            def levelUp(self, lvlTarget):
                lvlDifference  = lvlTarget - self.stats.lvl

                weightedList = []
                hpWeight = ((1000-self.stats.max_hp)*0.0002)
                if hpWeight < 0.08:
                    hpWeight = 0.08
                weightedList = [("HP", hpWeight), ("Power", self.stats.Power*0.01), ("Tech", self.stats.Tech*0.01), ("Int", self.stats.Int*0.01), ("Allure", self.stats.Allure*0.01), ("Willpower", self.stats.Willpower*0.01), ("Luck", self.stats.Luck*0.01)]
                ch = 0
                while ch < lvlDifference*3:
                    lvlChoice = weightedChoice(weightedList)

                    if lvlChoice == "HP":
                        self.stats.max_hp += 10
                        self.stats.max_true_hp =  self.stats.max_hp
                    elif lvlChoice == "Power":
                        self.stats.Power += 1
                    elif lvlChoice == "Tech":
                        self.stats.Tech += 1
                    elif lvlChoice == "Int":
                        self.stats.Int += 1
                    elif lvlChoice == "Allure":
                        self.stats.Allure += 1
                    elif lvlChoice == "Willpower":
                        self.stats.Willpower += 1
                    elif lvlChoice == "Luck":
                        self.stats.Luck += 1

                    ch +=1

                self.stats.max_hp += lvlDifference*10
                self.stats.max_true_hp =  self.stats.max_hp

                self.stats.max_ep += lvlDifference*2
                self.stats.max_true_ep =  self.stats.max_ep
                self.stats.ep += lvlDifference*2

                self.stats.lvl = lvlTarget
                return

        #depreciated classes that are only here so old saves don't implode
        class NPC:
            def __init__(self):
                self = self
