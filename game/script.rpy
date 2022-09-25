init python:
    import re
    def dynamic_loader(where):
        return [thing for thing in jsonList if re.match(where, thing)]

    #Thanks to Andy_kl for initial filter_list_files
    @renpy.pure
    def filter_list_files(where):
        where = where.rstrip('/') + '/'
        return [thing for thing in renpy.list_files() if thing.startswith(where)]

init python:
    import json
    import os
    import math
    import copy
    import random
    import time

    dontJumpOutOfGridEvents = 0
    postCombatEventGridFailsafe = 0

    config.rollback_length = 10
    config.longpress_vibrate = 0
    config.quicksave_slots = 12
    config.pause_after_rollback = True

    if persistent.showCharacterImages is None:
        persistent.showCharacterImages = True

    if persistent.showCardBubbles is None:
        persistent.showCardBubbles = True

    if persistent.showVFX is None:
        persistent.showVFX = True
    #showCharacterImages = False

    if persistent.setBaseVolume is None:
        _preferences.set_volume('music', 0.5)
        persistent.setBaseVolume = True
        renpy.restart_interaction()

    renpy.music.register_channel("soundChannel2","sfx",loop=False,tight=False)
    renpy.music.register_channel("loopingSound","sfx",loop=True,tight=True)
    renpy.music.register_channel("loopingSound2","sfx",loop=True,tight=True)

    kissQuickSoundBank = ["sfx/Erotic/KissQuick/Kiss sound 01.wav", "sfx/Erotic/KissQuick/Kiss sound 04.wav", "sfx/Erotic/KissQuick/Kiss sound 11.wav", "sfx/Erotic/KissQuick/Kiss sound 14.wav", "sfx/Erotic/KissQuick/kiss1.wav"]
    kissLongSoundBank = ["sfx/Erotic/KissLong/Kiss sound 07.wav", "sfx/Erotic/KissLong/Kiss sound 09.wav", "sfx/Erotic/KissLong/Kiss sound 10.wav", "sfx/Erotic/KissLong/Kiss sound 16.wav"]
    kissMakeOutSoundBank = ["sfx/Erotic/KissMakeout/Kiss sound 03.wav", "sfx/Erotic/KissMakeout/Kiss sound 05.wav", "sfx/Erotic/KissMakeout/Kiss sound 18.wav", "sfx/Erotic/KissMakeout/Kiss sound 19.wav", "sfx/Erotic/KissMakeout/Kiss sound 20.wav", "sfx/Erotic/KissMakeout/Kiss sound 21.wav",  "sfx/Erotic/KissMakeout/Kiss sound 23.wav", "sfx/Erotic/KissMakeout/Kiss sound 24.wav", "sfx/Erotic/KissMakeout/kiss2.mp3"]

    blowjobLickingSoundBank = ["sfx/Erotic/Sucking/Fast tongue movement.mp3", "sfx/Erotic/Sucking/licking010.wav", "sfx/Erotic/Sucking/licking015.wav", "sfx/Erotic/Sucking/licking031.wav", "sfx/Erotic/Sucking/licking040.wav", "sfx/Erotic/Sucking/lickingAndSucking.mp3"]
    blowjobSuckingSoundBank = ["sfx/Erotic/Sucking/sucking004.wav", "sfx/Erotic/Sucking/sucking012.wav", "sfx/Erotic/Sucking/sucking014.wav", "sfx/Erotic/Sucking/sucking028.wav", "sfx/Erotic/Sucking/sucking035.wav", "sfx/Erotic/Sucking/sucking037.wav",  "sfx/Erotic/Sucking/sucking041.wav", "sfx/Erotic/Sucking/sucking043.wav","sfx/Erotic/Sucking/sucking047.wav"]
    blowjobDeepSuckingSoundBank = ["sfx/Erotic/Sucking/slurp005.wav", "sfx/Erotic/Sucking/slurp006.wav", "sfx/Erotic/Sucking/suckingLong.mp3"]
    blowjobVigorousSoundBank = ["sfx/Erotic/Sucking/vigorous.mp3", "sfx/Erotic/Sucking/vigorous044.wav"]

    ejaculationSoundBank =  ["sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 1.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 5.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 10.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 1.wav"]
    messyEjaculationSoundBank = ["sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 3.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 4.wav","sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 8.wav"]



    MenuLineSceneCheckMark = -1

    viewportID2 = ""

    recoil = 0
    theTimeType = ""
    perkDurationTip = 0
    LostGameOver = 0

    itemEvent = 0

    inCalledSceneJump = 0

    specifyCurrentChoice = 0
    specifyDataLocation = 0

    MotionEffectLoop = 0

    spaceNext = 0

    inTownMenu = 0

    combatItems = 0
    currentEnemy = 0
    e = 0

    flatCore = 0
    percentCore = 0
    powerDisplay =0
    techDisplay = 0
    intDisplay = 0
    allureDisplay = 0
    willDisplay = 0
    luckDisplay = 0
    powerBoost = 0
    powerPerBoost = 0
    intBoost = 0
    intPerBoost = 0
    techBoost = 0
    techPerBoost = 0
    allureBoost = 0
    allurePerBoost = 0
    willBoost = 0
    willPerBoost = 0
    luckBoost = 0
    luckPerBoost = 0
    statDamMod = 0

    override = ""

    EventConsister = ""
    EventConsisterTarget = 0

    TogglePerkFilter = False
    PerkOrder = "None"
    PerkFilter = "None"

    textColor = "#F6BADC"
    textColor2 = "#F6BADC"
    textColor3 = "#F6BADC"
    textColor4 = "#F6BADC"
    textColor5 = "#F6BADC"
    textColor6 = "#F6BADC"
    textColor7 = "#F6BADC"

    rehauled = 0
    progressionBoost = 0

    npcCount = 0
    senCount = 0
    fetCount = 0

    notFunction = 0
    timeNotify = 0

    damageToPlayer = 0
    damageToEnemy = 0
    progressDisplay = 0
    playerOrgasmLine = ""
    monsterOrgasmLine = ""

    lineBank = ["Do your best!", "Can't we just hold hands?", "Or maybe, it's a nightmare?", "Free adventuring school!", "Why would you resist love?", "The goddess will protect you.", "Hot succubi are in your area.♥"]

    sexBank = ["pussy", "pussy", "slit", "honeypot"]
    assBank = ["ass", "ass", "rear", "behind", "derriere"]

    sexAdjectiveBank = ["", "wet ", "tight ", "wet ", "tight ", "receptive ", "warm "]
    assAdjectiveBank = ["", "tight ", "tight ", "curved ", "rounded ", "receptive "]


    Morning = "{color=#ffe9b5}Morning{/color}"
    Noon = "{color=#ffe9b5}Noon{/color}"
    Afternoon = "{color=#ffe9b5}Afternoon{/color}"

    MorningNight = "{color=#cfb8df}Morning{/color}"
    NoonNight = "{color=#cfb8df}Noon{/color}"
    AfternoonNight = "{color=#cfb8df}Afternoon{/color}"

    Dusk = "{color=#cfb8df}Dusk{/color}"
    Evening = "{color=#cfb8df}Evening{/color}"
    Midnight = "{color=#cfb8df}Midnight{/color}"

    DuskDay = "{color=#ffe9b5}Dusk{/color}"
    EveningDay = "{color=#ffe9b5}Evening{/color}"
    MidnightDay = "{color=#ffe9b5}Midnight{/color}"

    UseFancyScrollBar = False

    #config.use_cpickle = False
    config.history_length = 150

    npcProgHolder = []
    eventProgHolder = []
    advenProgHolder = []
    purchasing = 0
    amountToBuy = 1

    LoopedList = []
    LoopedListHolder = []
    teiHold = -1
    callLoopTei= []
    holdChoiceForLoop = []

    removedSkillPosition = []
    removedSkill = []

    manualSort = 0
    swappingSkill = -1

    overrideCombatMusic = 0
    musicLastPlayed = [""]

    buff = ""
    postNote = ""
    vfx = "white.png"
    vfx2 = "white.png"
    vfx3 = "white.png"
    spiralVFX = "white.png"

    spiritLost = 0

    expGiven = 1

    shifting = 1


    playBehind = 0
    sprialSpeed = 5
    spiralOpacity = 0.8

    pendulumSpeed = 5
    pendulumSway = 45
    pendulumVFX = "white.png"

    bounceAmount = 10
    bounceSpeed = 0.6

    #currently frame animation stuff
    animationList = [ ]
    animationChoice = ""
    currentAnimationImg = 1
    animationSpeed = 0.5
    animationTime = 0

    #currently frame animation stuff
    animationList2 = [ ]
    animationChoice2 = ""
    currentAnimationImg2 = 1
    animationSpeed2 = 0.5
    animationTime2 = 0

    #currently frame animation stuff
    animationList3 = [ ]
    animationChoice3 = ""
    currentAnimationImg3 = 1
    animationSpeed3 = 0.5
    animationTime3 = 0

    pulsingList = []
    pulsingChoice = ""
    currentPulsingImg = 0
    pulseZoom = 1.0
    pulsingSpeed = 1.0
    pulsingOpacity = 1.0
    pulsingTime = 0

    pulsingList2 = []
    pulsingChoice2 = ""
    currentPulsingImg2 = 0
    pulseZoom2 = 1.0
    pulsingSpeed2 = 1.0
    pulsingOpacity2 = 1.0
    pulsingTime2 = 0

    pulsingListRand = []
    pulsingChoiceRand = ""
    currentPulsingImgRand = 0
    pulseZoomRand = 1.0
    pulsingSpeedRand = 1.0
    pulsingOpacityRand = 1.0
    pulsingTimeRand = 0

    CurrentIteration = 0


    BarrageOpacity = 0
    barrageList = []
    barrageChoice = ""
    currentBarrageImg = 0
    BarrageTime = 0
    BarrageSpeed = 0

    barrageFadeList = []
    barrageFadeChoice = ""
    currentBarrageFadeImg = 0
    BarrageFadeTime = 0
    BarrageFadeSpeed = 0
    barragefadeSkip = 0

    BarrageOpacity2 = 0
    barrageList2 = []
    barrageChoice2 = ""
    currentBarrageImg2 = 0
    BarrageTime2 = 0
    BarrageSpeed2 = 0

    barrageFadeList2 = []
    barrageFadeChoice2 = ""
    currentBarrageFadeImg2 = 0
    BarrageFadeTime2 = 0
    BarrageFadeSpeed2 = 0
    barragefadeSkip2 = 0

    lastCombatSongPosition = ""
    lastCombatSong = ""



    quickMenuOn = 0

    selectingCircleBar = 0

    needToUpdate = 0
    critChance = 0
    critDamage = 0
    fontsize = 35
    HPfontsize = 25
    theXpadding = 12
    theYpadding = 10
    tt = Tooltip("")

    InStanceEvade = 0
    OutOfStanceEvade = 0
    AccuracyBonus = 0
    InStanceAccuracyBonus = 0

    effectiveText = ""
    statusEffectiveText = ""

    LastLine = ""
    LastSpeaker = ""

    whatStatisIt = ""
    whatItemIsIt = ""
    whatSkillIsIt = ""
    whatPerkIsIt = ""
    refinedSkillList = []



    theTarget = ""
    theAttacker = ""

    triggerItemUse = 0

    kissBarOnce = 0


    SexWords = sexBank
    SexAdjectives = sexAdjectiveBank

    randomMenuLine = renpy.random.choice(lineBank)

    config.rollback_enabled = False
    config.save_dump = True


    showMoreFetish = 0
    getFetish = 0
    setThisFetish = 0
    tryRemoveThisStance = 0


    ###############################MAKE LISTS###############################
    jsonDirList = []
    jsonDir = filter_list_files("Json/")
    #print jsonDir
    for dirData in jsonDir:
      if re.match(".*/_.*", dirData):
        pass
      else:
        jsonDirList.append(dirData)
    #print jsonDirList

    modDir = filter_list_files("Mods/")
    #print modDir
    modDirList = []
    for dirData in modDir:
      if re.match(".*/_.*", dirData):
        pass
      else:
        if dirData.endswith(".json"):
          modDirList.append(dirData)
    #print modDirList
    jsonList = jsonDirList + modDirList
    #print(jsonList)
    ###############################FETISH LIST###############################
    FetishList = []
    for each in dynamic_loader(".*/Fetishes/.*"):
      #print each
      fileName = renpy.file(each).read().decode("utf-8")
      try:
          currentData = json.loads(fileName)
      except:
          PrintException(fileName)

      for each in currentData['FetishList']:
          newFetish = Fetish()

          newFetish.name = each["Name"]
          newFetish.Level = int(each["BaseLevel"])
          newFetish.Type = each["Type"]
          newFetish.CreationOn = each["CreationOn"]
          newFetish.CreationOff = each["CreationOff"]
          FetishList.append(newFetish)


    creating = 1
    hasResPoints = 0
    loadingDatabaseType = 0
    respeccing = 0



    perkChosen = ""
    perkBuyUse = False

    InIntro = 0

