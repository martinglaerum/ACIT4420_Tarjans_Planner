import file_management
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

LOCATIONS = file_management.load_data() # Load the locations

def main(path=[], transport=[]):
        # Define the edges between each location
    edges = [(path[i-1], path[i]) for i in range(1, len(path))]
    
        # Create a graph and add edges
    G = nx.Graph()
    G.add_edges_from(edges)

        # Define positions based on latitude and longitude
    pos = {i: (LOCATIONS[i][4], LOCATIONS[i][3]) for i in range(len(LOCATIONS))}

        # Define the color mapping for transport modes
    transport_color_map = {
        "B": "blue",    # Bus
        "T": "green",   # Train
        "C": "yellow",  # Bicycle
        "W": "red",     # Walk
    }

        # List to hold unique labels for edges
    edge_labels = []

        # Assign a color to each edge based on the transport mode
    edge_colors = []
    for i in range(len(transport)):
        transport_type = transport[i]
        edge_colors.append(transport_color_map.get(transport_type, "black"))
        
            # Add the corresponding transport type label to edge_labels
        edge_labels.append(transport_type)

        # Draw the graph with locations and edges at geographic positions
    nx.draw_networkx_nodes(G, pos, nodelist=[0], node_size=700, node_color='green', node_shape='s', label="Tarjan's Home")
    nx.draw_networkx_nodes(G, pos, nodelist=list(range(1, len(LOCATIONS))), node_size=700, node_color='lightblue', node_shape='s', label="Residental Streets")
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=3)  # No generic label here, we'll use legends

        # Draw edge labels
    edge_labels_dict = {}
    for i, edge in enumerate(edges):
        edge_labels_dict[edge] = transport_color_map.get(transport[i], "black")
    
        # Create custom handles for the legend
    handles = []
    labels = ["Tarjan's Home", "Residental Streets"]  # Original labels for the locations

        # Create handles and labels for the location types
    handles.append(Patch(color='green', label="Tarjan's Home"))
    
        # Correct this part to use circles for "Residential Streets"
    handles.append(Patch(color='lightblue', label="Residential Streets"))

        # If the path is based on shortest distance, transport type is ignored
    if(transport[0] == "X"):
        handles.append(Line2D("X", "X", color="black", lw=4))
        labels.append(f"Travel Path")
    else: # Add labels for each transport type
        for t, color in transport_color_map.items():
            handles.append(Line2D([0], [0], color=color, lw=4))
            if (t == "B"):
                labels.append(f"Bus")
            elif (t == "T"):
                labels.append(f"Train")
            elif (t == "C"):
                labels.append(f"Bicycle")
            else:
                labels.append(f"Walking")
                
        # Draw the edge labels on the graph
    nx.draw_networkx_labels(G, pos, labels={i: LOCATIONS[i][0] for i in range(len(LOCATIONS))}, font_size=11)

     # Add custom legend with both location labels and transport modes
    plt.legend(handles=handles, labels=labels, loc="upper right", fontsize=11, markerscale=0.6, handleheight=2, handletextpad=1, borderpad=1.5, title="Transportation Modes and Locations")

        # Show the plot
    plt.title("Tarjan's Transportation Network in Seoul with Starting Location")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()
