class BaseEvent(object):
    """
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    """
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class Event_Initialize(BaseEvent):
    """
    Initialize event.
    """
    def __init__(self):
        self.name = "Initialize event"
    def __str__(self):
        return self.name

class Event_Restart(BaseEvent):
    """
    Restart event.
    """
    def __init__(self):
        self.name = "Restart event"
    def __str__(self):
        return self.name

class Event_Quit(BaseEvent):
    """
    Quit event.
    """
    def __init__ (self):
        self.name = "Quit event"
    def __str__(self):
        return self.name

class Event_StateChange(BaseEvent):
    """
    Change state event.
    """
    def __init__(self, state):
        self.name = "StateChange event"
        self.state = state
    def __str__(self):
        return "{0} => StateTo:{1}".format(self.name, self.state)

class Event_MoveWayChange(BaseEvent):
    
    def __init__(self, player):
        self.name = "MoveWayChange event"
        self.PlayerIndex = player
    def __str__(self):
        return "{0} => Playerindex={1}".format(self.name, self.PlayerIndex)

class Event_TimeLimitExceed(BaseEvent):
    """
    Event of time limit exceed when running AI code.
    """
    def __init__(self, player):
        self.name = "TimeLimitExceed event"
        self.PlayerIndex = player
    def __str__(self):
        return "{0} => Playerindex={1}".format(self.name, self.PlayerIndex)

class Event_SuddenDeath(BaseEvent):
    """
    Event of time limit exceed when running AI code.
    """
    def __init__(self):
        self.name = "SuddenDeath Event"
    def __str__(self):
        return "{0}".format(self.name)


class Event_TriggerExplosive(BaseEvent):

    def __init__(self, player, pos):
        self.PlayerIndex = player
        self.name = "TriggerExplosive event"
        self.pos = pos

    def __str__(self):
        return "Explosion!"
class Event_PlayerKilled(BaseEvent):

    def __init__(self, player, pos):
        self.name = "PlayerKilled event"
        self.PlayerIndex = player
        self.pos = pos

    def __str__(self):
        return "{0} => Playerindex={1} , Killed at {2}".format(self.name, self.PlayerIndex, self.pos)

class Event_Skill(BaseEvent):
    
    def __init__(self, player, number):
        self.name = "Skill Event"
        self.PlayerIndex = player
        self.number = number
    def __str__(self):
        return "{0} => Playerindex={1}".format(self.name, self.PlayerIndex)

class Event_CutIn(BaseEvent):
    
    def __init__(self, player, number):
        self.name = "CutIn Event"
        self.PlayerIndex = player
        self.number = number
    def __str__(self):
        return "{0} => Playerindex={1}".format(self.name, self.PlayerIndex)

class Event_EveryTick(BaseEvent):
    """
    Tick event.
    """
    def __init__ (self):
        self.name = "Tick event"
    def __str__(self):
        return self.name

class Event_EverySec(BaseEvent):
    """
    Sec event.
    """
    def __init__(self):
        self.name = "Sec event"
    def __str__(self):
        return self.name

class Event_TimeUp(BaseEvent):
    """
    TimeUp event.
    """
    def __init__(self):
        self.name = "TimeUp event"
    def __str__(self):
        return self.name

class Event_Move(BaseEvent):
    """
    Move event.
    """
    def __init__(self, player, direction):
        self.name = "Move event"
        self.PlayerIndex = player
        self.Direction = direction
    def __str__(self):
        return "{0} => Playerindex={1}, DirectionTo:{2}".format(self.name, self.PlayerIndex, self.Direction)

class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    def __init__(self):
        self.listeners = []

    def RegisterListener(self, listener):
        """ 
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        self.listeners.append(listener)

    def UnregisterListener(self, listener):
        """ 
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        pass
        
    def Post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        # # this segment use to debug
        # if not (isinstance(event, Event_EveryTick) or isinstance(event, Event_EverySec)):
        #     print( str(event) )
        for listener in self.listeners:
            listener.notify(event)
