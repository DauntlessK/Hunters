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

def verifyNextAction():
    """For each step of a patrol, ask for what to do next. Returns string: 'Continue', 'Supply', 'Status', 'Abort'"""
    notVerified = True
    while notVerified:
        inp = input("1) Continue\n2) Stores Report\n3) Damage Report\n4) Abort Patrol")
        match inp:
            case "1" | "Continue" | "C" | "continue" | "c":
                return "Continue"
            case "2" | "Stores" | "S" | "stores" | "s":
                return "Stores"
            case "3" | "Damage" | "D" | "damage" | "d":
                return "Damage"
            case "4" | "Abort" | "A" | "abort" | "a":
                return "Abort"
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