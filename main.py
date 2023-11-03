#Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os
import time

class Submarine():
    """Player's Submarine"""

    def __init__(self,subClass):
        self.subClass = subClass   # submarine type (IE: VIIC)

        match subClass:
            case "VIIA":
                self.patrol_length = 3              # number of spaces during patrols
                self.hull_hp = 7                    # total hull damage before sinking
                self.flooding_hp = 7                # total flooding damage before surfacing
                self.G7a = 6                        # default load of G7a steam torpedoes
                self.G7e = 5                        # default load of G7e electric torpedoes
                self.forward_tubes = 4              # number of forward torpedo tubes
                self.aft_tubes = 1                  # number of aft torpedo tubes
                self.torpedo_type_spread = 1        # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10             # current ammo for deck gun
                self.deck_gun_cap = 10              # sub's deck gun ammo capacity
                self.reserves_aft = 0               # number of aft torpedo roloads
            case "VIIB" | "VIIC":
                self.patrol_length = 4              # number of spaces during patrols
                self.hull_hp = 8                    # total hull damage before sinking
                self.flooding_hp = 8                # total flooding damage before surfacing
                self.G7a = 8                        # default load of G7a steam torpedoes
                self.G7e = 6                        # default load of G7e electric torpedoes
                self.forward_tubes = 4              # number of forward torpedo tubes
                self.aft_tubes = 1                  # number of aft torpedo tubes
                self.torpedo_type_spread = 3        # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 10             # current ammo for deck gun
                self.deck_gun_cap = 10              # sub's deck gun ammo capacity
                self.reserves_aft = 1               # number of aft torpedo reloads
            case "IXA":
                self.patrol_length = 5              # number of spaces during patrols
                self.hull_hp = 8                    # total hull damage before sinking
                self.flooding_hp = 8                # total flooding damage before surfacing
                self.G7a = 12                       # default load of G7a steam torpedoes
                self.G7e = 10                       # default load of G7e electric torpedoes
                self.forward_tubes = 4              # number of forward torpedo tubes
                self.aft_tubes = 2                  # number of aft torpedo tubes
                self.torpedo_type_spread = 4        # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 5              # current ammo for deck gun
                self.deck_gun_cap = 5               # sub's deck gun ammo capacity
                self.reserves_aft = 2               # number of aft torpedo reloads
            case "IXB":
                self.patrol_length = 6              # number of spaces during patrols
                self.hull_hp = 8                    # total hull damage before sinking
                self.flooding_hp = 9                # total flooding damage before surfacing
                self.G7a = 12                       # default load of G7a steam torpedoes
                self.G7e = 10                       # default load of G7e electric torpedoes
                self.forward_tubes = 4              # number of forward torpedo tubes
                self.aft_tubes = 2                  # number of aft torpedo tubes
                self.torpedo_type_spread = 4        # plus/minus of steam / electric torpedo mix
                self.deck_gun_ammo = 5              # current ammo for deck gun
                self.deck_gun_cap = 5               # sub's deck gun ammo capacity
                self.reserves_aft = 2               # number of aft torpedo reloads

            #TODO VIID, VIIC Flak


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

        # states are: 0=operational, 1=damaged, 2=inoperational
        self.e_engine1 = 0  # state of electric engine 1
        self.e_engine2 = 0  # state of electric engine 2
        self.d_engine1 = 0  # state of diesel engine 1
        self.d_engine2 = 0  # state of diesel engine 2
        self.periscope = 0
        self.radio = 0
        self.hydrophones = 0
        self.batteries = 0
        self.fwd_torp_doors = 0
        self.aft_torp_doors = 0
        self.dive_planes = 0
        self.fuel_tanks = 0
        self.deck_gun = 0
        self.flak_gun = 0

        # crew states & ranks
        self.crew_level = 1  # 0=green,  1=trained,  2=veteran,  3=elite
        self.crew1 = 0       # 0=fine,   1=lw        2=sw        4=kia
        self.crew2 = 0
        self.crew3 = 0
        self.crew4 = 0
        self.WO1_level = 0
        self.WO1 = 0
        self.WO2_level = 0
        self.WO2 = 0
        self.eng_level = 0
        self.eng = 0
        self.doc_level = 0
        self.doc = 0
        self.kmdt = 0

    def getType(self):
        return self.subClass

    def torpedoResupply(self):
        #TODO Resupply for minelaying missions (remove tubes and replace with mines)
        print("Submarine Resupply - You are given ", self.G7a, "(steam) and ", self.G7e, "(electric) torpedoes.")
        print("You can adjust this ratio by ", self.torpedo_type_spread, "torpedo(es).")
        SA = -1
        while SA < 0 or SA > self.torpedo_type_spread:
            print("Current # of steam torpedoes to add. 0 -", self.torpedo_type_spread)
            SA = int(input())
        self.G7a = self.G7a + SA
        self.G7e = self.G7e - SA
        if SA == 0: #if player did not add steam and remove electrics
            SE = -1
            while SE < 0 or SE > self.torpedo_type_spread:
                print("Current # of electric torpedoes to add. 0 -", self.torpedo_type_spread)
                SE = int(input())
            self.G7a = self.G7a - SE
            self.G7e = self.G7e + SE

        #ask player how many steam torpedoes to load forward
        f1 = -1
        print("Number of forward tubes: ", self.forward_tubes)
        while f1 < 0 or f1 > self.forward_tubes:
            f1 = int(input("Enter # of  G7a steam torpedoes to load in the forward tubes: "))
        self.forward_G7a = f1
        self.forward_G7e = self.forward_tubes - f1

        #ask player how many steam torpedoes to load aft
        f2 = -1
        print("Number of aft tubes: ", self.aft_tubes)
        while f2 < 0 or f2 > self.aft_tubes:
            f2 = int(input("Enter # of G7a steam torpedoes to load in the aft torpedo tube(s): "))
        self.aft_G7a = f2
        self.aft_G7e = self.aft_tubes - f2

        #ask player how many steam torpedoes for aft reserve(s)
        if self.reserves_aft > 0 and self.G7a - f1 - f2 > 0:
            print("Remaining G7a steam topedoes: ", self.G7a - f1 - f2)
            f3 = -1
            while f3 < 0 or f3 > self.aft_tubes:
                f3 = int(input("Enter # of G7a to load into the aft reserves."))
            self.reloads_aft_G7a = f3
            self.reloads_aft_G7e = self.reserves_aft - f3
        elif self.G7a == 0 and self.reserves_aft > 0:      #if there are no steam & aft reserves, fill with electrics
            self.aft_G7e = self.reserves_aft

        self.reloads_forward_G7a = self.G7a - self.forward_G7a - self.aft_G7a - self.reloads_aft_G7a  # number of reloads forward of G7a
        self.reloads_forward_G7e = self.G7e - self.forward_G7e - self.aft_G7e - self.reloads_aft_G7e

        self.deck_gun_ammo = self.deck_gun_cap

    def subSupplyPrintout(self):
        #print("Forward Tubes:", self.forward_tubes, "G7a:", self.forward_G7a, "G7e:", self.forward_G7e)
        #print("Forward Reserves:  G7a:", self.reloads_forward_G7a, "G7e:", self.reloads_forward_G7e)
        #print("Aft Tubes:", self.aft_tubes, "G7a:", self.aft_G7a, "G7e:", self.aft_G7e)
        #print("Aft Reserves:  G7a:", self.reloads_aft_G7a, "G7e:", self.reloads_aft_G7e)

        print("Forward- G7a:", self.forward_G7a, "/", self.reloads_forward_G7a, "G7e:", self.forward_G7e, "/", self.reloads_forward_G7e)
        print("Aft- G7a:", self.aft_G7a, "/", self.reloads_aft_G7a, "G7e:", self.aft_G7e, "/",
              self.reloads_aft_G7e)
        print("Deck Gun Ammo:", self.deck_gun_ammo, "/", self.deck_gun_cap)

    def crewKnockedOut(self):
        if self.crew1 > 1 and self.crew2 > 1 and self.crew3 > 1 and self.crew4 > 1:
            return True
        else:
            return False

