
from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm

class SelectionSort(SortAlgorithm):
    def sort(self, array, column_index=0):
        n = len(array)
        for i in tqdm(range(n), desc="Ordenando", unit="parte"):
            min_index = i
            for j in range(i + 1, n):
                if self._safe_compare(array[min_index][column_index], array[j][column_index]):  # Comparar años
                    min_index = j
            if min_index != i:  # Solo intercambiar si es necesario
                array[i], array[min_index] = array[min_index], array[i]
        return array