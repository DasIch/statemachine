Idea
====

This document explains the initial idea behind Statemachine and it's
design.

Abstract
--------

There two common ways to encapsulate the state of an application, you can
keep it in a datastructure you pass along or keep it local to a process.

However they focus on purely on the I/O part of the application,
processing as much data as possible in a certain time frame. While this is
an important goal they don't solve the problems arising when dealing with
state, they simply contain them.

I propose a way of encapsulating state which handles linear and non-linear
as well as ambiguous input, problems which I will discuss later on.

Basic Design
------------

First of all we have to think about what input is, in the context of this
project it is a stream of events or tokens, which are things that (might)
change the state of the application.

A state is something which receives events and creates new states for the
statemachine to transition to.

A statemachine is an object which receives events and passes them on to
the current state.

These definitions are not complete but that doesn't matter as of now,
let's take a look at this using an example.

Dealing with linear input
-------------------------

Let's consider a relatively simple situation. We want to build a parser for a
language and our input is a stream of characters. In this example every state
will be expected, and given the input is valid able, to handle the next
character.

Reusability
```````````

Let's take the following example::

    [foo bar baz]

We have 5 words, the 2 brackets and 3 strings. A string is a sequence of
a specific subset of characters, delimited by spaces and characters other
words are made of.

We have two problems though: sequences and nesting. We want to be able to
use a state to deal with a string and a state for the brackets. The
strings are contained in the brackets so we need to be able to pass the
string state, once it encounters a space, to the bracket state. Also if we
want to be able to nest brackets a bracket state needs to be passed to
it's parent if a closing bracket is encountered.

We solve this problem by giving the statemachine a stack of states, the
current state is now the state on top of the stack. States can push new
states onto the stack and stack can pop themselves off::

    input: '['
    # push a bracket state on the stack
    stack: []
    input: 'f'
    # push string on the stack
    stack: [] string
    ...
    input: ' '
    # string popped off
    stack: [foo]
    ...

This continues on until the bracket stack pops itself off the stack and
we have a result or at least a part of it if the input isn't finished.

Ambiguousness
``````````````

Let's consider something more advanced, consider a language in which we
have the following constructs::

    if <condition> then <foo>

    if <condition> then <foo> else <bar>

The first construct is an if-statement without an else-clause, the second
on is an if-statement with an else-clause.

The problem is that after encountering `<foo>` it is impossible to
determine if an else-clause follows or not without looking into the
future, the definition the system is based on is ambiguous.

This problem can be solves by introducing a new abstraction: the context.

The context receives events and sends each event to a set of
statemachines. States can now create multiple new states (or reuse
existing ones) at the same time, for each of those states a statemachine is
cloned one of the states is pushed on the stack of the statemachine. All those
clones reside in the context.

When the context calls a statemachine and the current state of it is unable to
handle a event said statemachine is killed.

If several statemachine successfully yield results the user has to choose
between the results.

The effort could be reduced by tracing the types and interaction of the
states and their respective statemachine and if they match one could
attempt to eliminate them once the state which created the clones is
popped of the stack.

The idea behind this optimization is that large parts of the input will probably
be interpreted equally and in turn only parts will be ambiguous, once such an
ambiguous part has been "visited" the statemachines should synchronize in their
behaviour. Once that happens the ambiguous parts could be checked.

Dealing with non-linear input
-----------------------------

Up until now we had a single current state, that is easy to deal with but
causes some problems if we have to maintain several states on the same
input.

As an example consider an IRC client, the server and the client exchange
messages between each other. If the IRC client authenticates that can be
either successful or not, if he joins a channel this might be successful
or not and at the same time we might receive messages of other people
doing things.

In this case each action we take can be described as it's own state and
all of those states can be considered active.

We can go about it the same way as with ambiguous input, for each active
state we yield a new statemachine, the only thing we have to make sure of
is that states that can't handle the events they are given, ignore them, so
that the context doesn't kill the statemachine.

Conclusion
----------

In conclusion the design consists of the following parts:

State
    A state handles events, pushes new states on the stack, adds
    statemachines to the context and pops itself of the stack.

Statemachine
    A statemachine holds a stack of states, receives events and passes
    them to the state at the top of the stack.

Context
    A context receives events and passes each to every statemachine it
    handles and kills those which fail. The purpose of the context is to
    provide a way to deal with ambiguous events and/or multiple parallel
    states.
