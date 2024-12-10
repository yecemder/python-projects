import pygame
import random
import heapq

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Algorithm Visualization")

# Cell Class
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.neighbors = []
        self.previous = None
        self.wall = True
        self.visited = False

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def add_neighbors(self, grid):
        if self.row < ROWS - 2:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 1:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 2:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 1:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

# Generate the grid
def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid

# Draw the grid lines
def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        for j in range(COLS):
            pygame.draw.line(win, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

# Draw everything
def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            if cell.wall:
                cell.draw(win, BLACK)
            elif cell.visited:
                cell.draw(win, BLUE)
            else:
                cell.draw(win, WHITE)
    draw_grid(win)
    pygame.display.update()

# Recursive Backtracker Maze Generation
def generate_maze(grid, start, end):
    stack = [start]
    start.wall = False  # Start cell should not be a wall

    while stack:
        current = stack.pop()
        current.visited = True

        # Find unvisited neighbors with walls
        neighbors = [cell for cell in current.neighbors if cell.wall and not cell.visited]
        if neighbors:
            stack.append(current)
            neighbor = random.choice(neighbors)
            neighbor.visited = True
            neighbor.wall = False
            # Remove the wall between current and neighbor
            wall_between = grid[(current.row + neighbor.row) // 2][(current.col + neighbor.col) // 2]
            wall_between.wall = False
            stack.append(neighbor)
        draw(WIN, grid)

    # Ensure there's a path to the goal by carving a direct path if necessary
    carve_path_to_goal(grid, start, end)

# Ensure there's a path from start to end
def carve_path_to_goal(grid, start, end):
    current = start
    while current != end:
        if current.row < end.row:
            next_cell = grid[current.row + 1][current.col]
        elif current.row > end.row:
            next_cell = grid[current.row - 1][current.col]
        elif current.col < end.col:
            next_cell = grid[current.row][current.col + 1]
        elif current.col > end.col:
            next_cell = grid[current.row][current.col - 1]
        next_cell.wall = False
        current = next_cell

# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

# A* Pathfinding Algorithm
def a_star_algorithm(grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start, end)

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            end.draw(WIN, GREEN)
            return True

        for neighbor in current.neighbors:
            if neighbor.wall:
                continue
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.visited = True

        draw(WIN, grid)
        if current != start:
            current.draw(WIN, RED)

    return False

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.draw(WIN, GREEN)
        pygame.display.update()

def main():
    grid = make_grid()
    for row in grid:
        for cell in row:
            cell.add_neighbors(grid)

    start = grid[0][0]
    end = grid[ROWS-1][COLS-1]
    start.wall = False
    end.wall = False

    generate_maze(grid, start, end)

    for row in grid:
        for cell in row:
            cell.visited = False

    a_star_algorithm(grid, start, end)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
