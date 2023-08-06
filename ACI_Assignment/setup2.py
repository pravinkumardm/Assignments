import numpy as np
from copy import deepcopy

class Ration:
    '''
        This class will define the different types of resources as a single entity, easier to handle during the execution
    '''
    def __init__(self,milk,bread,dhal,rice,flour):
        self.milk = milk
        self.bread = bread
        self.dhal = dhal
        self.rice = rice
        self.flour = flour
    
    def __str__(self):
        return f"\tMilk:{self.milk}\n\tBread:{self.bread}\n\tDhal:{self.dhal}\n\tRice:{self.rice}\n\tFlour:{self.flour}"
    
    def __add__(self, other):
        return Ration(
        self.milk + other.milk,
        self.bread + other.bread,
        self.dhal + other.dhal,
        self.rice + other.rice,
        self.flour + other.flour,
        )
    
    def __sub__(self, other):
        return Ration(
        self.milk - other.milk,
        self.bread - other.bread,
        self.dhal - other.dhal,
        self.rice - other.rice,
        self.flour - other.flour,
        )
    
    def __mul__(self, val):
        return Ration(
        self.milk * val,
        self.bread * val,
        self.dhal * val,
        self.rice * val,
        self.flour * val,
        )
    
    def add_weights(self):
        return self.milk + self.bread + self.dhal + self.rice + self.flour

class Person:
    '''
    This defines a generic class called person which helps us keep track of the different type of people. 
    '''
    def __init__(self, milk, bread, dhal, rice, flour):

        self.ration = Ration(milk, bread, dhal, rice, flour)



Adult = Person(0,0,1,3,3)
Child = Person(3,1,0,0,0)

class MapCell:
    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type
    
    def compute_manhattan_distance(self, other):
        if self.accessible and other.accessible:
            return abs(self.x - other.x) + abs(self.y - other.y)
        else:
            return float('inf')

class Tent(MapCell):
    def __init__(self, x, y, adult, child):
        super().__init__(x, y, cell_type = 1)
        self.count_adult = adult
        self.count_child = child
        self.required = self.compute_requirement()
        self.accessible = True
        
    def compute_requirement(self):
        requirement = (Adult.ration * self.count_adult) + (Child.ration * self.count_child)
        return requirement
    
    def __str__(self):
        return f"Adults : {self.count_adult}\nChildren : {self.count_child}\nRequirement: \n{self.required}"


class Supply(MapCell):
    def __init__(self, x, y, milk, bread, dhal, rice, flour):
        super().__init__(x, y, cell_type = 3)
        self.supply = Ration(milk, bread, dhal, rice, flour)
        self.accessible = True
    
    def __str__(self):
        return "Supply"

class Path(MapCell):
    def __init__(self, x, y):
        super().__init__(x, y, cell_type=2)
        self.accessible = True
    
    def __str__(self):
        return "-Path-"

class NA(MapCell):
    def __init__(self, x, y):
        super().__init__(x, y, cell_type=0)
        self.accessible = False
    
    def __str__(self):
        return "--NA--"

class Agent:
    def __init__(self, cell):
        self.x, self.y = cell.x, cell.y
        self.CAPACITY = 15
        self.ration = Ration(0,0,0,0,0)
        self.distance_traveled = 0
        self.current_weight = self.ration.milk + self.ration.bread + self.ration.dhal + self.ration.flour + self.ration.rice

    def get_valid_moves(self, map_2d):
        valid_moves = []
        if (self.x-1>=0) and map_2d[self.x-1][self.y].accessible:
            valid_moves.append("LEFT")
        if self.x+1<=5 and map_2d[self.x+1][self.y].accessible:
            valid_moves.append("RIGHT")
        if self.y-1>=0 and map_2d[self.x][self.y-1].accessible:
            valid_moves.append("DOWN")
        if self.y+1<=5 and map_2d[self.x][self.y+1].accessible:
            valid_moves.append("UP")
        return valid_moves
    
    def pick_supplies(self, milk, bread, dhal, rice, flour, supply):
        pick_needed = Ration(milk, bread, dhal, rice, flour)
        if pick_needed.add_weights() <= 15:
            supply = supply - pick_needed
            self.ration += pick_needed

    def drop_supplies(self, required:Ration):
        # if drone has more than required, it will drop as much as needed else if it has less than what is needed it will drop all it has until it reaches zero
            self.ration.milk -= min([self.ration.milk, required.milk])
            self.ration.bread -= min([self.ration.bread, required.bread])
            self.ration.dhal -= min([self.ration.dhal, required.dhal])
            self.ration.rice -= min([self.ration.rice, required.rice])
            self.ration.flour -= min([self.ration.flour, required.flour])
            required.milk -= min([self.ration.milk, required.milk])
            required.bread -= min([self.ration.bread, required.bread])
            required.dhal -= min([self.ration.dhal, required.dhal])
            required.rice -= min([self.ration.rice, required.rice])
            required.flour -= min([self.ration.flour, required.flour])
    
    def hill_climbing(self, state):
        # Keep track of the current state.
        current_state = self.current_node
        
        while True:
            # Generate all possible next states
            neighbors = self.get_neighbors(state)
            
            # Find the neighbor with the lowest heuristic cost
            next_state = min(neighbors, key = lambda state: state.heuristic(state.current_node, state.agent.current_node))
            
            # If the heuristic function can't be decreased, we've found a local optimum.
            if next_state.heuristic(next_state.current_node, next_state.agent.current_node) >= current_state.heuristic(current_state.current_node, current_state.agent.current_node):
                return current_state
            
            # Move to the next state.
            current_state = next_state
            self.current_node = next_state.agent.current_node

    def get_neighbors(self, state):
        neighbors = []
        for tent in state.unvisited:
            # Generate a new state for each possible move
            new_state = deepcopy(state)
            new_state.current_node = tent
            neighbors.append(new_state)
        return neighbors

    def move_agent(self, direction:str):
        if direction.lower() in self.get_valid_moves():
            if direction.lower() == "left":
                self.x = self.x - 1
                self.distance_traveled += 1
            if direction.lower() == "right":
                self.x = self.x + 1
                self.distance_traveled += 1
            if direction.lower() == "up":
                self.y = self.y + 1
                self.distance_traveled += 1
            if direction.lower() == "down":
                self.y = self.y - 1
                self.distance_traveled += 1
            
