# ACIT4420_Tarjan's_Planner

This project is part of an assignement in the course ACIT4420. **ACIT4420_Tarjan's_Planner** is a tool that will caluclate the shortest distance or time for Tarjans to travel between all of Tarjan's relatives. It will then display the path as a graph, including the transport which should be used. The tool also allows for specifying a budget, and will then show the fastest path within the budget.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)
## Features
- Calculatue shortest distance between all a set of places
- Calculatue least time between all a set of places
- Calculatue least time iwthin a buget between all a set of places
- Show the optimal path as a graph
- Edit the places to visit
## Installation
To get started, follow these steps:
1. **Clone the Repository** (or download the package):
   ```bash
   git clone https://github.com/martinglaerum/ACIT4420_Tarjans_Planner.git
   cd ACIT4420_Tarjans_Planner
   ```
2. **Create a Virtual Environment** (recommended):
   ```bash
   python3 -m venv gameenv
   source gameenv/bin/activate  # On Windows, use `gameenv\Scripts\activate`
   ```
3. **Install the Package**:
   ```bash
   pip install -e .
   ```
## Usage
Once installed, you can use the tool by running the following command in your terminal:
```bash
tarjanplanner
```
This will launch a menu where you can choose one of the following
1. **Find shortest path**
2. **Find fastest path**
3. **Find fastest path within a budget**
4. **Change location data**
5. **Exit**

Choosing **Find shortest path** will caluclate and show the shortest path to visit all locations.
Choosing **Find fastest path** will caluclate and show the fastest path to visit all locations.
Choosing **Find fastest path** will caluclate and show the fastest path to visit all locations wthin a specified budget.
Choosing **Change location data** will allow you to change the locations to visit.
Choosing **Exit** stops the program.


## Project Structure
Here is a brief overview of the project's structure:
```
ACIT4420_Message_Sender/
│
├── tarjanplanner/
│   ├── __init__.py
│   ├── main.py                # Entry point for the program
│   ├── calculate_distance.py
│   ├── create_graph.py
│   ├── file_management.py
│   ├── logger.py
│   ├── time_log.txt
│   ├── locations.txt
│
├── setup.py                   # Installation script
└── README.md                  # Project documentation (this file)
```
### Key Files:
- **`main.py`**: Contains the main function that launches the program.
- **`setup.py`**: Script for installing the package.
- **`calculate_distance.py`**: Calculates the optimal path
- **`create_graph.py`**: Creates and shows the graph of the optimal path
- **`file_management.py`**: Remove or add locations
- **`logger.py`**: Logs the time the program uses to run
- **`locations.txt`**: Contains all the locations
