from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
        self.second = False
        self.ingrav = False

    def decide( self ):
        helper = self.helper
        hPos = helper.getMyHeadPos()
        wb_radius = helper.wb_radius
        normalspeed=helper.normal_speed
        dashspeed=helper.dash_speed
        myindex=helper.getMyIndex()
        if helper.getDashPos() == None:
            speed=normalspeed
        else:
            speed=dashspeed
        bullets=helper.getAllPlayerBullet()

        for bullet in bullets:
        	bulletplayer,bulletpos,bulletdir,bulletradius,bulletspeed=bullet
        	if not helper.checkMeInGrav():
         		if helper.getOtherBulletNumInRange(hPos, 4 * wb_radius) > 0:
         			if (bulletplayer!=myindex) and (((bulletpos[0]-hPos[0])/(bulletpos[1]-hPos[1]))==((bulletpos[0]-bulletdir[0])/(bulletpos[1]-bulletdir[1]))):
         				print('dodge')
         				return AI_MoveWayChange
         			elif helper.getOtherBulletNumInRange(hPos, 3 * wb_radius) > 0:
         				return AI_MoveWayChange

        if not helper.checkMeInGrav():
            if helper.bodyOnRoute() or helper.headOnRoute():
                return AI_MoveWayChange

        if self.ingrav==False and helper.checkMeInGrav():
            self.ingrav = True
            self.second = True
            return AI_MoveWayChange
        if self.second == True:
            self.second = False
            return AI_MoveWayChange
        if not helper.checkMeInGrav():
            self.ingrav = False


        return AI_NothingToDo

        
