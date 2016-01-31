from loadJSON import openJSON
from paths import JSON

CONST_SPACE = openJSON(JSON.Directory+"CONST.JSON")
locals().update(CONST_SPACE)