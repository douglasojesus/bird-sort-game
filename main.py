from functions import *

def main():
    galhos = int(input('Número de galhos: '))
    tabuleiro = define_tabuleiro(galhos, 0)
    tabuleiro = popula_tabuleiro(tabuleiro)

    exibe_tabuleiro(tabuleiro)

    galhos_completos = verifica_se_pilha_esta_completa(tabuleiro)

    possiveis_escolhas_origem_destino = {}
    for i in range(galhos+2):
        possiveis_escolhas_origem_destino[i+1] = 'Galho '+str(i+1)

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