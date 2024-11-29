import file_management
from geopy.distance import distance
import math

    # Variables to track the shortest path and best path
SHORTEST_PATH_LENGTH = 100000.0
SHORTEST_PATH_TIME = 100000.0
BEST_COST = 100000.0
BEST_PATH = []
BEST_PATH_TRANSPORT = []

    # Variables to track paths checked
PATHS_CHECKED = 0
PATHS_CHECKED_LIMIT = 100000000

LOCATIONS = file_management.load_data() # Load the locations


class Vehicle:
    def __init__(self, speed, cost, transfer_time, identifier):
        self.speed = speed  # Speed in m/s
        self.cost = cost  # Cost per km
        self.transfer_time = transfer_time  # Transfer time in seconds
        self.identifier = identifier  # Transport identifier

        # Calculatting the travel time between locations
    def travel_time(self, distance):
        return (distance / self.speed) + self.transfer_time

        # Calculatting the cost between locations
    def travel_cost(self, distance):
        return (self.cost * distance) / 1000


    # Vehicle instances for different transport modes
bicycle = Vehicle(4.2,0,60,"C")
walking = Vehicle(1.4,0,0,"W")
bus = Vehicle(11.1,2,300,"B")
train = Vehicle(22.2,5,600,"T")

    # Stores the modes of transport
MODES = [bus, train, bicycle, walking]

    # Calculate the distances between all the different locations and store them
DISTANCE_TABLE = {
    (i, j): distance(
        (LOCATIONS[i][3], LOCATIONS[i][4]),
        (LOCATIONS[j][3], LOCATIONS[j][4])
    ).meters
    for i in range(len(LOCATIONS))
    for j in range(len(LOCATIONS))
}

    # Function to calculate distance between two locations
def distance_between_locations(place1, place2):
    return DISTANCE_TABLE[(place1, place2)]

    # Function for finding the shortest possible path between all the locations
def find_shortest_path(current_pos, visited_nodes, total_dist):
    global SHORTEST_PATH_LENGTH, BEST_PATH

        # If current path distance exceeds the known shortest path, don't continue checking this path
    if total_dist >= SHORTEST_PATH_LENGTH:
        return float('inf')

        # If all locations are visited, complete the loop back to starting location
    if len(visited_nodes) == len(LOCATIONS):
        total_dist += distance_between_locations(current_pos, 0)

            # Store the path if it's better than the previous best path
        if total_dist < SHORTEST_PATH_LENGTH:
            SHORTEST_PATH_LENGTH = total_dist
            BEST_PATH = visited_nodes + [0]
        return total_dist

        # Explore the next possible location
    for next_pos in range(1, len(LOCATIONS)):
        if next_pos not in visited_nodes:
            dist = distance_between_locations(current_pos, next_pos)
            new_visited_nodes = visited_nodes + [next_pos]
            find_shortest_path(next_pos, new_visited_nodes, total_dist + dist)

    return SHORTEST_PATH_LENGTH


    # Function for finding the path that takes the least time to visit all the locations
def find_least_time(current_pos, visited_nodes, total_time, transport_used):
    global SHORTEST_PATH_TIME, BEST_PATH, BEST_PATH_TRANSPORT

        # If current path time exceeds the known shortest time, don't continue checking this path
    if total_time >= SHORTEST_PATH_TIME:
        return float('inf')

        # If all locations are visited, complete the loop back to starting location
    if len(visited_nodes) == len(LOCATIONS):
        loop_back_distance = distance_between_locations(current_pos, 0)
        loop_back_time, loop_back_mode = min(((mode.travel_time(loop_back_distance), mode.identifier) for mode in MODES), key=lambda x: x[0])
        total_time += loop_back_time

            # Store the path if it's better than the previous best path
        if total_time < SHORTEST_PATH_TIME:
            SHORTEST_PATH_TIME = total_time
            BEST_PATH = visited_nodes + [0]
            BEST_PATH_TRANSPORT = transport_used + [loop_back_mode]
        return total_time

        # Explore the next possible location
    for next_pos in range(1, len(LOCATIONS)):
        if next_pos not in visited_nodes:
            dist = distance_between_locations(current_pos, next_pos)
                # Find the fastest time across all modes of transport
            travel_time, mode_used = min(((mode.travel_time(dist), mode.identifier) for mode in MODES), key=lambda x: x[0])
            new_total = total_time + travel_time
            find_least_time(next_pos, visited_nodes + [next_pos], new_total, transport_used + [mode_used])

    return SHORTEST_PATH_TIME


    # Function for finding the path that takes the least time to visit all the locations within a budget
