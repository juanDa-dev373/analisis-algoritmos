import os
from colorama import Fore, Style
from django.shortcuts import render

from analisis.algorithm.BitonicSort import BitonicSort
from analisis.algorithm.BucketSort import BucketSort
from analisis.algorithm.CombSort import CombSort
from analisis.algorithm.GnomeSort import GnomeSort
from analisis.algorithm.HeapSort import HeapSort
from analisis.algorithm.PigeonholeSort import PigeonholeSort
from analisis.algorithm.RadixSort import RadixSort
from analisis.algorithm.TreeSort import TreeSort

from .algorithm.TimSort import TimSort
from .algorithm.BinaryInsertionSort import BinaryInsertionSort
from .analysis.SortingAnalyzer import SortingAnalyzer
from .algorithm.SelectionSort import SelectionSort
from .algorithm.QuickSort import QuickSort
from .dataset.dataset_processor import DatasetProcessor


def menu_general(request):
    """Vista para el menú principal con las dos opciones"""
    return render(request, 'general_menu/general_menu.html')

def menu_analysis_methods(request):
    """Vista para el menú de métodos de análisis"""
    return render(request, 'analysis_methods/menu_analysis_methods.html')

def loading_screen(request, method):
    """Vista que muestra la pantalla de carga antes de iniciar el ordenamiento"""
    return render(request, 'loading.html', {'method': method})

def menu_ordenamiento(request):
    metodos = [
        {"nombre": "TimSort", 'slug': 'tim', "complejidad": "O(n log n)"},
        {"nombre": "Comb Sort", 'slug': 'comb', "complejidad": "O(n^2)"},
        {'nombre': 'Selection Sort', 'slug': 'selection', 'complejidad': 'O(n²)'},
        {"nombre": "Tree Sort", 'slug': 'tree', "complejidad": "O(n log n)"},
        {"nombre": "Pigeonhole Sort", 'slug': 'pigeonhole', "complejidad": "O(n + r)"},
        {"nombre": "BucketSort", 'slug': 'bucket', "complejidad": "O(n + k)"},
        {'nombre': 'Quick Sort', 'slug': 'quick', 'complejidad': 'O(n log n)'},
        {"nombre": "HeapSort", 'slug': 'heap', "complejidad": "O(n log n)"},
        {"nombre": "Bitonic Sort", 'slug': 'bitonic', "complejidad": "O(log^2 n)"},
        {"nombre": "Gnome Sort", 'slug': 'gnome', "complejidad": "O(n^2)"},
        {"nombre": "Binary Insertion Sort", 'slug': 'binary', "complejidad": "O(n log n)"},
        {"nombre": "RadixSort", 'slug': 'radix', "complejidad": "O(nk)"},
    ]
    return render(request, 'metodos_ordenamiento/menu.html', {"metodos": metodos})

def sort(request, method):
    input_file_path = 'analisis/static/assets/Data_Final/datafinalbib.csv'
    output_file_path = f'analisis/static/assets/Data_Final/sorted_{method}.bib'
    

    os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
    if not os.path.exists(input_file_path):
        return render(request, 'error.html', {'message': 'El archivo de datos no existe'})
    
    # Cargar y procesar los datos
    dataset_processor = DatasetProcessor(input_file_path, output_file_path)
    dataset = dataset_processor.load_data()
    
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
        'radix': RadixSort
    }
    
    sorter_class = sorting_methods.get(method)
    if not sorter_class:
        return render(request, 'error.html', {'message': 'Método de ordenamiento no válido'})
    
    # Aplicar el algoritmo de ordenamiento
    sorter = sorter_class()
    sorted_books = sorter.sort(dataset.copy(), 1)
    
    # Analizar y visualizar los resultados
    analyzer = SortingAnalyzer(sorter, f"analisis/static/assets/Data_Ordenamiento/{method}", method)
    analyzer.analyze(dataset, "Total de datos", len(dataset))
    analyzer.analyze(dataset[:len(dataset) // 2], "Mitad de datos", len(dataset) // 2)
    analyzer.analyze(dataset[:len(dataset) // 4], "Un cuarto de datos", len(dataset) // 4)
    analyzer.analyze(dataset[:100], "Primeros 100 datos", 100)
    analyzer.plot_results()
    
    print(Fore.MAGENTA + f"Ordenamiento completo con {method}." + Style.RESET_ALL)
    image_url = f'/static/assets/Data_Ordenamiento/{method}/tiempo_vs_tamaño.png'
    
    return render(request, 'sort_results/sort_results.html', {
        'sorted_books': sorted_books,
        'method': method,
        'output_file': output_file_path,
        'image_url': image_url
    })

# Vistas para los métodos de análisis
def analizar_frecuencia(request):
    # Implementación de la vista para analizar frecuencia
    return render(request, 'analysis_methods/analizar_frecuencia.html')

def generar_dendograma(request):
    # Implementación de la vista para generar dendograma
    return render(request, 'analysis_methods/generar_dendograma.html')

def generar_nube_palabras(request):
    # Implementación de la vista para generar nube de palabras
    return render(request, 'analysis_methods/generar_nube_palabras.html')

def graficas_frecuencia(request):
    # Implementación de la vista para gráficas de frecuencia
    return render(request, 'analysis_methods/graficas_frecuencia.html')
