from .SortAlgorithm import SortAlgorithm
import random
from tqdm import tqdm

class QuickSort(SortAlgorithm):
    def sort(self, data, column_index=0):
        data = data.copy() 
        self.column_index = column_index
        self._quick_sort(data)
        return data

    def _quick_sort(self, arr):
        stack = [(0, len(arr) - 1)]
        with tqdm(total=len(arr), desc="Ordenando", unit="parte") as pbar:
            while stack:
                low, high = stack.pop()
                if low < high:
                    pi = self._partition(arr, low, high)
                    stack.append((low, pi - 1))
                    stack.append((pi + 1, high))
                pbar.update(1)

    def _partition(self, arr, low, high):
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high][self.column_index] 
        i = low - 1
        for j in range(low, high):
            if self._safe_compare_major_equal(pivot,arr[j][self.column_index]) :
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
