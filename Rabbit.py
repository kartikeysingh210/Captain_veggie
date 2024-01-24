from Creature import Creature

class Rabbit(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, "R")
