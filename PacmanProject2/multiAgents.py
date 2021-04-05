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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #evaluationFunction in order for pacman to go to the nearest food and avoid the gosts if they are very close
        newFood = successorGameState.getFood().asList()
        closestDot= float("inf")
        for food in newFood:
            closestDot = min(closestDot, manhattanDistance(newPos, food))


        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 3):
                return -float('inf')

        return successorGameState.getScore() + 1.0/closestDot







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
      Directions.STOP:
        The stop direction, which is always legal
      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    return self.MinimaxSearch(gameState, 1, 0 )

  def MinimaxSearch(self, gameState, currentDepth, agentIndex):
    #check if it is a terminal status
    if currentDepth > self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
    #implementing MINIMAX algorithm
    legalMoves = [action for action in gameState.getLegalActions(agentIndex) if action!='Stop']

    # UPDATING THE AGENTS AND THE DEPTH DEPENDING ON THE SITUATION
    nextIndex = agentIndex + 1
    nextDepth = currentDepth
    #if we are finished with all the agents we re initialize the index ,,,,we are changing layer
    if nextIndex >= gameState.getNumAgents():
        nextIndex = 0
        nextDepth += 1
    #for each legal action calculating recursively  the minimax value
    # Choose one of the best actions
    values = [self.MinimaxSearch( gameState.generateSuccessor(agentIndex, action) ,\
                                  nextDepth, nextIndex) for action in legalMoves]
    #pacman first move
    if agentIndex == 0 and currentDepth == 1:
        bestDecision = max(values)
        bestIndices = [index for index in range(len(values)) if values[index] == bestDecision]
        #pick randomly among the best
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    if agentIndex == 0:
        #since we are on the max-player(pacman) take the maximun of the result
        bestDecision = max(values)
        return bestDecision
    else:
        #since we have !=0 we are in the min player (ghosts) return the minimun result
        bestDecision = min(values)
        return bestDecision

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
    #geting the number of the agents  initializing a ,b  as infinity .
	num_of_agents = gameState.getNumAgents()
	value,action = self.alpha_value(gameState,float('-inf'),float('inf'),0,self.depth)
	return action
    #for the maximazing player in this case pacman
    def alpha_value(self,state,alpha,beta,agentNumber,depth):
    #terminating check
	if state.isWin() or state.isLose():
		return self.evaluationFunction(state),'none'

	Eval = float('-inf')
	actions = state.getLegalActions(agentNumber)
	bestAction = actions[0]
    #find the best action among the legal actions
	for action in actions:
		previous_Eval = Eval
		successorGameState = state.generateSuccessor(agentNumber,action)
        #if we reached the arbitrary depth or we are in leaf nodes
		if depth == 0 or successorGameState.isWin() or successorGameState.isLose():
			Eval = max(Eval,self.evaluationFunction(successorGameState))
		else:
			Eval = max(Eval,self.beta_value(successorGameState,alpha,beta,agentNumber+1,depth))

        #checking for pruning ,refining aplha value and storing th best move
		if Eval > beta:
			return Eval,action
		alpha = max(alpha,Eval)
		if Eval != previous_Eval:
			bestAction = action
	return Eval,bestAction
    #now for the minimazing player (the ghosts)

    def beta_value(self,state,alpha,beta,agentNumber,depth):


	Eval= float('inf')
	actions = state.getLegalActions(agentNumber)
	flag = False
	for action in actions:

		successorGameState = state.generateSuccessor(agentNumber,action)
        #leaf or arbitrary depth
		if depth == 0 or successorGameState.isWin() or successorGameState.isLose():
			Eval = min(Eval,self.evaluationFunction(successorGameState))
        #using a flag to decrease depth onlu if we have gone through all agents (complete layer )
		elif agentNumber == (state.getNumAgents() - 1):
			if flag == False:
				depth = depth -1
				flag=True
            #if we reached the depth
			if depth == 0:
				Eval = min(Eval,self.evaluationFunction(successorGameState))
			else:
				Eval = min(Eval,self.alpha_value(successorGameState,alpha,beta,0,depth)[0])

		else:
			Eval = min(Eval,self.beta_value(successorGameState,alpha,beta,agentNumber+1,depth))
		if Eval < alpha:
			return Eval
		beta = min(beta,Eval)

	return Eval

        util.raiseNotDefined()











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
    #util.raiseNotDefined()
    return self.ExpectiMax(gameState, 1, 0)
  #REALLY SIMILAR TO MINIMAX  BUT IN GHOST NODE (MINIMIZING PLAYER) RETURNS THE EXPECTED  ACTION
  def ExpectiMax(self, gameState, currentDepth, agentIndex):
    #checking if we are at termination
    if currentDepth > self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    #getting legal actions
    legalMoves = [action for action in gameState.getLegalActions(agentIndex) if action!='Stop']

    #intializing and refining values depending on the situation
    nextIndex = agentIndex + 1
    nextDepth = currentDepth
    if nextIndex >= gameState.getNumAgents():
        nextIndex = 0
        nextDepth += 1
    #get recursively the values
    values = [self.ExpectiMax( gameState.generateSuccessor(agentIndex, action) , nextDepth, nextIndex) for action in legalMoves]

    if agentIndex == 0 and currentDepth == 1:
        bestDecision = max(values)
        bestIndices = [index for index in range(len(values)) if values[index] == bestDecision]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    if agentIndex == 0:
        bestDecision = max(values)
        return bestDecision
    else:
        #min player return expected action
        bestDecision = sum(values)/len(values)
        return bestDecision

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    question 5: this will be an evaluation function based on distances
    the highest priority for pacman will be not being eaten by ghosts while simultaneously eating as
