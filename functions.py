
import random

def exibe_tabuleiro(tabuleiro):
    for galho in tabuleiro:
        print(galho, '-', tabuleiro[galho])

def define_tabuleiro(qntd_galhos, tam_pilha):
    # define tabuleiro inicial, com as pilhas dos pássaros e os galhos
    tabuleiro = {}
    aux = 0
    for i in range(qntd_galhos+1):
        tabuleiro['Galho '+str(i+1)] = []
        aux = i+1
    tabuleiro['Galho '+str(aux)] = []
    tabuleiro['Galho '+str(aux+1)] = []

    return tabuleiro

def popula_tabuleiro(tabuleiro):
    passaros = [x+1 for x in range(len(tabuleiro)-2)] # -2 são os galhos extras
    passaros_total_nos_galhos = {}
    vezes_de_populacao = 0 # quando chegar a len(tabuleiro) - 2, sai do for galho in tabuleiro
    
    for passaro in passaros:
        passaros_total_nos_galhos[passaro] = 0

    for galho in tabuleiro: 
        for i in range(4):
            passaro_escolhido = random.choice(passaros)

            while passaros_total_nos_galhos[passaro_escolhido] >= 4:
                passaro_escolhido = random.choice(passaros)
            
            if len(tabuleiro[galho]) < 4:
                tabuleiro[galho].append(passaro_escolhido)
                passaros_total_nos_galhos[passaro_escolhido] += 1
            
        vezes_de_populacao += 1

        if vezes_de_populacao == (len(tabuleiro) - 2):
            break

    return tabuleiro

def verifica_se_ganhou(tabuleiro):
    qntd = 0
    for galho in tabuleiro:
        if tabuleiro[galho] != 'X':
            qntd += 1
    if qntd == 2:
        return True
    return False

def verifica_se_pode_voar(tabuleiro, origem, destino): # origem e destino devem se parecer como 'Galho 1'
    if tabuleiro[origem] and tabuleiro[destino]:
        if (tabuleiro[origem][-1] == tabuleiro[destino][-1]) and len(tabuleiro[destino]) < 4:
            return True
    elif tabuleiro[origem]:
        return True
    return False

def realiza_voo_passaro(tabuleiro, origem, destino):
    if verifica_se_pode_voar(tabuleiro, origem, destino):
        tabuleiro[destino].append(tabuleiro[origem][-1])
        tabuleiro[origem].pop()
        verifica_se_pilha_esta_completa(tabuleiro)
        return tabuleiro
    return False

def verifica_se_sao_todos_iguais(galho):
    qntd = 0
    if galho:
        passaro_1 = galho[0]
    else:
        return False
    for passaro in galho:
        if passaro == passaro_1:
            qntd += 1
    if qntd == 4:
        return True
    return False

def verifica_se_pilha_esta_completa(tabuleiro):
    galhos_completos = []
    for galho in tabuleiro:
        if verifica_se_sao_todos_iguais(tabuleiro[galho]):
            tabuleiro = quebra_galho(tabuleiro, galho)
            galhos_completos.append(galho)
    return galhos_completos

def quebra_galho(tabuleiro, galho):
    tabuleiro[galho] = 'X'
    return tabuleiro

