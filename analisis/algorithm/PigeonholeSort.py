from tqdm import tqdm
from .Sort_Algorithm import SortAlgorithm

class PigeonholeSort(SortAlgorithm):
    
    def sort(self, arr):
        if not arr:
            return

        min_val = min(arr, key=lambda x: x[2])[2]
        max_val = max(arr, key=lambda x: x[2])[2]
        size = max_val - min_val + 1
        holes = [[] for _ in range(size)]

        for book in arr:
            holes[book[2] - min_val].append(book)

        index = 0
        for hole in tqdm(holes, desc="Ordenando", unit="parte"):
            for book in hole:
                arr[index] = book
                index += 1

        return arr