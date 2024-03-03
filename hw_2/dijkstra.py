# First, let's define a function to find the node with the smallest distance
# that has not been visited yet

def min_distance(distances, visited):
    # Initialize minimum distance for next node
    min_val = float('inf')
    min_index = -1

    # Loop through all nodes to find minimum distance
    for i in range(len(distances)):
        if distances[i] < min_val and i not in visited:
            min_val = distances[i]
            min_index = i

    return min_index

# Now, let's implement Dijkstra's algorithm

def dijkstra_algorithm(graph: list, start_node: int) -> list:

    # Get total number of nodes in the graph
    num_nodes = len(graph)

    # Initialize distance and visited arrays
    distances = [float('inf')] * num_nodes
    visited = []

    # Set distance at starting node to 0 and add to visited list 
    distances[start_node] = 0

    # Loop through all nodes to find shortest path to each node
    for i in range(num_nodes):

        # Find minimum distance node that has not been visited yet
        current_node = min_distance(distances, visited)

        # Add current_node to list of visited nodes
        visited.append(current_node)

        # Loop through all neighboring nodes of current_node 
        for j in range(num_nodes):

            # Check if there is an edge from current_node to neighbor
            if graph[current_node][j] != 0:

                # Calculate the distance from start_node to neighbor, 
                # passing through current_node
                new_distance = distances[current_node] + graph[current_node][j]

                # Update the distance if it is less than previous recorded value 
                if new_distance < distances[j]:
                    distances[j] = new_distance

    # Return the list of the shortest distances to all nodes
    return distances