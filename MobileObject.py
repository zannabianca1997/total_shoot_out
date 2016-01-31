#libraries
from math import *
from Actor import Actor
from Vec2d import Vec2d
import pygame

#a container for variables and metods of every mobile object
class MobileObject (Actor):
    """An actors that moves"""

    __DEFAULT_PARAM = {"speed": (0,0), "drag": 0, "rotation": 0, "turn_drag":0.0, "facing_direction": 0.0}



    """def __init__(self, arena, position : Vec2d, sprite: pygame.Surface,
                 speed = (0,0), drag = 0, rotation = 0.0, turn_drag = 0.0, facing_direction = 0.0 ):"""
    def __init__(self,init_data):
        super().__init__(init_data)

        self.image = self.sprite

        for i in self.__DEFAULT_PARAM:
            if (not (i in self.__dict__)):
                self.__dict__[i] = self.__DEFAULT_PARAM[i]

        if not isinstance(self.speed,Vec2d):
            self.speed = Vec2d(self.speed)

        self.direction_changed() #rotate image

    def Frame(self, timepassed):
        """Phisic simulating: object moves, shoot, do stuff"""
        self.move(timepassed)
        
    def direction_changed(self):
        "call this every time facing_direction is changed"
        if self.facing_direction != 0:
            self.sprite = pygame.transform.rotate(self.image,-self.facing_direction*180/pi)
        else:
            self.sprite = self.image

    def get_move_direction(self):
        return self.speed.angle

    def move(self,timepassed):
        self.speed -= self.speed * self.drag * timepassed
        self.position += self.speed * timepassed

        self.rotation -= self.rotation * self.turn_drag * timepassed
        self.facing_direction += self.rotation * timepassed
        self.direction_changed()

        if not self.inArena():
            self._out_of_arena()

    def inArena(self):
        "l'oggetto è dentro l'arena"
        return (self.position.x > self.arena.dimension.left and
                self.position.x < self.arena.dimension.right and
                self.position.y > self.arena.dimension.top and
                self.position.y < self.arena.dimension.bottom )

    def _out_of_arena(self):
        "called whe object exit the arena"
        pass
