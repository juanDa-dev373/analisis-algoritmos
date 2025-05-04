from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm

class ShellSort(SortAlgorithm):

    def sort(self, array, column_index=0):
        """
        Ordena una lista de listas usando Shell Sort.
        """
        if not array:
            raise ValueError("El dataset está vacío o no tiene datos")

        return self._shell_sort(array, column_index)

    def _shell_sort(self, array: list, column_index: int) -> list:
        """
        Implementación de Shell Sort basado en la columna dada.
        """
        n = len(array)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = array[i]
                j = i
                while j >= gap and array[j - gap][column_index] > temp[column_index]:
                    array[j] = array[j - gap]
                    j -= gap
                array[j] = temp
            gap //= 2

        return array
