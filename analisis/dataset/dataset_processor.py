import pandas as pd
import os
from analisis.dataset.bib_file_processor import BibFileProcessor
from analisis.dataset.data_saver import DataSaver as bibsave


class DatasetProcessor:
    def __init__(self, file_path: str, output_dir: str):
        self.file_path = file_path
        self.output_dir = output_dir

    def load_and_process(self):
        """Carga y filtra los datos necesarios."""            
        dataset = BibFileProcessor("",[]).clean_and_transform_bib(self.file_path)
        dataset_filtered = dataset[['Title', 'Autor', 'Year']].copy()
        dataset_filtered['Year'] = pd.to_numeric(dataset_filtered['Year'], errors='coerce')
        dataset_filtered.dropna(subset=['Year'], inplace=True)
        dataset_filtered['Year'] = dataset_filtered['Year'].astype(int)
        return list(dataset_filtered.itertuples(index=False, name=None))

    def load_data(self):
        """Carga y filtra los datos del CSV."""
        df = pd.read_csv(self.file_path)
        df_filtered = df[['Title', 'Autor', 'Year']].copy()
        df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
        df_filtered.dropna(subset=['Year'], inplace=True)
        df_filtered['Year'] = df_filtered['Year'].astype(int)
        return list(zip(df_filtered['Title'], df_filtered['Autor'], df_filtered['Year']))

    def save_sorted_data(self, sorted_data, size):
        """Guarda los datos ordenados en un archivo CSV."""
        output_file = os.path.join(self.output_dir, f"treeSort_Ord_fechaPub_{size}.csv")
        sorted_df = pd.DataFrame(sorted_data, columns=['Title', 'Autor', 'Year'])
        bibsave.save_to_bib(sorted_df)
        return output_file
