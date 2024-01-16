import random
import math
from operator import *
from datetime import datetime

def d6Roll():
    """Rolls 1 die."""
    roll = random.randint(1, 6)
    return roll

def d6Rollx2():
    """Rolls 2 dice."""
    roll = d6Roll() + d6Roll()
    return roll

def verifyYorN(prompt):
    """Input prompt for a Yes or No response. Returns 'Y' or 'N' string, otherwise loops endlessly"""
    notVerified = True
    while notVerified:
        print(prompt)
        inp = getInputNum("1) Yes\n2) No ", 1, 2, prompt)
        match inp:
            case 1:
                return "Y"
            case 2:
                return "N"

def verifyNextAction(aborting):
    """For each step of a patrol, ask for what to do next. Returns string: 'Continue', 'Supply', 'Status', 'Abort'"""
    if aborting:
        inp = getInputNum("1) Continue\n2) Stores Report\n3) Damage Report ", 1, 3)
    else:
        inp = getInputNum("1) Continue\n2) Stores Report\n3) Damage Report\n4) Abort Patrol ", 1, 4)
    match inp:
        case 1:
            return "Continue"
        case 2:
            return "Stores"
        case 3:
            return "Damage"
        case 4:
            return "Abort"

def printTargetShipList(ship):
    print("Targets:")
    for s in range(len(ship)):
        strng = str(s + 1) + ") " + str(ship[s])
        print(strng)

def printRollandMods(rollFor, roll, mods):
    """Prints a roll for some check, plus the modifiers, then the modified roll total.
    Roll for x (7-): MF || Roll: 4 • Mods: +1"""
    total = roll + mods
    if mods <= 0:
        toPrint = rollFor + " " + str(total) + " || Roll: " + str(roll) + " • Mods: " + str(mods)
    if mods > 0:
        toPrint = rollFor + " " + str(total) + " || Roll: " + str(roll) + " • Mods: +" + str(mods)
    print(toPrint)

def getInputNum(prompt, minINCLUSIVE = -1, maxINCLUSIVE = 100, secondPrompt = ""):
    invalidInput = True
    while invalidInput:
        print(prompt, end="")
        inp = input()
        if inp == "?":
            if secondPrompt != "":
                helpText(secondPrompt)
            else:
                helpText(prompt)
            continue
        try:
            inp = int(inp)
        except:
            print("Invalid input. Enter a number.")
            continue
        if inp < minINCLUSIVE:
            print("Must be greater than or equal to", minINCLUSIVE)
        elif inp > maxINCLUSIVE:
            print("Must be less than or equal to", maxINCLUSIVE)
        else:
            return inp

def getInputNumNoSecondPrompt(prompt, minINCLUSIVE = -1, maxINCLUSIVE = 100):
    invalidInput = True
    while invalidInput:
        print(prompt, end="")
        inp = input()
        if inp == "?":
            helpText(prompt)
            continue
        try:
            inp = int(inp)
        except:
            print("Invalid input. Enter a number.")
            continue
        if inp < minINCLUSIVE:
            print("Must be greater than or equal to", minINCLUSIVE)
        elif inp > maxINCLUSIVE:
            print("Must be less than or equal to", maxINCLUSIVE)
        else:
            return inp

def Escorted(ships):
    """Returns true if the list of ships passed has an escort (as its first ship)"""
    if ships[0].type == "Escort":
        return True
    else:
        return False

