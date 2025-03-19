import pandas as pd
from colorama import Fore, Style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import os

class SortingAnalyzer:
    def __init__(self, sorting_algorithm, output_directory, name_file):
        self.sorting_algorithm = sorting_algorithm
        self.output_directory = output_directory
        self.name_file = name_file
        self.sizes_list = []
        self.times_list = []
        print(self.output_directory)
        os.makedirs(self.output_directory, exist_ok=True)

    def analyze(self, dataset, description, dataset_size):
        """Ejecuta el ordenamiento y mide el rendimiento."""
        self._display_title(description, dataset_size)

        start_time = time.time()
        tqdm.write(Fore.CYAN + "Ordenando..." + Style.RESET_ALL)

        sorted_data = self.sorting_algorithm.sort(dataset.copy())

        execution_time = time.time() - start_time

        self._save_results(sorted_data, dataset_size)
        self._log_execution_time(dataset_size, execution_time)
    
    def analyze2(self, dataset, description, dataset_size, param_ex):
        """Ejecuta el ordenamiento y mide el rendimiento."""
        self._display_title(description, dataset_size)

        start_time = time.time()
        tqdm.write(Fore.CYAN + "Ordenando..." + Style.RESET_ALL)

        sorted_data = self.sorting_algorithm.sort(dataset.copy(), param_ex)

        execution_time = time.time() - start_time

        self._save_results(sorted_data, dataset_size)
        self._log_execution_time(dataset_size, execution_time)


    def _display_title(self, description, dataset_size):
        print("\n" + Style.BRIGHT + Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + f"  ***   Ordenamiento {self.name_file} - {description}   ***")
        print(Fore.CYAN + "=" * 60 + "\n")
        print(Fore.GREEN + Style.BRIGHT + f"Tamaño del arreglo: {dataset_size}\n" + Style.RESET_ALL)

    def _save_results(self, sorted_data, dataset_size):
        output_csv_path = f'{self.output_directory}/{self.name_file}_Ord_fechaPub_{dataset_size}.csv'
        pd.DataFrame(sorted_data, columns=['Title', 'Autor', 'Year']).to_csv(output_csv_path, index=False)
        print(Fore.BLUE + f'Archivo CSV guardado en: {output_csv_path}' + Style.RESET_ALL)

    def _log_execution_time(self, dataset_size, execution_time):
        self.sizes_list.append(dataset_size)
        self.times_list.append(execution_time)
        print(Fore.YELLOW + f"Tiempo de ejecución: {execution_time:.4f} segundos\n" + Style.RESET_ALL)

    def plot_results(self):
        """Grafica los tiempos de ejecución en función del tamaño del dataset."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.sizes_list, self.times_list, marker='o', linestyle='-', color='b')
        plt.title(f'Tamaño del arreglo vs Tiempo de Ejecución ({self.name_file})')
        plt.xlabel('Tamaño del arreglo')
        plt.ylabel('Tiempo de Ejecución (segundos)')
        plt.xticks(self.sizes_list)
        plt.grid()

        output_png_path = f'{self.output_directory}/tiempo_vs_tamaño.png'
        plt.savefig(output_png_path)
        plt.close()
