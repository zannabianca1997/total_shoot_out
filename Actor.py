from Vec2d import Vec2d
from random import randrange
from CONSTS import *
if DEBUG and DEBUG_CIRCLES:
    from pygame import draw

class Actor:
    """A random object"""
    
    def __init__(self, init_data : dict):
        self.__dict__.update( init_data )

        if not ('position' in init_data):
            self.position = Vec2d(randrange(self.arena.dimension.left, self.arena.dimension.right),
                                  randrange(self.arena.dimension.top, self.arena.dimension.bottom))
        elif not isinstance(self.position,Vec2d):
            self.position = Vec2d(self.position)

        self.ID = self.arena.getID()
        self._calc_rect() #needed for radius
        self.radius = max(self.rect.height, self.rect.width) // 2

        self.disposed = False

    def _calc_rect(self):
        self.rect = self.sprite.get_rect()
        self.rect.center = self.position
        self.rect_clipped = self.rect.clip(self.arena.dimension)
        self.sprite_rect = self.rect_clipped.move(- self.rect.left, - self.rect.top)

    def Frame(self,timepassed: int):
        """Phisic simulating: object moves, shoot, do stuff"""
        pass

    def Check_collide(self, other : "Actor") -> bool :
        """Check the collision with another object"""
        return (self.position-other.position).get_length_sqrd() < \
               (self.radius + other.radius) ** 2
                    #all objects are circles!! 

    def  Collide(self,other : "Actor"):
        """Collide with some other actor"""
        pass

    def Paint(self):
        """Paint the object on the surface"""
        self._calc_rect()
        if DEBUG and DEBUG_CIRCLES:
            draw.circle(self.arena.surface, (100,100,100), self.position.IntVec(), self.radius)
        self.arena.surface.blit(self.sprite, self.rect_clipped, self.sprite_rect)

    def Dispose(self):
        """The object is being erased"""
        self.disposed = True

    def dist_from(self,other : "Actor"):
        """get the distance from two Actors"""
        return (self.position - other.position).length

    def __eq__(self, other):
        return self.ID == other.ID