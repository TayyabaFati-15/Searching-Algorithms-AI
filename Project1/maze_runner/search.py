"""
search.py
---------
THE MAZE RUNNER — Mini Project 1: Classical Search

This is where you implement the search algorithms (Questions 1–7).

Every algorithm receives a SearchProblem (see problems.py) and must return a
LIST OF ACTIONS that leads from the start state to a goal state, e.g.
['South', 'South', 'East']. Return [] if the start state is already a goal.

Conventions the grader relies on (please read — they matter!):

  * Use the fringe containers from util.py (Stack, Queue, PriorityQueue).
  * Calling problem.getSuccessors(state) counts as EXPANDING that state.
    Call it exactly once per expanded state, and never for a state you only
    generated.
  * Goal test when a state is POPPED from the fringe (just before you would
    expand it), not when it is pushed. (For BFS the grader also accepts
    the "early" goal test done when a state is generated.)
  * Push successors in the order getSuccessors returns them.
  * Q1, Q2, Q5, Q6, Q7 are GRAPH searches: keep a set of already-expanded
    states and never expand the same state twice.
"""

import util
from util import Stack, Queue, PriorityQueue, CUTOFF
from heuristics import nullHeuristic


# ----------------------------------------------------------------------
# Q0 (worked example, not graded): always go right
# ----------------------------------------------------------------------
def alwaysRightSearch(problem):
    """
    Not a real search: the runner keeps stepping right ('East') until he
    reaches the goal. If a wall blocks the way east, he is stuck and gives up
    (returns None). It shows you how to use the problem's methods. Try it:
        python runner.py -l maze_tiny -a right     (escapes)
        python runner.py -l maze_small -a right       (walks into a wall)
    """
    state = problem.getStartState()
    actions = []
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)   # list of (next, action, cost)
        east = [s for s in successors if s[1] == 'East']
        if not east:
            return None   # a wall straight ahead: the doors close with him inside
        nextState, action, stepCost = east[0]
        actions.append(action)
        state = nextState
    return actions


# ----------------------------------------------------------------------
# Q1: Depth-First Search
# ----------------------------------------------------------------------

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first (graph search).

    To get started, try printing:
        print("Start:", problem.getStartState())
        print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
        print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    Hint: a fringe entry can hold more than a state. Storing
    (state, actionsSoFar) is an easy way to remember how you got there.
    """
    fringe = Stack()
    # Store (state, actions_list)
    fringe.push((problem.getStartState(), []))#  push takes one argument so we gve it a tuple
    expanded = set()
    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions
        if state not in expanded:
            expanded.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in expanded:
                    fringe.push((successor, actions + [action]))

    return None


# ----------------------------------------------------------------------
# Q2: Breadth-First Search
# ----------------------------------------------------------------------
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first (graph search)."""
    fringe = Queue()
    # Store (state, actions_list)
    fringe.push((problem.getStartState(), []))
    expanded = set()
    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions
        if state not in expanded:
            expanded.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in expanded:
                    fringe.push((successor, actions + [action]))

    return None


# ----------------------------------------------------------------------
# Q3: Depth-Limited Search
# ----------------------------------------------------------------------
def depthLimitedSearch(problem, limit):
       BestDepth={}
       fringe=Stack()
       fringe.push((problem.getStartState(),[]))#  push takes one argument so we gve it a tuple
       isCutoff=False
       while fringe.isEmpty()==False:
           state,path=fringe.pop()
             
           if problem.isGoalState(state):
               return path

           if state in BestDepth and BestDepth[state]<=len(path):
               continue
           BestDepth[state]=len(path)

           if len(path)==limit:#we introduce this check after the previous one so that if state is present in bestDepth already then this loop is skipped to next
               isCutoff=True
               continue
            
           for nextState,paths,cost in problem.getSuccessors(state):
                  fringe.push((nextState,path+[paths]))

       return CUTOFF if isCutoff else None  
   