class State:
    def __init__(self, start_x, start_y, map_2d):
        self.map = self.read_map(map_2d)
        self.current = self.map[start_x][start_y]
        self.visited = set()
        self.unvisited = set()
        self.commutes = 0
        self.supply_left = Ration(0,0,0,0,0)
        self.updated_unvisited()
        self.complete = False
        self.agent = Agent(self.current)

    def updated_unvisited(self):
        for row in self.map:
            for cell in row:
                if cell.cell_type ==  2:
                    self.unvisited.add(cell)

    def read_map(self, maparray):
        citymap = []
        for i, v1 in enumerate(maparray):
            rowitem = []
            for j, v2 in enumerate(v1):
                data = v2.split(",")
                cell_type = data[0]
                args = [float(x) for x in data[1:]]
                if cell_type.lower() == "supply":
                    print(data, cell_type)
                    rowitem.append(Supply(i,j, milk = args[0], bread = args[1], dhal=args[2], rice=args[3], flour=args[4]))
                elif cell_type.lower() == "tent":
                    rowitem.append(Tent(i, j, *args))
                elif cell_type.lower() == "path":
                    rowitem.append(Path(i,j))
                else:
                    rowitem.append(NA(i,j))
            citymap.append(rowitem)
        return citymap
    
    def compute_manhattan_distance(self, start, other):
        if start.accessible and other.accessible:
            return abs(start.x - other.x) + abs(start.y - other.y)
        else:
            return float('inf')
    
    def is_goal_achieved(self):
        if (len(self.unvisited) == 0 )or (self.supply_left.add_weights == 0):
            return True
        return False
    
    def move_to_visited(self, node:Tent):
        if node.required.add_weights == 0:
            self.visited.add(node)
            self.unvisited.remove(node)
    
    def heuristic(self, start, end:Tent):
        weight_required = end.required.add_weights()
        distance = self.compute_manhattan_distance(start, end)
        return weight_required * distance

# def perform_action(state, agent):
#     current_cell = state.map[agent.x][agent.y]
#     if isinstance(current_cell, Supply):
#         # Pick up supplies from the current cell
#         # Ensure not to exceed the Agent's capacity
#         # Update state and agent's ration
#     elif isinstance(current_cell, Tent):
#         # Drop off supplies at the current cell
#         # Update state and agent's ration
#     elif isinstance(current_cell, Path):
#         # Use hill climbing to determine next move
#         # Update agent's position
#     # Check if goal is reached
#     if state.is_goal_achieved():
#         print("All tents have been supplied!")
#         return True
#     return False

def perform_action(state, agent):
    # print(agent.x, agent.y)
    # print(type(agent.x))
    current_cell = state.map[agent.x][agent.y]
    if isinstance(current_cell, Supply):
        # Pick up supplies from the current cell
        # Ensure not to exceed the Agent's capacity
        milk_needed = max(0, agent.CAPACITY - agent.ration.milk)
        bread_needed = max(0, agent.CAPACITY - agent.ration.bread)
        dhal_needed = max(0, agent.CAPACITY - agent.ration.dhal)
        rice_needed = max(0, agent.CAPACITY - agent.ration.rice)
        flour_needed = max(0, agent.CAPACITY - agent.ration.flour)
        agent.pick_supplies(milk_needed, bread_needed, dhal_needed, rice_needed, flour_needed, current_cell.supply)

    elif isinstance(current_cell, Tent):
        # Drop off supplies at the current cell
        agent.drop_supplies(current_cell.required)
        # move the node to visited if its required is met
        state.move_to_visited(current_cell)

    elif isinstance(current_cell, Path):
        # Use hill climbing to determine next move
        next_move = agent.hill_climbing(state)
        # Update agent's position
        agent.move_agent(next_move)

    # Check if goal is reached
    if state.is_goal_achieved():
        print("All tents have been supplied!")
        return True
    return False


