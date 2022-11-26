class GraphNode():
    """A box class for A* Pathfinding"""

    def __init__(self, agent = None, parent = None, position = None):

        self.agent = agent
        self.parent = parent
        self.position = position or agent.pos
        self.adjacentNodes = []

        #El costo de moverme de la celda inicial a la posicion actual 
        self.g = 0
        
        #Distancia euclideana al destino (pitagoras)
        self.h = 0

        # g + h 
        self.f = 0

    def __eq__(self, other):
        if self.agent == None and other.agent == None:
            return self.position == other.position
        elif self.agent == None or other.agent:
            return self.position == other.agent.pos
        else:
            return self.agent.pos == other.agent.pos
    

