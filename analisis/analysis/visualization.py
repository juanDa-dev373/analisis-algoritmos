import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
from colorama import Fore
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import networkx as nx
import os

class Visualization:
    def generate_wordclouds(self, frecuencias_categoria, output_path):
        os.makedirs(output_path + "/word-clouds", exist_ok=True)
        print(Fore.YELLOW+f"se inicia generacion de nube de palabras...")
        for categoria, freqs in frecuencias_categoria.items():
            print(Fore.YELLOW + f"se inicia la creacion de la nube de palabras de la categoria: {categoria}")
            if freqs:
                wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(freqs)
                plt.figure()
                plt.title(f'Nube de Palabras - {categoria}')
                plt.imshow(wc, interpolation='bilinear')
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(os.path.join(output_path + "/word-clouds", f'wordcloud_{categoria}.png'))
                plt.close()
                print(Fore.GREEN + f"se creo la nube de palabras de la categoria: {categoria}")
            print(Fore.GREEN + f"se finalizo la creacion de las nubes de palabras")

    def generate_global_wordcloud(self, frecuencias_categoria, output_path):
        os.makedirs(output_path + "/word-clouds", exist_ok=True)
        print(Fore.YELLOW+f"se inicia generacion de nube de palabras global...")
        global_freqs = {}
        for freqs in frecuencias_categoria.values():
            for palabra, count in freqs.items():
                global_freqs[palabra] = global_freqs.get(palabra, 0) + count

        if global_freqs:
            wc = WordCloud(
                width=1200,
                height=600,
                background_color='white',
                max_font_size=150,
                max_words=150  
            ).generate_from_frequencies(global_freqs)
            plt.figure()
            plt.title("Nube de Palabras - Global")
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(os.path.join(output_path + "/word-clouds", "wordcloud_global.png"))
            plt.close()
            print(Fore.GREEN + f"se finalizo la creacion de la nube de palabras Global")

    def generate_bar_charts(self, frecuencias_categoria, output_path):
        print(Fore.YELLOW+f"se inicia generacion de graficas...")
        os.makedirs(output_path + "/bar-charts", exist_ok=True)
        for categoria, freqs in frecuencias_categoria.items():
            print(Fore.YELLOW + f"se inicia la creacion de la grafica de la categoria: {categoria}")
            if not freqs:
                continue
            sorted_freqs = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=True))
            altura = max(2, len(sorted_freqs) * 0.6)  # al menos 2 pulgadas de alto, 0.6 por barra
            plt.figure(figsize=(10, altura))
            plt.barh(list(sorted_freqs.keys()), list(sorted_freqs.values()), color='lightsteelblue', edgecolor='navy')
            plt.xlabel("Frecuencia", fontsize=12, color="navy")
            plt.ylabel("Variables", fontsize=12, color="navy")
            plt.title(f"Frecuencia de Variables en la Categoría: {categoria}", fontsize=14, color="darkblue")
            plt.grid(axis='x', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            plt.savefig(os.path.join(output_path + "/bar-charts", f"frecuencia_{categoria}.png"))
            plt.close()
            print(Fore.GREEN + f"se creo la grafica de la categoria: {categoria}")
        print(Fore.GREEN + f"se finalizo la creacion de graficas")
        
    def draw_and_save_graph(self, graph, output_path):
        if not graph:
            print("No se generó ningún grafo de concurrencia.")
            return

        print("se inició el dibujo del grafo...")
        os.makedirs(os.path.join(output_path, "graph"), exist_ok=True)

        # Reemplazo de Louvain: greedy_modularity_communities
        communities = list(greedy_modularity_communities(graph))

        # Crear partición tipo dict: {nodo: id_comunidad}
        partition = {}
        for i, community in enumerate(communities):
            for node in community:
                partition[node] = i

        pos = nx.spring_layout(graph, k=9, seed=42)
        cmap = plt.get_cmap('tab20')

        node_color_dict = {node: cmap(partition[node]) for node in graph.nodes()}
        node_colors = [node_color_dict[node] for node in graph.nodes()]
        node_sizes = [300 + 40 * graph.degree(node) for node in graph.nodes()]
        edge_widths = [0.5 + graph[u][v].get('weight', 1) * 0.2 for u, v in graph.edges()]
        edge_colors = [node_color_dict[u] for u, v in graph.edges()]

        plt.figure(figsize=(22, 18))
        nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.85, edgecolors='black')
        nx.draw_networkx_edges(graph, pos, width=edge_widths, edge_color=edge_colors, alpha=0.4)
        nx.draw_networkx_labels(graph, pos, font_size=10)

        plt.title("Grafo", fontsize=18)
        plt.axis('off')
        plt.tight_layout()

        output_file = os.path.join(output_path, "graph", "co_word_graph.png")
        plt.savefig(output_file, dpi=300)
        plt.close()
        print("se creó correctamente el grafo :)")