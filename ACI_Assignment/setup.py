import numpy as np

class Ration:
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
    def __init__(self, milk, bread, dhal, rice, flour):
        # self.ration = Ration(3,1,0,0,0)
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
        if pick_needed.add_weights <= 15:
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

    def move_agent(self, direction:str):
        if direction.lower() in self.get_valid_moves():
            if direction.lower() == "left":
                self.x = self.x - 1
                self.distance_traveled += 1
            if direction.lower() == "right":
                self.x = self.x + 1
                self.distance_traveled += 1
            if direction.lower() == "up":
                self.x = self.y + 1
                self.distance_traveled += 1
            if direction.lower() == "down":
                self.x = self.y - 1
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
        for i in maparray:
            rowitem = []
            for j in i:
                data = j.split(",")
                cell_type = data[0]
                args = [float(x) for x in data[1:]]
                if cell_type.lower() == "supply":
                    rowitem.append(Supply(i,j,*args))
                elif cell_type.lower() == "tent":
                    rowitem.append(Tent(i, j, *args))
                elif cell_type.lower() == "path":
                    rowitem.append(Path(i,j))
                else:
                    rowitem.append(NA(i,j))
            citymap.append(rowitem)
        return citymap
    
    def compute_manhattan_distance(self, other):
        if self.accessible and other.accessible:
            return abs(self.x - other.x) + abs(self.y - other.y)
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

if __name__ == "__main__":
    mp = np.array(
        [
            ["NA", "NA", "Tent,2,3", "Tent,2,1", "NA", "NA"],
            ["Supply,10,20,30,40,50", "Path", "Path", "Path", "Path", "Tent,3,2"],
            ["NA", "Path", "NA","NA", "Path", "NA",],
            ["NA", "Path", "NA","NA", "Path", "NA",],
            ["NA", "Path", "Path", "Path", "Path", "Tent,4,0"],
            ["Tent,3,2", "NA", "NA", "Tent,12,0", "Tent,2,3", "NA"],
        ]
    )
