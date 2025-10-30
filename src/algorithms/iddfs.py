from src.algorithms.dfs import DFS
from src.search_algorithm import SearchAlgorithm

class IDDFS(SearchAlgorithm):
    def solve(self, board):
        self.start_timer()
        max_depth = 0

        while True:
            dfs = DFS()
            result = dfs.solve(board, max_depth)
            self.states_generated += dfs.get_states_generated()

            if result is not None:
                self.solution_path = result
                self.stop_timer()
                return result
            max_depth += 1
