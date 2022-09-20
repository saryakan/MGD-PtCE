################################################################################
## Initialization
################################################################################

init offset = -1

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True


style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb_offset 2

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)


################################################################################
## In-game screens
################################################################################
## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"


    window:
        id "window"

        if who is not None:

            window:

                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menuDetector():

        fixed:
            imagebutton:
                idle "textButtonBlank.png"
                hover "textButtonBlank.png"
                insensitive "textButtonBlank.png"
                xalign 0.5
                yalign -0.01
                xsize 1000
                action [NullAction()] hovered [SetVariable ("quickMenuOn", 1)] unhovered [SetVariable ("quickMenuOn", 0)]


screen quick_menu():


    #timer 0.2 action Hide("quick_menu", dissolve)

    ## Ensure this appears on top of other screens.
    zorder 300

    if quick_menu and quickMenuOn == 1:
        
        hbox:

            style_prefix "quick"

            xalign 0.5
            yalign 0.0

            textbutton _("History") action ShowMenu('history') hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True) hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
            textbutton _("Auto") action Preference("auto-forward", "toggle") hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
            textbutton _("Character") action [
                tt.Action(""),
                SetVariable("useItem", 0),
                SetVariable ("inventoryTarget", 0),
                ShowMenu("ON_CharacterDisplayScreen"),
                Function(cmenu_resetMenu),
                SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
                ] hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
            if not ptceConfig["hardcoreMode"]:
                textbutton _("Save") action ShowMenu('save') hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
                textbutton _("Q.Save") action QuickSave() hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
                textbutton _("Q.Load") action QuickLoad() hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade
            textbutton _("Prefs") action ShowMenu('Options') hovered [SetVariable ("quickMenuOn", 1)] at QuickMenuFade

    hbox:
        style_prefix "quick"

        xalign 0.025
        yalign 0.98
        text _(TimeOfDay) size 28


# Broken code to try and auto-hide the quick menu bar - unhovered events don't always fire

#    zorder 300
#    default showQuickMenu = False

#    if quick_menu:
#        button:
#            hovered SetScreenVariable("showQuickMenu", True)
#            unhovered SetScreenVariable("showQuickMenu", False)
#            action NullAction() # make hoverable

#            xalign 0.5

#            hbox:
#                xsize 500
#                style_prefix "quick"

#                xalign 0.5
#                yalign 0.0

#                if showQuickMenu:
#                    textbutton _("History"):
#                        action [SetScreenVariable("showQuickMenu", False), ShowMenu('history')]
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Skip"):
#                        action [SetScreenVariable("showQuickMenu", False), Skip()]
#                        alternate [SetScreenVariable("showQuickMenu", False), Skip(fast=True, confirm=True)]
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Auto"):
#                        action Preference("auto-forward", "toggle")
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Save"):
#                        action [SetScreenVariable("showQuickMenu", False), ShowMenu('save')]
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Q.Save"):
#                        action [SetScreenVariable("showQuickMenu", False), QuickSave()]
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Q.Load"):
#                        action [SetScreenVariable("showQuickMenu", False), QuickLoad()]
#                        hovered SetScreenVariable("showQuickMenu", True)
#                    textbutton _("Prefs"):
#                        action [SetScreenVariable("showQuickMenu", False), ShowMenu('Options')]
#                        hovered SetScreenVariable("showQuickMenu", True)




## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    quickMenuOn = 1
    if renpy.variant("small"):
        config.overlay_screens.append("quick_menu")
    else:
        config.overlay_screens.append("quick_menuDetector")
        config.overlay_screens.append("quick_menu")

    isDeletingSave = False


default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigationMain():

    vbox:
        style_prefix "navigation"

        xalign 0.5
        yalign 0.64

        spacing gui.navigation_spacing

        if main_menu:
            textbutton _("Start New Game") action Start()

        elif not ptceConfig["hardcoreMode"]:
            textbutton _("Save") action [SetVariable ("_game_menu_screen", "save"), ShowMenu("save")]

        textbutton _("Load Game") action ShowMenu("load")

        textbutton _("Options") action ShowMenu("Options")

        if not main_menu:
            textbutton _("History") action ShowMenu("history")

        if main_menu:
            textbutton _("Credits") action ShowMenu("about")

        textbutton _("Links") action ShowMenu("links")

        if renpy.variant("pc"):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Controls") action ShowMenu("help")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")



