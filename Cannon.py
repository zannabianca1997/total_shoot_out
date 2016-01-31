#libraries
from math import *
from Vec2d import Vec2d
from paths import Sprite
from Bullet import Bullet
from CONSTS import *

#the cannon
class Cannon:

    def __init__(self, cannon_data):
        self.__dict__.update( cannon_data )

        self.type = self.type.copy()

        self.type['sprite'] =  self.type["sprite"+str(self.parent.player)]
        self.type['parent'] = self.parent #bullet won't kill home ship
        self.type['arena'] = self.parent.arena

        self.calc_pos()

        #Se stai tentando di togliere questo codice per l'ennesima volta,
        # ricorda che i cannoni sparano a ritmo differente..
        #
        # times_i_tried_to_take_it_down =  4
        self.parent.arena.Timer.set_event(self.shoot, # va ripetuto, perchè contimua a sparare
                                          self.type['shoot_rate'],
                                          self.type['shoot_rate'])

    def Dispose(self):
        self.parent.arena.Timer.unset_event(self.shoot) #non ripeterlo piu'

    def calc_pos(self):
        self.pos = self.rel_pos.rotated(self.parent.facing_direction)#posizione rispetto alla nave
        #mo calcoliamo i proiettili
        self.type['facing_direction'] = self.parent.facing_direction + self.rel_direction
        self.type["speed"] = Vec2d.versor(self.type['facing_direction']) * self.type['launch_speed']


    def shoot(self, time: int):
        if self.parent.shooting:
            bullet_data = self.type.copy()
            bullet_data['speed'] += self.parent.speed
            bullet_data['position'] = self.parent.position + self.pos
            Bullet(bullet_data)