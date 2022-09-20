# PtCE Mod

This is a mod is a challenge mod, which changes a lot of fundamental gameplay and balancing aspects of MGD.

THIS MOD WILL NOT WORK WITH VANILLA SAVEFILES! 
PtCE savefiles should work with a vanilla game though.

## Version
This mod is supposed to work with the vanilla game Alpha-v24.3a.
It has been developed and tested for the pc version on linux (but should work on windows the same).

## Features
Most of these Features can be configured or even disabled entirely by editing the file in "./game/gamecode/ptce/config.json"

### Fetishes
Probably the core feature and biggest gameplay change in this mod is how fetishes are handled.
In vanilla fetishes are only increased via gaining perks or through certain events. Almost all events only increase your temporary fetish levels, which can be reset at the church for a fee.
Usually only fetish levels gained from perks are permanent. In PtCE you will gain fetish Levels A LOT more rapidly and thus managing them is more important.
The LevelCap for Fetishes is increased to 10000 instead of 100.
To compensate, the cost of resetting your temporary fetish levels has been reduced significantly down from 25 Eros per level to 5 Eros per level. The status screen also now not only shows your overall fetish level, but your permanent fetish level as well.
Example: "Legs Lvl: 120 / 45" would mean, that you currently have a fetish level of 120 overall, but you can reduce it down to 45 in the church.

Whenever an enemy hits you with an attack, it will increase your temporary fetish levels by a small amount. Which fetishes increase depends on the attack, while the amount is based on the enemies Allure stat.

Whenever an enemy makes you loose spirit, it will increase your permanent fetish levels by a moderate amount for each point of spirit lost.

Whenever you actually loose in combat to an enemy your permanent fetish levels will increase by a large amount.

Whenever the new Function "PlayerOrgasmFromFetish" is called/used in a scene it counts the same as if that enemy is making you loose spirit as well. However it only counts if you actually loose spirit. So if you are already at 0 spirit e.g. in a loss scene, you won't actually gain any fetish levels. That also means you don't have to worry about fetish gain in scenes where there is no spirit loss like in the brothel scenes.

If a skill does not have a fetish set in it's list, instead we look at it's required or initiated stances and try to determine a fetish from those.

You can exclude specific fetishes from this feature, by adding them to the array under "bannedFetishes" in the config file.

### EXP and Ero scaling
In the vanilla game it is really easy to grind, overlevel and gain a shit ton of Eros. That is pretty much, because EXP scaling from being much higher Level than your opponent is pretty much floored at 70% EXP and Eros isn't scaled at all.

In PtCE EXP and Eros penalties from being too high Level are much harsher and not floored. They also depend on your difficulty setting. While "Easy" allows you to still gain EXP from an Enemy up to 10 levels below you, choosing "Hard" will prevent you from gaining EXP from an enemy, which is 6 levels below you.

Eros gain has a flat 2.5%/5%/10% penalty per level above your enemy on Easy/Normal/Hard to a floor of 75%/50%/25% Eros gain.

You can disable these features and use vanilla scalings by setting "useVanillaErosMod" and/or "useVanillaExpMod" to true.

### Smarter enemy AI
During combat enemies will remember the fetishes of moves, which were very effective on you and give these moves preferential treatement whenever they decide which move to go for.
This is learned on a per-enemy-basis and only remembered for the duration of a single combat.

You can disable this feature by setting "enemiesLearnWeaknesses" to false in the config.

### HardcoreMode
PtCE comes with a "hardcoreMode". In this mode (quick-)saving and loading are both disabled.
The only way to load a save is from the title menu and the only way to save a game is now via a new option in the church (The confession booth).
While this doesn't fully prevent someone from savescumming, it makes it quite a bit more difficult.

If you want to enable this feature, you just need to set "hardcoreMode" to true in the config. This is not enabled by default. 

## Planned Features and Content

- Some way to reduce or reset "permanent" Fetish gain, which would involve a bigger cost than just some eros. Maybe some difficult side-quests, or maybe needing to farm rare consumable drops or something.
- Limit the amount of consumables you can use during an adventure in some form. This is probably quite complicated, and might not work without an overhaul of the whole inventory system, which would be quite hard to do without breaking compatibility with other content mods.
- Further improvements to enemy AI learning about your weaknesses. For some unique enemies it would e.g. make sense, when they remember them beyond a battle. Currently there is also weirdness, because they don't recognize whether a move was effective, based on fetishes or sensitivities. They also don't prioritize moves based on effectiveness, once a move is categorized as effective, it has the same priority as all other effective moves. Enemies should probably also learn about moves, which are not very effective on you.
- Small perks for each Fetish you choose at character creation.

### New Event Functions
I needed to introduce two new PtCE custom event functions:

- "SaveMenu" simply opens up the save menu. Needed for the confession booth event and to access the save menu in hardcoreMode
- "PlayerOrgasmFromFetish" works like "PlayerOrgasm" but after spirit lost also takes in another variable, which is the name of the fetish which will be increased as per PtCE rules. Example usage: ["PlayerOrgasmFromFetish", "1", "Feet"]

### Known Incompatabilities and Issues
_Should_ be compatible with "Quickie" and "Monster arousal display" 