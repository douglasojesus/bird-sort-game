import itertools
from queue import PriorityQueue
from src.search_algorithm import SearchAlgorithm
from src.functions import verifica_se_ganhou, verifica_se_pode_voar, realiza_voo_passaro

class UCS(SearchAlgorithm):
    def solve(self, board):
        self.start_timer()
        priority_queue = PriorityQueue()
        counter = itertools.count()
        priority_queue.put((0, next(counter), board, []))
        visited = set()

        while not priority_queue.empty():
            accumulated_cost, _, current_state, path = priority_queue.get()

            if verifica_se_ganhou(current_state):
                self.solution_path = path
                self.stop_timer()
                return path

            state_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in current_state.items())
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            for origin in current_state:
                if not current_state[origin] or current_state[origin] == 'X':
                    continue

                for destination in current_state:
                    if origin == destination or current_state[destination] == 'X':
                        continue

                    new_state = {k: v.copy() if v != 'X' else 'X' for k, v in current_state.items()}

                    if verifica_se_pode_voar(new_state, origin, destination):
                        realiza_voo_passaro(new_state, origin, destination)
                        new_state_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in new_state.items())

                        if new_state_tuple not in visited:
                            priority_queue.put((
                                accumulated_cost + 1,
                                next(counter),
                                new_state,
                                path + [(origin, destination)]
                            ))
                            self.states_generated += 1
        return None
