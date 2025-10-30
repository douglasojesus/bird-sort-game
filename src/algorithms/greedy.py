import itertools
from queue import PriorityQueue
from src.search_algorithm import SearchAlgorithm
from src.functions import verifica_se_ganhou, verifica_se_pode_voar, realiza_voo_passaro

class Greedy(SearchAlgorithm):
    def _heuristic_release(self, state):
        points = 0

        congestion = {branch: 0 for branch in state}

        for branch, birds in state.items():
            if birds == 'X' or not birds:
                continue

            if len(birds) >= 3:
                most_common_bird = max(set(birds), key=birds.count)
                qty = birds.count(most_common_bird)

                if qty < 3:
                    congestion[branch] = len(birds) * 10

            if len(set(birds)) == 1 and len(birds) >= 2:
                points -= 50 * len(birds)

        for branch, birds in state.items():
            if birds == 'X' or not birds:
                continue

            top = birds[-1]
            possible_moves = 0

            for other_branch in state:
                if (other_branch != branch and state[other_branch] != 'X' and
                    (not state[other_branch] or state[other_branch][-1] == top)):
                    possible_moves += 1

            points -= 20 * possible_moves

            points += congestion[branch]

        for branch, birds in state.items():
            if birds == 'X' or len(birds) != 3:
                continue

            if len(set(birds)) == 1:
                points -= 300

        return points

    def solve(self, board):
        self.start_timer()
        priority_queue = PriorityQueue()
        counter = itertools.count()
        priority_queue.put((
            self._heuristic_release(board),
            next(counter),
            board,
            []
        ))
        visited = set()

        while not priority_queue.empty():
            _, _, current_state, path = priority_queue.get()

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
                            heuristic = self._heuristic_release(new_state)
                            priority_queue.put((
                                heuristic,
                                next(counter),
                                new_state,
                                path + [(origin, destination)]
                            ))
                            self.states_generated += 1
        return None
