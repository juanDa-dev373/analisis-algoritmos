
from .Sort_Algorithm import SortAlgorithm
from tqdm import tqdm

class SelectionSort(SortAlgorithm):
    def sort(self, array):
        n = len(array)
        for i in tqdm(range(n), desc="Ordenando", unit="parte"):
            min_index = i
            for j in range(i + 1, n):
                if array[j][2] < array[min_index][2]:  # Comparar años
                    min_index = j
            if min_index != i:  # Solo intercambiar si es necesario
                array[i], array[min_index] = array[min_index], array[i]
        return array