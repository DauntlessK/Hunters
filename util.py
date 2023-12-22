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

def printRollandMods(rollFor, roll, mods):
    """Prints a roll for some check, plus the modifiers, then the modified roll total.
    Roll for x (7-): MF || Roll: 4 • Mods: +1"""
    total = roll + mods
    if mods <= 0:
        toPrint = rollFor + " " + str(total) + " || Roll: " + str(roll) + " • Mods: " + str(mods)
    if mods > 0:
        toPrint = rollFor + " " + str(total) + " || Roll: " + str(roll) + " • Mods: +" + str(mods)
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

def Escorted(ships):
    """Returns true if the list of ships passed has an escort (as its first ship)"""
    if ships[0].type == "Escort":
        return True
    else:
        return False
def scuttleFromFlooding(game, attacker, airAttack):
    print("Emergency blow ballast! Attempting to abandon ship and scuttle the boat.")
    scuttleRoll = d6Rollx2(game)
    scuttleDRM = 0
    if game.sub.crew_health["Kommandant"] == 2:
        scuttleDRM += 1
    printRollandMods("Scuttle roll (11-):", scuttleRoll, scuttleDRM)
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
    radioRoll = d6Rollx2(game)
    radioDRM = 0
    if game.sub.systems["Radio"] >= 2:
        radioDRM += 4
    printRollandMods(radioRoll, radioDRM)
    if radioRoll + radioDRM >= 11:
        causeText = "Lost at sea", game.getFullDate(), "after scuttling the boat due to inoperative diesel engines"
        gameover(game, causeText)
    else:
        print("Rescused! Get new Uboat")
        print("TODO")
        #todo


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
            if x == len(game.pastSubs):
                toprint = toprint + "U-" + str(game.pastSubs[x])
            else:
                toprint = toprint + "U-" + str(game.pastSubs[x]) + ", "
        print(toprint)

    #determine where in the patrol and what the orders were when game was ended
    adjustedOrders = game.currentOrders
    adjustedOrders = adjustedOrders.strip('(Minelaying)')
    adjustedOrders = adjustedOrders.strip('(Wolfpack)')
    adjustedOrders = adjustedOrders.strip('(Abwehr Agent Delivery)')
    if cause == "Survived - promoted to desk job":
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
        print("Awards:", game.sub.awardName[game.sub.knightsCross])
    print("Patrols completed:", str(game.patrolNum - 1))
    #print("End date:", game.getFullDate)
    print("Ships sunk:", str(len(game.shipsSunk)))
    grtSunk = 0
    for x in range (len(game.shipsSunk)):
        grtSunk += game.shipsSunk[x].GRT
    grtSunk = f"{grtSunk:,}"
    print("GRT sunk:", str(grtSunk))
    print("Damage done:", str(game.damageDone))
    print("Hits taken:", str(game.hitsTaken))
    print("Random Events:", str(game.randomEvents))
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

    raise SystemExit