screen navigation():
    fixed:
        style_prefix "navigation"

        xpos gui.navigation_xpos-35
        ypos 320 # moved down from 0.5 to fit backdrop animation
        xsize 280
        ysize 456

        vbox:
            xpos 25
            spacing gui.navigation_spacing


            if not main_menu:
                # Character screen replaces Stats, Skills, Inventory, Equipment
                textbutton _("Character") action [
                    tt.Action(""),
                    SetVariable("useItem", 0),
                    SetVariable ("inventoryTarget", 0),
                    ShowMenu("ON_CharacterDisplayScreen"),
                    Function(cmenu_resetMenu),
                    SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
                    ] text_xalign 0

                if not ptceConfig["hardcoreMode"]:
                    textbutton _("Save") action ShowMenu("save") text_xalign 0

            if not ptceConfig["hardcoreMode"]:
                textbutton _("Load") action ShowMenu("load") text_xalign 0

            textbutton _("Options") action ShowMenu("Options") text_xalign 0

            if not main_menu:
                textbutton _("History") action ShowMenu("history") text_xalign 0

            if _in_replay:

                textbutton _("End Replay") action EndReplay(confirm=True) text_xalign 0

            elif not main_menu:
                textbutton _("Main Menu") action MainMenu() text_xalign 0


            textbutton _("Credits") action ShowMenu("about") text_xalign 0

            textbutton _("Links") action ShowMenu("links") text_xalign 0

            if renpy.variant("pc"):
                ## Help isn't necessary or relevant to mobile devices.
                textbutton _("Controls") action ShowMenu("help") text_xalign 0


            if renpy.variant("pc"):
                ## The quit button is banned on iOS and unnecessary on Android.
                textbutton _("Quit") action Quit(confirm=not main_menu) text_xalign 0


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    ## This empty frame darkens the main menu.
    frame:
        pass

    if gui.show_name:

        use menu_background(mainMenu=True) # backdrop animation from on_menububblescreen.rpy

        text "Monster Girl Dreams":
            style "main_menu_title"
            xalign 0.5
            ypos 40

        text "[randomMenuLine]" xalign 0.5 ypos 100

        #vbox:
            #text "[config.name!t]":

            #text "[config.version]":
            #    style "main_menu_version"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigationMain


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 280
    yfill True

style main_menu_vbox:
    xalign 0.5
    #xoffset -20
    xmaximum 800
    yalign 0.05
    #yoffset -20

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None):

    style_prefix "game_menu"
    use menu_background # backdrop animation replaces game_menu.png and/or main_menu.png

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"
        text_xalign 0
        action Return()

    label title xoffset 350 yoffset -10

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 80

style game_menu_navigation_frame:
    xsize 400
    yfill True

