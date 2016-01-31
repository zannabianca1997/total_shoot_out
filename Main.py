import pygame
from Game import Game
from CONSTS import *

#inizializing pygame
pygame.init()

game = Game()
if DEBUG:
    conf = {"nav1" : (1, "zannaShip"),"nav2" : (1, "yourShip"), "background" : 6}
else:
    conf = {"nav1" : (0, "zannaShip"),"nav2" : ( 0, "yourShip"), "background" : 6}
game.Play(conf)

pygame.quit()