if __name__ == "__main__":
    # initialization of the map
    mp = np.array(
        [
            ["NA", "NA", "Tent,2,3", "Tent,2,1", "NA", "NA"],
            ["Supply,28,10,30,50,36", "Path", "Path", "Path", "Path", "Tent,3,2"],
            ["NA", "Path", "NA","NA", "Path", "NA",],
            ["NA", "Path", "NA","NA", "Path", "NA",],
            ["NA", "Path", "Path", "Path", "Path", "Tent,4,0"],
            ["Tent,3,2", "NA", "NA", "Tent,12,0", "Tent,2,3", "NA"],
        ]
    )

    # Initialization of the state and the agent
    state = State(1,0,mp)  # Assuming agent starts at the Supply cell
    agent = Agent(state.current)
    print("state current", state.current.x)
    print(agent.x)

    # Calculation of actual rations based on total supplies
    S = Ration(0,0,0,0,0)
    S_required = Ration(0,0,0,0,0)

    # Calculation of actual rations based on total supplies
    S = Ration(0,0,0,0,0)
    S_required = Ration(0,0,0,0,0)
    adults = 0
    children = 0

    for row in state.map:
        for cell in row:
            if isinstance(cell, Supply):
                S +=  cell.supply
            if isinstance(cell, Tent):
                S_required += cell.required
                adults += cell.count_adult
                children += cell.count_child

    ActualAdult = Person(0,0,round(S.dhal / adults, 2), round(S.rice / adults, 2), round(S.flour / adults, 2))
    ActualChild = Person(round(S.milk / children, 2), round(S.bread / children, 2), 0,0,0)

    print(Adult.ration, "\n")
    print(ActualAdult.ration, "\n")
    print(Child.ration, "\n")
    print(ActualChild.ration, "\n")

    # Start the execution loop
    # n=1
    # while not perform_action(state, agent):
    #     print(n)
    adults = 0
    children = 0

    for row in state.map:
        for cell in row:
            if isinstance(cell, Supply):
                S +=  cell.supply
            if isinstance(cell, Tent):
                S_required += cell.required
                adults += cell.count_adult
                children += cell.count_child

    ActualAdult = Person(0,0,round(S.dhal / adults, 2), round(S.rice / adults, 2), round(S.flour / adults, 2))
    ActualChild = Person(round(S.milk / children, 2), round(S.bread / children, 2), 0,0,0)

    print(Adult.ration, "\n")
    print(ActualAdult.ration, "\n")
    print(Child.ration, "\n")
    print(ActualChild.ration, "\n")

    # Start the execution loop
    loop_variable=1
    while not perform_action(state, agent) : # and loop_variable <500000
        print("LV", loop_variable)
        loop_variable= loop_variable+1
        # pass

# if __name__ == "__main__":
#     mp = np.array(
#         [
#             ["NA", "NA", "Tent,2,3", "Tent,2,1", "NA", "NA"],
#             ["Supply,28,10,30,50,36", "Path", "Path", "Path", "Path", "Tent,3,2"],
#             ["NA", "Path", "NA","NA", "Path", "NA",],
#             ["NA", "Path", "NA","NA", "Path", "NA",],
#             ["NA", "Path", "Path", "Path", "Path", "Tent,4,0"],
#             ["Tent,3,2", "NA", "NA", "Tent,12,0", "Tent,2,3", "NA"],
#         ]
#     )

#     st = State(0,0,mp)
#     S_required = Ration(0,0,0,0,0)
#     S = Ration(0,0,0,0,0)
#     adults = 0
#     children = 0
#     for row in st.map:
#         for cell in row:
#             if cell.cell_type == 3:
#                 S +=  cell.supply
#             if cell.cell_type == 1:
#                 S_required += cell.required
#                 adults += cell.count_adult
#                 children += cell.count_child
    
# ActualAdult = Person(0,0,round(S.dhal / adults, 2), round(S.rice / adults, 2), round(S.flour / adults, 2))
# ActualChild = Person(round(S.milk / children, 2), round(S.bread / children, 2), 0,0,0)

# print(Adult.ration, "\n")
# print(ActualAdult.ration, "\n")
# print(Child.ration, "\n")
# print(ActualChild.ration, "\n")



# while not perform_action(state, agent):
#     pass


