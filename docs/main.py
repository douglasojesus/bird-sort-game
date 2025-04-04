import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Abrindo os resultados...")
# Carregue seu JSON aqui (como string ou arquivo)
with open('../results/results.json', 'r') as f:
    data = json.load(f)

print("Transformando JSON em DataFrame...")
# Transforma o JSON em DataFrame
df_list = []

for algoritmo, resultados in data.items():
    for resultado in resultados:
        df_list.append({
            "algoritmo": algoritmo,
            "execucao": resultado["numero_da_execucao"],
            "tempo_de_execucao": resultado["tempo_de_execucao"],
            "quantidade_de_caminhos": resultado["quantidade_de_caminhos"],
            "quantidade_de_estados_gerados": resultado["quantidade_de_estados_gerados"]
        })

df = pd.DataFrame(df_list)

# Estilo do seaborn
sns.set(style="whitegrid")

print("Gerando gráfico de dispersão...")
# === Gráfico de Dispersão ===
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df,
    x="quantidade_de_estados_gerados",
    y="quantidade_de_caminhos",
    hue="algoritmo",
    palette="Set2",
    alpha=0.7
)
scatter.set_title("Dispersão: Estados Gerados vs Caminhos")
scatter.set_xlabel("Quantidade de Estados Gerados")
scatter.set_ylabel("Quantidade de Caminhos")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("Gerando gráfico de barras do tempo médio de execução...")
# === Gráfico de Barras: Tempo Médio de Execução ===
plt.figure(figsize=(10, 6))
bar1 = sns.barplot(
    data=df,
    x="algoritmo",
    y="tempo_de_execucao",
    estimator="mean",
    ci="sd",
    palette="Set3"
)
bar1.set_title("Tempo Médio de Execução por Algoritmo")
bar1.set_ylabel("Tempo Médio (s)")
bar1.set_xlabel("Algoritmo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Gerando gráfico de barras de caminhos médios por algoritmo...")
# === Gráfico de Barras: Caminhos Médios por Algoritmo ===
plt.figure(figsize=(10, 6))
bar2 = sns.barplot(
    data=df,
    x="algoritmo",
    y="quantidade_de_caminhos",
    estimator="mean",
    ci="sd",
    palette="Set1"
)
bar2.set_title("Quantidade Média de Caminhos por Algoritmo")
bar2.set_ylabel("Média de Caminhos")
bar2.set_xlabel("Algoritmo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
