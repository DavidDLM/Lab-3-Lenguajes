# Thompson function
# https://userpages.umbc.edu/~squire/cs451_l6.html

'''
The thompson function takes a regular expression as input
and returns the start state of the resulting NFA.
It uses a vertexvertexStack to keep track of sub-expressions,
and constructs the NFA incrementally as it processes each
symbolacter of the input string

'''
from re import S
import pandas as pd
from graphviz import Digraph
from machine import *

EPSILON = 'ε'


class Thompson():
    def __init__(this, regex=None, counter=None, automatas=None):
        this.transitionsList = []
        this.splitTransitionsList = []
        this.regex = regex
        this.finalStatesList = []
        vertexvertexStack = []
        # Edge dictionary represents transitions to other states
        edgeDict = {}
        stateCount = 0
        this.states = []
        this.states_list = []
        this.startingState = None
        this.finalState = None
        this.symbolList = []
        this.error = False
        this.counter = counter
        this.automatas = automatas
        this.result = []

    def compile(this):
        this.case_concurrence()
        symbolList = []
        regex = this.regex
        for i in regex:
            if this.item(i):
                if i not in symbolList:
                    symbolList.append(i)

        this.symbolList = sorted(symbolList)

        vertexStack = []
        start = this.counter+1
        end = this.counter+2

        automata_counter_A = this.counter+1
        automata_counter_B = this.counter+1

        # Thompson algorithm
        for symbol in regex:
            # Left parenthesis management
            if symbol == "(":
                vertexStack.append(startingState)
                startingState = None
                finalState = None
            # Right (end) parenthesis management
            elif symbol == ")":
                finalState = vertexStack.pop()
                if not vertexStack:
                    startingState = None
                else:
                    startingState = vertexStack[-1]
            # If kleene
            # Kleene star, 4 nodes, 4 transitions
            # From q1 to qfinal, Epsilon
            elif symbol == '*':
                try:
                    '''
                    # Kleene star guide/template:

                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end

                    '''
                    node1, node2 = vertexStack.pop()
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    if start == node1:
                        start = automata_counter_A
                    if end == node2:
                        end = automata_counter_B
                    this.splitTransitionsList.append([node2, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [node2, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nKleene error.")
            # If OR
            elif symbol == "|":
                try:
                    '''
                    # OR guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (OR: 4 transitions)
                    # Also add transitions to transition list
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})

                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    if start == node11 or start == node21:
                        start = automata_counter_A
                    if end == node22 or end == node12:
                        end = automata_counter_B
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node21])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node11])
                    this.splitTransitionsList.append(
                        [node12, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [node22, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nOR error.")
            # if Concatenation
            elif symbol == '.':
                try:
                    '''
                    # Concatenation guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    ---------------------------------

                    e2 = stack.pop()
                    e1 = stack.pop()
                    e1.accept = False
                    e1.edges[None] = [e2]
                    stack.append(e1)
                    stack.append(e2)s

                    '''
                    # Save states in variables
                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append([node21, node12])
                    if start == node11:
                        start = node21
                    if end == node22:
                        end = node12
                    this.splitTransitionsList.append([node22, EPSILON, node11])

                except:
                    this.error = True
                    print("\nConcatenation error.")
            # if Positive
            elif symbol == '+':
                try:
                    '''
                    # Union guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (UNION: 3 transitions)
                    # Add transition to transition list
                    node1, node2 = vertexStack.pop()
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    this.result[node2][EPSILON] = (node1, automata_counter_B)
                    if start == node1:
                        start = automata_counter_A
                    if end == node2:
                        end = automata_counter_B
                    this.splitTransitionsList.append([node2, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [node2, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node1])
                except:
                    this.error = True
                    print("\n+ error.")
            # If concurrence
            elif symbol == "?":
                try:
                    '''
                    # Concurrence guide/template:

                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (CONCURRENCE: 3 transitions)
                    # Add transition to transition list
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})

                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    # this.result[automata_counter_A]['ε'] = (node21, node11)
                    # this.result[node12]['ε'] = automata_counter_B
                    # this.result[node22]['ε'] = automata_counter_B
                    if start == node11 or start == node21:
                        start = automata_counter_A
                    if end == node22 or end == node12:
                        end = automata_counter_B
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node21])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node11])
                    this.splitTransitionsList.append(
                        [node12, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [node22, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nCONCURRENCE error.")
            else:
                this.counter = this.counter+1
                automata_counter_A = this.counter
                if automata_counter_A not in this.states:
                    this.states.append(automata_counter_A)
                this.counter = this.counter+1
                automata_counter_B = this.counter
                if automata_counter_B not in this.states:
                    this.states.append(automata_counter_B)
                this.result.append({})
                this.result.append({})
                vertexStack.append([automata_counter_A, automata_counter_B])
                this.splitTransitionsList.append(
                    [automata_counter_A, i, automata_counter_B])

        this.startingState = start
        this.finalStatesList.append(end)
        df = pd.DataFrame(this.result)
        string_afn = df.to_string()

        for i in range(len(this.splitTransitionsList)):
            this.transitionsList.append(
                "(" + str(this.splitTransitionsList[i][0]) + " - " + str(this.splitTransitionsList[i][1]) + " - " + str(this.splitTransitionsList[i][2]) + ")")
        this.transitionsList = ', '.join(this.transitionsList)

        for i in range(len(this.states)):
            if i == len(this.states)-1:
                finalStatesList = i
            this.states_list.append(str(this.states[i]))
        this.states_list = ", ".join(this.states_list)

        if this.error == False:
            return
        else:
            print("\nInvalid format or regex.")

    def lex_automata(this, filename):
        this.counter = this.counter+1
        this.startingState = this.counter
        states_set = set()
        finalState_set = set()
        symbol_set = set()
        for automata in this.automatas:
            this.finalStatesList.append(automata.finalStatesList[0])
            this.splitTransitionsList = this.splitTransitionsList + automata.splitTransitionsList
            this.states = this.states + automata.states
            this.splitTransitionsList.append(
                [this.startingState, EPSILON, automata.startingState])

        # This will create a graph with nodes and edges,
        #  with labels indicating the direction of the edges.
        dot = Digraph()
        for state in this.states:
            if state in this.finalStatesList:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state), shape="circle")
        for transition in this.splitTransitionsList:
            if transition[1] == EPSILON:
                dot.edge(str(transition[0]), str(transition[2]), label=EPSILON)
            else:
                dot.edge(str(transition[0]), str(
                    transition[2]), label=transition[1])
        dot.render(filename, format='png', view=True)

    def item(this, char):
        # Recognize char
        if(char.isalpha() or char.isnumeric() or char == EPSILON):
            return True
        else:
            return False

    def case_concurrence(this):
        # Case concurrence
        # Replace concurrence with epsilon
        this.regex = this.regex.replace('?', 'ε?')
