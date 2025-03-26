from src.functions import *
import src.algorithm as algorithm
from src import interfaceGame
from results.results import *

# criar possibilidade de iniciar jogo a partir de um tabuleiro criado pelo professor
# ele insere os galhos e como eles vão estar ajustados, ao invés de aleatoriamente
# o jogo gráfico pode ser só para o humano; a parte do uso do algoritmos pode estar para o terminal
# a heurística pode ser pensada como uma "vantagem" em um jogo real: o problema é codificar isso
# sobre a apresentação, vai depender da escolha do grupo

def main():
    
    galhos = int(input('Número de galhos (maior que 1): '))
    while galhos <= 1:
        galhos = int(input('Número de galhos (maior que 1): '))

    escolha = input("Se você quer usar um tabuleiro aleatório pressione 'A', se quer adicionar um tabuleiro manualmente, adicione 'M': ").strip().upper()
    while escolha != 'M' and escolha != 'A':
        escolha = input("Se você quer usar um tabuleiro aleatório pressione 'A', se quer adicionar um tabuleiro manualmente, adicione 'M': ").strip().upper()    

    if escolha == 'M':
        tabuleiro = define_tabuleiro_manualmente(galhos)
        while tabuleiro == None:
            tabuleiro = define_tabuleiro_manualmente(galhos)
    else:
        tabuleiro = define_tabuleiro(galhos, 0)
        tabuleiro = popula_tabuleiro(tabuleiro)
    print(tabuleiro)
    exibe_tabuleiro(tabuleiro)

    possiveis_escolhas_origem_destino = {}
    for i in range(galhos+2):
        possiveis_escolhas_origem_destino[i+1] = 'Galho '+str(i+1)

    if verifica_se_tabuleiro_esta_completo(tabuleiro):
        print("Tabuleiro já está solucionado! Parabéns, não precisou fazer nada.")
        return

    modo = input("Deseja jogar (J) ou ver a solução automática (S)? ").strip().upper()
    if modo == 'S':

        print("\nResolvendo o jogo com A*...")
        a_star = algorithm.Algoritmo()
        a_star.resolver_com_a_estrela(tabuleiro)
        tempo, qntd_caminhos = a_star.exibe()

        registrar_execucao('a_star', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com Custo Uniforme...")
        ucs = algorithm.Algoritmo()
        ucs.resolver_com_custo_uniforme(tabuleiro)
        tempo, qntd_caminhos = ucs.exibe()

        registrar_execucao('ucs', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com DFS...")
        dfs = algorithm.Algoritmo()
        dfs.resolver_com_dfs(tabuleiro)
        tempo, qntd_caminhos = dfs.exibe()

        registrar_execucao('dfs', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com DFS Iterarivo...")
        dfsi = algorithm.Algoritmo()
        dfsi.resolver_com_interatividade(tabuleiro)
        tempo, qntd_caminhos = dfsi.exibe()

        registrar_execucao('dfsi', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com BFS...")
        bfs = algorithm.Algoritmo()
        bfs.resolver_com_bfs(tabuleiro)
        tempo, qntd_caminhos = bfs.exibe()

        registrar_execucao('bfs', tempo, qntd_caminhos)

        exibir_resultados_comparativos()
    
    else:
        tipo_de_jogo_escolha = input("Você quer jogar no console (C) ou na interface gráfica (I)? ").strip().upper()
        while tipo_de_jogo_escolha != 'C' and tipo_de_jogo_escolha != 'I':
            tipo_de_jogo_escolha = input("Escolha 'C' (console) ou 'I' (interface): ").strip().upper()
        
        if tipo_de_jogo_escolha == 'I':
            interfaceGame.startGame(galhos, tabuleiro)
        else:
            while True:

                # Para conseguir uma dica, vamos pegar o estado atual e utilizar algum algoritmo, como o A*, para dizer o próximo passo (primeiro movimento do caminho resultado).
                
                dica = input("Se precisar de dica, escreva 'D' e pressione enter. Se não, pressione apenas enter. ")
                if dica == 'D' or dica == 'd':
                    print("\nRProcurando próximo movimento...")
                    a_star = algorithm.Algoritmo()
                    a_star.resolver_com_a_estrela(tabuleiro)
                    caminho = a_star.getCaminho()
                    if caminho:
                        print("Movimento:")
                        print(f"Mover de {caminho[0][0]} para {caminho[0][1]}")
                
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
