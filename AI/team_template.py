from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []

    def decide( self ):
        return AI_NothingToDo