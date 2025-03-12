from collections import deque
from functions import *
import time

'''
um estado é uma configuração específica do tabuleiro em um determinado momento
cada nó do grafo representa um estado do jogo (ou seja, uma configuração específica do tabuleiro).
cada aresta representa um movimento válido que leva de um estado para outro.

'''

def resolver_com_bfs(tabuleiro):
    inicio = time.time()
    fila = deque()  # Fila para armazenar os estados a serem explorados
    fila.append((tabuleiro, []))  # Adiciona o estado inicial e o caminho vazio
    visitados = set()  # Conjunto para armazenar estados já visitados

    while fila:
        estado_atual, caminho = fila.popleft()  # Remove o primeiro estado da fila

        if verifica_se_ganhou(estado_atual):  # Verifica se é o estado objetivo
            final = time.time()
            tempo_decorrido = final - inicio
            return caminho, tempo_decorrido  # Retorna o caminho para a solução

        # Marca o estado como visitado
        estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
        visitados.add(estado_tuple)

        # Gera todos os movimentos possíveis
        for origem in estado_atual:
            for destino in estado_atual:
                if origem != destino and estado_atual[origem] and estado_atual[destino] != 'X':
                    # Cria uma cópia do estado atual, tratando galhos quebrados ('X')
                    novo_estado = {}
                    for k, v in estado_atual.items():
                        if v == 'X':
                            novo_estado[k] = 'X'
                        else:
                            novo_estado[k] = v.copy()

                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        realiza_voo_passaro(novo_estado, origem, destino)
                        # Verifica se o novo estado já foi visitado
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())
                        if novo_estado_tuple not in visitados:
                            fila.append((novo_estado, caminho + [(origem, destino)]))  # Adiciona o sucessor à fila

    return None  # Retorna None se não encontrar solução

def resolver_com_dfs(tabuleiro):
    inicio = time.time()
    pilha = deque()  # Pilha para armazenar os estados a serem explorados
    pilha.append((tabuleiro, []))  # Adiciona o estado inicial e o caminho vazio
    visitados = set()  # Conjunto para armazenar estados já visitados

    while pilha:
        estado_atual, caminho = pilha.pop()  # Remove o último estado da pilha (LIFO)

        if verifica_se_ganhou(estado_atual):  # Verifica se é o estado objetivo
            final = time.time()
            tempo_decorrido = final - inicio
            return caminho, tempo_decorrido  # Retorna o caminho para a solução

        # Marca o estado como visitado
        estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
        visitados.add(estado_tuple)

        # Gera todos os movimentos possíveis
        for origem in estado_atual:
            for destino in estado_atual:
                if origem != destino and estado_atual[origem] and estado_atual[destino] != 'X':
                    # Cria uma cópia do estado atual, tratando galhos quebrados ('X')
                    novo_estado = {}
                    for k, v in estado_atual.items():
                        if v == 'X':
                            novo_estado[k] = 'X'
                        else:
                            novo_estado[k] = v.copy()

                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        realiza_voo_passaro(novo_estado, origem, destino)
                        # Verifica se o novo estado já foi visitado
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())
                        if novo_estado_tuple not in visitados:
                            pilha.append((novo_estado, caminho + [(origem, destino)]))  # Adiciona o sucessor à pilha

    return None  # Retorna None se não encontrar solução