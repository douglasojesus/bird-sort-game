# Métodos de Busca Heurística para Jogos de Solitário de Um Jogador

### Projeto a ser desenvolvido para a unidade curricular de Inteligência Artificial da FEUP.
**Jogo de inspiração escolhido: Bird Sort.**
**Algoritmos a serem implementados: sem conhecimento (busca em largura, busca em profundidade, aprofundamento iterativo, custo uniforme) e com heurística (busca gulosa, algoritmo A*, A* Ponderado).**

# Explicação dos Algoritmos de Busca para o Bird Sort

## Visão Geral
A classe `Algoritmo` implementa quatro métodos de busca para resolver o jogo tipo Bird Sort:
1. **BFS (Busca em Largura)**
2. **DFS (Busca em Profundidade)**
3. **Busca em Profundidade Iterativa**
4. **Busca de Custo Uniforme (UCS)**

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

## Comparação entre os Algoritmos

| Algoritmo | Completo | Ótimo | Complexidade Espaço | Melhor Caso |
|-----------|----------|-------|---------------------|-------------|
| BFS       | Sim      | Sim*  | O(b^d)              | Poucos movimentos |
| DFS       | Não      | Não   | O(bm)               | Solução profunda |
| IDDFS     | Sim      | Sim*  | O(bd)               | Balanceado |
| UCS       | Sim      | Sim   | O(b^(1+C/ε))        | Custos variáveis |

*Para problemas com custo uniforme por movimento

## Conclusão
A escolha do algoritmo depende dos requisitos:
- **BFS**: Para soluções com mínimo de movimentos
- **UCS**: Para soluções estratégicas com custos variáveis
- **DFS/IDDFS**: Quando a memória é limitada
