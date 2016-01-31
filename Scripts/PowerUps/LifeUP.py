obj.life += obj.max_life * LIFE_UP_FRACTION
if obj.life > obj.max_life:
    obj.life = obj.max_life