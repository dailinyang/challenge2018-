# State machine constants for the StateMachine class below
STATE_RESTART = 0
STATE_MENU = 1
STATE_STOP = 2
STATE_PLAY = 3
STATE_ENDGAME = 4
STATE_ENDMATCH = 5
STATE_CUTIN = 6
class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    def __init__ (self):
        self.statestack = []
    
    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None
    
    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            # empty stack
            return None
    
    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.statestack.append(state)
        return state

    def clear(self):
        """
        Clear the stack.
        """
        self.statestack = []
