from src.functions import *
import src.algorithm as algorithm

# criar possibilidade de iniciar jogo a partir de um tabuleiro criado pelo professor
# ele insere os galhos e como eles vão estar ajustados, ao invés de aleatoriamente
# o jogo gráfico pode ser só para o humano; a parte do uso do algoritmos pode estar para o terminal
# a heurística pode ser pensada como uma "vantagem" em um jogo real: o problema é codificar isso
# sobre a apresentação, vai depender da escolha do grupo

def main():
    galhos = int(input('Número de galhos: '))
    escolha = input("Se você quer usar um tabuleiro aleatório pressione 'A', se quer adicionar um tabuleiro manualmente, adicione 'M': ")

    if escolha == 'M':
        tabuleiro = define_tabuleiro_manualmente(galhos)
        while tabuleiro == None:
            tabuleiro = define_tabuleiro_manualmente(galhos)
    else:
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
        bfs = algorithm.Algoritmo()
        bfs.resolver_com_bfs(tabuleiro)
        bfs.exibe()
        
        print("\nResolvendo o jogo com DFS...")
        dfs = algorithm.Algoritmo()
        dfs.resolver_com_dfs(tabuleiro)
        dfs.exibe()

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


if __name__ == '__main__':
    main()