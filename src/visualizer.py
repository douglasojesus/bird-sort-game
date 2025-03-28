from graphviz import Digraph

def visualizar_arvore(nos):
    dot = Digraph()
    
    for no in nos:
        estado_id = hash(tuple((k, tuple(v) if v != 'X' else 'X') for k, v in no['estado'].items()))
        dot.node(str(estado_id), label=str(no['estado']))
        
        if no['pai'] is not None:
            dot.edge(str(no['pai']), str(estado_id), label=no['movimento'])
    
    dot.render('arvore_busca', view=True)