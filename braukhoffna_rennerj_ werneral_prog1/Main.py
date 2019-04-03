import itertools
import random
from filecmp import cmp
from tkinter import *
from tkinter import messagebox
import time
import math


def main():
    grid = puzzle()
    root = Tk()
    btns = [x[:] for x in [[0] * 3] * 3]
    for row in range(3):
        for col in range(3):
            btns[row][col] = Button(root, text="%s,%s" % (row, col),
                                    command=lambda row=row, col=col: click(row, col, grid, btns),
                                    font=("Courier", 44))
            btns[row][col].grid(row=row, column=col, sticky="nsew")
    update_btns(grid, btns)

    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label='Grid', menu=file_menu)
    file_menu.add_command(label='Reset', command=lambda: reset(grid, btns))
    file_menu.add_command(label='Random State', command=lambda: random_grid(grid, btns))
    file_menu.add_command(label='Input State', command=lambda: input_grid(grid, btns))

    solve_menu = Menu(menu)
    menu.add_cascade(label='Solve', menu=solve_menu)
    solve_menu.add_command(label='Breadth First Search', command=lambda: bfs(grid, btns, root))
    solve_menu.add_command(label='A* Search', command=lambda: a_star(grid, btns, root))
    solve_menu.add_command(label='Greedy Best First Search', command=lambda: greedy_bfs(grid, btns, root))

    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(3, weight=1)

    root.mainloop()


def click(row, col, grid, btns):
    grid.vals = update_vals(grid.vals, row, col)
    update_btns(grid, btns)


def reset(grid, btns):
    grid.reset()
    update_btns(grid, btns)


def random_grid(grid, btns):
    grid.new_grid()
    update_btns(grid, btns)


def input_grid(grid, btns):
    get_grid = Tk()

    Label(get_grid, text='Enter A String of Numbers such as \'123456780\'').grid(row=0)
    txt = Entry(get_grid)
    txt.grid(row=1, sticky='nsew')
    txt.focus_set()
    btn = Button(get_grid, text='Submit',
                 command=lambda form=get_grid, field=txt: save_string(form, field, grid, btns))
    btn.grid(row=2, sticky='nsew')
    get_grid.grid_columnconfigure(0, weight=1)
    get_grid.mainloop()


def save_string(form, field, grid, btns):
    try:
        string = field.get()
        form.destroy()
        grid.specific_grid(string)
    except Exception as inst:
        messagebox.showinfo("Error", inst.args[0])
        grid.reset()
    update_btns(grid, btns)


def update_btns(grid, btns):
    for i in range(3):
        for j in range(3):
            if grid.vals[i][j] != 0:
                btns[i][j].config(text=str(grid.vals[i][j]))
            else:
                btns[i][j].config(text='')


def update_vals(vals, row, col):
    new_vals = [x[:] for x in [[0] * 3] * 3]
    for i, j in itertools.product(range(3), repeat=2):
        new_vals[i][j] = vals[i][j]
    if new_vals[row][col] != 0:
        for direction in range(0, 4):
            new_row = row + (direction - 1 if direction % 2 == 0 else 0)
            new_col = col + (direction - 2 if direction % 2 == 1 else 0)
            if not (new_row < 0 or new_row >= 3 or
                    new_col < 0 or new_col >= 3):
                if new_vals[new_row][new_col] == 0:
                    temp = new_vals[new_row][new_col]
                    new_vals[new_row][new_col] = new_vals[row][col]
                    new_vals[row][col] = temp
    return new_vals


def get_moves(vals):
    row = -1
    col = -1
    for i, j in itertools.product(range(3), repeat=2):
        if vals[i][j] == 0:
            row = i
            col = j
    moves = []
    for direction in range(0, 4):
        new_row = row + (direction - 1 if direction % 2 == 0 else 0)
        new_col = col + (direction - 2 if direction % 2 == 1 else 0)
        if not (new_row < 0 or new_row >= 3 or
                new_col < 0 or new_col >= 3):
            moves.append([new_row, new_col])
    return moves


def bfs(grid, btns, root):
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    start_time = time.time()

    # Each node in the queue consists of 3 elements
    # 0: Current State
    # 1: Parent State
    queue = [[grid.vals, None]]

    # Each node in the explored list consists of 2 elements
    # 0: State
    # 1: Parent
    explored = {}

    while len(queue) != 0:
        node = queue.pop(0)
        explored[str(node[0])] = node[1]
        if node[0] == goal:
            break

        # Add children
        moves = get_moves(node[0])
        for move in moves:
            new_state = update_vals(node[0], move[0], move[1])
            if str(new_state) not in explored:
                queue.append((new_state, node[0]))

    solution = [goal]
    while solution[-1] is not None:
            solution.append(explored[str(solution[-1])])
    solution.pop(-1)
    end_time = time.time()
    moves = len(solution) - 1
    display_output(grid, solution, btns, root)
    messagebox.showinfo("Search Information", "Moves: " + str(moves) +
                        "\nTime: " + str(end_time - start_time) +
                        "\nTotal Nodes Visited: " + str(len(explored)))


