import itertools
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
    def check_solvable(vals):
        inversions = 0
        flat = list(itertools.chain.from_iterable(vals))
        for i in range(len(flat)):
            if flat[i] != 0:
                for j in range(i + 1, len(flat)):
                    if flat[j] != 0 and flat[i] > flat[j]:
                        inversions += 1
        return inversions % 2 == 0
