init python:
    global additionalDialogueFunctions
    global vanillaFunctionNames
    additionalDialogueFunctions = {}
    vanillaFunctionNames = [
        "PlayerSpeaks", "PlayerSpeaksSkill", "SetFlexibleSpeaker", "FlexibleSpeaks", "Speak", "Speaks", "Speaks2", "Speaks3",
        "Speaks4", "Speaks5", "Speaks6", "Speaks7", "Speaks8", "Speaks9", "Speaks10", "Speaks11",
        "Speaks12", "DisplayCharacters", "ChangeImageFor", "AnimateImageLayer", "ChangeImageLayer", "HideHealth", "SetProgress", "ChangeProgress",
        "ChangeProgressBasedOnVirility", "HoldCurrentVirility", "HoldCurrentVirilityEnd", "GetEventAndSetProgress", "GetEventAndChangeProgress", "ProgressEquals", "ProgressEqualsOrGreater", "ProgressEqualsOrLess",
        "GetAnEventsProgressThenIfEquals", "GetAnEventsProgressThenIfEqualsOrGreater", "GetAnEventsProgressThenIfEqualsOrLess", "EventsProgressEqualsOtherEventsProgress", "EventsProgressEqualsOrGreaterThanOtherEventsProgress", "IfEventsProgressEqualsOrLessThanOtherEventsProgress", "VirilityEqualsOrGreater", "IfRanAway",
        "IfChoice", "SetChoice", "GetEventAndIfChoice", "GetEventAndSetChoice", "SetChoiceToPlayerName", "SetChoiceTo PlayerName", "SetChoiceToPlayerNameFromOtherEvent", "ChoiceToDisplayPlayer",
        "ChoiceToDisplayMonster", "ChoiceToDisplayPlayerFromOtherEvent", "ChoiceToDisplayMonsterFromOtherEvent", "HealingSickness", "IfHealingSickness", "IfDelayingNotifications", "AdvanceTime", "RestPlayer",
        "SleepPlayer", "RefreshPlayer", "ClearPlayerStatusEffects", "RemoveStatusEffect", "ChangeArousal", "ChangeArousalQuietly", "ChangeArousalByPercent", "SetArousalToMax",
        "SetArousalToXUnlessHigherThanX", "SetArousalToXUnlessHigherThanXThenAddY", "ChangeEnergy", "ChangeEnergyQuietly", "ChangeEnergyByPercent", "PlayerCurrentEnergyCost", "ChangeSpirit", "ChangeSpiritQuietly",
        "SetSpirit", "ChangeMaxArousal", "ChangeMaxEnergy", "ChangeMaxSpirit", "ChangePower", "ChangeWill", "ChangeInt", "ChangeTech",
        "ChangeAllure", "ChangeLuck", "ChangeSensitivity", "PermanentlyChangeSensitivity", "PermanentChangeStatusEffectResistances", "ChangeFetish", "PermanentlyChangeFetish", "SetFetish",
        "IfPlayerOrgasm", "IfPlayerArousalOverPercentOfMax", "PlayerOrgasm", "EmptySpiritCounter", "PlayerOrgasmNoSpiritLoss", "IfPlayerEnergyLessThanPercent", "IfPlayerEnergyGone", "IfPlayerSpiritGone",
        "IfHasItem", "IfHasItemInInventory", "IfDoesntHaveItem", "IfHasItemEquipped", "IfHasSkill", "IfHasPerk", "IfSensitivityEqualOrGreater", "IfHasFetish",
        "IfFetishLevelEqualOrGreater", "Menu", "StatCheck", "StatCheckRollUnder", "StatEqualsOrMore", "ClearNonPersistentStatusEffects", "ApplyStatusEffect", "CombatEncounter",
        "IfInExploration", "JumpToScene", "JumpToRandomScene", "JumpToEvent", "JumpToEventThenScene", "CallNextSceneJumpThenReturn", "CallSceneThenReturn", "CallEventAndSceneThenReturn",
        "CallCombatEventAndScene", "JumpToNPCEvent", "JumpToNPCEventThenScene", "JumpToLossEvent", "ExitGridmap", "StunGridPlayer", "IfGridPlayerStunned", "RemoveGridNPC",
        "SetPlayerGridPosition", "ChangeGridNPCMovement", "IfGridNPCSeesPlayer", "IfGridNPCThere", "ChangeGridVision", "IfGridVisonOn", "SpawnGridNPC", "ChangeMapTile",
        "GoToMap", "LevelUpMonster", "EnergyDrain", "SemenHeal", "ApplyStance", "ApplyStanceToOtherMonster", "IfPlayerHasStance", "IfPlayerHasStances",
        "IfPlayerDoesntHaveStance", "IfMonsterHasStance", "IfMonsterDoesntHaveStance", "IfOtherMonsterHasStance", "IfOtherMonsterDoesntHaveStance", "EncounterSizeGreaterOrEqualTo", "EncounterSizeLessOrEqualTo", "IfThisMonsterIsInEncounter",
        "IfPlayerIsUsingThisSkill", "IfPlayerHasStatusEffect", "IfPlayerStunnedByParalysis", "IfPlayerLevelGreaterThan", "IfMonsterLevelGreaterThan", "IfMonsterHasStatusEffect", "IfPlayerHasStatusEffectWithPotencyEqualOrGreater", "IfMonsterHasStatusEffectWithPotencyEqualOrGreater",
        "IfOtherMonsterHasStatusEffect", "IfPlayerDoesntHaveStatusEffect", "IfMonsterDoesntHaveStatusEffect", "IfOtherMonsterDoesntHaveStatusEffect", "ChangeNextStatCheckDifficulty", "ResetStatCheckDifficultyModifer", "ChangeMonsterArousal", "ChangeMonsterEnergy",
        "ChangeMonsterLevel", "ChangeMonsterSpirit", "ChangeMonsterMaxArousal", "ChangeMonsterMaxEnergy", "ChangeMonsterMaxSpirit", "ChangeMonsterPower", "ChangeMonsterWill", "ChangeMonsterInt",
        "ChangeMonsterTech", "ChangeMonsterAllure", "ChangeMonsterLuck", "ChangeMonsterSensitivity", "ChangeMonsterStatusEffectResistances", "ChangeMonsterFetish", "ChangeMonsterErosDrop", "RecalculateMonsterErosDrop",
        "ChangeMonsterExpDrop", "RecalculateMonsterExpDrop", "RefreshMonster", "IfMonsterArousalGreaterThan", "IfMonsterOrgasm", "IfMonsterEnergyGone", "IfMonsterSpiritGone", "CallMonsterEncounterOrgasmCheck",
        "MonsterOrgasm", "ApplyStatusEffectToMonster", "GiveSkillToMonster", "RemoveSkillFromPlayer", "RemoveSkillFromPlayerQuietly", "RemoveSkillFromMonster", "GiveSkillThatWasTemporarilyRemoved", "RemoveSkillFromPlayerTemporarily",
        "IfMonsterHasSkill", "GivePerkToMonster", "RemovePerkFromMonster", "IfMonsterHasPerk", "ClearMonsterSkillList", "ClearMonsterPerks", "AddMonsterToEncounter", "ShuffleMonsterEncounter",
        "RefocusOnInitialMonster", "FocusOnMonster", "FocusOnRandomMonster", "FocusedSpeaks", "FocusedSpeaksSkill", "CallMonsterAttack", "HitMonsterWith", "HitPlayerWith",
        "DamagePlayerFromMonster", "DamageMonsterFromMonster", "EndCounterChecks", "DenyPlayerOrgasm", "DenyMonsterOrgasm", "DenyTargetOrgasm", "DenyAttackerOrgasm", "SkipPlayerAttack",
        "SkipMonsterAttack", "ResumeMonsterAttack", "SkipAllMonsterAttacks", "ResumeAllMonsterAttacks", "PlayerLosesCombat", "SetPostName", "HideMonsterEncounter", "ShowMonsterEncounter",
        "ClearStances", "ClearStanceFromMonsterAndPlayer", "RemoveStatusEffectFromMonster", "ClearMonsterEncounter", "ClearMonsterEncounterBossFight", "ClearFightForVictory", "EndCombat", "RemoveMonster",
        "DefeatMonster", "GoToRandomBrothelWaiterScene", "GoToRandomBrothelBarScene", "GoToRandomBrothelHoleScene", "GoToRandomBrothelDayScene", "StoreCurrentEventSpotSkippingLines", "GoBackToStoredEvent", "TimeBecomesNight",
        "TimeBecomesDay", "TimeBecomesNormal", "IfTimeIs", "PlayerStep", "SaveNextLine", "DisplaySavedLine", "UseSavedLineInMenu", "CallLossLevelUp",
        "ChangeBG", "StoreCurrentBG", "UseHeldBG", "StopBGM", "StopBGMHard", "ChangeBGM", "StoreCurrentBGM", "PlayStoredBGM",
        "ChangeBGM-OverrideCombatMusic", "ChangeBGM-NoFade", "ChangeBGM-List", "PlayThisSongAfterCombat", "PlaySoundEffect", "PlaySoundEffect2", "PlaySoundBankOnce", "PlayLoopingSoundEffect",
        "StopSoundEffectLoop", "PlayLoopingSoundEffect2", "StopSoundEffectLoop2", "ShowTreasureChest", "HideTreasureChest", "GiveTreasure", "PlayVisualEffect", "EndVisualEffect",
        "PlayVisualEffect2", "EndVisualEffect2", "PlayVisualEffect3", "EndVisualEffect3", "PlayImagePulseLoopingList", "EndImagePulseLoopingList", "PlayImagePulseLoopingList2", "EndImagePulseLoopingList2",
        "PlayImagePulseLoopingRandom", "EndImagePulseLoopingRandom", "PlayHypnoSpiral", "EndHypnoSpiral", "PlayPendulum", "EndPendulum", "PlayKiss", "PlayKissingBarrage",
        "EndKissingBarrage", "PlayKissingBarrageOnce", "PlayCustomBarrage", "EndCustomBarrage", "PlayCustomBarrage2", "EndCustomBarrage2", "PlayBlackOut", "EndBlackOut",
        "EndAllVisualEffects", "PlayMotionEffect", "PlayMotionEffectLoop", "EndMotionEffect", "PlayMotionEffectCustom", "HasErosLessThan", "GiveExp", "ChangeEros",
        "SetEros", "ChangeErosByPercent", "AllowInventory", "DenyInventory", "GiveItem", "GiveItemQuietly", "GiveSkill", "GiveSkillQuietly",
        "GivePerkPoint", "GivePerk", "GivePerkQuietly", "RemovePerk", "RemovePerkQuietly", "ChangePerkDuration", "GoToTown", "BumpToTown",
        "GoToChurch", "GameOver", "TrueGameOver", "QuestComplete", "AdventureComplete", "SkillShoppingMenu", "ShoppingMenu", "InputProgress",
        "HasErosLessThanInput", "IfInputEquals", "IfInputEqualsOrLessThan", "AddInputToProgress", "RemoveInputFromPlayerEros", "RemoveInputFromProgress", "RemoveProgressFromEros", "RespecPlayer",
        "DonateToGoddess", "SensitivityRestore", "PurgeFetishes", "AddTributeToProgress" ]

    class DialogueFunction:
        def __init__(self, prefix, name, functionRef):
            self.prefix = prefix
            self.name = name
            self.functionRef = functionRef
    
        def execute(self):
            self.functionRef()

    def registerDialogueFunction(prefix, name, functionRef, overrideVanilla=False):
        if name in vanillaFunctionNames and not overrideVanilla:
            raise Exception("Naming conflict while registering DialogueFunction '{0}' from module '{1}'. overrideVanillaFlag has not been set, but vanilla function with same name exists.".format(name, prefix))

        existingFunction = additionalDialogueFunctions.get(name);
        if existingFunction is not None:
            isVanilla = existingFunction.prefix == "vanilla"
            if (isVanilla and not overrideVanilla) or not isVanilla:
                raise Exception("Naming conflict while registering DialogueFunctions. Both the modules '{0}' and '{1}' define a DialogueFunction named '{2}'".format(existingFunction.prefix, prefix, name))
            
        additionalDialogueFunctions[name] = DialogueFunction(prefix, name, functionRef)
    
    
init python:

    def vanillaPlayerSpeaks():
        global lineOfScene, readLine, Speaker

        Speaker = Character(_(player.name+attackTitle), what_prefix='"', what_suffix='"')
        lineOfScene += 1
        readLine = 1
        
    registerDialogueFunction("vanilla", "PlayerSpeaks", vanillaPlayerSpeaks, overrideVanilla=True)