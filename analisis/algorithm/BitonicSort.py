from .SortAlgorithm import SortAlgorithm

class BitonicSort(SortAlgorithm):
    def __init__(self, direction=1):
        self.direction = direction

    def sort(self, array, column_index=0):
        self.column_index = column_index
        n = 1
        while n < len(array):
            n *= 2
        array.extend([(None, None, float('inf'))] * (n - len(array)))
        self._bitonic_sort(array, 0, n, self.direction)
        return array

    def _bitonic_sort(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            self._bitonic_sort(arr, low, k, 1)
            self._bitonic_sort(arr, low + k, k, 0)
            self._bitonic_merge(arr, low, cnt, direction)

    def _bitonic_merge(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                if ((direction == 1 and arr[i][self.column_index] > arr[i + k][self.column_index]) or 
                    (direction == 0 and arr[i][self.column_index] < arr[i + k][self.column_index])):
                    arr[i], arr[i + k] = arr[i + k], arr[i]
            self._bitonic_merge(arr, low, k, direction)
            self._bitonic_merge(arr, low + k, k, direction)
