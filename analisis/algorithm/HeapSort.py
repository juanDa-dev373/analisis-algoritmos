from .Sort_Algorithm import SortAlgorithm
from tqdm import tqdm

class HeapSort(SortAlgorithm):
    
    def heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left][2] > arr[largest][2]:
            largest = left
        if right < n and arr[right][2] > arr[largest][2]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def sort(self, array):
        n = len(array)
        for i in tqdm(range(n // 2 - 1, -1, -1), desc="Construyendo Heap", unit="parte"):
            self.heapify(array, n, i)

        for i in tqdm(range(n - 1, 0, -1), desc="Ordenando", unit="parte"):
            array[i], array[0] = array[0], array[i]
            self.heapify(array, i, 0)
        return array