import os
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from colorama import Style, init, Fore
from collections import defaultdict
from wordcloud import WordCloud
import community as community_louvain

init(autoreset=True)

class JournalGraphBuilder:
    def __init__(self, data_path: str, category_path: str, output_path: str):
        self.data_path = data_path
        self.category_path = category_path
        self.output_path = output_path
        self.df = pd.DataFrame()
        self.categorias = {}
        self.frecuencias_categoria = {}
        self.graph = nx.Graph()

    def run(self):
        self._print_title()
        self.df = self._load_and_prepare_data()
        self.categorias = self._load_categories_from_txt()
        self._compute_frequencies()
        self._build_co_word_graph()
        self._generate_wordclouds()
        self._draw_and_save_graph()
        self._print_success()

    def _print_title(self):
        print("\n" + Style.BRIGHT + Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + Style.BRIGHT + "  ***   Análisis de Categorías desde Abstracts   ***")
        print(Fore.CYAN + "=" * 60 + "\n")

    def _load_and_prepare_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        df['Abstract'] = df['Abstract'].fillna('').str.lower()
        return df

    def _load_categories_from_txt(self) -> dict:
        categorias = {}
        with open(self.category_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        categoria_actual = None
        for line in lines:
            if line in {"Habilidades", "Conceptos Computationales", "Actitudes", "Propiedades psicométricas", "Herramienta de evaluación",
            "Diseño de investigación", "Nivel de escolaridad", "Medio", "Estrategia", "Herramienta"}:
                categoria_actual = line
                categorias[categoria_actual] = []
            else:
                categorias[categoria_actual].append(line.lower())
        return categorias

    def _compute_frequencies(self):
        for categoria, variables in self.categorias.items():
            frecuencias = defaultdict(int)
            for var in variables:
                sinónimos = var.split('-')
                for abstract in self.df['Abstract']:
                    if any(re.search(rf'\b{re.escape(s)}\b', abstract) for s in sinónimos):
                        frecuencias[var] += sum(abstract.count(s) for s in sinónimos)
            self.frecuencias_categoria[categoria] = dict(frecuencias)

    def _generate_wordclouds(self):
        os.makedirs(self.output_path+"/word-clouds", exist_ok=True)
        for categoria, freqs in self.frecuencias_categoria.items():
            if freqs:
                wc = WordCloud(width=800, height=400).generate_from_frequencies(freqs)
                plt.figure()
                plt.title(f'Nube de Palabras - {categoria}')
                plt.imshow(wc, interpolation='bilinear')
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_path+"/word-clouds", f'wordcloud_{categoria}.png'))
                plt.close()

    def _build_co_word_graph(self):
        self.graph = nx.Graph()
        for abstract in self.df['Abstract']:
            presentes = []
            for variables in self.categorias.values():
                for var in variables:
                    sinónimos = var.split('-')
                    if any(s in abstract for s in sinónimos):
                        presentes.append(var)
            for i in range(len(presentes)):
                for j in range(i + 1, len(presentes)):
                    if self.graph.has_edge(presentes[i], presentes[j]):
                        self.graph[presentes[i]][presentes[j]]['weight'] += 1
                    else:
                        self.graph.add_edge(presentes[i], presentes[j], weight=1)

    def _draw_and_save_graph(self):
        if not self.graph:
            print("No se generó ningún grafo de co-ocurrencia.")
            return

        os.makedirs(self.output_path+"/graph", exist_ok=True)

        # Detección de comunidades con Louvain
        partition = community_louvain.best_partition(self.graph)

        # Posiciones con layout forzado
        pos = nx.spring_layout(self.graph, k=9, seed=42)

        # Colores y tamaños
        cmap = plt.get_cmap('tab20')
        node_colors = [cmap(partition[node]) for node in self.graph.nodes()]
        node_sizes = [300 + 40 * self.graph.degree(node) for node in self.graph.nodes()]
        edge_widths = [0.5 + self.graph[u][v]['weight'] * 0.2 for u, v in self.graph.edges()]

        plt.figure(figsize=(22, 18))
        nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.85, edgecolors=node_colors)
        nx.draw_networkx_edges(self.graph, pos, width=edge_widths, alpha=0.1)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_family='sans-serif')

        plt.title("Co-Word Network Visualization (Louvain Communities)", fontsize=18, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        output_file = os.path.join(self.output_path+"/graph", "co_word_graph.png")
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"Grafo guardado en: {output_file}")

    def _print_success(self):
        print(Fore.GREEN + Style.BRIGHT + "=" * 60)
        print(Fore.GREEN + f"Análisis completado. Archivos guardados en: {self.output_path}")
        print(Fore.GREEN + "=" * 60)

if __name__ == "__main__":
    builder = JournalGraphBuilder(
        data_path= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv"),
        category_path= os.path.join(os.path.dirname(__file__), "../static/assets/Category_txt/categories.txt"),
        output_path='../static/assets/statistics'
    )
    builder.run()
