# PtCE Mod

This is a challenge mod, which changes a lot of fundamental gameplay and balancing aspects of MGD.

THIS MOD WILL NOT WORK WITH VANILLA SAVEFILES! 

## Installation and Version
This mod is supposed to work with the vanilla game Alpha-v24.3a.
It has been developed and tested for the pc version on linux (but should work on windows the same).
Before installing the mod, it is advisable to create a copy of your games installation.
To install the mod just copy the game folder into the folder where your vanilla game is located and choose "overwrite files" when asked.

## Features
PtCE has a number of different features, most of which can be toggled and configured to your liking. If you want to change settings, you just need to edit the json file found under "/game/gamecode/ptce/config.json".
If you change the "useVanilla" property to true for anc of these features, you disable the feature.
In many cases you can also change the calculation that is used for a feature and define your own calculation. 

### Fetishes
The core feature and biggest gameplay change in this mod is how fetishes are handled.
In vanilla fetishes are only increased via gaining perks or through certain events. Almost all events only increase your temporary fetish levels, which can be reset at the church for a fee.
Usually only fetish levels gained from perks are permanent. In PtCE you will gain fetish Levels A LOT more rapidly and thus managing them is more important.
The LevelCap for Fetishes is increased to 1000 instead of 100.
The status screen also now not only shows your overall fetish level, but your permanent fetish level as well.
Example: "Legs Lvl: 120 / 45" would mean, that you currently have a fetish level of 120 overall, but you can reduce it down to 45 in the church.

Whenever an enemy hits you with an attack, it will increase your temporary fetish levels by a small amount. Which fetishes increase depends on the attack, while the amount is based on the enemies Allure stat.

Whenever an enemy makes you loose spirit, it will increase your permanent fetish levels by a small amount and your temporary fetishes by a medium amount for each point of spirit lost.

Whenever you actually loose in combat to an enemy your permanent fetish levels will increase by a medium amount.

There currently is no fetish gain in Event Scenes, unless the scene includes the Function "HitPlayerWith" and this is counted as being hit in battle. 

You can exclude specific fetishes from this feature, by adding them to the array under "bannedFetishes" in the config file.

You can customize the modifiers for temporary and permanent fetish gain for each difficulty and for each type of fetishGain (OnHit, OnSpiritLoss and OnCombatLoss)

There is also a popup in the top right corner, which tells you whenever you gained any fetish levels.

### EXP and Ero scaling
In the vanilla game it is really easy to grind, overlevel and gain a ton of Eros. That is pretty much, because EXP scaling from being much higher Level than your opponent is pretty much floored at 70% EXP and Eros isn't scaled at all.

In PtCE EXP and Eros penalties from being too high Level are much harsher and not floored. They also depend on your difficulty setting. While "Easy" allows you to still gain EXP from an Enemy up to 10 levels below you, choosing "Hard" will prevent you from gaining EXP from an enemy, which is 6 levels below you.

With the default calculation Eros gain has a flat 2.5%/5%/10% penalty per level above your enemy on Easy/Normal/Hard to a floor of 75%/50%/25% Eros gain.

### Smarter enemy AI
When an enemy uses a move during combat, they will learn how effective moves with that moves fetish and sensitivites are. Enemies will prioritize moves based on their knowledge and try to avoid moves which target areas where the player is strong against. Sometimes avoiding weak moves even can mean that an enemy tries to struggle out of a stance, since it now knows that all of it's moves now would be weak against you.
This information is learned on a per-enemy-basis and only remembered for the duration of a single combat.

### Changed Cost of Purging Temporary Fetishes
In Order to counteract the increase temporary fetish gain a bit, the cost of removing them in the church has been greatly reduced.
With the default config purging now costs 5 Eros per temporary level dwon from 25 in Vanilla.

### HardcoreMode
PtCE comes with a "hardcoreMode". In this mode (quick-)saving and loading are both disabled.
The only way to load a save is from the title menu and the only way to save a game is now via a new option in the church (The confession booth).
While this doesn't fully prevent someone from savescumming, it makes it quite a bit more difficult.

If you want to enable this feature, you just need to set "hardcoreMode" to true in the config. This is not enabled by default. 