style game_menu_content_frame:
    left_margin 20
    right_margin 20
    top_margin 1

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos-10
    yalign 0.98
    yoffset -10


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("Credits"), scroll="viewport"):

        style_prefix "about"

        vbox:
            label "[config.name!t] - Credits"
            text _("Version [config.version!t]\n")
            text ""
            if renpy.variant("mobile"):
                vbox:
                    text "Tap twice to open a link!"
            elif renpy.variant("pc"):
                vbox:
                    text "Use {i}ctrl{/i} + {i}click{/i} to open links!"
            text ""
            text "Threshold - {a=https://monstergirldreams.blogspot.ca}Dev Blog{/a} - {a=https://www.patreon.com/MonsterGirlDreams}Patreon{/a}"
            text "  Makes this game and multiple different things in it."
            text ""
            text ""
            text "{i}Artist Credits{/i}"
            text ""
            text "Jiffic - {a=https://www.pixiv.net/member.php?id=5691625}Pixiv{/a}"
            text "  Made art for: Perpetua, Nicci, Sofia, Jora, Elly, Elena, Shizu, Camilla, Himika, Mizuko, Minoni, Feng, Venefica, Gren, Nova, Iabel, the Town background, Sofia's Background, the kiss mark graphic, the world map, and the patreon banner."
            text ""
            text "Applehead - {a=https://twitter.com/mistimagi}Twitter{/a} - {a=https://kalayara.deviantart.com/gallery/}Deviant Art{/a}"
            text "  Made art for: Kyra, Mika, Matango, Toxic Matango, Alraune, Rosaura, Amber, Ancilla, Trisha, Belle, The Elf, The Lizard Girl, The Salarisi, The Manticore, The Minotaur, Galvi, The Kunoichi Trainee, and The Tengu. The forest background, and mountain background. (As well as the original Black Knight.)"
            text ""
            text "Plasmid - {a=https://twitter.com/Plasmidhentai/}Twitter{/a} - {a=https://www.patreon.com/plasmid#_=_}Patreon{/a}"
            text "  Made art for: Amy, The Original Mimic, and Mara."
            text ""
            text "Houpo - {a=https://houpoartist.wixsite.com/official}Houpo's Website{/a} - {a=https://www.deviantart.com/houpo}Deviant Art{/a}"
            text "  Made art for: Lillian, the Church Background, the Harpy, the Harpy Tengu, and the Ghost. (Also the original Imp)."
            text ""
            text "NickBeja - {a=https://www.deviantart.com/nickbeja}Deviant Art{/a} - {a=https://www.patreon.com/nickbeja}Patreon{/a}"
            text "  Made art for: The Blue Slime, and Nara. (As well as Original Vili),"
            text ""
            text "ADOPOLICH - {a=https://twitter.com/ADOPOLICH}Twitter{/a} - {a=https://www.pixiv.net/member.php?id=27601141}Pixiv{/a}"
            text "  Made art for: Aiko, Bed-Chan, Kotone, Lumiren, The Black Knight, The loot bag, Stella, Ushris and the Caverns background."
            text ""
            text "Kenshin187 - {a=https://twitter.com/kenshinx187}Twitter{/a} - {a=https://twitter.com/lonerurouni187}TwitterSFW{/a} - {a=https://artalley.porn/@kenshin187}Mastodon{/a}"
            text "  Made art for: Vivian and Selena."
            text ""
            text "Otani - {a=https://twitter.com/tani_00tani}Twitter{/a} - {a=https://tanitani00tani34.wixsite.com/gottanitei/blank}Website{/a} - {a=https://www.pixiv.net/en/users/20325366}Pixiv{/a}"
            text "  Made art for: The generic imp, Vili, Catherine, Jennifer, Heather, the mimic, and golden treasure chest."
            text ""
            text "Crescentia - {a=https://twitter.com/Crescentia4tuna}Twitter{/a} - {a=https://crescentia-fortuna.newgrounds.com/}Newgrounds{/a}"
            text "  Made art for: Beris."
            text ""
            text "Elakan  - {a=https://twitter.com/ElakanDraws}Twitter{/a}"
            text "  Made art for: Ceris."




            text ""
            text "ShivanHunter - Generously created the current UI."
            text ""
            text ""
            text "{i}Writing Credits{/i}"
            text ""
            text "Valentin Cognito"
            text "  The current official editor. Wrote the Minoni Hoof Stepping Scene, Gren, Jora stream bathing, a number of scenes for Selena, some of the Ancilla random facts, the Venefica Dream Scene, the breast worship scene for Ushris, and the food eating descriptions in the bar."
            text ""
            text "SubjectAlpha - Discord:(SubjectAlpha#7975) - Does writing commissions."
            text "  Wrote the Solo Imp loss scene, Solo Imp Brothel Scene, Solo Elf Brothel Scene, Elf Sex Dream Scene, the Nara neutral loss scene, and Galvi's intro, sex scene, and titfuck scene."
            text ""
            text "GameSalamander - Discord:(GameSalamander#0820) - {a=https://twitter.com/GameSalamander?s=09}Twitter{/a} - Does writing commissions."
            text "  Wrote the Kunoichi Feet Dream, the sex loss scene for Kyra, and the three roleplay scenes for Beris."
            text ""
            text "Oluap"
            text "  Wrote the Kunoichi Bottom brothel scene and Mara Glory Hole scene."
            text ""
            text "WilliamTheShatner - The now retired, unofficial, official editor. Also wrote some of the Ancilla random facts."
            text ""
            text ""
            text "{i}Music and SFX from the following.{/i} File names identify creator."
            text ""
            text "{a=https://www.bandlab.com/blackh20}Stalkwick{/a}: Discord (Stalwick#1518)"
            text "  Notably for providing: The Forest Dungeon Ambience (Forest Dungeon Lurking), 'Dreaming', 'Rough Travels', and 'Won't You be my experiment'."
            text ""
            text "{a=http://freemusicarchive.org/music/Ask%20Again/}Art Of Escapism/Ask Again/Mid Air Machine{/a}"
            text ""
            text "{a=https://www.purple-planet.com/}Purple Planet{/a}"
            text ""
            text "{a=http://wingless-seraph.net/}Wingless Seraph{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile193.html}MFP【Marron Fields Production】{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile220.html}Chocolate mint{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile162.html}Manbo Second Class{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile295.html}shimtone{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile217.html}Tanaka Tamago{/a}"
            text ""
            text "{a=https://maou.audio/}Maoudamashii{/a}"
            text ""
            text "{a=https://soundcloud.com/q7oumurij7fr/sets/rengoku-teien}Rengoku-Teien{/a}"
            text ""
            text "{a=https://pocket-se.info/}Pocket Sound{/a}"
            text ""
            text "{a=http://d-symphony.com/index.html}Dragon's symphony{/a}"
            text ""
            text "{a=https://www.dlsite.com/eng/circle/profile/=/maker_id/RG32138.html}ayato sound create{/a}"
            text ""
            text "{a=https://www.dlsite.com/ecchi-eng/circle/profile/=/maker_id/RG07477.html}pierrotlunaire{/a}"
            text ""
            text "{a=https://www.dlsite.com/ecchi-eng/circle/profile/=/maker_id/RG05893.html}A water flea{/a}"
            text ""
            text "{a=https://www.dlsite.com/ecchi-eng/circle/profile/=/maker_id/RG21728.html}Orange Lovers{/a}"
            text ""
            text "{a=https://www.dlsite.com/eng/circle/profile/=/maker_id/RG17630.html}pigmyon studio{/a}"
            text ""
            text "{a=https://www.dlsite.com/ecchi-eng/circle/profile/=/maker_id/RG14009.html.html}Onteishu{/a}"
            text ""
            text "{a=https://otologic.jp/}Otologic{/a}"
            text ""
            text "{a=https://taira-komori.jpn.org/freesound.html/}taira-komori{/a}"
            text ""
            text "{a=http://osabisi.sakura.ne.jp/m2/index}Osabisi{/a}"
            text ""
            text "{a=http://www.kurage-kosho.info/guide.html}kurage-kosho{/a}"
            text ""
            text ""
            text "StrangeMan52 - Created the ModLoader."
            text ""
            text ""
            text "Special thanks to: My patrons, Ren'Py, people who send me feedback and point out typos, and of course, you for playing this game."
            text ""
            text ""
            text "About Ren'Py"
            text ""
            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

