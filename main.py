from functions import *
import algorithms

def main():
    galhos = int(input('Número de galhos: '))
    tabuleiro = define_tabuleiro(galhos, 0)
    tabuleiro = popula_tabuleiro(tabuleiro)

    exibe_tabuleiro(tabuleiro)

    galhos_completos = verifica_se_pilha_esta_completa(tabuleiro)

    possiveis_escolhas_origem_destino = {}
    for i in range(galhos+2):
        possiveis_escolhas_origem_destino[i+1] = 'Galho '+str(i+1)

    modo = input("Deseja jogar (J) ou ver a solução automática (S)? ").strip().upper()
    if modo == 'S':
        print("\nResolvendo o jogo com BFS...")
        solucao, tempo_bfs = algorithms.resolver_com_bfs(tabuleiro)

        if solucao:
            print(f"Solução encontrada em {len(solucao)} movimentos!")
            print(f"Solução encontrada em {tempo_bfs} segundos.")
            print("Sequência de movimentos:")
            for movimento in solucao:
                print(f"Mover de {movimento[0]} para {movimento[1]}")
        else:
            print("Não foi possível encontrar uma solução.")

        print("\nResolvendo o jogo com DFS...")
        solucao, tempo_dfs = algorithms.resolver_com_dfs(tabuleiro)

        if solucao:
            print(f"Solução encontrada em {len(solucao)} movimentos!")
            print(f"Solução encontrada em {tempo_dfs} segundos.")
            print("Sequência de movimentos:")
            for movimento in solucao:
                print(f"Mover de {movimento[0]} para {movimento[1]}")
        else:
            print("Não foi possível encontrar uma solução.")
            
    else:
        while True:
            
            escolha_origem = int(input("Escolha o galho de origem: "))        
            escolha_destino = int(input("Escolha o galho de destino: "))

            while not (realiza_voo_passaro(tabuleiro, possiveis_escolhas_origem_destino[escolha_origem], possiveis_escolhas_origem_destino[escolha_destino])):
                print(f"Pássaro não pode sair da origem {possiveis_escolhas_origem_destino[escolha_origem]} e ir para o destino {possiveis_escolhas_origem_destino[escolha_destino]}.")
                escolha_origem = int(input("Escolha outro galho de origem: "))
                escolha_destino = int(input("Escolha outro galho de destino: "))

            if verifica_se_ganhou(tabuleiro):
                print("Parabéns!")
                break
            exibe_tabuleiro(tabuleiro)


main()