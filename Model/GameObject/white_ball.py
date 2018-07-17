# from Model.GameObject.utils import Vec
from pygame.math import Vector2 as Vec
import Model.const as modelConst
import View.const as viewConst
from Model.GameObject.body import Body 
import random

class White_Ball(object):
    def __init__(self, pos = Vec(-1,-1), following = False, target = -1, index = -1):
        self.following = following
        self.target = target
        self.index = index
        if target != -1:
            self.age = viewConst.whiteBallGenerationTime + 1
        else:
            self.age = 0
        if index == -1:
            self.color = viewConst.wbColor
        else:
            self.color = viewConst.playerColor[index]
        self.speed = modelConst.wb_speed
        self.radius = modelConst.wb_radius
        if pos == Vec(-2, -2) :
        	randpos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        	screen_mid = Vec( viewConst.ScreenSize[1]/2, viewConst.ScreenSize[1]/2 )
        	while (randpos - screen_mid).length_squared() < modelConst.init_no_wb_r ** 2:
        		randpos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        	self.pos = randpos
        elif pos == Vec(-1, -1) :
            #random init the position of balls
            self.pos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        else:
            #use the pos passed in
            self.pos = Vec(pos)

    def update(self, player_list):
        self.age += 1
        if not self.following:
            return True
        else:
            if not player_list[self.target].is_alive:
                return False
            targetobj = player_list[self.target].body_list[-1]
            targetpos = targetobj.pos_log[0]
            steps = (targetpos - self.pos).length() / self.speed
            multiplier = 3 if player_list[self.target].is_dash else 1
            if (self.pos - targetpos).length_squared() < (self.speed * (1 + steps/2/30) * multiplier) ** 2:
                player_list[targetobj.index].body_list.append(Body(player_list[targetobj.index].body_list[-1],self.index == -1))
                return False
            else:
                direction = (targetpos - self.pos).normalize()
                self.pos += direction * self.speed * (1 + steps/2/30) * multiplier
                return True



