from pygame import Rect
from pygame.draw import rect

class life_bar:
    """a simple bar"""

    def __init__(self,obj,rect,color, bkcolor = (0,0,0), vertical = True):
        self.rect = Rect(rect)
        self.obj = obj
        self.color = color
        self.bkcolor = bkcolor

        if vertical:
            self.delta = float(self.rect.height) / self.obj.max_life
            self.__get_dimension = self.__get_vertical_dimension
        else:
            self.delta = float(self.rect.width) / self.obj.max_life
            self.__get_dimension = self.__get_orizontal_dimension
    
    def __get_vertical_dimension(self):
        return (self.rect.width,self.delta * self.obj.life)

    def __get_orizontal_dimension(self):
        return (self.delta * self.obj.life,self.rect.height)

    def Paint(self,surface):
        #rect(surface,self.bkcolor,self.rect) # se lo schermo non si refresha da solo
        rect(surface,self.color,Rect(self.rect.topleft,self.__get_dimension()))


