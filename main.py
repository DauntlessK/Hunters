# Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os
import time
from operator import *


class Submarine():
    """Player's Submarine. Contains type, ammo, all damage-related stats, including crew health."""

    def __init__(self, subClass):
        self.subClass = subClass  # submarine type (IE: VIIC)

        # --------SUBSYSTEM STATES
        # states are: 0=operational, 1=damaged, 2=inoperational
        self.systems = {
            "Electric Engine #1": 0,
            "Electric Engine #2": 0,
            "Diesel Engine #1": 0,
            "Diesel Engine #2": 0,
            "Periscope": 0,
            "Radio": 0,
            "Hydrophones": 0,
            "Batteries": 0,
            "Forward Torpedo Doors": 0,
            "Aft Torpedo Doors": 0,
            "Dive Planes": 0,
            "Fuel Tanks": 0,
            "Deck Gun": 0,
            "Flak Gun": 0
        }

        # set sub-specific info
        match subClass:
            case "VIIA":
                self.patrol_length = 3  # number of spaces during patrols
                self.hull_hp = 7  # total hull damage before sinking
                self.flooding_hp = 7  # total flooding damage before surfacing
                self.G7a = 6  # default load of G7a steam torpedoes
                self.G7e = 5  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 1  # number of aft torpedo tubes
                self.torpedo_type_spread = 1  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10  # current ammo for deck gun
                self.deck_gun_cap = 10  # sub's deck gun ammo capacity
                self.reserves_aft = 0  # number of aft torpedo roloads
                self.systems["3.7 Flak"] = -1  # large (3.7) flak (-1 means not present)
            case "VIIB" | "VIIC":
                self.patrol_length = 4  # number of spaces during patrols
                self.hull_hp = 8  # total hull damage before sinking
                self.flooding_hp = 8  # total flooding damage before surfacing
                self.G7a = 8  # default load of G7a steam torpedoes
                self.G7e = 6  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 1  # number of aft torpedo tubes
                self.torpedo_type_spread = 3  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10  # current ammo for deck gun
                self.deck_gun_cap = 10  # sub's deck gun ammo capacity
                self.reserves_aft = 1  # number of aft torpedo reloads
                self.systems["3.7 Flak"] = -1  # large (3.7) flak (-1 means not present)
            case "IXA":
                self.patrol_length = 5  # number of spaces during patrols
                self.hull_hp = 8  # total hull damage before sinking
                self.flooding_hp = 8  # total flooding damage before surfacing
                self.G7a = 12  # default load of G7a steam torpedoes
                self.G7e = 10  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 2  # number of aft torpedo tubes
                self.torpedo_type_spread = 4  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 5  # current ammo for deck gun
                self.deck_gun_cap = 5  # sub's deck gun ammo capacity
                self.reserves_aft = 2  # number of aft torpedo reloads
                self.systems["3.7 Flak"] = 0  # large (3.7) flak (-1 means not present)
            case "IXB":
                self.patrol_length = 6  # number of spaces during patrols
                self.hull_hp = 8  # total hull damage before sinking
                self.flooding_hp = 9  # total flooding damage before surfacing
                self.G7a = 12  # default load of G7a steam torpedoes
                self.G7e = 10  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 2  # number of aft torpedo tubes
                self.torpedo_type_spread = 4  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 5  # current ammo for deck gun
                self.deck_gun_cap = 5  # sub's deck gun ammo capacity
                self.reserves_aft = 2  # number of aft torpedo reloads
                self.systems["3.7 Flak"] = 0  # large (3.7) flak (-1 means not present)
            case "VIID":
                self.patrol_length = 5  # number of spaces during patrols
                self.hull_hp = 8  # total hull damage before sinking
                self.flooding_hp = 8  # total flooding damage before surfacing
                self.G7a = 8  # default load of G7a steam torpedoes
                self.G7e = 6  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 1  # number of aft torpedo tubes
                self.torpedo_type_spread = 3  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10  # current ammo for deck gun
                self.deck_gun_cap = 10  # sub's deck gun ammo capacity
                self.reserves_aft = 1  # number of aft torpedo reloads
                self.systems["3.7 Flak"] = -1  # large (3.7) flak (-1 means not present)

            # TODO VIID, VIIC Flak  (Unsure if VIID is accurate)

        # ---------Ammunition (what's in what torpedo tube) and overall damage indicators
        self.hull_Damage = 0  # current amount of hull damage
        self.flooding_Damage = 0  # current amount of flooding
        self.forward_G7a = 0  # number of loaded G7a torpedoes (fore)
        self.forward_G7e = 0  # number of loaded G7e torpedoes (fore)
        self.aft_G7a = 0  # number of loaded G7a torpedoes (aft)
        self.aft_G7e = 0  # number of loaded G7e torpedoes (aft)
        self.reloads_forward_G7a = 0  # number of reloads forward of G7a
        self.reloads_forward_G7e = 0  # number of reloads forward of G7e
        self.reloads_aft_G7a = 0  # number of reloads aft of G7a
        self.reloads_aft_G7e = 0  # number of reloads aft of G7e

        # used to roll against to get damage location on sub
        self.damageChart = ["Batteries", "flooding", "crew injury", "Periscope", "Dive Planes", "Electric Engine #1",
                            "flooding", "Electric Engine #2", "Diesel Engine #1", "Flak guns", "Diesel Engine #2",
                            "3.7 Flak",
                            "flooding", "minor", "hull", "crew injury", "hull", "Deck Gun",
                            "hull", "Radio", "flooding", "flooding", "hull", "Flak Gun",
                            "flooding", "hull", "crew injury", "floodingx2", "hull", "Deck Gun",
                            "Hydrophones", "Aft Torpedo Doors", "crew injuryx2", "Forward Torpedo Doors", "hullx2",
                            "Fuel Tanks"]

        # --------CREW STATES & TRAINING LEVELS
        self.crew_level = 1  # 0=green,  1=trained,  2=veteran,  3=elite
        self.crew1 = 0  # 0=fine,   1=lw        2=sw        4=kia
        self.crew2 = 0
        self.crew3 = 0
        self.crew4 = 0
        self.WO1_level = 0  # 0=normal,  1=exp
        self.WO1 = 0
        self.WO2_level = 0
        self.WO2 = 0
        self.eng_level = 0
        self.eng = 0
        self.doc_level = 0
        self.doc = 0
        self.kmdt = 0

    def getType(self):
        """Returns string of submarine Type"""
        return self.subClass

    def getTotalInTubes(self, loc, type=""):
        """Returns the total number of torpedoes currently loaded in tubes in a given part (forward or aft)"""
        if loc == "Forward":
            if type == "":
                return self.forward_G7a + self.forward_G7e
            elif type == "G7a":
                return self.forward_G7a
            else:
                return self.forward_G7e
        elif loc == "Aft":
            if type == "":
                return self.aft_G7a + self.aft_G7e
            elif type == "G7a":
                return self.aft_G7a
            else:
                return self.aft_G7e

    def torpedoResupply(self):
        """Called for in-port resupply of torpedoes to determine how many of each torpedo is taken, and assigned where"""
        # TODO Resupply for minelaying missions (remove tubes and replace with mines)
        print("Submarine Resupply - You are given ", self.G7a, "(steam) and ", self.G7e, "(electric) torpedoes.")
        print("You can adjust this ratio by ", self.torpedo_type_spread, "torpedo(es).")
        SA = -1
        while SA < 0 or SA > self.torpedo_type_spread:
            print("Current # of steam torpedoes to add. 0 -", self.torpedo_type_spread)
            SA = int(input())
        self.G7a = self.G7a + SA
        self.G7e = self.G7e - SA
        if SA == 0:  # if player did not add steam and remove electrics
            SE = -1
            while SE < 0 or SE > self.torpedo_type_spread:
                print("Current # of electric torpedoes to add. 0 -", self.torpedo_type_spread)
                SE = int(input())
            self.G7a = self.G7a - SE
            self.G7e = self.G7e + SE

        # ask player how many steam torpedoes to load forward
        f1 = -1
        print("Number of forward tubes: ", self.forward_tubes)
        while (f1 < 0 or f1 > self.forward_tubes) and (f1 + self.getTotalInTubes("Forward")):
            f1 = int(input("Enter # of  G7a steam torpedoes to load in the forward tubes: "))
        self.forward_G7a = f1
        self.forward_G7e = self.forward_tubes - f1

        # ask player how many steam torpedoes to load aft
        f2 = -1
        print("Number of aft tubes: ", self.aft_tubes)
        while (f2 < 0 or f2 > self.aft_tubes) and (f2 + self.getTotalInTubes("Aft")):
            f2 = int(input("Enter # of G7a steam torpedoes to load in the aft torpedo tube(s): "))
        self.aft_G7a = f2
        self.aft_G7e = self.aft_tubes - f2

        # ask player how many steam torpedoes for aft reserve(s)
        if self.reserves_aft > 0 and self.G7a - f1 - f2 > 0:
            print("Remaining G7a steam topedoes: ", self.G7a - f1 - f2)
            f3 = -1
            while f3 < 0 or f3 > self.aft_tubes:
                f3 = int(input("Enter # of G7a to load into the aft reserves."))
            self.reloads_aft_G7a = f3
            self.reloads_aft_G7e = self.reserves_aft - f3
        elif self.G7a == 0 and self.reserves_aft > 0:  # if there are no steam & aft reserves, fill with electrics
            self.aft_G7e = self.reserves_aft

        self.reloads_forward_G7a = self.G7a - self.forward_G7a - self.aft_G7a - self.reloads_aft_G7a  # number of reloads forward of G7a
        self.reloads_forward_G7e = self.G7e - self.forward_G7e - self.aft_G7e - self.reloads_aft_G7e

        self.deck_gun_ammo = self.deck_gun_cap

    def fireTorpedo(self, forwardOrAft, type):
        """Fires a torpedo from the sub, removing it from the loaded 'tubes'"""
        match forwardOrAft:
            case "Forward":
                if type == "G7a":
                    self.forward_G7a -= 1
                else:
                    self.forward_G7e -= 1
            case "Aft":
                if type == "G7a":
                    self.aft_G7a -= 1
                else:
                    self.aft_G7e -= 1

    def subSupplyPrintout(self, specific=""):
        """Prints current ammunition loads (by default, forward, aft and deck gun ammo. Can pass Forward or Aft
        to get JUST the loadout of that part of the boat. Prints as LOADED/RELOADS for a specific type."""
        if specific == "" or specific == "Forward":
            print("Forward- G7a:", self.forward_G7a, "/", self.reloads_forward_G7a, "G7e:", self.forward_G7e, "/",
                  self.reloads_forward_G7e)
        if specific == "" or specific == "Aft":
            print("Aft- G7a:", self.aft_G7a, "/", self.reloads_aft_G7a, "G7e:", self.aft_G7e, "/",
                  self.reloads_aft_G7e)
        if specific == "" or specific == "Deck Gun":
            print("Deck Gun Ammo:", self.deck_gun_ammo, "/", self.deck_gun_cap)

    def reloadForward(self):
        """Reloads forward tubes (gets input based on which types are available and which to load.)"""
        self.subSupplyPrintout("Forward")

        # if there are forward steam reloads, otherwise no steam to reload
        if self.reloads_forward_G7a > 0:
            invalid = True
            print("Number of forward tubes: ", self.forward_tubes)
            while invalid:
                f1 = int(input("Enter # of  G7a steam torpedoes to load in the forward tubes: "))
                # check if G7a torpedoes to load + total currently in tubes is greater than total number of tubes
                if f1 + self.getTotalInTubes("Forward") > self.forward_tubes:
                    continue
                # check if G7a torpedoes to load is more than currently held on the boat
                if f1 > self.reloads_forward_G7a:
                    continue
                invalid = False

            self.forward_G7a = self.forward_G7a + f1
            self.reloads_forward_G7a = self.reloads_forward_G7a - f1

        # IF there are still empty tubes AND if there are forward electric reloads, otherwise no electrics to reload
        if self.getTotalInTubes("Forward") < self.forward_tubes and self.reloads_forward_G7e > 0:
            self.subSupplyPrintout("Forward")
            invalid = True
            while (invalid):
                f1 = int(input("Enter # of  G7e electric torpedoes to load in the forward tubes: "))
                # check if G7e torpedoes to load + total currently in tubes is greater than total number of tubes
                if f1 + self.getTotalInTubes("Forward") > self.forward_tubes:
                    continue
                # check if G7a torpedoes to load is more than currently held on the boat
                if f1 > self.reloads_forward_G7e:
                    continue
                invalid = False

            self.forward_G7e = self.forward_G7e + f1
            self.reloads_forward_G7e = self.reloads_forward_G7e - f1

        self.subSupplyPrintout()

    def crewKnockedOut(self):
        """Returns true if all 4 'regular' crewmen are SW or KIA - state 2 or 3"""
        if self.crew1 >= 2 and self.crew2 >= 2 and self.crew3 >= 2 and self.crew4 >= 2:
            return True
        else:
            return False

    def diveToTestDepth(self):
        """Performs the dive to test depth. Giving 1 damage then checking to see if further damage is incurred. Can
        recrusively call itself if damage continues."""
        self.hull_Damage = self.hull_Damage + 1
        crushdamage = d6Rollx2()
        print("Depth damage roll: ", crushdamage)
        if crushdamage < self.hull_Damage:
            print("The hull creaks until... CRUSH")
            gameover()
        elif crushdamage == self.hull_Damage:
            print("The hull strains under the pressure. Taking additional damage...")
            self.diveToTestDepth()
        else:
            print("The U-boat takes the pressure of the depths admirably.")

    def attacked(self, attackDepth, mod, year, airAttack=False):
        """When rolling against chart E3- when the sub takes damage. By default, escort attack only but can pass
        True as third value for an air attack. Mod (second param) is 1 when 12+ is rolled on detection."""
        attackRoll = d6Rollx2()
        attackMods = 0
        if self.systems["Fuel Tanks"] >= 1:
            attackMods += 1
        if self.systems["Hydrophones"] >= 1:
            attackMods += 1
        if self.systems["Batteries"] >= 1:
            attackMods += 1
        if self.systems["Electric Engine #1"] >= 1:
            attackMods += 1
        if self.systems["Electric Engine #2"] >= 1:
            attackMods += 1
        attackMods = attackMods + mod
        if year >= 1943:
            attackMods += 1
        if airAttack:
            attackMods += 2

        print("Taking damage!")
        printRollandMods(attackRoll, attackMods)

        match attackRoll + attackMods:
            case 2 | 3:
                print("Their depth charges were ineffective!")
            case 4 | 5 | 6:
                print("1 hit on the sub!")
                self.damage(1)
            case 7 | 8:
                print("2 hits on the sub!")
                self.damage(2)
            case 9 | 10:
                print("3 hits on the sub!")
                self.damage(3)
            case 11:
                print("4 hits on the sub!")
                self.damage(4)
            case 12:
                print("5 hits on the sub!!")
                self.damage(5)
            case 13 | 14 | 15 | 15 | 16 | 17 | 18 | 19 | 20:
                print("Too much damage sir, we're taking on too much water!!")
                gameover()

    def damage(self, numOfHits):
        """Rolls against damage chart E4 x number of times and adjusts the Submarine object accordingly. Then checks
        for being sunk etc."""
        tookFloodingThisRound = False
        for x in range(numOfHits):
            damage = self.damageChart[random.randint(0, 35)]
            match damage:
                case "crew injury":
                    # todo deal with crew injury
                    print("Crew Injury")
                case "crew injuryx2":
                    # todo deal with crew injury
                    print("Crew Injury x2!")
                case "flooding":
                    print("Flooding!")
                    self.flooding_Damage += 1
                    tookFloodingThisRound = True
                case "floodingx2":
                    print("Major flooding!")
                    self.flooding_Damage += 2
                    tookFloodingThisRound = True
                case "hull":
                    print("Hull damage!")
                    self.hull_Damage += 1
                case "hullx2":
                    print("Major hull damage!")
                    self.hull_Damage += 2
                case "Flak Guns":
                    if self.systems["3.7 Flak Gun"] >= 0:
                        print("Both flak guns have been damaged!")
                        self.systems.update({"3.7 Flak Gun": 1})
                    else:
                        print("Flak gun has been hit!")
                    self.systems.update({"Flak Gun": 1})
                case "minor":
                    print("Damage is minor, nothing to report!")
                case _:
                    print("The " + damage + " has taken damage!")
                    # damageVariation = d6Roll()
                    # match damageVariation:
                    #     case 1:
                    #         print("The" + self.systems[damage].key + "have taken damage!")
                    #     case 2:
                    self.systems.update({damage: 1})

        time.sleep(3)
        # check if flooding took place this round and roll for additional flooding chance
        if tookFloodingThisRound:
            addlFlooding = d6Roll()
            floodingMods = 0
            if self.eng >= 2:
                floodingMods += 1
            elif self.eng_level == 1:
                floodingMods -= 1

            printRollandMods(addlFlooding, floodingMods)

            if addlFlooding + floodingMods <= 4:
                print("Leaks have been patched- no more flooding.")
            else:
                print("Leaks weren't contained quickly enough! Additional flooding!")
                self.flooding_Damage = self.flooding_Damage + 1

        # check to see if sunk from hull damage
        if self.hull_Damage >= self.hull_hp:
            print("The hull sustains too much damage and the ship breaks apart under the damage, sinking.")
            gameover()
        if self.flooding_Damage >= self.flooding_hp:
            print("The ship takes on too much water, forcing you to blow the ballast tanks and surface.")
            # todo scuttle
            gameover()

    def printStatus(self):
        print("Current damage/HP: ", self.hull_Damage, "/", self.hull_hp)
        print("Current flooding/HP ", self.flooding_Damage, "/", self.flooding_hp)
        #check if any damaged systems, then print list
        damagedTotal = countOf(self.systems.values(), 1)
        count = 0
        if damagedTotal > 0:
            print("Damaged systems: ", end="")
            for key in self.systems:
                if self.systems[key] == 1:
                    if count == damagedTotal - 1:
                        print(key)
                    else:
                        print(key, end=", ")
                        count += 1
        # check if any inop systems, then print list
        inopTotal = countOf(self.systems.values(), 2)
        count = 0
        if inopTotal > 0:
            print("Inoperative systems: ", end="")
            for key in self.systems:
                if self.systems[key] == 2:
                    if count == inopTotal - 1:
                        print(key)
                    else:
                        print(key, end=", ")
                        count += 1

    def pumps(self):
        self.flooding_Damage = 0


