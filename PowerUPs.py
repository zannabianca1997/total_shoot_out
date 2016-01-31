#libraries
from pygame.image import load

from paths import Sprite
from Actor import Actor
from Navicella import Navicella
from CONSTS import *


class PowerUp (Actor):

    def __init__(self, init_data):
        super().__init__(init_data)
        self.arena.AddPwu(self)
        self.arena.Timer.set_event(self.timeouted,self.timeout)

    def Collide(self,other):
        if type(other) is Navicella:
            safe_space = CONST_SPACE.copy()
            safe_space.update(self.CONST) #json defined const
            safe_space['obj'] = other #deve modificarlo, no?

            exec(self.function,{},safe_space) #execute code ... (safe??) NO

            self.Dispose()

    def timeouted(self,time):
        self.Dispose()

    def Dispose(self):
        self.arena.RmvPwu(self)
        super().Dispose()