# coding: utf-8
"""
    parser
    ~~~~~~

    This is an example for a simple parser.

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import re
import sys
sys.path.insert(0, sys.path[0] + '/..')

from statemachine import State, Statemachine


class BracketState(State):
    def __init__(self):
        self.contents = []

    def handle_event(self, statemachine, event):
        if event == '[':
            statemachine.push_state(BracketState())
        elif event == ']':
            statemachine.pop_state(self.contents)
        else:
            statemachine.push_state(StringState())
            statemachine.handle_event(event)

    def handle_result(self, result):
        self.contents.append(result)


class StringState(State):
    def __init__(self):
        self.contents = []

    def handle_event(self, statemachine, event):
        if re.match(r'\w|\d', event):
            self.contents.append(event)
        else:
            statemachine.pop_state(''.join(self.contents))
            if event != ' ':
                statemachine.handle_event(event)


def main():
    strings = [
        ('[1 2 3]', ['1', '2', '3']),
        ('[1 [2 3]]', ['1', ['2', '3']]),
        ('[1[2[3]]]', ['1', ['2', ['3']]])
    ]
    for string, expected_result in strings:
        statemachine = Statemachine([BracketState()])
        for character in string[1:]:
            statemachine.handle_event(character)
        assert statemachine.results[0] == expected_result
        print 'input:', string
        print 'got:', statemachine.results[0]
        print 'expected:', expected_result


if __name__ == '__main__':
    main()