class Ship():
    """All ships that can be targeted by the player."""
    type = ""  # small freighter, large freighter, tanker, warship or capital ship
    hp = 0
    damage = 0
    name = ""
    GRT = 0
    clss = ""
    sunk = False

    def __init__(self, type, loc=""):
        self.type = type
        self.G7aINCOMING = 0
        self.G7eINCOMING = 0

        match self.type:
            case "Small Freighter":
                self.damage = 0
                self.hp = 2
                self.sunk = False
                self.clss = type
                with open("Small Freighter.txt", "r") as fp:
                    lines = fp.readlines()
                    if loc == "North America":
                        print("Get NA small freighter from end of list")
                        # TODO add NA freighters AFTER regular freighters
                        # TODO get lines[randomint] of 101-120 or whatever
                    else:
                        entry = lines[random.randint(1, 25)]  # TODO finish small freighter .txt and increase to 100
                    entry = entry.split("-")
                    self.name = entry[0]
                    self.GRT = int(entry[1])

            case "Large Freighter" | "Tanker":
                with open(f"{type}.txt", "r") as fp:
                    lines = fp.readlines()
                    if loc == "North America":
                        print("Get NA ship from end of list")
                        # TODO add NA freighters AFTER regular freighters
                        # TODO get lines[randomint] of 101-120 or whatever
                    else:
                        entry = lines[
                            random.randint(1, 25)]  # TODO finish large freighter.txt + tanker.txt and increase to 100
                    entry = entry.split("-")
                    self.name = entry[0]
                    self.GRT = int(entry[1])
                if self.GRT >= 10000:
                    self.hp = 4
                else:
                    self.hp = 3
                self.clss = type
                self.damage = 0
                self.sunk = False

            case "Escort":
                with open("Escort.txt", "r") as fp:
                    lines = fp.readlines()
                    entry = lines[random.randint(1, 669)]
                    entry = entry.split("#")
                    self.name = entry[0]
                    self.clss = entry[1]
                    self.GRT = int(entry[2])
                    self.hp = 4  # TODO doublecheck HP on escorts
                    self.damage = 0
                    self.sunk = False

            case "Capital Ship":
                # TODO - add capital ship.txt etc
                print("TODO")

    def __str__(self):
        s = self.name + " (" + self.clss + " [" + str(self.GRT) + " GRT])"
        return s

    def fireG7a(self, num):
        """Adds a steam torpedo to the ship's incoming type. Helps keep track of how many to roll against."""
        self.G7aINCOMING = self.G7eINCOMING + num

    def fireG7e(self, num):
        """Adds an electric torpedo to the ship's incoming type. Helps keep track of how many to roll against."""
        self.G7eINCOMING = self.G7eINCOMING + num

    def hasTorpedoesIncoming(self):
        """Returns true if it has any incoming torpedoes"""
        if self.G7aINCOMING > 0 or self.G7eINCOMING > 0:
            return True
        else:
            return False

    def resetG7a(self):
        """Sets incoming steam torpedoes to zero"""
        self.G7aINCOMING = 0

    def resetG7e(self):
        """Sets incoming electric torpedoes to zero"""
        self.G7eINCOMING = 0

    def removeG7a(self):
        """Removes 1 steam torpedo from incoming - as in it was resolved."""
        self.G7aINCOMING = self.G7aINCOMING - 1

    def removeG7e(self):
        """Removes 1 electric torpedo from incoming - as in it was resolved."""
        self.G7eINCOMING = self.G7eINCOMING - 1

    def takeDamage(self, dam):
        """Attributes damage to this ship object and checks if it was sunk."""
        self.damage = self.damage + dam
        if self.damage >= self.hp:
            self.sunk = True


