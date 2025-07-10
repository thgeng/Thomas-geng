#!/usr/bin/env python3

import sys

DIRECTIONS = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1),
}

class State:
    def __init__(self, robot_pos, dirty, path):
        self.robot_pos = robot_pos
        self.dirty = frozenset(dirty)
        self.path = path

    def is_goal (self):
        return len(self.dirty) == 0
    
    def __hash__(self):
      return hash((self.robot_pos,self.dirty)) 

    def __eq__(self, other) :
        return self.robot_pos == other.robot_pos and self.dirty == other.dirty 
    
def apply(filename):
    with open (filename) as f:
        col = int(f.readline())
        row = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(row)]
    return col, row, grid
    
def get_initial_state(grid):
    dirty = set()
    robot = None 
    for r, row in enumerate(grid): # moving up to down 
        for c, val in enumerate(row): # moving left to right 
            if val == '@': #this is start location by robot
                robot = (r, c)
            elif val == '*':
                dirty.add((r, c))
    return State(robot, dirty, []) # this is going back to original locaion robot is original location, begining all the dirty spot, initial path 

def get_successors(state, grid):
    successors = []#empty state  
    r, c = state.robot_pos #robot location 
    rows, cols = len(grid), len(grid[0]) #map 

    #moving action 
    for action, (dr, dc) in DIRECTIONS.items():
        nr, nc = r +dr, c + dc  # after move to the new location 
        #check hit the wall 
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            # if can move append in the new sta e successor 
            successors.append(State((nr, nc), state.dirty, state.path + [action]))
        # Vaccum action 
    if (r, c) in state.dirty:
        new_dirty = set(state.dirty)
        new_dirty.remove((r, c))
        successors.append(State((r, c), new_dirty, state.path + ['clean']))

    return  successors

def dfs(initial_state, grid):
    stack = [initial_state]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if state.is_goal():
            return state.path, nodes_generated, nodes_expanded

        for succ in get_successors(state, grid):
            stack.append(succ)
            nodes_generated += 1

    return [], nodes_generated, nodes_expanded

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 DFS.py depth-first <world_file>")
        return

    algorithm = sys.argv[1]
    filename = sys.argv[2]
    _, _, grid = apply(filename)
    initial_state = get_initial_state(grid)

    if algorithm == 'depth-first':
        path, generated, expanded = dfs(initial_state, grid)
    else:
        print("Only depth-first is implemented.")
        return

    for step in path:
        print(step)
    print(f"{generated} nodes generated")
    print(f"{expanded} nodes expanded")

if __name__ == "__main__":
    main()


