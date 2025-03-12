import time

class Algoritmo:
    def __init__(self):
        self.tempo_inicio = 0
        self.tempo_final = 0
        self.tempo_algoritmo = 0
        self.memoria = 0
        self.estados_gerados = ''
        self.solucao = ''

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

    def resolver_com_bfs(tabuleiro):
        pass

    def resolver_com_dfs(tabuleiro):
        pass

    def resolver_com_interatividade(tabuleiro):
        pass

    def resolver_com_custo_uniforme(tabuleiro):
        pass

    def resolver_com_busca_gulosa(tabuleiro):
        pass

    def resolver_com_a_estrela(tabuleiro):
        pass

    def resolver_com_a_estrela_ponderado(tabuleiro):
        pass

    def __str__(self):
        pass
        


