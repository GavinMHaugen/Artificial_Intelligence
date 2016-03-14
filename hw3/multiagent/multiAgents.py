# multiAgents.py
# --------------
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

# Gavin Haugen
# 108809993
# 3/11/16


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        oldFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPositions = successorGameState.getGhostPositions()

        if newPos in newGhostPositions:
          return 0
        if len(oldFood) == len(newFood):
          mindist = 9999
          for food in newFood:
            dist = manhattanDistance(newPos, food)
            if dist < mindist:
              mindist = dist
          return 1 / float(mindist)
        return 2

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #just going to make the MinimaxAgent function return a recursive sub function:
        def RecursiveMiniMax(gameState, depth, agent, Max, Root):

          #Base Case for our algorithm
          if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)

          #Finding the legal actions for the given agent
          legalActions = gameState.getLegalActions(agent)

          #PacMans actions
          #now we look for our Max option which happens to be our best case option
          if Max:
            action = None 
            SuccessorState = None
            MaxScore = -99999

            for actions in legalActions:
              #set the successor state
              SuccessorState = gameState.generateSuccessor(agent, actions)
              #Recursively call the function to find the first ghost agent
              ActionValue = RecursiveMiniMax(SuccessorState, depth, 1, False, False)
              #If our ActionValue is bigger than our old max then we must set it as the new max
              if ActionValue > MaxScore:
                MaxScore = ActionValue
                action = actions

            #if our action that we are looking for is at the root then return the root
            if Root:
              return action
            #if not, then we just return our maxscore at the current depth
            else:
              return MaxScore


          #Ghost Agent actions
          #now we look for our Min option
          else:
            SuccessorState = None
            MinScore = 99999

            for actions in legalActions:
              #set the successor state
              SuccessorState = gameState.generateSuccessor(agent, actions)
              #Recursively call the function to revert back to pacmans actions
              if (agent + 1) % gameState.getNumAgents() == 0:
                ActionValue = RecursiveMiniMax(SuccessorState, depth - 1, 0, True, False)
              #Recursively call the function for ghosts actions
              else:
                ActionValue = RecursiveMiniMax(SuccessorState, depth, agent + 1, False, False)

              #If our ActionValue is smaller than our old min then we must set it as the new min
              if ActionValue < MinScore:
                MinScore = ActionValue
            return MinScore

        #now we call the recursive function implemented above
        return RecursiveMiniMax(gameState, self.depth, 0, True, True)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Since this evaluation and the previous evaluation were very similar to each other
        #I'm just going to impolement it the same way but with the alpha and beta conditions
        def RecursiveAlphaBetaPruning(gameState, depth, agent, Max, Root, alpha, beta):

          #Base Case for our algorithm
          if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)

          #Finding the legal actions for the given agent
          legalActions = gameState.getLegalActions(agent)

          #PacMans actions
          #now we look for our Max option which happens to be our best case option
          if Max:
            action = None 
            SuccessorState = None
            MaxScore = -99999

            for actions in legalActions:
              #set the successor state
              SuccessorState = gameState.generateSuccessor(agent, actions)
              #Recursively call the function to find the first ghost agent
              ActionValue = RecursiveAlphaBetaPruning(SuccessorState, depth, 1, False, False, alpha, beta)
              #If our ActionValue is bigger than our old max then we must set it as the new max
              if ActionValue > MaxScore:
                MaxScore = ActionValue
                action = actions

              #checking our alpha beta conditions
              if ActionValue > alpha:
                alpha = ActionValue
              #if our beta is greater than our alpha value we break the loop
              if beta < alpha:
                break

            #if our action that we are looking for is at the root then return the root
            if Root:
              return action
            #if not, then we just return our maxscore at the current depth
            else:
              return MaxScore


          #Ghost Agent actions
          #now we look for our Min option
          else:
            SuccessorState = None
            MinScore = 99999

            for actions in legalActions:
              #set the successor state
              SuccessorState = gameState.generateSuccessor(agent, actions)
              #Recursively call the function to revert back to pacmans actions
              if (agent + 1) % gameState.getNumAgents() == 0:
                ActionValue = RecursiveAlphaBetaPruning(SuccessorState, depth - 1, 0, True, False, alpha, beta)
              #Recursively call the function for ghosts actions
              else:
                ActionValue = RecursiveAlphaBetaPruning(SuccessorState, depth, agent + 1, False, False, alpha, beta)

              #If our ActionValue is smaller than our old min then we must set it as the new min
              if ActionValue < MinScore:
                MinScore = ActionValue

              #checking our alpha beta conditions
              if ActionValue < beta:
                beta = ActionValue

              if beta < alpha:
                break

            return MinScore
        #now, we recurse
        return RecursiveAlphaBetaPruning(gameState, self.depth, 0, True, True, -99999, 99999)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