#in DLS we shouldnot keep track of the visited nodes because if a nodes is explored and depth is reached then we should not explore it again but if we have a node that is explored and depth is not reached then we should explore it again becuase it might give us goal otherwise we will miss the goal cause we wont be exploring this node since its already in visited set

# just removing the visited works absolutely fine but to not revisit te nodes already explored in that specific branch i introduced bestDepth
   
       return None


# ----------------------------------------------------------------------
# Q4: Iterative Deepening Search
# ----------------------------------------------------------------------
def iterativeDeepeningSearch(problem, maxDepth=10000):
    for depth in range(maxDepth+1):#+1 so that last depth is included
        result=depthLimitedSearch(problem,depth)
        if result is not CUTOFF:
            return result

    return None

 


# ----------------------------------------------------------------------
# Q5: Uniform-Cost Search
# ----------------------------------------------------------------------
def uniformCostSearch(problem):
    pq=PriorityQueue()
    visited=set()
    pq.push((problem.getStartState(),[],0),0)#parameters are tuple and priority 
    while pq.isEmpty()==False:
        state,path,cost=pq.pop()

        if problem.isGoalState(state):
            return path
        if state not in visited:
            visited.add(state)

            for nextState,paths,stepCost in problem.getSuccessors(state):
                pq.push((nextState,path+[paths],cost+stepCost),cost+stepCost)

    return None

               
# ----------------------------------------------------------------------
# Q6: Greedy Best-First Search
# ----------------------------------------------------------------------
def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    pq=PriorityQueue()
    expanded=set()
    pq.push((problem.getStartState(),[],0),0)
    while pq.isEmpty()==False:
      state,path,heuristicCost=pq.pop()
      if problem.isGoalState(state):
          return path
      if state not in expanded:
          expanded.add(state)
          for nextState,paths,stepCost in problem.getSuccessors(state):
              newHeuristic=heuristic(nextState,problem)
              pq.push((nextState,path+[paths],newHeuristic),newHeuristic)#greedy doesnot care about accumulated cost so we only push the heuristic value as priority
   
    return None
# ----------------------------------------------------------------------
# Q7: A* Search
# ----------------------------------------------------------------------
def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node with the lowest f(n) = g(n) + heuristic(n) first
    (graph search).
    """
    fringe = PriorityQueue()
    start_state = problem.getStartState()
    # Store (state, actions_list, g_cost)
    fringe.push((start_state, [], 0), 0 + heuristic(start_state, problem))
    expanded = set()
    while not fringe.isEmpty():
        state, actions, g_cost = fringe.pop()
        if problem.isGoalState(state):
            return actions
        if state not in expanded:
            expanded.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in expanded:
                    new_g = g_cost + stepCost
                    f = new_g + heuristic(successor, problem)
                    fringe.push((successor, actions + [action], new_g), f)

    return None


# Abbreviations
always_right = alwaysRightSearch
dfs = depthFirstSearch
bfs = breadthFirstSearch
dls = depthLimitedSearch
ids = iterativeDeepeningSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
astar = aStarSearch



#Q1 and 2  ,7 ,3(Rehab)
#Q4,5,6,8,9 (Tayyaba)



# def aStarSearch(problem, heuristic=nullHeuristic):
#         pq=PriorityQueue()
#         expanded=set()
#         pq.push((problem.getStartState(),[],0),0)
#         while pq.isEmpty()==False:
#           state,path,heuristicPathCost=pq.pop()
#           if problem.isGoalState(state):
#               return path
#           if state not in expanded:
#               expanded.add(state)
#               for nextState,paths,stepCost in problem.getSuccessors(state):
#                   newHeuristic=heuristic(nextState,problem)
#                   nextCost=stepCost+heuristicPathCost
#                   f=newHeuristic+nextCost
#                   pq.push((nextState,path+[paths],nextCost),f)#we are pusing next cost as the accumulated cost and f as the  priority where f is cost +heuristic
       
#         return None