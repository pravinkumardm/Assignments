# Define a function to calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

 

# Define a function to calculate the Manhattan distance between two points
def calculate_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

 

# Define a function to generate successors (neighbors) of a given state
def generate_successors(state):
    x, y = state
    successors = []

    # Generate all possible moves (up, down, left, right)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        successors.append((new_x, new_y))

    return successors

 

# Iterative Deepening A* algorithm
def iterative_deepening_astar(source, destination, calculate_heuristic, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        stack = [(source, 0, calculate_heuristic(source))]

        while stack:
            current_state, path_cost, heuristic = stack.pop()

            if current_state == destination:
                return current_state

            if path_cost + heuristic <= depth:
                visited.add(current_state)
                successors = generate_successors(current_state)

                for successor in successors:
                    if successor not in visited:
                        new_path_cost = path_cost + 1  # Assuming all moves have a cost of 1
                        new_heuristic = calculate_heuristic(successor)
                        stack.append((successor, new_path_cost, new_heuristic))

    return None

 

# Apply the Iterative Deepening A* algorithm using Euclidean distance
final_position_euclidean = iterative_deepening_astar(source, destination, calculate_distance, 20)

 

print("Final position using Euclidean distance:", final_position_euclidean)
print("Distance to destination:", calculate_distance(final_position_euclidean, destination))

 

# Apply the Iterative Deepening A* algorithm using Manhattan distance
final_position_manhattan = iterative_deepening_astar(source, destination, calculate_manhattan_distance, 20)

 

print("Final position using Manhattan distance:", final_position_manhattan)
print("Manhattan distance to destination:", calculate_manhattan_distance(final_position_manhattan, destination))

this is what i got for ida from chat gpt by Mangala, Gowtham Gangadhar Export License Required - US Collins
Mangala, Gowtham Gangadhar Export License Required - US Collins
12:22 PM

this is what i got for ida from chat gpt

change the heuristic fromm just a distance ... by Mangala, Gowtham Gangadhar Export License Required - US Collins
Mangala, Gowtham Gangadhar Export License Required - US Collins
12:23 PM

change the heuristic fromm just a distance to the one which we did earlier

def manhattan_distance(point1, point2):  ... by Mangala, Gowtham Gangadhar Export License Required - US Collins
Mangala, Gowtham Gangadhar Export License Required - US Collins
Yesterday 12:24 PM

def manhattan_distance(point1, point2):
    # Calculate the Manhattan distance between two points on a grid
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

 

def heuristic(city_map, current_position, tents_to_supply):
    # Calculate the minimum weighted Manhattan distance from the current position to any tent to be supplied
    min_weighted_distance = float('inf')

 

    for tent in tents_to_supply:
        required_adults, required_children = city_map[tent[0]][tent[1]]
        total_goods_required = required_adults + required_children

 

        distance = manhattan_distance(current_position, tent)
        weighted_distance = distance * total_goods_required

 

        min_weighted_distance = min(min_weighted_distance, weighted_distance)

 

    return min_weighted_distance
