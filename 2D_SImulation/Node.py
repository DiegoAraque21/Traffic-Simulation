class GraphNode():
    """A box class for A* Pathfinding"""

    def __init__(self, agent = None, parent = None):
        self.agent = agent
        self.parent = parent
        self.position = agent.pos
        self.adjacentNodes = []

        #El costo de moverme de la celda inicial a la posicion actual 
        self.g = 0
        
        #Distancia euclideana al destino (pitagoras)
        self.h = 0

        # g + h 
        self.f = 0

    def __eq__(self, other):
        return self.agent.pos == other.agent.pos
    

