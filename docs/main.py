import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Criar o diretório splot caso não exista
output_dir = "splot"
os.makedirs(output_dir, exist_ok=True)

print("Abrindo os resultados...")
with open('../results/results.json', 'r') as f:
    data = json.load(f)

print("Transformando JSON em DataFrame...")
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

sns.set(style="whitegrid")

print("Gerando gráfico de dispersão de estados gerados vs caminhos...")
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
plt.savefig(os.path.join(output_dir, "dispersao_estados_vs_caminhos.png"))
plt.close()

print("Gerando gráfico de dispersão de tempo vs estados gerados...")
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df,
    x="tempo_de_execucao",
    y="quantidade_de_estados_gerados",
    hue="algoritmo",
    palette="Set2",
    alpha=0.7
)
scatter.set_title("Eficiência: Tempo vs Estados Gerados")
scatter.set_xlabel("Tempo de Execução (s)")
scatter.set_ylabel("Quantidade de Estados Gerados")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "eficiencia_tempo_estados.png"))
plt.close()

print("Gerando gráfico de boxplot da distribuição de tempo de execução...")
# Analisa a distribuição do tempo de execução para cada algoritmo, ajudando a identificar variações e outliers.
plt.figure(figsize=(10, 6))
box = sns.boxplot(
    data=df,
    x="algoritmo",
    y="tempo_de_execucao",
    palette="pastel"
)
box.set_title("Distribuição do Tempo de Execução por Algoritmo")
box.set_xlabel("Algoritmo")
box.set_ylabel("Tempo de Execução (s)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "boxplot_tempo_execucao.png"))
plt.close()

print("Gerando gráfico de Heatmap de Correlação entre Variáveis")
# Se há alguma relação forte entre os parâmetros como tempo de execução, estados gerados e quantidade de caminhos.
plt.figure(figsize=(8, 6))
corr_matrix = df[["tempo_de_execucao", "quantidade_de_estados_gerados", "quantidade_de_caminhos"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlação entre Variáveis")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "heatmap_correlacao.png"))
plt.close()

# Criar gráfico comparando heurísticas no tempo de execução
plt.figure(figsize=(10, 6))
bar = sns.barplot(
    data=df[df["algoritmo"].isin(["a_star", "greedy", "a_star_p"])],  # Filtra heurísticas específicas
    x="algoritmo",
    y="tempo_de_execucao",
    estimator="mean",
    ci="sd",
    palette="coolwarm"
)

# Adicionando valores no topo das barras
for p in bar.patches:
    bar.annotate(f'{p.get_height():.3f}',
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                  ha='center', va='bottom', fontsize=10, fontweight='bold')

bar.set_title("Comparação de Algoritmos com Heurísticas no Tempo de Execução")
bar.set_xlabel("Heurística")
bar.set_ylabel("Tempo Médio (s)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "comparacao_heuristicas.png"))
plt.close()

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

# Adicionando valores no topo das barras
for p in bar1.patches:
    bar1.annotate(f'{p.get_height():.3f}',
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                  ha='center', va='bottom', fontsize=10, fontweight='bold')

bar1.set_title("Tempo Médio de Execução por Algoritmo")
bar1.set_ylabel("Tempo Médio (s)")
bar1.set_xlabel("Algoritmo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "tempo_medio_execucao.png"))
plt.close()

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

# Adicionando valores no topo das barras
for p in bar2.patches:
    bar2.annotate(f'{p.get_height():.1f}',
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                  ha='center', va='bottom', fontsize=10, fontweight='bold')

bar2.set_title("Quantidade Média de Caminhos por Algoritmo")
bar2.set_ylabel("Média de Caminhos")
bar2.set_xlabel("Algoritmo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "caminhos_medios_por_algoritmo.png"))
plt.close()

print("Gráficos salvos no diretório 'splot'.")
