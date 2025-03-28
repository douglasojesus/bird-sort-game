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
        self.tempo_algoritmo = float(self.tempo_final - self.tempo_inicio)

    def getEstadosGerados(self):
        return self.estados_gerados
    
    def getTempo(self):
        return self.tempo_algoritmo
    
    def getSolucao(self):
        return self.solucao
    
    def getMemoria(self):
        pass

    def getCaminho(self):
        return self.caminho

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
    
    def calcular_heuristica_liberacao(self, estado):
        """Nova heurística focada em liberação de espaço e mobilidade"""
        pontos = 0
        grupos_prioritarios = []
        
        # Fator de congestionamento por galho
        congestionamento = {galho: 0 for galho in estado}
        
        # 1. Identificar grupos prioritários e calcular congestionamento
        for galho, passaros in estado.items():
            if passaros == 'X' or not passaros:
                continue
                
            # Penalidade por galhos muito cheios (exceto se forem grupos bons)
            if len(passaros) >= 3:
                passaro_mais_comum = max(set(passaros), key=passaros.count)
                qtd = passaros.count(passaro_mais_comum)
                
                if qtd < 3:  # Se estiver cheio mas não formando grupo bom
                    congestionamento[galho] = len(passaros) * 10  # Penalidade alta
                    
            # Bonificação para grupos quase completos
            if len(set(passaros)) == 1 and len(passaros) >= 2:
                pontos -= 50 * len(passaros)  # Grupo uniforme é bom
                
        # 2. Analisar mobilidade dos pássaros no topo
        for galho, passaros in estado.items():
            if passaros == 'X' or not passaros:
                continue
                
            topo = passaros[-1]
            movimentos_possiveis = 0
            
            # Verifica para quantos galhos este pássaro pode voar
            for outro_galho in estado:
                if (outro_galho != galho and estado[outro_galho] != 'X' and 
                    (not estado[outro_galho] or estado[outro_galho][-1] == topo)):
                    movimentos_possiveis += 1
                    
            # Bonificação por pássaros com muitas opções de movimento
            pontos -= 20 * movimentos_possiveis
            
            # Penalidade extra por congestionamento neste galho
            pontos += congestionamento[galho]
            
        # 3. Bonificação especial se algum galho puder ser completado imediatamente
        for galho, passaros in estado.items():
            if passaros == 'X' or len(passaros) != 3:
                continue
                
            if len(set(passaros)) == 1:  # 3 pássaros iguais
                pontos -= 300  # Prioridade máxima para completar
                
        return pontos

    def resolver_com_busca_gulosa(self, tabuleiro):
        """Implementação do algoritmo de busca gulosa com nova heurística"""
        self.inicia()
        fila_prioridade = PriorityQueue()
        contador = itertools.count()
        visitados = set()

        # Adiciona o estado inicial com a nova heurística
        fila_prioridade.put((
            self.heuristica_modular_simples(tabuleiro),
            next(contador),
            tabuleiro,
            []
        ))

        while not fila_prioridade.empty():
            _, _, estado_atual, caminho = fila_prioridade.get()

            if verifica_se_ganhou(estado_atual):
                self.caminho = caminho
                self.finaliza()
                return caminho

            estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
            if estado_tuple in visitados:
                continue
            visitados.add(estado_tuple)

            for origem in estado_atual:
                if not estado_atual[origem] or estado_atual[origem] == 'X':
                    continue

                for destino in estado_atual:
                    if origem == destino or estado_atual[destino] == 'X':
                        continue

                    novo_estado = {k: v.copy() if v != 'X' else 'X' for k, v in estado_atual.items()}
                    
                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        realiza_voo_passaro(novo_estado, origem, destino)
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())

                        if novo_estado_tuple not in visitados:
                            heuristica = self.heuristica_modular_simples(novo_estado)
                            fila_prioridade.put((
                                heuristica,
                                next(contador),
                                novo_estado,
                                caminho + [(origem, destino)]
                            ))

        return None

    def heuristica_prioriza_quase_prontos(self, estado):
        pontos = 0
        grupos_prioritarios = []
        galhos_completos = []
        
        # Primeiro identificamos todos os galhos quase completos (3/4)
        for galho, passaros in estado.items():
            if passaros == 'X' or not passaros:
                continue
            
            passaro_mais_comum = max(set(passaros), key=passaros.count)
            qtd = passaros.count(passaro_mais_comum)
            
            if qtd == 3:
                grupos_prioritarios.append(passaro_mais_comum)
                galhos_completos.append((galho, passaro_mais_comum))

        # Agora analisamos cada galho
        for galho, passaros in estado.items():
            if passaros == 'X' or not passaros:
                continue

            passaro_mais_comum = max(set(passaros), key=passaros.count)
            qtd = passaros.count(passaro_mais_comum)
            topo = passaros[-1] if passaros else None

            # Caso 1: Galho pode ser completado com pássaros de outros galhos
            for gc, passaro_alvo in galhos_completos:
                if gc == galho:
                    continue
                    
                if passaro_alvo in passaros and passaros[-1] != passaro_alvo:
                    # Se o pássaro que completa está neste galho (mesmo bloqueado)
                    # NÃO penalizamos - é justamente o que queremos liberar!
                    pass
                elif passaro_alvo == passaro_mais_comum and qtd >= 2:
                    # Bonificação por galhos que contribuem para completar outros
                    pontos -= 40 * qtd

            # Caso 2: Galho quase completo (3/4)
            if qtd == 3:
                pontos -= 200  # Máxima prioridade (valor negativo = melhor)
                
            # Caso 3: Galho com par no topo que pode virar trio
            elif qtd >= 2 and passaros[-1] == passaros[-2]:
                # Bonificação por pares expostos
                pontos -= 30
                
            # Caso 4: Pássaro bloqueado que NÃO ajuda em nenhum galho prioritário
            elif topo != passaro_mais_comum:
                # Verifica se o pássaro no topo não é útil para completar outros galhos
                if not any(topo == p for _, p in galhos_completos):
                    pontos += 80  # Penaliza somente quando realmente não é útil

        return pontos

    def resolver_com_a_estrela(self, tabuleiro):
        """
        Implementação do algoritmo A* para resolver o problema.
        f(n) = g(n) (custo do caminho) + h(n) (heurística)
        """
        self.inicia()
        fila_prioridade = PriorityQueue()
        contador = itertools.count()  # Para desempate na fila de prioridade
        visitados = set()  # Armazena estados já explorados

        # Adiciona o estado inicial: (f(n), id, estado, caminho, g(n))
        fila_prioridade.put((
            0 + self.heuristica_prioriza_quase_prontos(tabuleiro),
            next(contador),
            tabuleiro,
            [],
            0
        ))

        while not fila_prioridade.empty():
            _, _, estado_atual, caminho, custo_acumulado = fila_prioridade.get()

            # Verifica se é estado objetivo
            if verifica_se_ganhou(estado_atual):
                self.caminho = caminho
                self.finaliza()
                return caminho

            # Converte para tupla para armazenar no conjunto de visitados
            estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
            if estado_tuple in visitados:
                continue
            visitados.add(estado_tuple)

            # Gera todos os movimentos possíveis
            for origem in estado_atual:
                if not estado_atual[origem] or estado_atual[origem] == 'X':
                    continue  # Ignora galhos vazios/quebrados

                passaro = estado_atual[origem][-1]  # Pássaro no topo

                for destino in estado_atual:
                    if origem == destino or estado_atual[destino] == 'X':
                        continue  # Movimento inválido

                    # Cria novo estado
                    novo_estado = {k: v.copy() if v != 'X' else 'X' for k, v in estado_atual.items()}
                    
                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        realiza_voo_passaro(novo_estado, origem, destino)
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())

                        if novo_estado_tuple not in visitados:
                            novo_custo = custo_acumulado + 1
                            prioridade = novo_custo + self.heuristica_prioriza_quase_prontos(novo_estado)
                            fila_prioridade.put((
                                prioridade,
                                next(contador),
                                novo_estado,
                                caminho + [(origem, destino)],
                                novo_custo
                            ))

        return None  
    
    def heuristica_modular_simples(self, estado):
        """Heurística modular básica e pouco eficiente"""
        pontos = 0
        
        # 1. Contagem básica de pássaros
        total_passaros = sum(len(p) for p in estado.values() if p != 'X')
        
        # 2. Fator de dispersão (quanto mais dispersos, pior)
        tipos_por_galho = []
        for galho, passaros in estado.items():
            if passaros == 'X':
                continue
            tipos_por_galho.append(len(set(passaros)))
        
        fator_dispersao = sum(tipos_por_galho)
        
        # 3. Galhos vazios (considerados bons)
        galhos_vazios = sum(1 for p in estado.values() if p != 'X' and not p)
        
        # 4. Cálculo simples (quanto menor, melhor)
        pontos = total_passaros + fator_dispersao - galhos_vazios
        
        return pontos

    def resolver_com_a_estrela_ponderado(self, tabuleiro, peso_heuristica=1.5):
        """
        Implementação do algoritmo A* ponderado para resolver o problema.
        f(n) = g(n) + w * h(n), onde w é o peso da heurística
        
        Args:
            tabuleiro: estado inicial do tabuleiro
            peso_heuristica: peso dado ao componente heurístico (default=1.5)
        """
        self.inicia()
        fila_prioridade = PriorityQueue()
        contador = itertools.count()  # Para desempate na fila de prioridade
        visitados = set()  # Armazena estados já explorados

        # Adiciona o estado inicial: (f(n), id, estado, caminho, g(n))
        fila_prioridade.put((
            0 + peso_heuristica * self.heuristica_modular_simples(tabuleiro),
            next(contador),
            tabuleiro,
            [],
            0
        ))

        while not fila_prioridade.empty():
            _, _, estado_atual, caminho, custo_acumulado = fila_prioridade.get()

            # Verifica se é estado objetivo
            if verifica_se_ganhou(estado_atual):
                self.caminho = caminho
                self.finaliza()
                return caminho

            # Converte para tupla para armazenar no conjunto de visitados
            estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in estado_atual.items())
            if estado_tuple in visitados:
                continue
            visitados.add(estado_tuple)

            # Gera todos os movimentos possíveis
            for origem in estado_atual:
                if not estado_atual[origem] or estado_atual[origem] == 'X':
                    continue  # Ignora galhos vazios/quebrados

                passaro = estado_atual[origem][-1]  # Pássaro no topo

                for destino in estado_atual:
                    if origem == destino or estado_atual[destino] == 'X':
                        continue  # Movimento inválido

                    # Cria novo estado
                    novo_estado = {k: v.copy() if v != 'X' else 'X' for k, v in estado_atual.items()}
                    
                    if verifica_se_pode_voar(novo_estado, origem, destino):
                        realiza_voo_passaro(novo_estado, origem, destino)
                        novo_estado_tuple = tuple((k, tuple(v) if v != 'X' else 'X') for k, v in novo_estado.items())

                        if novo_estado_tuple not in visitados:
                            novo_custo = custo_acumulado + 1
                            prioridade = novo_custo + peso_heuristica * self.heuristica_modular_simples(novo_estado)
                            fila_prioridade.put((
                                prioridade,
                                next(contador),
                                novo_estado,
                                caminho + [(origem, destino)],
                                novo_custo
                            ))

        return None

    def exibe(self):
        if self.caminho:
            print(f"Solução encontrada em {len(self.caminho)} movimentos!")
            print(f"Solução encontrada em {self.tempo_algoritmo:.4} segundos.")
            print("Sequência de movimentos:")
            for movimento in self.caminho:
                print(f"Mover de {movimento[0]} para {movimento[1]}")
        else:
            print("Não foi possível encontrar uma solução.")
        return self.tempo_algoritmo, len(self.caminho)
        
    def consegue_dica(self, tabuleiro):
        """Retorna uma dica (movimento sugerido)"""
        caminho = self.resolver_com_a_estrela(tabuleiro)

        if caminho and len(caminho) > 0:
            self.caminho = caminho
            return f"Mover de {caminho[0][0]} para {caminho[0][1]}"
        return None