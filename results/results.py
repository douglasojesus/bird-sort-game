import json
import os
from collections import defaultdict

def registrar_execucao(nome_algoritmo, tempo_execucao, qtd_caminhos):
    """
    Registra uma execução no arquivo results.json
    
    Args:
        nome_algoritmo (str): Nome do algoritmo (a_star, ucs, dfsi, bfs, dfs)
        tempo_execucao (float): Tempo de execução em segundos
        qtd_caminhos (int): Quantidade de caminhos/movimentos da solução
    """
    # Dados da nova execução
    nova_execucao = {
        'tempo_de_execucao': tempo_execucao,
        'quantidade_de_caminhos': qtd_caminhos
    }

    # Carrega os dados existentes ou cria estrutura vazia
    try:
        with open('results.json', 'r') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {
            'a_star': [], 'ucs': [], 'dfsi': [], 'bfs': [], 'dfs': []
        }

    # Adiciona a nova execução
    if nome_algoritmo in dados:
        numero_execucao = len(dados[nome_algoritmo]) + 1
        dados[nome_algoritmo].append({
            'numero_da_execucao': numero_execucao,
            **nova_execucao
        })
    else:
        dados[nome_algoritmo] = [{
            'numero_da_execucao': 1,
            **nova_execucao
        }]

    # Salva no arquivo
    with open('results.json', 'w') as f:
        json.dump(dados, f, indent=4)

def exibir_resultados_comparativos():
    """
    Exibe todos os resultados registrados de forma comparativa e organizada
    """
    try:
        with open('results.json', 'r') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Nenhum dado de execução registrado ainda.")
        return

    # Organiza os dados para exibição comparativa
    tabela = []
    for algoritmo, execucoes in dados.items():
        for execucao in execucoes:
            tabela.append((
                execucao['numero_da_execucao'],
                algoritmo,
                execucao['tempo_de_execucao'],
                execucao['quantidade_de_caminhos']
            ))

    # Ordena por número de execução e depois por algoritmo
    tabela.sort(key=lambda x: (x[0], x[1]))

    # Exibe os resultados formatados
    print("\n=== RESULTADOS COMPARATIVOS ===")
    print(f"{'Exec.':<6} | {'Algoritmo':<8} | {'Tempo (s)':<10} | {'Caminhos':<8}")
    print("-" * 45)
    
    for execucao in tabela:
        print(f"{execucao[0]:<6} | {execucao[1]:<8} | {execucao[2]:<10.4f} | {execucao[3]:<8}")