
import random

def exibe_tabuleiro(tabuleiro):
    for galho in tabuleiro:
        print(galho, '-', tabuleiro[galho])

def define_tabuleiro_manualmente(qntd_galhos):
    print("""Instruções: 
- Adicione até 4 pássaros por galho;
- Insira, exatamente, 4 pássaros do mesmo tipo no conjunto de galhos;""")
    
    tabuleiro = {}
    is_valid = {}  # Dicionário para contar a quantidade de cada tipo de pássaro
    tipos_passaros = set()  # Conjunto para armazenar os tipos de pássaros inseridos

    for i in range(qntd_galhos):
        while True:
            galho = input(f"Adicione, entre vírgulas, os pássaros no Galho {i+1} (ex: 1, 1, 2, 1): ")
            try:
                galho = [int(passaro) for passaro in galho.split(",")]
                
                if len(galho) > 4:
                    print("Erro: Um galho não pode ter mais de 4 pássaros. Tente novamente.")
                    continue
                
                for passaro in galho:
                    if passaro in is_valid:
                        is_valid[passaro] += 1
                    else:
                        is_valid[passaro] = 1
                    tipos_passaros.add(passaro)
                
                tabuleiro[f"Galho {i+1}"] = galho
                break
            except ValueError:
                print("Erro: Insira apenas números separados por vírgulas. Tente novamente.")
    
    # Verifica se há exatamente 4 pássaros de cada tipo
    for passaro in tipos_passaros:
        if is_valid.get(passaro, 0) != 4:
            print(f"Erro: O tipo de pássaro {passaro} não tem exatamente 4 pássaros. Reinicie o processo.")
            return None

    tabuleiro[f"Galho {qntd_galhos + 1}"] = []
    tabuleiro[f"Galho {qntd_galhos + 2}"] = []

    print("\nTabuleiro criado com sucesso:")
    return tabuleiro





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
    # Verifica se o galho de origem não está quebrado ('X') e se o galho de destino não está quebrado
    if tabuleiro[origem] != 'X' and tabuleiro[destino] != 'X':
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

