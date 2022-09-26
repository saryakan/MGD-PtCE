init python:
    import threading

    global fetishGainQueue
    fetishGainQueue = []

    def dequeueFetishGain():
        if (len(fetishGainQueue) < 1):
            renpy.hide_screen("fetishGainDisplay")
        else:
            fetishGainQueue.pop()
            renpy.show_screen("fetishGainDisplay")
    
    def enqueueFetishGain(fetishName, levelsGained, gainType):
        fetishGainQueue.append((fetishName, levelsGained, gainType))
        threading.Timer(3, dequeueFetishGain).start()
        renpy.show_screen("fetishGainDisplay")

style fetishGainDisplayStyle:
    xalign 0.98
    spacing 3

screen fetishGainDisplay():
    tag fetishGain
    
    vbox:
        style "fetishGainDisplayStyle"
        for element in fetishGainQueue:
            $ fetishName, levelsGained, gainType = element
            frame:
                label "[gainType] [fetishName]+[levelsGained]"
    
    on "show" action [renpy.restart_interaction]