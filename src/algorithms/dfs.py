from collections import deque
from src.search_algorithm import SearchAlgorithm
from src.functions import verifica_se_ganhou, verifica_se_pode_voar, realiza_voo_passaro

class DFS(SearchAlgorithm):
    def solve(self, board, max_depth=None):
        self.start_timer()
        stack = deque()
        stack.append((board, [], 0))
        visited = set()

        while stack:
            current_state, path, depth = stack.pop()

            if verifica_se_ganhou(current_state):
                self.solution_path = path
                self.stop_timer()
                return path

            if max_depth is not None and depth >= max_depth:
                continue

            state_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in current_state.items())
            visited.add(state_tuple)

            for origin in current_state:
                for destination in current_state:
                    if origin != destination and current_state[origin] and current_state[destination] != 'X':
                        new_state = {k: v.copy() if v != 'X' else 'X' for k, v in current_state.items()}

                        if verifica_se_pode_voar(new_state, origin, destination):
                            realiza_voo_passaro(new_state, origin, destination)
                            new_state_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in new_state.items())

                            if new_state_tuple not in visited:
                                stack.append((new_state, path + [(origin, destination)], depth + 1))
                                self.states_generated += 1
        return None