label RenameSaveFile:
    $ renpy.retain_after_load()

    hide screen save
    hide screen load
    $ save_name = renpy.input(_("What do you want to rename your save file to? The save file name will be updated the next time you save."),  length=99) or _("")
    return

    $ _game_menu_screen="Save"
    call _game_menu from _call__game_menu_6
    return



screen save():
    $ _game_menu_screen = "Save"

    tag menu

    use file_slots(_("Save"))


screen load():
    $ _game_menu_screen = "Load"

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    if renpy.mobile:
                        button:
                            action [If(isDeletingSave, false=[FileAction(slot)], true=[FileDelete(slot)])]

                            has vbox

                            add FileScreenshot(slot) xalign 0.5

                            text FileSaveName(slot):
                                style "slot_name_text"

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"

                    else:
                        button:
                            action FileAction(slot)

                            has vbox

                            add FileScreenshot(slot) xalign 0.5

                            text FileSaveName(slot):
                                style "slot_name_text"

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"



                            key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.4
                yalign 1.0

                spacing gui.page_spacing

                if renpy.mobile and not isDeletingSave:
                    textbutton _("Delete") action [If(isDeletingSave, true=[SetVariable("isDeletingSave", False)], false=[SetVariable("isDeletingSave", True)])]
                if isDeletingSave:
                    textbutton _("{color=#E470B2}Delete{/color}") action [If(isDeletingSave, true=[SetVariable("isDeletingSave", False)], false=[SetVariable("isDeletingSave", True)])]

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                if renpy.mobile:
                    for page in range(1, 16):
                        textbutton "[page]" action FilePage(page)
                else:
                    for page in range(1, 21):
                        textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
                if not main_menu:
                    textbutton _("Rename Save") action Jump("RenameSaveFile")
    on "replaced" action SetVariable("isDeletingSave", False)
    on "hide" action SetVariable("isDeletingSave", False)




