# Métodos de Busca Heurística para Jogos de Solitário de Um Jogador

### Projeto a ser desenvolvido para a unidade curricular de Inteligência Artificial da FEUP.

**Jogo de inspiração escolhido: Bird Sort.**

**Algoritmos a serem implementados: sem conhecimento (busca em largura, busca em profundidade, aprofundamento iterativo, custo uniforme) e com heurística (busca gulosa, algoritmo A*, A* Ponderado).

# Explicação dos Algoritmos de Busca para o Bird Sort

## Visão Geral
A classe `Algoritmo` implementa sete métodos de busca para resolver o jogo tipo Bird Sort:
1. **BFS (Busca em Largura)**
2. **DFS (Busca em Profundidade)**
3. **Busca em Profundidade Iterativa**
4. **Busca de Custo Uniforme (UCS)**
5. **A*** - Busca informada ótima
6. **A* Ponderado** - Versão balanceada do A*
7. **Busca Gulosa** - Busca puramente heurística

Cada algoritmo tem características distintas na forma de explorar o espaço de estados do jogo.

## 1. BFS (Busca em Largura)

### Funcionamento
- Utiliza uma **fila (FIFO)** para explorar todos os nós de um nível antes de avançar para o próximo
- Explora o tabuleiro em camadas de profundidade crescente
- Garante encontrar a solução com menor número de movimentos (ótima para custos uniformes)

### Características
- **Completo**: Sempre encontra solução se existir
- **Ótimo**: Para problemas com custo constante por movimento
- **Complexidade**: O(b^d) em espaço e tempo (b = fator de ramificação, d = profundidade da solução)

### Aplicação
- Ideal quando todos os movimentos têm igual importância
- Gera a solução com menos movimentos totais

## 2. DFS (Busca em Profundidade)

### Funcionamento
- Utiliza uma **pilha (LIFO)** para explorar um ramo até o fim antes de retroceder
- Pode ser limitado por profundidade máxima
- Não garante solução ótima (pode encontrar caminhos mais longos primeiro)

### Características
- **Não completo**: Pode entrar em loops infinitos em espaços ilimitados
- **Não ótimo**: Pode encontrar soluções subótimas
- **Complexidade**: O(bm) em espaço (b = fator de ramificação, m = profundidade máxima)

### Aplicação 
- Útil quando a solução está em ramos profundos
- Requer menos memória que BFS para espaços grandes

## 3. Busca em Profundidade Iterativa

### Funcionamento
- Combina BFS e DFS executando DFS com limites de profundidade crescente
- Reinicia a busca incrementando o limite até encontrar a solução
- Mantém as vantagens de ambos: completude do BFS e eficiência em espaço do DFS

### Características
- **Completo**: Como BFS
- **Ótimo**: Para custo uniforme
- **Complexidade**: O(b^d) tempo, O(bd) espaço

### Aplicação
- Boa alternativa quando não se sabe a profundidade da solução
- Equilíbrio entre desempenho e consumo de memória

## 4. Busca de Custo Uniforme (UCS)

### Funcionamento
- Versão generalizada do BFS que considera custos variáveis por movimento
- Utiliza **fila de prioridade** para expandir sempre o nó com menor custo acumulado
- Implementa critérios estratégicos específicos para o Bird Sort

### Critérios de Custo
1. **Prioridade Máxima (0.001)**: Completar grupos de 4 pássaros iguais
2. **Alta Prioridade (0.1)**: Formar grupos de 3 pássaros iguais
3. **Prioridade Média (0.5)**: Movimentos para galhos vazios
4. **Penalidade (10.0)**: Movimentos não estratégicos

### Características
- **Completo** e **Ótimo**: Encontra a solução de menor custo total
- **Complexidade**: O(b^(1+C/ε)) onde C é o custo da solução ótima

### Aplicação
- Produz soluções mais inteligentes que BFS/DFS
- Prioriza formação de grupos completos de pássaros
- Adequado quando diferentes movimentos têm importância estratégica distinta

## 5. Algoritmo A*

### Funcionamento
- Combina custo real do caminho (g(n)) com estimativa heurística (h(n))
- Utiliza **fila de prioridade** ordenada por f(n) = g(n) + h(n)
- Implementa heurística especializada para formação de grupos de pássaros

### Heurística Utilizada (`heuristica_prioriza_quase_prontos`)
1. **Prioridade Máxima (-200)**: Galhos com 3/4 pássaros iguais (quase completos)
2. **Alta Prioridade (-30)**: Pares de pássaros expostos no topo
3. **Bonificação (-40/qtd)**: Galhos que contribuem para completar outros grupos
4. **Penalização (+80)**: Pássaros bloqueados que não ajudam em outros grupos

### Características
- **Completo** e **Ótimo**: Garante solução com menor custo total (se heurística for admissível)
- **Complexidade**: O(b^d) - Exponencial na profundidade da solução
- **Eficiência**: Mais rápido que UCS em problemas complexos

### Aplicação
- Solução ideal para configurações complexas do jogo
- Quando se necessita da solução com menor número de movimentos
- Problemas onde a heurística pode fornecer boa orientação

