# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    "Here we are initializing things we will need for the function"
    "We will use a set to keep track of all of the visited nodes"
    VistedNodes = set()
    "We'll implement a stack for this search since we will need to follow the LIFO ordering"
    NodeStack = util.Stack()
    "Pushing the initial state to the stack"
    NodeStack.push((problem.getStartState(), [], 0))

    while NodeStack:
        "Base case for the search. If its an empty stack then the search is done"
        if NodeStack.isEmpty():
            return []

        "Now we have to pop a state from the NodeStack"
        nState, nAction, nCost = NodeStack.pop()

        "Now that we have a state to check, we check if it is our goal state"
        if problem.isGoalState(nState):
            return nAction

        "Checking if the node has already been visted"
        if nState in VistedNodes:
            continue

        "This adds the node to the Visted Node ds if it hasnt been visted already and isnt the goal state"
        VistedNodes.add(nState)

        "This is the part that iterates through the tree"
        "we are getting the next states that are currently availible from the current state"
        for State, Action, Cost in problem.getSuccessors(nState):
            "pushing the next states onto the Node Stack"
            NodeStack.push((State, nAction+[Action], nCost))



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    "Used to keep track of all of the visted nodes"
    VisitedNodes = set()
    "We'll implement a queue for this search since BFS exapnds the shallowest nodes in the tree therefor we need to follow FIFO"
    NodeQueue = util.Queue()
    "Pushing the initial state to the queue"
    NodeQueue.push((problem.getStartState(), [], 0))

    while NodeQueue:
        "Base case for the search. If its an empty queue then the search is done"
        if NodeQueue.isEmpty():
            return []

        "Now we have to push a state from the Node queue"
        nState, nAction, nCost = NodeQueue.pop()

        "Now that we have a state to check, we check if it is our goal state"
        if problem.isGoalState(nState):
            return nAction

        "Checking if the node has already been visited"
        if nState in VisitedNodes:
            continue

        "This adds the node to Visited Nodes if if hasnt been visited already and isnt our goal state"
        VisitedNodes.add(nState)

        "This is the part that iterates through the tree"
        "we are getting the next states that are currently availible from the current state"
        for State, Action, Cost in problem.getSuccessors(nState):
            "pushing the next states onto the Node Queue"
            NodeQueue.push((State, nAction+[Action], nCost))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    "So the UniformCostSearch is literally the same as the BFS but it expands with the lowest node cost instead"
    "We will be using a Priority Queue as the Data Structure"
    "I will note the differences between the two instead of redocumenting it all the same"

    VisitedNodes = set()
    NodePriorityQueue = util.PriorityQueue()
    "setting the initial cost of the start state with 0"
    NodePriorityQueue.push((problem.getStartState(), [], 0), 0)

    while NodePriorityQueue:

        if NodePriorityQueue.isEmpty():
            return []

        nState, nAction, nCost = NodePriorityQueue.pop()

        if problem.isGoalState(nState):
            return nAction

        if nState in VisitedNodes:
            continue

        VisitedNodes.add(nState)

        for State, Action, Cost in problem.getSuccessors(nState):
            "Because of the Priority Queue taking into consideration the cost, we have to add a second argument with the cost of reaching said node"
            NodePriorityQueue.push((State, nAction+[Action], nCost), problem.getCostOfActions(nAction+[Action]))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    "The A* search also uses the PriorityQueue Data Structure but it uses the sum of nCost + heuristic function return value to determine the cost"

    VisitedNodes = set()
    NodePriorityQueue = util.PriorityQueue()
    NodePriorityQueue.push((problem.getStartState(), [], 0), 0)

    while NodePriorityQueue:

        if NodePriorityQueue.isEmpty():
            return []

        nState, nAction, nCost = NodePriorityQueue.pop()

        if nState in VisitedNodes:
            continue

        VisitedNodes.add(nState)

        for State, Action, Cost in problem.getSuccessors(nState):
            NodePriorityQueue.push((State, nAction+[Action], nCost), problem.getCostOfActions(nAction+[Action]) + heuristic(State, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
