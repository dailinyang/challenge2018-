import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.white_ball import White_Ball
from pygame.math import Vector2 as Vec
from Model.GameObject.bullet import Bullet
from Model.GameObject.head import Head
from Model.GameObject.item import Item, Explosive, Bigbullet, Multibullet

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst
from math import pi, sin, cos, atan2

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AINames):
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AINames = AINames
        self.TurnTo = 0

        self.player_list = []
        
        self.wb_list = []
        self.bullet_list = []
        
        #self item
        ##explsion
        self.item_list = []
        self.ticks = 0
        self.score_list = [0, 0, 0, 0]
        self.endgame_ticks = 0
        self.have_scoreboard = [True] * 4

        self.gamenumber = 1
        self.special_scoreboard = [False] * 4

        
    def initialize(self):
        self.grav_index = -1
        self.bombtimer = [-1] * 4
        self.ticks = 0
        self.tmp_score_list = [0, 0, 0, 0]
        self.endgame_ticks = 0
        self.init_wb_list()
        self.init_player_list()
        self.init_body_list()
        self.init_bullet_list()
        self.init_item_list()

    def init_wb_list(self):
        #init wb list
        self.wb_list = []
        for i in range(modelConst.wb_init_num):
            self.wb_list.append(White_Ball(Vec(-2,-2)))
    #init item list
    def init_item_list(self):
        self.item_list = []
        pass
        '''
        self.item_list = []
        for i in range(modelConst.item_init_num):
            rnd = randint(1,3)
            if rnd == 1:
                self.item_list.append(Explosive())
            if rnd == 2:
                self.item_list.append(Multibullet())
            if rnd == 3:
                self.item_list.append(Bigbullet())
        '''

    def init_player_list(self):
        tmp = []
        if len(self.player_list) > 0:
            for i in self.player_list:
                tmp.append(i.score)
        else :
            for i in range(modelConst.PlayerNum):
                tmp.append(0)
        self.player_list = []
        ManualPlayerNum = 0
        for index in range(modelConst.PlayerNum):
            if len(self.AINames) > index:
                PlayerName = self.AINames[index]
                if PlayerName == "~":
                    if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                        ManualPlayerNum += 1
                    else:
                        self.AINames[index] = "_"
            else:
                if ManualPlayerNum < modelConst.MaxManualPlayerNum:
                    ManualPlayerNum += 1
                    self.AINames.append("~")
                else:
                    self.AINames.append("_")

        # init Player object
        for index in range(modelConst.PlayerNum):
            if self.AINames[index] == "~":
                Tmp_P = Head(index, "manual", False)
            elif self.AINames[index] == "_":
                Tmp_P = Head(index, "default", True)
            else:
                Tmp_P = Head(index, 'player' + self.AINames[index], True)
            self.player_list.append(Tmp_P)
    
    def init_body_list(self):
        # No bodies at start of game
        pass
    def init_bullet_list(self):
        # No bullets at start of game
        self.bullet_list = []
    
    def create_ball(self):
        # update and see if create new ball
        if len(self.wb_list) < modelConst.wb_max_num and random.randint(0,modelConst.wb_born_period*viewConst.FramePerSec)==0:
            self.wb_list.append(White_Ball())
            
    def create_item(self):
        # update and see if create new item
        if len(self.item_list) < modelConst.item_max and random.randint(0,modelConst.item_born_period*viewConst.FramePerSec)==0:
            rnd = random.randint(1,3)
            if rnd == 1:
                self.item_list.append(Explosive(self.evManager))
            if rnd == 2:
                self.item_list.append(Multibullet())
            if rnd == 3:
                self.item_list.append(Bigbullet())
    def create_bullet(self):
        if self.ticks < modelConst.suddendeath_ticks:
            return
        if self.ticks == modelConst.suddendeath_ticks:
            self.evManager.Post(Event_SuddenDeath())
        if random.randint(0, modelConst.freq * int(viewConst.FramePerSec**2 / (self.ticks - modelConst.suddendeath_ticks + 1))) ==0:
            screen_mid = Vec( viewConst.ScreenSize[1]/2, viewConst.ScreenSize[1]/2 )
            rndtheta = random.random() * 2 * pi
            self.bullet_list.append( Bullet(screen_mid, Vec(cos(rndtheta),sin(rndtheta)), -1, modelConst.bullet_radius,\
                                            modelConst.suddendeath_speed , 0 ) )
    
    def tick_update(self):
        #update bullets
        for i in range(len(self.bullet_list)-1,-1,-1):
            item = self.bullet_list[i]
            #update failed means the bullet should become a white ball
            upd = item.update()
            if upd == None:
                for j in range(modelConst.bomb_amount):
                    theta = 2 * pi / modelConst.bomb_amount * j
                    self.bullet_list.append( Bullet(item.pos, Vec(cos(theta),sin(theta)), item.index, modelConst.bullet_radius,\
                                                    modelConst.suddendeath_speed , 0 ) )
                self.bullet_list.pop(i)
            elif not upd:
                self.wb_list.append(White_Ball(item.pos))
                self.bullet_list.pop(i)
        #update white balls
        if self.player_list[0].init_timer == -1:
            self.create_ball()
            self.create_item()
        self.create_bullet()
        #update items
        for item in self.item_list:
            item.update()


        for i in range(len(self.wb_list)-1,-1,-1):
            item = self.wb_list[i]
            if not item.update(self.player_list):
                self.wb_list.pop(i)
        #update heads
        alive = 0
        for item in self.player_list:
            killed=0
            if item.is_dash:
                for i in range(modelConst.dash_speed_multiplier):
                    killed |= item.update(self.player_list,self.wb_list,self.bullet_list,self.item_list,self.score_list,self.tmp_score_list)
            else:
                killed = item.update(self.player_list,self.wb_list,self.bullet_list,self.item_list,self.score_list,self.tmp_score_list)
            if killed == 1:
                self.evManager.Post(Event_PlayerKilled(item.index,item.pos))
            if item.is_alive:
                alive += 1
        if alive <= 1:
            self.endgame_ticks += 1
            if self.endgame_ticks > 300:
                if self.gamenumber == 5:
                    self.evManager.Post(Event_StateChange(STATE_ENDMATCH))
                else:
                    self.evManager.Post(Event_StateChange(STATE_ENDGAME))
                self.gamenumber += 1
        self.ticks += 1
        for i in range(4):
            if self.bombtimer[i] == 0:
                self.bomb(i)
                self.bombtimer[i] = -1
            elif self.bombtimer[i] > 0:
                self.bombtimer[i] -= 1


    def bomb(self,index):
        i = index*2 + 1
        pos = (viewConst.GameSize[0] + viewConst.GameSize[1] // (modelConst.PlayerNum * 2), viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * i)
        radius = int(viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * 0.7)
        self.bullet_list.append(Bullet(pos, (self.player_list[index].pos - pos).normalize(), index, radius,modelConst.bomb_speed, modelConst.bomb_a) )
        self.have_scoreboard[index] = False
    def can_use_skill(self, index):
        player = self.player_list[index]
        return (self.ticks > 200) and player.is_alive and (self.endgame_ticks == 0)
    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                # every tick update
                self.tick_update() 
        elif isinstance(event, Event_MoveWayChange):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.player_list[event.PlayerIndex].click(self.bullet_list,self.wb_list)
        elif isinstance(event, Event_Skill):
            number = event.number
            player = self.player_list[event.PlayerIndex]
            cur_state = self.state.peek()
            if (cur_state not in [STATE_PLAY, STATE_CUTIN]) or not self.can_use_skill(player.index):
                return
            if cur_state == STATE_PLAY:
                self.evManager.Post(Event_CutIn(player.index,number))
                self.state.push(STATE_CUTIN)
            else:
                self.state.pop()
                if number == 1:
                    self.item_list.append(Explosive(self.evManager, player.pos))
                elif number == 2:
                    player.always_bigbullet = False
                    player.always_multibullet = True
                elif number == 3:
                    player.always_bigbullet = True
                    player.always_multibullet = False
                elif number == 4:
                    player.blast(self.bullet_list)
                elif number == 5:
                    self.bombtimer[player.index] = modelConst.bombtime
                elif number == 6:
                    player.is_rainbow = True
                    #player.rainbow_mode()
                elif number == 7:
                    self.grav_index = player.index
            
        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state is None:
                # false if no more states are left
                if self.state.peek() == STATE_ENDGAME:
                    modelConst.next_grav()
                    self.evManager.Post(Event_Initialize())
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            elif event.state == STATE_ENDGAME:
                self.state.push(STATE_ENDGAME)
            elif event.state == STATE_ENDMATCH:
                self.state.clear()
                self.state.push(STATE_ENDMATCH)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_Quit):
            self.running = False
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Restart):
            self.initialize()
            self.score_list = [0, 0, 0, 0]
            self.have_scoreboard = [True, True, True, True]
            self.gamenumber = 1


    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)