## 6. A* Ponderado (Weighted A*)

### Funcionamento
- Versão parametrizada do A* com peso na heurística
- Utiliza fórmula f(n) = g(n) + w × h(n) (w > 1)
- Implementa heurística modular simples para avaliação rápida

### Heurística Simplificada (`heuristica_modular_simples`)
1. **Contagem de Pássaros**: Total de pássaros no tabuleiro
2. **Fator de Dispersão**: Soma de tipos diferentes por galho
3. **Galhos Vazios**: Bonificação por espaços livres

### Características
- **Completo**: Garante encontrar solução se existir
- **Subótimo**: Encontra soluções mais rápidas (mas não necessariamente ótimas)
- **Ajustável**: Peso (w) controla balanceamento entre custo e heurística

### Aplicação
- Quando se busca soluções rápidas com qualidade razoável
- Problemas grandes onde A* tradicional é muito lento
- Como alternativa à busca gulosa quando se quer algum controle de qualidade

## 7. Busca Gulosa (Greedy Best-First)

### Funcionamento
- Considera apenas o valor heurístico (ignora custo do caminho)
- Utiliza **fila de prioridade** ordenada apenas por h(n)
- Implementa mesma heurística de liberação

### Características
- **Não Completo**: Pode falhar em encontrar solução existente
- **Não Ótimo**: Encontra soluções de qualidade variável
- **Eficiência**: Extremamente rápido em problemas simples

### Aplicação
- Análise inicial de problemas simples
- Quando velocidade é mais importante que qualidade da solução
- Como linha de base para comparação com outros algoritmos

## Comparação entre os Algoritmos

| Algoritmo       | Completo | Ótimo | Complexidade Espaço | Complexidade Tempo | Melhor Caso |
|-----------------|----------|-------|---------------------|-------------------|-------------|
| BFS            | Sim      | Sim*  | O(b^d)              | O(b^d)            | Poucos movimentos |
| DFS            | Não      | Não   | O(bm)               | O(b^m)            | Solução profunda |
| IDDFS          | Sim      | Sim*  | O(bd)               | O(b^d)            | Balanceado |
| UCS            | Sim      | Sim   | O(b^(1+C/ε))        | O(b^(1+C/ε))      | Custos variáveis |
| A*             | Sim      | Sim** | O(b^d)              | O(b^d)            | Problemas complexos |
| A* Ponderado   | Sim      | Não   | O(b^d)              | O(b^(d/w))        | Soluções rápidas |
| Busca Gulosa   | Não      | Não   | O(b^m)              | O(b^m)            | Testes rápidos |

Legenda:
- *Ótimo para problemas com custo uniforme
- **Quando a heurística é admissível
- b = fator de ramificação
- d = profundidade da solução ótima
- m = profundidade máxima da árvore
- C = custo da solução ótima
- ε = custo mínimo por ação
- w = peso da heurística (w > 1)

## Conclusão
A escolha do algoritmo depende dos requisitos:
 Para soluções com mínimo de movimentos
- **UCS**: Para soluções estratégicas com custos variáveis
- **DFS/IDDFS**: Quando a memória é limitada

A escolha do algoritmo ideal depende dos requisitos específicos do problema e dos recursos disponíveis:

- **BFS**: Melhor para soluções com mínimo absoluto de movimentos, garantindo o caminho mais curto em problemas com custo uniforme. Indicado quando a otimalidade é crucial e o espaço de estados é moderado.

- **UCS**: Ideal para soluções estratégicas com custos variáveis de movimento, priorizando ações mais significativas. Excelente quando diferentes movimentos têm pesos distintos na estratégia de solução.

- **DFS/IDDFS**: Mais adequados quando a memória é limitada ou quando se suspeita que a solução está em níveis mais profundos da árvore de busca. O IDDFS oferece bom equilíbrio entre completude e uso de memória.

- **A***: A melhor opção para problemas complexos onde uma boa heurística está disponível, combinando eficiência com garantia de solução ótima quando a heurística é admissível.

- **A* Ponderado**: Recomendado quando se necessita de soluções rápidas com qualidade razoável, especialmente em problemas grandes onde o A* tradicional seria muito lento.

- **Busca Gulosa**: Útil para análises preliminares rápidas ou quando o tempo de resposta é crítico, mas a qualidade da solução é secundária.

Cada algoritmo apresenta vantagens específicas, e a escolha final deve considerar o trade-off entre:
✔️ Qualidade da solução (otimalidade)
✔️ Velocidade de processamento
✔️ Consumo de memória
✔️ Complexidade de implementação

# Análise de Heurísticas para o Bird Sort

## 🔍 Heurística de Priorização de Grupos
**Método:** `heuristica_prioriza_quase_prontos()`  
**Algoritmo:** A* clássico

### 📊 Métrica de Avaliação
```python
def calcular_heuristica(estado):
    pontos = 0
    # Identifica grupos quase completos (3/4)
    for galho, passaros in estado.items():
        if len(passaros) == 3 and all(p == passaros[0] for p in passaros):
            pontos -= 200  # Prioridade máxima
            
        # Verifica pares no topo
        elif len(passaros) >= 2 and passaros[-1] == passaros[-2]:
            pontos -= 30
            
    return pontos
```
### ✔️ Vantagens
- Foco estratégico em completar grupos
- Eficaz para soluções ótimas
- Precisão em jogos complexos