style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Options screen ##########################################################
##
## The Options screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#Options
label reloadDatabase:
    $ renpy.retain_after_load()
    $ CurrentVersion = config.version
    $ loadingDatabaseType = 1
    hide screen CharacterDialogueScreen
    $ npcProgHolder = copy.deepcopy(ProgressNPC)
    $ eventProgHolder = copy.deepcopy(ProgressEvent)
    $ advenProgHolder = copy.deepcopy(ProgressAdventure)
    $ MenuLineSceneCheckMark = -1
    $ runAndStayInEvent = 0
    $ victoryScene = 0
    $ inChurch = 0

    $ player.Update()

    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    python:
        try:
            persistantMonSetData
        except:
            persistantMonSetData = []
    $ persistantMonSetData = persistantMonSetData

    call uncapStats from _call_uncapStats_1

    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []
    call loadDatabase from _call_loadDatabase_1
    $ npcProgHolder = []
    $ eventProgHolder = []
    $ advenProgHolder = []


    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)
        python:
            for tempFet in TempFetishes:
                for pastFet in holdFetish:
                    if tempFet.name == pastFet.name:
                        tempFet.Level = pastFet.Level


    if rehauled == 0: #this is solely for updating saves to v23, and can be deleted later.
        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)
        python:
            perkHolder = copy.deepcopy(player.perks)
            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, -1)
            i = 0
            for each in player.FetishList:

                player.FetishList[i].Level = player.FetishList[i].Level*10 - 5
                if player.FetishList[i].Level <= 0:
                    player.FetishList[i].Level = 0

                TempFetishes[i].Level = TempFetishes[i].Level*10
                if TempFetishes[i].Level <= 0:
                    TempFetishes[i].Level = 0
                i+=1

            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, 1)

    if progressionBoost == 0: #this is solely for updating saves to v23.9, and can be deleted later.
        $ progressionBoost = 1
        $ player.statPoints += copy.deepcopy(player.stats.lvl) - 1
        $ display = "Gained " + str(player.stats.lvl - 1) + " stat points!"
        "[display]"

        if player.stats.lvl >= 5:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl >= 10:
            $ player.perkPoints += 2
            $ perkIncreases += 2

        if player.stats.lvl >= 20:
            $ player.perkPoints += 2
            $ perkIncreases += 2
        $ display = "Gained " + str(perkIncreases) + " perk points!"
        "[display]"

        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)



    $ progressionBoost = 1
    $ rehauled = 1
    $ player.CalculateStatBoost()
    "Save updated!"



    #$ _game_menu_screen="Options"
    #call _game_menu from _call__game_menu_1
    jump exitCombatFunction

label AutoReloadDatabase:
    $ CurrentVersion = config.version
    $ loadingDatabaseType = 1
    $ MenuLineSceneCheckMark = -1
    $ runAndStayInEvent = 0
    $ victoryScene = 0
    $ inChurch = 0


    $ npcProgHolder = copy.deepcopy(ProgressNPC)
    $ eventProgHolder = copy.deepcopy(ProgressEvent)
    $ advenProgHolder = copy.deepcopy(ProgressAdventure)
    hide screen CharacterDialogueScreen

    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    python:
        try:
            persistantMonSetData
        except:
            persistantMonSetData = []
    $ persistantMonSetData = persistantMonSetData

    $ player.Update()

    call uncapStats from _call_uncapStats_2

    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []
    call loadDatabase from _call_loadDatabase_3
    $ npcProgHolder = []
    $ eventProgHolder = []
    $ advenProgHolder = []


    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)
        python:
            for tempFet in TempFetishes:
                for pastFet in holdFetish:
                    if tempFet.name == pastFet.name:
                        tempFet.Level = pastFet.Level

    if rehauled == 0: #this is solely for updating saves to v23, and can be deleted later.
        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)
        python:
            perkHolder = copy.deepcopy(player.perks)
            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, -1)
            i = 0
            for each in player.FetishList:
                player.FetishList[i].Level = player.FetishList[i].Level*10 - 5
                if player.FetishList[i].Level <= 0:
                    player.FetishList[i].Level = 0

                TempFetishes[i].Level = TempFetishes[i].Level*10
                if TempFetishes[i].Level <= 0:
                    TempFetishes[i].Level = 0
                i+=1

            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, 1)

    if progressionBoost == 0: #this is solely for updating saves to v23.9, and can be deleted later.
        $ progressionBoost = 1
        $ player.statPoints += copy.deepcopy(player.stats.lvl) - 1
        $ display = "Gained " + str(player.stats.lvl - 1) + " stat points!"
        "[display]"

        if player.stats.lvl >= 5:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl >= 10:
            $ player.perkPoints += 2
            $ perkIncreases += 2

        if player.stats.lvl >= 20:
            $ player.perkPoints += 2
            $ perkIncreases += 2
        $ display = "Gained " + str(perkIncreases) + " perk points!"
        "[display]"

        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)



    $ player.CalculateStatBoost()
    $ rehauled = 1
    $ progressionBoost = 1

    #$ _game_menu_screen="Options"
    #call _game_menu from _call__game_menu_1
    jump exitCombatFunction

