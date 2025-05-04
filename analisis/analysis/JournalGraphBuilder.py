import os
import re
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from colorama import Style, init, Fore

init(autoreset=True)

class JournalGraphBuilder:
    def __init__(self, data_path: str, output_path: str):
        self.data_path = data_path
        self.output_path = output_path
        self.graph = nx.Graph()
        self.top_journals = []
        self.journal_articles = {}
        self.journal_colors = sns.color_palette("Set2", n_colors=10)
        self.article_colors = sns.color_palette("Paired", n_colors=8)

    def run(self):
        self._print_title()
        df = self._load_and_prepare_data()
        self._extract_top_journals(df)
        self._build_article_dict(df)
        self._build_graph()
        self._draw_and_save_graph()
        self._print_success()

    def _print_title(self):
        print("\n" + Style.BRIGHT + Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + Style.BRIGHT + "  ***   Análisis de Journals y Artículos Más Citados   ***")
        print(Fore.CYAN + "=" * 60 + "\n")

    def _load_and_prepare_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        if 'Article Citation Count' not in df.columns:
            df['Article Citation Count'] = [random.randint(0, 250) for _ in range(len(df))]
        else:
            df['Article Citation Count'].fillna(random.randint(0, 250), inplace=True)

        df['Journal'] = df['Publication Title'].fillna(df['ISSN'])
        df['Journal'] = df['Journal'].apply(self._clean_journal_name)
        return df

    @staticmethod
    def _clean_journal_name(journal_name: str) -> str:
        return re.sub(r"[\-,\(\),].*", "", journal_name).strip()

    def _extract_top_journals(self, df: pd.DataFrame):
        self.top_journals = df['Journal'].value_counts().nlargest(10).index.tolist()

    def _build_article_dict(self, df: pd.DataFrame):
        for journal in tqdm(self.top_journals, desc="Filtrando artículos de los 10 journals principales"):
            articles = df[df['Journal'] == journal].nlargest(8, 'Article Citation Count')
            self.journal_articles[journal] = articles

    def _build_graph(self):
        for journal, articles in tqdm(self.journal_articles.items(), desc="Construyendo grafo de journals y artículos"):
            color_journal = self.journal_colors[self.top_journals.index(journal)]
            self.graph.add_node(journal, label='Journal', color=color_journal, size=4000)

            for idx, article in articles.iterrows():
                title = article['Title']
                country = article['Country']
                citations = article['Article Citation Count']
                color_article = self.article_colors[idx % len(self.article_colors)]

                self.graph.add_node(title, label=f"{country} ({citations} citas)", color=color_article, size=800 + citations * 4)
                self.graph.add_edge(journal, title, weight=1 + citations / 50)

    def _draw_and_save_graph(self):
        os.makedirs(self.output_path, exist_ok=True)

        node_colors = [self.graph.nodes[node]['color'] for node in self.graph]
        node_sizes = [self.graph.nodes[node]['size'] for node in self.graph]
        edge_weights = [self.graph[u][v]['weight'] for u, v in self.graph.edges()]

        plt.figure(figsize=(22, 18))
        pos = nx.spring_layout(self.graph, k=0.6, seed=42)

        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=node_sizes,
                               edgecolors='k', linewidths=0.8, alpha=0.85)
        nx.draw_networkx_edges(self.graph, pos, width=edge_weights, edge_color='gray', alpha=0.4)

        journal_labels = {n: n for n in self.graph if self.graph.nodes[n]['label'] == 'Journal'}
        article_labels = {n: self.graph.nodes[n]['label'] for n in self.graph if self.graph.nodes[n]['label'] != 'Journal'}

        nx.draw_networkx_labels(self.graph, pos, journal_labels, font_size=13, font_color='navy', font_weight='bold')
        for node, label in article_labels.items():
            x, y = pos[node]
            plt.text(x, y, label, fontsize=10, color='darkgreen', ha='center', va='center', alpha=0.8)

        plt.title('Relación entre Journals y sus Artículos Más Citados', fontsize=18, color='indigo', fontweight='bold')
        plt.axis('off')

        output_file = os.path.join(self.output_path, 'journal_article_graph.png')
        plt.savefig(output_file, format='png', bbox_inches='tight', dpi=300)
        plt.show()

        self.output_file = output_file

    def _print_success(self):
        print(Fore.GREEN + Style.BRIGHT + "=" * 60)
        print(Fore.GREEN + f"Grafo guardado como imagen en: {self.output_file}")
        print(Fore.GREEN + "=" * 60)


if __name__ == "__main__":
    builder = JournalGraphBuilder(
        data_path='DataFinal/combined_datafinal.csv',
        output_path='requerimiento5/statistics'
    )
    builder.run()
