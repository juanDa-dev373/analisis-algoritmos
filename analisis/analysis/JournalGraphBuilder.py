import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import networkx as nx
from analisis.dataset.data_handler import DataHandler
from analisis.analysis.graph_analysis import GraphAnalysis
from analisis.analysis.visualization import Visualization
from analisis.analysis.dendogram import DrawDendogram

class JournalGraphBuilder:
    def __init__(self, data_path: str, category_path: str, output_path: str):
        self.data_path = data_path
        self.category_path = category_path
        self.output_path = output_path
        dataHandler = DataHandler(self.data_path, self.category_path)
        self.df = dataHandler.load_and_prepare()
        self.categorias = dataHandler._load_categories_from_txt()
        self.frecuencias_categoria = dataHandler._compute_frequencies(self.categorias, self.df)
        self.graph = nx.Graph()
        self.visualition = Visualization()

    def generateDendogram(self):
        dendogram = DrawDendogram()
        dendogram._generate_dendrograms(self.df, self.output_path, self.categorias)


    def drawSaveGraph(self):
        graph = GraphAnalysis()
        abstracts = self.df['Abstract']
        self.graph = graph.build_graph(abstracts, self.categorias)
        self.visualition.draw_and_save_graph(self.graph, self.output_path)

    def drawGenerateBarCharts(self):
        self.visualition.generate_bar_charts(self.frecuencias_categoria, self.output_path)

    def drawWordClouds(self):
        self.visualition.generate_wordclouds(self.frecuencias_categoria, self.output_path)

    def drawGlobalWordCloud(self):
        self.visualition.generate_global_wordcloud(self.frecuencias_categoria, self.output_path)


if __name__ == "__main__":
    builder = JournalGraphBuilder(
        data_path= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv"),
        category_path= os.path.join(os.path.dirname(__file__), "../static/assets/Category_txt/categories.txt"),
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/assets/statistics"))
    )
    builder.generateDendogram()
    builder.drawWordClouds()
    builder.drawGlobalWordCloud()
    builder.drawSaveGraph()
    builder.drawGenerateBarCharts()