def scuttleFromFlooding(game, attacker, airAttack):
    print("Emergency blow ballast! Attempting to abandon ship and scuttle the boat.")
    scuttleRoll = d6Rollx2()
    scuttleDRM = 0
    if game.sub.crew_health["Kommandant"] == 2:
        scuttleDRM += 1
    printRollandMods("Scuttle roll (11-):", scuttleRoll, scuttleDRM)

    #check to see if unspent luck and didn't successfully scuttle
    while game.halsUndBeinbruch > 0 and scuttleRoll + scuttleDRM > 11:
        print("Your luck that did not save your boat helps you instead re-attempt scuttling!")
        game.halsUndBeinbruch -= 1
        scuttleRoll = d6Rollx2()
        printRollandMods("Scuttle reroll (11-):", scuttleRoll, scuttleDRM)

    if scuttleRoll + scuttleDRM <= 11:
        if airAttack:
            print("Successfully scuttled. The U-boat slips under the waves.")
            causeText = "Scuttled " + game.getFullDate() + " due to flooding after an attack by a" + attacker
            gameover(game, causeText)
        else:
            print("Successfully scuttled. The U-boat slips under the waves as your crew is captured.")
            causeText = "Scuttled " + game.getFullDate() + " due to flooding after depth charges from the " + attacker
            gameover(game, causeText)
    else:
        print("The boat fails to go down and is successfully captured by the enemy. It's a massive failure as your crew are captured.")
        if airAttack:
            causeText = "Captured " + game.getFullDate() + " after an attack by a " + attacker
            gameover(game, causeText)
        else:
            causeText = "Captured " + game.getFullDate() + " after depth charge attack from the " + attacker
            gameover(game, causeText)



def scuttleFromDieselsInop(game):
    print("Emergency blow ballast! Attempting to abandon ship and scuttle the boat.")
    radioRoll = d6Rollx2()
    radioDRM = 0
    if game.sub.systems["Radio"] >= 2:
        radioDRM += 4
    printRollandMods("Roll to see if rescued at sea (11-):", radioRoll, radioDRM)

    #check to see if luck and needs aving
    while game.halsUndBeinbruch > 0 and radioRoll + radioDRM >= 11:
        print("Your luck that did not save your boat helps you instead re-attempt scuttling!")
        game.halsUndBeinbruch -= 1
        radioRoll = d6Rollx2()
        printRollandMods("Reroll to see if rescued at sea (11-):", radioRoll, radioDRM)

    if radioRoll + radioDRM >= 11:
        causeText = "Lost at sea", game.getFullDate(), "after scuttling the boat due to inoperative diesel engines"
        gameover(game, causeText)
    else:
        game.pastSubs.append(self.id)
        game.id = random.randint(20, 999)
        toprinttext = "You've been rescued at sea. On return, BDU has reassigned you to U-" + str(self.id)
        print(toprinttext)


