import random
from operator import *
from util import *

class Aircraft():
    type = ""

    def __init__(self):

        with open("aircraft.txt", "r") as fp:
            lines = fp.readlines()
            entry = lines[random.randint(0, 17)]
            self.type = entry
            self.type = self.type.strip(('\n'))

    def getType(self):
        return type