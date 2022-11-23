from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        self.model.grid.move_to_empty(self)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        pass

        # TODO: get next position direction

        # if nextPosition.isAvailable:
        #     self.move()
        #     return 
        # Else pass
    
