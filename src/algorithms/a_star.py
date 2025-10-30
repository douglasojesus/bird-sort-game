import itertools
from queue import PriorityQueue
from src.search_algorithm import SearchAlgorithm
from src.functions import verifica_se_ganhou, verifica_se_pode_voar, realiza_voo_passaro

class AStar(SearchAlgorithm):
    def _heuristic_prioritize_almost_complete(self, state):
        estimated_cost = 0

        almost_complete_branches = []
        for branch, birds in state.items():
            if birds == 'X' or len(birds) < 3:
                continue
            most_common_bird = max(set(birds), key=birds.count)
            if birds.count(most_common_bird) == 3:
                almost_complete_branches.append((branch, most_common_bird))

        for branch, birds in state.items():
            if birds == 'X' or not birds:
                continue

            if len(birds) == 4 and len(set(birds)) == 1:
                continue

            if (branch, birds[0]) in almost_complete_branches:
                estimated_cost += 1
                continue

            most_common_bird = max(set(birds), key=birds.count)
            estimated_cost += len([b for b in birds if b != most_common_bird])

        return estimated_cost

    def solve(self, board):
        self.start_timer()
        priority_queue = PriorityQueue()
        counter = itertools.count()
        priority_queue.put((0 + self._heuristic_prioritize_almost_complete(board), next(counter), board, [], 0))
        visited = set()

        while not priority_queue.empty():
            _, _, current_state, path, accumulated_cost = priority_queue.get()

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
                            new_cost = accumulated_cost + 1
                            priority = new_cost + self._heuristic_prioritize_almost_complete(new_state)
                            priority_queue.put((
                                priority,
                                next(counter),
                                new_state,
                                path + [(origin, destination)],
                                new_cost
                            ))
                            self.states_generated += 1
        return None

    def get_hint(self, board):
        path = self.solve(board)

        if path and len(path) > 0:
            self.solution_path = path
            return f"Move from {path[0][0]} to {path[0][1]}"
        return None
