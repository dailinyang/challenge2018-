import Model.const as modelConst
from pygame.math import Vector2 as Vec
"""
define Application Programming Interface(API) 
"""
def Mirroring(pos):
    Pos = Vec(pos)
    if Pos.x < 0:
        Pos.x = -Pos.x
    if Pos.y < 0:
        Pos.y = -Pos.y
    if Pos.x > 800:
        Pos.x = 1600 - Pos.x
    if Pos.y > 800: 
        Pos.y = 1600 - Pos.y 
    return tuple(Pos)

class Helper(object):
    explosive_radius = modelConst.explosive_radius
    head_radius = modelConst.head_radius
    body_radius = modelConst.body_radius
    wb_radius = modelConst.wb_radius
    normal_speed = modelConst.normal_speed
    dash_speed = modelConst.dash_speed
    dash_cool = modelConst.dash_cool
    max_dash_time=modelConst.max_dash_time
    bullet_acc = modelConst.bullet_a
    dash_time = modelConst.max_dash_time
    bullet_speed = modelConst.bullet_speed0
    bullet_radius = modelConst.bullet_radius
    def __init__(self, model, index):
        self.model = model
        self.index = index

    #map info
    def getExplosionRadius(self):
        return modelConst.explosive_radius
    
    def getHeadRadius(self):
        return modelConst.head_radius

    def getBodyRadius(self):
        return modelConst.body_radius

    def getWhiteballRadius(self):
        return modelConst.wb_radius

    def getNormalSpeed(self):
        return modelConst.normal_speed

    def getDashSpeed(self):
        return modelConst.dash_speed

    def getBulleyAcceleration(self):
        return modelConst.bullet_a

    def getNearestGravOnRoute(self):
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        min_dist = float('inf')
        min_gPos = None
        min_gRadius = None
        for gPos, gRadius in modelConst.grav:
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, gPos, gRadius):
                dist = (gPos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_gPos = Vec(gPos)
                    min_gRadius = gRadius
        if min_gPos is None:
            return None
        return tuple(min_gPos), min_gRadius

    def getAllGravs(self):
        return [(tuple(gPos), gRadius) for gPos, gRadius in modelConst.grav]

    def getNearestPosToCenter(self):
        if not self.checkMeInGrav():
            return None
        gPos, gRadius = self.getMyGrav()
        gPos = Vec(gPos)
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        inner_product = (gPos - hPos).dot(hDir)
        return tuple(hPos + inner_product * hDir)

    def getBallNumInRange(self, center, radius):
        count = 0
        for wb in self.model.wb_list:
            if wb.target == -1 and (wb.pos - center).length_squared() <= radius ** 2:
                count += 1
        return count

    def getOtherBulletNumInRange(self, center, radius):
        count = 0
        for bullet in self.model.bullet_list:
            if bullet.index == self.index:
                continue
            if (bullet.pos - center).length_squared() <= radius ** 2:
                count += 1
        return count

    def getAllBallsPos(self):
        return [tuple(wb.pos) for wb in self.model.wb_list if wb.target == -1]

    def getExplosivePos(self):
        return [tuple(item.pos) for item in self.model.Item_list if item.type == modelConst.PROP_TYPE_EXPLOSIVE]

    def getMultibulletPos(self):
        return [tuple(item.pos) for item in self.model.Item_list if item.type == modelConst.PROP_TYPE_MULTIBULLET]

    def getBigbulletPos(self):
        return [tuple(item.pos) for item in self.model.Item_list if item.type == modelConst.PROP_TYPE_BIGBULLET]
    
    def canGetByExplosion(self, Epos):
        count = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if (wb.pos - Epos).length_squared() < (modelConst.explosive_radius + modelConst.wb_radius) ** 2:
                count += 1
        return count

    def canGetBySpin(self):
        if not self.checkMeInGrav():
            return None
        gPos, gRadius = self.getMyGrav()
        gPos = Vec(gPos)
        inRadius = self.model.player_list[self.index].circling_radius - modelConst.dash_radius
        outRadius = self.model.player_list[self.index].circling_radius + modelConst.dash_radius
        count = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if (wb.pos - gPos).length_squared() > inRadius ** 2 and (wb.pos - gPos).length_squared() < outRadius ** 2:
                count += 1
        return count

    def canGetOnRoute(self):
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        count  = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, wb.pos, modelConst.wb_radius):
                count += 1
        return count

    def getNearestballOnRoute(self):
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        min_pos = Vec(0, 0)
        min_dist = float('inf')
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, wb.pos, modelConst.wb_radius):
                dist = (wb.pos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(wb.pos)
        if min_pos == Vec(0, 0):
            return None 
        return tuple(min_pos)

    def headOnRoute(self):
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        pos_list = []
        for player in self.model.player_list:
            if player.index == self.index or (not player.is_alive):
                continue
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, player.pos, modelConst.head_radius):
                pos_list.append(tuple(player.pos))
        return pos_list

    def bodyOnRoute(self):
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        pos_list = []
        for player in self.model.player_list:
            if player.index == self.index or (not player.is_alive):
                continue
            for body in player.body_list:
                if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, body.pos, modelConst.body_radius):
                    pos_list.append(tuple(body.pos))
        return pos_list

    def collisionOnRoute(self, pos1, radius1, _dir, pos2, radius2):
        Pos1 = Vec(pos1)
        Pos2 = Vec(pos2)
        Dir = Vec(_dir)
        inner_product = (Pos2 - Pos1).dot(Dir)
        outer_product = abs((Pos2 - Pos1).cross(Dir))
        return inner_product > 0 and outer_product > 0 and outer_product + modelConst.eps <= radius1 + radius2


    #me info
    def getMyIndex(self):
        return self.index

    def getMyHeadPos(self):
        return tuple(self.model.player_list[self.index].pos)

    def getMyBodyPos(self):
        return [tuple(body.pos) 
                for body in self.model.player_list[self.index].body_list[1:]]

    def getMyDir(self):
        return tuple(self.model.player_list[self.index].direction)

    def getMyGrav(self):
        if not self.checkMeInGrav():
            return None
        hPos = Vec(self.getMyHeadPos())
        for gPos, gRadius in modelConst.grav:
            if (hPos - gPos).length_squared() < gRadius ** 2:
                return tuple(gPos), gRadius

    def getDashPos(self):
        if not self.checkInvisible():
            return None
        hPos = Vec(self.getMyHeadPos())
        hDir = Vec(self.getMyDir())
        return Mirroring(Vec(hPos + modelConst.dash_speed * (self.model.player_list[self.index].dash_timer // 3) * hDir))

    def getMyDashRemainTime(self):
        return self.model.player_list[self.index].dash_timer // 3

    def getMyDashCoolRemainTime(self):
        dashcooltime = self.model.player_list[self.index].dash_cool
        if dashcooltime > modelConst.dash_cool :
            return (dashcooltime - modelConst.dash_cool)//3 + modelConst.dash_cool
        else :
            return dashcooltime

    def checkMeInGrav(self):
        return self.model.player_list[self.index].is_ingrav

    def checkMeCircling(self):
        return self.model.player_list[self.index].is_circling

    def checkInvisible(self):
        return self.model.player_list[self.index].is_dash

    def getMyCirclingRadius(self):
        return self.model.player_list[self.index].circling_radius

    def getMyBullet(self):
        return [(tuple(bullet.pos), tuple(bullet.direction), bullet.radius, bullet.speed) 
                for bullet in self.model.bullet_list if bullet.index == self.index]

    def getMyScore(self):
        return self.model.score_list[self.index]

    #player info
    def getPlayerHeadPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return tuple(self.model.player_list[player_id].pos)

    def getPlayerBodyPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return [tuple(body.pos) 
                for body in self.model.player_list[player_id].body_list[1:]]

    def getPlayerDir(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return tuple(self.model.player_list[player_id].direction)

    def getPlayerDashRemainTime(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].dash_timer // 3

    def getPlayerDashCoolRemainTime(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        dashcooltime = self.model.player_list[player_id].dash_cool
        if dashcooltime > modelConst.dash_cool :
            return (dashcooltime - modelConst.dash_cool)//3 + modelConst.dash_cool
        else :
            return dashcooltime
    def checkPlayerInGrav(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_ingrav

    def checkPlayerInvisible(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_dash
    
    def checkPlayerCircling(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_circling
    
    def checkPlayerAlive(self, player_id):
        return self.model.player_list[player_id].is_alive

    def getPlayerCirclingRadius(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].circling_radius

    def getAllPlayerBullet(self):
        return [(bullet.index, tuple(bullet.pos), tuple(bullet.direction), bullet.radius, bullet.speed) 
                for bullet in self.model.bullet_list if bullet.index != self.index]

    def getPlayerScore(self, player_id):
        return self.model.score_list[player_id]

    def getAllBodyPos(self):
        lst = []
        for i in range(4):
            if (not self.model.player_list[i].is_alive) or i == self.index:
                continue
            else:
                lst += self.getPlayerBodyPos(i)
        return lst