from mesa import Agent
from agents.Obstacle import Obstacle
from Node import GraphNode

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
            self.best_route = self.astar( GraphNode(self) )
        else:
            print(self.best_route)
        # TODO: get next position direction

        # if nextPosition.isAvailable:
        #     self.move()
        #     return 
        # Else pass
    

    def astar(self, start_node):
        """Returns a list of tuples as a path from the given start to the given end in the given board"""
        pass