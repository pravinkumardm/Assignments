import numpy as np
import copy
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
        # self.list_of_items = 
    
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

initial_adult_ration = Ration(0,0,1,3,3)
initial_child_ration = Ration(3,1,0,0,0)
class MapCell:
    def __init__(self, x, y, cell_type, accessible):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.accessible = accessible

    def compute_manhattan_distance(self, other):
        if self.accessible and other.accessible:
            return abs(self.x - other.x) + abs(self.y - other.y)
        else:
            return float('inf')

class Tent(MapCell):
    def __init__(self, x:int, y:int, adult:int, child:int):
        super().__init__(x, y, cell_type = 1, accessible=True)
        self.count_adult = adult
        self.count_child = child
        self.required = self.compute_requirement(initial_adult_ration, initial_child_ration)
    
    def compute_requirement(self, adult_ration:Ration, child_ration:Ration):
        requirement = (adult_ration * self.count_adult) + (child_ration * self.count_child)
        return requirement

    def __str__(self):
        return f"Adults : {self.count_adult}\nChildren : {self.count_child}\nRequirement: \n{self.required}"

class Supply(MapCell):
    def __init__(self, x, y, milk, bread, dhal, rice, flour):
        super().__init__(x, y, cell_type = 3, accessible = True)
        self.supply = Ration(milk, bread, dhal, rice, flour)
    
    def __str__(self):
        return "Supply"

class Path(MapCell):
    def __init__(self, x, y):
        super().__init__(x, y, cell_type=2,accessible = True)
    
    def __str__(self):
        return "-Path-"

class NA(MapCell):
    def __init__(self, x, y):
        super().__init__(x, y, cell_type=0, accessible = False)
    
    def __str__(self):
        return "--NA--"