### ❌ Limitações
- Custo computacional elevado
- Implementação mais complexa


## 📐 Heurística Modular Simples
**Método:** `heuristica_modular_simples()`  
**Algoritmo:** A* Ponderado e Busca Gulosa

### 📈 Fórmula Básica
```python
def heuristica_simples(estado):
    total_passaros = sum(len(p) for p in estado.values())
    diversidade = sum(len(set(p)) for p in estado.values())
    vazios = sum(1 for p in estado.values() if not p)
    
    return total_passaros + diversidade - vazios
```

## 🧩 Heurística de Liberação
**Método:** `calcular_heuristica_liberacao()`  
**Algoritmo:** A* Ponderado e Busca Gulosa

### 🔧 Mecânica Principal
```python
def calcular_liberacao(estado):
    pontos = 0
    # Penaliza congestionamento
    for galho, passaros in estado.items():
        if len(passaros) > 2 and len(set(passaros)) > 1:
            pontos += 10 * len(passaros)
            
    # Bonifica mobilidade
    pontos -= calcular_movimentos_possiveis(estado) * 20
    
    return pontos
```

## 📌 Tabela Comparativa Completa
| Heurística       | Complexidade | Melhor Caso de Uso | Custo Computacional |
|------------------|--------------|--------------------|---------------------|
| Priorização Grupos | Alta | Finais de jogo | Alto |
| Modular Simples    | Baixa | Análise inicial | Muito Baixo |
| Liberação | Média | Situações de bloqueio | Moderado |

# Resultados e Análise de Desempenho dos Algoritmos

## Gráficos e Interpretações

### 1. Dispersão: Estados Gerados vs Caminhos
![Dispersão Estados vs Caminhos](docs/splot/dispersao_estados_vs_caminhos.png)  
**O que mostra**:  
- Relação entre quantidade de estados explorados e caminhos analisados  
- Algoritmos no canto superior direito (BFS/UCS) são menos eficientes  
- A* Ponderado aparece mais concentrado (mais consistente)

---

### 2. Eficiência: Tempo vs Estados Gerados
![Tempo vs Estados](docs/splot/eficiencia_tempo_estados.png)  
**Insights**:  
- Correlação clara: mais estados = mais tempo de execução  
- BFS/UCS no canto superior direito (piores desempenhos)  
- A* Ponderado no canto inferior esquerdo (melhor eficiência)

---

### 3. Distribuição do Tempo de Execução
![Boxplot Tempo](docs/splot/boxplot_tempo_execucao.png)  
**Destaques**:  
- BFS/UCS com maior variação e outliers extremos  
- Heurísticas (A*/Greedy) com distribuição mais compacta  
- DFS apresenta alguns picos de tempo

---

### 4. Correlação entre Variáveis
![Heatmap Correlação](docs/splot/heatmap_correlacao.png)  
**Principais correlações**:  
- Tempo e Estados Gerados: >0.8 (forte)  
- Caminhos e Estados: ~0.6 (moderada)  
- Tempo e Caminhos: ~0.5 (fraca)

---

### 5. Comparação de Heurísticas
![Comparação Heurísticas](docs/splot/comparacao_heuristicas.png)  
**Resultados**:  
1. A* Ponderado: mais rápido (0.01s médio)  
2. A*: intermediário (0.25s)  
3. Greedy: variável (0.35s)

---

### 6. Tempo Médio por Algoritmo
![Tempo Médio](docs/splot/tempo_medio_execucao.png)  
**Ranking**:  
- Piores: BFS (25s) e UCS (3.5s)  
- Melhores: DFS (0.005s) e A* Ponderado (0.01s)  
- Intermediários: DFSi (0.02s), A* (0.25s)

---

### 7. Caminhos Médios Explorados
![Caminhos Médios](docs/splot/caminhos_medios_por_algoritmo.png)  
**Observações**:  
- DFS explora mais caminhos (média alta)  
- Heurísticas reduzem caminhos não ótimos  
- BFS/UCS mantêm equilíbrio na exploração

## Conclusões Gerais
✅ **A* Ponderado** apresenta melhor equilíbrio entre tempo e qualidade  
⚠️ **Greedy** pode ser rápido, mas menos consistente  
⏳ **BFS/UCS** garantem otimalidade com alto custo computacional  
⚡ **DFS/DFSi** são rápidos, mas arriscados para problemas complexos


# Instruções de Execução do Bird Sort Game

## 📋 Pré-requisitos

### Para Windows e Linux
- [Python 3.8+](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/) (normalmente vem com Python)
- [Git](https://git-scm.com/downloads) (opcional, mas recomendado)

## 🛠️ Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/douglasojesus/bird-sort-game.git
cd bird-sort-game
```

### 2. Criar ambiente virtual (recomendado)
- No windows:
```bash
python -m venv venv
venv\Scripts\activate
```
- No linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. 🚀 Execução
```bash
python main.py
```
