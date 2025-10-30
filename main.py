from src.functions import *
from src.algorithms.bfs import BFS
from src.algorithms.dfs import DFS
from src.algorithms.iddfs import IDDFS
from src.algorithms.ucs import UCS
from src.algorithms.a_star import AStar
from src.algorithms.weighted_a_star import WeightedAStar
from src.algorithms.greedy import Greedy
from src.interface import BirdSortGame
from results.results import *

def run_and_register_algorithm(algorithm_class, algorithm_name, board):
    print(f"\nSolving with {algorithm_name}...")
    algorithm = algorithm_class()
    algorithm.solve(board)
    time, path_length, states_generated = algorithm.display_results()
    registrar_execucao(algorithm_name.lower().replace(" ", "_"), time, path_length, states_generated)

def main():
    
    branches = int(input('Number of branches (must be greater than 1 and less than 9): '))
    while branches <= 1 or branches >= 9:
        branches = int(input('Number of branches (must be greater than 1 and less than 9): '))

    choice = input("Press 'A' for a random board, or 'M' to create a board manually: ").strip().upper()
    while choice not in ['M', 'A']:
        choice = input("Press 'A' for a random board, or 'M' to create a board manually: ").strip().upper()

    if choice == 'M':
        board = define_tabuleiro_manualmente(branches + 2)
        while board is None:
            board = define_tabuleiro_manualmente(branches + 2)
    else:
        board = define_tabuleiro(branches)
        board = popula_tabuleiro(board)

    print(board)
    exibe_tabuleiro(board)

    possible_choices_origin_destination = {i + 1: f'Galho {i + 1}' for i in range(branches + 2)}

    if verifica_se_tabuleiro_esta_completo(board):
        print("The board is already solved! Congratulations, you didn't have to do anything.")
        return

    mode = input("Play (J) or see the automatic solution (S)? ").strip().upper()
    if mode == 'S':
        run_and_register_algorithm(BFS, "BFS", board)
        run_and_register_algorithm(Greedy, "Greedy", board)
        run_and_register_algorithm(WeightedAStar, "Weighted A*", board)
        run_and_register_algorithm(AStar, "A*", board)
        run_and_register_algorithm(UCS, "UCS", board)
        run_and_register_algorithm(DFS, "DFS", board)
        run_and_register_algorithm(IDDFS, "IDDFS", board)

        exibir_resultados_comparativos()
    
    else:
        game_type_choice = input("Play in the console (C) or in the graphical interface (I)? ").strip().upper()
        while game_type_choice not in ['C', 'I']:
            game_type_choice = input("Choose 'C' (console) or 'I' (interface): ").strip().upper()

        if game_type_choice == 'I':
            game = BirdSortGame(board)
            game.run()
        else:
            while True:
                hint_choice = input("If you need a hint, type 'D' and press enter. Otherwise, just press enter. ")
                if hint_choice.lower() == 'd':
                    print("\nLooking for the next move...")
                    algorithm = AStar()
                    hint = algorithm.get_hint(board=board)
                    print("Move:")
                    print(hint)
                    
                origin_choice = int(input("Choose the origin branch: "))
                destination_choice = int(input("Choose the destination branch: "))

                while not (realiza_voo_passaro(board, possible_choices_origin_destination[origin_choice], possible_choices_origin_destination[destination_choice])):
                    print(f"The bird cannot fly from {possible_choices_origin_destination[origin_choice]} to {possible_choices_origin_destination[destination_choice]}.")
                    origin_choice = int(input("Choose another origin branch: "))
                    destination_choice = int(input("Choose another destination branch: "))

                if verifica_se_ganhou(board):
                    print("Congratulations!")
                    break

                exibe_tabuleiro(board)

def generate_automatic_solution_execution_for_registration(branches, number_of_executions):
    for i in range(number_of_executions):
        print("Execution number", i + 1)
        board = define_tabuleiro(branches)
        board = popula_tabuleiro(board)
        exibe_tabuleiro(board)

        if verifica_se_tabuleiro_esta_completo(board):
            print("The board is already solved! Congratulations, you didn't have to do anything.")
            return

        run_and_register_algorithm(BFS, "BFS", board)
        run_and_register_algorithm(Greedy, "Greedy", board)
        run_and_register_algorithm(WeightedAStar, "Weighted A*", board)
        run_and_register_algorithm(AStar, "A*", board)
        run_and_register_algorithm(UCS, "UCS", board)
        run_and_register_algorithm(DFS, "DFS", board)
        run_and_register_algorithm(IDDFS, "IDDFS", board)

        exibir_resultados_comparativos()

if __name__ == '__main__':
    main()