class State:
    def __init__(self, start_x:int, start_y:int, map_2d:np.array, adult_requirement:Ration, child_requirement:Ration):
        self.adult_requirement = adult_requirement
        self.child_requirement = child_requirement
        self.map = self.read_map(map_2d)
        self.visited= set()
        self.unvisited_tents = set()
        self.unvisited_supplies = set()
        self.update_unvisited()
        self.supply_left = self.current_supply()
        self.demand_supply()


        self.source = self.map[start_x][start_y]
        self.agent = Agent(self.source)
        self.adult_requirement = Ration(0,0,0,0,0)
        self.child_requirement = Ration(0,0,0,0,0)
        self.path_stack = []
        # self.distance_travelled = 0
        # self.commutes = 0
        # self.complete = False
        self.destination = None

    def read_map(self, textmap):
        state_map = []
        for x, row in enumerate(textmap):
            state_map_row = []
            for y , cell in enumerate(row):
                data = cell.lower().split(',')
                cell_type = data[0]
                args = [float(x) for x in data[1:]]
                
                if cell_type == "supply":
                    state_map_row.append(Supply(x, y, milk = args[0], bread = args[1], dhal=args[2], rice=args[3], flour=args[4]))
                elif cell_type == "tent":
                    state_map_row.append(Tent(x, y, adult=args[0], child=args[1]))
                elif cell_type == "path":
                    state_map_row.append(Path(x, y))
                else:
                    state_map_row.append(NA(x, y))
            state_map.append(state_map_row)
        return state_map

    def update_unvisited(self):
        for row in self.map:
            for cell in row:
                if isinstance(cell, Tent):
                    if cell.required.add_weights == 0:
                        self.visited_tents.add(cell)
                    else:
                        self.unvisited_tents.add(cell)
                elif isinstance(cell, Supply):
                    if cell.supply.add_weights == 0:
                        self.visited_supplies.add(cell)
                    else:
                        self.unvisited_supplies.add(cell)

    def current_supply(self):
        R = Ration(0,0,0,0,0)
        for S in self.unvisited_supplies:
            R += S.supply
        return R

    def is_goal_achieved(self):
        if (len(self.unvisited_tents) == 0) or (self.supply_left.add_weights == 0):
            return True
        return False

    def move_to_visited(self):
        update = []
        for i in self.unvisited_tents:
            if i.required.add_weights() == 0:
                update.append(i)
        for i in self.unvisited_supplies:
            if i.supply.add_weights() == 0:
                update.append(i)
        for i in update:
            if isinstance(i, Supply):
                self.unvisited_supplies.remove(i)
            elif isinstance(i, Tent):
                self.unvisited_tents.remove(i)
                self.visited.add(i)
    
    def demand_supply(self):
        S = Ration(0,0,0,0,0)
        adults = children = 0
        for row in self.map:
            for cell in row:
                if isinstance(cell, Supply):
                    S += cell.supply
                if isinstance(cell, Tent):
                    adults += cell.count_adult
                    children += cell.count_child
        dhal = min(round(S.dhal / adults, 2), self.adult_requirement.dhal)
        rice = min(round(S.rice / adults, 2), self.adult_requirement.rice)
        flour = min(round(S.flour / adults, 2), self.adult_requirement.flour)
        milk = min(round(S.milk / children, 2), self.child_requirement.milk)
        bread = min(round(S.bread / children, 2), self.child_requirement.bread)
        self.adult_requirement = Ration(0,0,dhal, rice, flour)
        self.child_requirement = Ration(milk, bread, 0, 0, 0)
    
    def find_destination(self, get_dest = "supply", source = None):
        if source == None:
            source = self.source
        min_distance = float('inf')
        best_dest = None
        if get_dest == "supply":
            for i in self.unvisited_supplies:
                dist = self.calculate_manhattan_distance(source, i)
                if dist < min_distance:
                    best_dest = i
                    min_distance = dist
        else:
            for i in self.unvisited_tents:
                dist = self.calculate_manhattan_distance(source, i)
                if dist < min_distance:
                    best_dest = i
                    min_distance = dist
        return best_dest
        # if check_from == None:
        #     if not self.destination:
        #         if self.agent.current_weight == 0:
        #             min_distance = float('inf')
        #             for i in self.unvisited_supplies:
        #                 dist = self.calculate_manhattan_distance(self.source, i)
        #                 if dist <= min_distance:
        #                     self.destination = i
        #         else:
        #             min_distance = float('inf')
        #             for i in self.unvisited_tents:
        #                 dist = self.calculate_manhattan_distance(self.source, i)
        #                 if dist <= min_distance:
        #                     self.destination = i
        #     else:
        #         pass
        # else:
        #     min_distance = float('inf')
        #     if isinstance(check_from, Tent):
        #         dest = None
        #         for i in self.unvisited_supplies:
        #             dist = self.calculate_manhattan_distance(check_from, i)
        #             if dist <= min_distance:
        #                 dest = i
        #     elif isinstance(check_from, Supply):
        #         dest = None
        #         for i in self.unvisited_tents:
        #             dist = self.calculate_manhattan_distance(check_from, i)
        #             if dist <= min_distance:
        #                 dest = i
        #     return dest

    def calculate_manhattan_distance(self, source, destination):
        return abs(source.x - destination.x) + abs(source.y - destination.y)
    
    def get_valid_neighbours(self, cell):
        valid_neighbours = []
        if cell.x - 1 >= 0 and self.map[cell.x-1][cell.y].accessible:
            valid_neighbours.append(self.map[cell.x-1][cell.y])
        if cell.x + 1 <= 5 and self.map[cell.x+1][cell.y].accessible:
            valid_neighbours.append(self.map[cell.x+1][cell.y])
        if cell.y - 1 >=0 and self.map[cell.x][cell.y-1].accessible:
            valid_neighbours.append(self.map[cell.x][cell.y-1])
        if cell.y + 1 <=5 and self.map[cell.x][cell.y+1].accessible:
            valid_neighbours.append(self.map[cell.x][cell.y+1])
        return valid_neighbours
    
    def update_state_location(self):
        self.source = self.map[self.agent.x][self.agent.y]
        self.destination = None

    def update_supplies(self):
        if isinstance(self.map[self.agent.x][self.agent.y], Supply):
            nearest_tent = self.find_destination(get_dest="tent", source=self.map[self.agent.x][self.agent.y])
            for item in ["milk", "bread", "dhal", "rice", "flour"]:
                supply_item = getattr(self.supply_left, item)
                agent_carriable = self.agent.CAPACITY - self.agent.carrying.add_weights()
                require_item = getattr(nearest_tent.required, item)
                taken_qty = min(supply_item, require_item, agent_carriable)
                setattr(self.supply_left, item, supply_item-taken_qty)
                setattr(self.agent.carrying, item, getattr(self.agent.carrying, item)+taken_qty)
            # while self.agent.carrying.add_weights()<self.agent.CAPACITY:
            #     for item in ["milk", "bread", "dhal", "rice", "flour"]:
            #         supply_item = getattr(self.supply_left, item)
            #         agent_carriable = self.agent.CAPACITY - self.agent.carrying.add_weights()
            #         taken_qty = min(supply_item, agent_carriable)
            #         setattr(self.supply_left, item, getattr(self.supply_left, item) - taken_qty)
            #         setattr(self.agent.carrying, item, getattr(self.agent.carrying, item) + taken_qty)

        elif isinstance(self.map[self.agent.x][self.agent.y], Tent):
            for item in ["milk", "bread", "dhal", "rice", "flour"]:
                required_item = getattr(self.map[self.agent.x][self.agent.y].required, item)
                agent_carrying = getattr(self.agent.carrying, item)
                drop_qty = min(required_item, agent_carrying)
                setattr(self.agent.carrying, item, getattr(self.agent.carrying, item) - drop_qty)
                setattr(self.map[self.agent.x][self.agent.y].required, item, getattr(self.map[self.agent.x][self.agent.y].required, item) - drop_qty)