class Ship():
    type = ""   #small freighter, large freighter, tanker, warship or capital ship
    hp = 0
    damage = 0
    name = ""
    GRT = 0
    sunk = False

    def __init__(self, type):
        self.type = type

        match self.type:
            case "Small Freighter":
                self.hp = 2
                self.damage = 0
                self.sunk = False
            case "Large Freighter":



def d6Roll():
    roll = random.randint(1, 6)
    return roll
def d6Rollx2():
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
        self.rank = ["Oberleutnant zur See", "Kapitän-leutnant", "Korvetten-kapitän", "Fregatten-kapitän", "Kapitän zur See"]
        self.rankMod = 0
        self.establishFirstRank()
        self.sub.subSupplyPrintout()
        print("---------------")
        print("Guten Tag,", self.rank[self.rankMod], "- The date is", self.getFullDate())
        self.currentOrders = ""
        self.patrolCount = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
                  "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
                  "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth"]
        self.patrolNum = 1
        self.randomEvent = False
        self.currentLocationStep = 0
        self.onStationSteps = self.sub.patrol_length
        self.patrolLength = 0
        self.gameloop()

    def getMonth(self):
        return self.date_month
    def getYear(self):
        return self.date_year
    def getFullDate(self):
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

    def getTime(self):
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        year = str(Game.date_year)
        toReturn = Game.month[Game.date_month] + " / " + year
        return toReturn

    def establishFirstRank(self):
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

    def startPatrol(self):
        if self.rankMod > 0:
            print("PATROL ASSIGNMENT: Roll to choose next patrol? Y/N")
            np = input()
            match np:
                case "Yes" | "Y" | "y" | "yes":
                    roll = d6Roll()
                    print("Die roll:", roll)
                    if roll <= self.rankMod:
                        print("You may select your patrol.")
                        self.getPatrol(self.date_month, self.date_year, d6Roll(), self.sub.getType(), True)
                    else:
                        self.getPatrol(self.date_month, self.date_year, d6Roll(), self.sub.getType(), False)
        else:
            self.getPatrol(self.date_month,self.date_year,d6Roll(),self.sub.getType(), False)
        print("Patrol Assignment:", self.currentOrders)
        depart = "U-" + str(self.id) + " departs port early before dawn for " + self.rank[
            self.rankMod] + " " + self.kmdt + "'s " + str(self.patrolCount[self.patrolNum] + " patrol.")
        print(depart)
        self.currentLocationStep = 1
        self.patrolLength = self.getPatrolLength(self.currentOrders)

    def getPatrolLength(self, patrol):
        match patrol:
            case "North America" | "Caribbean":
                return self.sub.patrol_length + 8 #NA patrol has normal 2 BoB + 2 transits + extra 4 transits
            case _:
                return self.sub.patrol_length + 4

    def pickPatrol(self):
        #TODO open correct patrol chart and prompt response from user of those choices MAYBE NOT NEEDED
        print("TODO")

    def getPatrol(self, month, year, roll, subClass, pickingPatrol):
        if year == 1939 or (month <= 2 and year == 1940):           #1939 - Mar 1940
            with open("PatrolChart1.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    input = ("Pick your orders (Case-sensitive): ")
                    orders = input
                else:
                    orders = lines [roll-2]
        elif month > 2 and month <= 5 and year == 1940:             #1940 - Apr - Jun
            with open("PatrolChart2.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    input = ("Pick your orders (Case-sensitive): ")
                    orders = input
                else:
                    orders = lines[roll - 2]
        elif month > 5 and month <= 11 and year == 1940:            #1940 - Jul - Dec
            with open("PatrolChart3.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    input = ("Pick your orders (Case-sensitive): ")
                    orders = input
                else:
                    orders = lines[roll - 2]
        ##TODO add other date patrol charts and txt files

        orders = self.validatePatrol(orders)

        #change time on station (onStationSteps) by one less if North American Orders
        if orders == "North America" or orders == "Caribbean":
            self.onStationSteps = self.sub.patrol_length - 1
        elif "Minelaying" in orders or "Abwehr" in orders:
            self.onStationSteps = self.sub.patrol_length - 1
        else:
            self.onStationSteps = self.sub.patrol_length

        #strip any stray returns that may have gotten into the orders string
        orders = orders.strip('\n')

        self.currentOrders = orders

    def validatePatrol(self, orders):
        """Deal with changes in orders based on U-Boat type"""
        if orders == "Mediterranean" or orders == "Artic" and (self.subClass == "IXA" or self.subClass == "IXB"):
            orders = "West African Coast"
        if orders == "West African Coast" or orders == "Caribbean" and (
                self.subClass == "VIIA" or self.subClass == "VIIB" or self.subClass == "VIIC"):  # VII Cannot patrol west africa
            orders = "Atlantic"
        if orders == "British Isles" and self.subClass == "VIID":
            orders = "British Isles (Minelaying)"

        #deal with permanent stations
        if self.permMedPost:
            orders == "Mediterranean"
        if self.permArcPost:
            orders == "Arctic"

        return orders
        ##TODO: deal with VIID and VIIC Flak boats not being allowed in med (reroll req)

    def gameloop(self):
        self.startPatrol()
        self.patrol()
        self.portReturn()

    def patrol(self):
        """Full patrol loop accounting for leaving porn, transiting, patrolling and returning"""

        if self.currentOrders == "Arctic":   #if Artic patrol, roll to see if permanently assigned to Arctic
            if d6Roll() <= 3:
                print("You've been assigned permanently to the Arctic.")
                self.permArcPost = True

        while self.currentLocationStep <= self.getPatrolLength(self.currentOrders):

            currentBox = self.getLocation(self.currentOrders, self.currentLocationStep)
            #if sub is patrolling area (not in transit)
            if currentBox == self.currentOrders:
                self.onStationSteps -= 1
            self.getEncounter(currentBox, self.date_year, self.randomEvent)

            #end of loop - go to next box of patrol
            self.currentLocationStep += 1

        if self.currentOrders == "Mediterranean":   #if it was a Med patrol, set U boat permanently to Med
            self.permMedPost = True

    def portReturn(self):
        print("You've made it home!")


    def getLocation(self, patrol, step):
        """Gets current location box to determine encounter (transit, Atlantic, etc)"""
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
            return "Random Event"

        #determine if this is a mission box to roll against mission
        if (loc == "British Isles (Minelaying)" or loc == "British Isles (Abwehr Agent Delivery)") and self.currentLocationStep == 3:
            loc = "Mission"
        if loc == "North America (Abwehr Agent Delivery)" and self.currentLocationStep == 5:
            loc = "Mission"


        match loc:
            case "Transit":  # Transit encounter chart
                match roll:
                    case 2 | 3:
                        #aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 12:
                        #ship
                        print("Ship")
                        self.encounterAttack()
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Arctic":  # Artic encounter chart
                match roll:
                    case 2:
                        print("Capital Ship")
                    case 3:
                        print("Ship")
                    case 6 | 7 | 8:
                        print("Convoy")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Atlantic":  # Atlantic encounter chart
                match roll:
                    case 2:
                        print("Capital Ship")
                    case 3:
                        print("Ship")
                    case 6 | 7 | 9 | 12:
                        print("Convoy")
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "British Isles":  # British Isles encounter chart
                match roll:
                    case 2:
                        print("Capital Ship")
                    case 5 | 8:
                        print("Ship")
                    case 6:
                        print("Ship + Escort")
                    case 10:
                        print("Convoy")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Caribbean":  # Carribean encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 4 | 8:
                        print("Ship")
                    case 6:
                        print("Two Ships + Escort")
                    case 9 | 10:
                        return "Tanker"
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Mediterranean":  # Mediterranean encounter chart
                match roll:
                    case 2 | 3 | 11 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 4:
                        print("Capital Ship")
                    case 7:
                        print("Ship")
                    case 8:
                        print("Convoy")
                    case 10:
                        print("Two Ships + Escort")
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "North America":  # North American encounter chart
                match roll:
                    case 2:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 4 | 6:
                        print("Ship")
                    case 5:
                        print("Two Ships + Escort")
                    case 8:
                        print("Two Ships")
                    case 9 | 12:
                        print("Tanker")
                    case 11:
                        print("Convoy")
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Norway":  # Norway encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 3 | 11:
                        print("Capital Ship")
                    case 4 | 9 | 10:
                        print("Ship + Escort")
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "Spanish Coast":  # Spanish Coast encounter chart
                match roll:
                    case 2 | 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case 5:
                        print("Ship + Escort")
                    case 6 | 7:
                        print("Ship")
                    case 10 | 11:
                        print("Convoy")
                    case _:
                        #no encounter
                        self.encounterNone(loc)
            case "West African Coast":  # West African Coast encounter chart
                match roll:
                    case 2:
                        print("Capital Ship")
                    case 3 | 7:
                        print("Ship")
                    case 6 | 10:
                        print("Convoy")
                    case 9:
                        print("Ship + Escort")
                    case 12:
                        # aircraft
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case _:
                        #no encounter
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
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case _:
                        #no encounter
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
                        self.encounterAircraft(self.sub, self.date_year, self.currentOrders)
                    case _:
                        #no encounter
                        self.encounterNone(loc)

    ##----------------------------------------------- PATROL BOXES (TO DETERMINE WHICH ENCOUNTER TO ROLL)

    def patrolBoxTransit(self):
        if self.currentLocationStep == 1 and (self.currentOrders == "Artic" or self.currentOrders == "Norway"):
            print("Your U-Boat sails North towards its patrol area.")
        elif self.onStationSteps > 0:
            print("Your U-Boat sails on towards its assigned patrol area.")
        else:
            print("Your U-Boat turns around and heads for home.")
        self.getEncounter(self.getLocation(self.currentOrders, self.currentLocationStep), self.date_year, self.randomEvent)

    def patrolBoxBayOfBiscay(self):
        print("Your U-Boat transits across the perilous Bay of Biscay.")
        self.getEncounter(self.getLocation(self.currentOrders, self.currentLocationStep), self.date_year, self.randomEvent)


    ##----------------------------------------------- ENCOUNTERS

    def encounterNone(self, loc):
        randResult = random.randint(0, 2)
        match loc:
            case "Transit":
                print("You have an uneventful transit.")
            case "Bay of Biscay":
                print("You cross the Bay of Biscay without issues.")
            case "Mission":
                #TODO ?
                print("Mission")
            case "Arctic" | "Norway":
                match randResult:
                    case 0:
                        print("You spot nothing in this section of your frigid patrol.")
                    case 1:
                        print("Inclement weather ensures you find nothing on this part of your patrol.")
                    case 2:
                        print("This part of your Northern patrol is uneventful.")
            case "Atlantic":
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
                        print("Nasty storms reduce visibility to nothing - ensuring you find nothing on this part of your patrol.")
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
                        print("A timely storm pushes several patrolling ships off station, allowing you to run straight through Gibraltar.")
            case "Additional Round of Combat":
                #TODO
                print("TODO")
        time.sleep(2)


    def encounterAircraft(self, sub, year, patrolType):
        print("ALARM! Aircraft in sight! Rolling to crash dive!")
        roll = d6Rollx2()
        drm = 0

        if sub.crew_level == 0:
            drm -= 1
        elif sub.crew_level == 3:
            drm += 1
        if sub.crewKnockedOut():
            drm -= 1
        if sub.dive_planes > 0:
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

        total = roll + drm
        print("Roll:", roll, "• Modifiers:", drm, "| MODIFIED ROLL:", total)

        if total <= 1:
            print("TWO ATTACKS!")
        elif total <= 5:
            print("One attack!")
        else:
            print("Successful crash dive!")

        time.sleep(2)

    def encounterAttack(self, enc):
        tgt = []
        if enc == "Ship":
            tgt[1] = getShip()

    def getShip():
        shipType = d6Roll()

        if


def gameover():
    print("GAMEOVER!")








Game()
