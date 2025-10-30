import time

class SearchAlgorithm:
    def __init__(self):
        self.execution_time = 0
        self.states_generated = 0
        self.solution_path = []
        self.start_time = 0

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        end_time = time.time()
        self.execution_time = float(end_time - self.start_time)

    def get_states_generated(self):
        return self.states_generated

    def get_execution_time(self):
        return self.execution_time

    def get_solution_path(self):
        return self.solution_path

    def solve(self, board):
        raise NotImplementedError

    def display_results(self):
        if self.solution_path:
            print(f"Solution found in {len(self.solution_path)} moves!")
            print(f"Execution time: {self.execution_time:.4f} seconds.")
            print(f"States generated: {self.states_generated}.")
            print("Move sequence:")
            for move in self.solution_path:
                print(f"Move from {move[0]} to {move[1]}")
        else:
            print("Could not find a solution.")
        return self.execution_time, len(self.solution_path), self.states_generated

    def get_hint(self, board):
        path = self.solve(board)

        if path and len(path) > 0:
            self.solution_path = path
            return f"Move from {path[0][0]} to {path[0][1]}"
        return None
