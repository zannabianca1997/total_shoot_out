from random import randrange, randint, uniform, choice
from CONSTS import *
from Arena import Arena
from Navicella import Navicella
from Asteroids import Asteroid
from PowerUPs import PowerUp
from life_bar import life_bar
from paths import JSON, Sprite
from loadJSON import read_astdata, read_navdata, read_pwrup
from os import listdir

import pygame
from pygame.locals import * #Key consts

class Game:
    """The complete game class"""

    def create_screen(self):
        if not CONST_SPACE['FULLSCREEN']:
            self.screen = pygame.display.set_mode(WINDOW_DIMENSION)
        else:
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)


    def precalculate_values(self):
        self.WINNING_FONT = pygame.font.Font(pygame.font.match_font(WINNING_FONT),WINNING_FONT_SIZE)
        self.WINNING_FONT.set_bold(WINNING_FONT_BOLD)
        
        screen_rect =  self.screen.get_rect()
        self.WINDOW_DIMENSION = (screen_rect.width, screen_rect.height)
        
        self.LIFE_BARS_WIDTH = int(self.WINDOW_DIMENSION[0]*LIFE_BAR_WIDTH_FRACTION)

        
        self.GAME_WINDOWS_DIMENSION = (self.WINDOW_DIMENSION[0] - (self.LIFE_BARS_WIDTH * 2),self.WINDOW_DIMENSION[1])
        self.SCREEN_CENTER = (self.WINDOW_DIMENSION[0]//2,self.WINDOW_DIMENSION[1]//2)

    def charge_astdata(self):
        if ASTEROIDS:
            astfiles=[ filename for filename in listdir(JSON.Asteroids) if filename[-5:] == ".JSON" and (filename[0] != "~" or DEBUG)]
            self.ASTEROIDS = [ read_astdata(astfile)  for astfile in astfiles]
        else:
           self.ASTEROIDS = []

    def charge_powerUps(self):
        if POWER_UPS:
            pwrfiles= [ filename for filename in listdir(JSON.PowerUps) if filename[-5:] == ".JSON" and (filename[0] != "~" or DEBUG)]
            self.POWER_UPS = [ read_pwrup(pwrfile) for pwrfile in pwrfiles]
        else:
            self.POWER_UPS = []

    def charge_NavData(self):
        navfiles = [ filename for filename in listdir(JSON.Navi) if filename[-5:] == ".JSON" and (filename[0] != "~" or DEBUG)]
        self.NAV_DATAS = [ read_navdata(navfile) for navfile in navfiles]

    def charge_screens(self):
        backfiles=[ Sprite.Sfondi + filename for filename in listdir(Sprite.Sfondi) ]
        self.backgrounds = [pygame.transform.scale(pygame.image.load(backfile), self.WINDOW_DIMENSION)
                            for backfile in backfiles]


    def __init__(self):
        #creating clock
        self.clock = pygame.time.Clock()
        #creating screen
        self.create_screen()
        #precalculate values
        self.precalculate_values()
        #creating game screens
        self.game_screen = pygame.Surface(self.GAME_WINDOWS_DIMENSION,SRCALPHA)
        self.game_screen_rect = pygame.Rect((self.LIFE_BARS_WIDTH,0),self.GAME_WINDOWS_DIMENSION)
        #charging datas from json
        self.charge_astdata()
        #creating power_ups list
        self.charge_powerUps()
        #creating nav datas
        self.charge_NavData()
        #charging screens
        self.charge_screens()

    def Play(self, options):
        playing = True

        #Variables

        #keys values
        keys = {
            "Kd_kp4" : False,
            "Kd_kp6" : False,
            "Kd_kp8" : False,
            "Kd_kp0" : False,
            "Kd_renter" : False,
    
            "Kd_a" : False,
            "Kd_d" : False,
            "Kd_w" : False,
            "Kd_space" : False,
            "Kd_lcontrol" : False,
        }

        #choosing background
        background = self.backgrounds[options["background"]]
        #create arena
        arena = Arena(self.screen, self.game_screen_rect )
        #creating a contestualized copy of the variables
        asteroids, power_ups, nav_datas = self.get_dinamic_lists(arena)
        #creating navs
        navs = self.create_navs(options, nav_datas)
        #create life bars
        life_bar1, life_bar2 = self.create_life_bars(navs)
        #set no winner
        self.winner = 3

        while playing:
            #event gestor
            for e in pygame.event.get():
                playing = self.process(e, keys)

            timepassed = self.clock.tick(MAX_FPS)

            self.spawn(timepassed, arena, asteroids, power_ups)
            self.guide(navs, keys)

            self.screen.blit(background,(0,0))

            arena.Timer.Frame(timepassed) #qui fa tutto

            life_bar1.Paint(self.screen)
            life_bar2.Paint(self.screen)

            if self.winner == 3: #nessuno è ancora morto
                pygame.display.flip()
            else:
                playing = False
                self.GameOver()


    def create_navs(self, choosen_nav, nav_datas):
        init_data_1 = nav_datas[choosen_nav["nav1"][0]].copy()
        init_data_1['metadata']["name"] = choosen_nav["nav1"][1]
        init_data_1['player'] = 1
        init_data_2 = nav_datas[choosen_nav["nav2"][0]].copy()
        init_data_2['metadata']["name"] = choosen_nav["nav2"][1]
        init_data_2['player'] = 2
        return (Navicella(init_data_1), Navicella(init_data_2))

    def process(self, e, keys):
        """process an event"""
        if e.type == pygame.QUIT: return False
        elif e.type == pygame.KEYDOWN:
            if e.key == K_KP4: keys['Kd_kp4'] = True
            elif e.key == K_KP6: keys['Kd_kp6'] = True
            elif e.key == K_KP8: keys['Kd_kp8'] = True
            elif e.key == K_KP0: keys['Kd_kp0'] = True
            elif e.key == K_KP_ENTER: keys['Kd_renter'] = True
            elif e.key == K_a: keys['Kd_a'] = True
            elif e.key == K_d: keys['Kd_d'] = True
            elif e.key == K_w: keys['Kd_w'] = True
            elif e.key == K_SPACE: keys['Kd_space'] = True
            elif e.key == K_LCTRL: keys['Kd_lcontrol'] = True
            elif e.key == K_ESCAPE: return False  # exit game
        elif e.type == pygame.KEYUP:
            if e.key == K_KP4: keys['Kd_kp4'] = False
            elif e.key == K_KP6: keys['Kd_kp6'] = False
            elif e.key == K_KP8: keys['Kd_kp8'] = False
            elif e.key == K_KP0: keys['Kd_kp0'] = False
            elif e.key == K_KP_ENTER: keys['Kd_renter'] = False
            elif e.key == K_a: keys['Kd_a'] = False
            elif e.key == K_d: keys['Kd_d'] = False
            elif e.key == K_w: keys['Kd_w'] = False
            elif e.key == K_SPACE: keys['Kd_space'] = False
            elif e.key == K_LCTRL: keys['Kd_lcontrol'] = False
        return True

    def get_dinamic_lists(self, arena):
        "copy list and set arena"
        asteroids = []
        for ASTEROID in self.ASTEROIDS:
            asteroid = ASTEROID.copy()
            asteroid['arena'] = arena
            asteroids.append(asteroid)
        power_ups = []
        for POWER_UP in self.POWER_UPS:
            power_up = POWER_UP.copy()
            power_up['arena'] = arena
            power_ups.append(power_up)
        nav_datas = []
        for NAV_DATA in self.NAV_DATAS:
            nav_data = NAV_DATA.copy()
            nav_data['arena'] = arena
            nav_data['game'] = self
            nav_datas.append(nav_data)
        return (asteroids, power_ups, nav_datas)

    #SPAWNING
    def SpawnAsteroid(self, arena, ast_type):
        rect = ast_type["sprite"].get_rect()
        if randint(0,1):
            pos=(-rect.width//2,
                 randrange(-rect.height//2 + arena.dimension.top, rect.height//2 + arena.dimension.bottom))
        else:
            pos=(randrange(-rect.width//2 + arena.dimension.left, rect.width//2 + arena.dimension.right)
                 ,-rect.height//2)
        ast_data = ast_type.copy()
        ast_data["position"] = pos
        Asteroid(ast_data)

    def SpawnPwrUp(self, arena, pwr_up):
        PowerUp(pwr_up.copy())

    def spawn(self, timepassed, arena, asteroids, power_ups):
        if len(asteroids) <= MAX_ASTEROIDS:
            for asteroid in asteroids:
                if uniform(0,1) > asteroid['spawn_rate'] ** timepassed:
                    self.SpawnAsteroid(arena,asteroid)
        for pwr_up in power_ups:
            if uniform(0,1) > pwr_up['spawn_rate'] ** timepassed:
                self.SpawnPwrUp(arena,pwr_up)

    def guide(self, navs, keys):
        navs[0].accelerating = keys["Kd_w"]
        navs[0].turning = keys["Kd_a"] - keys["Kd_d"]
        navs[0].shooting = keys["Kd_space"] or keys["Kd_lcontrol"]

        navs[1].accelerating = keys["Kd_kp8"]
        navs[1].turning = keys["Kd_kp6"] - keys["Kd_kp4"]
        navs[1].shooting = keys["Kd_kp0"] or keys["Kd_renter"]

    def create_life_bars(self, navs):
        return (life_bar(navs[0],(0,0,self.LIFE_BARS_WIDTH,self.WINDOW_DIMENSION[1]),COLOR_1),
                life_bar(navs[1],(self.WINDOW_DIMENSION[0]-self.LIFE_BARS_WIDTH,0,
                                  self.WINDOW_DIMENSION[0],self.WINDOW_DIMENSION[1]),COLOR_2))

    def GameOver(self):
        if self.winner == 0:
            color = DRAW_COLOR
            renderstring = "It's a draw"
        else:
            if self.winner == 1:
                color = COLOR_1
            else:
                color = COLOR_2
            renderstring = 'Player '+str(self.winner)+' Won!'
        wintext = self.WINNING_FONT.render(renderstring,1,color)
        rect = wintext.get_rect()
        rect.center = self.SCREEN_CENTER
        self.screen.blit(wintext,rect)
        pygame.display.flip()
        event = pygame.event.wait()
        while event.type != pygame.QUIT and not (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            event = pygame.event.wait()

    def died(self, player):
        self.winner -= player

