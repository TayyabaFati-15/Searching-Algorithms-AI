"""
heuristics.py
-------------
Heuristics for the basic maze problem (Question 6).

A heuristic is a function heuristic(state, problem) that returns an estimate
of the cost of the cheapest path from 'state' to a goal. For a MazeProblem,
'state' is a (row, col) tuple and the goal position is 'problem.goal'.
"""

import math

import util


def nullHeuristic(state, problem=None):
    """The trivial heuristic: it knows nothing, so it always says 0."""
    return 0


def manhattanHeuristic(state, problem):
    x1,y1=state
    x2,y2=problem.goal
    return abs(x1-x2)+abs(y1-y2)



def euclideanHeuristic(state, problem):
    x1,y1=state
    x2,y2=problem.goal
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

