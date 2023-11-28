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
        inp = input("1) Yes\n2) No")
        match inp:
            case "1" | "Yes" | "Y" | "y" | "yes":
                return "Y"
            case "2" | "No" | "N" | "n" | "no":
                return "N"
            case _:
                print("Unknown command. Try again.")
                continue

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


def gameover(cause=""):
    print("++++++++++++++GAMEOVER!++++++++++++++")
    print("Carrer summary:")
    print(self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
    print("Number of patrols:", self.patrolNum)
    print("End date:", self.getFullDate)
    print("Cause:", cause)
    print("Ships sunk:", + str(len(self.shipsSunk)))
    damageCount = 0
    for x in range(len(self.shipsSunk)):
        damageCount += self.shipsSunk[x].damage
    print("Damage done:", damageCount)
    raise SystemExit