#libraries
from math import *
from Vec2d import Vec2d
from Damageable import DamageableObject
from Cannon import Cannon
from Arena import Arena
from CONSTS import *
#A ship
class Navicella (DamageableObject):
    def __init__(self,init_data):

        init_data['sprite'] = init_data["sprite" + str(init_data['player'])]
        init_data['restitution'] = NAVICELLA_RESTITUTION

        self.cannons = [] #init will call direction_changed, that will recalculate the cannons. so they must be initializated here

        super().__init__(init_data)

        self.shooting = False
        self.accelerating = False
        self.turning = 0 # -1,0,1

        self.max_level = len(self.upgrades) - 1
        self.level = 0
        self.direction_changed()

        self.arena.AddAct(self)

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level
        for cannon in self.cannons:
            cannon.Dispose()
        self.cannons = []
        for gun in self.upgrades[level]:
            cannon_data = self.available_cannons[gun]
            cannon_data['parent'] = self
            self.cannons.append(Cannon(cannon_data))

    
    def direction_changed(self):
        super().direction_changed()
        self.onWard_versor = Vec2d.versor(self.facing_direction)
        self.recalculate_cannon()

    def recalculate_cannon(self):
        for cannon in self.cannons:
            cannon.calc_pos()

    #move with accelerations
    def move(self,timepassed):
        if self.accelerating:
            self.accelerate(timepassed)
        if self.turning != 0:
            self.turn(timepassed)
        super().move(timepassed)

    #comandi

    def turn(self,timepassed):
        self.rotation += self.turning * self.turn_speed * timepassed

    def accelerate(self,timepassed):
        self.speed += self.onWard_versor * self.acceleration * timepassed

    def Die(self):
        self.game.died(self.player)
        super().Die()

    def Dispose(self):
        for cannon in self.cannons:
            cannon.Dispose()
        super().Dispose()

    def _out_of_arena(self):
        super()._out_of_arena()
        Arena.wrap_to_arena(self)
            
            