def gameover(game, cause):
    print("++++++++++++++++++++++++++++")
    print("++        GAMEOVER!       ++")
    print("++++++++++++++++++++++++++++")
    print("Carrer summary of ", end = "")
    print(game.rank[game.sub.crew_levels["Kommandant"]], game.kmdt, end = "")
    toprint = ", Commander of U-" + str(game.id)
    print(toprint)
    if len(game.pastSubs) > 0:
        toprint = "Other commands: "
        for x in range(len(game.pastSubs)):
            if x == len(game.pastSubs) - 1:
                toprint = toprint + "U-" + str(game.pastSubs[x])
            else:
                toprint = toprint + "U-" + str(game.pastSubs[x]) + ", "
        print(toprint)

    #determine where in the patrol and what the orders were when game was ended
    adjustedOrders = game.currentOrders
    adjustedOrders = adjustedOrders.strip('(Minelaying)')
    adjustedOrders = adjustedOrders.strip('(Wolfpack)')
    adjustedOrders = adjustedOrders.strip('(Abwehr Agent Delivery)')
    if cause == "Survived - promoted to desk job in Training Command":
        toprint = "Promoted to a desk job in Training Command"
    elif "KIA" in cause:
        toprint = cause
    else:
        whilePatrolling = "x"
        match game.patrolArray[game.currentBox]:
            case "British Isles":
                whilePatrolling = " while patrolling the British Isles "
            case "West African Coast" | "Spanish Coast":
                whilePatrolling = " while patrolling off the " + game.patrolArray[game.currentBox]
            case "Norway":
                whilePatrolling = " while patrolling off " + game.patrolArray[game.currentBox]
            case "Atlantic":
                whilePatrolling = " while patrolling the mid-" + game.patrolArray[game.currentBox]
            case "Mediterranean" | "Arctic" | "Caribbean":
                whilePatrolling = " while patrolling the " + game.patrolArray[game.currentBox]
            case "North America":
                whilePatrolling = " while patrolling the " + game.patrolArray[game.currentBox] + "n station"
            case "Transit":
                #determine if on the way to or from patrol
                if game.currentBox <= 4:   #if on the way to patrol
                    match adjustedOrders:
                        case "British Isles" | "Atlantic" | "Mediterranean" | "Arctic" | "Caribbean" | "West African Coast" | "Spanish Coast":
                            whilePatrolling = " while on the way to patrol the " + adjustedOrders
                        case "Norway":
                            whilePatrolling = " while on the way to patrol off " + adjustedOrders
                        case "North America":
                            whilePatrolling = " while on the way to patrol the " + adjustedOrders + "n station"
                else:
                    match adjustedOrders:
                        case "British Isles" | "Atlantic" | "Mediterranean" | "Arctic" | "Caribbean" | "West African Coast" | "Spanish Coast":
                            whilePatrolling = " while returning from a patrol of the " + adjustedOrders
                        case "Norway":
                            whilePatrolling = " while returning from a patrol off " + adjustedOrders
                        case "North America":
                            whilePatrolling = " while returning from a patrol on the " + adjustedOrders + "n station"
            case "Bay of Biscay":
                # determine if on the way to or from patrol
                if game.currentBox <= 4:  # if on the way to patrol
                    match adjustedOrders:
                        case "British Isles" | "Atlantic" | "Mediterranean" | "Arctic" | "Caribbean" | "West African Coast" | "Spanish Coast":
                            whilePatrolling = " crossing the Bay of Biscay to patrol the " + adjustedOrders
                        case "Norway":
                            whilePatrolling = " crossing the Bay of Biscay to patrol off " + adjustedOrders
                        case "North America":
                            whilePatrolling = " crossing the Bay of Biscay to patrol the " + adjustedOrders + "n station"
                else:
                    match adjustedOrders:
                        case "British Isles" | "Atlantic" | "Mediterranean" | "Arctic" | "Caribbean" | "West African Coast" | "Spanish Coast":
                            whilePatrolling = " while crossing the Bay of Biscay returning from a patrol of the " + adjustedOrders
                        case "Norway":
                            whilePatrolling = " while crossing the Bay of Biscay returning from a patrol off " + adjustedOrders
                        case "North America":
                            whilePatrolling = " while crossing the Bay of Biscay returning from a patrol on the " + adjustedOrders + "n station"
            case "Mission":
                match game.currentOrders:
                    case "British Isles(Minelaying)":
                        whilePatrolling = " while conducting a minelaying mission off the " + adjustedOrders
                    case "British Isles(Abwehr Agent Delivery)":
                        whilePatrolling = " while attempting to land an agent off the " + adjustedOrders
                    case "North America(Abwehr Agent Delivery)":
                        whilePatrolling = " while attempting to land an agent off the " + adjustedOrders + "n coast"

        toprint = "Fate of U-" + str(game.id) + ": " + cause + whilePatrolling

    print(toprint)

    if game.sub.knightsCross > 0:
        print("Awards:", game.awardName[game.sub.knightsCross])
        award = game.awardName[game.sub.knightsCross]
    else:
        award = "-"
    print("Patrols completed:", str(game.patrolNum - 1))
    #print("End date:", game.getFullDate)
    print("Ships sunk:", str(len(game.shipsSunk)))
    grtSunk = 0
    warshipsSunk = 0
    for x in range (len(game.shipsSunk)):
        grtSunk += game.shipsSunk[x].GRT
        if game.shipsSunk[x].hp == 5:
            warshipsSunk += 1
    print("Warships sunk:", str(warshipsSunk))
    grtSunkSTR = f"{grtSunk:,}"
    print("GRT sunk:", str(grtSunkSTR))
    print("Damage done:", str(game.damageDone))
    print("Hits taken:", str(game.hitsTaken))
    print("Random Events:", str(game.randomEvents))

    now = str(datetime.now())
    now = now.split(".")
    now = now[0]
    fate = cause + whilePatrolling
    insertNewScore(game.kmdt, game.getFullUboatID(), game.sub.getType(), str(game.patrolNum - 1), str(grtSunkSTR), str(game.damageDone), str(len(game.shipsSunk)), str(warshipsSunk), str(game.hitsTaken), str(game.randomEvents), fate, game.getOfficerRank(), award, now)

    print("Result: ", end="")
    if "Captured" in cause:
        print("DEFEAT!")
        print("You are a disgrace to the Kriegsmarine, your family, and yourself. Consider a career after the war on land.\nYour U-Boat was captured and you have delivered a working Enigma code machine and other secrets into\nAllied hands, possibly sabotaging the entire U-Boat campaign.")
    elif grtSunk < 50000:
        print("DEFEAT")
        if "Survived" in cause:
            print("You are a disgrace to the Kriegsmarine, your family, and yourself. Consider a career after the war on land.")
        else:
            print("You are a disgrace to the Kriegsmarine, your family, and yourself. You should have signed up for something on land instead.")
    elif grtSunk < 100000:
        print("DRAW")
        print("You have fulfilled your obligations to the nation. Book and movies about you are probably not in the cards, however.")
    elif grtSunk < 150000:
        print("MARGINAL VICTORY")
        if "Survived" in cause:
            print("You have enjoyed a modicum of success as a U-Boat commander. Your crew respects your abilities, and Oberkommando der Marine places you in Training Command.")
        else:
            print("You have enjoyed a modicum of success as a U-Boat commander. Had you survived, Oberkommando der Marine would have placed you in Training Command.")
    elif grtSunk < 200000:
        print("SUBSTANTIAL VICTORY")
        if "Survived" in cause:
            print("You are one of the Kriegsmarine’s top U-Boat elite, and have gained the respect of your peers, your crew, and commanders. You are often mentioned in the nation’s papers and are offered command of a flotilla.")
        else:
            print("You were one of the Kriegsmarine’s top U-Boat elite, and had gained the respect of your peers, your crew, and commanders. Had you survived, you would have been offered command of a flotilla.")
    else:
        print("DECISIVE VICTORY")
        if "Survived" in cause:
            print("You are the scourge of the seas and the pride of the entire Kriegsmarine. Your legendary exploits place you at the top of the U-Boat elite and are mentioned prominently in propaganda efforts. Your peers are amazed at your bold successes. You hopefully retire peacefully in what’s left of Hamburg after the war.")
        else:
            print("You were the scourge of the seas and the pride of the entire Kriegsmarine. Your legendary exploits place you at the top of the U-Boat elite and are mentioned prominently in propaganda efforts.")

    print("\n")
    printTable()

    raise SystemExit

