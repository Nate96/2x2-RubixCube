import itertools
import time
import Main


class GreedyBFS:
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

    start_time = None
    grid = None
    root = None

    def __init__(self, grid, root):
        self.start_time = time.time()
        self.grid = grid
        self.root = root

    """
    def run(problem)
        open = set()
        close = set() 
        
        add root to open
        while root != goals
            get moves
            for (number of moves)
                create neighbor for move x
                if (neighbor.value < root.value)
                    add root to close
                    root = neighbor 
                    add root to open
                    break
                else if (i = move length 
                    get node from open with least value
                    root = node    
    """

    # calculate how many numbers are in the wrong spot in the grid
    def calculate_heuristic_value(self, grid):
        total = 0
        for row, col in itertools.product(range(3), repeat=2):
            if grid[row][col] != self.goal[row][col]:
                total += 1
        return total

    # create neighbor


if __name__ == '__main__':
    test = GreedyBFS(None, None)
    print(test.calculate_heuristic_value([[2, 1, 3],
                                    [4, 5, 6],
                                    [7, 0, 9]]))