label checkData:
    $ needToUpdate = 0
    python:
        #try:
        #    CurrentVersion
        #except NameError:
        #    needToUpdate = 1
        #    CurrentVersion = config.version
        #else:
        #    if CurrentVersion != config.version:
        #        needToUpdate = 1
        #        CurrentVersion = config.version
        UpdatedGameCheck = len(SkillsDatabase) + len(ItemDatabase) + len(MonsterDatabase) + len(PerkDatabase) + len(LocationDatabase) + len(EventDatabase) + len(AdventureDatabase)

        try:
            CurrentIteration
        except NameError:
            needToUpdate = 1
            CurrentIteration = copy.deepcopy(UpdatedGameCheck)

    if CurrentIteration != UpdatedGameCheck:
        $ needToUpdate = 1
        $ CurrentIteration = copy.deepcopy(UpdatedGameCheck)


    if needToUpdate == 1 or CurrentVersion != config.version:
        $ CurrentVersion = config.version
        call AutoReloadDatabase from _call_AutoReloadDatabase


    jump exitCombatFunction

label imageVisibilityYes:
    $ persistent.showCharacterImages = True

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu
    jump exitCombatFunction

label imageVisibilityNo:
    $ persistent.showCharacterImages = False

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu_2
    jump exitCombatFunction

label cardBubblesYes:
    $ persistent.showCardBubbles = True

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu_1
    jump exitCombatFunction

label cardBubblesNo:
    $ persistent.showCardBubbles = False

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu_3
    jump exitCombatFunction

label showVFXYes:
    $ persistent.showVFX = True

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu_4
    jump exitCombatFunction

label showVFXNo:
    $ persistent.showVFX = False

    $ _game_menu_screen="Options"
    call _game_menu from _call__game_menu_5
    jump exitCombatFunction

screen Options():
    $ _game_menu_screen = "Options"

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 6

    use game_menu(_("Options"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        label _("Display")
                        text"" size 10
                        textbutton "1280 x 720" action Preference("display", 0.666666666667)
                        text"" size 10
                        textbutton "1600 x 900" action Preference("display", 0.83333333333)
                        text"" size 10
                        textbutton _("1920 x 1080") action Preference("display", "window")
                        text"" size 10
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                text""
                vbox:
                    #style_prefix "check"
                    label _("Skip")
                    text"" size 10
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    text"" size 10
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    text"" size 10
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))
                text ""
                vbox:
                    style_prefix "check"
                    label _("Character Images")
                    # Button colors here were reversed from the intuitive color scheme (white when selected)
                    if persistent.showCharacterImages == False:
                        textbutton _("On") action Jump("imageVisibilityYes")
                    else:
                        textbutton _("{color=#E470B2}On{/color}") action Jump("imageVisibilityYes")
                    if persistent.showCharacterImages == False:
                        textbutton _("{color=#E470B2}Off{/color}") action Jump("imageVisibilityNo")
                    else:
                        textbutton _("Off") action Jump("imageVisibilityNo")
                text ""
                vbox:
                    style_prefix "check"
                    label _("Card Bubbles")
                    # Button colors here were reversed from the intuitive color scheme (white when selected)
                    if persistent.showCardBubbles == False:
                        textbutton _("On") action Jump("cardBubblesYes")
                    else:
                        textbutton _("{color=#E470B2}On{/color}") action Jump("cardBubblesYes")
                    if persistent.showCardBubbles == False:
                        textbutton _("{color=#E470B2}Off{/color}") action Jump("cardBubblesNo")
                    else:
                        textbutton _("Off") action Jump("cardBubblesNo")
                text ""
                vbox:
                    style_prefix "check"
                    label _("Show VFX")
                    # Button colors here were reversed from the intuitive color scheme (white when selected)
                    if persistent.showVFX == False:
                        textbutton _("On") action Jump("showVFXYes")
                    else:
                        textbutton _("{color=#E470B2}On{/color}") action Jump("showVFXYes")
                    if persistent.showVFX == False:
                        textbutton _("{color=#E470B2}Off{/color}") action Jump("showVFXNo")
                    else:
                        textbutton _("Off") action Jump("showVFXNo")






                if not main_menu:
                    vbox:
                        text ""
                        style_prefix "check"
                    vbox:
                        text ""
                        text ""
                        #label _("Update Save")
                        textbutton _("Update Save") action [Jump("reloadDatabase"),  SensitiveIf(InventoryAvailable)]

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined Options.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:


                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

                if not main_menu:
                    vbox:
                        textbutton _("Player Appearance") action [Jump("AppearanceCreator"),  SensitiveIf(InventoryAvailable)]


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what + "\n"

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


