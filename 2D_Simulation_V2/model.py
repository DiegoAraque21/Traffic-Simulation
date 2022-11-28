from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.Car import Car
from agents.Destination import Destination
from agents.ObstacleCar import ObstacleCar
from agents.Obstacle import Obstacle
from agents.Road import Road
from agents.Traffic_Light import Traffic_Light
import json

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("./map_templates/mapDictionary.json"))

        self.traffic_lights = []
        self.destinations = []
        self.spawn_cars_cells = [(0,0), (0,24), (23,0), (23,24)]
        self.tl_direction = {
            "U": "Up",
            "R": "Right",
            "L": "Left",
            "A": "Down",
        }
        self.num_agents = N
        self.running = True
        self.counter = 0

        with open('./map_templates/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Road agents
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    # Traffic light agents
                    elif col in ["U", "R", "L", "A"]:
                        # Place traffic light agent
                        tl_id = f"tl_{r*self.width+c}"
                        agent = Traffic_Light(tl_id, self, False if (col == "U" or col =="A") else True, int(dataDictionary[col]), col)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)

                        # Place also a road agent with the correspoding direction
                        self.traffic_lights.append(agent)
                        road = Road(f"r_{r*self.width+c}", self, self.tl_direction[agent.type])
                        self.grid.place_agent(road, (c, self.height - r - 1))

                    # Obstacle agents
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    # Destination agents
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))
                        self.schedule.add(agent)


        self.spawn_cars()        


        # Spawn obstacle cars to test
        # obstacle_cars = [(19,23), (20,23), (21,23), (22,23), (22,22), (22,21)]
        # for i in range(len(obstacle_cars)):
        #     obstacle_car = ObstacleCar(9000+i, self)
        #     self.grid.place_agent(obstacle_car, obstacle_cars[i])


    def step(self):
        '''Advance the model by one step.'''
        self.spawn_cars()
        
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()

    
    def spawn_cars(self):
        """Spawn cars at the corners of the grid."""
        # For each spawn spot
        for cell in self.spawn_cars_cells:

            if self.random.random() < 0.2:
                destination = self.random.choice(self.destinations) # Random destination
                cell_agents = self.get_cell_agents(cell) # Get cell agents

                # Search a car in agents
                for a in cell_agents:
                    if isinstance(a, Car):
                        continue # Don't spawn

                # Spawn car
                car = Car(8000+self.counter, self, destination)
                self.grid.place_agent(car, cell)
                self.schedule.add(car)
                self.counter += 1


    def get_cell_agents(self, position):
        """Get list of agents of a cell."""
        # Get neighbors including center cell
        neighbors = self.grid.get_neighbors(position, False, True)

        # Get agents in position
        agents = []
        for n in neighbors:
            if n.pos == position:
                agents.append(n)

        return agents