def find_least_cost(current_pos, visited_nodes, total_time, total_cost, transport_used, maximum_cost):
    global SHORTEST_PATH_TIME, BEST_PATH, BEST_PATH_TRANSPORT, BEST_COST, PATHS_CHECKED, PATHS_CHECKED_LIMIT

        # Update the amount of paths checked
    PATHS_CHECKED += 1

        # Stops calculating if the amount of paths is more than the limit, can be removed but will increase execution time by alot
    if (PATHS_CHECKED > PATHS_CHECKED_LIMIT):
        return float('inf')

        # If current path time exceeds the known shortest time or exceedes the budget, don't continue checking this path
    if total_time >= SHORTEST_PATH_TIME or total_cost > maximum_cost:
        return float('inf')

        # If all locations are visited, complete the loop back to starting location
    if len(visited_nodes) == len(LOCATIONS):
        loop_back_distance = distance_between_locations(current_pos, 0)
        
        # Calculate time and cost for the return trip to the starting location
        best_return_option = min(
            ((mode.travel_time(loop_back_distance), mode.travel_cost(loop_back_distance), mode.identifier) 
             for mode in MODES),
            key=lambda x: (x[0], x[1])
        )
        
        loop_back_time, loop_back_cost, loop_back_mode = best_return_option
        total_time += loop_back_time
        total_cost += loop_back_cost

            # Store the path if it's better than the previous best path
        if total_time < SHORTEST_PATH_TIME and total_cost <= maximum_cost:
            SHORTEST_PATH_TIME = total_time
            BEST_COST = total_cost
            BEST_PATH = visited_nodes + [0]
            BEST_PATH_TRANSPORT = transport_used + [loop_back_mode]
        return total_time

        # Explore the next possible location
    for next_pos in range(1, len(LOCATIONS)):
        if next_pos not in visited_nodes:
            dist = distance_between_locations(current_pos, next_pos)
            
            for mode in MODES:
                travel_time = mode.travel_time(dist)
                travel_cost = mode.travel_cost(dist)
                new_total_time = total_time + travel_time
                new_total_cost = total_cost + travel_cost
                
                # Proceed only if the total cost stays within budget
                if total_cost + travel_cost < maximum_cost:
                    find_least_cost(
                        next_pos, 
                        visited_nodes + [next_pos],  
                        new_total_time, 
                        new_total_cost,
                        transport_used + [mode.identifier], 
                        maximum_cost
                    )

    return SHORTEST_PATH_TIME


    # Used to calculate total cost for a path
def calculate_cost():
    temp_cost=0
    temp_distance=0
    temp_vehicle="X"
    for i in range(len(BEST_PATH_TRANSPORT)):
        temp_distance = distance_between_locations(BEST_PATH[i], BEST_PATH[i+1])
        temp_vehicle = BEST_PATH_TRANSPORT[i]
        if (temp_vehicle == "B"):
            temp_cost +=  bus.travel_cost(temp_distance)
        if (temp_vehicle == "T"):
            temp_cost +=  train.travel_cost(temp_distance)
        if (temp_vehicle == "C"):
            temp_cost +=  bicycle.travel_cost(temp_distance)
        if (temp_vehicle == "W"):
            temp_cost +=  walking.travel_cost(temp_distance)
    return temp_cost


    # Used to calculate total time for a path
def calculate_time():
    temp_time=0
    temp_distance=0
    temp_vehicle="0"
    for i in range(len(BEST_PATH_TRANSPORT)):
        temp_distance = distance_between_locations(BEST_PATH[i], BEST_PATH[i+1])
        temp_vehicle = BEST_PATH_TRANSPORT[i]
        if (temp_vehicle == "B"):
            temp_time +=  bus.travel_time(temp_distance)
        if (temp_vehicle == "T"):
            temp_time +=  train.travel_time(temp_distance)
        if (temp_vehicle == "C"):
            temp_time +=  bicycle.travel_time(temp_distance)
        if (temp_vehicle == "W"):
            temp_time +=  walking.travel_time(temp_distance)
    return temp_time


    # Used to calculate total distance for a path
def calculate_dist():
    temp_distance=0
    for i in range(len(BEST_PATH)-1):
        temp_distance += distance_between_locations(BEST_PATH[i], BEST_PATH[i+1])
    return temp_distance

def main(current_pos, visited_nodes, total, optimization, maximum_cost):
    global SHORTEST_PATH_LENGTH, SHORTEST_PATH_TIME, BEST_PATH, BEST_PATH_TRANSPORT, BEST_COST
        
    if(optimization == "distance"): # Find shortest distance
        find_shortest_path(current_pos, visited_nodes, total)
        BEST_PATH_TRANSPORT=["X","X","X","X","X","X","X","X","X","X","X"] # Transport vehicle doesn't matter, so default values are stored
    elif(optimization == "time"):   # Find least time
        transport = []
        find_least_time(current_pos, visited_nodes, total, transport)
        SHORTEST_PATH_LENGTH=calculate_dist()
        BEST_COST=calculate_cost()
    elif(optimization == "cost"):   # Find least time within a budget
        transport = []
        find_least_cost(current_pos, visited_nodes, total, 0, transport, maximum_cost)
        SHORTEST_PATH_LENGTH=calculate_dist()
        SHORTEST_PATH_TIME=calculate_time()

        # Dictionary containg the results
    result = {
        "shortest_path_found": BEST_PATH,            
        "total_distance": round(SHORTEST_PATH_LENGTH, 2), 
        "total_time": round(SHORTEST_PATH_TIME, 0),       
        "transport_used": BEST_PATH_TRANSPORT,
        "total_cost": math.ceil(BEST_COST)
    }

    return result
