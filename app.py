from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
]

# 1. Create a grid
grid = Grid(matrix=matrix)

# 2. Create a start and end cell
start = grid.node(0, 0)  # Start node at top-left corner
end = grid.node(5, 2)    # End node at bottom-right corner

# 3. Create a finder with a movement style
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

# 4. Use the finder to find path
path, runs = finder.find_path(start, end, grid)

print(f"Path: {path}")
print(f"Number of runs: {runs}")
