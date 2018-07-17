import Model.const as modelConst
from pygame.math import Vector2 as Vec
import View.const as viewConst
class Bullet(object):
    def __init__(self, pos,direction,index, radius = modelConst.bullet_radius,\
                 speed = modelConst.bullet_speed0, acc = modelConst.bullet_a):
        self.pos = Vec(pos)
        self.index = index
        if self.index == -1:
            self.color = viewConst.Color_Black
        else:
            self.color = viewConst.playerColor[index]
        self.direction = Vec(direction)
        self.radius = radius
        self.speed = speed
        self.age = viewConst.bulletFlickerCycle
        self.acc = acc
        if self.acc == 0:
            self.is_flash = False
        else:
            self.is_flash = True
    def update(self):
        '''
        return:
            True: update success
            False: update failed
        '''

        ########## collide with walls ###########
        if (self.direction.x > 0 and self.pos.x+self.radius >= viewConst.ScreenSize[1] - modelConst.eps) \
            or (self.direction.x < 0 and self.pos.x-self.radius <= -modelConst.eps):
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y+self.radius >= viewConst.ScreenSize[1] - modelConst.eps) \
            or (self.direction.y < 0 and self.pos.y-self.radius <= -modelConst.eps):
            self.direction.y *= -1
        
        self.pos += self.direction * self.speed
        self.speed -= self.acc
        if self.index != -1:
            self.age += 1
        if self.speed <= 0 and self.radius > modelConst.bigbullet_r * 1.1:
            return None
        return self.speed > 0

    
