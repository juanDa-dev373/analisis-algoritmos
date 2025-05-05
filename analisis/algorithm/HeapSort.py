from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm

class HeapSort(SortAlgorithm):
    
    def heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self._safe_compare(arr[left][self.column_index], arr[largest][self.column_index]):
            largest = left
        if right < n and self._safe_compare(arr[right][self.column_index], arr[largest][self.column_index]):
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def sort(self, array, column_index=0):
        self.column_index = column_index
        n = len(array)
        for i in tqdm(range(n // 2 - 1, -1, -1), desc="Construyendo Heap", unit="parte"):
            self.heapify(array, n, i)

        for i in tqdm(range(n - 1, 0, -1), desc="Ordenando", unit="parte"):
            array[i], array[0] = array[0], array[i]
            self.heapify(array, i, 0)
        return array