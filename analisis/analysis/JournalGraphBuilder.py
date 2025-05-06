import os
import re
import sys
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from colorama import Style, init, Fore
from collections import defaultdict
from wordcloud import WordCloud
import community as community_louvain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
        self.generate_global_wordcloud()
        self._draw_and_save_graph()
        self.generar_graficas_por_categoria()
        self._generate_dendrograms()
        self._print_success()

    def _print_title(self):
        print("\n" + Style.BRIGHT + Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + Style.BRIGHT + "  ***   Análisis de Categorías desde Abstracts   ***")
        print(Fore.CYAN + "=" * 60 + "\n")

    def _load_and_prepare_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        df['Abstract'] = df['Abstract'].fillna('').apply(self._preprocess_text)
        # Vectorizar todos los abstracts
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['Abstract'])
        # Calcular matriz de similitud de coseno
        similarity_matrix = cosine_similarity(tfidf_matrix)
        # Sumar las similitudes de cada abstract con los demás
        similarity_scores = similarity_matrix.sum(axis=1)
        # Obtener los índices de los 50 abstracts más similares
        top_indices = similarity_scores.argsort()[-50:][::-1]
        # Filtrar DataFrame para quedarse con esos 50
        df = df.iloc[top_indices].reset_index(drop=True)
        return df

    def _preprocess_text(self, text: str) -> str:
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text.lower())
        words = [lemmatizer.lemmatize(w) for w in words if w.isalpha() and w not in stopwords.words('english')]
        return ' '.join(words)

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
                    if any(re.search(rf'\\b{re.escape(s)}\\b', abstract) for s in sinónimos):
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

    def generate_global_wordcloud(self):
        os.makedirs(self.output_path + "/word-clouds", exist_ok=True)
        global_freqs = defaultdict(int)
        for freqs in self.frecuencias_categoria.values():
            for palabra, count in freqs.items():
                global_freqs[palabra] += count

        if global_freqs:
            wc = WordCloud(width=1000, height=500, background_color='black').generate_from_frequencies(global_freqs)
            plt.figure()
            plt.title("Nube de Palabras - Global")
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_path + "/word-clouds", "wordcloud_global.png"))
            plt.close()
            print("Nube de palabras global guardada.")

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

        os.makedirs(self.output_path + "/graph", exist_ok=True)
        partition = community_louvain.best_partition(self.graph)
        pos = nx.spring_layout(self.graph, k=9, seed=42)
        cmap = plt.get_cmap('tab20')
        node_color_dict = {node: cmap(partition[node]) for node in self.graph.nodes()}
        node_colors = [node_color_dict[node] for node in self.graph.nodes()]
        node_sizes = [300 + 40 * self.graph.degree(node) for node in self.graph.nodes()]
        edge_widths = [0.5 + self.graph[u][v]['weight'] * 0.2 for u, v in self.graph.edges()]
        edge_colors = [node_color_dict[u] for u, v in self.graph.edges()]

        plt.figure(figsize=(22, 18))
        nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.85, edgecolors='black')
        nx.draw_networkx_edges(self.graph, pos, width=edge_widths, edge_color=edge_colors, alpha=0.4)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_family='sans-serif')

        plt.title("Co-Word Network Visualization (Louvain Communities)", fontsize=18, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        output_file = os.path.join(self.output_path + "/graph", "co_word_graph.png")
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"Grafo guardado en: {output_file}")

    def _print_success(self):
        print(Fore.GREEN + Style.BRIGHT + "=" * 60)
        print(Fore.GREEN + f"Análisis completado. Archivos guardados en: {self.output_path}")
        print(Fore.GREEN + "=" * 60)

    def generar_graficas_por_categoria(self):
        os.makedirs(self.output_path + "/bar-charts", exist_ok=True)
        for categoria, freqs in self.frecuencias_categoria.items():
            if not freqs:
                continue
            sorted_freqs = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=True))
            plt.figure(figsize=(10, 6))
            plt.barh(list(sorted_freqs.keys()), list(sorted_freqs.values()), color='lightsteelblue', edgecolor='navy')
            plt.xlabel("Frecuencia", fontsize=12, color="navy")
            plt.ylabel("Variables", fontsize=12, color="navy")
            plt.title(f"Frecuencia de Variables en la Categoría: {categoria}", fontsize=14, color="darkblue")
            plt.grid(axis='x', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            output_file = os.path.join(self.output_path+"/bar-charts", f"frecuencia_{categoria}.png")
            plt.savefig(output_file, dpi=300)
            plt.close()

    def _generate_dendrograms(self):
        os.makedirs(self.output_path + "/dendrograms", exist_ok=True)
        abstracts = self.df['Abstract'].tolist()
        titles = self.df['Title'].fillna('Sin título').tolist()

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(abstracts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        distance_matrix = 1 - similarity_matrix

        methods = ['ward', 'average']
        for method in methods:
            linkage_matrix = linkage(distance_matrix, method=method)
            plt.figure(figsize=(18, 10))
            dendrogram(linkage_matrix, labels=titles, leaf_rotation=90)
            plt.title(f"Dendrograma de Agrupamiento - Método: {method.capitalize()}")
            plt.xlabel("Artículos")
            plt.ylabel("Distancia")
            plt.tight_layout()
            output_file = os.path.join(self.output_path + "/dendrograms", f"abstracts_dendrogram_{method}.png")
            plt.savefig(output_file, dpi=300)
            plt.close()

            # Comparar con categorías (solo para evaluar calidad de cluster)
            cluster_labels = fcluster(linkage_matrix, t=5, criterion='maxclust')
            true_labels = self._generate_true_labels()
            ari = adjusted_rand_score(true_labels, cluster_labels)
            print(f"ARI (Adjusted Rand Index) para método {method}: {ari:.4f}")

    def _generate_true_labels(self):
        """
        Se asigna un índice entero a cada categoría que aparece en cada abstract.
        Se usará para comparar con clustering real.
        """
        label_map = {cat: i for i, cat in enumerate(self.categorias)}
        labels = []
        for abstract in self.df['Abstract']:
            found = False
            for cat, variables in self.categorias.items():
                if any(var in abstract for var in variables):
                    labels.append(label_map[cat])
                    found = True
                    break
            if not found:
                labels.append(-1)  # Sin categoría encontrada
        return labels            
if __name__ == "__main__":
    builder = JournalGraphBuilder(
        data_path= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv"),
        category_path= os.path.join(os.path.dirname(__file__), "../static/assets/Category_txt/categories.txt"),
        output_path='../static/assets/statistics'
    )
    builder.run()
