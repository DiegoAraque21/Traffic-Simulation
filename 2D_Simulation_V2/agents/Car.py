from mesa import Agent
from agents.Road import Road
from agents.ObstacleCar import ObstacleCar
from queue import PriorityQueue
import math

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """
    

    def __init__(self, unique_id, model, end):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.end = end
        self.route = {}
        self.blocked_cells = []


    def step(self):
        """ 
        Determines the new direction it will take, and then moves.
        """

        # If car has arrived to the end
        if self.pos == None or self.pos == self.end:
            return # Await until destiny removes car

        # If there isn't a route
        if not self.route:
            # If there are no blocked cells
            self.route = self.get_route(self.pos) # Get route
            return

        # If there is a red light in front of agent, don't move until it changes to green
        if self.check_red_light():
            return

        # Check if the next position is available
        next_pos = self.route[self.pos] # Get the next route position
        next_pos_available = self.check_road_availability(next_pos)

        # If the next pos in not available
        if not next_pos_available:

            # If the next position is a diagonal, the agent can't wait because it will make traffic in a new street
            front_cell = self.get_front_cell(self.pos) # Get front cell
            if next_pos != front_cell:
                self.change_route()
                return

            # If traffic on route
            if self.check_traffic_on_route(): 
                self.change_route()
                return

            # If the next pos isn't available, but there is no traffic, wait
            return
        
        # Move agent to next cell
        self.model.grid.move_agent(self, next_pos)


    def get_route(self, start):
        """Find the best route from current position to destination."""

        # Maps to store values
        g_values = {}
        f_values = {}

        # Init all g and f values of the cells at infinite
        for i in range(self.model.width):
            for j in range(self.model.height):
                g_values[(i, j)] = float('inf')
                f_values[(i, j)] = float('inf')

        # Set start cell values
        g_values[start] = 0
        f_values[start] = h_value_start = self.h(start, self.end)

        # Create a priority queue to store wich cells are better options for the route
        cells = PriorityQueue()
        # The priority will be the lowest f value, then the h value
        cells.put((f_values[start], h_value_start, start))

        route = {} # Dictionary to store the previous route cell of a current cell
        while not cells.empty():
            # Get the cell of most priority (less f value) and get its position
            curr_cell = cells.get()[2]

            # If cell is the end break
            if curr_cell == self.end:
                break

            # Get possible cells to move from this current cell
            possible_cells = self.get_possible_next_cells(curr_cell)
            
            # Compute new values for all possible cells
            for possible_cell in possible_cells:
                g_value_temp = g_values[curr_cell] + 1
                h_value_temp = self.h(possible_cell, self.end)
                f_value_temp = h_value_temp + g_value_temp

                # If this f_value is smaller than the stored one
                if f_value_temp < f_values[possible_cell]:
                    # Update values because its cheaper to get from this new route
                    g_values[possible_cell] = g_value_temp
                    f_values[possible_cell] = f_value_temp

                    # Add to the priority cells list the new values
                    cells.put((f_value_temp, h_value_temp, possible_cell))

                    # Indicate that the best possible way to get to this cell is by current cell
                    route[possible_cell] = curr_cell

        # The route map its in reverse order, its useful to get from end to start, so we we need to invert it
        normal_route={}

        # If there is a value in the route for the end, it means the end was reached successfully
        if route.get(self.end):
            # Get normal route by inverting the path of route
            cell = self.end
            while cell != start:
                normal_route[route[cell]] = cell
                cell = route[cell]

            self.blocked_cells = []
            return normal_route

        # If end wasn't reached, then there is no valid route
        self.blocked_cells = []
        return None

    
    def h(self, cell1, cell2):
        """Get the euclidian distance from one cell to another one."""
        x1, y1 = cell1
        x2, y2 = cell2
        return math.sqrt(abs(x1 - x2) + abs(y1 - y2))


    def get_possible_next_cells(self, cell):
        """Get posible next cells to add in the route."""
        # Depending on the road direction, the next possible route cells will be these additions
        coordinates_additions = {
            "Up": [(-1, 1), (0, 1), (1, 1)],
            "Left": [(-1, -1), (-1, 0), (-1, 1)],
            "Down": [(-1, -1), (0, -1), (1, -1)],
            "Right": [(1, -1), (1, 0), (1, 1)]
        }

        # Find the direction of the current route cell
        curr_direction = self.get_road_direction(cell)

        # Get the additions of the route cell
        additions = coordinates_additions[curr_direction]
        # Create possible cells adding the corresponding values to the current route cell
        possible_cells = [(cell[0] + add[0], cell[1] + add[1]) for add in additions]

        # Get the forbidden directions for lateral cells to asure the route follows the road way
        forbidden_directions = {}
        if curr_direction in ["Up", "Down"]:
            forbidden_directions[possible_cells[0]] = "Right"
            forbidden_directions[possible_cells[2]] = "Left"

        if curr_direction in ["Left", "Right"]:
            forbidden_directions[possible_cells[0]] = "Up"
            forbidden_directions[possible_cells[2]] = "Down"

        # Filter blocked cells
        if len(self.blocked_cells) != 0:
            for cell in possible_cells:
                # If cell is blocked remove it
                if cell in self.blocked_cells:
                    possible_cells.remove(cell)

        # Get the next possible cells depending on the roads
        results = []

        # Get neighbors of the current cell
        neighbors = self.model.grid.get_neighbors(cell, True, True)
        for n in neighbors:
            # If neighbor is in a possible cell
            if n.pos in possible_cells:

                # If its a destination, it will only be valid if its the end
                if n.pos == self.end:
                    results.append(n.pos) # Append the destination position

                # If its a road
                if isinstance(n, Road):
                    # Get cell's forbidden direction
                    forbidden_direction = forbidden_directions.get(n.pos)

                    # If there isn't a forbidden direction or it is different from cell direction
                    if not forbidden_direction or forbidden_direction != n.direction:
                            results.append(n.pos) # Append the road position

        return results


    def check_red_light(self):
        """Check if there is a red light in front of agent."""
        # Get front cell of agent
        front_cell = self.get_front_cell(self.pos)

        # Search front cell position in traffic lights
        for i in range(len(self.model.traffic_lights)):
            # If traffic light posistion is front cell
            if front_cell == self.model.traffic_lights[i].pos:
                return not self.model.traffic_lights[i].state # Return true if its red

        return False


    def get_front_cell(self, cell):
        """Get the front cell of a based on direction of given cell"""
        # Get current road direction
        curr_direction = self.get_road_direction(cell)

        # Get front cell position
        additions = {
            "Up": (0, 1),
            "Left": (-1, 0),
            "Down": (0, -1),
            "Right": (1, 0)
        }
        addition = additions[curr_direction]
        front_cell = (self.pos[0] + addition[0], self.pos[1] + addition[1])
        return front_cell



    def get_road_direction(self, position):
        """Get the direction of a road agent."""
        # Get neighbors including center cell
        neighbors = self.model.grid.get_neighbors(position, False, True)

        # Find a road in the given position
        for n in neighbors:
            if isinstance(n, Road) and n.pos == position:
                return n.direction

        # If no road was founded in the position
        return None


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


    def check_road_availability(self, position):
        """Check if a road is available."""
        # Array that contains roads to check
        roads_to_check = [position] # Begin with next route position

        front_cell = self.get_front_cell(self.pos) # Get front cell of agent
        curr_direction = self.get_road_direction(self.pos) # Get current direction
        
        # If next route position isn't front cell, then check that the lateral cells are also available
        if position != front_cell:
            if curr_direction in ["Left", "Right"]:
                lateral_cell = (self.pos[0], position[1])
            else:
                lateral_cell = (position[0], self.pos[1])
            roads_to_check.append(lateral_cell)
        
        # Check that all roads are available
        available = True
        for road in roads_to_check:
            # Get road agents
            agents = self.get_cell_agents(road)

            # Variables to store if agents were founded
            found_road = False
            found_car = False

            for a in agents:
                # Mark if its a road
                if isinstance(a, Road):
                    found_road = True
                # Mark if its a car
                if isinstance(a, Car) or isinstance(a, ObstacleCar):
                    found_car = True

            # If it found a road and a car, the cell is not available
            if found_road and found_car:
                available = False

        return available


    def check_traffic_on_route(self):
        """Function that indicates if the current route has traffic."""

        # Get next 5 route positions of the route
        n_positions = 5
        counter = 0
        cells = []
        cell = self.pos # Begin with next position
        while counter < n_positions:
            cell = self.route.get(cell)
            if cell:
                cells.append(cell)
            counter += 1

        # If there is a red light in those next positions, there is no real traffic so wait
        for cell in cells:
            for i in range(len(self.model.traffic_lights)):
                # If there is a red traffic light in a cell
                if cell == self.model.traffic_lights[i].pos and not self.model.traffic_lights[i].state:
                    return False # Return no traffic

        # Get amount of cars in those cells to get if there is traffic
        n_cars = 0
        for cell in cells:
            # Get cell agents
            agents = self.get_cell_agents(cell)
            for a in agents:
                # If there is a car
                if isinstance(a, Car) or isinstance(a, ObstacleCar):
                    n_cars += 1 # Increase counter

        # iF true is there are many cars, because there is traffic
        traffic = n_cars >= 5

        if traffic:
            # Add blocked cells to prevent getting a route over them
            self.blocked_cells = cells
            
        return traffic # Return result
            

    def change_route(self):
        """Move car to any available cell and get a new route."""
        # Get possible next cells
        possible_cells = self.get_possible_next_cells(self.pos)

        # From possible cells, get the available ones
        available_cells = [cell for cell in possible_cells if self.check_road_availability(cell)]

        # If there are not available cells to change, wait in that cell
        if len(available_cells) == 0:
            return

        # Select one random available cell
        next_cell = self.random.choice(available_cells)

        # Move car to next available cell and calculate new route from there
        self.model.grid.move_agent(self, next_cell)
        self.route = self.get_route(next_cell)

        # Note: when we need to change the route, the car will first move to any available
        # cell and then calculate the new route from there to prevent stop the car
        # to calculate the route from the current position and generate more traffic