many dots as possible (however eating for this function is not more important than avoiding ghosts)
note that being to far from ghosts is meaningless as long as you have safe distance from them (lets say 5)
(thats why we take the max between 5 and distance_from_ghost in order not to favor positions that ghosts
 are already to far and are not being a threat for pacman while favoring the safe distance 5)
so we have this ->> score += max(Dist_from_Gost, 5) * 2  (multiplying by 2 makes the argument really strong because as we said the most importnat thing its not being eaten)
so now as we have strongly kept pacman away from ghosts we need to favor positions-moves that will make pacman eat as many dots as possible
so we have this ->>  score -=  minDistFromDot * 2 i subtract from the score the distance to the closest food multiplayed by 2 in order to get closer to the food in every move
This, however, i need to add a penalty for the remaining food because the above practice  make the pacman be avoid secluded food (food in a distant area)
so ->>>score -= 3.5 * len(dot_positions)(bonus if you minimize the number of the remaining food in general)
lastly,
i believe that we need to favor  pacman to eat the ghosts and add a bonus in eating capsules(subtract a value*its distance from capsules)
the value will be 4 to push pacman slightly being closer to capsules
so-->>score -= 4 * len(capsule_positions)


  """
  "*** YOUR CODE HERE ***"
  if currentGameState.isWin():
      return float("inf")
  if currentGameState.isLose():
      return - float("inf")


  score = scoreEvaluationFunction(currentGameState)
  newFood = currentGameState.getFood()
  dot_positions = newFood.asList()
  minDistFromDot = float("inf")

  for position in dot_positions:
      dist = util.manhattanDistance(position, currentGameState.getPacmanPosition())
      if (dist <  minDistFromDot):
          minDistFromDot = dist


  numghosts = currentGameState.getNumAgents() - 1
  i = 1
  Dist_from_Gost = float("inf")
  while i <= numghosts:
      nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
      Dist_from_Gost = min(Dist_from_Gost, nextdist)
      i += 1
  score += max(Dist_from_Gost, 5) * 2
  score -=  minDistFromDot * 2

  capsule_positions= currentGameState.getCapsules()
  score -= 3.5 * len(dot_positions)
  score -= 4 * len(capsule_positions)
  return score


# Abbreviation
better = betterEvaluationFunction
