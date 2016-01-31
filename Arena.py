from Timer import Timer
from CONSTS import *
from PhisicEngine import PhisicEngine
from pygame.rect import Rect
from pygame.surface import Surface

class Arena:
    """the game fiels"""

    def __init__(self,surface : Surface, dimension:Rect = None ):
        if dimension == None:
            dimension = surface.get_rect()

        self.surface = surface
        self.dimension = dimension

        self.__IDCounter = 0

        self.actors = []
        self.bullets = []
        self.power_ups = []

        self.Timer = Timer()

        self.Timer.subscribe(self.Simulate)
        self.Timer.subscribe(self.Paint)

    def Simulate(self, timepassed):
        for actor in self.actors:
            actor.Frame(timepassed)
            if not actor.disposed:
                for other_actor in self.actors:
                    if (other_actor != actor) and actor.Check_collide(other_actor):
                        PhisicEngine.Collided(actor, other_actor)
                        actor.Collide(other_actor)
                        other_actor.Collide(actor)
        for bullet in self.bullets:
            bullet.Frame(timepassed)
            if not bullet.disposed:
                for actor in self.actors:
                    if bullet.Check_collide(actor):
                        actor.Collide(bullet)
                        bullet.Collide(actor)
        for power_up in self.power_ups:
            power_up.Frame(timepassed)
            if not power_up.disposed:
                for actor in self.actors:
                    if power_up.Check_collide(actor):
                        actor.Collide(power_up)
                        power_up.Collide(actor)

    def Paint(self,timepassed):
        for actor in self.actors:
            actor.Paint()
        for bullet in self.bullets:
            bullet.Paint()
        for power_up in self.power_ups:
            power_up.Paint()

    def AddAct(self,Actor):
        self.actors.append(Actor)
    def AddBul(self,Bullet):
        self.bullets.append(Bullet)
    def AddPwu(self,PowerUp):
        self.power_ups.append(PowerUp)

    def RmvAct(self,Actor):
        if Actor in self.actors:
            self.actors.remove(Actor)
    def RmvBul(self,Bullet):
        if Bullet in self.bullets:
            self.bullets.remove(Bullet)
    def RmvPwu(self,PowerUp):
        if PowerUp in self.power_ups:
            self.power_ups.remove(PowerUp)

    def getID(self):
        self.__IDCounter += 1
        return (self.__IDCounter - 1)
    
    @staticmethod
    def wrap_to_arena(obj):
        if obj.position.x < obj.arena.dimension.left:
            obj.position.x = obj.arena.dimension.right
        elif obj.position.x > obj.arena.dimension.right:
            obj.position.x = obj.arena.dimension.left
        if obj.position.y < obj.arena.dimension.top:
            obj.position.y = obj.arena.dimension.bottom
        elif obj.position.y > obj.arena.dimension.bottom:
            obj.position.y = obj.arena.dimension.top