#-----------------------------------------------SCORE RECORDING

def createScoreArray():
    with open("scores.txt", "r") as fp:
        lines = fp.readlines()
        scoreList = []

        for x in range (len(lines)):
            y = lines[x].split("_")
            y[13] = y[13].replace("\n", "")
            newEntry = addScore(y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12], y[13])
            scoreList.append(newEntry)

        return scoreList

def addScore(name, uboat, type, patrols, GRT, damageDone, SS, WS, hitsTaken, ran, fate, rank, awards, timestamp):

    newDictEntry = {
                "NAME" : name,
                "U-BOAT" : uboat,
                "TYPE" : type,
                "PATROLS" : patrols,
                "GRT" : GRT,
                "DAMAGE DONE" : damageDone,
                "SS" : SS,
                "WS" : WS,
                "HITS TAKEN" : hitsTaken,
                "RAN" : ran,
                "FATE" : fate,
                "RANK": rank,
                "AWARDS" : awards,
                "TIMESTAMP" : timestamp
            }
    return newDictEntry

def insertNewScore(name, uboat, type, patrols, GRT, damageDone, SS, WS, hitsTaken, ran, fate, rank, awards, timestamp):

    newList = []
    notInserted = True
    originalList = createScoreArray()

    try:
        GRTINT = GRT.replace(",", "")
        GRTINT = int(GRTINT)
    except:
        print("Error creating GRT int")

    for x in range (len(originalList)):
        try:
            origGRT = originalList[x]["GRT"]
            origGRT = origGRT.replace(",", "")
            origGRT = int(origGRT)
        except:
            print("Error creating original GRT int")

        if GRTINT > origGRT and notInserted:
            toAdd = addScore(name, uboat, type, patrols, GRT, damageDone, SS, WS, hitsTaken, ran, fate, rank, awards, timestamp)
            newList.append(toAdd)
            notInserted = False

        newList.append(originalList[x])
    #add for very end of list
    if notInserted:
        toAdd = addScore(name, uboat, type, patrols, GRT, damageDone, SS, WS, hitsTaken, ran, fate, rank, awards, timestamp)
        newList.append(toAdd)

    writeNewScores(newList)