init:
    $ config.save_dump = False
    $ _game_menu_screen = None

    transform invisible:
        alpha 0.0

    $ SkillsDatabase = []
    $ ItemDatabase = []
    $ MonsterDatabase = []
    $ PerkDatabase = []
    $ LocationDatabase = []
    $ EventDatabase = []
    $ AdventureDatabase = []

    $ LevelingPerkDatabase = []
    $ PerkDatabaseLVLDisplay = []
    $ AdditionalLevelPerks = []

    $ LocationList = []

    $ EndOfDayList = []
    $ TimePassedList = []
    $ StepTakenList = []
    $ EndOfTurnList = []
    $ EndOfCombatList = []
    $ StartOfTurnList = []
    $ StartOfCombatList = []
    $ OnPlayerClimaxList = []
    $ DreamList = []

    $ WaiterBrothel = []
    $ BarBrothel = []
    $ GloryHoleBrothel = []
    $ DayBrothel = []
    $ monSkillChoice = []

    $ config.layers = ['master', 'transient', 'visualEffects', 'screens',  'overlay' ]
    #$ config.say_layer = "sayScreen"


    define config.gl2 = True

    call UpdateGameVersionVariables from _call_UpdateGameVersionVariables
    call InitInventory from _call_InitInventory
    call Functions from _call_Functions
    call specialEffects from _call_specialEffects
    call playerClass from _call_playerClass
    call monsterClass from _call_monsterClass
    call AdventuringDeckClass from _call_AdventuringDeckClass
    call combatFunctions from _call_combatFunctions
    call loadDatabase from _call_loadDatabase


    $ PlayerHue = 1.0
    $ PlayerBrightness = 1.0
    $ PlayerOpacity = 1.0
    $ PlayerSaturation = 1.0
    $ PlayerSaturationR = 0.2126
    $ PlayerSaturationG = 0.7152
    $ PlayerSaturationB = 0.0722
    $ PlayerTint = "#FFFFFF"

    $ PlayerDisplay = "Body"

    transform CharacterBrightness:
        matrixcolor BrightnessMatrix(PlayerBrightness-1)
    transform CharacterColor:
        matrixcolor HueMatrix(PlayerHue)
    transform CharacterOpacity:
        matrixcolor OpacityMatrix(PlayerOpacity)
    transform CharacterSaturation:
        matrixcolor SaturationMatrix(PlayerSaturation,(PlayerSaturationR, PlayerSaturationG, PlayerSaturationB))
    transform CharacterTint:
        matrixcolor TintMatrix(PlayerTint)


    $ PlayerSilHue = 1.0
    $ PlayerSilBrightness = 1.0
    $ PlayerSilOpacity = 0.9
    $ PlayerSilSaturation = 1.0
    $ PlayerSilSaturationR = 0.2126
    $ PlayerSilSaturationG = 0.7152
    $ PlayerSilSaturationB = 0.0722
    $ PlayerSilTint = "#FFFFFF"

    transform CharacterSilBrightness:
        matrixcolor BrightnessMatrix(PlayerSilBrightness-1)
    transform CharacterSilColor:
        matrixcolor HueMatrix(PlayerSilHue)
    transform CharacterSilOpacity:
        matrixcolor OpacityMatrix(PlayerSilOpacity)
    transform CharacterSilSaturation:
        matrixcolor SaturationMatrix(PlayerSaturation,(PlayerSilSaturationR, PlayerSilSaturationG, PlayerSilSaturationB))
    transform CharacterSilTint:
        matrixcolor TintMatrix(PlayerSilTint)

    transform CharacterColorNot:
        matrixcolor SaturationMatrix(0,(0.2126, 0.7152, 0.0722)) #doesnt seem to tint or colorize properly afterwards regardless if set to zero. nbase images wortk better.
        matrixcolor ColorizeMatrix("AF7351", "E3BBA5") #basically useless for this.

        matrixcolor TintMatrix("#DEC4A1")
        matrixcolor TintMatrix("#AF826B")
        matrixcolor TintMatrix("#F6BADC")
        matrixcolor TintMatrix("#73BCFF")


    $ Quake = Shake((0, 0, 0, 0), 6000.0, dist=5)
    $ Crash = Shake((0, 0, 0, 0), 0.5, dist=20)
    $ Explosion = Shake((0, 0, 0, 0), 0.75, dist=35)
    $ LongExplosion = Shake((0, 0, 0, 0), 3.0, dist=35)

    $ motionSpeed = 0.3
    $ motionDistance = 10

    $ GlobalMotion = ""

    python:
        style.smallerTextButton = Style(style.button_text)
        style.smallerTextButton.size = 20
        style.smallerTextButton.color = "#E470B2"
        style.smallerTextButton.hover_color = "#F6BADC"


    image bg = "#3f3f3f"
    image bg heaven = "heaven.png"
    image bg combat = "combat.png"
    image bg forest = "forest.png"
    image bg town = "standIn.png"

    image splashScreen = "SplashPage.png"

    image chest = "Monsters/Mimic/mimic_closed.png"
    image bag = "Monsters/Stella/BagPlain.png"

    transform CharacterZoom:
        zoom 0.75

    transform statusIconZoom:
        zoom 0.25

    transform LossSceneZoom:
        zoom 1.0

    transform QuickMenuFade:
        on show:
            alpha 0.0
            linear 1.0 alpha 1.0
        on hide:
            linear 0.5 alpha 0.0



    $ God = Character(_('???'),
                            what_prefix='"',
                            what_suffix='"')

    $ Goddess = Character(_('Goddess Venereae'),
                            what_prefix='"',
                            what_suffix='"')


    $ Lily = Character(_('Lillian'),
                            what_prefix='"',
                            what_suffix='"')

    $ shopKeeper = Character(_('Amber'),
                            what_prefix='"',
                            what_suffix='"')

    $ innKeeper = Character(_('Vivian Von Kaar'),
                            what_prefix='"',
                            what_suffix='"')

    $ guildDesk = Character(_('Elena'), #Farshaw
                            what_prefix='"',
                            what_suffix='"')

    $ Librarian = Character(_('Elly'), #Farshaw
                            what_prefix='"',
                            what_suffix='"')



    $ Perpetua = Character(_('Perpetua'), #Slime Girl
                            what_prefix='"',
                            what_suffix='"')

    $ srsly = Character(_('Allura'),
                            what_prefix='"',
                            what_suffix='"')

    $ Aife = Character(_('Aife'), #elf
                            what_prefix='"',
                            what_suffix='"')

    $ Nihltu = Character(_('Nihltu'), #Demon Commander 4
                            what_prefix='"',
                            what_suffix='"')

    #places
    #Lucidia - Monster Continent
    #Fertilia - Human continent
    #Adventum - Adventuring School!



