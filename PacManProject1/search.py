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
    #getting the initial state of the problem and checking if its the goal state
    initial_state= problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    #because we are going to perform a dfs we will need a LIFO frontier,we will use a stack
    #we will push the fisrt node(initial_state,initial_path) in it
    #we aslo initialize a set which will keep the already explored states
    frontier=util.Stack()
    explored=set()
    frontier.push((initial_state, []))
    #while the frontier has nodes keep popping nodes and check if the state is expolred
    # and also if the state is the goal state
    # lastly,for each state (current_state) i take its succesors push new nodes to the frontier
    #as the formed ((next_state,path_for_the_next_state))
    # where path_for_the_next_state=path+a Direction
    while not (frontier.isEmpty()):
        current_state, path =frontier.pop()

        if current_state not in explored:


            explored.add(current_state)
            if problem.isGoalState(current_state):
                return path
            for next_state, direction, cost in problem.getSuccessors(current_state):
                new_path = path + [direction]
                frontier.push((next_state, new_path))

#in bfs same approach as in dfs but we use a lifo frontier


def breadthFirstSearch(problem):
    #getting the initial state of the problem and checking if its the goal state
    initial_state= problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    #because we are going to perform a dfs we will need a FIFO frontier,we will use a queue
    #we will push the fisrt node(initial_state,initial_path) in it
    #we aslo initialize a set which will keep the already explored states
    frontier=util.Queue()
    explored=[]
    frontier.push((initial_state, []))
    #while the frontier has nodes keep popping nodes and check if the state is expolred
    # and also if the state is the goal state
    # lastly,for each state (current_state) i take its succesors push new nodes to the frontier
    #as the formed ((next_state,path_for_the_next_state))
    # where path_for_the_next_state=path+a Direction
    while not (frontier.isEmpty()):
        current_state, path =frontier.pop()

        if current_state not in explored:


            explored.append(current_state)
            if problem.isGoalState(current_state):
                return path
            for next_state, direction, cost in problem.getSuccessors(current_state):
                new_path = path + [direction]
                frontier.push((next_state, new_path))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #the highest priority is the node with the least totalcoast and the quening goes that way
    #initialize frontier and explored list
    frontier = util.PriorityQueue()
    explored = []
    #push the initial_state into queue
    frontier.push((problem.getStartState(),[],0),0)
    #put initial_node(state) into the explored list
    (state,toDirection,toCost) = frontier.pop()
    explored.append((state,toCost))
    #while we havent reached goal
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        #for each succesor
        for suc in successors:
            flag = False
            #calculate the total cost for the succesor
            total_cost = toCost + suc[2]
            for (exploredState,exploredToCost) in explored:
            # we add the element only if the successor is unvisited
            # or we need to upadate his cost with a lower new
                if (suc[0] == exploredState) and (total_cost >= exploredToCost):
                    flag = True
                    break
            if not flag:
                #update the explored list with the point and push the point with priority number its totalCost
                frontier.push((suc[0],toDirection + [suc[1]],toCost + suc[2]),toCost + suc[2])
                explored.append((suc[0],toCost + suc[2]))
        (state,toDirection,toCost) = frontier.pop()

    return toDirection




    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0




def aStarSearch(problem, heuristic=nullHeuristic):
    #a star is an alogorithm in the family of best-first algorithms
    #a star uses as an evaluation function the sum if h(n),g(n),(F=h+g)
    #where h(n) the cost of the most cheap path from state n to a goal-states
    # and g(n)=the minimum cost to state n

    #getting the initial state of the problem and checking if its the goal state
    initial_state= problem.getStartState()
    if problem.isGoalState(initial_state):
        return []
    #because we are going to perform a dfs we will need a  frontier,we will use a priorityqueue
    #this queue prioritize the node with the minimum F=h(n)+minimumcost_to_n (evaluation)
    #we will push the fisrt node(initial_state,initial_path) in it
    #we aslo initialize a set which will keep the already explored states
    explored = []

    frontier = util.PriorityQueue()
    frontier.push((initial_state, [], 0), 0) #((state,path_to_state/coordinate,cost_to_state/coordinate),priority of this node)
    #after that i approach the solution in a way similar as dfs and bfs


    #while the frontier has nodes keep popping nodes and check if the state is expolred
    # and also if the state is the goal state
    # lastly,for each state (current_state) i take its succesors push new nodes to the frontier
    #as they are formed ((next_state,new_path,costofthenew_path)evaluation(priority))
    #priority=F_next_state (new_cost(cost to next_state)+ h(minimum cost from next_state to Goal))
    while not frontier.isEmpty():
        current_state, path, old_cost = frontier.pop()

        if current_state not in explored:
            explored.append(current_state)

            if problem.isGoalState(current_state):
                return path
            for next_state, direction, cost in problem.getSuccessors(current_state):
                new_path = path + [direction]
                new_cost = old_cost + cost
                F_next_state = new_cost + heuristic(next_state,problem)
                frontier.push((next_state, new_path, new_cost),F_next_state)

    util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
