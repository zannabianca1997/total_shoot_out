#libraries
from MobileObject import MobileObject
from PhisicEngine import PhisicEngine
from math import *

class WeightedObject (MobileObject):
    def __init__(self, init_data):

        WeightedObject.set_weight(init_data)
        super().__init__(init_data)

    @staticmethod
    def set_weight(init_data):
        if (not ('restitution' in init_data)):
            init_data['restitution'] = 1
        if init_data['weight'] != -1:  # -1 is infinite mass
            if init_data['weight'] != 0:
                init_data['inverseweight'] = (1 / init_data['weight'])
            else:
                init_data['inverseweight'] = None
        else:
            init_data['inverseweight'] = 0

    def takeimpulse(self, impulse):
        self.speed += impulse * self.inverseweight