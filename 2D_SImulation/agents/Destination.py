from mesa import Agent
from agents.Car import Car


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


    def step(self):
        self.clean_cars()
        

    def clean_cars(self):
        """Remove cars that are in destiny"""
        # Get destination agents
        agents = self.model.get_cell_agents(self.pos)

        # Remove cars
        for a in agents:
            if isinstance(a, Car):
                self.model.grid.remove_agent(a)