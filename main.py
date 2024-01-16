# Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os
import time
from datetime import datetime
from operator import *
from ship import *
from submarine import *
from aircraft import *
from util import *

#TODO:
#order in which escorts on convoy duty roll (before firing torps?)
#career report when in port
#patrol report?

#BUGS SEEN----
#promotion check mods don't seem to be working?

def mainMenu():
    print("Welcome to The Hunters: German U-Boats at War, 1939-43")
    print("-Programmed by Kyle BB-")
    print("To play, please ensure you own a copy of the GMT game.")
    print("Instructions: Follow prompts- 99% of the game is simple input in the form of entering a number.")
    print("You can type a question mark (?) in any prompt instead to get a few helpful, relevant explanations.")
    time.sleep(3)
    print("===========================================")
    act = getInputNum("1) Play Game\n2) High Scores", 1, 2)
    if act == 1:
        Game()
    elif act == 2:
        printTable()


class Game():

    def __init__(self):
        self.month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        self.date_month = 0
        self.date_year = 1939
        self.rank = ["Oberleutnant zur See", "Kapitän-leutnant", "Korvetten-kapitän", "Fregatten-kapitän",
                     "Kapitän zur See"]
        self.awardName = ["", "Knight's Cross", "Knight's Cross with Oakleaves", "Knight's Cross with Oakleaves and Swords",
                          "Knight's Cross with Oakleaves, Swords and Diamonds"]
        self.monthsSinceLastPromotionCheck = 0     #how many months since last promotion roll
        self.shipsSunkSinceLastPromotionCheck= 0
        self.knightsCrossSinceLastPromotionCheck = 0
        self.unsuccessfulPatrolsSinceLastPromotionCheck = 0
        self.capitalShipsSunkSinceLastKnightsCross = 0
        self.monthOfLastKnightsCrossAward = -1
        self.yearOfLastKnightsCrossAward = -1
        self.currentOrders = ""
        self.patrolCount = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
                            "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
                            "seventeenth", "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second",
                            "twenty-third", "twenty-fourth"]
        self.patrolNum = 1
        self.missionComplete = False
        self.successfulPatrols = 0
        self.unsuccessfulPatrolsInARow = 0
        self.eligibleForNewUboat = False
        self.lastPatrolWasUnsuccessful = False
        self.randomEvent = False
        self.superiorTorpedoes = False
        self.halsUndBeinbruch = 0
        self.weatherDuty = False
        self.severeWeather = False
        self.eligibleForNewBoat = False
        self.lastPatrolWasUnsuccessful = False
        self.abortingPatrol = False
        self.permMedPost = False
        self.permArcPost = False
        self.francePost = False
        self.patrolArray = []
        self.currentBox = 0
        self.G7aFired = 0
        self.G7eFired = 0
        self.firedForward = False
        self.firedAft = False
        self.firedDeckGun = False
        self.shipsSunk = []
        self.shipsSunkOnCurrentPatrol = []
        self.damageDone = 0
        self.hitsTaken = 0
        self.randomEvents = 0
        self.pastSubs = []
        self.startGame()
        self.gameloop()

    def startGame(self):

        #get player info
        self.sub = Submarine(self.chooseSub())
        invalid = True
        while invalid:
            self.kmdt = input("Enter Kommandant name: ")
            if "_" in self.kmdt:
                print("Underscores not allowed.")
                continue
            elif len(self.kmdt) > 25:
                print("Name too long.")
                continue
            else:
                invalid = False
        self.id = getInputNum("Enter U-Boat #: ", 1, 9999)

        self.sub.torpedoResupply()
        self.establishFirstRank()
        self.sub.subSupplyPrintout(False)

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

    def getFullUboatID(self):
        """Returns string 'U-XXX'"""
        toReturn = "U-" + str(self.id)
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
        if (self.date_month >= 6 and self.date_year == 1940) or self.date_year > 1940:
            self.francePost = True

    def promotionCheck(self):
        # check if up for promotion
        finalPromotion = False
        if self.date_month >= 7 and self.date_year == 1943:
            finalPromotion = True

        #check if normal promotion or final promotion at end of game
        if self.monthsSinceLastPromotionCheck >= 12 or finalPromotion:
            if not finalPromotion:
                print("You're up for a possible promotion.")
            else:
                print("You're up for promotion to a desk job in Training Command.")

            promotionRoll = d6Roll()
            promoMods = 0
            if self.knightsCrossSinceLastPromotionCheck >= 1:
                promoMods1 = 1
            else:
                promoMods1 = 0
            promoMods2 = self.shipsSunkSinceLastPromotionCheck // 10
            promoMods3 = self.unsuccessfulPatrolsSinceLastPromotionCheck
            promoMods = promoMods1 + promoMods2 + promoMods3
            print(promoMods1, promoMods2, promoMods3)

            printRollandMods("Roll to be promoted (4-):", promotionRoll, promoMods)

            #allow player with luck to spend it for a new promotion roll
            while promotionRoll + promoMods > 4 and self.halsUndBeinbruch > 0:
                if verifyYorN("You can spend some luck to reroll the promotion roll. Spend luck? ") == "Y":
                    promotionRoll = d6Roll()
                    self.halsUndBeinbruch -= 1
                else:
                    break

            if promotionRoll + promoMods <= 4:
                self.sub.crew_levels["Kommandant"] += 1
                print("You've been promoted! Congratulations,", self.getOfficerRank())
            else:
                print("You have been passed over this time around for a promotion. Sorry,", self.getOfficerRank())

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

    def chooseSub(self, reassignment = False):
        """Gets input from player to choose Submarine Type"""

        if not reassignment:
            print("1. VIIA (Start date Sept-39)")
            print("2. VIIB (Start date Sept-39)")
            print("3. IXA  (Start date Sept-39)")
            print("4. IXB  (Start date Apr-40)")
            print("5. VIIC (Start date Oct-40)")
            print("6. VIID (Start date Jan-42)")
            subChosen = getInputNum("Choose a U-Boat: ", 1, 6)
            match subChosen:
                case 1:
                    self.date_month = 8
                    self.date_year = 1939
                    return "VIIA"
                case 2:
                    self.date_month = 8
                    self.date_year = 1939
                    return "VIIB"
                case 3:
                    self.date_month = 8
                    self.date_year = 1939
                    return "IXA"
                case 4:
                    self.date_month = 3
                    self.date_year = 1940
                    return "IXB"
                case 5:
                    self.date_month = 9
                    self.date_year = 1940
                    self.francePost = True
                    return "VIIC"
                case 6:
                    self.date_month = 0
                    self.date_year = 1942
                    self.francePost = True
                    return "VIID"
                case 7:
                    self.date_month = 4
                    self.date_year = 1943
                    self.francePost = True
                    return "VIIC Flak"
        else:
            if "IX" in self.sub.getType():
                subsavail = 1
                print("1. IXA")
                if (self.date_month > 3 and self.date_year == 1940) or self.date_year > 1940:
                    subsavail += 1
                    print("2. IXB")
                subChosen = getInputNum("Choose new U-Boat: ", 1, subsavail)
                match subChosen:
                    case 1:
                        return "IXA"
                    case 2:
                        return "IXB"
            else:
                subsavail = 2
                print("1. VIIA")
                print("2. VIIB")

                if (self.date_month > 9 and self.date_year == 1940) or self.date_year > 1940:
                    subsavail += 1
                    print("3. VIIC")
                if self.date_year >= 1942:
                    subsavail += 1
                    print("4. VIID")
                subChosen = getInputNum("Choose new U-Boat: ", 1, subsavail)
                match subChosen:
                    case 1:
                        return "VIIA"
                    case 2:
                        return "VIIB"
                    case 3:
                        return "VIIC"
                    case 4:
                        return "VIID"


    def getPatrolLength(self, patrol):
        """Determines full length of a given patrol (number of on station steps + all transit steps"""
        match patrol:
            case "North America" | "Caribbean":
                return self.sub.patrol_length - 1 + 8  # NA patrol has 1 less on station patrol + 2 BoB + EXTRA 2 transits
            case _:
                return self.sub.patrol_length + 4

    def getPatrol(self, pickingPatrol):
        """Gets patrol based on date, type, permanent assignments, etc from patrol text files."""

        patrolChart = ""
        if self.date_year == 1939 or (self.date_month <= 2 and self.date_year == 1940):  # 1939 - Mar 1940
            patrolChart = "PatrolChart1.txt"
        elif self.date_month > 2 and self.date_month <= 5 and self.date_year == 1940:  # 1940 - Apr - Jun
            patrolChart = "PatrolChart2.txt"
        elif self.date_month >= 6 and self.date_month <= 11 and self.date_year == 1940:  # 1940 - Jul - Dec
            patrolChart = "PatrolChart3.txt"
        elif self.date_month >= 0 and self.date_month <= 5 and self.date_year == 1941:  # 1941 - Jan - Jun
            patrolChart = "PatrolChart4.txt"
        elif self.date_month >= 6 and self.date_month <= 11 and self.date_year == 1941:  # 1941 - Jul - Dec
            patrolChart = "PatrolChart5.txt"
        elif self.date_month >= 0 and self.date_month <= 5 and self.date_year == 1942:  # 1942 - Jan - Jun
            patrolChart = "PatrolChart6.txt"
        elif self.date_month >= 6 and self.date_month <= 11 and self.date_year == 1942:  # 1942 - Jul - Dec
            patrolChart = "PatrolChart7.txt"
        elif self.date_year == 1943:  # 1943
            patrolChart = "PatrolChart8.txt"
        else:
            print("Error getting txt")

        ordersRoll = d6Rollx2()

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
                    count = x + 1
                    tp = str(count) + ") " + uniqueOrders[x]
                    print(tp)
                inpNum = getInputNum("Pick your orders: ", 1, len(uniqueOrders))
                orders = uniqueOrders[inpNum - 1]
            else:
                orders = lines[ordersRoll - 2]

        # strip any stray returns that may have gotten into the orders string
        orders = orders.strip('\n')

        orders = self.validatePatrol(orders, pickingPatrol)

        self.currentOrders = orders

    def buildPatrol(self, patrol):
        """Builds array of strings, each item being a step in the patrol. Step 0 is port."""
        #build patrol for non NA patrols
        NAorders = False
        if self.currentOrders == "North America" or self.currentOrders == "Carribean":
            NAorders = True

        patrolLength = self.getPatrolLength(self.currentOrders)
        for x in range (patrolLength + 1):
            if x == 0:
                self.patrolArray.append("Port")
            elif x == 1 or x == patrolLength:
                if self.francePost and not self.permMedPost:
                    self.patrolArray.append("Bay of Biscay")
                else:
                    self.patrolArray.append("Transit")
            elif x == 2 or x == patrolLength - 1:
                self.patrolArray.append("Transit")
            elif x == 3 and "Abwehr" in self.currentOrders and not NAorders:
                self.patrolArray.append("Mission")
            elif x == 3 and "Minelaying" in self.currentOrders and not NAorders:
                self.patrolArray.append("Mission")
            elif (x == 3 or x == patrolLength - 2) and NAorders:
                self.patrolArray.append("Transit")
            elif (x == 4 or x == patrolLength - 3) and NAorders:
                self.patrolArray.append("Transit")
            elif x == 5 and "Abwehr" in self.currentOrders and NAorders:
                self.patrolArray.append("Mission")
            elif x == 5 and "Minelaying" in self.currentOrders and NAorders:
                self.patrolArray.append("Mission")
            else:
                newp = self.currentOrders
                if "Abwehr" in self.currentOrders:
                    newp = self.currentOrders.replace("(Abwehr Agent Delivery)", "")
                elif "Minelaying" in self.currentOrders:
                    newp = self.currentOrders.replace("(Minelaying)", "")
                elif "Wolfpack" in self.currentOrders:
                    newp = self.currentOrders.replace("(Wolfpack)", "")
                self.patrolArray.append(newp)

        #remove one NA/Caribbean patrol if applicable
        if "Caribbean" in self.currentOrders or "North America" in self.currentOrders:
            try:
                self.patrolArray.remove("North America")
                self.patrolArray.remove("Caribbean")
            except:
                pass

    def validatePatrol(self, orders, pickingPatrol):
        """Deal with changes in orders based on U-Boat type"""
        if orders == "Mediterranean" or orders == "Artic" and ("IX" in self.sub.getType()): #IX cannot patrol Artic or Med
            orders = "West African Coast"
        if (orders == "West African Coast" or orders == "Caribbean") and ("VII" in self.sub.getType()):  # VII Cannot patrol west africa
            orders = "Atlantic"
        if orders == "British Isles" and self.sub.getType() == "VIID":
            orders = "British Isles(Minelaying)"

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

        #Do not allow VIID and VIIC Flak in the Med, so recall and get new orders
        if self.sub.getType() == "VIID" or self.sub.getType() == "VIIC Flak":
            if orders == "Mediterranean":
                orders = self.getPatrol(pickingPatrol)

        return orders

    def gameloop(self):
        """The normal game loop. Get patrol, conduct patrol, return and repair+rearm."""
        playing = True
        while playing:
            self.startPatrol()
            self.patrol()
            self.portReturn()
            if self.date_year == 1943 and self.date_month > 5:
                playing = False

        self.promotionCheck()
        gameover(self, "Survived - promoted to desk job")

    #------------------ PATROL LOOP -------------------

    def startPatrol(self):
        """Starts a new patrol, getting new assignment based on rank, date etc."""
        print("---------------")
        print("Guten Tag,", self.getOfficerRank(), "- The date is", self.getFullDate())

        #get next patrol orders
        if self.sub.crew_levels["Kommandant"] > 0:
            if verifyYorN("PATROL ASSIGNMENT: Roll to choose next patrol? ") == "Y":
                roll = d6Roll()
                print("Die roll:", roll)
                #check to see if player can select orders
                if roll <= self.sub.crew_levels["Kommandant"]:
                    print("You may select your patrol.")
                    self.getPatrol(True)
                else:
                    self.getPatrol(False)
        else:
            self.getPatrol(False)

        print("Patrol Assignment:", self.currentOrders)
        time.sleep(2)
        depart = "U-" + str(self.id) + " departs port early before dawn for " + self.getOfficerRank() + " " + self.kmdt + "'s " + str(self.patrolCount[self.patrolNum] + " patrol.")
        print(depart)
        self.currentBox = 1
        self.abortingPatrol = False
        self.buildPatrol(self.currentOrders)
        time.sleep(3)

    def patrol(self):
        """Full patrol loop accounting for leaving port, transiting, patrolling and returning"""

        # if Artic patrol, roll to see if permanently assigned to Arctic
        if self.currentOrders == "Arctic":
            print("BDU is currently determining to assign you to the arctic permanently. ")
            if d6Roll() <= 3:
                print("You've been assigned permanently to the Arctic.")
                self.permArcPost = True

        # while current step is less than the full patrol length (station patrol + transit boxes)
        #LOOP TO RUN THROUGH PATROL ARRAY (each patrol box)
        x = 0
        patrolLength = len(self.patrolArray) - 1
        while x <= patrolLength:

            if x == 0: #skip first entry in patrol array which is port
                x += 1
                continue
            if self.abortingPatrol and x < len(self.patrolArray) - 2:
                x += 1
                continue

            #if doctor is SW or KIA, see if any other injured crew members die (each patrol box, before encounter)
            if self.sub.crew_health["Doctor"] >= 2:
                # check if any hurt crewmen
                swCrew = countOf(self.sub.crew_health.values(), 2)
                count = 0
                if swCrew > 0:
                    for key in self.sub.crew_health:
                        if self.sub.crew_health[key] == 2:
                            survivalRoll = d6Roll()
                    for key in self.sub.crew_health:
                        if self.crew_health[key] == 2:
                            survivalRoll = d6Roll()
                            if survivalRoll >= 4:
                                print(key, "has died of his wounds.")
                                self.sub.crew_health[key] = 3

            currentBoxName = self.patrolArray[x]

            #check for automatic aborts (diesel engine(s) inop, fuel tanks inop)
            if self.sub.dieselsInop() == 2:
                if x == len(self.patrolArray):
                    print("We are towed back to port.")
                    break
                else:
                    print("Both Diesel engines are knocked out. We must scuttle the boat!")
                    scuttleFromDieselsInop(self)
                    return 0
            elif (self.sub.dieselsInop() == 1 or self.sub.systems["Fuel Tanks"] == 2) and not self.abortingPatrol:
                if self.sub.systems["Fuel Tanks"] == 2:
                    print("We must abort the patrol, our fuel tanks are damaged beyond repair.")
                if self.sub.dieselsInop() == 1:
                    print("We must abort the patrol, one our diesel engines are damaged beyond repair.")
                self.abortingPatrol = True
                continue

            self.printPatrolStatus(currentBoxName, x)

            #check if on weather duty or severe weather random events... (skips current box)
            if self.weatherDuty:
                #skip if on mine or abwehr duties and in mission box (delay skipping of box until next)
                if currentBoxName == "Mission":
                    print("Approaching mission location, we will delay sending our weather reports.")
                elif (x < len(self.patrolArray) - 2) or (x < len(self.patrolArray) - 1):
                    self.weatherDuty = False
                    print("Sending weather reports.")
                    x += 1
                    continue
            if self.severeWeather:
                if currentBoxName == "Mission":
                    print("Approaching mission location, despite the severe storm.")
                    self.severeWeather = False
                elif (x < len(self.patrolArray) - 2 or x < len(self.patrolArray) - 1):
                    print("We ride out the storm for a while and finally the storm abates.")
                    self.severeWeather = False
                    x += 1
                    continue

            #skip first iteration of asking for action (on departure)- otherwise ask for next action before making roll
            if x == 1:
                invalid = False
            else:
                self.currentBox = x
                invalid = True
            while invalid:
                action = verifyNextAction(self.abortingPatrol)
                match action:
                    case "Continue":
                        invalid = False
                    case "Stores":
                        self.sub.subSupplyPrintout(False)
                    case "Damage":
                        self.sub.printStatus()
                    case "Abort":
                        print("Aborting patrol.")
                        self.abortingPatrol = True
                        invalid = False
            if self.abortingPatrol and x < len(self.patrolArray) - 2:
                continue

            self.getEncounter(currentBoxName, self.getYear(), self.randomEvent)

            #roll second time for 1 inop... 2 rolls for encounter when aborting and 1 diesel engine knocked out
            if self.sub.dieselsInop() == 1 and currentBoxName == "Transit":
                self.getEncounter(currentBoxName, self.getYear(), self.randomEvent)

            # check for resupply at the last patrol space before transit home
            if x == len(self.patrolArray) - 3:
                if self.currentOrders != "Mediterranean" or self.currentOrders != "North America" or self.currentOrders != "Caribbean":
                    if self.milkCow():
                        x = 2

            #increment loop and move to next box
            x += 1

        # check at end of patrol... if it was a Med patrol, set U boat permanently to Med
        if self.currentOrders == "Mediterranean":
            self.permMedPost = True

    def drawPatrolMeter(self, currentBoxNum):
        numDashes = self.getPatrolLength(self.currentOrders)
        print("<", end = "")
        for x in range (numDashes):
            if x == currentBoxNum - 1:
                print(" 0 ", end = "")
            else:
                print(" - ", end = "")
        print(">")

    def printPatrolStatus(self, currentBox, currentBoxNum):
        self.drawPatrolMeter(currentBoxNum)
        print("Current Box:", currentBox)

    #-------------END OF PATROL GAMEKEEPING-------------

    def portReturn(self):
        """Called after patrol to deal with notification, print out sunk ships so far, and then deal with repair and rearm."""

        self.portReturnText()

        # reset ships sunk on current patrol
        self.shipsSunkSinceLastPromotionCheck += len(self.shipsSunkOnCurrentPatrol)
        self.shipsSunkOnCurrentPatrol.clear()

        #refit and advance time based on damage
        refitTime = self.sub.refit(self)
        #if refit time was more than 5 months, it is changed to 0 months and player is given new sub
        if refitTime == 0:
            self.pastSubs.append(self.id)
            self.id = random.randint(20,999)
            toprinttext = "Repair and refit will take too long, BDU has reassigned you to U-" + str(self.id)
            print(toprinttext)
        else:
            self.advanceTime(refitTime)

        #move forward 2 months per patrol of larger boats, otherwise 1 month
        if self.sub.getType() == "IXA" or self.sub.getType() == "IXB" or self.sub.getType() == "VIID":
            self.advanceTime(2)
        else:
            self.advanceTime(1)

        #determine if mission was completed for patrol and adjust mission counts
        if self.missionComplete:
            self.successfulPatrols += 1
            self.unsuccessfulPatrolsInARow = 0
            self.lastPatrolWasUnsuccessful = False
        if self.missionComplete == False:
            self.lastPatrolWasUnsuccessful = True
            self.unsuccessfulPatrolsSinceLastPromotionCheck += 1
            self.unsuccessfulPatrolsInARow += 1
            if self.unsuccessfulPatrolsInARow == 3:
                self.sub.crew_levels["Crew"] = self.sub.crew_levels["Crew"] - 1
                if self.sub.crew_levels["Crew"] < 0:
                    self.sub.crew_levels["Crew"] = 0

        #ensure no abwehr agent is aboard
        self.sub.crew_health["Abwehr Agent"] = -1
        #reset superior Torpedoes
        self.superiorTorpedoes = False
        #reset random Event
        self.randomEvent = False
        #reset successful mission
        self.missionComplete = False

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

        #determine if 1WO is experienced, and roll to see if he is promoted out of the ship
        if self.sub.crew_levels["Watch Officer 1"] == 1:
            if d6Roll() == 6:
                print("Watch Officer 1 has been promoted to captain a new boat. You have received a replacement 1WO.")
                self.sub.crew_levels["Watch Officer 1"] = 0

        self.knightsCrossCheck()
        reassigned = False
        if self.eligibleForNewBoat:
            if verifyYorN("You're eligible for reassignment to a new boat. Would you like to be reassigned? ") == "Y":
                self.pastSubs.append(self.id)
                newsub = self.chooseSub(True)
                self.sub2 = Submarine(newsub)

                #move things over
                self.sub2.crew_levels = self.sub.crew_levels
                self.sub2.knightsCross = self.sub.knightsCross

                self.sub = self.sub2
                del self.sub2
                self.id = random.randint(10,999)
                reassigned = True
                self.eligibleForNewBoat = False
                toP = "You've been assigned to U-" + str(self.id)
                print(toP)

        totalTonnage = 0
        for x in range(len(self.shipsSunk)):
            totalTonnage = totalTonnage + self.shipsSunk[x].GRT
        totalTonnage = f"{totalTonnage:,}"
        if self.patrolNum > 1:
            print("You've made", str(self.patrolNum), "patrols and sunk", str(len(self.shipsSunk)), "ships totaling", totalTonnage, "tons.")
        else:
            print("You've made", str(self.patrolNum), "patrol and sunk", str(len(self.shipsSunk)), "ships totaling",
                  totalTonnage, "tons.")

        if self.sub.knightsCross > 0:
            print("Awards: ", end="")
            print(self.awardName[self.sub.knightsCross])

        self.patrolNum += 1
        self.patrolArray.clear()
        time.sleep(5)

        #rearm boat
        if not reassigned:
            if verifyYorN("Use same loadout as previous patrol? ") == "Y":
                self.sub.setLastLoadout()
            else:
                self.sub.torpedoResupply()
        else:
            self.sub.torpedoResupply()

    def portReturnText(self):
        """Runs through patrol return flavor text and checks last patrol success or failure"""
        flavorText1 = d6Roll()
        flavorText2 = d6Roll()
        print("====================================================")
        damagedTotal = countOf(self.sub.systems.values(), 1)
        if self.sub.hull_Damage >= 6:
            returnMessage = "U-" + str(self.id) + " slowly moves into the bay, barely afloat. A tug is needed to help you in."
        elif self.sub.hull_Damage >= 4:
            returnMessage = "U-" + str(self.id) + " limps back into port, scarred and damaged, but still afloat."
        elif damagedTotal > 3:
            returnMessage = "U-" + str(self.id) + " returns to port with visible signs of damage."
        else:
            match flavorText1:
                case 1 | 2:
                    returnMessage = "U-" + str(self.id) + " glides back into port with much fanfare."
                case 3 | 4:
                    returnMessage = "U-" + str(self.id) + " cruises into your home port with the band playing on the pier."
                case 5 | 6:
                    returnMessage = "U-" + str(self.id) + " is welcomed back to port with cheers and flowers."
        print(returnMessage)

        sunkCap = False
        for x in range (len(self.shipsSunkOnCurrentPatrol)):
            if self.shipsSunkOnCurrentPatrol[x].type == "Capital Ship":
                capname = self.shipsSunkOnCurrentPatrol[x].name
                sunkCap = True

        if self.missionComplete:
            match flavorText2:
                case 1 | 2:
                    if "Mine" in self.currentOrders:
                        print("Great job. The successful deployment of mines on your patrol is critical to victory.")
                    elif "Abwehr" in self.currentOrders:
                        print("Well done. The delivery of our agent onto enemy shores will hinder their war effort greatly.")
                    elif sunkCap:
                        print("The news outlets are abuzz with your glorious sinking of the", capname)
                    elif len(self.shipsSunkOnCurrentPatrol) > 1:
                        print("Excellent work. Your patrol was a success, sinking", len(self.shipsSunkOnCurrentPatrol), "ships!")
                    else:
                        print("Good work, we know you can do better out there, but it's still a successful patrol.")
                case 3 | 4:
                    if "Mine" in self.currentOrders:
                        print("The war effort has benefitted greatly from your successful mining of the target area.")
                    elif "Abwehr" in self.currentOrders:
                        print("Thanks to your successful mission, our agent is now able to feed us critical intelligence.")
                    elif sunkCap:
                        print("The sinking of the", capname, "has hurt their morale and brought you glory!")
                    elif len(self.shipsSunkOnCurrentPatrol) > 1:
                        print("A great patrol. By sinking", len(self.shipsSunkOnCurrentPatrol), "ships, you've hindered the enemy's war effort drastically.")
                    else:
                        print("Nice job. A single ship sunk won't help us enough but keep at it.")
                case 5 | 6:
                    if "Mine" in self.currentOrders:
                        print("Reports intercepted from the enemy indicate the mining of your target area was a success. Great job.")
                    elif "Abwehr" in self.currentOrders:
                        print("We're receiving great intelligence reports from the agent you landed. Well done.")
                    elif sunkCap:
                        print("Your story of the sinking of the", capname, "fuels our propagada machine!")
                    elif len(self.shipsSunkOnCurrentPatrol) > 1:
                        print("With", len(self.shipsSunkOnCurrentPatrol), "less enemy ships, you've hurt the enemy's capabilities to continue the war.")
                    else:
                        print("BDU would like to see you sink more than a single ship per patrol. Get back out there and get some more.")
        else:
            if "Mine" in self.currentOrders:
                print("Failure to mine the designated grid hinders our efforts at sea.")
            elif "Abwehr" in self.currentOrders:
                print("Failure to delivery our agent has hurt the war effort greatly.")
            else:
                print("Countless ships have managed to get by our patrols - we need to see improvement.")

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
                self.eligibleForNewBoat = True
        # if KMDT has Knight's Cross, check for awarding of for Knight's Cross Oakleaves KCO
        # (175k tons, or sunk capital ship / 75k tons since last promo)
        # in addition to above bonus, favorable -1 roll mod when firing (to hit)
        elif self.sub.knightsCross == 1:
            if totalTonnageSunk > 175000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 75000:
                print("You've been awarded the Knight's Cross with Oakleaves! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 2
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
                self.eligibleForNewBoat = True
        # if KMDT has Knight's Cross Oakleaves, check for awarding of for Knight's Cross Oakleaves and Swords KCO&S
        # (250k tons, or sunk capital ship / 75k tons since last promo)
        # in addition to above bonuses, favorable -1 roll mod for escort detection
        elif self.sub.knightsCross == 2:
            if totalTonnageSunk > 200000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 75000:
                print("You've been awarded the Knight's Cross with Oakleaves and Swords! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 3
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
                self.eligibleForNewBoat = True
        # if KMDT has Knight's Cross Oakleaves and Swords, check for awarding of for Knight's Cross Oakleaves, Swords, and Diamonds KCOS&D
        # (300k tons, or sunk capital ship / 50k tons since last promo)
        # in addition to above bonuses, following attempts are always successful
        elif self.sub.knightsCross == 3:
            if totalTonnageSunk > 300000 or self.capitalShipsSunkSinceLastKnightsCross > 0 or GRTSunkSinceLastKnightsCross > 50000:
                print("You've been awarded the Knight's Cross with Oakleaves, Swords, and Diamonds! Congratulations,",
                      self.rank[self.sub.crew_levels["Kommandant"]], self.kmdt)
                self.sub.knightsCross = 4
                self.capitalShipsSunkSinceLastKnightsCross = 0
                self.monthOfLastKnightsCrossAward = self.getMonth()
                self.yearOfLastKnightsCrossAward = self.getYear()
                self.eligibleForNewBoat = True

    #--------------------------------------------- Patrol checks and encounter checks

    def getEncounter(self, loc, year, randomEvent, existingPlane = ""):
        """Determines which location encounter chart to use, then rolls against and returns the string encounter name"""
        roll = d6Rollx2()
        if loc != "Additional Round of Combat":
            print("Roll for location:", loc, "-", roll)

        # First check if random event (natural 12)
        if roll == 12 and randomEvent == False and loc != "Additional Round of Combat" and loc != "Mission":
            print("RANDOM EVENT!")
            time.sleep(2)
            self.encounterRandomEvent()
            self.randomEvent = True
            return "Random Event"

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
                        if loc == "Additional Round of Combat":
                            print("An enemy escort has arrived!")
                        else:
                            print("We were unable to slip through! An escort is headed for us!")
                        shipE = Ship("Escort")
                        self.escortDetection("", 7, "Submerged", "Day", True, 0, 0, shipE.name, 0)
                    case 4 | 5:
                        if loc == "Additional Round of Combat":
                            if existingPlane == "":
                                print("A plane has picked up our combat and is making an attack run!")
                                self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                            else:
                                print("The plane is making another attack!")
                                self.encounterAircraft(self.sub, self.getYear(), self.currentOrders, existingPlane)
                        else:
                            print("We were unable to slip through! A plane is making an attack run!")
                            self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                    case _:
                        # no encounter
                        self.encounterNone(loc)
            case "Bay of Biscay" | "Mission" | "Resupply":
                if loc == "Resupply":
                    resupply = True
                    resupplyNotInterrupted = True
                else:
                    resupply = False
                rollDRM = 0
                if year == 1942 and (loc == "Bay of Biscay" or loc == "Resupply"):
                    rollDRM -= 1
                elif year == 1943 and (loc == "Bay of Biscay" or loc == "Resupply"):
                    rollDRM -= 2
                if loc == "Mission":
                    rollDRM -= 1
                match roll + rollDRM:
                    case -2 | -1 | 0 | 1 | 2 | 3 | 4:
                        # aircraft encounter during mission
                        if loc == "Mission":
                            missionInterrupted = True
                            while missionInterrupted:
                                self.encounterAircraft(self.sub, self.getYear(), self.currentOrders)
                                roll = d6Roll()
                                if roll + rollDRM <= 4:
                                    continue
                                else:
                                    print("We've lost the aircraft, we can move in to perform our mission.")
                                    missionInterrupted = False
                        #normal aircraft encounter in BoB
                        else:
                            if resupply:
                                resupplyNotInterrupted = False
                                print("While moving alongside to refuel, an aircraft moves in to attack!")
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
                        self.missionComplete = True
                    self.sub.reload()
                #check to see if abwehr agent mission was success
                if loc == "Mission" and "Abwehr" in self.currentOrders:
                    self.sub.crew_health["Abwehr Agent"] = -1
                    self.missionComplete = True
                    print("We successfully land our agent on shore.")
                #check if resupply was interrupted, if not, returns true
                if resupply:
                    return resupplyNotInterrupted


    ##----------------------------------------------- ENCOUNTERS

    def milkCow(self):
        """Checks to see if a milk cow U-Boat is available to resupply the player's ship with fuel and possibly torpedoes
        Returns TRUE if the player was able to successfully resupply fuel. Otherwise returns FALSE"""
        toReturn = False

        #check if milk cow is available to resupply fuel
        if d6Roll() == 1:
            print("A milk cow is moving to rendevous and resupply you with fuel!")
            if self.getEncounter("Resupply", self.date_year, self.randomEvent) == True:
                print("We successfully refuel.")
                toReturn = True

                #check if torpedoes are available
                torpedoSupplyRoll = d6Roll()
                numToAdd = d6Roll()
                if torpedoSupplyRoll == 1:
                    #receive steam torpedoes
                    numAdded = self.sub.addTorpedoes("G7a", numToAdd)
                    print("They were able to resupply us with", numAdded, "steam torpedoes!")
                elif torpedoSupplyRoll == 2:
                    #receive electric torpedoes
                    numAdded = self.sub.addTorpedoes("G7e", numToAdd)
                    print("They were able to resupply us with", numAdded, "electric torpedoes!")
                elif torpedoSupplyRoll == 3:
                    #receive 2 of each torpedoes
                    numAddedS = self.sub.addTorpedoes("G7a", 2)
                    numAddedE = self.sub.addTorpedoes("G7e", 2)
                    print("They were able to supply us with", numAddedS, "steam torpedoes and", numAddedE, "electric torpedoes!")
                else:
                    print("The milk cow does not have any torpedoes it can provide us.")

            if toReturn == True:
                self.advanceTime(1, True)
        return toReturn

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
            #case "Additional Round of Combat":

        time.sleep(2)

    def encounterRandomEvent(self):
        """When 12 is rolled for the first time on an encounter box in a patrol - roll against random event table."""
        self.randomEvents += 1
        eventroll = d6Rollx2()
        printRollandMods("Roll for random event: ", eventroll, 0)
        match eventroll:
            case 2:
                dead = d6Roll()
                while self.halsUndBeinbruch > 0 and dead == 1:
                    print("You got lucky! Rerolling who was swept overboard.")
                    self.halsUndBeinbruch -= 1
                    dead = d6Roll()
                match dead:
                    case 1:
                        gameover(self, "KMDT was swept overboard at sea")
                    case 2:
                        if self.sub.crew_health["Engineer"] < 3:
                            self.sub.crew_health["Engineer"] = 3
                            print("Man overboard! A huge wave hit the U-boat and our engineer was swept overboard.")
                    case 3, 4:
                        if self.sub.crew_health["Watch Officer 1"] < 3:
                            self.sub.crew_health["Watch Officer 1"] = 3
                            print("Man overboard! A huge wave hit the U-boat and our First Watch Officer was swept overboard.")
                    case 5, 6:
                        if self.sub.crew_health["Watch Officer 2"] < 3:
                            self.sub.crew_health["Watch Officer 2"] = 3
                            print("Man overboard! A huge wave hit the U-boat and our Second Watch Officer was swept overboard.")
            case 3:
                print("Caught Unawares! An aircraft attacks out of the sun!")
                aircraft = Aircraft()
                aircraftT = aircraft.getType()
                self.sub.crewInjury(self, aircraftT, True)
                self.encounterAircraft(self.sub, self.getYear(), self.currentOrders, aircraftT)
            case 4:
                print("Our gyrocompass has failed. Attempt to repair...")
                repairroll = d6Roll()
                repairMods = 0
                if self.sub.crew_levels["Engineer"] == 1:
                    repairMods -= 1
                printRollandMods("Attempt to repair gyrocompass (2-):", repairroll, repairMods)
                if repairroll + repairMods <= 2:
                    print("We successfully repaired the gyrocompass!")
                else:
                    print("Unable to repair. We must return to port.")
                    self.abortingPatrol = True
            case 5:
                print("We've discovered during maintenance that our boat has been loaded with superior torpedoes!")
                print("Our dud chances have been reduced!")
                self.superiorTorpedoes = True
            case 6:
                print("We meet a sister ship at sea.")
                inopTotal = countOf(self.sub.systems.values(), 2)
                count = 2
                if inopTotal > 0 and inopTotal <= 2:
                    print("She's able to help with some repairs.")
                    for key in self.systems:
                        if self.systems[key] == 2:
                            print(key, "was repaired!")
                            self.systems[key] = 0
                if inopTotal > 2:
                    print("She's able to help repair two damaged systems.")
                    for key in self.systems:
                        if self.systems[key] == 2 and count > 0:
                            if count == 2:
                                print("2 repairs left. Repair:", key, "?")
                            else:
                                print("1 repair left. Repair:", key, "?")
                            if verifyYorN("Repair System? ") == "Y":
                                self.systems[key] = 0
                                count -= 1
                else:
                    print("You exchange some news and wish each other luck in the hunt.")
            case 7:
                print("Hals und beinbruch! You feel lucky!")
                self.halsUndBeinbruch += 1
            case 8:
                if "Caribbean" not in self.currentOrders or "North America" not in self.currentOrders or "West African Coast" not in self.currentOrders:
                    print("You've received a report from the Luftwaffe of a single ship nearby.")
                    self.encounterAttack("Ship")
                else:
                    print("The luftwaffe is unable to provide you with useful ship movements in this area.")
            case 9:
                print("We've been assigned to weather reporting duties.")
                self.weatherDuty = True
            case 10:
                if self.sub.getTotalTorpedoes() > 0:
                    print("Torpedo has broken loose during servicing!")
                    self.sub.crewInjury(self, "Torpedo Incident")
            case 11:
                print("Severe storm - we must ride it out. We're not going to find anything out here for a while.")
                self.severeWeather = True
            case 12:
                if "Caribbean" in self.currentOrders or "West African Coast" in self.currentOrders or "Mediterranean" in self.currentOrders:
                    print("Swim call! Everyone on deck for a relaxing swim.")
                    faller = d6Roll()
                    while self.halsUndBeinbruch > 0 and faller == 1:
                        print("You got lucky! Rerolling who was swept overboard.")
                        self.halsUndBeinbruch -= 1
                        faller = d6Roll()
                    match faller:
                        case 1:
                            gameover(self, "KMDT slipped and fell on deck, hitting his head")
                        case 2:
                            if self.sub.crew_health["Engineer"] < 3:
                                self.sub.crew_health["Engineer"] = 3
                                print("While running on the deck, the engineer slipped and hit his head. Rest in peace.")
                        case 3, 4:
                            if self.sub.crew_health["Watch Officer 1"] < 3:
                                self.sub.crew_health["Watch Officer 1"] = 3
                                print("While running on the deck, the First Watch Officer slipped and hit his head. Rest in peace.")
                        case 5, 6:
                            if self.sub.crew_health["Watch Officer 2"] < 3:
                                self.sub.crew_health["Watch Officer 2"] = 3
                                print("While running on the deck, the Second Watch Officer slipped and hit his head. Rest in peace.")
                else:
                    print("The ship's crew could've enjoyed a nice swim if we were in warmer waters.")


    def encounterAircraft(self, sub, year, patrolType, aircraftT = ""):
        """When 'Aircraft' is rolled on a given encounter chart, or additional round of combat brings an aircraft"""
        if aircraftT == "":
            aircraft = Aircraft()
            aircraftT = aircraft.getType()
            print("ALARM! Aircraft in sight! Looks like it's a", aircraftT)
            #print("Rolling to crash dive!")
        else:
            print(aircraftT, "is making another attack run!")

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
        if self.patrolArray[self.currentBox] == "Mission":
            drm -= 1

        a1AircraftEncounterRoll = roll + drm
        printRollandMods("Roll for crash dive! (6+):", roll, drm)

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
                    self.sub.crewInjury(self, aircraftT, True)
                    self.sub.attacked(self, "Surfaced", 0, self.getYear(), aircraftT, True)
                    aircraft = "Destroyed"
                else:
                    print("We've managed to damage the aircraft!")
                    self.sub.crewInjury(self, aircraftT, True)
                    self.sub.attacked(self, "Surfaced", 0, self.getYear(), aircraftT, True)
                    if a1AircraftEncounterRoll <= 1:
                        self.sub.attacked(self, "Surfaced", 0, self.getYear(), aircraftT, True)
                    if flakRoll + flakMods <= 5:
                        aircraft = "Damaged"
        else:
            print("Successful crash dive!")

        #roll for another possible encounter if crash dive was not successful and aircraft was not shot down
        if aircraft == "Damaged" or aircraft == "Undamaged" and a1AircraftEncounterRoll <= 5:
            self.getEncounter("Additional Round of Combat", self.getYear(), self.randomEvent, aircraftT)

        if a1AircraftEncounterRoll <= 5:
            self.sub.repair(self)

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

        if verifyYorN("Do you wish to attack? ") == "N":
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

        self.sub.repair(self)
        self.sub.reload()
        self.G7aFired = 0
        self.G7eFired = 0
        #check if lost contact from changing from night to day
        if lostthem == "Lost Them":
            print("We lost them!")
            return "exit"

        #check if diesel engines were knocked out during fight
        if self.sub.dieselsInop() > 0 or self.sub.systems["Fuel Tanks"] == 2:
            return "exit"

        #check if all ships aside from escorts have been sunk (end of combat)
        elif (shipsSunk == len(ship) - 1 and ship[0].type == "Escort") or shipsSunk == len(ship):
            if enc == "Convoy":
                if verifyYorN("Attempt to follow convoy? ") == "Y":
                    followRoll = d6Roll()
                    if followRoll <= 4 or self.sub.knightsCross == 4:
                        self.encounterAttack("Convoy")
                    else:
                        print("We lost contact with the convoy!")
            else:
                print("We sunk all targets!")
        else:   #for when any target ships (not escorts) are still afloat
            #decide whether to follow or not
            if verifyYorN("Follow target(s) to make another attack? ") == "Y":
                #deal with convoys
                if enc == "Convoy":
                    if shipsDamaged > 0:
                        followPrompt = getInputNum("Follow damaged ship(s) or the convoy?\n1) Damaged Ships\n2) Convoy", 1, 2)
                    else:
                        followPrompt = 2

                    match followPrompt:
                        #Following damaged ship(s) - remove undamaged ships, automatic follow, see if it was escorted
                        case 1:
                            self.followFlow(ship)
                        #following convoy, roll to follow etc
                        case 2:
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
                            followPrompt = getInputNum("Follow damaged ship(s) or the rest?\n1) Damaged Ship(s)\n2) Undamaged Ship(s)", 1, 2)
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
                    elif shipsDamaged == 1:
                        if Escorted(ship):
                            followRoll = d6Roll()
                            if followRoll <= 4 or self.sub.knightsCross == 4:
                                print("Following the damaged, escorted ship.")
                                self.encounterAttack(enc, ship)
                            else:
                                print("The escort seems to have separated from the damaged ship. We can follow easily.")
                                ship.pop(0)
                                self.encounterAttack(enc, ship)

                        else:   #this else catches all unescorted encounters
                            #first check on Addl round of combat chart to see if an escort shows up
                            if self.getEncounter("Additional Round of Combat", self.getYear(), self.randomEvent) == "Escort":
                                newShip = []
                                newShip.append(Ship("Escort"))
                                newShip.append(ship[0])
                                if ship[1] is not None:
                                    newShip.append(ship[1])
                                self.escortDetection(enc, 7, "Submerged", "Day", False, self.G7aFired, self.G7eFired, newShip[0].name, 0)
                                self.encounterAttack("Ship + Escort", newShip)
                            else:
                                print("Closing to attack again!")
                                self.encounterAttack(enc, ship)
                    else: #no damaged ships - should trigger after an early detection and attempt to follow with same exact enc and existing ship array- should not trigger at any other point
                        followRoll = d6Roll()
                        if followRoll <= 4 or self.sub.knightsCross == 4:
                            self.encounterAttack(enc, ship)
                        else:
                            print("We weren't able to follow.")

        time.sleep(2)

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
            for x in range(len(ship)):
                if ship[x].type == "Escort":
                    continue
                if ship[0].type == "Escort":
                    toPrint = (str(x) + ") " + str(ship[x]))
                else:
                    toPrint = (str(x+1) + ") " + str(ship[x]))
                print(toPrint)

            if ship[0].type == "Escort":
                b = getInputNum("Select ship to follow: ", 1, len(ship)-1)
            else:
                b = getInputNum("Select ship to follow: ", 1, len(ship))
                b = b - 1

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

    def escortDetection(self, enc, range, depth, timeOfDay, previouslyDetected, firedG7a, firedG7e, escortName, wpMod, firedFandA = False):
        """Called when an escort detection roll is required."""
        attackDepth = depth

        escortRoll = d6Rollx2()
        escortMods = 0

        #if wolfpack and -1 passed in to escort detection (not rolled yet for combat)
        #determine if escorts are busy with other boats, or focused on player's
        if "Wolfpack" in self.currentOrders and wpMod == 0 and enc == "Convoy":
            wolfpackRoll = d6Roll()
            if wolfpackRoll <= 5:
                print("Escorts are busy chasing other U-Boats, we should have an easier time attacking.")
                wpMod = -1
            else:
                print("Escorts are focused on our boat, we will have a harder time attacking.")
                wpMod = 1
            escortMods += wpMod

        # deal with close range detection before anything has been fired first, then deal with normal detection
        if range == 8 and firedG7a == 0 and firedG7e == 0 and previouslyDetected == False:
            escortMods -= 2
            if self.getYear() >= 1941 and range == 8:
                escortMods = escortMods + (self.getYear() - 1940)
            if self.sub.knightsCross >= 3:
                escortMods -= 1
        else:
            if depth != "Surfaced" or previouslyDetected:
                self.sub.printStatus()
                if self.sub.hull_Damage == (self.sub.hull_hp - 1):
                    print("We're unable to dive to test depth, as we fear it would be the end of us. Our hull is only just holding together.")
                else:
                    if verifyYorN("Dive to test depth? ") == "Y":
                        self.sub.diveToTestDepth(self, escortName)
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
            if firedFandA and not previouslyDetected:
                escortMods += 1
            if range == 6:
                escortMods -= 1
            if depth == "Test Depth":
                escortMods -= 1

        printRollandMods("Escort pinging! Detection on 9+:", escortRoll,escortMods)
        time.sleep(3)
        # snake eyes automatic avoid detection
        if escortRoll == 2:
            "Our ship completely avoided detection!"
            time.sleep(3)
            return "Escaped"
        if escortRoll + escortMods <= 8:
            flavorText = d6Roll()
            match flavorText:
                case 1 | 2:
                    print("We've evaded detection!")
                case 3 | 4:
                    print("We've managed to slip away!")
                case 5 | 6:
                    print("We've lost the escort!")
            time.sleep(2)
            return "Escaped"
        elif escortRoll + escortMods <= 11:
            print("Detected!")
            self.sub.attacked(self, attackDepth, 0, self.getYear(), escortName)
        elif escortRoll + escortMods >= 12:
            print("Detected! Big Problems!")
            self.sub.attacked(self, attackDepth, 1, self.getYear(), escortName)
        time.sleep(3)
        self.escortDetection(enc, range, depth, timeOfDay, True, firedG7a, firedG7e, escortName, wpMod)

    def wasDud(self, torp):
        """Determines whether a fired torpedo was a dud based on date and a d6 roll"""
        dudRoll = d6Roll()
        if self.superiorTorpedoes:
            dudRoll -= 1
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
        if self.sub.systems["Periscope"] >= 1:
            print("Reminder, Captain, that our periscope is knocked out and we cannot attack submerged.")
        if timeOfDay == "Night":
            toFlip = verifyYorN("Do you wish to continue the attack at night? ")
        else:
            toFlip = verifyYorN("Do you wish to continue the during the day? ")
        if toFlip == "N":
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
            typeofAttack = getInputNum("Do you wish to attack: \n1) Surfaced\n2) Submerged ", 1, 2)
            match typeofAttack:
                case 1:
                    print("Manning the UZO for surface attack!")
                    depth = "Surfaced"
                case 2:
                    print("Periscope Depth!")
                    depth = "Submerged"

        # determine range
        if Escorted(ship):
            r = getInputNum("Choose Range:\n1) -WARNING ESCORT- Close\n2) Medium Range\n3) Long Range ", 1, 3)
        else:
            r = getInputNum("Choose Range:\n1) Close\n2) Medium Range\n3) Long Range ", 1, 3)
        detectedOnClose = False
        match r:
            case 1:
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

                    printRollandMods("Roll for avoid early detection (9-):", detectionRoll, detectionMods)
                    time.sleep(2)
                    if detectionRoll + detectionMods >= 12:
                        print("Detected! Big Problems!")
                        self.sub.attacked(self, "Submerged", 1, self.getYear(), ship[0].name)
                        time.sleep(3)
                        self.escortDetection(enc, 8, depth, timeOfDay, True, 0, 0, ship[0].name, 0)
                        detectedOnClose = True
                    elif detectionRoll + detectionMods >= 10:
                        print("They've detected us before we could attack!")
                        self.sub.attacked(self, "Submerged", 0, self.getYear(), ship[0].name)
                        time.sleep(3)
                        self.escortDetection(enc, 8, depth, timeOfDay, True, 0, 0, ship[0].name, 0)
                        detectedOnClose = True
            case 2:
                r = 7  # hit on 7 or less
            case 3:
                r = 6  # hit on 6 or less

        # show and assign weps
        if not detectedOnClose:
            self.sub.subSupplyPrintout(False)
            self.getAttackType(ship, depth, timeOfDay, r)

        if self.firedForward and self.firedAft:
            firedBoth = True
        else:
            firedBoth = False

        # post shot escort detection
        if Escorted(ship) and not detectedOnClose:
            if depth == "Surfaced":
                print("Escort incoming on our position! Dive! Dive!")
            else:
                print("Escort incoming on our position!")
            time.sleep(2)
            self.escortDetection(enc, r, depth, timeOfDay, False, self.G7aFired, self.G7eFired, ship[0].name, 0, firedBoth)

        #deal with additional attacks on unescorted
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check for further attacks in same round for unescorted targets
        didAttackSecondTime = False
        if not Escorted(ship) and shipsSunk != len(ship) and not detectedOnClose:
            if verifyYorN("Should we make another attack? ") == "Y":
                self.getAttackType(ship, depth, timeOfDay, r)
                didAttackSecondTime = True
            else:
                didAttackSecondTime = False

        #recheck for sunk / damaged ships
        shipsSunk = 0
        shipsDamaged = 0
        for x in range (len(ship)):
            if ship[x].sunk:
                shipsSunk += 1
            if ship[x].damage > 0 and ship[x].sunk == False:
                shipsDamaged += 1

        #check third (final) time for attack in same round on unescorted targets
        if not Escorted(ship) and shipsSunk != len(ship) and didAttackSecondTime:
            if verifyYorN("Should we make another attack? ") == "Y":
                self.getAttackType(ship, depth, timeOfDay, r)

        # resets to zero the number of torpedoes fired for the engagement
        self.G7aFired = 0
        self.G7eFired = 0
        self.firedForward = False
        self.firedAft = False
        self.firedDeckGun = False


    def getTarget(self, ship):
        """Validates input on ships to target. Only accepts a # from 0-# of ships, disallows firing at escorts. A 0 would
        indicate finished firing."""
        notValid = True
        while notValid:
            if len(ship) == 2 and ship[0].type == "Escort":  #assume target is only valid target
                target = 2
            if len(ship) > 1:
                target = getInputNum("Enter ship # from above to target. Enter 0 if done attacking. ", 0, len(ship))
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

        notFiredAtAllShips = True
        # validation loop to get a target, then # of torps to fire at it, then get next target if torpedoes are available
        while self.sub.getTotalInTubes(foreOrAft) != 0 and notFiredAtAllShips:
            target = self.getTarget(ship)
            if target == 0:
                break
            target = target - 1

            self.sub.subSupplyPrintout(True, foreOrAft)
            # if steam torpedoes are available, ask how many to fire, otherwise / then ask how many electric to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7a") > 0:
                # get num of steam torpedoes to fire
                G7aFire = getInputNum("Fire how many G7a torpedoes? ", 0, self.sub.getTotalInTubes(foreOrAft, "G7a"))
                ship[target].fireG7a(G7aFire)
                for x in range(G7aFire):
                    self.sub.fireTorpedo(foreOrAft, "G7a")
                    self.G7aFired += 1
            # if electric torpedoes are available, ask how many to fire
            if self.sub.getTotalInTubes(foreOrAft, "G7e") > 0:
                # get num of electric torpedoes to fire
                G7eFire = getInputNum("Fire how many G7e torpedoes? ", 0, self.sub.getTotalInTubes(foreOrAft, "G7e"))
                ship[target].fireG7e(G7eFire)
                for x in range(G7eFire):
                    self.sub.fireTorpedo(foreOrAft, "G7e")
                    self.G7eFired += 1
            if foreOrAft == "Forward":
                self.firedForward = True
            elif foreOrAft == "Aft":
                self.firedAft = True
            else:
                self.firedForward = True
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
                if self.firedForward and self.firedAft and self.sub.knightsCross == 0:
                    rollMod += 1
                if ship[s].G7aINCOMING > 0:
                    THstring = "Roll to hit " + ship[s].name + " (" + str(r) + "-): "
                    printRollandMods(THstring, torpRoll, rollMod)
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
                                    self.damageDone += 4
                                case 2:
                                    print("Critical damage! (3)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(3)
                                    self.damageDone += 3
                                case 3:
                                    print("Serious damage! (2)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(2)
                                    self.damageDone += 2
                                case _:
                                    print("Minor damage! (1)")
                                    ship[s].removeG7a()
                                    ship[s].takeDamage(1)
                                    self.damageDone += 1
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
                    THstring = "Roll to hit " + ship[s].name + " (" + str(r) + "-): "
                    printRollandMods(THstring, torpRoll, rollMod)
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
                                    self.damageDone += 4
                                case 2:
                                    print("Critical damage! (3)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(3)
                                    self.damageDone += 3
                                case 3:
                                    print("Serious damage! (2)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(2)
                                    self.damageDone += 2
                                case _:
                                    print("Minor damage! (1)")
                                    ship[s].removeG7e()
                                    ship[s].takeDamage(1)
                                    self.damageDone += 1
                            time.sleep(3)
                    else:
                        print("Torpedo Missed.")
                        ship[s].removeG7e()
                        time.sleep(3)

            if ship[s].sunk:
                print(ship[s].name, "has been sunk!")
                self.shipsSunk.append(ship[s])
                self.shipsSunkOnCurrentPatrol.append(ship[s])
                if "Minelaying" not in self.currentOrders and "Abwehr" not in self.currentOrders:
                    self.missionComplete = True
                time.sleep(2)

    def deckGunAttack(self, ship, r):
        """Attack called (already assumed to have at least one shot) for deck guns."""
        printTargetShipList(ship)
        self.sub.subSupplyPrintout(False, "Deck Gun")

        target = self.getTarget(ship)

        target = target - 1

        #get how many shots to fire (1 or 2)- automatically fire 1 if only 1 shot remaining
        if self.sub.deck_gun_ammo == 1:
            shots = 1
        else:
            shots = getInputNum("Number of shots to fire (1 or 2) ", 1, 2)

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

            THstring = "Roll to hit " + ship[target].name + " (" + str(r) + "-): "
            printRollandMods(THstring, gunRoll, rollMod)
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
                self.damageDone += damage
            else:
                print("Deck gun missed!")
            self.sub.deck_gun_ammo -= 1

        self.firedDeckGun = True
        if ship[target].sunk:
            print(ship[target].name, "has been sunk!")
            self.shipsSunkOnCurrentPatrol.append(ship[target])
            self.shipsSunk.append(ship[target])
            if "Minelaying" not in self.currentOrders and "Abwehr" not in self.currentOrders:
                self.missionComplete = True
        time.sleep(2)

mainMenu()