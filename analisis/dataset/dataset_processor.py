import pandas as pd
import os
import re
from analisis.dataset.bib_file_processor import BibFileProcessor
from analisis.dataset.data_saver import DataSaver as bibsave

class DatasetProcessor:
    TERMS = [
        "Abstraction", "Motivation", "Algorithm", "Persistence", "Coding Block", "Creativity", 
        "Mobile application", "Logic", "Programming", "Conditionals", "Robotic", "Loops", "Scratch"
    ]

    def __init__(self, file_path: str, output_dir: str):
        self.file_path = file_path
        self.output_dir = output_dir

    def load_and_process(self):
        """Carga y filtra los datos necesarios."""            
        dataset = BibFileProcessor("",[]).clean_and_transform_bib(self.file_path)
        dataset_filtered = dataset[['Title', 'Autor', 'Year', 'Abstract']].copy()
        dataset_filtered['Year'] = pd.to_numeric(dataset_filtered['Year'], errors='coerce')
        dataset_filtered.dropna(subset=['Year'], inplace=True)
        dataset_filtered['Year'] = dataset_filtered['Year'].astype(int)
        return list(dataset_filtered.itertuples(index=False, name=None))

    def load_data(self):
        """Carga y filtra los datos del CSV."""
        dataset = pd.read_csv(self.file_path)
        dataset_filtered = dataset[['Title', 'Autor', 'Year', 'Abstract']].copy()
        dataset_filtered['Year'] = pd.to_numeric(dataset_filtered['Year'], errors='coerce')
        dataset_filtered.dropna(subset=['Year'], inplace=True)
        dataset_filtered['Year'] = dataset_filtered['Year'].astype(int)
        return list(dataset_filtered.itertuples(index=False, name=None))

    def save_sorted_data(self, sorted_data, size):
        """Guarda los datos ordenados en un archivo CSV."""
        output_file = os.path.join(self.output_dir, f"treeSort_Ord_fechaPub_{size}.csv")
        sorted_df = pd.DataFrame(sorted_data, columns=['Title', 'Autor', 'Year'])
        bibsave.save_to_bib(sorted_df)
        return output_file
    
    def count_terms(self):
        """Cuenta la frecuencia de términos en los abstracts."""
        term_counts = {term: 0 for term in self.TERMS}
        dataset = pd.read_csv(self.file_path)

        for abstract in dataset["Abstract"].dropna():
            words = re.findall(r'\b\w+\b', abstract.lower())
            for term in self.TERMS:
                term_counts[term] += words.count(term.lower())

        # Convertir el diccionario a lista de tuplas
        return list(term_counts.items())