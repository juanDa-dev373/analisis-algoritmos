from .Sort_Algorithm import SortAlgorithm
from tqdm import tqdm

class BinaryInsertionSort(SortAlgorithm):
    
    def binary_search(self, sub_arr, val, start, end):
        while start <= end:
            mid = (start + end) // 2
            if sub_arr[mid][2] < val:
                start = mid + 1
            else:
                end = mid - 1
        return start

    def sort(self, array):
        for i in tqdm(range(1, len(array)), desc="Ordenando", unit="parte"):
            key_item = array[i]
            insert_index = self.binary_search(array, key_item[2], 0, i - 1)
            array.insert(insert_index, array.pop(i))

        return array