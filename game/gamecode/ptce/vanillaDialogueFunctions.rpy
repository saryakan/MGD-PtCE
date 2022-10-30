init 1 python:
    def vanillaPlayerSpeaks():
        global lineOfScene, readLine, Speaker

        Speaker = Character(_(player.name+attackTitle), what_prefix='"', what_suffix='"')
        lineOfScene += 1
        readLine = 1
    
    registerDialogueFunction("vanilla", "PlayerSpeaks", vanillaPlayerSpeaks)