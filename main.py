# Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os
import time
from operator import *
from ship import *
from submarine import *

#TODO:
#Deal with patrol aborts
#high score recording
#reroll for boats not allowed in med
#deal with missions 1) BUG mission encounter boxes 2) loading of mines 3) completing mine/abwehr missions
#successfull vs unsuccessful patrols
#crew and captain promotions (3 patrols and 1 year promotion check)
#decreased a crew skill level (to green?) for 3 unsuccessful patrols
#captain medals / awards - checking for awards and giving them
#port repair and time passage
#wolfpacks
#additional round of combat roll
#random events
#arctic times
#scuttle roll
#crew injury rolls
#add final subs (VIID and VIIC Flak)
#decreasing crew level for replacement of 3+ crew members (not below trained)
#request new uboat (reassignment rulebook 11.4) if, at the end of a patrol, player receives knights cross or higher vers
#capital ship count
#resupply at sea (rulebook 14.9)


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
        self.awardName = ["", "Knight's Cross", "Knight's Cross with Oakleaves", "Knight's Cross with Oakleaves and Swords",
                          "Knight's Cross with Oakleaves, Swords and Diamonds"]
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
        self.sunkOnCurrentPatrol = 0
        self.successfulPatrols = 0
        self.randomEvent = False
        self.currentLocationStep = 0
        self.onStationSteps = self.sub.patrol_length
        self.patrolLength = 0
        self.G7aFired = 0
        self.G7eFired = 0
        self.firedForward = False
        self.firedAft = False
        self.firedDeckGun = False
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

    def advanceTime(self, months):
        """Moves time forward"""

        #move forward x months
        self.date_month += 1
        #reset month to be within 0-11
        if self.date_month > 11:
            self.date_month = self.date_month - 12
            self.date_year += 1
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
                self.sub.crew_levels["Kommandant"] = 1
            else:
                self.sub.crew_levels["Kommandant"] = 0

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
        if self.sub.crew_levels["Kommandant"] > 0:
            print("PATROL ASSIGNMENT: Roll to choose next patrol?")
            if verifyYorN() == "Y":
                roll = d6Roll()
                print("Die roll:", roll)
                if roll <= self.sub.crew_levels["Kommandant"]:
                    print("You may select your patrol.")
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), True)
                else:
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)
        else:
            self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)
        print("Patrol Assignment:", self.currentOrders)
        depart = "U-" + str(self.id) + " departs port early before dawn for " + self.rank[
            self.sub.crew_levels["Kommandant"]] + " " + self.kmdt + "'s " + str(self.patrolCount[self.patrolNum] + " patrol.")
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
        playing = True
        while playing:
            self.startPatrol()
            self.patrol()
            self.portReturn()
            if self.date_year == 1943 and self.date_month > 5:
                playing = False

        #TODO game over stuff, high scores etc
        print("Game Over- GO THROUGH GAME OVER STEPS")

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

        #move forward 2 months per patrol of larger boats, otherwise 1 month
        if self.sub.getType() == "IXA" or self.sub.getType() == "IXB" or self.sub.getType() == "VIID":
            self.advanceTime(2)
        else:
            self.advanceTime(1)

        #TODO determine mission sucessful
        if "Minelaying" in self.currentOrders or "Abwehr" in self.currentOrders:
            print("FIGURE OUT IF THIS WAS SUCCESSFUL")
        else:
            if self.sunkOnCurrentPatrol > 0:
                self.successfulPatrols += 1
        #reset ships sunk
        self.sunkOnCurrentPatrol = 0

        #determine if crew rank increases
        if self.successfulPatrols >= 3:
            print("We've made 3 successfull patrols!")
            crewAd = d6Roll()
            match crewAd:
                case 1:
                    self.sub.crew_levels["Engineer"] = 1
                case 2:
                    self.sub.crew_levels["Doctor"] = 1
                case 3:
                    self.sub.crew_levels["Watch Officer 1"] = 1
                case 4:
                    self.sub.crew_levels["Watch Officer 2"] = 1
                case 5 | 6:
                    self.sub.crew_levels["Crew"] += 1
                    if self.sub.crew_levels["Crew"] > 3:
                        self.sub.crew_levels["Crew"] = 3

        totalTonnage = 0
        for x in range(len(self.shipsSunk)):
            totalTonnage = totalTonnage + self.shipsSunk[x].GRT
        totalTonnage = f"{totalTonnage:,}"
        print("You've sunk", totalTonnage, "tons.")
        for x in range(len(self.shipsSunk)):
            if x != len(self.shipsSunk):
                print(self.shipsSunk[x], end=", ")
            else:
                print(self.shipsSunk[x])
        if self.sub.knightsCross > 0:
            print(self.awardName[self.sub.knightsCross])

        self.patrolNum += 1
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
            case _:
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

        if sub.crew_levels["Crew"] == 0:
            drm -= 1
        elif ub.crew_levels["Crew"] == 3:
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

        #if starting an encounter with an existing ship list
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

        self.attackRound(enc, ship)

        #allow for more rounds of combat
        #get number of ships sunk and damaged out of entire encounter
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check if all ships aside from escorts have been sunk (end of combat)
        if ship[0].type == "Escort":
            if shipsSunk == len(ship) - 1:
                print("END COMBAT - NO OTHER TARGETS - reload and repair")
                self.sub.repair()
                self.sub.reload()
        elif shipsSunk == len(ship):
            print("END COMBAT - NO OTHER TARGETS - reload and repair")
            self.sub.repair()
            self.sub.reload()
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

        # if shipsSunk != len(ship) and ship[0] != "Escort" and action2 is not None:
        #     self.sub.subSupplyPrintout()

        #reload
        #self.sub.reload()
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
            if self.sub.knightsCross >= 3:
                escortMods -= 1
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
            if self.sub.knightsCross >= 3:
                escortMods -= 1
            if self.sub.crew_health["Kommandant"] >= 2 and self.sub.crew_health["Watch Officer 1"] >= 2:
                escortMods += 2
            elif self.sub.crew_health["Kommandant"] == 2:
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

    def getAttackType(self, ship, depth, timeOfDay, r):
        """Gets a valid attack type and returns string of the attack."""
        bowSalvoAvail = True
        aftSalvoAvail = True
        secondSalvoAvail = True
        deckGunAvail = True

        print("How should we attack?")
        #bow
        if self.sub.systems["Forward Torpedo Doors"] == 0 and (self.sub.forward_G7a > 0 or self.sub.forward_G7e > 0) and self.firedForward == False:
            print("1) Bow Torpedo Salvo")
        else:
            print("1) -UNAVAILABLE- Bow Torpedo Savlo ")
            bowSalvoAvail = False
        #aft
        if self.sub.systems["Aft Torpedo Doors"] == 0 and (self.sub.aft_G7a > 0 or self.sub.aft_G7e > 0) and self.firedAft == False:
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
        if self.sub.deck_gun_ammo > 0 and depth == "Surfaced" and ship[0].type != "Escort" and self.firedDeckGun == False and self.sub.systems["Deck Gun"] == 0:
            print("4) Engage with Deck Gun")
        else:
            print("4) -UNAVAILABLE- Engage with Deck Gun")
            deckGunAvail = False

        notValid = True
        while notValid:
            action = input()
            if action == "1" and bowSalvoAvail:
                self.torpedoSalvo("Forward", ship, depth, r)
                notValid = False
            elif action == "2" and aftSalvoAvail:
                self.torpedoSalvo("Aft", ship, depth, r)
                notValid = False
            elif action == "3" and secondSalvoAvail:
                self.torpedoSalvo("Both", ship, depth, r)
                notValid = False
            elif action == "4" and deckGunAvail:
                self.deckGunAttack(ship, r)
                notValid = False
            else:
                print("We can't do that! Choose a valid attack!")


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
            print("Do you wish to attempt to follow the target and attack during the day?")
        else:
            print("Do you wish to attempt to follow the target and attack during the night?")
        if self.sub.systems["Periscope"] >= 1:
            print("Reminder, Captain, that our periscope is knocked out and we cannot attack submerged.")
        if verifyYorN() == "Y":
            fliproll = d6Roll()
            if fliproll >= 5:
                print("We lost them! Roll:", fliproll)
                return exit
            else:
                print("We successfully followed them.")

        #call off attack if periscope is damaged and day, because submerged attacks cannot be made
        if self.sub.systems["Periscope"] >= 1 and timeOfDay == "Day":
            print("Unable to attack with periscope damaged and escort nearby. Submerging to escape.")
            return

        # choosing depth
        if ship[0].type == "Escort" and timeOfDay == "Day":
            print("Periscope Depth!")
            depth = "Submerged"
        elif ship[0].type == "Escort" and self.sub.systems["Periscope"] >= 1:
            print("Manning UZO for surface attack since periscope is damaged!")
            depth = "Surfaced"
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

        # resets to zero the number of torpedoes fired for the engagement
        self.G7aFired = 0
        self.G7eFired = 0
        self.firedForward = False
        self.firedAft = False
        self.firedDeckGun = False

        # show and assign weps
        self.sub.subSupplyPrintout()
        self.getAttackType(ship, depth, timeOfDay, r)

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
                self.getAttackType(ship, depth, timeOfDay, r)

        #recheck for sunk / damaged ships
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check third (final) time for attack in same round on unescorted targets
        if ship[0].type != "Escort" and shipsSunk != len(ship):
            print("Should we make another attack?")
            if verifyYorN() == "Y":
                self.getAttackType(ship, depth, timeOfDay, r)

    def getTarget(self, ship):
        notValid = True
        while notValid:
            if len(ship) > 1:
                target = int(input("Enter ship # from above to target. Enter 0 if done attacking."))
            else:
                target = 1

            target = target - 1
            if target < -1 or target > len(ship):
                continue
            elif target == 0 and ship[0].type == "Escort":  # disallow firing at escort
                continue
            else:
                break
        return target

    def torpedoSalvo(self, foreOrAft, ship, depth, r):
        printTargetShipList(ship)
        both = False
        if foreOrAft == "Both":
            foreOrAft = "Forward"
            both = True

        target = -1
        # validation loop to get a target, then # of torps to fire at it, then get next target if torpedoes are available
        while target != 0 and self.sub.getTotalInTubes(foreOrAft) != 0:

            target = self.getTarget(ship)

            self.sub.subSupplyPrintout(foreOrAft)
            # if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7a") > 0:
                # validation loop
                G7aFire = -1
                while G7aFire < 0 or G7aFire > self.sub.getTotalInTubes(foreOrAft, "G7a"):
                    G7aFire = int(input("Fire how many G7a torpedoes?"))
                ship[target].fireG7a(G7aFire)
                for x in range(G7aFire):
                    self.sub.fireTorpedo(foreOrAft, "G7a")
                    self.G7aFired += 1
            # if electric torpedoes are available, ask how many to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7e") > 0:
                # validation loop
                G7eFire = -1
                while G7eFire < 0 or G7eFire > self.sub.getTotalInTubes(foreOrAft, "G7e"):
                    G7eFire = int(input("Fire how many G7e torpedoes?"))
                ship[target].fireG7e(G7eFire)
                for x in range(G7eFire):
                    self.sub.fireTorpedo(foreOrAft, "G7e")
                    self.G7eFired += 1

            if foreOrAft == "Forward":
                self.firedForward = True
            else:
                self.firedAft = True

            # if both, allow for firing aft as well
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
                if self.sub.getTotalInTubes("Aft", "G7e") > 0:
                    # validation loop
                    G7eFire = -1
                    while G7eFire < 0 or G7eFire > self.sub.getTotalInTubes("Aft", "G7e"):
                        G7eFire = int(input("Fire how many G7e torpedoes?"))
                    ship[target].fireG7e(G7eFire)
                    for x in range(G7eFire):
                        self.sub.fireTorpedo("Aft", "G7e")
                        self.G7eFired += 1
                self.firedAft = True

        self.resolveTorpedoes(ship, depth, r)

    def resolveTorpedoes(self, ship, depth, r):
        for s in range(len(ship)):
            while ship[s].hasTorpedoesIncoming():
                currentship = str(ship[s])
                torpRoll = d6Rollx2()
                rollMod = 0
                if depth == "Surfaced":
                    rollMod -= 1
                if self.sub.knightsCross >= 2:
                    rollMod -= 1
                if self.sub.crew_levels["Crew"] == 0:
                    rollMod += 1
                if self.sub.crewKnockedOut():
                    rollMod += 1
                if self.sub.crew_health["Kommandant"] > 1:
                    if self.sub.crew_health["Watch Officer 1"] > 1:
                        rollMod += 2
                    else:
                        rollMod += 1
                # todo add mod for second salvo IGNORED FOR KNIGHTS CROSS level 1+
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
                                case _:
                                    print("Minor damage! (1)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(1)
                            time.sleep(3)
                    else:
                        print("Torpedo Missed.")
                        ship[s].removeG7a()
                        time.sleep(3)
                if ship[s].G7eINCOMING > 0:
                    if r == 7:
                        rollMod += 1
                    if r == 6:
                        rollMod += 2
                    print("Roll to hit on", ship[s].name, ": ", end="")
                    printRollandMods(torpRoll, rollMod)
                    self.G7eFired += 1
                    if torpRoll + rollMod <= r:
                        print("Hit! ", end="")
                        # roll for dud
                        if self.wasDud("G7e"):
                            print("Torpedo was a dud!")
                            time.sleep(3)
                            ship[s].removeG7e()
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
                                case _:
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
                self.sunkOnCurrentPatrol += 1
                time.sleep(3)

    def deckGunAttack(self, ship, r):
        printTargetShipList(ship)
        self.sub.subSupplyPrintout("Deck Gun")

        target = self.getTarget(ship)

        #get how many shots to fire (1 or 2)
        shots = -1
        while shots < 0 or shots > 2:
            if self.sub.deck_gun_ammo == 1:
                shots = 1
            shots = int(input("Number of shots to fire (1 or 2)"))

        for x in range (shots):
            gunRoll = d6Rollx2()
            rollMod = 0
            if self.sub.knightsCross >= 2:
                rollMod -= 1
            if self.sub.crew_levels["Crew"] == 0:
                rollMod += 1
            if self.sub.crewKnockedOut():
                rollMod += 1
            if self.sub.crew_health["Kommandant"] > 1:
                if self.sub.crew_health["Watch Officer"] > 1:
                    rollMod += 2
                else:
                    rollMod += 1

            print("Roll to hit on", ship[target].name, ": ", end="")
            printRollandMods(gunRoll, rollMod)
            if gunRoll + rollMod <= r:
                damRoll = d6Roll()
                mod = 0
                if "IX" in self.sub.getType():
                    mod -= 1
                if damRoll <= 1:
                    damage = 2
                else:
                    damage = 1
                print("Hit!", ship[target].name, "takes", damage, "damage!")
                ship[target].takeDamage(damage)
            else:
                print("Deck gun missed!")
            self.sub.deck_gun_ammo -= 1

        self.firedDeckGun = True
        if ship[target].sunk:
            print(ship[target].name, "has been sunk!")
            self.shipsSunk.append(ship[target])
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
