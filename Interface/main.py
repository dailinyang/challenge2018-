import imp, traceback
import sys, signal

import Model.main as model
from Events.Manager import *

from Interface.helper import Helper
from time import time

import AI.base as AI

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class Interface(object):
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.playerAI = {}

        self.is_initAI = False

        self.skill_queue = []
        self.cutin_isdisplay = False
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_PLAY:
                self.API_play()
        elif isinstance(event, Event_Quit):
            pass
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Skill):
            if self.cutin_isdisplay and self.skill_queue:
                self.cutin_isdisplay = not self.cutin_isdisplay
                self.evManager.Post(self.skill_queue.pop(0))
            else:
                self.cutin_isdisplay = not self.cutin_isdisplay
    
    def API_play(self):
        # for player in self.model.player_list:
        #assert self.skill_queue == []
        #assert self.cutin_isdisplay == False
        for idx, player in enumerate(self.model.player_list):
            if player.is_AI:
                AI_Dir = self.playerAI[player.index].decide()
                if AI_Dir == AI.AI_MoveWayChange:
                    self.evManager.Post(Event_MoveWayChange(player.index))
                elif 2 <= AI_Dir <= 8:
                    if self.model.can_use_skill(idx) and self.playerAI[player.index].skill[AI_Dir-2] > 0:
                        self.playerAI[player.index].skill[AI_Dir-2] -= 1
                        self.skill_queue.append(Event_Skill(player.index, AI_Dir-1))

        if self.skill_queue:
            self.evManager.Post(self.skill_queue.pop(0))

    def API_play_linux(self):
        # for player in self.model.player_list:
        for idx, player in enumerate(self.model.player_list):
            if player.is_AI:
                try:
                    signal.signal(signal.SIGALRM, self.handler)
                    signal.setitimer(signal.ITIMER_REAL, 0.001)
                    start_time = time()
                    AI_Dir = self.playerAI[player.index].decide()
                    print('player:', idx, time() - start_time)
                    if AI_Dir == AI.AI_MoveWayChange:
                        self.evManager.Post(Event_MoveWayChange(player.index))
                    elif AI_Dir == AI.AI_Skill:
                        self.evManager.Post(Event_Skill(player.index, 0))
                    signal.setitimer(signal.ITIMER_REAL, 0)
                except signal.ItimerError:
                    # print('TimeOut: %s' % player.name)
                    self.evManager.Post(Event_TimeLimitExceed(player.index))
                finally:
                    signal.signal(signal.SIGALRM, signal.SIG_DFL)


    def handler(self, signum, frame):
        raise signal.ItimerError

    def initialize(self):
        if self.is_initAI: return

        self.is_initAI = True
        for index, player in enumerate(self.model.player_list):
            if player.name == "manual":
                    continue
            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_'+ player.name +'.py')
            except:
                self.loadmsg( str(index), player.name, "AI can't load")
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            self.loadmsg( str(index), player.name, "Loading")
            # init TeamAI class
            try:
                self.playerAI[player.index] = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                self.loadmsg( str(index), player.name, "AI init crashed")
                traceback.print_exc()
                player.name, player.is_AI, player.ai= "Error" , False, None
                continue
            self.loadmsg( str(index), player.name, "Successful to Load")

    def loadmsg(self, index, name ,msg):
        print("["+ str(index) +"] team_" + name + ".py: "+ msg)
    