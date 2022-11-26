from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.Car import Car
from agents.Destination import Destination
from agents.Obstacle import Obstacle
from agents.Road import Road
from agents.Traffic_Light import Traffic_Light
from Node import GraphNode
import json
import random

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):
        dataDictionary = json.load(open("./map_templates/mapDictionary.json"))
        self.traffic_lights = []
        self.global_matrix = []
        self.destinies = []

        with open('./map_templates/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            for r, row in enumerate(lines):
                newRow = []
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        newRow.append(GraphNode(agent))

                    elif col in ["U", "R", "L", "A"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if (col == "U" or col =="A") else True, int(dataDictionary[col]), col)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        newRow.append(GraphNode(agent))


                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        newRow.append(GraphNode(agent))


                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        node = GraphNode(agent)
                        self.destinies.append(node)
                        newRow.append(node)

                self.global_matrix.append(newRow)
        

        #Iterar por todos los vehiculos y asigarnles una copia de la matriz 


        spawn_arr = [(23,24)]
        for i in range(len(spawn_arr)):
            car_matrix = self.global_matrix.copy()
            print(len(self.destinies))
            carAgent = Car(8000+i, self, car_matrix, self.destinies[10])
            print(self.destinies[10].position)
            self.grid.place_agent(carAgent, spawn_arr[i])
            self.schedule.add(carAgent)

            
        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()