def d6Roll():
    """Rolls 1 die."""
    roll = random.randint(1, 6)
    return roll


def d6Rollx2():
    """Rolls 2 dice."""
    roll = d6Roll() + d6Roll()
    return roll


class Game():

    def __init__(self):
        self.month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        self.date_month = 0
        self.date_year = 1939
        print("Welcome to The Hunters: German U-Boats at War, 1939-43")
        print("First choose a Submarine:")
        self.permMedPost = False
        self.permArcPost = False
        self.francePost = False
        self.sub = Submarine(self.chooseSub())
        self.kmdt = input("Enter Kommandant name: ")
        self.id = input("Enter U-Boat #: ")
        self.sub.torpedoResupply()
        self.rank = ["Oberleutnant zur See", "Kapitän-leutnant", "Korvetten-kapitän", "Fregatten-kapitän",
                     "Kapitän zur See"]
        self.rankMod = 0
        self.establishFirstRank()
        self.sub.subSupplyPrintout()
        print("---------------")
        print("Guten Tag,", self.rank[self.rankMod], "- The date is", self.getFullDate())
        self.currentOrders = ""
        self.patrolCount = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
                            "tenth",
                            "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
                            "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
                            "twenty-fourth"]
        self.patrolNum = 1
        self.randomEvent = False
        self.currentLocationStep = 0
        self.onStationSteps = self.sub.patrol_length
        self.patrolLength = 0
        self.G7aFired = 0
        self.G7eFired = 0
        self.shipsSunk = []
        self.gameloop()

    def getMonth(self):
        """Returns Month (#)"""
        return self.date_month

    def getYear(self):
        """Returns Year"""
        return self.date_year

    def getFullDate(self):
        """Returns string of the month - year"""
        toReturn = self.month[self.date_month] + " - " + str(self.date_year)
        return toReturn

    def advanceTime(self):
        """Moves time forward one month and checks for end of game if beyond June 1943"""
        self.date_month += 1
        if self.date_month == 12:
            self.date_month = 0
            self.date_year += 1
        if self.date_month >= 6 & self.date_year > 43:
            gameover()
        if (self.month[self.date_month] == "July") and self.date_year == 1940:
            self.francePost = True

    def establishFirstRank(self):
        """Determines starting rank of player"""
        if self.sub.getType() == "IXA" or self.sub.getType() == "IXB":
            self.rankMod = 1
        else:
            roll = d6Roll()
            print("Rolling for starting rank. Roll is: ", roll)
            if roll >= 3:
                self.rankMod = 1
            else:
                self.rankMod = 0

    def chooseSub(self):
        """Gets input from player to choose Submarine Type"""
        print("1. VIIA (Start date Sept-39)")
        print("2. VIIB (Start date Sept-39)")
        print("3. IXA (Start date Sept-39)")
        print("4. IXB (Start date Apr-40)")
        print("5. VIIC (Start date Oct-40)")
        print("6. VIID (Start date Jan-42)")
        print("7. VIIC Flak (Start date May-43)")
        subChosen = input()
        match subChosen:
            case "1" | "VIIA":
                self.date_month = 8
                self.date_year = 1939
                return "VIIA"
            case "2" | "VIIB":
                self.date_month = 8
                self.date_year = 1939
                return "VIIB"
            case "3" | "IXA":
                self.date_month = 8
                self.date_year = 1939
                return "IXA"
            case "4" | "IXB":
                self.date_month = 3
                self.date_year = 1940
                return "IXB"
            case "5" | "VIIC":
                self.date_month = 9
                self.date_year = 1940
                self.francePost = True
                return "VIIC"
            case "6" | "VIID":
                self.date_month = 0
                self.date_year = 1942
                self.francePost = True
                return "VIID"
            case "7" | "VIIC Flak":
                self.date_month = 4
                self.date_year = 1943
                self.francePost = True
                return "VIIC Flak"
            case _:
                print("Invalid Sub Type.")
                gameover()

    def startPatrol(self):
        """Starts a new patrol, getting new assignment based on rank, date etc."""
        if self.rankMod > 0:
            print("PATROL ASSIGNMENT: Roll to choose next patrol?")
            if verifyYorN() == "Y":
                roll = d6Roll()
                print("Die roll:", roll)
                if roll <= self.rankMod:
                    print("You may select your patrol.")
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), True)
                else:
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)
        else:
            self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)
        print("Patrol Assignment:", self.currentOrders)
        depart = "U-" + str(self.id) + " departs port early before dawn for " + self.rank[
            self.rankMod] + " " + self.kmdt + "'s " + str(self.patrolCount[self.patrolNum] + " patrol.")
        print(depart)
        self.currentLocationStep = 1
        self.patrolLength = self.getPatrolLength(self.currentOrders)

    def getPatrolLength(self, patrol):
        """Determines full length of a given patrol (number of on station steps + all transit steps"""
        match patrol:
            case "North America" | "Caribbean":
                return self.sub.patrol_length + 8  # NA patrol has normal 2 BoB + 2 transits + extra 4 transits
            case _:
                return self.sub.patrol_length + 4

    def getPatrol(self, month, year, roll, subClass, pickingPatrol):
        """Gets patrol based on date, type, permanent assignments, etc from patrol text files."""
        patrolChart = ""
        if year == 1939 or (month <= 2 and year == 1940):  # 1939 - Mar 1940
            patrolChart = "PatrolChart1.txt"
        elif month > 2 and month <= 5 and year == 1940:  # 1940 - Apr - Jun
            patrolChart = "PatrolChart2.txt"
        elif month >= 6 and month <= 11 and year == 1940:  # 1940 - Jul - Dec
            patrolChart = "PatrolChart3.txt"
        elif month >= 0 and month <= 5 and year == 1941:  # 1941 - Jan - Jun
            patrolChart = "PatrolChart4.txt"
        elif month >= 6 and month <= 11 and year == 1941:  # 1941 - Jul - Dec
            patrolChart = "PatrolChart5.txt"
        elif month >= 0 and month <= 5 and year == 1942:  # 1942 - Jan - Jun
            patrolChart = "PatrolChart6.txt"
        elif month >= 6 and month <= 11 and year == 1942:  # 1942 - Jul - Dec
            patrolChart = "PatrolChart7.txt"
        elif year == 1943:  # 1943
            patrolChart = "PatrolChart8.txt"
        else:
            print("Error getting txt")

        with open(patrolChart, "r") as fp:
            lines = fp.readlines()
            if pickingPatrol:
                print(lines)
                inp = input("Pick your orders (Case-sensitive): ")
                orders = inp
            else:
                orders = lines[roll - 2]

        orders = self.validatePatrol(orders)

        # change time on station (onStationSteps) by one less if North American Orders
        if orders == "North America" or orders == "Caribbean":
            self.onStationSteps = self.sub.patrol_length - 1
        elif "Minelaying" in orders or "Abwehr" in orders:
            self.onStationSteps = self.sub.patrol_length - 1
        else:
            self.onStationSteps = self.sub.patrol_length

        # strip any stray returns that may have gotten into the orders string
        orders = orders.strip('\n')

        self.currentOrders = orders

    def validatePatrol(self, orders):
        """Deal with changes in orders based on U-Boat type"""
        # noinspection PyUnresolvedReferences
        if orders == "Mediterranean" or orders == "Artic" and (self.subClass == "IXA" or self.subClass == "IXB"):
            orders = "West African Coast"
        if orders == "West African Coast" or orders == "Caribbean" and (
                self.subClass == "VIIA" or self.subClass == "VIIB" or self.subClass == "VIIC"):  # VII Cannot patrol west africa
            orders = "Atlantic"
        if orders == "British Isles" and self.subClass == "VIID":
            orders = "British Isles (Minelaying)"

        # deal with permanent stations
        if self.permMedPost:
            orders == "Mediterranean"
        if self.permArcPost:
            orders == "Arctic"

        return orders
        ##TODO: deal with VIID and VIIC Flak boats not being allowed in med (reroll req)

    def gameloop(self):
        """The normal game loop. Get patrol, conduct patrol, return and repair+rearm."""
        # while alive etc loop
        self.startPatrol()
        self.patrol()
        self.portReturn()

    def patrol(self):
        """Full patrol loop accounting for leaving port, transiting, patrolling and returning"""

        # if Artic patrol, roll to see if permanently assigned to Arctic
        if self.currentOrders == "Arctic":
            if d6Roll() <= 3:
                print("You've been assigned permanently to the Arctic.")
                self.permArcPost = True

        # while current step is less than the full patrol length (station patrol + transit boxes)
        while self.currentLocationStep <= self.getPatrolLength(self.currentOrders):

            currentBox = self.getLocation(self.currentOrders, self.currentLocationStep)
            # if sub is patrolling area (not in transit)
            if currentBox == self.currentOrders:
                self.onStationSteps -= 1
            self.getEncounter(currentBox, self.getYear(), self.randomEvent)

            # end of loop - go to next box of patrol
            self.currentLocationStep += 1

        # if it was a Med patrol, set U boat permanently to Med
        if self.currentOrders == "Mediterranean":  #
            self.permMedPost = True

    def portReturn(self):
        """Called after patrol to deal with notification, print out sunk ships so far, and then deal with repair and rearm."""
        # TODO messages based on repair (safely returns, returns with minor damage, limps back to port, etc?)
        returnMessage = "U-" + self.id + " glides back into port, docking with much fanfare."
        print(returnMessage)
        totalTonnage = 0
        for x in range(len(self.shipsSunk)):
            totalTonnage = totalTonnage + self.shipsSunk[x].GRT
        print("You've sunk", totalTonnage, "tons.")
        for x in range(len(self.shipsSunk)):
            print(self.shipsSunk[x])
        # TODO: crew increasing rank (3 patrols), captain promotion (1 year), healing, repair and rearm

    def getLocation(self, patrol, step):
        """Gets current location box on a patrol to determine encounter type (transit, Atlantic, etc)"""
        # TODO wolfpacks?
        match step:
            case 1:
                if patrol == "Norway" or patrol == "Arctic":
                    return "Transit"
                elif self.francePost and self.permMedPost == False:
                    return "Bay of Biscay"
                else:
                    return "Transit"
            case 2:
                if patrol == "Mediterranean" and self.permMedPost == False:
                    return "Gibraltar Passage"
                else:
                    return "Transit"
            case 3:
                if patrol == "North America" or patrol == "Caribbean":
                    return "Transit"
                else:
                    return patrol
            case 4:
                if patrol == "North America" or patrol == "Caribbean":
                    return "Transit"
                else:
                    return patrol
            case 5:
                return patrol
            case 6:
                if self.onStationSteps == 0:
                    if self.currentLocationStep == self.patrolLength - 1:
                        return "Transit"
                    elif self.currentLocationStep == self.patrolLength:
                        if self.permArcPost or self.francePost:
                            return "Bay of Biscay"
                    elif (patrol == "Mediterranean" or patrol == "Arctic"):
                        return "Transit"
                    else:
                        print("ERROR getting loc")
                else:
                    return patrol
            case 7:
                if self.onStationSteps == 0:
                    if self.currentLocationStep == self.patrolLength - 1:
                        return "Transit"
                    elif self.currentLocationStep == self.patrolLength:
                        if self.permArcPost or self.francePost:
                            return "Bay of Biscay"
                    elif (patrol == "Mediterranean" or patrol == "Arctic"):
                        return "Transit"
                    else:
                        print("ERROR getting loc")
                else:
                    return patrol
            case 8:
                if self.onStationSteps == 0:
                    if self.currentLocationStep == self.patrolLength - 1:
                        return "Transit"
                    elif self.currentLocationStep == self.patrolLength:
                        if self.permArcPost or self.francePost:
                            return "Bay of Biscay"
                    elif (patrol == "Mediterranean" or patrol == "Arctic"):
                        return "Transit"
                    else:
                        print("ERROR getting loc")
                else:
                    return patrol

    def getEncounter(self, loc, year, randomEvent):
        """Determines which location encounter chart to use, then rolls against and returns the string encounter name"""
        roll = d6Rollx2()
        print("Roll for location:", loc, "-", roll)
        if roll == 12 and randomEvent == False and loc != "Additional Round of Combat":  # First check if random event (natural 12)
            print("Random Event! TODO")
            return "Random Event"

        # determine if this is a mission box to roll against mission
        if (
                loc == "British Isles (Minelaying)" or loc == "British Isles (Abwehr Agent Delivery)") and self.currentLocationStep == 3:
            loc = "Mission"
        if loc == "North America (Abwehr Agent Delivery)" and self.currentLocationStep == 5:
            loc = "Mission"

        match loc:
            case "Transit":  # Transit encounter chart
                match roll:
                    case 2 | 3:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 12:
                        self.encounterAttack("Ship")
                    case _:
                        self.encounterNone(loc)
            case "Arctic":  # Artic encounter chart
                match roll:
                    case 2:
                        self.encounterAttack("Capital Ship")
                    case 3:
                        self.encounterAttack("Ship")
                    case 6 | 7 | 8:
                        self.encounterAttack("Convoy")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Atlantic" | "Atlantic (Wolfpack)":  # Atlantic encounter chart
                match roll:
                    case 2:
                        self.encounterAttack("Capital Ship")
                    case 3:
                        self.encounterAttack("Ship")
                    case 6 | 7 | 9 | 12:
                        self.encounterAttack("Convoy")
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "British Isles":  # British Isles encounter chart
                match roll:
                    case 2:
                        self.encounterAttack("Capital Ship")
                    case 5 | 8:
                        self.encounterAttack("Ship")
                    case 6:
                        self.encounterAttack("Ship + Escort")
                    case 10:
                        self.encounterAttack("Convoy")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Caribbean":  # Carribean encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 4 | 8:
                        self.encounterAttack("Ship")
                    case 6:
                        self.encounterAttack("Two Ships + Escort")
                    case 9 | 10:
                        return "Tanker"
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Mediterranean":  # Mediterranean encounter chart
                match roll:
                    case 2 | 3 | 11 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 4:
                        self.encounterAttack("Capital Ship")
                    case 7:
                        self.encounterAttack("Ship")
                    case 8:
                        self.encounterAttack("Convoy")
                    case 10:
                        self.encounterAttack("Two Ships + Escort")
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "North America":  # North American encounter chart
                match roll:
                    case 2:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 4 | 6:
                        self.encounterAttack("Ship")
                    case 5:
                        self.encounterAttack("Two Ships + Escort")
                    case 8:
                        self.encounterAttack("Two Ships")
                    case 9 | 12:
                        self.encounterAttack("Tanker")
                    case 11:
                        self.encounterAttack("Convoy")
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Norway":  # Norway encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 3 | 11:
                        self.encounterAttack("Capital Ship")
                    case 4 | 9 | 10:
                        self.encounterAttack("Ship + Escort")
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Spanish Coast":  # Spanish Coast encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case 5:
                        self.encounterAttack("Ship + Escort")
                    case 6 | 7:
                        self.encounterAttack("Ship")
                    case 10 | 11:
                        self.encounterAttack("Convoy")
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "West African Coast":  # West African Coast encounter chart
                match roll:
                    case 2:
                        self.encounterAttack("Capital Ship")
                    case 3 | 7:
                        self.encounterAttack("Ship")
                    case 6 | 10:
                        self.encounterAttack("Convoy")
                    case 9:
                        self.encounterAttack("Ship + Escort")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Additional Round of Combat" | "Gibraltar Passage":
                if year == 1942:
                    roll = roll - 1
                    print("-1 for 1942")
                elif year == 1943:
                    roll = roll - 2
                    print("-2 for 1943")
                if loc == "Gibraltar Passage":
                    roll = roll - 2
                    print("-2 for Gibraltar")
                match roll:
                    case -2, -1, 0, 1, 2, 3:
                        return "Escort"
                    case 4 | 5:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Bay of Biscay" | "Mission":
                if year == 1942 and loc == "Bay of Biscay":
                    roll = roll - 1
                    print("-1 for 1942")
                elif year == 1943 and loc == "Bay of Biscay":
                    roll = roll - 2
                    print("-2 for 1943")
                match roll:
                    case 0 | 1 | 2 | 3 | 4:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)

    ##----------------------------------------------- PATROL BOXES (TO DETERMINE WHICH ENCOUNTER TO ROLL)

    def patrolBoxTransit(self):
        """When ship is on a transit box."""
        if self.currentLocationStep == 1 and (self.currentOrders == "Artic" or self.currentOrders == "Norway"):
            print("Your U-Boat sails North towards its patrol area.")
        elif self.onStationSteps > 0:
            print("Your U-Boat sails on towards its assigned patrol area.")
        else:
            print("Your U-Boat turns around and heads for home.")
        self.getEncounter(self.getLocation(self.currentOrders, self.currentLocationStep), self.getYear(),
                          self.randomEvent)

    def patrolBoxBayOfBiscay(self):
        """When ship is on the Bay of Biscay box"""
        print("Your U-Boat transits across the perilous Bay of Biscay.")
        self.getEncounter(self.getLocation(self.currentOrders, self.currentLocationStep), self.getYear(),
                          self.randomEvent)

    ##----------------------------------------------- ENCOUNTERS

    def encounterNone(self, loc):
        """When '-' is rolled on the encounter chart for a given location"""
        randResult = random.randint(0, 2)
        match loc:
            case "Transit":
                match randResult:
                    case 0:
                        print("You have an uneventful transit.")
                    case 1:
                        print("Your cruise onwards is uneventful.")
                    case 2:
                        print("You continue to sail towards your destination, finding nothing along the way.")
            case "Bay of Biscay":
                print("You cross the Bay of Biscay without issues.")
            case "Mission":
                # TODO ?
                print("Mission")
            case "Arctic" | "Norway":
                match randResult:
                    case 0:
                        print("You spot nothing in this section of your frigid patrol.")
                    case 1:
                        print("Inclement weather ensures you find nothing on this part of your patrol.")
                    case 2:
                        print("This part of your Northern patrol is uneventful.")
            case "Atlantic" | "Atlantic (Wolfpack)":
                match randResult:
                    case 0:
                        print("You spot nothing in this part of the Atlantic.")
                    case 1:
                        print("Your patrol area in this part of the Atlantic seems to be empty.")
                    case 2:
                        print("Foul weather ensures you find nothing on this part of your patrol in the Atlantic.")
            case "British Isles":
                match randResult:
                    case 0:
                        print("No contacts in the vicinity of your ship off the British Isles.")
                    case 1:
                        print("Your patrol area near the shores of the British Isles is deserted.")
                    case 2:
                        print("Foul weather ensures you find nothing on this part of your patrol of the British Isles.")
            case "Caribbean" | "North America":
                match randResult:
                    case 0:
                        print("A long way from home and you find nothing on this part of the patrol.")
                    case 1:
                        print("This area of the Western waters appear to be empty.")
                    case 2:
                        print(
                            "Nasty storms reduce visibility to nothing - ensuring you find nothing on this part of your patrol.")
            case "Mediterranean" | "Spanish Coast" | "West African Coast":
                match randResult:
                    case 0 | 1:
                        print("This part of your patrol was uneventful.")
                    case 2:
                        print("Storms disrupt your ability to search for targets and you find nothing this time.")
            case "Gibraltar":
                match randResult:
                    case 0:
                        print("In the cover of night you were able to slip through the Gibraltar patrols.")
                    case 1:
                        print("A foggy morning and some luck allow you to pass unnoticed through Gibraltar.")
                    case 2:
                        print(
                            "A timely storm pushes several patrolling ships off station, allowing you to run straight "
                            "through Gibraltar.")
            case "Additional Round of Combat":
                # TODO
                print("TODO")
        time.sleep(2)

    def encounterAircraft(self, sub, year, patrolType):
        """When 'Aircraft' is rolled on a given encounter chart"""
        print("ALARM! Aircraft in sight! Rolling to crash dive!")
        roll = d6Rollx2()
        drm = 0

        if sub.crew_level == 0:
            drm -= 1
        elif sub.crew_level == 3:
            drm += 1
        if sub.crewKnockedOut():
            drm -= 1
        if sub.systems["Dive Planes"] > 0:
            drm -= 1
        if sub.subClass == "VIID" or sub.subClass == "IXA" or sub.subClass == "IXB":
            drm -= 1
        match year:
            case 1939:
                drm += 1
            case 1942:
                drm -= 1
            case 1943:
                drm -= 2
        if (
                patrolType == "British Isles (Minelaying)" or patrolType == "British Isles (Abwehr Agent Delivery)") and self.currentLocationStep == 3:
            drm -= 1
        if patrolType == "North America (Abwehr Agent Delivery)" and self.currentLocationStep == 5:
            drm -= 1

        total = roll + drm
        printRollandMods(roll, drm)

        if total <= 1:
            print("The aircraft caught us by surprise! 2 Attacks!")
            self.sub.attacked("Surfaced", 0, self.getYear(), True)
            self.sub.attacked("Surfaced", 0, self.getYear(), True)
        elif total <= 5:
            print("We didn't dive quick enough! 1 attack!")
            self.sub.attacked("Surfaced", 0, self.getYear(), True)
        else:
            print("Successful crash dive!")

        time.sleep(2)

    def encounterAttack(self, enc, existingShips = None):
        """When any type of ship/convoy is rolled as an encounter"""
        if existingShips is None:
            ship = self.getShips(enc)
        else:
            ship = existingShips

        bearing = random.randint(0, 359)
        course1 = random.randint(0, 15)
        course = ["N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE", "E", "ENE", "NE", "NNE"]
        if enc == "Tanker" or enc == "Ship":
            toPrint = "Ship Spotted! Bearing " + str(bearing) + " course " + course[course1]
            print(toPrint)
        else:
            toPrint = "Ships Spotted! Bearing " + str(bearing) + " course " + course[course1]
            print(toPrint)

        # Print target ship(s)
        for s in range(len(ship)):
            strng = "• " + str(ship[s])
            print(strng)
        time.sleep(2)

        print("Do you wish to attack?")
        if verifyYorN() == "N":
            # break out of encounter
            return "exit"

        action1 = self.attackRound(enc, ship)

        #allow for more rounds of combat
        #get number of ships sunk and damaged out of entire encounter
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #deal with unescorted ships (allow multiple weapons to be fired
        #TODO Probably consider all weapon firings on unescorted targets in 1 single round
        if ship[0].type != "Escort":
            action2 = self.attackRound(enc, ship)

        #check if all ships aside from escorts have been sunk (end of combat)
        if ship[0].type == "Escort":
            if shipsSunk == len(ship) - 1:
                print("END COMBAT - NO OTHER TARGETS - reload and repair")
        elif shipsSunk == len(ship):
            print("END COMBAT - NO OTHER TARGETS - reload and repair")
        else:
            #decide whether to follow or not
            print("Follow target(s) to make another attack?")
            follow = verifyYorN()
            if follow == "Y":
                #deal with convoys
                if enc == "Convoy":
                    if shipsDamaged > 0:
                        print("Follow damaged ship(s) or the convoy?")
                        print("1) Damaged ship(s)")
                        print("2) Convoy")
                        inp = ""
                        while inp != "1" or inp != "2":
                            inp = input()
                            match inp:
                                case "1":
                                    print("Automatic follow of damaged ships, remove undamaged ships. Roll for escorts")
                                    print("Reload and repair")
                                case "2":
                                    print("Roll for contact loss")
                                    print("start entire new convoy enc")
                elif enc == "Two Ships + Escort":
                    if shipsDamaged > 0:
                        print("Decide whether to follow undamaged ship(s) or damaged ships")
                        print("Follow damaged ship(s) or the rest?")
                        print("1) Damaged ship(s)")
                        print("2) Rest")
                        inp = ""
                        while inp != "1" or inp != "2":
                            inp = input()
                            match inp:
                                case "1":
                                    print("Automatic follow of damaged ships, remove undamaged ships. Roll for escorts")
                                    print("Reload and repair")
                                case "2":
                                    print("Roll to see if successfully follow ship(s)")
                                    print("Repair, reload and new enc with same ship(s)")
                    else:
                        print("Roll to see if successfully follow ship(s)")
                        print("Repair, reload and new enc with same ship(s)")





        action2 = None
        if shipsSunk != len(ship) and ship[0] != "Escort":
            self.sub.subSupplyPrintout()
            if action == "Forward Torpedo Salvo":
                action2 = self.getAttackType(ship, depth, timeOfDay, True)
            elif action == "Aft Torpedo Salvo":
                action2 = self.getAttackType(ship, depth, timeOfDay, False, True)
            elif action == "Deck Gun":
                action2 = self.getAttackType(ship, depth, timeOfDay, False, False, True)

        # if shipsSunk != len(ship) and ship[0] != "Escort" and action2 is not None:
        #     self.sub.subSupplyPrintout()

        #reload
        self.sub.reloadForward()
        self.G7aFired = 0
        self.G7eFired = 0

    def getShips(self, enc):
        """Creates and returns a list of ship object(s) for a given encounter."""
        tgt = []
        if enc == "Convoy" or enc == "Capital Ship" or "Escort" in enc:
            tgt.append(Ship("Escort"))

        if enc == "Tanker":
            tgt.append(Ship("Tanker"))

        if enc == "Capital Ship":
            tgt.append(Ship("Capital Ship"))

        if enc == "Ship" or enc == "Two Ships" or enc == "Convoy" or enc == "Ship + Escort" or enc == "Two Ships + Escort":
            tgt.append(Ship(self.getTargetShipType()))

        if "Two Ships" in enc or enc == "Convoy":
            tgt.append(Ship(self.getTargetShipType()))

        if enc == "Convoy":
            tgt.append(Ship(self.getTargetShipType()))
            tgt.append(Ship(self.getTargetShipType()))

        return tgt

    def getTargetShipType(self):
        """Rolls to determine a created ship object's type."""
        shipRoll = d6Roll()
        if shipRoll <= 3:
            return "Small Freighter"
        elif shipRoll <= 5:
            return "Large Freighter"
        else:
            return "Tanker"

    def escortDetection(self, enc, range, depth, timeOfDay, previouslyDetected, firedG7a, firedG7e):
        """Called when an escort detection roll is required."""
        attackDepth = depth

        escortRoll = d6Rollx2()
        escortMods = 0

        # deal with close range detection before anything has been fired first, then deal with normal detection
        if range == 8 and firedG7a == 0 and firedG7e == 0 and previouslyDetected == False:

            if self.getYear() >= 1941 and range == 8:
                escortMods = escortMods + (self.getYear() - 1940)
            # TODO mod for KMDT is KC+O+S and close range
        else:
            if depth != "Surfaced":
                # print("Current damage/HP: ", self.sub.hull_Damage, "/", self.sub.hull_hp)
                self.sub.printStatus()
                print("Dive to test depth?")
                testDive = verifyYorN()
                match testDive:
                    case "Y":
                        self.sub.diveToTestDepth()
                        depth = "Test Depth"
            if self.getYear() >= 1941 and range == 8:
                escortMods = escortMods + (self.getYear() - 1940)
            # TODO mod for KMDT is KC+O+S and close range
            if self.sub.kmdt >= 2 and self.sub.WO1 >= 2:
                escortMods += 2
            elif self.sub.kmdt == 2:
                escortMods += 1
            if self.sub.systems["Fuel Tanks"] >= 1:
                escortMods += 1
            if self.sub.systems["Dive Planes"] >= 1:
                escortMods += 1
            if enc == "Capital Ship":
                escortMods += 1
            if firedG7a and timeOfDay == "Day":
                escortMods += 1
            if previouslyDetected:
                escortMods += 1
            if range == 8 and (firedG7a > 0 or firedG7e > 0):
                escortMods += 1
            if attackDepth == "Surfaced" and timeOfDay == "Night" and self.getYear() >= 1941:
                escortMods += 1
            # TODO deal with forward + aft salvoes, wolfpack
            if range == 6:
                escortMods -= 1
            if depth == "Test Depth":
                escortMods -= 1

        print("Escort Pinging! ", end="")
        printRollandMods(escortRoll,escortMods)
        time.sleep(3)
        # snake eyes automatic avoid detection
        if escortRoll == 2:
            "Our ship completely avoided detection!"
            time.sleep(3)
            return "SnakeEyes"
        if escortRoll + escortMods <= 8:
            print("We've evaded detection!")
            self.sub.printStatus()
            time.sleep(2)
            return "escaped"
        elif escortRoll + escortMods <= 11:
            print("Detected!")
            self.sub.attacked(attackDepth, 0, self.getYear())
        elif escortRoll + escortMods >= 12:
            print("Detected! Big Problems!")
            self.sub.attacked(attackDepth, 1, self.getYear())
        time.sleep(3)
        self.escortDetection(enc, range, depth, timeOfDay, True, firedG7a, firedG7e)

    def wasDud(self, torp):
        """Determines whether a fired torpedo was a dud based on date and a d6 roll"""
        # TODO superior torpedoes mod?
        dudRoll = d6Roll()
        if self.getYear() >= 1941:
            if dudRoll == 1:
                return True
            else:
                return False
        elif self.getYear() == 1940 and self.date_month >= 6:
            if dudRoll >= 2:
                return False
            else:
                return True
        else:
            if torp == "G7a" and dudRoll >= 2:
                return False
            elif torp == "G7e" and dudRoll >= 3:
                return False
            else:
                return True

    def getAttackType(self, ship, depth, timeOfDay, firedForward=False, firedAft=False, firedDeckGun=False):
        """Gets a valid attack type and returns string of the attack."""
        notValid = True
        bowSalvoAvail = True
        aftSalvoAvail = True
        secondSalvoAvail = True
        deckGunAvail = True

        print("How should we attack?")
        #bow
        if self.sub.systems["Forward Torpedo Doors"] == 0 and (self.sub.forward_G7a > 0 or self.sub.forward_G7e > 0) and firedForward == False:
            print("1) Bow Torpedo Salvo")
        else:
            print("1) -UNAVAILABLE- Bow Torpedo Savlo ")
            bowSalvoAvail = False
        #aft
        if self.sub.systems["Aft Torpedo Doors"] == 0 and (self.sub.aft_G7a > 0 or self.sub.aft_G7e > 0) and firedAft == False:
            print("2) Aft Torpedo Salvo")
        else:
            print("2) -UNAVAILABLE- Aft Torpedo Salvo")
            aftSalvoAvail = False
        #bow and aft salvo
        if bowSalvoAvail and aftSalvoAvail and timeOfDay == "Night" and depth == "Surfaced":
            print("3) Forward & Aft Torpedo Salvo")
        else:
            print("3) -UNAVAILABLE- Forward & Aft Torpedo Salvo")
            secondSalvoAvail = False
        #deck gun
        if self.sub.deck_gun_ammo > 0 and depth == "Surfaced" and ship[0] != "Escort" and firedDeckGun == False:
            print("4) Engage with Deck Gun")
        else:
            print("4) -UNAVAILABLE- Engage with Deck Gun")
            deckGunAvail = False

        while notValid:
            action = input()
            if action == "1" and bowSalvoAvail:
                return "Forward Torpedo Salvo"
            if action == "2" and aftSalvoAvail:
                return "Aft Torpedo Salvo"
            if action == "3" and secondSalvoAvail:
                return "Bow & Aft Torpedo Salvo"
            if action == "4" and deckGunAvail:
                return "Deck Gun"
            print("We can't do that! Choose a valid attack!")

    def torpedoSalvo(self, foreOrAft, ship):
        printTargetShipList(ship)
        both = False
        if foreOrAft == "Both":
            foreOrAft = "Forward"
            both = True

        totalToFire = -1

        #validation loop to get a target, then # of torps to fire at it, then get next target if torpedoes are available
        while totalToFire < 1 and self.sub.getTotalInTubes(foreOrAft) != 0:

            target = int(input("Enter ship # from above to target. Enter 0 if done attacking."))

            target = target - 1
            if target < -1 or target > len(ship):
                continue
            if target == 0 and ship[0].type == "Escort":  #disallow firing at escort
                continue
            if target == -1:
                break

            self.sub.subSupplyPrintout(foreOrAft)
            #if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7a") > 0:
                #validation loop
                G7aFire = -1
                while G7aFire < 0 or G7aFire > self.sub.getTotalInTubes(foreOrAft, "G7a"):
                    G7aFire = int(input("Fire how many G7a torpedoes?"))
                ship[target].fireG7a(G7aFire)
                for x in range(G7aFire):
                    self.sub.fireTorpedo(foreOrAft, "G7a")
                    self.G7aFired += 1
                totalToFire = totalToFire - G7aFire
            if self.sub.getTotalInTubes(foreOrAft, "G7e") > 0:
                # validation loop
                G7eFire = -1
                while G7eFire < 0 or G7eFire > self.sub.getTotalInTubes(foreOrAft, "G7e"):
                    G7eFire = int(input("Fire how many G7e torpedoes?"))
                ship[target].fireG7e(G7eFire)
                for x in range(G7eFire):
                    self.sub.fireTorpedo(foreOrAft, "G7e")
                    self.G7eFired += 1
                totalToFire = totalToFire - G7eFire

            if both:
                self.sub.subSupplyPrintout("Aft")
                # if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
                if self.sub.getTotalInTubes("Aft", "G7a") > 0:
                    # validation loop
                    G7aFire = -1
                    while G7aFire < 0 or G7aFire > self.sub.getTotalInTubes("Aft", "G7a"):
                        G7aFire = int(input("Fire how many G7a torpedoes?"))
                    ship[target].fireG7a(G7aFire)
                    for x in range(G7aFire):
                        self.sub.fireTorpedo("Aft", "G7a")
                        self.G7aFired += 1
                    totalToFire = totalToFire - G7aFire
                if self.sub.getTotalInTubes("Aft", "G7e") > 0:
                    # validation loop
                    G7eFire = -1
                    while G7eFire < 0 or G7eFire > self.sub.getTotalInTubes("Aft", "G7e"):
                        G7eFire = int(input("Fire how many G7e torpedoes?"))
                    ship[target].fireG7e(G7eFire)
                    for x in range(G7eFire):
                        self.sub.fireTorpedo("Aft", "G7e")
                        self.G7eFired += 1
                    totalToFire = totalToFire - G7eFire

    def deckGunAttack(self, ship):
        printTargetShipList(ship)
        self.sub.subSupplyPrintout("Deck Gun")

        #get how many shots to fire (1 or 2)
        notValid = True
        while notValid:
            if self.sub.deck_gun_ammo == 1:
                shots = 1
            shots = int(input("Number of shots to fire (1 or 2)"))

    def attackRound(self, enc, ship, isFollowing = False):

        if isFollowing:
            print("Attack during day or night?")
            print("1) Day")
            print("2) Night")
            choice = input()
            match choice:
                case "1" | "Day" | "day":
                    timeOfDay = "Day"
                case "2" | "Night" | "night":
                    timeOfDay = "Night"
        else:
            timeRoll = d6Roll()
            if timeRoll <= 3:
                timeOfDay = "Day"
            else:
                timeOfDay = "Night"
            # TODO deal with arctic times

        print("Current time:", timeOfDay)

        # ask to flip to day or night
        if timeOfDay == "Night":
            print("Do you wish to attempt to attempt to follow the target and attack during the day?")
        else:
            print("Do you wish to attempt to attempt to follow the target and attack during the night?")
        if verifyYorN() == "Y":
            fliproll = d6Roll()
            if fliproll >= 5:
                print("We lost them! Roll:", fliproll)
                return exit
            else:
                print("We successfully followed them.")

        # choosing depth
        if ship[0].type == "Escort" and timeOfDay == "Day":
            print("Periscope Depth!")
            depth = "Submerged"
        else:
            typeofAttack = input("Do you wish to attack: \n1) Surfaced\n2) Submerged")
            match typeofAttack:
                case "Submerged" | "submerged" | "sub" | "2":
                    print("Periscope Depth!")
                    depth = "Submerged"
                case "Surface" | "surface" | "Surfaced" | "surfaced" | "1":
                    print("Manning the UZO for surface attack!")
                    depth = "Surfaced"

        # determine range
        if ship[0].type == "Escort":
            # print("Choose Range:\n1) Close -WARNING ESCORT-\n2) Medium Range\n3)Long Range")
            r = input("Choose Range:\n1) -WARNING ESCORT- Close\n2) Medium Range\n3) Long Range")
        else:
            r = input("Choose Range:\n1) Close\n2) Medium Range\n3) Long Range")
        match r:
            case "1" | "Close":
                r = 8  # must hit on 8 or less
                if ship[0].type == "Escort":
                    print("Approaching the targets... hopefully we are not spotted.")
                    self.escortDetection(enc, r, "Submerged", timeOfDay, False, 0, 0)
            case "2" | "Medium":
                r = 7  # hit on 7 or less
            case "3" | "Long":
                r = 6  # hit on 6 or less

        # show and assign weps
        self.sub.subSupplyPrintout()
        action = self.getAttackType(ship, depth, timeOfDay)

        match action:
            case "Forward Torpedo Salvo":
                self.torpedoSalvo("Forward", ship)
            case "Aft Torpedo Salvo":
                self.torpedoSalvo("Aft", ship)
            case "Forward & Aft Torpedo Salvo":
                self.torpedoSalvo("Both", ship)
            case "Deck Gun":
                self.deckGunAttack(ship)

        # resets to zero the number of torpedoes fired for the engagement
        self.G7aFired = 0
        self.G7eFired = 0
        # resolve each torpedo by rolling and getting roll mods
        self.resolveTorpedoes(ship, depth, r)

        # post shot escort detection
        if ship[0].type == "Escort":
            print("Escort incoming on our position!")
            self.escortDetection(enc, r, depth, timeOfDay, False, self.G7aFired, self.G7eFired)

        #deal with additional attacks on unescorted
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check for further attacks in same round for unescorted targets
        if ship[0].type != "Escort" and shipsSunk != len(ship):
            print("Should we make another attack?")
            if verifyYorN() == "Y":
                match action:
                    case "Forward Torpedo Salvo":
                        self.torpedoSalvo("Forward", ship)
                    case "Aft Torpedo Salvo":
                        self.torpedoSalvo("Aft", ship)
                    case "Forward & Aft Torpedo Salvo":
                        self.torpedoSalvo("Both", ship)
                    case "Deck Gun":
                        self.deckGunAttack(ship)

        return action

    def resolveTorpedoes(self, ship, depth, r):
        for s in range(len(ship)):
            while ship[s].hasTorpedoesIncoming():
                currentship = str(ship[s])
                torpRoll = d6Rollx2()
                rollMod = 0
                if depth == "Surfaced":
                    rollMod = rollMod - 1
                # TODO add mod for KC+Oakleaves award
                if self.sub.crew_level == 0:
                    rollMod += 1
                if self.sub.crewKnockedOut():
                    rollMod += 1
                if self.sub.kmdt > 1:
                    if self.sub.WO1 > 1:
                        rollMod += 2
                    else:
                        rollMod += 1
                # todo add mod for second salvo
                if ship[s].G7aINCOMING > 0:
                    print("Roll to hit on", ship[s].name, ": ", end="")
                    printRollandMods(torpRoll, rollMod)
                    self.G7aFired += 1
                    if torpRoll + rollMod <= r:
                        print("Hit! ", end="")
                        # roll for dud
                        if self.wasDud("G7a"):
                            print("Torpedo was a dud!")
                            time.sleep(3)
                            ship[s].removeG7a()
                        else:
                            damRoll = d6Roll()
                            match damRoll:
                                case 1:
                                    print("Massive damage! (4)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(4)
                                case 2:
                                    print("Critical damage! (3)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(3)
                                case 3:
                                    print("Serious damage! (2)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(2)
                                case 4 | 5 | 6:
                                    print("Minor damage! (1)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(1)
                            time.sleep(3)
                    else:
                        print("Torpedo Missed.")
                        ship[s].removeG7a()
                        time.sleep(3)
                if ship[s].G7eINCOMING > 0:
                    print("Roll to hit on", ship[s].name, ": ", end="")
                    printRollandMods(torpRoll, rollMod)
                    self.G7eFired += 1
                    if torpRoll + rollMod <= r:
                        print("Hit! ", end="")
                        # roll for dud
                        if self.wasDud("G7e"):
                            print("Torpedo was a dud!")
                            time.sleep(3)
                            ship[s].removeG7a()
                        else:
                            damRoll = d6Roll()
                            match damRoll:
                                case 1:
                                    print("Massive damage! (4)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(4)
                                case 2:
                                    print("Critical damage! (3)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(3)
                                case 3:
                                    print("Serious damage! (2)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(2)
                                case 4 | 5 | 6:
                                    print("Minor damage! (1)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(1)
                            time.sleep(3)
                    else:
                        print("Torpedo Missed.")
                        ship[s].removeG7e()
                        time.sleep(3)

            if ship[s].sunk:
                print(ship[s].name, "has been sunk!")
                self.shipsSunk.append(ship[s])
                time.sleep(3)


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


def gameover():
    print("GAMEOVER!")
    exit()


Game()
