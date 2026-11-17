"""
griever_hole.py
---------------
Questions 8 and 9: escaping through the Griever Hole.

The Griever Hole only opens after the runners have entered the escape code.
The pieces of the code (marked K in the maze) are scattered through the
corridors. Thomas has to pick up ALL of them, in any order, and then reach the
exit E. Picking up a piece happens automatically when he steps onto its cell.

Try it once you are done:
    python runner.py -l keys_small -p keys -a bfs
    python runner.py -l keys_medium -p keys -a astar -H keyhunt
"""

import util
from problems import SearchProblem, mazeDistance


class KeyHuntProblem(SearchProblem):
    """
    Q8: Collect every code piece, then reach the exit.

    You choose the state representation, with two requirements:
      1. A state must be HASHABLE (tuples, frozensets, ints, strings... but
         not lists, sets or dicts), because your search keeps them in sets.
      2. A state must be a TUPLE whose FIRST element is Thomas's (row, col)
         position. The display and the grader read state[0].

    Keep the state small: store only what you need to know to decide what
    happens next. Do NOT put the whole maze in the state.
    """

    def __init__(self, maze):
        self.maze = maze
        self.startPosition = maze.start
        self.keys = tuple(maze.keys)      # positions of all code pieces
        self.exit = maze.exit
        self.heuristicInfo = {}           # scratch space for your heuristic
        # Bookkeeping for the display and the grader. Do not touch.
        self._expanded = 0
        self._expandedOrder = []
        "*** YOUR CODE HERE (optional: set up anything else you need) ***"

    def getStartState(self):
        # so wht we are doing is tht if a key is present in start state then after removing it return the rest keysLeft 
        keysLeft=[]
        for key in self.keys:
            if key!=self.startPosition:
              keysLeft.append(key)
        return (self.startPosition,frozenset(keysLeft))#frozenset is used to make the keysLeft hashable and also it will be unordered so that we can pick the keys in any order


    def isGoalState(self, state):
        return len(state[1]) == 0 and state[0]==self.exit
        

    def getSuccessors(self, state):
        """
        Returns a list of (successor, action, stepCost) triples.

        Use self.maze.neighbors(position), which gives the legal
        (action, nextPosition) pairs in North, South, East, West order, and
        self.maze.cost(nextPosition) for the step cost.
        """
        # Bookkeeping. Keep these two lines.
        self._expanded += 1
        self._expandedOrder.append(state[0])


        successors = []
        #maze.neighbours give list of pair
        #example
        #[("north",(1,2)),("south",(1,0)),("east",(2,1)),("west",(0,1))]
        # thats why i put for loop here
        for action ,nextPosition in self.maze.neighbors(state[0]):
            keysLeft=[]

            for key in state[1]:
             
             if key!=nextPosition:#here we say state[1] not self.keys bec it contain the original keys
                keysLeft.append(key)

            State=(nextPosition,frozenset(keysLeft))
            stepCost=self.maze.cost(nextPosition)
            successors.append((State, action,stepCost))
  
        return successors

    # --- Provided: you do not need to change anything below -------------
    def getCostOfActions(self, actions):
        """Total step cost of a sequence of actions (inf if it hits a wall)."""
        import maze as mazeModule
        if actions is None:
            return float('inf')
        pos = self.startPosition
        total = 0
        for action in actions:
            dr, dc = mazeModule.DELTA[action]
            pos = (pos[0] + dr, pos[1] + dc)
            if self.maze.isWall(pos):
                return float('inf')
            total += self.maze.cost(pos)
        return total

    def positionOf(self, state):
        return state[0]

    def expandedPositions(self):
        return list(self._expandedOrder)


def keyHuntHeuristic(state, problem):
    """
    Q9: A heuristic for KeyHuntProblem.

    It must be CONSISTENT (and therefore admissible): for every state s and
    successor s' reached with step cost c,  h(s) <= c + h(s'),  and h must be
    0 at goal states. The grader checks this.

    The more informed (larger) your heuristic is while staying consistent,
    the fewer states A* expands and the more points you earn.

    Useful tools:
      * problem.keys, problem.exit, and whatever your state stores
      * mazeDistance(pos1, pos2, problem.maze, problem.heuristicInfo) gives
        the true number of steps between two cells, and caches the result
      * util.manhattanDistance(pos1, pos2)
    """
    position = state[0]


    nodes=[position]
    for key in state[1]:
        nodes.append(key)
    nodes.append(problem.exit)

    # so we made a list containing all the nodes from sttart to exit
    connected=[nodes[0]]#starting position
    remaining=nodes[1:]#skip the starting and store from index 1 till end

    min=0
    total_min=0
    if  len(remaining)==0:
     return mazeDistance(position,problem.exit,problem.maze,problem.heuristicInfo)
    while len(remaining)>0:
        min=float('inf')#some very big number
        shortest_node=None

        for a in connected:
            for b in remaining:
                current_dist=mazeDistance(a,b,problem.maze,problem.heuristicInfo)
                if current_dist<min:
                    min=current_dist
                    shortest_node=b
                
        total_min+=min
        connected.append(shortest_node)
        remaining.remove(shortest_node)

    return total_min



    # maxDist=mazeDistance(position,problem.exit,problem.maze,problem.heuristicInfo)# we keep this as max dist at start bcause wht if theres no key left then this dist will be returned
    # for key in state[1]:
    #     dist=mazeDistance(position,key,problem.maze,problem.heuristicInfo)+mazeDistance(key,problem.exit,problem.maze,problem.heuristicInfo)
    #     if dist>maxDist:
    #       maxDist=dist


    # return maxDist

    return 0   # the trivial (but consistent!) heuristic

#APPROACH:1
# i had this approach for question 9 that wht we do is lets say there are 5 keys so calculate the shortest distance for 
#all the keys and choose the smallest one of all but thats very expensive becaause we hav to loop factorial times so 5 keys means 
# 5! =120 and so 10!=3628800 so we do small calculations 

#APPROACH 2
# where we find the dist btw [key+current_position]+[key+exit] anad we take the largest of this distance
# we take the max because others will be underestimate so we take the most neareer estimated distance which is the max 
#but this approach still gives alot of nodes so next we take this approach that

#APPROACH 3
# lets say we have Thoumus posiution ,k1,k2,k3,exit
#  The mazeDistance between each pair:

#   	K1	K2	K3	E
# T	    3	8	5	9
# K1		6	2	7
# K2			4	3
# K3				6
# but here keeping this thing in mind we find k1 distance from T but not vice versa otherwise there will be alot nodes being explored