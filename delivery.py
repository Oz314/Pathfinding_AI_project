import tkinter as tk
import heapq
import time
import random

# Grid parameters
CELL_SIZE = 25
ROWS = 20
COLS = 20
NUM_OBSTACLES = 90

# Modern colors
COLOR_BG = "#2C2F33"
COLOR_FREE = "#99AAB5"
COLOR_WALL = "#23272A"
COLOR_START = "#3B88C3"
COLOR_END = "#E91E63"
COLOR_PATH = "#43B581"
COLOR_VISITED = "#FEE75C"
COLOR_TEXT = "#ffffff"

# Window creation
window = tk.Tk()
window.title("A* Pathfinding - AI Mini Project (with Arrows)")
window.config(bg=COLOR_BG)

title_label = tk.Label(window, text="🧭 Optimal Path Search (A*)", 
                 font=("Helvetica", 16, "bold"), bg=COLOR_BG, fg="white")
title_label.pack(pady=10)

# Canvas
canvas = tk.Canvas(window, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, 
                   bg=COLOR_BG, highlightthickness=0)
canvas.pack(pady=10)

# Result label
result_label = tk.Label(window, text="", font=("Helvetica", 13, "bold"), 
                          bg=COLOR_BG, fg="white")
result_label.pack(pady=5)

# Grid creation
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)

def generate_obstacles():
    """Generate random obstacles in the grid."""
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j] = 0
    for _ in range(NUM_OBSTACLES):
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (x, y) not in [start, end]:
            grid[x][y] = 1

def draw_grid():
    """Draw the base grid."""
    global rectangles
    rectangles = {}
    for i in range(ROWS):
        for j in range(COLS):
            color = COLOR_FREE if grid[i][j] == 0 else COLOR_WALL
            rect = canvas.create_rectangle(
                j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE,
                fill=color, outline=COLOR_BG
            )
            rectangles[(i, j)] = rect

def color_cell(coord, color):
    """Change the color of a cell."""
    canvas.itemconfig(rectangles[coord], fill=color)
    window.update()

def heuristic(a, b):
    """Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, end):
    """A* algorithm."""
    neighbors = [(0,1),(1,0),(-1,0),(0,-1)]
    queue = []
    heapq.heappush(queue, (heuristic(start, end), 0, start))
    costs = {start: 0}
    parents = {start: None}

    while queue:
        _, cost, current = heapq.heappop(queue)

        if current == end:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]

        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost + 1
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(queue, (priority, new_cost, neighbor))
                    parents[neighbor] = current

                    if neighbor not in [start, end]:
                        color_cell(neighbor, COLOR_VISITED)
                        time.sleep(0.005)
    return None

def draw_arrow(start, end):
    """Draw a directional arrow between two cells in the path."""
    x1, y1 = start[1]*CELL_SIZE + CELL_SIZE/2, start[0]*CELL_SIZE + CELL_SIZE/2
    x2, y2 = end[1]*CELL_SIZE + CELL_SIZE/2, end[0]*CELL_SIZE + CELL_SIZE/2

    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill=COLOR_PATH)
    window.update()

def start_search():
    """Launch the A* search and display arrows for the path."""
    generate_obstacles()
    draw_grid()
    color_cell(start, COLOR_START)
    color_cell(end, COLOR_END)
    result_label.config(text="Searching for the best path...", fg="white")
    window.update()

    path = a_star(grid, start, end)

    if path:
        for i in range(1, len(path)):
            previous = path[i-1]
            current = path[i]
            if current not in [start, end]:
                color_cell(current, COLOR_PATH)
            draw_arrow(previous, current)
            time.sleep(0.02)
        result_label.config(text="✅ Path found successfully!", fg="#43B581")
    else:
        result_label.config(text="❌ No possible path found.", fg="#E91E63")

# Launch button
btn_start = tk.Button(window, text="🔁 Generate and Run A*", 
                       command=start_search, 
                       font=("Helvetica", 12, "bold"), 
                       bg="#5865F2", fg="white", relief="flat", padx=10, pady=5)
btn_start.pack(pady=10)

# Initialization
draw_grid()
color_cell(start, COLOR_START)
color_cell(end, COLOR_END)

window.mainloop()
