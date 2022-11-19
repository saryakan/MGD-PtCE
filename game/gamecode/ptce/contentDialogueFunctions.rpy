init 1 python:
    import json

    MOD_PREFIX = "ptce_content"

    global PTCE_CALCULATIONS
    PTCE_CALCULATIONS = {}

    def storeCalculationForTarget():
        global lineOfScene, displayingScene, monsterEncounter, CombatFunctionEnemytarget, player
        name = displayingScene[lineOfScene + 1]
        calculations = json.loads(displayingScene[lineOfScene + 2])
        targetString = displayingScene[lineOfScene + 3]
        target = player if targetString == "Player" else monsterEncounter[CombatFunctionEnemytarget]
        PTCE_CALCULATIONS[name] = calculateAll(calculations, target)
        lineOfScene += 3
    
    def printCalculationResult():
        global lineOfScene, displayingScene
        name = displayingScene[lineOfScene + 1]
        lineOfScene += 1
        renpy.say("name: {0} result: {1}".format(name, PTCE_CALCULATIONS.get(name, "null")))

    
    def skipNLinesAndRemoveSelf():
        global lineOfScene, displayingScene
        toSkip = int(displayingScene[lineOfScene + 1]) - 1
        displayingScene.pop(lineOfScene)
        displayingScene.pop(lineOfScene)
        lineOfScene += toSkip

    def ifCheck():
        global lineOfScene, displayingScene
        
        lineOfScene += 1
        condition = renpy.python.py_eval(displayingScene[lineOfScene])
        startOfBlock = lineOfScene + 1
        endOfIfBranchIndex = findEndOfBlockIndex(startOfBlock, displayingScene, ["else", "endif"])
        if displayingScene[endOfIfBranchIndex] is "endif":
            if condition:
                displayingScene.insert(endOfIfBranchIndex - 1, "1")
                displayingScene.insert(endOfIfBranchIndex - 1, "skipNLinesAndRemoveSelf")
            else:
                lineOfScene = endOfIfBranchIndex
            return
        
        if displayingScene[endOfIfBranchIndex] is "else":
            endOfElseBlockIndex = findEndOfBlockIndex(endOfIfBranchIndex + 1, displayingScene, ["endif"])
            if condition:
                displayingScene.insert(endOfIfBranchIndex - 1, endOfElseBlockIndex - endOfIfBranchIndex +1)
                displayingScene.insert(endOfIfBranchIndex - 1, "skipNLinesAndRemoveSelf")
            else:
                displayingScene.insert(endOfElseBlockIndex - 1, "1")
                displayingScene.insert(endOfElseBlockIndex - 1, "skipNLinesAndRemoveSelf")
                lineOfScene = endOfIfBranchIndex
            return
        
        raise Exception("Something went wrong while trying to parse an if-else statement in a scene.")
        
    def findEndOfBlockIndex(startOfBlock, displayingScene, terminatorTokens):
        terminatorsNeeded = 1
        ptr = startOfBlock

        while terminatorsNeeded > 0:
            if displayingScene[ptr] = "if":
                terminatorsNeeded += 1
            
            if displayingScene in terminatorTokens:
                terminatorsNeeded -= 1
            
            ptr += 1
        
        return ptr - 1