screen links():
    $ _game_menu_screen = "Links"

    tag menu

    use game_menu(_("Links"), scroll="viewport"):

        if renpy.variant("mobile"):
            vbox:
                text "Tap twice to open a link!"
                text ""
        elif renpy.variant("pc"):
            vbox:
                text "Use {i}ctrl{/i} + {i}click{/i} to open links!"
                text ""
        hbox:
            xalign 0.5
            label "{a=https://monstergirldreams.miraheze.org/wiki/Monster_Girl_Dreams_Wiki}Game Wiki{/a}"
        hbox:
            xalign 0.5
            text "Contains walkthroughs and general game information.{b} Caution of spoilers{/b}."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://discord.com/invite/Md5n5KJ}Discord{/a}"
        hbox:
            text "Features a range of channels from game help, bug and typo reporting, and just socializing with other MGD fans."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://monstergirldreams.blogspot.com}Game Blog{/a}"
        hbox:
            xalign 0.5
            text "Contains the most detailed archive of game changelogs."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://twitter.com/ThresholdMGD}Threshold's Twitter{/a}"
        hbox:
            xalign 0.5
            text "Tweets related to the game and occasionally personal developer notes."

style links_label is gui_label
style links_label_text is gui_label_text
style links_text is gui_text

style links_label_text:
    size gui.label_text_size


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():
    $ _game_menu_screen = "Help"

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 15

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():



    hbox:
        label _("Shift")
        text _("Increment leveling up, and buying/selling options by 5.")

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Delete/Del")
        text _("Delete saves in the save menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "Shift+S or Alt+S"
        text _("Takes a screenshot.")

    hbox:
        label "Shift+A"
        text _("Opens the renpy accessibility menu.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 8

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 250
    right_padding 20

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 300

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:
        xminimum 1000
        xmaximum 1000
        yminimum 300
        ymaximum 300

        label _(message):
            style "confirm_prompt"
            xalign 0.5
            yalign 0.1

        fixed: ##Return button
            xalign 0.15
            yalign 1.0
            xsize 324
            ysize 81
            use ON_TextButton(text="Yes", action=yes_action)


        fixed: ##Return button
            xalign 0.85
            yalign 1.0
            xsize 324
            ysize 81
            use ON_TextButton(text="No", action=no_action)


    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 450

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "small"

    zorder 300

    hbox:
        style_prefix "quick"

        xalign 0.5
        yalign 0.0

        textbutton _("History") action ShowMenu('history')
        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Menu") action ShowMenu()
        textbutton _("Q.Save") action QuickSave() hovered [SetVariable ("quickMenuOn", 1)]
        textbutton _("Q.Load") action QuickLoad() hovered [SetVariable ("quickMenuOn", 1)]
    hbox:
        style_prefix "quick"

        xalign 0.025
        yalign 0.98
        text _(TimeOfDay) size 28
    hbox:
        style_prefix "quick"
        xalign 0.975
        yalign 0.98
        textbutton _("Hide-UI") action HideInterface()




style window:
    variant "small"
    background "gui/phone/textbox.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"

style game_menu_outer_frame:
    variant "small"

style game_menu_navigation_frame:
    variant "small"
    xsize 340

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 400

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 600
