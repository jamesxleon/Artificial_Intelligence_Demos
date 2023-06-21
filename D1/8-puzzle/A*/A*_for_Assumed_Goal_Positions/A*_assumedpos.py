from queue import PriorityQueue
from graphviz import Digraph
import networkx as nx
import random

#For a deterministic initial state, useful for testing
INITIAL_STATE = tuple(map(tuple, [[8, 1, 3], [4, 0, 2], [7, 6, 5]])) 

# Define the goal state and the initial state
GOAL_STATE = tuple(map(tuple, [[1, 2, 3], [4, 5, 6], [7, 0, 8]]))

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

# Create a priority queue for the frontier
frontier = PriorityQueue()

# Create a graph to store the state space
G = nx.Graph()

# Define the heuristic function (Manhattan distance)
# This heuristic works under the assumption that the position of the tiles 
# in the goal state is known (ordered from 1 to 8 and 0 at the end)
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

# Define the search function
def search(state, g):
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
        cost = search(state, g)
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
cost = search(INITIAL_STATE, 0)

# Print the cost
print(f'Cost: {cost}')

# Create a Digraph object
dot = Digraph()

# Add nodes and edges tothe graph
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
