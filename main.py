# Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os
import time
from operator import *
from ship import *
from submarine import *
from util import *

#TODO:
#Deal with patrol aborts
#high score recording
#better end of game causes for high score reporting (reason for sinking,enemy, weapon etc)
#reroll for boats not allowed in med
#additional round of combat roll
#need to continiously roll for encounters, if an encounter is rolled for the mission location... is ship a possiblity?
#captain Knight's Cross checks and awards - checking for awards and giving them
#wolfpacks
#random events
#scuttle roll
#crew injury rolls
#add final subs (VIID and VIIC Flak)
#request new uboat (reassignment rulebook 11.4) if, at the end of a patrol, player receives knights cross or variants
#resupply at sea (rulebook 14.9)
#did not reload after second attack?
#hydrophones damage?
#medic sw or kia rolls for crew members hurt each patrol movement
#forward and aft salvo targeting different targets
#test dive depth on subsequent rounds for a surface-attack

#BUGS SEEN-
#ABORT PATROL ACTING FUNNY

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
        self.monthsSinceLastPromotionCheck = 0     #how many months since last promotion roll
        self.shipsSunkSinceLastPromotionCheck= 0
        self.knightsCrossSinceLastPromotionCheck = 0
        self.unsuccessfulPatrolsSinceLastPromotionCheck = 0
        self.capitalShipsSunkSinceLastKnightsCross = 0
        self.monthOfLastKnightsCrossAward = -1
        self.yearOfLastKnightsCrossAward = -1
        self.sub.subSupplyPrintout()
        self.currentOrders = ""
        self.patrolCount = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
                            "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
                            "seventeenth", "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second",
                            "twenty-third", "twenty-fourth"]
        self.patrolNum = 1
        self.sunkOnCurrentPatrol = 0
        self.successfulPatrols = 0
        self.unsuccessfulPatrols = 0
        self.unsuccessfulPatrolsInARow = 0
        self.lastPatrolWasUnsuccessful = False
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

    def getOfficerRank(self):
        return self.rank[self.sub.crew_levels["Kommandant"]]

    def advanceTime(self, months, wasAtSea = True):
        """Moves time forward - if was at sea is false, it passes the months one at a time to check for promotion"""

        if wasAtSea:
            self.date_month = self.date_month + months
            self.monthsSinceLastPromotionCheck = self.monthsSinceLastPromotionCheck + months
            self.promotionCheck()
        else:
            #move forward x months, one at a time
            for x in range (months):
                self.date_month = self.date_month + 1
                self.monthsSinceLastPromotionCheck = self.monthsSinceLastPromotionCheck + 1
                self.promotionCheck()

        #reset month to be within 0-11
        if self.date_month > 11:
            self.date_month = self.date_month - 12
            self.date_year += 1
        if (self.month[self.date_month] == "July") and self.date_year == 1940:
            self.francePost = True

    def promotionCheck(self):
        # check if up for promotion
        if self.monthsSinceLastPromotionCheck >= 12:
            promotionRoll = d6Roll()
            promoMods = 0
            if self.knightsCrossSinceLastPromotionCheck >= 1:
                promoMods -= 1
            promoMods -= self.shipsSunkSinceLastPromotionCheck // 10
            promoMods += self.unsuccessfulPatrolsSinceLastPromotionCheck

            print("You're up for a possible promotion.")
            printRollandMods(promotionRoll, promoMods)

            if promotionRoll + promoMods <= 4:
                self.sub.crew_levels["Kommandant"] += 1
                print("You've been promoted! Congratulations, " + self.getOfficerRank())
            else:
                print("You have been passed over this time around for a promotion. Sorry, ",
                      + self.getOfficerRank())

            # reset counts from last promotion check
            self.monthsSinceLastPromotionCheck = 0
            self.shipsSunkSinceLastPromotionCheck = 0
            self.unsuccessfulPatrolsSinceLastPromotionCheck = 0
            self.knightsCrossSinceLastPromotionCheck = 0

    def establishFirstRank(self):
        """Determines starting rank of player"""
        if self.sub.getType() == "IXA" or self.sub.getType() == "IXB":
            self.sub.crew_levels["Kommandant"] = 1
        else:
            roll = d6Roll()
            print("Rolling for starting rank. Roll is: ", roll)
            match self.date_year:
                case 1939:
                    self.sub.crew_levels["Kommandant"] = 1
                case 1940:
                    if roll >= 3:
                        self.sub.crew_levels["Kommandant"] = 1
                    else:
                        self.sub.crew_levels["Kommandant"] = 0
                case 1941:
                    if roll >= 4:
                        self.sub.crew_levels["Kommandant"] = 1
                    else:
                        self.sub.crew_levels["Kommandant"] = 0
                case 1942 | 1943:
                    if roll >= 6:
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
        print("---------------")
        print("Guten Tag,", self.getOfficerRank(), "- The date is", self.getFullDate())

        #get next patrol orders
        if self.sub.crew_levels["Kommandant"] > 0:
            print("PATROL ASSIGNMENT: Roll to choose next patrol?")
            if verifyYorN() == "Y":
                roll = d6Roll()
                print("Die roll:", roll)
                #check to see if player can select orders
                if roll <= self.sub.crew_levels["Kommandant"]:
                    print("You may select your patrol.")
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), True)
                else:
                    self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)
        else:
            self.getPatrol(self.getMonth(), self.getYear(), d6Roll(), self.sub.getType(), False)

        print("Patrol Assignment:", self.currentOrders)
        time.sleep(2)
        depart = "U-" + str(self.id) + " departs port early before dawn for " + self.getOfficerRank() + " " + self.kmdt + "'s " + str(self.patrolCount[self.patrolNum] + " patrol.")
        print(depart)
        self.currentLocationStep = 1
        self.patrolLength = self.getPatrolLength(self.currentOrders)
        time.sleep(3)

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
                #get unique list of orders, then print them and ask for input
                uniqueOrders = []
                for x in lines:
                    x = x.rstrip('\r\n')
                    if x not in uniqueOrders:
                        uniqueOrders.append(x)
                for x in range(len(uniqueOrders)):
                    if x == len(uniqueOrders):
                        print(uniqueOrders[x])
                    else:
                        print(uniqueOrders[x], end=", ")

                inp = "None"
                while inp not in uniqueOrders:
                    inp = input("Pick your orders (Case-sensitive): ")
                orders = inp
            else:
                orders = lines[roll - 2]

        # strip any stray returns that may have gotten into the orders string
        orders = orders.strip('\n')

        orders = self.validatePatrol(orders)

        # change time on station (onStationSteps) by one less if North American Orders
        if orders == "North America" or orders == "Caribbean":
            self.onStationSteps = self.sub.patrol_length - 1
        elif "Minelaying" in orders or "Abwehr" in orders:
            self.onStationSteps = self.sub.patrol_length - 1
        else:
            self.onStationSteps = self.sub.patrol_length

        self.currentOrders = orders

    def validatePatrol(self, orders):
        """Deal with changes in orders based on U-Boat type"""
        if orders == "Mediterranean" or orders == "Artic" and ("IX" in self.sub.getType()): #IX cannot patrol Artic or Med
            orders = "West African Coast"
        if (orders == "West African Coast" or orders == "Caribbean") and ("VII" in self.sub.getType()):  # VII Cannot patrol west africa
            orders = "Atlantic"
        if orders == "British Isles" and self.sub.getType() == "VIID":
            orders = "British Isles (Minelaying)"

        # deal with permanent stations
        if self.permMedPost:
            orders = "Mediterranean"
        if self.permArcPost:
            orders = "Arctic"

        #change loadout of boat by adding mines
        if "Minelaying" in orders:
            self.sub.forward_G7a = 0
            self.sub.forward_G7e = 0
            self.sub.aft_G7a = 0
            self.sub.aft_G7e = 0
            self.sub.minesLoadedForward = True
            self.sub.minesLoadedAft = True

        if "Abwehr" in orders:
            self.sub.crew_health["Abwehr Agent"] = 0

        return orders
        ##TODO: deal with VIID and VIIC Flak boats not being allowed in med (reroll req)

    def portReturn(self):
        """Called after patrol to deal with notification, print out sunk ships so far, and then deal with repair and rearm."""
        # TODO messages based on repair (safely returns, returns with minor damage, limps back to port, etc?)
        print("====================================================")
        returnMessage = "U-" + self.id + " glides back into port with much fanfare."
        print(returnMessage)

        #move forward 2 months per patrol of larger boats, otherwise 1 month
        if self.sub.getType() == "IXA" or self.sub.getType() == "IXB" or self.sub.getType() == "VIID":
            self.advanceTime(2)
        else:
            self.advanceTime(1)

        #refit and advance time based on damage
        refitTime = self.sub.refit()
        self.advanceTime(refitTime)

        #ensure no abwehr agent is aboard
        self.sub.crew_health["Abwehr Agent"] = -1

        #TODO determine mission sucessful ABWEHR
        if self.sunkOnCurrentPatrol > 0:
            print("Well done. We've had another successful patrol.")
            self.successfulPatrols += 1
            self.unsuccessfulPatrolsInARow = 0
            self.lastPatrolWasUnsuccessful = False
        else:
            self.unsuccessfulPatrols += 1
            self.lastPatrolWasUnsuccessful = True
        #reset ships sunk on current patrol
        self.shipsSunkSinceLastPromotionCheck = self.monthsSinceLastPromotionCheck + self.sunkOnCurrentPatrol
        self.sunkOnCurrentPatrol = 0

        #determine if crew rank increases
        if self.successfulPatrols >= 3:
            print("We've made 3 successful patrols! Our ", end= "")
            crewAd = d6Roll()
            match crewAd:
                case 1:
                    self.sub.crew_levels["Engineer"] = 1
                    print("Engineer has become an expert!")
                case 2:
                    self.sub.crew_levels["Doctor"] = 1
                    print("Doctor has become an expert!")
                case 3:
                    self.sub.crew_levels["Watch Officer 1"] = 1
                    print("Watch Officer 1 has become an expert!")
                case 4:
                    self.sub.crew_levels["Watch Officer 2"] = 1
                    print("Watch Officer 2 has become an expert!")
                case 5 | 6:
                    self.sub.crew_levels["Crew"] += 1
                    print("crew's experience level has increased!")
                    if self.sub.crew_levels["Crew"] > 3:
                        print("They can't gain more experience!")
                        self.sub.crew_levels["Crew"] = 3
            self.successfulPatrols = 0

        #Report of total ships and tonnage sunk to date
        #determine if 3 unsuccessful patrols were made in a row
        if self.lastPatrolWasUnsuccessful:
            self.unsuccessfulPatrolsInARow += 1
            if self.unsuccessfulPatrolsInARow == 3:
                self.sub.crew_levels["Crew"] = self.sub.crew_levels["Crew"] - 1
                if self.sub.crew_levels["Crew"] < 0:
                    self.sub.crew_levels["Crew"] = 0

        self.knightsCrossCheck()

        totalTonnage = 0
        for x in range(len(self.shipsSunk)):
            totalTonnage = totalTonnage + self.shipsSunk[x].GRT
        totalTonnage = f"{totalTonnage:,}"
        print("You've made", str(self.patrolNum), "patrols and sunk", str(len(self.shipsSunk)), "ships totaling", totalTonnage, "tons.")
        # for x in range(len(self.shipsSunk)):
        #     if x+1 != len(self.shipsSunk):
        #         print(self.shipsSunk[x], end=", ")
        #     else:
        #         print(self.shipsSunk[x])
        if self.sub.knightsCross > 0:
            print("Awards: ", end="")
            print(self.awardName[self.sub.knightsCross])

        self.patrolNum += 1
        time.sleep(7)

        #rearm boat
        self.sub.torpedoResupply()

    def knightsCrossCheck(self):
        """Checks if the conditions for the NEXT knight's cross award is applicable, and awards it"""

        #get total GRT Sunk
        totalTonnageSunk = 0
        for x in range (len(self.shipsSunk)):
            totalTonnageSunk += self.shipsSunk[x].GRT
        #get GRT of ships sunk since last knight's cross award
        if self.sub.knightsCross > 0:
            GRTSunkSinceLastKnightsCross = 0
            for x in range (len(self.shipsSunk)):
                if self.shipsSunk[x].yearSunk > self.yearOfLastKnightsCrossAward:
                    GRTSunkSinceLastKnightsCross += self.shipsSunk[x].GRT
                elif self.shipsSunk[x].yearSunk == self.yearOfLastKnightsCrossAward and self.shipsSunk[x].monthSunk >= self.monthOfLastKnightsCrossAward:
                    GRTSunkSinceLastKnightsCross += self.shipsSunk[x].GRT


        # if KMDT has no knights cross awards, check for awarding of Knight's Cross
        # (100k tons, or sunk capital ship)
        # no +1 die roll when firing second salvo from aft tubes during night surface attack
        if self.sub.knightsCross == 0:
            if totalTonnageSunk > 100000 or self.capitalShipsSunkSinceLastKnightsCross > 0:
                print("You've been awarded the Knight's Cross! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 1
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
                #TODO IF AWARDED ANY KC, CAN REQUEST REASSIGNMENT
        # if KMDT has Knight's Cross, check for awarding of for Knight's Cross Oakleaves KCO
        # (175k tons, or sunk capital ship / 75k tons since last promo)
        # in addition to above bonus, favorable -1 roll mod when firing (to hit)
        elif self.sub.knightsCross == 1:
            if totalTonnageSunk > 175000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 75000:
                print("You've been awarded the Knight's Cross! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 2
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
        # if KMDT has Knight's Cross Oakleaves, check for awarding of for Knight's Cross Oakleaves and Swords KCO&S
        # (250k tons, or sunk capital ship / 75k tons since last promo)
        # in addition to above bonuses, favorable -1 roll mod for escort detection
        elif self.sub.knightsCross == 2:
            if totalTonnageSunk > 200000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 75000:
                print("You've been awarded the Knight's Cross! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 3
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
        # if KMDT has Knight's Cross Oakleaves and Swords, check for awarding of for Knight's Cross Oakleaves, Swords, and Diamonds KCOS&D
        # (300k tons, or sunk capital ship / 50k tons since last promo)
        # in addition to above bonuses, following attempts are always successful
        elif self.sub.knightsCross == 3:
            if totalTonnageSunk > 300000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 50000:
                print("You've been awarded the Knight's Cross! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 4
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()

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
        gameover()

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
            self.printPatrolStatus(currentBox)

            if self.sub.dieselsInop() == 2:
                if self.currentLocationStep == self.patrolLength - 1:
                    print("We are towed back to port.")
                else:
                    print("Both Diesel engines are knocked out. We must scuttle the boat!")
                    #TODO SCUTTLE ROLL
                    gameover("Scuttled due to engines being knocked out.")
            elif self.sub.dieselsInop() == 1:
                print("We must abort the patrol, one our diesel engines are damaged beyond repair.")
                self.abortPatrol()

            #skip first iteration of asking for action (on departure)- otherwise ask for next action before making roll
            if self.currentLocationStep == 1:
                invalid = False
            else:
                invalid = True
            while invalid:
                action = verifyNextAction()
                match action:
                    case "Continue":
                        invalid = False
                    case "Stores":
                        self.sub.subSupplyPrintout()
                    case "Damage":
                        self.sub.printStatus()
                    case "Abort":
                        print("Aborting patrol.")
                        self.abortPatrol()
                        currentBox = "Transit"
                        invalid = False

            # if sub is patrolling area (not in transit)
            if currentBox == self.currentOrders:
                self.onStationSteps -= 1
            self.getEncounter(currentBox, self.getYear(), self.randomEvent)
            #roll second time for 1 inop... 2 rolls for encounter when aborting and 1 diesel engine knocked out
            if self.sub.dieselsInop() == 1:
                self.getEncounter(currentBox, self.getYear(), self.randomEvent)

            # end of loop - go to next box of patrol
            self.currentLocationStep += 1

        # if it was a Med patrol, set U boat permanently to Med
        if self.currentOrders == "Mediterranean":
            self.permMedPost = True

    def abortPatrol(self):
        """Aborts current patrol, setting the player's current location to the end of the patrol less one- so two
        transits take place before arrive back."""
        self.currentLocationStep = self.getPatrolLength(self.currentOrders) - 1
        self.onStationSteps = 0

    def drawPatrolMeter(self):
        numDashes = self.getPatrolLength(self.currentOrders)
        print("<", end = "")
        for x in range (numDashes):
            if x == self.currentLocationStep - 1:
                print(" 0 ", end = "")
            else:
                print(" - ", end = "")
        print(">")

    def printPatrolStatus(self, currentBox):
        self.drawPatrolMeter()
        print("Current Box:", currentBox)

    #--------------------------------------------- Patrol checks and encounter checks

    def getLocation(self, patrol, step):
        """Gets current location box on a patrol to determine encounter type (transit, Atlantic, etc)"""
        # TODO wolfpacks?
        #if minelaying patrol is beyond mission square, change orders to just regular british isles
        if self.onStationSteps < self.sub.patrol_length and "Minelaying" in self.currentOrders:
            patrol = patrol.replace("(Minelaying)", "")
        #if abwehr patrol is beyond mission square, change orders to just regular NA or British Isles patrol
        if self.onStationSteps < self.sub.patrol_length and "Abwehr" in self.currentOrders:
            patrol = patrol.replace("(Abwehr Agent Delivery)", "")

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
                    if "Minelaying" in self.currentOrders:
                        return "Mission"
                    elif "Abwehr" in self.currentOrders and "British Isles" in self.currentOrders:
                        return "Mission"
                    else:
                        return patrol
            case 4:
                if patrol == "North America" or patrol == "Caribbean":
                    return "Transit"
                else:
                    return patrol
            case 5:
                if "Abwehr" in self.currentOrders and "North America" in self.currentOrders:
                    return "Mission"
                else:
                    return patrol
            case 6:
                if self.onStationSteps == 0:
                    if self.currentLocationStep == self.patrolLength - 1:
                        return "Transit"
                    elif self.currentLocationStep == self.patrolLength:
                        if self.permArcPost or self.francePost:
                            return "Bay of Biscay"
                        else:
                            return "Transit"
                    elif patrol == "Mediterranean" or patrol == "Arctic":
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
                        else:
                            return "Transit"
                    elif patrol == "Mediterranean" or patrol == "Arctic":
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
                        else:
                            return "Transit"
                    elif patrol == "Mediterranean" or patrol == "Arctic":
                        return "Transit"
                    else:
                        print("ERROR getting loc")
                else:
                    return patrol

    def getEncounter(self, loc, year, randomEvent):
        """Determines which location encounter chart to use, then rolls against and returns the string encounter name"""
        roll = d6Rollx2()
        print("Roll for location:", loc, "-", roll)

        # First check if random event (natural 12)
        if roll == 12 and randomEvent == False and loc != "Additional Round of Combat":
            print("Random Event! TODO")
            return "Random Event"

        # determine if this is a mission box to roll against mission
        if (loc == "British Isles (Minelaying)" or loc == "British Isles (Abwehr Agent Delivery)") and self.currentLocationStep == 3:
            loc = "Mission"
        #elif loc == "British Isles (Minelaying)" and self.currentLocationStep WORK OUT IF AT PATROL LOC TO CHANGE TO BRITISH ISLES
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
                elif year == 1943:
                    roll = roll - 2
                if loc == "Gibraltar Passage":
                    roll = roll - 2
                match roll:
                    case -2, -1, 0, 1, 2, 3:
                        print("Enemy escort has arrived!")
                        self.escortDetection("", 7, "Submerged", "Day", True, 0, 0)
                    case 4 | 5:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Bay of Biscay" | "Mission":
                if year == 1942 and loc == "Bay of Biscay":
                    roll = roll - 1
                elif year == 1943 and loc == "Bay of Biscay":
                    roll = roll - 2
                if loc == "Mission":
                    roll -= 1
                match roll:
                    case -2 | -1 | 0 | 1 | 2 | 3 | 4:
                        # aircraft
                        self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
                #check to see if minelaying was success
                if loc == "Mission" and "Minelaying" in self.currentOrders:
                    self.sub.minesLoadedForward = False
                    self.sub.minesLoadedAft = False
                    if self.sub.systems["Forward Torpedo Doors"] >= 1:
                        print("Unable to deploy forward mines.")
                        self.sub.minesLoadedForward = True
                    elif self.sub.systems["Aft Torpedo Doors"] >= 1:
                        print("Unable to deploy aft mines.")
                        self.sub.minesLoadedAft = True
                    else:
                        print("Successfully deployed mines. Mission complete. Continuing patrol.")
                        self.sunkOnCurrentPatrol += 1
                    self.sub.reload()
                #check to see if abwehr agent mission was success
                if loc == "Mission" and "Abwehr" in self.currentOrders:
                    self.sub.crew_health["Abwehr Agent"] = -1
                    self.sunkOnCurrentPatrol += 1



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
                if "Minelaying" in self.currentOrders:
                    print("Approaching designated mine area.")
                elif "Abwehr" in self.currentOrders:
                    print("Approaching the shore to land our agent.")
                else:
                    print("Error getting mission")
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
                # TODO - needed?
                print("TODO")
        time.sleep(3)

    def encounterAircraft(self, sub, year, patrolType):
        """When 'Aircraft' is rolled on a given encounter chart"""
        print("ALARM! Aircraft in sight! Rolling to crash dive!")
        time.sleep(2)
        roll = d6Rollx2()
        drm = 0

        if sub.crew_levels["Crew"] == 0:
            drm -= 1
        elif sub.crew_levels["Crew"] == 3:
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
        if (patrolType == "British Isles (Minelaying)" or patrolType == "British Isles (Abwehr Agent Delivery)") and self.currentLocationStep == 3:
            drm -= 1
        if patrolType == "North America (Abwehr Agent Delivery)" and self.currentLocationStep == 5:
            drm -= 1

        print("Roll for crash dive!")
        a1AircraftEncounterRoll = roll + drm
        printRollandMods(roll, drm)

        aircraft = "Undamaged"
        if a1AircraftEncounterRoll <= 5:
            print("The aircraft caught us by surprise!")
            time.sleep(3)
            #sub fires first
            if self.sub.systems["Flak Gun"] == 0:
                flakRoll = d6Roll()
                flakMods = 0
                if self.sub.getType() == "VIIA":
                    flakMods += 1
                if self.sub.systems["3.7 Flak"] == 0:
                    flakMods -= 1
                if self.sub.crew_levels["Crew"] >= 2:
                    flakMods -= 1
                if self.sub.getType() == "VIIC Flak":
                    flakMods -= 2
                if flakRoll + flakMods <= 3:
                    print("We shot down aircraft!")
                    self.sub.crewInjury()
                    self.sub.attacked("Surfaced", 0, self.getYear(), True)
                    aircraft = "Destroyed"
                else:
                    print("We've managed to damage the aircraft!")
                    self.sub.crewInjury()
                    self.sub.attacked("Surfaced", 0, self.getYear(), True)
                    if a1AircraftEncounterRoll <= 1:
                        self.sub.attacked("Surfaced", 0, self.getYear(), True)
                    if flakRoll + flakMods <= 5:
                        aircraft = "Damaged"
        else:
            print("Successful crash dive!")

        #roll for another possible encounter if crash dive was not successful and aircraft was not shot down
        if aircraft == "Damaged" or aircraft == "Undamaged" and a1AircraftEncounterRoll <= 5:
            self.getEncounter("Additional Round of Combat", self.getYear(), self.randomEvent)

        if a1AircraftEncounterRoll <= 5:
            self.sub.repair()

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

        #remove ability to attack escorted targets if carrying mines
        if (self.sub.minesLoadedForward or self.sub.minesLoadedAft) and ship[0].type == "Escort":
            return "exit"

        print("Do you wish to attack?")
        if verifyYorN() == "N":
            # break out of encounter
            return "exit"

        lostthem = self.attackRound(enc, ship)

        #allow for more rounds of combat
        #get number of ships sunk and damaged out of entire encounter
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
                #count sunken capital ships (over 22k GRT) as they count towards getting KC awards
                if ship[x].type == "Capital Ship" and ship[x].GRT > 22000:
                    print("We've sunk a major warship!")
                    self.capitalShipsSunkSinceLastKnightsCross += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        self.sub.repair()
        self.sub.reload()
        self.G7aFired = 0
        self.G7eFired = 0
        #check if lost contact from changing from night to day
        if lostthem == "Lost Them":
            print("We lost them!")
        #check if all ships aside from escorts have been sunk (end of combat)
        elif (shipsSunk == len(ship) - 1 and ship[0].type == "Escort") or shipsSunk == len(ship):
            if enc == "Convoy":
                print("Attempt to follow convoy?")
                if verifyYorN() == "Y":
                    followRoll = d6Roll()
                    if followRoll <= 4 or self.sub.knightsCross == 4:
                        self.encounterAttack("Convoy")
                    else:
                        print("We lost contact with the convoy!")
            else:
                print("We sunk all targets!")
        else:   #for when any target ships (not escorts) are still afloat
            #decide whether to follow or not
            print("Follow target(s) to make another attack?")
            if verifyYorN() == "Y":
                #deal with convoys
                if enc == "Convoy":
                    if shipsDamaged > 0:
                        inpInvalid = True
                        while inpInvalid:
                            followPrompt = input("Follow damaged ship(s) or the convoy?\n1) Damaged Ships\n2) Convoy")
                            if followPrompt == "1" or followPrompt == "2":
                                inpInvalid = False
                    else:
                        followPrompt = "2"

                    match followPrompt:
                        #Following damaged ship(s) - remove undamaged ships, automatic follow, see if it was escorted
                        case "1":
                            self.followFlow(ship)
                        #following convoy, roll to follow etc
                        case "2":
                            followRoll = d6Roll()
                            if followRoll <= 4 or self.sub.knightsCross == 4:
                                self.encounterAttack("Convoy")
                            else:
                                print("We lost contact with the convoy!")
                #if encounter is capital ship - allow for following ONLY if the capital ship was damaged
                elif enc == "Capital Ship":
                    if ship[1].damage > 0:
                        self.encounterAttack("Capital Ship", ship)
                    else:
                        print("Unable to follow the", ship[1].name)
                #all other encounter types NOT convoys and capital ships
                else:
                    #for 2+ damaged ships
                    if shipsDamaged >= 2:
                        if shipsDamaged == len(ship) - 1 and Escorted(ship):
                            #all ships aside from the escort are damaged. Find out which to follow
                            self.followFlow(ship)
                        elif shipsDamaged == len(ship) and not Escorted(ship):
                            #all ships are damaged. Find out which to follow
                            self.followFlow(ship)
                        else:
                            #some are damaged and some are not, figure out if following damaged or undamaged
                            inpInvalid = True
                            while inpInvalid:
                                followPrompt = input("Follow damaged ship(s) or the rest?\n1) Damaged Ship(s)\n2) Undamaged Ship(s)")
                                if followPrompt == "1" or followPrompt == "2":
                                    inpInvalid = False
                            if followPrompt == "1":
                                print("Following damaged ship(s).")
                                #remove undamaged ships
                                for x in range (len(ship)):
                                    if ship[x].type != "Escort" and ship[x].damage == 0:
                                        ship.remove(ship[x])
                                self.followFlow(ship)
                            else:
                                print("Attempting to follow undamaged ship(s)")
                                followRoll = d6Roll()
                                if followRoll <= 4 or self.sub.knightsCross == 4:
                                    # remove damaged ships
                                    for x in range(len(ship)):
                                        if ship[x].type != "Escort" and ship[x].damage > 0:
                                            ship.remove(ship[x])
                                    self.encounterAttack(enc, ship)
                                else:
                                    print("Unable to follow the contact!")
                    #one damaged ship
                    else:
                        if Escorted(ship):
                            followRoll = d6Roll()
                            if followRoll <= 4 or self.sub.knightsCross == 4:
                                self.encounterAttack(enc, ship)
                            else:
                                print("Unable to follow the contact!")
                        else:   #this else catches all unescorted encounters
                            #first check on Addl round of combat chart to see if an escort shows up
                            if self.getEncounter("Additional Round of Combat", self.getYear(), self.randomEvent) == "Escort":
                                newShip = []
                                newShip.append(Ship("Escort"))
                                newShip.append(ship[0])
                                if ship[1] is not None:
                                    newShip.append(ship[1])
                                self.escortDetection(enc, 7, "Submerged", "Day", False, self.G7aFired, self.G7eFired)
                                self.encounterAttack("Ship + Escort", newShip)
                            else:
                                print("Closing to attack again!")
                                self.encounterAttack(enc, ship)

        time.sleep(3)

    def followFlow(self, ship):
        """Prompts and displays for following damaged ship(s) --- ONLY damaged ships, aka automatic follow"""
        # determine if escorted
        escortedRoll = d6Roll()
        if escortedRoll <= 4:
            ship[0].damage = 1
        # remove undamaged ships by adding to new ship list then subbing it
        newShip = []
        for s in range(len(ship)):
            if ship[s].damage > 0 and (ship[s].damage < ship[s].hp):
                print("Adding ship to follow: ", str(ship[s]), " | DAMAGE:", str(ship[s].damage))  #DEBUG
                newShip.append(ship[s])
        ship = newShip
        if escortedRoll <= 4:
            ship[0].damage = 0
        # determine type of encounter and start it
        if not Escorted(ship) and (len(ship) == 1):  # 1 ship only
            self.encounterAttack("Ship", ship)
        elif Escorted(ship) and (len(ship) == 2):  # 1 ship and escort
            self.encounterAttack("Ship + Escort", ship)
        elif len(ship) > 1:  # otherwise more than 1 ship damaged
            print("Select ship to follow:")
            for x in range(len(ship)):
                if ship[x].type == "Escort":
                    continue
                toPrint = (str(x) + ") " + str(ship[x]))
                print(toPrint)
            invalid = True
            while invalid:
                b = int(input())
                if b <= 0 or b > len(ship):
                    continue
                else:
                    invalid = False
            newShip2 = []
            if Escorted(ship):
                newShip2.append(ship[0])
            newShip2.append(ship[b])
            if Escorted(ship):
                self.encounterAttack("Ship + Escort", newShip2)
            else:
                self.encounterAttack("Ship", newShip2)
        else:
            print("Error following damaged ship(s)")

    def getShips(self, enc):
        """Creates and returns a list of ship object(s) for a given encounter."""
        tgt = []
        if enc == "Convoy" or enc == "Capital Ship" or "Escort" in enc:
            tgt.append(Ship("Escort", self.shipsSunk, self.getMonth(), self.getYear()))

        if enc == "Tanker":
            tgt.append(Ship("Tanker", self.shipsSunk, self.getMonth(), self.getYear()))

        if enc == "Capital Ship":
            tgt.append(Ship("Capital Ship", self.shipsSunk, self.getMonth(), self.getYear()))

        if enc == "Ship" or enc == "Two Ships" or enc == "Convoy" or enc == "Ship + Escort" or enc == "Two Ships + Escort":
            tgt.append(Ship(self.getTargetShipType(), self.shipsSunk, self.getMonth(), self.getYear()))

        if "Two Ships" in enc or enc == "Convoy":
            tgt.append(Ship(self.getTargetShipType(), self.shipsSunk, self.getMonth(), self.getYear()))

        if enc == "Convoy":
            tgt.append(Ship(self.getTargetShipType(), self.shipsSunk, self.getMonth(), self.getYear()))
            tgt.append(Ship(self.getTargetShipType(), self.shipsSunk, self.getMonth(), self.getYear()))

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
            escortMods -= 2
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
            return "Escaped"
        if escortRoll + escortMods <= 8:
            print("We've evaded detection!")
            self.sub.printStatus()
            time.sleep(2)
            return "Escaped"
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

    def getTimeOfDay(self, isFollowing):
        """Returns string of time of day (Day or Night) based on current orders and die roll"""
        #first deal with actic always day or always night months if applicable
        if self.currentOrders == "Arctic" and (self.date_month == 5 or self.date_month == 11):
            if self.date_month == 5:
                return "Day"
            elif self.date_month == 11:
                return "Night"
            else:
                print("Error with arctic day night")
        #otherwise, if following, choose day or night to attack
        elif isFollowing:
            print("Attack during day or night?")
            print("1) Day")
            print("2) Night")
            choice = input()
            match choice:
                case "1" | "Day" | "day":
                    return "Day"
                case "2" | "Night" | "night":
                    return "Night"
        #otherwise randomly determine day or night
        else:
            timeRoll = d6Roll()
            #deal with arctic times
            if self.currentOrders == "Artic":
                match self.date_month:
                    case 0 | 1 | 2 | 9 | 10:
                        if timeRoll <= 2:
                            return "Day"
                        else:
                            return "Night"
                    case 3 | 4 | 6 | 7 | 8:
                        if timeRoll <= 4:
                            return "Day"
                        else:
                            return "Night"
                    case 5:
                        return "Day"
                    case 11:
                        return "Night"
            #non-arctic day/night 50/50 roll
            else:
                if timeRoll <= 3:
                    return "Day"
                else:
                    return "Night"

    def getAttackType(self, ship, depth, timeOfDay, r):
        """Gets a valid attack type and calls the method relavant to the attack selected. Exits method if no valid attack"""
        #determine valid attack options first
        #bow
        if self.sub.systems["Forward Torpedo Doors"] == 0 and (
                self.sub.forward_G7a > 0 or self.sub.forward_G7e > 0) and self.firedForward == False and self.sub.minesLoadedForward == False:
            bowSalvoAvail = True
        else:
            bowSalvoAvail = False
        #aft
        if self.sub.systems["Aft Torpedo Doors"] == 0 and (self.sub.aft_G7a > 0 or self.sub.aft_G7e > 0) and self.firedAft == False and self.sub.minesLoadedAft == False:
            aftSalvoAvail = True
        else:
            aftSalvoAvail = False
        #bow and aft salvo
        if bowSalvoAvail and aftSalvoAvail and timeOfDay == "Night" and depth == "Surfaced":
            secondSalvoAvail = True
        else:
            secondSalvoAvail = False
        #deck gun
        if self.sub.deck_gun_ammo > 0 and depth == "Surfaced" and ship[0].type != "Escort" and self.firedDeckGun == False and self.sub.systems["Deck Gun"] == 0:
            deckGunAvail = True
        else:
            deckGunAvail = False

        #TODO check attack availabilty first, then print options0
        if bowSalvoAvail == False and aftSalvoAvail == False and deckGunAvail == False:
            return "exitAttack"

        print("How should we attack?")
        if bowSalvoAvail:
            print("1) Bow Torpedo Salvo")
        else:
            print("1) -UNAVAILABLE- Bow Torpedo Salvo ")
        if aftSalvoAvail:
            print("2) Aft Torpedo Salvo")
        else:
            print("2) -UNAVAILABLE- Aft Torpedo Salvo")
        if secondSalvoAvail:
            print("3) Forward & Aft Torpedo Salvo")
        else:
            print("3) -UNAVAILABLE- Forward & Aft Torpedo Salvo")
        if deckGunAvail:
            print("4) Engage with Deck Gun")
        else:
            print("4) -UNAVAILABLE- Engage with Deck Gun")

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
        """An attack round that consists of firing all AVAILABLE weapons a max of 1 time (on unescorted ships)"""
        timeOfDay = self.getTimeOfDay(isFollowing)

        print("Current time:", timeOfDay)

        # ask to flip to day or night
        if timeOfDay == "Night":
            print("Do you wish to continue the attack at night?")
        else:
            print("Do you wish to continue the attack during the day?")
        if self.sub.systems["Periscope"] >= 1:
            print("Reminder, Captain, that our periscope is knocked out and we cannot attack submerged.")
        if verifyYorN() == "N":
            fliproll = d6Roll()
            if fliproll >= 5:
                return "Lost Them"
            else:
                print("We successfully followed them.")
                if timeOfDay == "Night":
                    timeOfDay = "Day"
                else:
                    timeOfDay = "Night"

        #call off attack if periscope is damaged and day, because submerged attacks cannot be made
        if self.sub.systems["Periscope"] >= 1 and timeOfDay == "Day":
            print("Unable to attack with periscope damaged and escort nearby. Submerging to escape.")
            return

        # choosing depth
        if Escorted(ship) and timeOfDay == "Day":
            print("Periscope Depth!")
            depth = "Submerged"
        elif Escorted(ship) and self.sub.systems["Periscope"] >= 1:
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
        if Escorted(ship):
            r = input("Choose Range:\n1) -WARNING ESCORT- Close\n2) Medium Range\n3) Long Range")
        else:
            r = input("Choose Range:\n1) Close\n2) Medium Range\n3) Long Range")
        detectedOnClose = False
        match r:
            case "1" | "Close":
                r = 8  # must hit on 8 or less
                if Escorted(ship):
                    print("Approaching the targets... hopefully we are not detected.")
                    detectionRoll = d6Rollx2()
                    detectionMods = 0
                    time.sleep(2)
                    if self.getYear() >= 1941:
                        detectionMods = detectionMods + (self.getYear() - 1940)
                    if self.sub.knightsCross >= 3:
                        detectionMods -= 1

                    printRollandMods(detectionRoll, detectionMods)
                    time.sleep(2)
                    if detectionRoll + detectionMods >= 12:
                        print("Detected! Big Problems!")
                        self.sub.attacked("Submerged", 1, self.getYear())
                        time.sleep(3)
                        self.escortDetection(enc, 8, depth, timeOfDay, True, 0, 0)
                        detectedOnClose = True
                    elif detectionRoll + detectionMods >= 10:
                        print("They've detected us before we could attack!")
                        self.sub.attacked("Submerged", 0, self.getYear())
                        time.sleep(3)
                        self.escortDetection(enc, 8, depth, timeOfDay, True, 0, 0)
                        detectedOnClose = True
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
        if not detectedOnClose:
            self.sub.subSupplyPrintout()
            self.getAttackType(ship, depth, timeOfDay, r)

        # post shot escort detection
        if Escorted(ship) and not detectedOnClose:
            print("Escort incoming on our position!")
            time.sleep(2)
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
        if not Escorted(ship) and shipsSunk != len(ship):
            print("Should we make another attack?")
            if verifyYorN() == "Y":
                self.getAttackType(ship, depth, timeOfDay, r)

        #recheck for sunk / damaged ships
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check third (final) time for attack in same round on unescorted targets
        if not Escorted(ship) and shipsSunk != len(ship):
            print("Should we make another attack?")
            if verifyYorN() == "Y":
                self.getAttackType(ship, depth, timeOfDay, r)



    def getTarget(self, ship):
        """Validates input on ships to target. Only accepts a # from 0-# of ships, disallows firing at escorts. A 0 would
        indicate finished firing."""
        notValid = True
        while notValid:
            if len(ship) == 2 and ship[0].type == "Escort":  #assume target is only valid target
                target = 2
            if len(ship) > 1:
                target = int(input("Enter ship # from above to target. Enter 0 if done attacking."))
            else:
                target = 1   # only 1 target, so just choose that ship only
            #TODO work out whether the target was already fired at so we don't ask player again to fire at it

            if target < 0 or target > len(ship):  #if out of bounds (less than 0 and greater than # ships
                continue
            elif target == 1 and ship[0].type == "Escort":  # disallow firing at escort
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

        notFiredAtAllShips = True
        # validation loop to get a target, then # of torps to fire at it, then get next target if torpedoes are available
        while self.sub.getTotalInTubes(foreOrAft) != 0 and notFiredAtAllShips:
            target = self.getTarget(ship)
            if target == 0:
                break
            target = target - 1

            self.sub.subSupplyPrintout(foreOrAft)
            invalidFire = True
            # if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7a") > 0:
                # validation loop
                while invalidFire:
                    G7aFire = int(input("Fire how many G7a torpedoes?"))
                    if G7aFire < 0 or G7aFire > self.sub.getTotalInTubes(foreOrAft, "G7a"):
                        continue
                    else:
                        invalidFire = False
                ship[target].fireG7a(G7aFire)
                for x in range(G7aFire):
                    self.sub.fireTorpedo(foreOrAft, "G7a")
                    self.G7aFired += 1
            invalidFire = True
            # if electric torpedoes are available, ask how many to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7e") > 0:
                # validation loop
                while invalidFire:
                    G7eFire = int(input("Fire how many G7e torpedoes?"))
                    if G7eFire < 0 or G7eFire > self.sub.getTotalInTubes(foreOrAft, "G7e"):
                        continue
                    else:
                        invalidFire = False
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
                invalidFire = True
                # if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
                if self.sub.getTotalInTubes("Aft", "G7a") > 0:
                    # validation loop
                    while invalidFire:
                        G7aFire = int(input("Fire how many G7a torpedoes?"))
                        if G7aFire < 0 or G7aFire > self.sub.getTotalInTubes("Aft", "G7a"):
                            continue
                        else:
                            invalidFire = False
                    ship[target].fireG7a(G7aFire)
                    for x in range(G7aFire):
                        self.sub.fireTorpedo("Aft", "G7a")
                        self.G7aFired += 1
                invalidFire = True
                if self.sub.getTotalInTubes("Aft", "G7e") > 0:
                    # validation loop
                    while invalidFire:
                        G7eFire = int(input("Fire how many G7e torpedoes?"))
                        if G7eFire < 0 or G7eFire > self.sub.getTotalInTubes("Aft", "G7e"):
                            continue
                        else:
                            invalidFire = False
                    ship[target].fireG7e(G7eFire)
                    for x in range(G7eFire):
                        self.sub.fireTorpedo("Aft", "G7e")
                        self.G7eFired += 1
                self.firedAft = True

            shipsFiredAtCount = 0
            for x in range (len(ship)):
                if ship[x].type == "Escort":
                    shipsFiredAtCount +=1
                else:
                    if ship[x].G7aINCOMING > 0 or ship[x].G7eINCOMING > 0:
                        shipsFiredAtCount += 1
            if shipsFiredAtCount == len(ship):
                notFiredAtAllShips = False


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
        """Attack called (already assumed to have at least one shot) for deck guns."""
        printTargetShipList(ship)
        self.sub.subSupplyPrintout("Deck Gun")

        target = self.getTarget(ship)

        target = target - 1

        #get how many shots to fire (1 or 2)- automatically fire 1 if only 1 shot remaining
        shots = -1
        while shots < 0 or shots > 2:
            if self.sub.deck_gun_ammo == 1:
                shots = 1
                break
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

def Escorted(ships):
    """Returns true if the list of ships passed has an escort (as its first ship)"""
    if ships[0].type == "Escort":
        return True
    else:
        return False

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

Game()
