import itertools
from tkinter import *
import random


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
        # Algorithm from https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
        inversions = 0
        flat = list(itertools.chain.from_iterable(self.vals))
        for i in range(len(flat)):
            if flat[i] != 0:
                for j in range(i + 1, len(flat)):
                    if flat[j] != 0 and flat[i] > flat[j]:
                        inversions += 1
        if inversions % 2 == 1:
            self.new_grid()


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
    file_menu.add_command(label='Random Board', command=lambda: random_grid(grid, btns))

    solve_menu = Menu(menu)
    menu.add_cascade(label='Solve', menu=solve_menu)
    solve_menu.add_command(label='Breadth First Search', command=lambda: bfs(grid, btns, root))

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
    # Each node in the queue consists of 3 elements
    # 0: Current State
    # 1: Current Depth
    # 2: Parent State
    queue = [[grid.vals, 0, None]]

    # Each node in the explored list consists of 2 elements
    # 0: State
    # 1: Parent
    explored = {}

    while len(queue) != 0:
        node = queue.pop(0)
        explored[str(node[0])] = node[2]
        # '[[1, 2, 3], [4, 5, 6], [7, 8, 0]]'
        # Check Goal State
        # if node[0] == [[1, 2, 3],
        #                [4, 5, 6],
        #                [7, 8, 0]]:
        #     break
        if node[0] == [[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]]:
            break

        # Add children
        moves = get_moves(node[0])
        for move in moves:
            new_state = update_vals(node[0], move[0], move[1])
            if str(new_state) not in explored:
                queue.append((new_state, node[1] + 1, node[0]))

    solution = [[[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 0]]]
    while solution[-1] is not None:
        solution.append(explored[str(solution[-1])])
    solution.pop(-1)
    display_output(grid, solution, btns, root)


def display_output(grid, solution, btns, root):
    grid.vals = solution.pop(-1)
    update_btns(grid, btns)
    if len(solution) != 0:
        root.after(500, lambda: display_output(grid, solution, btns, root))


if __name__ == '__main__':
    main()
