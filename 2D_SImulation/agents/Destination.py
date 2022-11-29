from mesa import Agent
from agents.Car import Car


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


    def step(self):
        self.clean_cars
        

    def clean_cars(self):
        """Remove cars that are in destiny"""
        # Get destination agents
        agents = self.get_cell_agents(self.pos)

        # Remove cars
        for a in agents:
            if isinstance(a, Car):
                self.model.grid.remove_agent(a)


    def get_cell_agents(self, position):
        """Get list of agents of a cell."""
        # Get neighbors including center cell
        neighbors = self.model.grid.get_neighbors(position, False, True)

        # Get agents in position
        agents = []
        for n in neighbors:
            if n.pos == position:
                agents.append(n)

        return agents