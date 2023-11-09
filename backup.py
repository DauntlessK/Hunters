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