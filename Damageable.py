#libraries
from WeightedObject import WeightedObject
from CONSTS import *


class DamageableObject (WeightedObject):
    def __init__(self, init_data):

        super().__init__(init_data)

        self.life = self.max_life

    def damage(self,value):
        self.life -= value
        if self.life < 0:
            self.Die()

    def takeimpulse(self, impulse, damage = True):
        super().takeimpulse(impulse)
        if damage:
            self.damage( COLLISION_COST * impulse.length )

    def Die(self):
        self.Dispose()