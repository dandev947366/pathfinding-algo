from pathfinding.core.grid import Grid

matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
]

# 1. create a grid
grid = Grid(matrix=matrix)
# 2. create a start and end cell
start = grid.node(0,0)
end = grid.node(5,2)