from classes.exceptions.main import NoNextStateException, EndStateException


class fsm(object):
    """ A simple to use finite state machine class.
        Allows definition of multiple states, condition functions from state to state and optional callbacks
    """

    def __init__(self, states=[]):
        self._states = states
        self.currentState = None
        self.next_state = None
        self.IdentifierTable = []

    def start(self, startState=None):
        """ Start the finite state machine
        """
        if not startState or not (startState in [x[0] for x in self._states]):
            raise ValueError("Not a valid start state")
        self.currentState = (startState, False)

    def stop(self):
        """ Stop the finite state machine
        """
        # Bug fix 15 Dec 2012 - self.currentState should be reset, not startState - Identified by Holger Waldmann
        self.currentState = None

    def add_transition(self, fromState, toState, condition, end_state=False, callback=None):
        """ Add a state transition to the list, order is irellevant, loops are undetected
            Can only add a transition if the state machine isn't started.
        """
        if not self.currentState:
            raise ValueError("StateMachine already Started - cannot add new transitions")

        # add a transition to the state table
        self._states.append((fromState, toState, condition, end_state, callback))

    def event(self, value):
        """ Trigger a transition - return a tuple (<new_state>, <changed>)
            Raise an exception if no valid transition exists.
            Callee needs to determine if the value will be consumed or re-used
        """
        if not self.currentState:
            raise ValueError("StateMachine not Started - cannot process event")

        if self.currentState[1]:
            raise EndStateException("StateMachine is in the end state")

        # get a list of transitions which are valid

        self.next_state = None

        for state in self._states:
            if state[0] == self.currentState[0] and (state[2] == True or (callable(state[2]) and state[2](value))):
                self.next_state = state
                break

        # self.next_states = [x for x in self._states
        #                     if x[0] == self.currentState[0]
        #                     and (x[2] == True or (callable(x[2]) and x[2](value)))]

        if not self.next_state:
            raise NoNextStateException(
                "No Transition defined from state {0} with value '{1}'".format(self.currentState, value))

        # elif len(self.next_states) > 1:
        #     raise ValueError("Ambiguous transitions from state {0} with value '{1}' ->  New states defined {2}".format(
        #         self.currentState, value, [x[0] for x in self.next_states]))
        else:
            if len(self.next_state) == 5:
                current, next, condition, end_state, callback = self.next_state
            else:
                current, next, condition, end_state = self.next_state
                callback = None

            if self.currentState[0] != next:
                self.currentState = (next, end_state)
                changed = True
            else:
                self.currentState = (next, end_state)
                changed = False

            # self.currentState, changed = (next, True) if self.currentState != next else (next, False)

            # Execute the callback if defined
            if callable(callback):
                callback(self, value)

            return self.currentState + (changed,)

    def current_state(self):
        """ Return the current State of the finite State machine
        """
        return self.currentState
