import random
import math
from environment import Agent, Environment
from simulator import Simulator
import sys
from searchUtils import searchUtils


class SearchAgent(Agent):
    """ An agent that drives in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env,location=None):
        super(SearchAgent, self).__init__(env)     # Set the agent in the evironment 
        self.valid_actions = self.env.valid_actions  # The set of valid actions
        self.action_sequence=[]
        self.searchutil = searchUtils(env)

    def choose_action(self):
        """ The choose_action function is called when the agent is asked to choose
            which action to take next"""

        # Set the agent state and default action
        action=None
        #print(self.action_sequence)
        if len(self.action_sequence) >=1:
            action = self.action_sequence[0] 
        if len(self.action_sequence) >=2:
            self.action_sequence=self.action_sequence[1:]
        else:
            self.action_sequence=[]
        return action

    def drive(self,startstate, goalstates,inputs):
        """Write your algorithm for self driving car"""
        act_sequence=[]
        route = []
        for goal in goalstates:
            goalReached, path = self.A_star(startstate, goal)
            act_sequence.extend(path)
        return act_sequence

    def A_star(self, start, goal):
        closedSet = []
        openSet = [start["location"]]
        cameFrom = {}
        gScore = {}
        gScore[start["location"]] = 0  # starting coordinate is 0
        # gScore.append(start.values())
        fScore = {}
        fScore[start["location"]] = self.heuristic_cost_estimate(start["location"], goal["location"])
        current = {}

        while len(openSet) > 0:
            # Lowest fScore
            min_val = min(fScore.values())
            current["location"] = [k for k, v in fScore.items() if v == min_val][0]
            if current["location"] == goal["location"]:
                print('Goal Reached!')
                return True, self.reconstruct_path(cameFrom, current["location"])
            # remove current from openSet and closedSet, add to closedSet.
            openSet.remove(current["location"])
            fScore.pop(current["location"], None)
            closedSet.append(current["location"])
            action = ["forward", "forward-2x", "forward-3x", "left", "right"]
            for i in action:
                neighbor = self.env.applyAction(self, current, i)
                if neighbor["location"] == current["location"]:
                    continue
                tentative_gScore = gScore[current["location"]] + self.heuristic_cost_estimate(current["location"],
                                                                                              neighbor[
                                                                                                  "location"]) * 2  # undo the divide by 2 in heuristic_cost_estimate function as we only want total dist.
                if neighbor["location"] not in openSet:
                    openSet.append(neighbor["location"])
                elif tentative_gScore > gScore[neighbor["location"]]:
                    continue
                cameFrom[neighbor["location"]] = (current["location"], i)  # returns (location, action)
                gScore[neighbor["location"]] = tentative_gScore
                fScore[neighbor["location"]] = gScore[neighbor["location"]] + self.heuristic_cost_estimate(
                    neighbor["location"], goal["location"])

        if current["location"] == goal["location"]:
            print('Goal Reached!')
            return True, self.reconstruct_path(cameFrom, current["location"])
        else:
            print('Goal Not Reachable')
            return False, self.reconstruct_path(cameFrom, current["location"])

    def reconstruct_path(self, cameFrom, current):
        total_path = []
        total_path.append(
            current)  # arranges all the coordinates,actions in a list. pull action out from here into action sequence. it is stored from end to start.
        while current in cameFrom.keys():
            total_path.append(current)
            current = cameFrom[current]
        total_path.append(current)
        return total_path


    def heuristic_cost_estimate(self, start, goal):
        distance_x = abs(start[0] - goal[0])
        distance_y = abs(start[1] - goal[1])
        return (distance_x + distance_y)/2



    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """
        startstate = self.state
        goalstates =self.env.getGoalStates()
        inputs = self.env.sense(self)
        self.action_sequence = self.drive(startstate, goalstates,inputs)
        action = self.choose_action()  # Choose an action
        self.state = self.env.act(self,action)        
        return
        

def run(filename):
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    env = Environment(config_file=filename,fixmovement=False)
    
    agent = env.create_agent(SearchAgent)
    env.set_primary_agent(agent)
    
    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    sim = Simulator(env, update_delay=2)
    
    ##############
    # Run the simulator
    ##############
    sim.run()


if __name__ == '__main__':
    run(sys.argv[1])
