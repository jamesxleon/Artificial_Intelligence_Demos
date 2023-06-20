from collections import deque
from graphviz import Digraph
import networkx as nx
import random

# Define the goal state and the initial state
GOAL_STATE = tuple(map(tuple, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]))
INITIAL_STATE = tuple(map(tuple, [[1, 2, 3], [4, 5, 6], [0, 7, 8]]))

# Create a stack for the frontier
frontier = deque()

# Create a graph to store the state space
G = nx.Graph()

# Define the search function
def search(state):
    frontier.append(state)
    G.add_node(state)
    while frontier:
        state = frontier.pop()
        if state == GOAL_STATE:
            return True
        for action in ACTIONS:
            new_state = apply_action(state, action)
            if new_state is not None and new_state not in G:
                G.add_edge(state, new_state)
                frontier.append(new_state)
    return False

# Define the action function
def apply_action(state, action):
    new_state = [list(row) for row in state]
    i, j = next((i, j) for i, row in enumerate(state) for j, cell in enumerate(row) if cell == 0)
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

ACTIONS = ['up', 'down', 'left', 'right']

# Perform the search
found = search(INITIAL_STATE)

# Print the result
print(f'Goal found: {found}')

# Print the path from the initial state to the goal state to the terminal
print("Path from the initial state to the goal state:")
path = nx.shortest_path(G, source=INITIAL_STATE, target=GOAL_STATE)

print(len(path))
'''
for state in path:
    for row in state:
        print(row)
    print()

# Create a Digraph object
dot = Digraph()

# Add nodes and edges to the graph
for state in G.nodes:
    if state == INITIAL_STATE:
        dot.node(str(state), color='green')
    elif state in nx.shortest_path(G, source=INITIAL_STATE, target=GOAL_STATE):
        dot.node(str(state), color='blue')
    else:
        dot.node(str(state), color='red')

for state1, state2 in G.edges:
    dot.edge(str(state1), str(state2))

# Render the graph
dot.render('state_space.gv', view=True)
'''