def writeNewScores(listOfScores):
    f = open("scores.txt", "w")
    for x in range (len(listOfScores)):
        for key in (listOfScores[x]):
            f.write(listOfScores[x][key])
            if key != "TIMESTAMP":
                f.write("_")
            else:
                if x != len(listOfScores) - 1:
                    f.write("\n")

def printTable():
    scoreList = createScoreArray()

    #print table header
    print("———————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
    print("  #  |        CAPTAIN NAME       |  U-BOAT   | TYPE  | PTRLS |    GRT    | DMG DON | SS  | WS  | HTS RCV | RAN |               FATE")
    #COLUMN SPACING: 5 RANK, 27 NAME, 11 UBOAT, 7 PATROLS, 11 GRT, 13 DAMAGE DONE, 13 HITS TAKEN, 5 RE, 12+ FATE
    print("———————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
    for x in range (len(scoreList)):
        printColumn(5, str(x+1))
        printColumn(27, scoreList[x]["NAME"])
        printColumn(11, scoreList[x]["U-BOAT"])
        printColumn(7, scoreList[x]["TYPE"])
        printColumn(7, scoreList[x]["PATROLS"])
        printColumn(11, scoreList[x]["GRT"])
        printColumn(9, scoreList[x]["DAMAGE DONE"])
        printColumn(5, scoreList[x]["SS"])
        printColumn(5, scoreList[x]["WS"])
        printColumn(9, scoreList[x]["HITS TAKEN"])
        printColumn(5, scoreList[x]["RAN"])
        printColumn(150, scoreList[x]["FATE"], True)


def printColumn(totalWidth, toPrint, fate = False):
    midpoint = int(math.ceil(totalWidth / 2))
    middleOfToPrint = int(math.ceil(len(toPrint) / 2))
    totalSpaces = totalWidth - len(toPrint)
    spacesOnLeft = totalSpaces / 2
    spacesOnRight = totalSpaces / 2

    if spacesOnLeft % 2 != 0:
        spacesOnLeft = math.floor(spacesOnLeft)
    if spacesOnRight % 2 != 0:
        spacesOnRight = math.ceil(spacesOnRight)

    spacesOnLeft = int(spacesOnLeft)
    spacesOnRight = int(spacesOnRight)

    if fate:
        spacesOnLeft = 2

    for x in range (spacesOnLeft):
        print(" ", end="")
    print(toPrint, end="")

    if not fate:
        for x in range(spacesOnRight):
            print(" ", end="")
        print("|", end="")
    else:
        print("")

#============================================= HELP PROMPT

def helpText(prompt):
    match prompt:
        case "Enter U-Boat #: ":
            print("---All U-Boats were indentified by a number. For example, U-95. Choose a number between 1 and 9999.")
        case "Choose a U-Boat: ":
            print("---The two main types of U-Boats during the war were type VII and type IX boats with some differences in variants.")
            print("---Choosing a boat also determines the start date of your campaign.")
            print("---Type VII boats were the workhorse of the Kriegsmarine. Very versatile and deadly.")
            print("---Type IX boats were larger and less common. They had greater range (and thus longer patrols) at the expense of less overall number of patrols compared to VII boats.")
        case "Choose new U-Boat: ":
            print("---You've been given a reassignment opportunity to move into a new boat of the same type. This is your chance to get into a newer variant of boat.")
        case "Pick your orders: " | "PATROL ASSIGNMENT: Roll to choose next patrol? ":
            print("---If you're lucky (and with high rank, you're more likely to be lucky) you can choose your next patrol assignment.")
            print("---The ability to choose your assignment lets you weed out unfavorable patrol orders at the very least.")
        case "Follow damaged ship(s) or the convoy?\n1) Damaged Ships\n2) Convoy":
            print("---Choose if you'd like to ATTEMPT to follow the convoy (which generates a new set of 4 ships if successful) or follow the damaged ship(s)")
            print("---Following damaged ships is always guaranteed. Any escort (if present) may or may not remain with damaged ship.")
        case "Follow damaged ship(s) or the rest?\n1) Damaged Ship(s)\n2) Undamaged Ship(s)":
            print("---Choose if you'd like to ATTEMPT to follow the undamaged ship(s) or follow the damaged ship(s)")
            print("---Following damaged ships is always guaranteed. Any escort (if present) may or may not remain with damaged ship.")
        case "Select ship to follow: ":
            print("---Choose specifically which ship to pursue and attack again.")
        case "Do you wish to attack: \n1) Surfaced\n2) Submerged ":
            print("---Attacking from the surface gives you a slight advantage (-1) to hit because your crew can use the UZO to fire from.")
            print("---The disadvantage is that with escorts present, you will not be able to dive to test depth on the first round of attacks from escorts.")
            print("---In addition, in later years (1941+), enemy radar has improved enough that it actually makes it a bit easier to detect and attack you.")
        case "Choose Range:\n1) -WARNING ESCORT- Close\n2) Medium Range\n3) Long Range ":
            print("---Attacking at closer range makes it more likely to hit. At close range, a hit is 2D6 roll of 8 or less, before modifiers.")
            print("---However, at close range the escort has a chance to detect you (10+) before you even get your torpedoes off thus ruining this attack.")
            print("---Not to mention, at close range escorts will have an easier time finding you to drop depth charges. Conversely at long range they will have a harder time.")
            print("---Finally, electric (G7e) torpedoes struggle at longer ranges and are less likely to hit beyond close range.")
        case "Choose Range:\n1) Close\n2) Medium Range\n3) Long Range ":
            print("---Attacking at closer range makes it more likely to hit. At close range, a hit is 2D6 roll of 8 or less, before modifiers.")
            print("---Electric (G7e) torpedoes struggle at longer ranges and are less likely to hit beyond close range.")
        case "Enter ship # from above to target. Enter 0 if done attacking. ":
            print("---Choose which ship to assign torpedoes to fire at. Order does not matter.")
        case "Fire how many G7a torpedoes? ":
            print("---Choose how many steam (G7a) torpedoes to fire at the target.")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
            print("---Each torpedo, if it hits and is not a dud, has a chance of doing between 1 and 4 damage.")
            print("---Ships with less than 5k GRT have 2HP. Ships with 5001-9999 GRT have 3HP. Ships with 10k+ have 4HP. Capital ships have 5 HP.")
        case "Fire how many G7e torpedoes? ":
            print("---Choose how many steam (G7a) torpedoes to fire at the target.")
            print("---Electric torpedoes are less reliable than steam until later in the war (mid-1940+) and suffer increased issues at medium and especially long ranges.")
            print("---Their advantage is that if fired during the day, escorts will have an harder time finding the sub compared to firing steam torpedoes.")
            print("---Each torpedo, if it hits and is not a dud, has a chance of doing between 1 and 4 damage.")
            print("---Ships with less than 5k GRT have 2HP. Ships with 5001-9999 GRT have 3HP. Ships with 10k+ have 4HP. Capital ships have 5 HP.")
        case "Number of shots to fire (1 or 2)":
            print("---Choose how much ammo to consume for the deck gun attack. Up to two can be consumed per attack round / turn.")
            print("---Technically, each ammo represents ~25 shots from the deck gun but is abstracted a bit in game.")
            print("---Each 'shot' has a chance, if hit, to do 1 or 2 damage.")
            print("---Ships with less than 5k GRT have 2HP. Ships with 5001-9999 GRT have 3HP. Ships with 10k+ have 4HP. Capital ships have 5 HP.")
        case "Current # of steam torpedoes to add. 0 - 1: " | "Current # of steam torpedoes to add. 0 - 2: "  | "Current # of steam torpedoes to add. 0 - 3: "  | "Current # of steam torpedoes to add. 0 - 4: " | "Current # of steam torpedoes to add. 0 - 5: ":
            print("---All U-Boats have a specific loadout of X number of G7a (steam) torpedoes and Y number of G7e (electric) torpedoes.")
            print("---Depending on the type, you can get a certain amount more of one type or another (based on the spread). This will reduce the number of the other torpedo type.")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
            print("---Electric torpedoes are less reliable than steam until later in the war (mid-1940+) and suffer increased issues at medium and especially long ranges.")
            print("---Their advantage is that if fired during the day, escorts will have an harder time finding the sub compared to firing steam torpedoes.")
        case "Current # of electric torpedoes to add. 0 - ":
            print("---All U-Boats have a specific loadout of X number of G7a (steam) torpedoes and Y number of G7e (electric) torpedoes.")
            print("---Depending on the type, you can get a certain amount more of one type or another (based on the spread). This will reduce the number of the other torpedo type.")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
            print("---Electric torpedoes are less reliable than steam until later in the war (mid-1940+) and suffer increased issues at medium and especially long ranges.")
            print("---Their advantage is that if fired during the day, escorts will have an harder time finding the sub compared to firing steam torpedoes.")
        case "Enter # of G7a steam torpedoes to load in the forward tubes: ":
            print("---This is the number of steam torpedoes to be loaded and will be ready to fire from the forward tubes at the next engagement.")
            print("---Entering a number less than the total tubes will mean the rest are loaded with electric type.")
            print("---Note: If you're loading during rearm at port, these are liable to be removed completely if you're assigned a minelaying mission (mines will take their place.)")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
        case "Enter # of G7a steam torpedoes to load in the aft tube(s): ":
            print("---This is the number of steam torpedoes to be loaded and will be ready to fire from the aft tube(s) at the next engagement.")
            print("---Entering a number less than the total tubes will mean the rest are loaded with electric type.")
            print("---Note: If you're loading during rearm at port, these are liable to be removed completely if you're assigned a minelaying mission (mines will take their place.)")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
        case "Enter # of G7a to load into the aft reserves: ":
            print("---This determines how many steam torpedoes will be placed in the aft reloads.")
            print("---Entering a number less than the total aft reserves will mean the rest are loaded with electric type.")
            print("---Steam torpedoes are more reliable (less dud rates than electric) and do not suffer range penalties.")
            print("---Their disadvantage is that if fired during the day, escorts will have an easier time finding the sub thanks to the steam of bubbles they leave on their way to the target.")
        case "1) Continue\n2) Stores Report\n3) Damage Report ":
            print("---Decide your next action.")
            print("---Continue moves you to the next box in your patrol, continuing onwards in your mission where you may or may not meet enemy ships.")
            print("---Your stores report allows you to take a look at all of the ammunition on the ship- what is loaded and still left in reserve in terms of torpedoes and gun ammunition.")
            print("---Damage report gives you a look at the state of your boat. What is and is not working, the hull condition, and the state of your crew members.")
        case "1) Continue\n2) Stores Report\n3) Damage Report\n4) Abort Patrol ":
            print("---Decide your next action.")
            print("---Continue moves you to the next box in your patrol, continuing onwards in your mission where you may or may not meet enemy ships.")
            print("---Your stores report allows you to take a look at all of the ammunition on the ship- what is loaded and still left in reserve in terms of torpedoes and gun ammunition.")
            print("---Damage report gives you a look at the state of your boat. What is and is not working, the hull condition, and the state of your crew members.")
            print("---Aborting your patrol turns your boat around to head back to port. This is not an automatic unsuccessful patrol.")
            print("---By aborting (because you are out of ammo or too damaged to complete the patrol), you are moved 2 spaces from port.")
        case "You can spend some luck to reroll the promotion roll. Spend luck? ":
            print("---You can spend a Hals und Beinbruch luck token to reroll your promotion roll.")
        case "You're eligible for reassignment to a new boat. Would you like to be reassigned? ":
            print("---You can choose not to spend your reassignment (instead wait for the preferred U-Boat type to become available)")
            print("---Reassignment allows you to move you and your crew to a new U-Boat of the same base type (VIIA -> VIIC)")
        case "Use same loadout as previous patrol? ":
            print("---This avoids going through setting up your U-Boat with the specific torpedo-type loadout.")
            print("---It loads the same torpedoes types into the same locations as your previous patrol.")
        case "Repair System? ":
            print("---You have gotten lucky and your sister ship has a limited number of repairs to help you out.")
            print("---Choose which system you'd like to have repaired back to working order.")
        case "Do you wish to attack? ":
            print("---You are able to determine whether it's worth the risk to attack or not.")
            print("---Some targets, especially small escorted ships, are not worth the risk, or worth the expenditure of torpedoes / ammo.")
        case "Attempt to follow convoy? ":
            print("---You can try to follow the convoy on a D6 roll of 4 or less.")
            print("---If successful, a new attack round will begin. This generates a new set of 4 ships to engage.")
        case "Follow target(s) to make another attack? ":
            print("---You can try to follow undamaged target(s) on a D6 roll of 4 or less.")
            print("---If there are damaged ships and undamaged ships, you will have to choose which to follow.")
            print("---Following damaged ships is always successful, while following undamaged capital ships is impossible.")
        case "Dive to test depth? ":
            print("---You can increase your odds at escape by diving extremely deep for 1 round of enemy attacks. Doing so gives you a -1 to detection odds.")
            print("---Doing so puts strain on your hull and automatically incurs 1 hull damage.")
            print("---In addition, you must roll to see if the boat can withstand the pressure of the deep dive.")
            print("---With more and more hull damage, the liklihood of a horrific implosion death increases. ")
        case "Do you wish to continue the attack at night? " | "Do you wish to continue the during the day? ":
            print("---You are presented with the option of attacking now, or waiting to flip from day to night or vice versa.")
            print("---Waiting runs the risk of losing your target. On a D6 roll of 5+ you lose your target.")
            print("---Attacking during the day is riskier and requires you to be submerged. Attacking with steam (G7a) torpedoes during the day makes it a bit easier for escorts to hunt you.")
            print("---Attacking at night allows you to attack surfaced or submerged. Attacking from the surface makes it slightly easier to hit targets with torpedoes but can be riskier.")
            print("---From the surface you cannot dive to test depth fast enough, so that option is unavailable the first round. Additionally radar (Available to the enemy 1941+) makes you easier to detect.")
        case "Should we make another attack? ":
            print("---You can make multiple attacks within the same round on unescorted targets. They must be different attack types, however.")
            print("---If you still haven't sunk your target(s) within the max 3 rounds (assuming 1 forward torpedo salvo, 1 aft torpedo salvo, and 1 deck gun attack), you will have the option to follow the target to make another attack.")
            print("---Unescorted targets may be able to call for assistance - this will result in escorts or planes showing up to attack you.")
        case "Reroll damage? ":
            print("---Thanks to your Hals und Beinbruch luck, you have the opportunity to reroll this damage roll.")
            print("---This helps you avoid especially crippling damage rolls.")
        case "Spend some luck to reroll the injury? ":
            print("---Thanks to your Hals und Beinbruch luck, you have the opportunity to reroll this injury roll.")
            print("---This helps you avoid especially crippling injury rolls.")