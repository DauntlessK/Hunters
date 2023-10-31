#Kyle Breen-Bondie - Hunters: Uboat Board Game Recreation
import random
import os

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
            case "VIIB":
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
        self.crew_level = 1  # 0=green, 1=trained, 2=veteran, 3=elite
        self.crew1 = 0
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


def d6Roll():
    roll = random.randint(0, 5) + 1
    return roll
def d6Rollx2():
    roll = d6Roll() + d6Roll()
    return roll

def advanceTime():
    """Moves time forward one month and checks for end of game if beyond June 1943"""
    Game.date_month += 1
    if Game.date_month == 12:
        Game.date_month = 0
        Game.date_year += 1
    if Game.date_month >= 6 & Game.date_year > 43:
        gameover()

def getTime():
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    year = str(Game.date_year)
    toReturn = Game.month[Game.date_month] + " / " + year
    return toReturn

class Game():

    def __init__(self):
        self.month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        self.date_month = 0
        self.date_year = 1939
        print("Welcome to The Hunters: German U-Boats at War, 1939-43")
        print("First choose a Submarine:")
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
        self.patrol = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
                  "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
                  "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth"]
        self.patrolNum = 1
        self.randomEvent = False
        self.currentLocationStep = 0
        self.onStationSteps = self.sub.patrol_length
        self.gameloop()

    def getMonth(self):
        return self.date_month
    def getYear(self):
        return self.date_year
    def getFullDate(self):
        toReturn = self.month[self.date_month] + " - " + str(self.date_year)
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
                return "VIIC"
            case "6" | "VIID":
                self.date_month = 0
                self.date_year = 1942
                return "VIID"
            case "7" | "VIIC Flak":
                self.date_month = 4
                self.date_year = 1943
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
                        #TODO SELECT PATROL
                    else:
                        self.getPatrol(self.date_month, self.date_year, d6Roll(), self.sub.getType())
        else:
            self.getPatrol(self.date_month,self.date_year,d6Roll(),self.sub.getType())
        print("Patrol Assignment:", self.currentOrders)
        depart = "U-" + self.id + " departs port early before dawn for" + self.rank + " " + self.kmdt + "'s " + self.patrol[self.patrolNum]
        print(depart)
        self.currentLocationStep = 1


    def getPatrol(self,month,year,roll,subClass):
        if year == 1939 or (month <= 2 and year == 1940):           #1939 - Mar 1940
            with open("PatrolChart1.txt", "r") as fp:
                lines = fp.readlines()
                orders = lines [roll-2]
        elif month > 2 and month <= 5 and year == 1940:             #1940 - Apr - Jun
            with open("PatrolChart2.txt", "r") as fp:
                lines = fp.readlines()
                orders = lines[roll - 2]
        elif month > 5 and month <= 11 and year == 1940:            #1940 - Jul - Dec
            with open("PatrolChart3.txt", "r") as fp:
                lines = fp.readlines()
                orders = lines[roll - 2]

        #deal with changes in orders based on uboat type
        if orders == "Mediterranean" or orders == "Artic" and (subClass == "IXA" or subClass == "IXB"):
            orders = "West African Coast"
        if orders == "West African Coast" or orders == "Caribbean" and (
                subClass == "VIIA" or subClass == "VIIB" or subClass == "VIIC"):  # VII Cannot patrol west africa
            orders = "Atlantic"
        if orders == "British Isles" and subClass == "VIID":
            orders = "British Isles (Minelaying)"
        ##TODO: deal with VIID and VIIC Flak boats not being allowed in med
        self.currentOrders = orders

    def gameloop(self):
        self.startPatrol()
        getEncounter(getLocation(self.currentOrders,self.currentLocationStep,self.onStationSteps), self.randomEvent)


def gameover():
    print("GAMEOVER!")

def getEncounter(loc,randomEvent):
    roll = d6Rollx2()
    print("Roll for location", loc, "-", roll)
    if roll == 12 and randomEvent == False:                 #First check if random event (natural 12)
        return "Random Event"
    match loc:
        case "Transit":                                     #Transit encounter chart
            match roll:
                case 2 | 3:
                    return "Aircraft"
                case 12:
                    return "Ship"
                case _:
                    return "-"
        case "Arctic":                                      #Artic encounter chart
            match roll:
                case 2:
                    return "Capital Ship"
                case 3:
                    return "Ship"
                case 6 | 7 | 8:
                    return "Convoy"
                case 12:
                    return "Aircraft"
                case _:
                    return "-"
        case "Atlantic":                                    #Atlantic encounter chart
            if roll == 2:
                return "Capital Ship"
            elif roll == 3:
                return "Ship"
            elif roll == 6 or roll == 7 or roll == 9 or roll == 12:
                return "Convoy"
            else:
                return "-"
        case "British Isles":                               #British Isles encounter chart
            if roll == 2:
                return "Capital Ship"
            elif roll == 5 or roll == 8:
                return "Ship"
            elif roll == 6:
                return "Ship + Escort"
            elif roll == 10:
                return "Convoy"
            elif roll == 12:
                return "Aircraft"
            else:
                return "-"
        case "Caribbean":                                    # Carribean encounter chart
            if roll == 2 or roll == 12:
                return "Aircraft"
            elif roll == 4 or roll == 8:
                return "Ship"
            elif roll == 6:
                return "Two Ships + Escort"
            elif roll == 9 or roll == 10:
                return "Tanker"
            else:
                return "-"
        case "Mediterranean":                                # Mediterranean encounter chart
            if roll <= 3 or roll >= 11:
                return "Aircraft"
            elif roll == 4:
                return "Capital Ship"
            elif roll == 7:
                return "Ship"
            elif roll == 8:
                return "Convoy"
            elif roll == 10:
                return "Two Ships + Escort"
            else:
                return "-"

def getLocation(patrol,step,onStationLeft):
    """Gets current location box to determine encounter (transit, Atlantic, etc)"""
    #TODO wolfpacks?

    if step == 1 and (patrol == "Norway" or patrol == "Artic"):
        return "Transit"
    elif step == 1:
        return "Bay of Biscay"

    if step == 2 and patrol == "Mediterranean":
        return "Gibraltar Passage"
    elif step == 2:
        return "Transit"

    if step == 3 and (patrol == "North America" or patrol == "Caribbean"):
        return "Transit"
    elif step == 3 and ("Minelaying" in patrol or "Abwehr" in patrol):
        return "Mission"
    elif step == 3:
        return patrol




#Game()
#getPatrol(9,1940,9, "IXA")

test = getEncounter("Arctic",False)
print(test)