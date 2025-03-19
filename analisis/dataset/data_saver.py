import os
from typing import List
import pandas as pd
from colorama import Style, init, Fore
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from tqdm import tqdm
from analisis.dataset.bib_file_processor import BibFileProcessor
from analisis.dataset.bib_file_processor import AbstractFetcher


class DataSaver:
    """Clase responsable de guardar y manipular DataFrames."""
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, file_path: str):
        df.to_csv(file_path, index=False)
        print(Fore.MAGENTA + Style.BRIGHT + f'\nArchivo CSV guardado en: {file_path}')
    
    @staticmethod
    def save_to_bib(df: pd.DataFrame, file_path: str):
        """
        Guarda un DataFrame en formato BibTeX (.bib).

        :param df: DataFrame con los datos bibliográficos.
        :param file_path: Ruta donde se guardará el archivo .bib.
        """
        bib_database = BibDatabase()
        bib_database.entries = []

        for _, row in df.iterrows():
            entry = {
                'ENTRYTYPE': 'article',  # Puedes ajustar según el tipo de referencia
                'ID': row.get('Title', 'unknown').replace(" ", "_"),
                'author': row.get('Autor', 'Sin Valor'),
                'title': row.get('Title', 'Sin Valor'),
                'year': row.get('Year', 'Sin Valor'),
                'volume': row.get('Volume', 'Sin Valor'),
                'number': row.get('Issue', 'Sin Valor'),
                'pages': f"{row.get('Start Page', '')}-{row.get('End Page', '')}" if row.get('Start Page') != 'Sin Valor' else 'Sin Valor',
                'abstract': row.get('Abstract', 'Sin Valor'),
                'doi': row.get('DOI', 'Sin Valor'),
                'journal': row.get('Database', 'Sin Valor')
            }
            bib_database.entries.append(entry)
        
        writer = BibTexWriter()
        with open(file_path, 'w', encoding='utf-8') as bibfile:
            bibfile.write(writer.write(bib_database))
        
        print(Fore.GREEN + Style.BRIGHT + f'\nArchivo BibTeX guardado en: {file_path}')
    
    @staticmethod
    def clean_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[:, (df != 'Sin Valor').any(axis=0)]

import os
import pandas as pd
from tqdm import tqdm
from typing import List, Tuple

class DataUnifier:
    """Clase para unificar múltiples archivos .bib en un DataFrame único."""
    def __init__(self, directorio: str, sources: List[str]):
        self.bib_files = self.obtener_archivos_bib(directorio)
        self.sources = self.bib_files  # sources[:len(self.bib_files)]
        self.related_abstracts = AbstractFetcher.get_related_abstracts()

    def obtener_archivos_bib(self, directorio: str) -> List[str]:
        """
        Retorna una lista con los nombres de los archivos .bib en el directorio dado.

        :param directorio: Ruta del directorio a buscar.
        :return: Lista de nombres de archivos .bib.
        """
        try:
            return [os.path.join(directorio, archivo) for archivo in os.listdir(directorio) if archivo.endswith('.bib')]
        except FileNotFoundError:
            print(f"Error: El directorio '{directorio}' no existe.")
            return []
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return []
        
    def unify_bib_files(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Unifica múltiples archivos .bib en un único DataFrame y devuelve también los registros duplicados.

        :return: Una tupla con dos DataFrames:
                 - El primero contiene los registros únicos.
                 - El segundo contiene los registros duplicados eliminados.
        """
        all_records = pd.DataFrame()
        for file_path, source in tqdm(zip(self.bib_files, self.sources), total=len(self.bib_files), desc="Unificando archivos .bib"):
            df = BibFileProcessor(source, self.related_abstracts).clean_and_transform_bib(file_path)
            all_records = pd.concat([all_records, df], ignore_index=True)
        
        # Identificar duplicados antes de eliminarlos
        duplicated_records = all_records[all_records.duplicated(subset=['Title', 'Autor', 'Year', 'DOI'], keep=False)]
        
        # Eliminar duplicados dejando solo los registros únicos
        unique_records = all_records.drop_duplicates(subset=['Title', 'Autor', 'Year', 'DOI'])
        
        return unique_records, duplicated_records
