from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm

class GnomeSort(SortAlgorithm):

    def _ascii_first_char(self, value):
        """Devuelve el código ASCII del primer carácter de un valor dado."""
        if value is None:
            return 0
        value_str = str(value).strip()
        return ord(value_str[0]) if value_str else 0
    
    def sort_char(self, arr, column_index=0):
        n = len(arr)
        index = 0
        step = max(1, n // 100)

        with tqdm(total=n, desc="Ordenando", unit="elemento") as pbar:
            last_progress = 0
            while index < n:
                if index == 0:
                    index += 1
                elif self._ascii_first_char(arr[index][column_index]) >= self._ascii_first_char(arr[index - 1][column_index]):
                    index += 1
                else:
                    arr[index], arr[index - 1] = arr[index - 1], arr[index]
                    index -= 1
                    if index < 0:
                        index = 0

                if index - last_progress >= step or index == n - 1:
                    pbar.update(index - last_progress)
                    last_progress = index
                    
        return arr

    def sort_numeric(self, arr, column_index=0):
        n = len(arr)
        index = 0
        step = max(1, n // 100)
        
        with tqdm(total=n, desc="Ordenando", unit="parte") as pbar:
            while index < n:
                if index == 0:
                    index += 1
                if arr[index][column_index] >= arr[index - 1][column_index]:
                    index += 1
                else:
                    arr[index], arr[index - 1] = arr[index - 1], arr[index]
                    index -= 1
                    if index < 0:
                        index = 0
                if index % step == 0 or index == n - 1:
                    pbar.update(1)
        
        return arr
    
    def sort(self, arr, column_index=0):
        self.column_index = column_index
        if not arr:
            return []

        first_value = arr[0][column_index]

        if self._is_numeric(first_value):
            return self.sort_numeric(arr, column_index)
        else:
            return self.sort_char(arr, column_index)