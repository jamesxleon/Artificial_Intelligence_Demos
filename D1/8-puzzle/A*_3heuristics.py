from queue import PriorityQueue
from graphviz import Digraph
import networkx as nx
import math
import random

#For a deterministic initial state, useful for testing
INITIAL_STATE = tuple(map(tuple, [[8, 1, 3], [4, 0, 2], [7, 6, 5]])) 

# Define the goal state and the initial state
GOAL_STATE = tuple(map(tuple, [[1, 2, 3], [4, 5, 6], [7, 0, 8]]))

# Map the values to the positions in the goal state
GOAL_POS = {num:(i,j) for i, row in enumerate(GOAL_STATE) for j, num in enumerate(row)}

goal_row_order = [sorted(row) for row in GOAL_STATE]
goal_column_order = [sorted(column) for column in zip(*GOAL_STATE)]

#Useful to randomize initial states and play around
#def randomize_initial_state():
    # Flatten the state into a list
#    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # Shuffle the list
#    random.shuffle(state)

    # Reshape the list back into a 3x3 grid
#    state = [state[i:i+3] for i in range(0, len(state), 3)]

#    return tuple(map(tuple, state))

# Use this function to get a randomized initial state
#INITIAL_STATE = randomize_initial_state()

def Manhattan_heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = GOAL_POS[state[i][j]]
                distance += abs(x - i) + abs(y - j)
    return distance

def Euclidean_heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = GOAL_POS[state[i][j]]
                distance += math.sqrt((x - i)**2 + (y - j)**2)
    return distance

def Max_heuristic(state):
    manhattan_distance = 0
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = GOAL_POS[state[i][j]]
                manhattan_distance += abs(x - i) + abs(y - j)
                if (i, j) != (x, y):
                    misplaced_tiles += 1
    return max(manhattan_distance, misplaced_tiles)

def Linear_Conflict_Heuristic(state):
    distance = 0
    row_conflicts = [0]*3
    column_conflicts = [0]*3
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # Calculate the Manhattan distance
                x, y = GOAL_POS[state[i][j]]
                distance += abs(x - i) + abs(y - j)

                # Check for linear conflicts
                if state[i][j] in goal_row_order[i]:
                    for k in range(j+1, 3):
                        if state[i][k] in goal_row_order[i] and state[i][j] > state[i][k]:
                            row_conflicts[i] += 1
                if state[j][i] in goal_column_order[i]:
                    for k in range(j+1, 3):
                        if state[k][i] in goal_column_order[i] and state[j][i] > state[k][i]:
                            column_conflicts[i] += 1
    linear_conflicts = sum(row_conflicts) + sum(column_conflicts)
    return distance + 2*linear_conflicts

def default():
    print("Invalid choice. Please try again.")

switch = {
    "1": Manhattan_heuristic,
    "2": Euclidean_heuristic,
    "3": Max_heuristic,
    "4": Linear_Conflict_Heuristic,
}

# Define the search function
def search(state, g, heuristic):
    # If the state is the goal state, return the cost
    if state == GOAL_STATE:
        return g

    # Generate the state space
    for action in ACTIONS:
        new_state = apply_action(state, action)
        if new_state is not None and new_state not in G:
            G.add_edge(state, new_state)
            cost = g + 1 + heuristic(new_state)
            frontier.put((cost, new_state, g + 1))

    # Continue the search
    while not frontier.empty():
        _, state, g = frontier.get()
        cost = search(state, g, heuristic)
        if cost is not None:
            return cost

# Define the action function
def apply_action(state, action):
    # Copy the state
    new_state = [list(row) for row in state]

    # Find the blank space
    i, j = next((i, j) for i, row in enumerate(state) for j, cell in enumerate(row) if cell == 0)

    # Apply the action
    if action == 'up' and i > 0:
        new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
    elif action == 'down' and i < 2:
        new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
    elif action == 'left' and j > 0:
        new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
    elif action == 'right' and j < 2:
        new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]
    else:
        return None

    return tuple(map(tuple, new_state))

# Define the possible actions
ACTIONS = ['up', 'down', 'left', 'right']

# Perform the search

while True:

    # Create a priority queue for the frontier
    frontier = PriorityQueue()

    # Create a graph to store the state space
    G = nx.Graph()

    print("Please select a heuristic:")
    print("1. Manhattan")
    print("2. Euclidean")
    print("3. Max")
    print("4. Linear Conflict")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "5":
        print("Exiting...")
        break
    else:

        heuristic_function = switch.get(choice, default)
        cost = search(INITIAL_STATE, 0, heuristic_function)

        #Print the cost
        print(f'Cost: {cost}')

        # Create a Digraph object
        dot = Digraph()

        # Add nodes and edges to the graph
        for state in G.nodes:
            if state == INITIAL_STATE:
                dot.node(str(state), color='green')  # colorize the root node
            elif state in nx.shortest_path(G, source=INITIAL_STATE, target=GOAL_STATE):
                dot.node(str(state), color='blue')  # colorize the resulting path nodes
            else:
                dot.node(str(state), color='red')  # colorize the discarded paths nodes

        for state1, state2 in G.edges:
            dot.edge(str(state1), str(state2))

        # Render the graph
        dot.render('state_space.gv', view=True)

        # Print the path from the initial state to the goal state to the terminal
        print("Path from the initial state to the goal state:")
        path = nx.shortest_path(G, source=INITIAL_STATE, target=GOAL_STATE)
        for state in path:
            for row in state:
                print(row)
            print()