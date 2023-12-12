import random

def d6Roll():
    """Rolls 1 die."""
    roll = random.randint(1, 6)
    return roll


def d6Rollx2():
    """Rolls 2 dice."""
    roll = d6Roll() + d6Roll()
    return roll

def verifyYorN():
    """Input prompt for a Yes or No response. Returns 'Y' or 'N' string, otherwise loops endlessly"""
    notVerified = True
    while notVerified:
        inp = getInputNum("1) Yes\n2) No ", 1, 2)
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

def printRollandMods(roll, mods):
    """Prints a roll for some check, plus the modifiers, then the modified roll total."""
    total = roll + mods
    if mods <= 0:
        print("Roll:", roll, "• Modifiers:", mods, "| MODIFIED ROLL:", total)
    if mods > 0:
        toPrint = "Roll: " + str(roll) + " • Modifiers: +" + str(mods) + " | MODIFIED ROLL: " + str(total)
        print(toPrint)

def getInputNum(prompt, minINCLUSIVE = -1, maxINCLUSIVE = 100):
    invalidInput = True
    while invalidInput:
        print(prompt, end="")
        inp = input()
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


def scuttleFromFlooding(game):
    print("Emergency blow ballast! Attempting to abandon ship and scuttle the boat.")
    scuttleRoll = d6Rollx2()
    scuttleDRM = 0
    if game.sub.crew_health["Kommandant"] == 2:
        scuttleDRM += 1
    printRollandMods(scuttleRoll, scuttleDRM)
    if scuttleRoll + scuttleDRM <= 11:
        print("Successfully scuttled. The U-boat slips under the waves as your crew escapes.")
        gameover(game, "Scuttled due to flooding")
    else:
        print("The boat fails to go down and is successfully captured by the enemy. It's a massive failure as your crew are captured.")
        gameover("Boat was captured after emergency surface from flooding")



def scuttleFromDieselsInop(game):
    print("Emergency blow ballast! Attempting to abandon ship and scuttle the boat.")
    radioRoll = d6Rollx2()
    radioDRM = 0
    if game.sub.systems["Radio"] >= 2:
        radioDRM += 4
    printRollandMods(radioRoll, radioDRM)
    if radioRoll + radioDRM >= 11:
        gameover(game, "Lost at sea after scuttling the boat due to inoperative diesel engines")
    else:
        print("Rescused! Get new Uboat")
        print("TODO")
        #todo


def gameover(game, cause):
    print("++++++++++++++++++++++++++++")
    print("++        GAMEOVER!       ++")
    print("++++++++++++++++++++++++++++")
    print("Carrer summary:")
    print(game.rank[game.sub.crew_levels["Kommandant"]], game.kmdt)
    toprint = "Commander of U-" + game.id
    print(toprint)
    if len(game.pastSubs) > 0:
        toprint = "Other commands: "
        for x in range(len(game.pastSubs)):
            if x == len(game.pastSubs):
                toprint = toprint + "U-" + game.pastSubs[x]
            else:
                toprint = toprint + "U-" + game.pastSubs[x] + ", "
        print(toprint)
    toprint = "Fate of U-" + game.id + ": " + cause
    #TODO get ship that sunk it if applicable
    if game.sub.knightsCross > 0:
        print("Awards:", game.sub.awardName[game.sub.knightsCross])
    print("Number of patrols:", game.patrolNum)
    print("End date:", game.getFullDate)
    print("Ships sunk:", + str(len(game.shipsSunk)))
    damageCount = 0
    for x in range(len(game.shipsSunk)):
        damageCount += game.shipsSunk[x].damage
    print("Damage done:", damageCount)
    raise SystemExit