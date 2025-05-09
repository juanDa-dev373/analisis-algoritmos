import networkx as nx

class GraphAnalysis:
    def build_graph(self, abstracts, categorias):
        graph = nx.Graph()
        for abstract in abstracts:
            presentes = []
            for variables in categorias.values():
                for var in variables:
                    sinonimos = var.split('-')
                    if any(s in abstract for s in sinonimos):
                        presentes.append(var)
            for i in range(len(presentes)):
                for j in range(i + 1, len(presentes)):
                    if graph.has_edge(presentes[i], presentes[j]):
                        graph[presentes[i]][presentes[j]]['weight'] += 1
                    else:
                        graph.add_edge(presentes[i], presentes[j], weight=1)
        return graph
