import random
import os
import time
from operator import *
from util import *

class Ship():
    """A ship (freighter, tanker, warships or escort. Has a type, class, damage, HP and other things to track"""
    type = ""  # small freighter, large freighter, tanker, warship or capital ship
    hp = 0
    damage = 0
    name = ""
    GRT = 0
    clss = ""
    sunk = False


    def __init__(self, type, shipsSunk, month, year, loc=""):
        self.type = type
        self.G7aINCOMING = 0
        self.G7eINCOMING = 0
        self.dateSunk = ""
        self.monthSunk = month
        self.yearSunk = year

        notUniqueShip = True
        while notUniqueShip:
            match self.type:
                case "Small Freighter":
                    self.damage = 0
                    self.hp = 2
                    self.sunk = False
                    self.clss = type
                    with open("Small Freighter.txt", "r") as fp:
                        lines = fp.readlines()
                        if loc == "North America":
                            entry = lines[random.randint(101, 120)]
                        else:
                            entry = lines[random.randint(1, 100)]
                        entry = entry.split("-")
                        self.name = entry[0]
                        self.GRT = int(entry[1])

                case "Large Freighter" | "Tanker":
                    with open(f"{type}.txt", "r") as fp:
                        lines = fp.readlines()
                        if loc == "North America":
                            entry = lines[
                                random.randint(101, 120)]
                        else:
                            entry = lines[
                                random.randint(1, 100)]
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
                        self.hp = 4
                        self.damage = 0
                        self.sunk = False

                case "Capital Ship":
                    with open("Capital Ship.txt", "r") as fp:
                        lines = fp.readlines()
                        entry = lines[random.randint(1, 10)]
                        entry = entry.split("#")
                        self.name = entry[0]
                        self.clss = entry[1]
                        self.GRT = int(entry[2])
                        self.hp = 5
                        self.damage = 0
                        self.sunk = False

            #ensure ship is unique
            if len(shipsSunk) == 0:
                notUniqueShip = False
            for x in range(len(shipsSunk)):
                if shipsSunk[x].name == self.name:
                    continue
                else:
                    notUniqueShip = False

    def __str__(self):
        s = self.name + " (" + self.clss + " [" + str(self.GRT) + " GRT])"
        return s

    def fireG7a(self, num):
        """Adds a steam torpedo to the ship's incoming type. Helps keep track of how many to roll against."""
        self.G7aINCOMING = self.G7aINCOMING + num

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
