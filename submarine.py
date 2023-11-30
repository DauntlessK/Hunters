import random
import os
import time
from operator import *
from util import *

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
                self.patrol_length = 3                      # number of spaces during patrols
                self.hull_hp = 7                            # total hull damage before sinking
                self.flooding_hp = 7                        # total flooding damage before surfacing
                self.G7aStarting = 6                        # default load of G7a steam torpedoes
                self.G7eStarting = 5                        # default load of G7e electric torpedoes
                self.forward_tubes = 4                      # number of forward torpedo tubes
                self.aft_tubes = 1                          # number of aft torpedo tubes
                self.torpedo_type_spread = 1                # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10                     # current ammo for deck gun
                self.deck_gun_cap = 10                      # sub's deck gun ammo capacity
                self.reserves_aft = 0                       # number of aft torpedo roloads
                self.systems["3.7 Flak"] = -1               # large (3.7) flak (-1 means not present)
            case "VIIB" | "VIIC":
                self.patrol_length = 4  # number of spaces during patrols
                self.hull_hp = 8  # total hull damage before sinking
                self.flooding_hp = 8  # total flooding damage before surfacing
                self.G7aStarting = 8  # default load of G7a steam torpedoes
                self.G7eStarting = 6  # default load of G7e electric torpedoes
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
                self.G7aStarting = 12  # default load of G7a steam torpedoes
                self.G7eStarting = 10  # default load of G7e electric torpedoes
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
                self.G7aStarting = 12  # default load of G7a steam torpedoes
                self.G7eStarting = 10  # default load of G7e electric torpedoes
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
                self.G7aStarting = 8  # default load of G7a steam torpedoes
                self.G7eStarting = 6  # default load of G7e electric torpedoes
                self.forward_tubes = 4  # number of forward torpedo tubes
                self.aft_tubes = 1  # number of aft torpedo tubes
                self.torpedo_type_spread = 3  # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10  # current ammo for deck gun
                self.deck_gun_cap = 10  # sub's deck gun ammo capacity
                self.reserves_aft = 1  # number of aft torpedo reloads
                self.systems["3.7 Flak"] = -1  # large (3.7) flak (-1 means not present)

            # TODO VIID, VIIC Flak  (Unsure if VIID is accurate)

        self.G7a = 0
        self.G7e = 0

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
        self.minesLoadedForward = False
        self.minesLoadedAft = False

        # used to roll against to get damage location on sub
        self.damageChart = ["Batteries", "flooding", "crew injury", "Periscope", "Dive Planes", "Electric Engine #1",
                            "flooding", "Electric Engine #2", "Diesel Engine #1", "Flak guns", "Diesel Engine #2",
                            "3.7 Flak",
                            "flooding", "minor", "hull", "crew injury", "hull", "Deck Gun",
                            "hull", "Radio", "flooding", "flooding", "hull", "Flak Gun",
                            "flooding", "hull", "crew injury", "floodingx2", "hull", "Deck Gun",
                            "Hydrophones", "Aft Torpedo Doors", "crew injuryx2", "Forward Torpedo Doors", "hullx2",
                            "Fuel Tanks"]

        # --------CREW TRAINING LEVELS / RANKS
        #levels for individual crew members are 0=normal, 1=trained/expert
        #levels for kmdt are 0 = Oberleutnant zur See, 1 = Kapitan-leutnant, 2 = Fregatten-kapitan, 3 = Kapitan zur See
        #levels for regular crew are 0 = green, 1 = trained, 2 = Veteran, 3 = Elite
        self.crew_levels = {
            "Crew": 1,
            "Watch Officer 1": 0,
            "Watch Officer 2": 0,
            "Engineer": 0,
            "Doctor": 0,
            "Kommandant": 0
        }
        # --------CREW STATES
        #states are 0 = fine, 1 = LW, 2 = SW, 3 = KIA
        self.crew_health = {
            "Crew 1": 0,
            "Crew 2": 0,
            "Crew 3": 0,
            "Crew 4": 0,
            "Watch Officer 1": 0,
            "Watch Officer 2": 0,
            "Engineer": 0,
            "Doctor": 0,
            "Kommandant": 0,
            "Abwehr Agent": 0
        }

        #Knight's Cross decoration level
        #  0 = none
        #  1 = KC =   Knight's Cross (sink 100k GRT or sink 1 capital ship) - no +1 penalty for firing fore and aft salvo
        #  2 = KCO=   Knight's Cross & Oakleaves (Sink 175k GRT OR sink 1 capital ship after being given KC OR sink 75k GRT after being given GC)
        #  3 = KCO&S= Knight's Cross Oakleaves & Swords (Sink 250k GRT, OR sink 1 capital ship after being given KCO, or sink 75k GRT after being given GCO)
        #  4 = KCOS&D=Knight's Cross Oakleaves, Swords and Diamonds (Sink 300k GRT, sink 1 capital ship after being given KCO&S or sink 50k GRT after being given GCO&S
        self.knightsCross = 0

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
        self.forward_G7a = 0
        self.forward_G7e = 0
        self.aft_G7a = 0
        self.aft_G7e = 0
        self.reloads_forward_G7a = 0
        self.reloads_forward_G7e = 0
        self.reloads_aft_G7a = 0
        self.reloads_aft_G7e = 0

        print("Submarine Resupply - You are given ", self.G7aStarting, "(steam) and ", self.G7eStarting, "(electric) torpedoes.")
        print("You can adjust this ratio by ", self.torpedo_type_spread, "torpedo(es).")
        SA = -1
        while SA < 0 or SA > self.torpedo_type_spread:
            print("Current # of steam torpedoes to add. 0 -", self.torpedo_type_spread)
            SA = int(input())
        self.G7a = self.G7aStarting + SA
        self.G7e = self.G7eStarting - SA
        if SA == 0:  # if player did not add steam and remove electrics
            SE = -1
            while SE < 0 or SE > self.torpedo_type_spread:
                print("Current # of electric torpedoes to add. 0 -", self.torpedo_type_spread)
                SE = int(input())
            self.G7a = self.G7aStarting - SE
            self.G7e = self.G7eStarting + SE

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
            print("Remaining G7a steam torpedoes: ", self.G7a - f1 - f2)
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
            if self.minesLoadedForward:
                print("Forward- G7a:", "MINES", "/", self.reloads_forward_G7a, "G7e:", "MINES", "/",
                      self.reloads_forward_G7e)
            else:
                print("Forward- G7a:", self.forward_G7a, "/", self.reloads_forward_G7a, "G7e:", self.forward_G7e, "/",
                      self.reloads_forward_G7e)

        if specific == "" or specific == "Aft":
            if self.minesLoadedAft:
                print("Aft- G7a:", "MINES", "/", self.reloads_aft_G7a, "G7e:", "MINES", "/", self.reloads_aft_G7e)
            else:
                print("Aft- G7a:", self.aft_G7a, "/", self.reloads_aft_G7a, "G7e:", self.aft_G7e, "/",
                      self.reloads_aft_G7e)
        if specific == "" or specific == "Deck Gun":
            print("Deck Gun Ammo:", self.deck_gun_ammo, "/", self.deck_gun_cap)

    def reload(self):
        """Reloads forward tubes (gets input based on which types are available and which to load.)"""
        #check forward tubes needing reload
        if self.getTotalInTubes("Forward") != self.forward_tubes and not self.minesLoadedForward:
            self.subSupplyPrintout("Forward")
            # if there are forward steam reloads, otherwise no steam to reload
            if self.reloads_forward_G7a > 0:
                invalid = True
                while invalid:
                    f1 = int(input("Enter # of  G7a steam torpedoes to load in the forward tubes: "))
                    # check if G7a torpedoes to load + total currently in tubes is greater than total number of tubes
                    if f1 + self.getTotalInTubes("Forward") > self.forward_tubes:
                        continue
                    # check if G7a torpedoes to load is more than currently held on the boat
                    if f1 > self.reloads_forward_G7a:
                        continue
                    invalid = False
                self.forward_G7a += f1
                self.reloads_forward_G7a -= f1
            if self.reloads_forward_G7e > 0 and self.getTotalInTubes("Forward") != self.forward_tubes:
                invalid = True
                while invalid:
                    f1 = int(input("Enter # of  G7e electric torpedoes to load in the forward tubes: "))
                    # check if G7a torpedoes to load + total currently in tubes is greater than total number of tubes
                    if f1 + self.getTotalInTubes("Forward") > self.forward_tubes:
                        continue
                    # check if G7a torpedoes to load is more than currently held on the boat
                    if f1 > self.reloads_forward_G7e:
                        continue
                    invalid = False
                self.forward_G7e += f1
                self.reloads_forward_G7e -= f1

        # check aft tubes needing reload
        if self.getTotalInTubes("Aft") != self.aft_tubes and not self.minesLoadedAft:
            self.subSupplyPrintout("Aft")
            # if there are forward steam reloads, otherwise no steam to reload
            if self.reloads_aft_G7a > 0:
                invalid = True
                while invalid:
                    f1 = int(input("Enter # of  G7a steam torpedoes to load in the aft tubes: "))
                    # check if G7a torpedoes to load + total currently in tubes is greater than total number of tubes
                    if f1 + self.getTotalInTubes("Aft") > self.aft_tubes:
                        continue
                    # check if G7a torpedoes to load is more than currently held on the boat
                    if f1 > self.reloads_aft_G7a:
                        continue
                    invalid = False
                self.aft_G7a += f1
                self.reloads_aft_G7a -= f1
            if self.reloads_aft_G7e > 0 and self.getTotalInTubes("Aft") != self.aft_tubes:
                invalid = True
                while invalid:
                    f1 = int(input("Enter # of  G7e electric torpedoes to load in the aft tubes: "))
                    # check if G7a torpedoes to load + total currently in tubes is greater than total number of tubes
                    if f1 + self.getTotalInTubes("Aft") > self.aft_tubes:
                        continue
                    # check if G7a torpedoes to load is more than currently held on the boat
                    if f1 > self.reloads_aft_G7e:
                        continue
                    invalid = False
                self.aft_G7e += f1
                self.reloads_aft_G7e -= f1

        self.subSupplyPrintout()

    def crewKnockedOut(self):
        """Returns true if all 4 'regular' crewmen are SW or KIA - state 2 or 3"""
        if self.crew_health["Crew 1"] >= 2 and self.crew_health["Crew 2"] >= 2 and self.crew_health["Crew 3"] >= 2 and self.crew_health["Crew 4"] >= 2:
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
            gameover("Dove too deep and was crushed by the pressure")
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
                gameover("Sub was obliterated by too much damage")

    def damage(self, numOfHits):
        """Rolls against damage chart E4 x number of times and adjusts the Submarine object accordingly. Then checks
        for being sunk etc."""
        tookFloodingThisRound = False
        for x in range(numOfHits):
            damage = self.damageChart[random.randint(0, 35)]
            match damage:
                case "crew injury":
                    self.crewInjury()
                case "crew injuryx2":
                    self.crewInjury()
                    self.crewInjury()
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
                    # TODO damageVariation = d6Roll()
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
            if self.crew_health["Engineer"] >= 2:
                floodingMods += 1
            elif self.crew_levels["Engineer"] == 1:
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
            gameover("The sub's hull took too much damage")
        if self.flooding_Damage >= self.flooding_hp:
            print("The ship takes on too much water, forcing you to blow the ballast tanks and surface.")
            # todo scuttle
            gameover("Ship Scuttled")

    def dieselsInop(self):
        """Returns int of how many inoperative diesel engines"""
        numInOp = 0
        if self.systems["Diesel Engine #1"] == 2:
            numInOp += 1
        if self.systems["Diesel Engine #2"] == 2:
            numInOp += 1
        return numInOp

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

    def repair(self):

        damagedTotal = countOf(self.systems.values(), 1)
        count = 0
        if self.flooding_Damage > 0 or damagedTotal > 0:
            print("Repairing the boat.")

        self.pumps()

        if damagedTotal > 0:
            for key in self.systems:
                if self.systems[key] == 1:
                    repairRoll = d6Roll()
                    repairMod = 0
                    if self.crew_health["Engineer"] <= 1 and self.crew_levels["Engineer"] > 0:
                        repairMod -= 1
                    elif self.crew_levels["Engineer"] >= 2:
                        repairMod += 1
                    # determine amount to roll based on system damaged. # is inclusive so 4 is 4 or less.
                    if "Engine" in key:
                        toRoll = 4
                    elif key == "Hydrophones" or key == "Dive Planes" or key == "Radio" or key == "Fuel Tanks":
                        toRoll = 2
                    elif "Gun" in key:
                        toRoll = 2
                    elif key == "Periscope" or key == "Batteries":
                        toRoll = 4
                    elif "Doors" in key:
                        toRoll = 2
                    else:
                        print("Error getting damaged system repair roll.")

                    if repairRoll + repairMod <= toRoll:
                        print("Successfully repaired", key)
                        self.systems[key] = 0
                    else:
                        print("We aren't able to repair", key, "at sea.")
                        self.systems[key] = 2

        self.printStatus()

    def refit(self):
        """In port repair - systems and hull as well as healing crew and replacing any as necessary"""
        refitTime = 1   #default refit time in months

        #determine length of hull repair damage, then repair hull
        if self.hull_Damage == 0:
            self.hull_Damage = 0 #skip
        elif self.hull_Damage <= 3:
            print("One additional month for hull repairs.")
            refitTime += 1
        elif self.hull_Damage <= 6:
            print("Two additional months for hull repairs.")
            refitTime += 2
        else:
            print("Three additional months for major hull repair.")
            refitTime += 3
        self.hull_Damage = 0

        #determine length of systems damage, then repair all systems
        systemDamagedCount = 0
        for key in self.systems:
            if self.systems[key] >= 1:
                systemDamagedCount += 1
                self.systems[key] = 0
        if systemDamagedCount >= 3:
            print("Additional month of refit for systems repairs.")
            refitTime += 1

        self.crewHeal(refitTime)

        return refitTime

    def crewHeal(self, refitTime):
        """Goes through all crew members that are SW and KIA and replaces them as needed, otherwise heals the crew"""
        #TODO deal with long term injuries to KMDT
        crewReplacedCount = 0
        for key in self.crew_health:
            #check for seriously wounded members first and determine if they need to be replaced or will heal in time for next patrol
            if self.crew_health[key] == 2:
                monthsToHeal = d6Roll()
                if self.crew_levels["Doctor"] == 1 and self.crew_health["Doctor"] <= 1:
                    monthsToHeal -= 1
                if monthsToHeal > refitTime:
                    print(key, "is too injured to join us on our next patrol. He will be replaced.")
                    if "Crew" in key:
                        crewReplacedCount += 1
                    self.crew_levels[key] = 0
                else:
                    print(key, "has healed and is ready to join us on our next patrol.")
            #check if KIA, and replace him
            elif self.crew_health[key] == 4:
                print(key, "was killed in action the previous patrol. Another trained crew member has filled in.")
                self.crew_levels[key] = 0

            self.crew_health[key] = 0

        if crewReplacedCount >= 3:
            self.crew_levels["Crew"] -= 1
            if self.crew_levels["Crew"] < 1:
                self.crew_levels = 1

    def crewInjury(self):
        #todo probably need to rethink how injuries are stored
        crewInjuryRoll = d6Rollx2()
        severity = d6Roll()
        if self.crew_health["Doctor"] <= 1 and self.crew_levels["Doctor"] > 0:
            severity -= 1
        if severity <= 3:
            sevText = "lightly wounded!"
            wounds = 1
        elif severity <= 5:
            sevText = "severely wounded!"
            wounds = 2
        else:
            sevText = "killed in action!"
            wounds = 3
        match crewInjuryRoll:
            case 2:
                toprint = "Kmdt has been " + sevText
                print(toprint)
                self.crew_health["Kommandant"] += wounds
                if self.crew_health["Kommandant"] == 4:
                    gameover("Kommandant has been KIA")
            case 3:
                toprint = "1st Officer has been " + sevText
                print(toprint)
                self.crew_health["Watch Officer 1"] += wounds
            case 4:
                toprint = "Engineer has been " + sevText
                print(toprint)
                self.crew_health["Engineer"] += wounds
            case 5:
                toprint = "Doctor has been " + sevText
                print(toprint)
                self.crew_health["Doctor"] += wounds
            case 6 | 7 | 8 | 9:
                toprint = "Crew member has been " + sevText
                print(toprint)
                injuryAllocated = False
                for key in self.crew_health:
                    if "Crew" in key:
                        #find an uninjured crew first
                        if self.crew_health[key] == 0:
                            self.crew_health[key] += wounds
                            injuryAllocated = True
                            break
                    else:
                        continue
                if injuryAllocated == False:
                    #todo
                    print("Injury unallocated!")
            case 10:
                toprint = "Second Officer has been " + sevText
                print(toprint)


def printRollandMods(roll, mods):
    """Prints a roll for some check, plus the modifiers, then the modified roll total."""
    total = roll + mods
    if mods <= 0:
        print("Roll:", roll, "• Modifiers:", mods, "| MODIFIED ROLL:", total)
    if mods > 0:
        toPrint = "Roll: " + str(roll) + " • Modifiers: +" + str(mods) + " | MODIFIED ROLL: " + str(total)
        print(toPrint)