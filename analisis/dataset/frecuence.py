from colorama import Style, init, Fore
from analisis.dataset.data_saver import DataSaver
from analisis.dataset.data_saver import DataUnifier
from analisis.dataset.dataset_processor import DatasetProcessor
from analisis.algorithm.BitonicSort import BitonicSort
from analisis.algorithm.BucketSort import BucketSort
from analisis.algorithm.CombSort import CombSort
from analisis.algorithm.GnomeSort import GnomeSort
from analisis.algorithm.HeapSort import HeapSort
from analisis.algorithm.PigeonholeSort import PigeonholeSort
from analisis.algorithm.RadixSort import RadixSort
from analisis.algorithm.TreeSort import TreeSort
from analisis.algorithm.BubbleSort import BubbleSort


from analisis.algorithm.TimSort import TimSort
from analisis.algorithm.BinaryInsertionSort import BinaryInsertionSort
from analisis.analysis.SortingAnalyzer import SortingAnalyzer
from analisis.algorithm.SelectionSort import SelectionSort
from analisis.algorithm.QuickSort import QuickSort
from analisis.dataset.dataset_processor import DatasetProcessor

# Inicializar colorama
init(autoreset=True)

if __name__ == "__main__":
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Frecuencia de palabras en los Abstract   ***")
    print(Fore.CYAN + "=" * 60)
    
    input_file_path = 'analisis/static/assets/Data_Final/datafinalbib.csv'
    
    dataset_processor = DatasetProcessor(input_file_path, "")
    dataset = dataset_processor.count_terms()

    # Métodos de ordenamiento disponibles
    sorting_methods = {
        'tim': TimSort,
        'comb': CombSort,
        'selection': SelectionSort,
        'tree': TreeSort,
        'pigeonhole': PigeonholeSort,
        'bucket': BucketSort,
        'quick': QuickSort,
        'heap': HeapSort,
        'bitonic': BitonicSort,
        'gnome': GnomeSort,
        'binary': BinaryInsertionSort,
        'radix': RadixSort,
        'bubble' : BubbleSort
    }

    
    analyzer = SortingAnalyzer("", "analisis/static/assets/Data_Final/frecuence.csv", "")

    analyzer.analyzeAll(dataset, len(dataset), sorting_methods)
    print("Proceso completado. Registros únicos y duplicados guardados.")
