import sys
import os

    # Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import calculate_distance
import create_graph
import logger
import file_management

def main():
    initial_position = 0 # Starting position, which is Tarjan's home
    visited_nodes = [initial_position]
    maximum_cost = 100000

        # Runs until user inputs a valid choice
    while True:
        print("This is Tarjan's planner. It will calculate the most efficient path based on your preference.")
        print('To find the shortest path, enter "distance"')
        print('To find the fastest path, enter "time"')
        print('To find the most cost-efficient path, enter "cost"')
        print('To input or remove data, enter "data"')
        print('To exit, enter "exit"')
        optimazation = input("Enter the option representing your choice: ").strip().lower()
        print('\n\n')

        if optimazation in ["distance", "time", "cost", "data", "exit"]:
            break  # Exit the loop if a valid choice is made
        else:
            print("Invalid choice. Please try again.\n")

        # Find the budget for the user
    while (optimazation == "cost"):
        maximum_cost = input("What is your budget?")
        if (maximum_cost > 0 and maximum_cost < 100000):
            break  # Exit the loop if a valid choice is made
        else:
            print("Invalid choice. Please try again.\n")

       # Find the optimal path based on the user's choice     
    if (optimazation == "data"):
        file_management.changeData()
    elif (optimazation in ["distance", "time", "cost"]):
            # Wrap the calulation in logger to time the calulation process
        timed_calculate_distance = logger.timethis(calculate_distance.main)
        result = timed_calculate_distance(initial_position, visited_nodes, 0, optimazation, maximum_cost)

            # Change the distance to kilometers and meters
        kilometers = int(result["total_distance"]  // 1000)
        meters = int(result["total_distance"]  % 1000)

            # Print the best path and its total distance
        print("Shortest path:", result["shortest_path_found"])
        print("Total distance:", f"{kilometers} km and {meters} meters")

            # Change the time to hours, minutes and seconds
        if(optimazation == "time" or optimazation == "cost"):
            hours = int(result["total_time"] // 3600)
            remaining_seconds = result["total_time"] % 3600
            minutes = int(remaining_seconds // 60)
            seconds = int(remaining_seconds % 60)

                # Print the total time for the path
            print(f"Total time:, {hours} hours, {minutes} minutes, and {seconds} seconds")
            print("Total cost:", result["total_cost"])

            # Create and show the graph
        create_graph.main(result["shortest_path_found"], result["transport_used"])
    
if __name__ == "__main__":
    main()
