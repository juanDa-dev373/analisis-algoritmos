from .Sort_Algorithm import SortAlgorithm
from tqdm import tqdm

class GnomeSort(SortAlgorithm):
    def sort(self, arr):
        n = len(arr)
        index = 0
        step = max(1, n // 100)
        
        with tqdm(total=n, desc="Ordenando", unit="parte") as pbar:
            while index < n:
                if index == 0:
                    index += 1
                if arr[index][2] >= arr[index - 1][2]:
                    index += 1
                else:
                    arr[index], arr[index - 1] = arr[index - 1], arr[index]
                    index -= 1
                    if index < 0:
                        index = 0
                if index % step == 0 or index == n - 1:
                    pbar.update(1)
        
        return arr       