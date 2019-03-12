from tkinter import *
import random


class puzzle:
    vals = [[1, 2, 3],
            [8, None, 4],
            [7, 6, 5]]

    def update_vals(self, row, col):
        grid_size = 3
        if self.vals[row][col] is not None:
            for direction in range(0, 4):
                new_row = row + (direction - 1 if direction % 2 == 0 else 0)
                new_col = col + (direction - 2 if direction % 2 == 1 else 0)
                if not (new_row < 0 or new_row >= grid_size or
                        new_col < 0 or new_col >= grid_size):
                    if self.vals[new_row][new_col] is None:
                        temp = self.vals[new_row][new_col]
                        self.vals[new_row][new_col] = self.vals[row][col]
                        self.vals[row][col] = temp

    def reset(self):
        self.vals = [[1, 2, 3],
                     [8, None, 4],
                     [7, 6, 5]]

    def new_grid(self):
        self.vals = [x[:] for x in [[None] * 3] * 3]
        for i in range(1, 9):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            while self.vals[x][y] is not None:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
            self.vals[x][y] = i


def main():
    vals = puzzle()
    root = Tk()
    btns = [x[:] for x in [[None] * 3] * 3]
    for row in range(3):
        for col in range(3):
            btns[row][col] = Button(root, text="%s,%s" % (row, col),
                               command=lambda row=row, col=col: click(row, col, vals, btns),
                               font=("Courier", 44))
            btns[row][col].grid(row=row, column=col, sticky="nsew")
    update_btns(vals, btns)

    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='Reset', command=lambda vals=vals, btns=btns : reset(vals, btns))
    filemenu.add_command(label='Random Board', command=lambda vals=vals, btns=btns: new_grid(vals, btns))

    root.grid_rowconfigure(10, weight=1)
    root.grid_columnconfigure(10, weight=1)

    root.mainloop()


def click(row, col, vals, btns):
    vals.update_vals(row, col)
    update_btns(vals, btns)


def reset(vals, btns):
    vals.reset()
    update_btns(vals, btns)


def new_grid(vals, btns):
    vals.new_grid()
    update_btns(vals, btns)


def update_btns(vals, btns):
    for i in range(3):
        for j in range(3):
            if vals.vals[i][j] is not None:
                btns[i][j].config(text=str(vals.vals[i][j]))
            else:
                btns[i][j].config(text='')


if __name__ == '__main__':
    main()
