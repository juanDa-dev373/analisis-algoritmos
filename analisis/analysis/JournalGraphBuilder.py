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
        self.df = pd.DataFrame()
        self.categorias = {}
        self.frecuencias_categoria = {}
        self.graph = nx.Graph()
        self.visualition = Visualization()

    def run(self):
        dataHandler = DataHandler(self.data_path, self.category_path)
        self.df = dataHandler.load_and_prepare()
        self.categorias = dataHandler._load_categories_from_txt()
        self.frecuencias_categoria = dataHandler._compute_frequencies(self.categorias, self.df)
        graph = GraphAnalysis()
        #print(self.df['Abstract'])
        abstracts = self.df['Abstract']
        self.graph = graph.build_graph(abstracts, self.categorias)
        #visualition = Visualization()

        self.drawSaveGraph()
        #visualition.draw_and_save_graph(self.graph, self.output_path)
        
        dfs = dataHandler._load_and_prepare_all_data()
        frecuencies = dataHandler._compute_frequencies(self.categorias, dfs)

        self.drawGenerateBarCharts(frecuencies, self.output_path)
        #visualition.generate_bar_charts(frecuencies, self.output_path)
        
        self.drawWordClouds(frecuencies, self.output_path)
        #visualition.generate_wordclouds(frecuencies, self.output_path)
        
        self.drawGlobalWordCloud( frecuencies)
        #visualition.generate_global_wordcloud(frecuencies, self.output_path)

        dendogram = DrawDendogram()
        dendogram._generate_dendrograms(self.df, self.output_path, self.categorias)

    def drawSaveGraph(self):
        self.visualition.draw_and_save_graph(self.graph, self.output_path)

    def drawGenerateBarCharts(self, frecuencies, output_path):
        self.visualition.generate_bar_charts(frecuencies, output_path)

    def drawWordClouds(self, frecuencies, output_path):
        self.visualition.generate_wordclouds(frecuencies, output_path)

    def drawGlobalWordCloud(self, frecuencies):
        self.visualition.generate_global_wordcloud(frecuencies, self.output_path)


if __name__ == "__main__":
    builder = JournalGraphBuilder(
        data_path= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv"),
        category_path= os.path.join(os.path.dirname(__file__), "../static/assets/Category_txt/categories.txt"),
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/assets/statistics"))
    )
    builder.run()
