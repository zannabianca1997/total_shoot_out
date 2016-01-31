class Assets:
    Directory = "./assets/"

    __Asteroids = "Asteroids/"
    __Navi = "Navi/"
    __Cannons = __Navi + "Cannons/"
    __PowerUps = "PowerUps/"

    __Sfondi = "Sfondi/"

class Sprite:
    Directory = Assets.Directory + "Sprite/"

    Asteroids = Directory + Assets._Assets__Asteroids
    Navi = Directory + Assets._Assets__Navi
    Cannons = Directory + Assets._Assets__Cannons
    PowerUps = Directory + Assets._Assets__PowerUps
    Sfondi = Directory + Assets._Assets__Sfondi

class JSON:
    Directory = Assets.Directory + "JSON/"

    Asteroids = Directory + Assets._Assets__Asteroids
    Navi = Directory + Assets._Assets__Navi
    Cannons = Directory + Assets._Assets__Cannons
    PowerUps = Directory + Assets._Assets__PowerUps

class Scripts:
    Directory = "./Scripts/"

    PowerUps = Directory + Assets._Assets__PowerUps





