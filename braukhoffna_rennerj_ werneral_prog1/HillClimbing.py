import time


class HillClimbing:
    goal = None
    start_time = None

    def __init__(self):
        self.goal = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]
        self.start_time = time.time()