class Agent:
    def __init__(self, cell):
        self.x, self.y = cell.x, cell.y
        self.CAPACITY = 15
        self.carrying = Ration(0,0,0,0,0)
        self.distance_traveled = 0
        self.commutes = 0
        self.current_weight = self.carrying.add_weights()

    def pick_supplies(self, state:State, pick_required:Ration):
        required = copy.deepcopy(pick_required)
        # print('within pick_supplies')
        for item in ['milk', 'bread', 'dhal', 'rice', 'flour']:
            if self.carrying.add_weights() == self.CAPACITY:
                break
            supply_amount = getattr(state.supply_left, item)
            # print("supply_amount :", supply_amount)
            required_amount = getattr(required, item)
            # print("required_amount :", required_amount)
            load_amount = min(supply_amount, required_amount, self.CAPACITY-self.carrying.add_weights())
            # print("load_amount :", load_amount)
            setattr(self.carrying,item,load_amount)
            state.supply_left = state.supply_left - self.carrying
            required = required - self.carrying
        self.current_weight = self.carrying.add_weights()
    
    def drop_supplies(self, required:Ration):
        for item in ['milk', 'bread', 'dhal', 'rice', 'flour']:
            carried_item = getattr(self.carrying, item)
            required_item = getattr(required, item)
            drop_item = min(carried_item, required_item)
            left_with_agent = carried_item - drop_item
            setattr(self.carrying, item, left_with_agent)
            setattr(required, item, required_item - drop_item)
        self.current_weight = self.carrying.add_weights()

        
    
    def get_valid_moves(self, state_map):
        valid_moves = []
        if (self.x-1>=0) and state_map[self.x-1][self.y].accessible:
            valid_moves.append("LEFT")
        if self.x+1<=5 and state_map[self.x+1][self.y].accessible:
            valid_moves.append("RIGHT")
        if self.y-1>=0 and state_map[self.x][self.y-1].accessible:
            valid_moves.append("DOWN")
        if self.y+1<=5 and state_map[self.x][self.y+1].accessible:
            valid_moves.append("UP")
        return valid_moves

    def pick_or_drop(self, p_d, state:State):
        if p_d == "drop":
            self.drop_supplies(state.source.required)
        elif p_d == "pick":
            # print("within Pick")
            next_dest = state.find_destination("tent")
            # print(next_dest)
            self.pick_supplies(state, next_dest.required)

def hill_climbing_2(state:State):
    if state.source == state.destination:
        return
    current = state.source
    destination = state.destination
    while current != destination:
        neighbours = state.get_valid_neighbours(current)
        new_pos = current
        for neighbour in neighbours:
            if state.calculate_manhattan_distance(neighbour, destination) <= state.calculate_manhattan_distance(new_pos, destination):
                new_pos = neighbour
        current = new_pos
        state.agent.distance_traveled += 1
    state.agent.x = current.x
    state.agent.y = current.y
    state.agent.commutes += 1




if __name__ == "__main__":
    # Initiate State
    # Update States
    # Stop State
    iteration = 0
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
    state = State(1,0,mp,Ration(0,0,1,3,3), Ration(3,1,0,0,0))
    while not state.is_goal_achieved():
        if iteration >= 10:
            break
        print(f"---------------Iteration {iteration} -------------------------")
        print(f"\nSupply:{state.supply_left}\n")
        print(f'''\nCurrent Location:
            {state.source.__class__.__name__} : {state.source.x}, {state.source.y}\n
            Carrying
            {state.agent.carrying}
            ''')
        if state.agent.carrying.add_weights() > 0:
            next_destination = "tent"
            action = "drop"
            closest = state.find_destination(get_dest="tent")
        else:

            next_destination = "supply"
            action = "pick"
            closest = state.find_destination(get_dest="supply")
        state.destination = closest
        print(f'\n Destination : {state.destination.__class__.__name__} : {state.destination.x}, {state.destination.y}')
        hill_climbing_2(state)
        state.update_state_location()
        state.update_supplies()
        state.move_to_visited()
        iteration += 1
