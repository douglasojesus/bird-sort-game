import time
from collections import deque
from src.functions import *
from queue import PriorityQueue
import itertools

# possíveis heurísticas
# estimar quantidade de movimentos para um galho estar completo (se precisa ter 4 em um galho, e tem 3, falta só 1 para completar)
# 

class Algoritmo:
    def __init__(self):
        self.tempo_inicio = 0
        self.tempo_final = 0
        self.tempo_algoritmo = 0
        self.memoria = 0
        self.estados_gerados = 0
        self.solucao = ''
        self.caminho = ''

    def inicia(self):
        self.tempo_inicio = time.time()

    def finaliza(self):
        self.tempo_final = time.time()
        self.tempo_algoritmo = self.tempo_final - self.tempo_inicio

    def getEstadosGerados(self):
        return self.estados_gerados
    
    def getTempo(self):
        return self.tempo_algoritmo
    
    def getSolucao(self):
        return self.solucao
    
    def getMemoria(self):
        pass

    def resolver_com_bfs(self, tabuleiro):
        self.inicia()
        fila = deque()  # Fila para armazenar os estados a serem explorados
        fila.append((tabuleiro, []))  # Adiciona o estado inicial e o caminho vazio
        visitados = set()  # Conjunto para armazenar estados já visitados

        while fila:
            estado_atual, caminho = fila.popleft()  # Remove o primeiro estado da fila

            if verifica_se_ganhou(estado_atual):  # Verifica se é o estado objetivo
                self.caminho = caminho
                self.finaliza()
                return caminho  # Retorna o caminho para a solução

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

    def resolver_com_dfs(self, tabuleiro, profundidade_maxima=None):
        self.inicia()
        pilha = deque()  # Pilha para armazenar os estados a serem explorados
        pilha.append((tabuleiro, [], 0))  # Adiciona o estado inicial, o caminho vazio e a profundidade atual
        visitados = set()  # Conjunto para armazenar estados já visitados

        while pilha:
            estado_atual, caminho, profundidade = pilha.pop()  # Remove o último estado da pilha (LIFO)

            if verifica_se_ganhou(estado_atual):  # Verifica se é o estado objetivo
                self.caminho = caminho
                self.finaliza()
                return caminho  # Retorna o caminho para a solução

            # Se a profundidade máxima for definida e atingida, ignora este nó
            if profundidade_maxima is not None and profundidade >= profundidade_maxima:
                continue

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
                                pilha.append((novo_estado, caminho + [(origem, destino)], profundidade + 1))  # Adiciona o sucessor à pilha

        return None  # Retorna None se não encontrar solução

    def resolver_com_interatividade(self, tabuleiro):
        self.inicia()
        profundidade_maxima = 0  # Começa com profundidade 0 e aumenta iterativamente

        while True:
            resultado = self.resolver_com_dfs(tabuleiro, profundidade_maxima)
            if resultado is not None:  # Se uma solução for encontrada
                self.caminho = resultado
                self.finaliza()
                return resultado
            profundidade_maxima += 1  # Aumenta a profundidade máxima

    def resolver_com_custo_uniforme(self, tabuleiro):
        self.inicia()
        fila_prioridade = PriorityQueue()
        contador = itertools.count()
        fila_prioridade.put((0, next(contador), tabuleiro, []))
        visitados = set()

        while not fila_prioridade.empty():
            custo_acumulado, _, estado_atual, caminho = fila_prioridade.get()

            if verifica_se_ganhou(estado_atual):
                self.caminho = caminho
                self.finaliza()
                return caminho

            estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
            visitados.add(estado_tuple)

            for origem in estado_atual:
                if not estado_atual[origem] or estado_atual[origem] == 'X':
                    continue

                passaro = estado_atual[origem][-1]

                for destino in estado_atual:
                    if origem == destino or estado_atual[destino] == 'X':
                        continue

                    novo_estado = {k: v.copy() if v != 'X' else 'X' for k, v in estado_atual.items()}
                    
                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        # Hierarquia de prioridades
                        if estado_atual[destino] and estado_atual[destino][-1] == passaro:
                            qtd_iguais = estado_atual[destino].count(passaro)
                            if qtd_iguais >= 2:
                                custo_movimento = 0.001  # Prioridade absoluta para completar grupos
                            else:
                                custo_movimento = 0.1    # Prioridade alta para iniciar grupos
                        elif not estado_atual[destino]:
                            custo_movimento = 0.5        # Prioridade média para galhos vazios
                        else:
                            custo_movimento = 10.0       # Penalidade alta para movimentos não estratégicos

                        realiza_voo_passaro(novo_estado, origem, destino)
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())
                        
                        if novo_estado_tuple not in visitados:
                            fila_prioridade.put((
                                custo_acumulado + custo_movimento,
                                next(contador),
                                novo_estado,
                                caminho + [(origem, destino)]
                            ))

        return None

    def resolver_com_busca_gulosa(self, tabuleiro):
        pass

    def resolver_com_a_estrela(self, tabuleiro):
        pass

    def resolver_com_a_estrela_ponderado(self, tabuleiro):
        pass

    def exibe(self):
        if self.caminho:
            print(f"Solução encontrada em {len(self.caminho)} movimentos!")
            print(f"Solução encontrada em {self.tempo_algoritmo:.4} segundos.")
            print("Sequência de movimentos:")
            for movimento in self.caminho:
                print(f"Mover de {movimento[0]} para {movimento[1]}")
        else:
            print("Não foi possível encontrar uma solução.")