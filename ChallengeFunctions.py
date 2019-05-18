#!/usr/bin/env python3

import random
import GlobalVars as V

def randNpc():
    count1, count2, count3 = 0, 0, 0
    type1, type2, type3 = None, None, None
    line1 = ""
    availableTargets = V.targetCount

    #Randomize npc rule
    npcOptions = ["type","area","area"]
    option = random.choice(npcOptions)

    if option == "type":
        #Randomize targets by type
        type1 = random.choice(V.npc_types_list)
        V.npc_types_list.remove(type1)

        if type1 in ["civilian", "armed"]:
            count1 = random.randint(1,availableTargets)
            availableTargets -= count1

            if availableTargets > 0:
                type2 = random.choice(V.npc_types_list)
                V.npc_types_list.remove(type2)

                if type2 in ["civilian", "armed"]:
                    count2 = random.randint(1,availableTargets)
                    availableTargets -= count2

                    if availableTargets > 0 and V.npc_types_list:
                        type3 = V.npc_types_list[0]
                        V.npc_types_list.remove(type3)
                        count3 = random.randint(1,min(availableTargets, len(V.map.unique_npcs)))
                        availableTargets -= count3

                else:
                    count2 = random.randint(1, min(availableTargets, len(V.map.unique_npcs)))
                    availableTargets -= count2

                    if availableTargets > 0 and V.npc_types_list:
                        type3 = V.npc_types_list[0]
                        V.npc_types_list.remove(type3)
                        count3 = random.randint(1,availableTargets)
                        availableTargets -= count3

        else:
            count1 = random.randint(1, min(availableTargets, len(V.map.unique_npcs)))
            availableTargets -= count1

            if availableTargets > 0:
                type2 = random.choice(V.npc_types_list)
                V.npc_types_list.remove(type2)
                count2 = random.randint(1,availableTargets)
                availableTargets -= count2

                if availableTargets > 0 and V.npc_types_list:
                    type3 = V.npc_types_list[0]
                    V.npc_types_list.remove(type3)
                    count3 = random.randint(1,availableTargets)
                    availableTargets -= count3
        #Bandaid fix
        while availableTargets > 0:
            count1 += 1
            availableTargets -= 1
        #Print targets in a nice format
        if count1 == 1:
            temp = "target"
        else:
            temp = "targets"

        line1 += "{} {} {}".format(str(count1), type1, temp)

        if count2 > 0:
            if count2 == 1:
                temp = "target"
            else:
                temp = "targets"
            line1 += ", {} {} {}".format(str(count2), type2, temp)
            if count3 > 0:
                line1 += ", {} {} target".format(str(count3), type3)
        line1 += "."

    elif option == "area":
        areaOptions = ["sameroom","floor","trespassing"]
        if availableTargets < V.map.floors:
            areaOptions.remove("floor")
        option = random.choice(areaOptions)

        if option == "sameroom":
            line1 += "All targets must be in the same room."

        elif option == "floor":
            line1 += "All targets must be in different floors"

        elif option == "trespassing":
            line1 += "You must be trespassing when killing targets."

    print(line1)
    V.finalChallenge.append(V.FinalChallengeComponent("Target rule:", line1, ""))

def randWeapons():
    count1, count2, count3 = 0, 0, 0
    type1, type2, type3 = None, None, None
    availableTargets = V.targetCount
    line1, line2 = "", ""

    #Randomize weapon rule
    weaponOptions = ["many","single","mix","accidents","improv"]
    if availableTargets < 5:
        weaponOptions.remove("mix")
    option = random.choice(weaponOptions)

    #Randomize weapons and target count
    if option == "mix":
        type1 = random.choice(V.map.weapons)
        V.map.weapons.remove(type1)
        count1 = random.randint(2,3)
        availableTargets -= count1

        type2 = random.choice(V.map.weapons)
        V.map.weapons.remove(type2)
        count2 = random.randint(2,availableTargets)
        availableTargets -= count2
        line1 += "Kill {} targets with {} and {} targets with {}".format(str(count1), type1, str(count2), type2)

        if availableTargets > 0:
            type3 = random.choice(V.map.weapons)
            V.map.weapons.remove(type3)
            count3 = 1
            availableTargets -= count3
            line1.replace(" and ", ", ")
            line2 += " and {} target with {}".format(str(count3), type3)
        line1 += "."

    elif option == "many":
        count1 = availableTargets
        availableTargets -= count1
        type1 = random.sample(V.map.weapons, count1)
        s = ", "
        line1 += "Kill each target with a different weapon."
        line2 += "Weapon list: " + s.join(type1)

    elif option == "single":
        count1 = availableTargets
        availableTargets -= count1
        type1 = random.choice(V.map.weapons)
        line1 += "Kill each target with {}.".format(str(type1))

    elif option == "accidents":
        count1 = availableTargets
        line1 += "Kill each target with a different accident."

    elif option == "improv":
        count1 = availableTargets
        line1 += "Kill each target with a different improvised weapon"
        line2 += "from the room the hit takes place in."

    #Print targets in a nice format
    print(line1)
    V.finalChallenge.append(V.FinalChallengeComponent("Weapon rule:", line1, line2))

def randDisguise():
    count1, count2, count3 = 0, 0, 0
    disguise = None
    availableTargets = V.targetCount
    line1, line2 = "", ""

    #Randomize disguise rule
    disguiseOptions = ["neverchange","timer"]
    option = random.choice(disguiseOptions)

    if option == "timer":
        line1 += "You must change to a fresh disguise at least once between each kill."

    elif option == "neverchange":
        disguise = random.choice(V.map.unique_disguises)
        line1 += "Kill all targets while disguised as {}.".format(disguise)
        line2 += "You may not change to any other disguises."

    elif option == "changeonkill":
        line1 += "You must always take your victim's outfit."
        line2 += "Exceptions can be made in case of unique targets."

    print(line1)
    V.finalChallenge.append(V.FinalChallengeComponent("Disguise rule:", line1, line2))

def randExtra():
    line1, line2 = "", ""
    extraOptions = ["5s","noguns","killshot"]
    option = random.choice(extraOptions)

    if option == "5s":
        line1 += "You must fire a loud weapon within 5 seconds of starting the mission."

    elif option == "noguns":
        line1 += "You must not use any firearms or explosives."

    elif option == "killshot":
        line1 += "You must fire a loud weapon at least once between each kill."

    print(line1)
    V.finalChallenge.append(V.FinalChallengeComponent("Extra rule:", line1, line2))