class Node:
    grid = []
    parent = None
    g = 0
    f = 0

    def __init__(self, grid, parent, g):
        self.grid = grid
        self.parent = parent
        self.g = g
        self.f = 0

    def calculate_heuristic(self):
        if self.grid == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            self.f = 0
        else:
            self.f = self.g + manhattan_heuristic(self.grid)


class puzzle:
    vals = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

    def reset(self):
        self.vals = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

    def new_grid(self):
        self.vals = [x[:] for x in [[0] * 3] * 3]
        for i in range(1, 9):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            while self.vals[x][y] != 0:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
            self.vals[x][y] = i

        # Check Solvability
        if not self.check_solvable(self.vals):
            self.new_grid()

    def specific_grid(self, grid_vals):
        vals = [int(i) for i in list(grid_vals)]
        digits = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if not (all(elem in vals for elem in digits) and len(vals) == len(digits)):
            raise Exception('Invalid Input.')
        self.vals = [x[:] for x in [[0] * 3] * 3]
        for i, j in itertools.product(range(3), repeat=2):
            self.vals[i][j] = vals[i * 3 + j]
        if not self.check_solvable(self.vals):
            raise Exception('Puzzle is not solvable from that state.')

    # Returns true if solvable, false otherwise
    # Algorithm adapted from https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
    def check_solvable(self, vals):
        inversions = 0
        flat = list(itertools.chain.from_iterable(vals))
        for i in range(len(flat)):
            if flat[i] != 0:
                for j in range(i + 1, len(flat)):
                    if flat[j] != 0 and flat[i] > flat[j]:
                        inversions += 1
        return inversions % 2 == 0


def a_star(grid, btns, root):
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    start_time = time.time()

    g = 0

    # list contains - Node : (grid, parent grid, g)
    open_list = [Node(grid.vals, None, g)]
    traversed = {}

    goal_node = None
    while len(open_list) != 0:
        # Sort open, pop the least f node, and append to traversed
        open_list.sort(key=lambda y: y.f)
        x = open_list.pop(0)
        traversed[str(x.grid)] = x
        if x.grid == goal:
            goal_node = x
            break

        # Append children to open_list
        children = get_moves(x.grid)
        for child in children:
            child_grid = update_vals(x.grid, child[0], child[1])
            child_node = Node(child_grid, x, x.g + 1)
            child_node.calculate_heuristic()
            if str(child_grid) not in traversed:
                open_list.append(child_node)

    solution = []
    while goal_node.parent is not None:
        solution.append(goal_node.grid)
        goal_node = goal_node.parent
    end_time = time.time()
    moves = len(solution)
    if len(solution) == 0:
        solution = [goal]
    display_output(grid, solution, btns, root)
    messagebox.showinfo("Search Information", "Moves: " + str(moves) +
                        "\nTime: " + str(end_time - start_time) +
                        "\nTotal Nodes Visited: " + str(len(traversed)))


def manhattan_heuristic(grid):
    total = 0
    for val in range(9):
        for row, col in itertools.product(range(3), repeat=2):
            if grid[row][col] == val:
                total += math.fabs(math.floor((val - 1) / 3) - row)
                total += math.fabs((val - 1) % 3 - col)
                break

    return total


def display_output(grid, solution, btns, root):
    grid.vals = solution.pop(-1)
    update_btns(grid, btns)
    if len(solution) != 0:
        root.after(300, lambda: display_output(grid, solution, btns, root))


def greedy_bfs(grid, btns, root):
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    start_time = time.time()

    open_node = list()
    close_node = list()

    next_node = Node(grid.vals, None, 0)
    open_node.append(next_node)

    while len(open_node) != 0:
        open_node.sort(key=lambda o: o.g)
        next_node = open_node.pop(0)

        if next_node.grid == goal:
            close_node.insert(len(close_node) + 1, next_node)
            break

        # create children
        moves = get_moves(next_node.grid)
        for move in moves:
            child = Node(update_vals(next_node.grid, move[0], move[1]), next_node, 0)
            child.g = calculate_heuristic_value(goal, child.grid)
            if child.grid not in close_node:
                open_node.insert(len(open_node) + 1, child)

        if next_node.grid not in close_node:
            close_node.insert(len(close_node) + 1, next_node.grid)

    move_set = [next_node.grid]
    while next_node.parent is not None:
        move_set.append(next_node.grid)
        next_node = next_node.parent

    end_time = time.time()

    display_output(grid, move_set, btns, root)
    messagebox.showinfo("Search Information", "Moves: " + str(len(move_set)) +
                        "\nTime: " + str(end_time - start_time) +
                        "\nTotal Nodes Visited: " + str(len(close_node)))


# calculate how many numbers are in the wrong spot in the grid
def calculate_heuristic_value(goal, grid):
    total = 0
    for row, col in itertools.product(range(3), repeat=2):
        if grid[row][col] != goal[row][col]:
            total += 1
    return total


if __name__ == '__main__':
     main()
