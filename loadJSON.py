import json
from paths import JSON, Sprite, Scripts
from pygame.image import load
from Vec2d import Vec2d

def openJSON(name):
    json_string = open(name,"r").read()
    return json.loads(json_string)

def read_navdata(nav_file):
    navdata = openJSON(JSON.Navi + nav_file)
    navdata["sprite1"] = load(Sprite.Navi + navdata["sprite1"])
    navdata["sprite2"] = load(Sprite.Navi + navdata["sprite2"])
    for cannon in navdata["available_cannons"].values():
        cannon["rel_pos"] = Vec2d(cannon["rel_pos"]['x'], cannon["rel_pos"]['y'])

        cannon["type"] = openJSON( JSON.Cannons + cannon["type"] + '.JSON') #reading cannon datas
        cannon["type"]["sprite1"] = load(Sprite.Cannons + cannon["type"]["sprite1"])
        cannon["type"]["sprite2"] = load(Sprite.Cannons + cannon["type"]["sprite2"])
    return navdata

def read_astdata(ast_file):
    astdata = openJSON(JSON.Asteroids + ast_file )
    astdata['sprite'] = load( Sprite.Asteroids + astdata['sprite'])
    if astdata['spawn_rate'] != 0:
        astdata['spawn_rate'] =  (0.5 ** (1/astdata['spawn_rate'])) #precalculating probability for milliseconds
    else:
        astdata['spawn_rate'] = 1
    return astdata

def read_pwrup(pwrup_file):
    pwrupdata = openJSON(JSON.PowerUps + pwrup_file )
    pwrupdata['sprite'] = load( Sprite.PowerUps + pwrupdata['sprite'])
    if pwrupdata['spawn_rate'] != 0:
        pwrupdata['spawn_rate'] = (0.5 ** (1/pwrupdata['spawn_rate'])) #precalculating probability for milliseconds
    else:
        pwrupdata['spawn_rate'] = 1
    with open(Scripts.PowerUps + pwrupdata['function']) as f:
        pwrupdata['function'] = compile(f.read(),pwrup_file,"exec") #compiling function
    return pwrupdata

