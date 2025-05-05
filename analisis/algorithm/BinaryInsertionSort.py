from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm

class BinaryInsertionSort(SortAlgorithm):
    
    def binary_search(self, sub_arr, val, start, end):
        while start <= end:
            mid = (start + end) // 2
            if  self._safe_compare(val, sub_arr[mid][self.column_index]):
                start = mid + 1
            else:
                end = mid - 1
        return start

    def sort(self, array,column_index=0):
        self.column_index = column_index
        for i in tqdm(range(1, len(array)), desc="Ordenando", unit="parte"):
            key_item = array[i]
            insert_index = self.binary_search(array, key_item[column_index], 0, i - 1)
            array.insert(insert_index, array.pop(i))

        return array