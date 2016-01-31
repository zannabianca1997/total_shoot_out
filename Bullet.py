#libraries
from MobileObject import MobileObject
from WeightedObject import WeightedObject
from Damageable import DamageableObject

#a bullet
class Bullet (MobileObject):
    def __init__(self, init_data):
        super().__init__(init_data)
        self.arena.AddBul(self)

    def Collide(self,other):
        if (other != self.parent):
            if issubclass(type(other),WeightedObject):
                if issubclass(type(other),DamageableObject) and (other != self.parent or self.friendly_fire): #bullet won't hit mothership
                    other.damage(self.damage)
                    other.takeimpulse(self.impulse * self.speed, False)
                else:
                    other.takeimpulse(self.impulse * self.speed)
                self.Dispose()
        super().Collide(other)

    def _out_of_arena(self):
        self.Dispose()
        super()._out_of_arena()

    def Dispose(self):
        self.arena.RmvBul(self)
        super().Dispose()