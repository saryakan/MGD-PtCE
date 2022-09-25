init -1 python:
    import json

    PTCE_CONFIG_PATH = renpy.loader.transfn("gamecode/ptce/config.json")

    global ptceConfig

    DEFAULT_CONFIG = {
        "fetishGain": {
            "fetishMaxLevel": 1000,
            "bannedFetishes": [],
            "stancesByFetish": {
                "Feet": ["Footjob", "Feet Pussy", "Behind Footjob", "Electric Massage"],
                "Legs": ["Thighjob", "Kneejob"],
                "Monstrous": ["Tail Fuck", "Slimed", "Slimed 50%", "Slimed 100%", "Tailjob"],
                "Ass": ["Anal", "Face Sit"],
                "Oral": ["Blowjob"],
                "Breasts": ["Titfuck", "Breast Smother", "Nursing"],
                "Sex": ["Sex"],
                "Kissing": ["Making Out"]
            },
            "calculation": { "calculationType": "squareRoot", "rootMultiplier": 5, "flatMultiplier": 0.1, "flatBonus": 0 },
            "multipliers": {
                "onHitTemp": { "Easy": 0.05, "Normal": 0.1, "Hard": 0.2 },
                "onHitPerm": { "Easy": 0, "Normal": 0, "Hard": 0 },
                "onSpiritLossTemp": { "Easy": 0.65, "Normal": 0.8, "Hard": 0.95 },
                "onSpiritLossPerm": { "Easy": 0.1, "Normal": 0.2, "Hard": 0.3 },
                "onCombatLossTemp": { "Easy": 0, "Normal": 0, "Hard": 0 },
                "onCombatLossPerm": { "Easy": 0.75, "Normal": 1, "Hard": 1.25 }
            }
        },
        "expGain": {
            "useVanilla": False,
            "calculation": { "calculationType": "quadratic", "quadraticMultiplier": -1, "flatMultiplier": 0, "flatBonus": 0 },
            "multiplier": { "Easy": 0.01, "Normal": 0.021, "Hard": 0.03 },
            "floor": { "Easy": 0, "Normal": 0, "Hard": 0 }
        },
        "erosGain": {
            "useVanilla": False,
            "calculation": { "calculationType": "quadratic", "quadraticMultiplier": 0, "flatMultiplier": -1, "flatBonus": 0 },
            "multiplier": { "Easy": 0.025, "Normal": 0.05, "Hard": 0.1 },
            "floor": { "Easy": 0.75, "Normal": 0.5, "Hard": 0.25 }
        },
        "fetishPurge": {
            "useVanilla": False,
            "calculation": { "calculationType": "quadratic", "quadraticMultiplier": 0, "flatMultiplier": 5, "flatBonus": 0 }
        },
        "combatAI": {
            "enemiesLearnWeaknesses": True,
            "enemiesLearnStrengths": True
        },
        "hardcoreMode": False
    }

    ptceConfig = DEFAULT_CONFIG

    def loadPtCEConfigs():
        global ptceConfig
        with open(PTCE_CONFIG_PATH, "r") as file:
            loadedConfig = json.load(file)
            ptceConfig = {}
            ptceConfig.update(DEFAULT_CONFIG)
            ptceConfig.update(loadedConfig)