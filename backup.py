#if first leg of patrol
            if self.currentLocationStep == 1 and (self.currentOrders == "Arctic" or self.currentOrders == "Norway"):
                print("Your U-Boat sails North.")
                print(getEncounter(getLocation(self.currentOrders, self.currentLocationStep, self.onStationSteps),
                                   self.randomEvent))
            elif self.currentLocationStep == 1:
                print("Your U-Boat transits across the perilous Bay of Biscay.")
                encounter = getEncounter(getLocation(self.currentOrders, self.currentLocationStep, self.onStationSteps), self.date_year,
                                   self.randomEvent)
                match encounter:
                    case "-":
                        print("Uneventful Passage.")
                    case _:
                        encounterAircraft(self.sub, self.date_year, self.currentOrders)

            #if on second leg...
            elif self.currentLocationStep == 2:
                if "Abwehr" in self.currentOrders or "Minelaying" in self.currentOrders:
                    print("Your U-Boat continues on to approach the mission area.")
                else:
                    print("Your U-boat continues on to approach the designated patrol area.")
                encounterAircraft(self.sub, self.date_year, self.currentOrders)

            #advance patrol to next leg
            self.currentLocationStep += 1



            -------------------

if step >= 3 and self.onStationSteps > 0 and (patrol == "North America" or patrol == "Caribbean"):
    return "Transit"
elif step == 3 and ("Minelaying" in patrol or "Abwehr" in patrol):
    return patrol
elif step >= 3 and self.onStationSteps > 0:
    return patrol
elif step == self.patrolLength and (patrol == "Norway" or patrol == "Artic"):
    return "Transit"
elif step == self.patrolLength:
    return "Bay of Biscay"
# elif step == self.getPatrolLength() - 1 and patrol:
else:
    print("ERROR GETTING LOCATION BOX")



    def getTime(self):
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        year = str(Game.date_year)
        toReturn = Game.month[Game.date_month] + " / " + year
        return toReturn


        if year == 1939 or (month <= 2 and year == 1940):  # 1939 - Mar 1940
            with open("PatrolChart1.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    inp = input("Pick your orders (Case-sensitive): ")
                    orders = inp
                else:
                    orders = lines[roll - 2]
        elif month > 2 and month <= 5 and year == 1940:  # 1940 - Apr - Jun
            with open("PatrolChart2.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    inp = input("Pick your orders (Case-sensitive): ")
                    orders = inp
                else:
                    orders = lines[roll - 2]
        elif month > 5 and month <= 11 and year == 1940:  # 1940 - Jul - Dec
            with open("PatrolChart3.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    inp = input("Pick your orders (Case-sensitive): ")
                    orders = inp
                else:
                    orders = lines[roll - 2]
        elif month > 5 and month <= 11 and year == 1940:  # 1940 - Jul - Dec
            with open("PatrolChart4.txt", "r") as fp:
                lines = fp.readlines()
                if pickingPatrol:
                    print(lines)
                    inp = input("Pick your orders (Case-sensitive): ")
                    orders = inp
                else:
                    orders = lines[roll - 2]

                    case
                    "batteries":
                    print("Our batteries have taken a hit!")
                    if self.batteries == 0:
                        self.batteries = 1
                        self.damagedList["Batteries"] = 1
                case
                "periscope":
                print("Our periscope has been damaged!")
                if self.periscope == 0:
                    self.periscope = 1
                    self.damagedList["Periscope"] = 1
            case
            "dive_planes":
            print("Our batteries have taken a hit!")
            if self.dive_planes == 0:
                self.dive_planes = 1
                self.damagedList["Dive Planes"] = 1
        case
        "e_engine1":
        print("Eletric Engine #1 has been incapacitated!")
        if self.e_engine1 == 0:
            self.e_engine1 = 1
            self.damagedList["Electric Engine #1"] = 1


    case
    "e_engine2":
    print("Eletric Engine #2 has been knocked out!")
    if self.e_engine2 == 0:
        self.e_engine2 = 1
        self.damagedList["Dive Planes"] = 1
case
"d_engine1":
print("Diesel Engine #1 has been damaged!")
if self.d_engine1 == 0:
    self.d_engine1 = 1
case
"d_engine2":
print("Diesel Engine #2 has been hit!")
if self.d_engine2 == 0:
    self.d_engine2 = 1
case
"flak_guns":
print("Flak guns have been hit!")
if self.large_flak == 0:
    self.large_flak = 1
if self.flak_gun == 0:
    self.flak_gun = 1
case
"large_flak":
print("3.7mm flak gun damage!")
if self.large_flak == 0:
    self.large_flak = 1
case
"minor":
print("Minor damage. No damage to major systems.")
case
"deck_gun":
print("The deck gun has been knocked out!")
if self.deck_gun == 0:
    self.deck_gun = 1
case
"radio":
print("Our radio has been smashed!")
if self.radio == 0:
    self.radio = 1
case
"hydrophones":
print("The hydrophones has been incapacitated!")
if self.hydrophones == 0:
    self.hydrophones = 1
case
"aft_torp_doors":
print("The aft torpedo doors are jammed shut!")
if self.aft_torp_doors == 0:
    self.aft_torp_doors = 1
case
"fwd_torp_doors":
print("The forward torpoedo tubes have been damaged!")
if self.fwd_torp_doors == 0:
    self.fwd_torp_doors = 1
case
"fuel_tanks":
print("A fuel tank has been hit! We are leaking fuel!")
if self.fuel_tanks == 0:
    self.fuel_tanks = 1