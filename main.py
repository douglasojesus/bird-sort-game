from src.functions import *
from src.algorithm import *
from src.interface import BirdSortGame
from results.results import *

def main():
    
    galhos = int(input('Número de galhos (maior que 1 e menor que 9): '))
    while galhos <= 1 or galhos >= 9:
        galhos = int(input('Número de galhos (maior que 1 e menor que 9): '))

    escolha = input("Se você quer usar um tabuleiro aleatório pressione 'A', se quer adicionar um tabuleiro manualmente, adicione 'M': ").strip().upper()
    while escolha != 'M' and escolha != 'A':
        escolha = input("Se você quer usar um tabuleiro aleatório pressione 'A', se quer adicionar um tabuleiro manualmente, adicione 'M': ").strip().upper()    

    if escolha == 'M':
        tabuleiro = define_tabuleiro_manualmente(galhos+2)
        while tabuleiro == None:
            tabuleiro = define_tabuleiro_manualmente(galhos+2)
    else:
        tabuleiro = define_tabuleiro(galhos)
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

        print("\nResolvendo o jogo com BFS...")
        bfs = Algoritmo()
        bfs.resolver_com_bfs(tabuleiro)
        tempo, qntd_caminhos = bfs.exibe()

        print("\nResolvendo o jogo com Busca Gulosa...")
        greedy = Algoritmo()
        greedy.resolver_com_busca_gulosa(tabuleiro)
        tempo, qntd_caminhos = greedy.exibe()

        print("\nResolvendo o jogo com A estrela Ponderada...")
        a_star_p = Algoritmo()
        a_star_p.resolver_com_a_estrela_ponderado(tabuleiro)
        tempo, qntd_caminhos = a_star_p.exibe()

        """print("\nResolvendo o jogo com A*...")
        a_star = Algoritmo()
        a_star.resolver_com_a_estrela(tabuleiro)
        tempo, qntd_caminhos = a_star.exibe()

        registrar_execucao('a_star', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com Custo Uniforme...")
        ucs = Algoritmo()
        ucs.resolver_com_custo_uniforme(tabuleiro)
        tempo, qntd_caminhos = ucs.exibe()

        registrar_execucao('ucs', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com DFS...")
        dfs = Algoritmo()
        dfs.resolver_com_dfs(tabuleiro)
        tempo, qntd_caminhos = dfs.exibe()

        registrar_execucao('dfs', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com DFS Iterarivo...")
        dfsi = Algoritmo()
        dfsi.resolver_com_interatividade(tabuleiro)
        tempo, qntd_caminhos = dfsi.exibe()

        registrar_execucao('dfsi', tempo, qntd_caminhos)

        print("\nResolvendo o jogo com BFS...")
        bfs = Algoritmo()
        bfs.resolver_com_bfs(tabuleiro)
        tempo, qntd_caminhos = bfs.exibe()

        registrar_execucao('bfs', tempo, qntd_caminhos)

        exibir_resultados_comparativos()"""
    
    else:
        tipo_de_jogo_escolha = input("Você quer jogar no console (C) ou na interface gráfica (I)? ").strip().upper()
        while tipo_de_jogo_escolha != 'C' and tipo_de_jogo_escolha != 'I':
            tipo_de_jogo_escolha = input("Escolha 'C' (console) ou 'I' (interface): ").strip().upper()

        if tipo_de_jogo_escolha == 'I':
            game = BirdSortGame(tabuleiro)
            game.run()
        else:
            while True:
                # Para conseguir uma dica, vamos pegar o estado atual e utilizar algum algoritmo, como o A*, para dizer o próximo passo (primeiro movimento do caminho resultado).
                
                escolha_dica = input("Se precisar de dica, escreva 'D' e pressione enter. Se não, pressione apenas enter. ")
                if escolha_dica == 'D' or escolha_dica == 'd':
                    print("\nProcurando próximo movimento...")
                    algoritmo = Algoritmo()
                    dica = algoritmo.consegue_dica(tabuleiro=tabuleiro)
                    print("Movimento:")
                    print(dica)
                    
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
