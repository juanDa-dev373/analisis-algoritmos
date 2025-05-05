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

    def sort_numeric(self, arr, column_index=0):
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
    
    def counting_sort_by_first_char(self, arr):
        n = len(arr)
        output = [None] * n
        count = [0] * 256

        for i in range(n):
            char = str(arr[i][self.column_index]).strip()
            ascii_code = ord(char[0]) if char else 0
            ascii_code = ascii_code if ascii_code < 256 else 255
            count[ascii_code] += 1

        for i in range(1, 256):
            count[i] += count[i - 1]

        for i in reversed(range(n)):
            char = str(arr[i][self.column_index]).strip()
            ascii_code = ord(char[0]) if char else 0
            ascii_code = ascii_code if ascii_code < 256 else 255
            output[count[ascii_code] - 1] = arr[i]
            count[ascii_code] -= 1

        return output

    def sort_string(self, arr, column_index=0):
        self.column_index = column_index
        if not arr:
            return []
        return self.counting_sort_by_first_char(arr)
    
    def sort(self, arr, column_index=0):
        self.column_index = column_index
        if not arr:
            return []

        first_value = arr[0][column_index]

        if self._is_numeric(first_value):
            return self.sort_numeric(arr, column_index)
        else:
            return self.sort_string(arr, column_index)