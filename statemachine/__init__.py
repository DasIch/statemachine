# coding: utf-8
"""
    statemachine
    ~~~~~~~~~~~~

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""


class State(object):
    """
    This is a base class for states.
    """
    def handle_event(self, statemachine, event):
        """
        Gets called when the statemachine receives an event.
        """
        raise NotImplementedError(event)

    def handle_result(self, result):
        """
        Gets called when a state pushed onto the stack by this state pops
        itself of with the given `result`.
        """
        raise NotImplementedError(result)


class Statemachine(object):
    """
    This is the statemachine.

    :param state_stack:
        A stack with states which is used initially.
    """
    def __init__(self, state_stack):
        #: A stack with all the states.
        self.stack = state_stack
        #: The results as a list.
        self.results = []

    @property
    def current_state(self):
        """
        A simple helper always pointing to the top of :attr:`stack`.
        """
        return self.stack[-1]

    def push_state(self, state):
        """
        Pushes the given `state` on the stack.
        """
        self.stack.append(state)

    def pop_state(self, result):
        """
        Pops the current state of the stack and calls the next current state
        with the given `result`.
        """
        self.stack.pop()
        try:
            current_state = self.current_state
        except IndexError:
            self.results.append(result)
        else:
            current_state.handle_result(result)

    def handle_event(self, event):
        """
        Calls :meth:`State.handle_meth` of the current state with the given
        `event`.
        """
        self.current_state.handle_event(self, event)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.stack)
