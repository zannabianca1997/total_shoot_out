#libraries
from math import *
from Damageable import DamageableObject
from random import uniform
from Arena import Arena
from CONSTS import *

#the asteroids
class Asteroid (DamageableObject):
    def __init__(self,init_data):
        # gli asteroidi hanno limiti sulla velocità iniziale.
        Asteroid.set_ast_data(init_data)
        super().__init__(init_data)

        self.arena.AddAct(self)

    @staticmethod
    def set_ast_data(init_data):
        if not ('speed' in init_data):  # se non hanno specificato niente
            init_data['facing_direction'] = uniform(0, 2 * pi)
            newspeed = uniform(init_data["start_speed_range"][0], init_data["start_speed_range"][1])
            init_data['speed'] = (cos(init_data['facing_direction']) * newspeed,
                                  - sin(init_data['facing_direction']) * newspeed)
        if not ('rotation' in init_data):
            init_data['rotation'] = uniform(init_data['start_rotation_range'][0],init_data['start_rotation_range'][1])
        init_data['restitution'] = ASTEROID_RESTITUTION

    def _out_of_arena(self):
        super()._out_of_arena()
        if uniform(0,1) < ASTEROIDS_DESPAWN_PROB: #a volte se ne vanno
            self.Dispose()
        else:
            Arena.wrap_to_arena(self)

    def Dispose(self):
        self.arena.RmvAct(self)
        super().Dispose()