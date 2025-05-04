from tqdm import tqdm
from .SortAlgorithm import SortAlgorithm


# Función para implementar TimSort
class TimSort(SortAlgorithm):
    def __init__(self, min_run=32):
        self.min_run = min_run

    def sort(self, array, column_index=0):
        self.column_index = column_index
        self._insertion_sort_chunks(array)
        self._merge_chunks(array)
        return array

    def _insertion_sort_chunks(self, array):
        """Ordena subarreglos pequeños dentro del array usando Insertion Sort."""
        for start in range(0, len(array), self.min_run):
            end = min(start + self.min_run - 1, len(array) - 1)
            self._insertion_sort(array, start, end)

    def _insertion_sort(self, array, left, right):
        """Método de Insertion Sort para pequeños fragmentos del array."""
        for i in range(left + 1, right + 1):
            key_item = array[i]
            j = i - 1

            while j >= left and self._safe_compare(array[j][self.column_index], key_item[self.column_index]):
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key_item

    def _merge_chunks(self, array):
        """Fusiona los subarreglos ordenados mediante Merge Sort."""
        size = self.min_run
        while size < len(array):
            for left in tqdm(range(0, len(array), size * 2), desc="Ordenando", unit="parte"):
                mid = min(len(array) - 1, left + size - 1)
                right = min((left + 2 * size - 1), (len(array) - 1))
                if mid < right:
                    self._merge(array, left, mid, right)
            size *= 2

    def _merge(self, array, left, mid, right):
        """Fusión de dos subarreglos ordenados."""
        left_part = array[left:mid + 1]
        right_part = array[mid + 1:right + 1]

        left_index, right_index, sorted_index = 0, 0, left

        while left_index < len(left_part) and right_index < len(right_part):
            if not self._safe_compare(left_part[left_index][self.column_index], right_part[right_index][self.column_index]):
                array[sorted_index] = left_part[left_index]
                left_index += 1
            else:
                array[sorted_index] = right_part[right_index]
                right_index += 1
            sorted_index += 1

        array[sorted_index:right + 1] = left_part[left_index:] + right_part[right_index:]