label splashscreen:
    if persistent.shownSplash is True:
        return

    play music "music/Forest/Starry sky.mp3" fadeout 1.0 fadein 1.0
    show splashScreen
    $ persistent.shownSplash = True
    pause

    return

# The game starts here.
label start:
    define config.after_load_callbacks = [loadPtCEConfigs]
    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    $ persistantMonSetData = []
    $ renpy.block_rollback()
    $ config.rollback_enabled = False
    $ renpy.retain_after_load()
    #load in all the stuff
    $ TempSensitivity = BodySensitivity()
    $ CurrentVersion = config.version
    python:
      ###############################FETISH LIST###############################
      FetishList = []
      for each in dynamic_loader(".*/Fetishes/.*"):
        #print each
        fileName = renpy.file(each).read().decode("utf-8")
        try:
            currentData = json.loads(fileName)
        except:
            PrintException(fileName)

        for each in currentData['FetishList']:
            newFetish = Fetish()

            newFetish.name = each["Name"]
            newFetish.Level = int(each["BaseLevel"])
            newFetish.Type = each["Type"]
            newFetish.CreationOn = each["CreationOn"]
            newFetish.CreationOff = each["CreationOff"]
            FetishList.append(newFetish)
    python:
        playerGone = 0
        playerCloseMark = 0
        monsterEncounter = []
        trueMonsterEncounter = []
        DefeatedEncounterMonsters = []
        finalDamage = 0
        lastAttack = ""
        theLastAttacker = ""
        critText = ""
        display = ""
        displayOrder = []
        attackerName = ""
        attackerNameStance2 = ""
        attackerNameStance3 = ""
        attackerNameStance4 = ""
        attackerNameStance5 = ""
        targetName = ""

        SPLossLow = 35
        SPLossHigh = 65
        stanceGo = "False"
        AIStruggle = 0
        ExpPool = 0
        LootDrops = []
        MoneyDrops = 0
        canRun = True
        RanAway = "False"
        Run = "True"
        canbreakFree = False
        combatChoice = ""
        justEscapedStance = 0
        SkillNumber = 0
        ItemNumber = 0
        index = 0
        moveFilter = ""
        runBG = ""

        DataLocation = 0
        isEventNow = 0

        DayNumber = 1
        TimeOfDay = copy.deepcopy(Morning)


    $ orgasmCount = 0
    $ lossCount = 0

    $ difficulty = "Normal"

    $ bg = ""

    $ VisualEffect = ""
    $ VisualEffect2 = ""
    $ VisualEffect3 = ""

    $ MotionEffect = ""
    $ MotionEffectLoop = 0

    $ CurrentIteration = len(SkillsDatabase) + len(ItemDatabase) + len(MonsterDatabase) + len(PerkDatabase) + len(LocationDatabase) + len(EventDatabase) + len(AdventureDatabase)

    $ Speaker = Character(_(''))
    $ extension = ""
    $ currentLocation = ""
    $ currentNPC = 0
    $ currentChoice = 0
    $ introduced = 1
    $ choiceName = ""
    $ HoldChoice = 0
    $ HoldChoiceNumber = 0

    $ rehauled = 1
    $ progressionBoost = 1

    $ attacker = Monster(Stats())
    $ defender = Monster(Stats())
    $ skillChoice = Skill()

    $ DisplayInventory = 1
    $ useItem = 0
    $ inventoryTarget = 0
    $ inventoryETarget = 0
    $ ItemToolTip = 0
    $ InventoryAvailable = False
    $ InvTopRowAlignmentY = 0.265
    $ morePages = False
    $ blankHoverValue = 0

    $ DisplaySkills = 1
    $ useSkill = 0
    $ skillTarget = 0
    $ skillToolTip = 0

    $ SkillTopRowAlignmentY = InvTopRowAlignmentY + 0.15

    $ TargetingEquipSlot = 0
    $ equippingItem = 0
    $ unequippingItem = 0
    $ RemovingEquipment = 0

    $ targetLocation = 0
    $ adventureDeck = []
    $ explorationDeck = []
    $ monsterDeck = []
    $ eventDeck = []
    $ QuestSlot = Event()
    $ tabToggle = 1
    $ currentCardName = ""
    $ currentEvent = 0
    $ deckProgress = 0
    $ questTaken = 0
    $ onAdventure = 0
    $ AdventureHolder = AdventuringDeck()

    $ displayHealthInEvent = 1

    $ Rut = False

    $ debt = 1000000
    $ debtPayed = "False"

    $ tribute = 0
    $ tributeStep = 0


    $ lossCount = 0
    $ winCount = 0


    $ TempFetishes = copy.deepcopy(FetishList)
    $ player = Player()
    $ player._resetPlayerAtStart(copy.deepcopy(FetishList))

    $ tentativeStats = copy.deepcopy(player)


    #make base player
    $ povname = ""
    $ pov = DynamicCharacter("povname", color=(192, 64, 64, 255))

    $ displayingScene = Dialogue()
    $ actorNames = ["", "", "", "", "", "", "", "", "", "", "", ""]


    $ DialogueIsFrom = ""
    $ SceneCharacters = ""
    $ showOnSide = 0

    python:
        player.stats.isPlayer = "True"
        addSkillTo("Kiss", player)
        addSkillTo("Breast Caress", player)
        addSkillTo("Grope Ass", player)
        addSkillTo("Penetrate", player)
        addSkillTo("Thrust", player)

        player.inventory.give("Calming Potion", 5)
        player.inventory.give("Energy Potion", 3)
        player.inventory.give("Anaph Herb", 3)

        player.inventory.money = 1000
        player.CalculateStatBoost()
        #player.perks.append(PerkDatabase[getFromName("Alluring", PerkDatabase)])


    $ _game_menu_screen="save"
    $ skippedIntro = 0


    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []


    $ loadingDatabaseType = 1


    call loadDatabase from _call_loadDatabase_2
    $ loadPtCEConfigs()
    $ _game_menu_screen = "ON_CharacterDisplayScreen" if ptceConfig.get("hardcoreMode") else "save"

    $ player.name = "Adventurer"

    scene bg town

    menu watchIntro:
        "Watch Intro":
            jump Intro
        "Skip Intro":
            jump SkipIntro


    label SkipIntro:
        scene bg heaven
        $ player.name = renpy.input(_("What's your name?"), length=13) or _("Hero")
        $ player.name.strip()
        $ save_name = copy.deepcopy(player.name)
        $ tentativeStats = copy.deepcopy(player)
        $ skippedIntro = 1
        "(Any unspent points will be lost after character creation.)"
        jump characterCreation
        #jump to char creator
        ##Goto Town

    label Intro:
        $ InIntro = 1
        $ currentEvent = 0
        $ DataLocation = 0

        $ DialogueIsFrom= "Event"
        $ displayingScene =  EventDatabase[getFromName("Intro Part 1", EventDatabase)].theEvents[0]

        $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
        $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
        if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
            $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name

        call displayScene from _call_displayScene_5

        scene bg heaven
        window show dissolve
        "A serene female voice is heard from all around you."

        $ God = Character(_('Goddess Venereae'),
                                what_prefix='"',
                                what_suffix='"')
        God "I am the Goddess Venereae, and I have chosen you. You are destined to defeat the Demon Queen."
        "She seems to mutter to herself for a moment."
        God "Now let's see... Male... Graduated Adventum... Ooo top of your class..."
        "She coughs before asking you something important."

        $ player.name = renpy.input(_("Oh brave hero. What is your name?"),  length=13) or _("Hero")
        $ player.name.strip()
        $ save_name = copy.deepcopy(player.name)
        God "[player.name!t]... a fitting name for a hero..."
        God "Now... let's see your heroic qualifications..."
        "(Any unspent points will be lost after character creation.)"
        $ tentativeStats = copy.deepcopy(player)
        jump characterCreation
    label creatorEnd:
        hide screen  CreatorDisplay
        call uncapStats from _call_uncapStats
        $ player.statPoints = 0
        $ player.SensitivityPoints = 0
        $ creating = 0
        $ tt = Tooltip("")
    if skippedIntro == 0:
        God "Ah, that should probably do."
        God "Now awaken chosen hero. Your adventure awaits..."

        $ bg = "town.png"
        show screen ON_HealthDisplayBacking #(_layer="hplayer")
        show screen ON_HealthDisplay #(_layer="sayScreen")
        show screen DisplayBG (_layer="master")
        $ InIntro = 1
        $ currentEvent = 0
        $ explorationDeck = []
        $ DataLocation = getFromName("Intro Part 2", EventDatabase)
        $ DialogueIsFrom= "Event"
        $ displayingScene =  EventDatabase[DataLocation].theEvents[0]

        $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
        $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
        if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
            $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name
        call displayScene from _call_displayScene_6


    $ explorationDeck = []
    $ SceneCharacters = []
    $ InIntro = 0

    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)

        $ i = 0
        while i < len(holdFetish):
            $ TempFetishes[i].Level = holdFetish[i].Level

            $ i += 1
    $ player.stats.refresh()
    jump Town

    # This ends the game.

    return
