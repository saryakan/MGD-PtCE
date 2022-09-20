init:
    $ hpFloor = 50
    $ epFloor = 20
    $ spFloor = 1

    $ powFloor = 1
    $ spdFloor = 1
    $ intFloor = 1
    $ allFloor = 1
    $ wilFloor = 1
    $ lukFloor = 1

    $ sexResFloor = 95
    $ assResFloor = 50
    $ nipResFloor = 50
    $ chuResFloor = 50
    $ seducResFloor = 50
    $ magResFloor = 50
    $ painResFloor = 50

    $ hpCap = 150
    $ epCap = 100
    $ spCap = 3

    $ powCap = 10
    $ spdCap = 10
    $ intCap = 10
    $ allCap = 10
    $ wilCap = 10
    $ lukCap = 10

    $ sexResCap = 150
    $ assResCap = 150
    $ nipResCap = 200
    $ chuResCap = 150
    $ seducResCap = 150
    $ magResCap = 150
    $ painResCap = 150

label NormalStats:
    $ hpCap = 150
    $ epCap = 100
    $ spCap = 3

    $ powCap = 10
    $ spdCap = 10
    $ intCap = 10
    $ allCap = 10
    $ wilCap = 10
    $ lukCap = 10
    return

label EasyStats:
    $ hpCap = 9999
    $ epCap = 9999
    $ spCap = 99

    $ powCap = 100
    $ spdCap = 100
    $ intCap = 100
    $ allCap = 100
    $ wilCap = 100
    $ lukCap = 100

    return

label uncapStats:
    $ hpCap = 10000
    $ epCap = 10000
    $ spCap = 99

    $ powCap = 100
    $ spdCap = 100
    $ intCap = 100
    $ allCap = 100
    $ wilCap = 100
    $ lukCap = 100

    $ sexResFloor =  75
    $ assResFloor =  30
    $ nipResFloor = 25
    $ chuResFloor = 50
    $ seducResFloor = 50
    $ magResFloor = 50
    $ painResFloor = 30


label setStatFloors:
    $ hpFloor = player.stats.max_hp
    $ epFloor = player.stats.max_ep
    $ spFloor = player.stats.max_sp

    $ powFloor = player.stats.Power
    $ spdFloor = player.stats.Tech
    $ intFloor = player.stats.Int
    $ allFloor = player.stats.Allure
    $ wilFloor = player.stats.Willpower
    $ lukFloor = player.stats.Luck


    $ sexResCap =  player.BodySensitivity.Sex
    $ assResCap =  player.BodySensitivity.Ass
    $ nipResCap = player.BodySensitivity.Breasts
    $ chuResCap = player.BodySensitivity.Mouth
    $ seducResCap = player.BodySensitivity.Seduction
    $ magResCap = player.BodySensitivity.Magic
    $ painResCap = player.BodySensitivity.Pain
