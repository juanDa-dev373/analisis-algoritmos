from tqdm import tqdm
from .SortAlgorithm import SortAlgorithm

class RadixSort(SortAlgorithm):
    def counting_sort(self, arr, exp):
        n = len(arr)
        output = [None] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i][self.column_index] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i][self.column_index] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]

    def sort(self, arr, column_index=0):
        self.column_index = column_index
        if not arr:
            return []
        max_value = max(arr, key=lambda x: x[column_index])[column_index]
        exp = 1
        max_digits = len(str(max_value))

        for _ in tqdm(range(max_digits), desc="Ordenando", unit="dígito"):
            self.counting_sort(arr, exp)
            exp *= 10
        return arr