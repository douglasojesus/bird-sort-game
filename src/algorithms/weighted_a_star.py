import itertools
from queue import PriorityQueue
from src.search_algorithm import SearchAlgorithm
from src.functions import verifica_se_ganhou, verifica_se_pode_voar, realiza_voo_passaro

class WeightedAStar(SearchAlgorithm):
    def __init__(self, heuristic_weight=1.5):
        super().__init__()
        self.heuristic_weight = heuristic_weight

    def _heuristic_simple_modular(self, state):
        points = 0

        total_birds = sum(len(b) for b in state.values() if b != 'X')

        types_per_branch = []
        for branch, birds in state.items():
            if birds == 'X':
                continue
            types_per_branch.append(len(set(birds)))

        dispersion_factor = sum(types_per_branch)

        empty_branches = sum(1 for b in state.values() if b != 'X' and not b)

        points = total_birds + dispersion_factor - empty_branches

        return points

    def _heuristic_admissible(self, state):
        minimum_moves = 0

        for branch, birds in state.items():
            if birds == 'X' or not birds:
                continue

            if len(birds) == 4 and len(set(birds)) == 1:
                continue

            if birds:
                most_common_type = max(set(birds), key=birds.count)
                minimum_moves += len([b for b in birds if b != most_common_type])

        return minimum_moves

    def solve(self, board):
        self.start_timer()
        priority_queue = PriorityQueue()
        counter = itertools.count()
        priority_queue.put((
            0 + self.heuristic_weight * self._heuristic_simple_modular(board),
            next(counter),
            board,
            [],
            0
        ))
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
                            priority = new_cost + self.heuristic_weight * self._heuristic_simple_modular(new_state)
                            priority_queue.put((
                                priority,
                                next(counter),
                                new_state,
                                path + [(origin, destination)],
                                new_cost
                            ))
                            self.states_generated += 1
        return None
