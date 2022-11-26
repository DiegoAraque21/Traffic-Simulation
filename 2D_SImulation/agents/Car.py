from mesa import Agent
from agents.Obstacle import Obstacle
from Node import GraphNode
from agents.Traffic_Light import Traffic_Light
from agents.Road import Road
from agents.Destination import Destination

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, graph, end_node):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.graph = graph
        self.end_node = end_node
        self.best_route = []

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        self.model.grid.move_to_empty(self)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if len(self.best_route) == 0:
            self.best_route = self.get_nearest_path()
            print(self.end_node.position)
            print(self.best_route)
        else:
            print(self.best_route)
        # TODO: get next position direction

        # if nextPosition.isAvailable:
        #     self.move()
        #     return 
        # Else pass
    

    def get_nearest_path(self):
        """Returns a list of tuples as a path from the given start to the given end in the given board"""
        # assign the start node as the current node
        start = GraphNode(None, None, self.pos)
        # assign the end node as the goal node
        end = self.end_node

        # initilized list to keep track of the nodes that have been visited
        queue= []
        visited = []

        # add the start node to the queue
        queue.append(start)

        # loop until the queue is empty, if it is no path is found
        while len(queue) > 0:
            
            # get the firs node
            current_node = queue[0]
            current_index = 0

            #  select the node with less f value
            for index, item in enumerate(queue):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # remove the current node from the queue
            queue.pop(current_index)
            # add the current node to the visited list
            visited.append(current_node)

            # if the current node is the goal node, return the path
            if current_node == end:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                return path[::-1]

            #  get agents in my current position
            arrAgents = self.model.grid.get_cell_list_contents(current_node.position)
            currentAgent = None
            isTrafficLight = False
            #  check if it contains a traffic light or normal road
            for agent in arrAgents:
                if isinstance(agent, Traffic_Light):
                    isTrafficLight = True
                    currentAgent = agent
                elif isinstance(agent, Road):
                    currentAgent = agent
                else:
                    pass
            
            # array of possible steps
            possible_steps = []
            
            if isTrafficLight:
                # get type of the traffic light, and their possible steps respectively
                if agent.type == "U":
                    possible_steps = self.get_possible_steps([(0,1), (1,1)], current_node, possible_steps)
                elif agent.type == "A":
                    possible_steps = self.get_possible_steps([(0,-1), (-1,-1)], current_node, possible_steps)
                elif agent.type == "R":
                    possible_steps = self.get_possible_steps([(1,0), (1,1)], current_node, possible_steps)
                elif agent.type == "L":
                    possible_steps = self.get_possible_steps([(-1,0), (-1,-1)], current_node, possible_steps)
                    
            else:
                # it is a road, get the possible steps
                if currentAgent.direction == "Left":
                    possible_steps = self.get_possible_steps([(-1,1),(-1,0), (-1,-1)], current_node, possible_steps)
                elif currentAgent.direction == "Right":
                    possible_steps = self.get_possible_steps([(1,1),(1,0), (1,-1)], current_node, possible_steps)
                elif currentAgent.direction == "Up":
                    possible_steps = self.get_possible_steps([(-1,1), (0,1),(1,1)], current_node, possible_steps)
                elif currentAgent.direction == "Down":
                    possible_steps = self.get_possible_steps([(-1,-1), (0,-1),(1,-1)], current_node, possible_steps)
        
            
            # loop through the possible steps
            for step in possible_steps:
                
                # check if the step is in the visited list
                for visited_node in visited:
                    if visited_node == step:
                        continue

                # calculate respective values, include the euristic distance
                step.g = current_node.g + 1
                step.h = ((step.position[0] - end.position[0]) ** 2) + ((step.position[1] - end.position[1]) ** 2)
                step.f = step.g + step.h

                # check if the step is in the queue
                for not_visited in queue:
                    if not_visited == step and step.g > not_visited.g:
                        continue
                
                # add the step to the queue
                queue.append(step)

            

            
    def get_possible_steps(self, origin_positions, node, possible_steps):
        for origin_pos in origin_positions:
            pos = (node.position[0] + origin_pos[0], node.position[1] + origin_pos[1])
            if pos[1] > (len(self.graph) - 1) or pos[1] < 0 or pos[0] > (len(self.graph[0]) -1) or pos[0] < 0:
                continue


            if isinstance(self.graph[len(self.graph) - 1 - pos[1]][pos[0]].agent, Obstacle):
                continue

            if isinstance(self.graph[len(self.graph) - 1 - pos[1]][pos[0]].agent, Destination) and self.graph[len(self.graph) - 1 - pos[1]][pos[0]].agent != self.end_node.agent:
                continue

            possible_step = GraphNode(None, node, pos)

            possible_steps.append(possible_step)

        return possible_steps