import Model.const as modelconst
import View.const as viewconst
import random
from math import pi, sin, cos, atan2
from pygame.math import Vector2 as Vec
# from pygame.math import Vec2d as Vec
from Model.GameObject.white_ball import White_Ball
from Model.GameObject.body import Body 
from Model.GameObject.bullet import Bullet
from Model.GameObject.item import Item

class Head(object):
    def __init__(self, index, name = "player", is_AI = False, Score = 0):
        # basic data
        self.name = name
        self.index = index
        self.is_AI = is_AI
        self.color = viewconst.playerColor[index]
        screen_mid = Vec( viewconst.ScreenSize[1]/2, viewconst.ScreenSize[1]/2 )

        #up down left right
        self.pos = screen_mid + modelconst.init_r * modelconst.Vec_dir[self.index]        
        self.theta = index * (pi/2)
        self.direction = Vec( cos(self.theta), -sin(self.theta) )
        
        #information
        self.speed = modelconst.normal_speed
        self.is_dash = False
        self.dash_timer = 0
        self.dash_cool=0
        self.radius = modelconst.head_radius
        self.is_alive = True
        self.score = Score
        self.body_list = [self]
        self.is_ingrav = False
        self.is_circling = True
        self.circling_radius = modelconst.init_r
        self.ori = 1
        self.init_timer = 200
        self.have_multibullet = False
        self.have_bigbullet = False
        self.always_multibullet = False
        self.always_bigbullet = False
        #if in grav
        self.grav_center = Vec( 0, 0 )
        self.pos_log = [Vec(self.pos)]

        self.is_rainbow = False

    def update(self,player_list, wb_list, bullet_list, item_list, score_list, tmp_score_list):
        if not self.is_alive:
            return 0

        self.pos += self.direction * self.speed
        
        if self.is_circling:
            self.theta += self.speed / self.circling_radius * self.ori
            #print(self.theta, self.speed/self.circling_radius)
            self.direction = Vec( cos(self.theta), -sin(self.theta) )
        if self.init_timer != -1:
            self.init_timer -= 1
        if self.init_timer > 0:
            return 0
        elif self.init_timer == 0:
            self.is_circling = False
            self.init_timer = -1

        #update pos log
        self.pos_log.append(Vec(self.pos))
        if len(self.pos_log) > modelconst.pos_log_max :
            self.pos_log.pop(0)
        
        #is in circle
        self.is_ingrav=False
        for i in modelconst.grav :
            if ( self.pos - i[0] ).length_squared() < i[1]**2 :
                self.is_ingrav = True
                self.grav_center = i[0]

        #collision with wall
        if (self.direction.x > 0 and self.pos.x + self.radius > viewconst.ScreenSize[1]-modelconst.eps) \
            or (self.direction.x < 0 and self.pos.x - self.radius < 0 - modelconst.eps) :
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y + self.radius > viewconst.ScreenSize[1]-modelconst.eps) \
            or (self.direction.y < 0 and self.pos.y - self.radius < 0 - modelconst.eps) :
            self.direction.y *= -1
        
        #collision with white ball
        for i in range(len(wb_list)-1,-1,-1):
            wb = wb_list[i]
            if wb.following:
                continue
            if (self.pos - wb.pos).length_squared() < (self.radius + wb.radius)**2 :

                wb_list.append(White_Ball(Vec(wb.pos),True,self.index))
                wb_list.pop(i)

        #collision with competitor's body and bullet
        tmp = False
        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index :
                    continue
                for j in enemy.body_list[1:]:
                    if (self.pos - j.pos).length_squared() < (self.radius + j.radius)**2 :
                        #self die
                        killer = enemy.index
                        self.is_alive = False
                        tmp = True
                        self.add_score(player_list,score_list,tmp_score_list)
                        break
                else:
                    continue
                break
            for bullet in bullet_list :
                if (bullet.index != self.index) and \
                   (self.pos - bullet.pos).length_squared() < (self.radius + bullet.radius)**2 :
                    killer = bullet.index
                    self.is_alive = False
                    if tmp == False:
                        self.add_score(player_list,score_list,tmp_score_list)
                    break
        ##player die
        if not self.is_alive:
            self.is_dash = True
            while len(self.body_list) > 1:
                if killer != -1 and player_list[killer].is_alive:
                    wb_list.append(White_Ball(Vec(self.body_list[-1].pos),True,killer))
                    #player_list[killer].body_list.append(Body(player_list[killer].body_list[-1]))
                self.body_list.pop(-1)

            return 1
        #collision with competitor's head
        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index or enemy.is_dash == True:
                    continue
                if (self.pos - enemy.pos).length_squared() < (self.radius + enemy.radius)**2 :
                    rrel = enemy.pos - self.pos
                    if (self.direction - enemy.direction).dot(rrel) > 0:
                        self.direction.reflect_ip(rrel)
                        enemy.direction.reflect_ip(rrel)
                        self.is_circling = False
                        enemy.is_circling = False
        
        #collision with item
        cnt = 0
        for i in player_list:
            if i.is_alive:
                cnt += 1
        if cnt != 1:
            for i in range(len(item_list)-1,-1,-1):
                item = item_list [ i ]
                if ( self.pos - item.pos ).length_squared() < (self.radius + item.radius)**2 :
                    item.trigger(self.index,player_list,wb_list)
                    item_list.pop(i)
        #dash timer
        if self.is_dash:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.is_dash = False
                #self.speed = modelconst.normal_speed
        # dash cool
        if self.dash_cool>0:
            self.dash_cool-=1
        #update theta
        #self.theta = atan2(self.direction.x, -self.direction.y)
        for j in range(1, len(self.body_list)):
                self.body_list[j].update()

        if self.is_rainbow:
            self.rainbow_mode()
        return 0
    def click(self, bullet_list, wb_list) :
        if not self.is_alive:
            return
        if self.init_timer != -1:
            return
        if not self.is_dash:
            if self.is_circling or self.is_ingrav:
                self.is_circling = (not self.is_circling)
                if self.is_circling:
                    self.circling_radius = (self.pos - self.grav_center).length()
                    ori = self.direction.cross(self.pos - self.grav_center)
                    if ori > 0: #counterclockwise
                        self.theta = atan2( self.pos.y - self.grav_center.y , -self.pos.x + self.grav_center.x ) - pi / 2
                        self.direction = Vec( cos(self.theta) , - sin(self.theta) )
                        self.ori = 1
                    else:
                        self.theta = atan2( self.pos.y - self.grav_center.y , -self.pos.x + self.grav_center.x ) + pi / 2
                        self.direction = Vec( cos(self.theta) , - sin(self.theta) )
                        self.ori = -1
                else:
                    self.circling_radius = 0

            elif self.dash_cool==0:
                self.is_dash = True
                self.dash_timer = modelconst.max_dash_time * modelconst.dash_speed_multiplier
                self.dash_cool=self.dash_timer+modelconst.dash_cool
                #self.speed = modelconst.dash_speed
                if len(self.body_list)>1 :
                    self.body_list.pop(-1)
                    if self.always_multibullet or self.have_multibullet:
                        bullet_list.append(Bullet(self.pos,self.direction,self.index))
                        bullet_list.append(Bullet(self.pos,self.direction.rotate(30),self.index))
                        bullet_list.append(Bullet(self.pos,self.direction.rotate(-30),self.index))
                        self.have_multibullet = False
                    elif self.always_bigbullet or self.have_bigbullet:
                        bullet_list.append(Bullet(self.pos,self.direction,self.index,modelconst.bigbullet_r))
                        self.have_bigbullet = False
                    else:
                        bullet_list.append(Bullet(self.pos,self.direction,self.index))

    def add_score(self, player_list, score_list,tmp_score_list):
        for enemy in player_list:
            if enemy.index == self.index:
                continue
            else :
                if enemy.is_alive:
                    score_list[enemy.index] += 1
                    tmp_score_list[enemy.index] += 1

    def blast(self, bullet_list):
        for i in range(len(self.body_list)-1,0,-1):
            cb = self.body_list[i]
            rndtheta = random.random() * 2 * pi
            bullet_list.append(Bullet(cb.pos, Vec(cos(rndtheta), sin(rndtheta)), self.index, 2 * modelconst.bullet_radius))
            self.body_list.pop()

    def rainbow_mode(self):
        for ii in range(len(self.body_list)-1,0,-1):
            i = self.body_list[ii]
            if i.color == i.pre.color:
                i.color = ( random.randint(0,255), random.randint(0,255), random.randint(0,255))




