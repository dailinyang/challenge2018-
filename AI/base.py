"""
const of AI code use.
"""
#action

AI_NothingToDo     = 0
AI_MoveWayChange   = 1
AI_Explosion       = 2
AI_MultiBullet     = 3
AI_BigBullet       = 4
AI_NuclFission     = 5
AI_HypSniping      = 6
AI_ExSpecHarmony   = 7
AI_GravResonance   = 8


"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass