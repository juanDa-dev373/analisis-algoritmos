import math
from tqdm import tqdm
from .SortAlgorithm import SortAlgorithm
from typing import List, Any

class PigeonholeSort(SortAlgorithm):

    def sort(self, array: List[List[Any]], column_index: int = 0) -> List[List[Any]]:
        """
        Ordena una lista de listas usando Pigeonhole Sort.
        :param array: Lista de listas con los datos.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        if not array:
            raise ValueError("El dataset está vacío o no tiene datos")

        first_value = array[0][column_index]

        if self._is_numeric(first_value):
            return self._sort_numeric_data(array, column_index)
        elif isinstance(first_value, str):
            return self._sort_string_data(array, column_index)
        else:
            raise ValueError("No se reconoce el tipo de datos en la columna seleccionada")

    def _sort_numeric_data(self, array: List[List[Any]], column_index: int) -> List[List[Any]]:
        """
        Ordena datos numéricos usando Pigeonhole Sort.
        :param array: Lista de listas con datos numéricos.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        numeric_values = [float(row[column_index]) for row in array if self._is_numeric(row[column_index])]
        if not numeric_values:
            raise ValueError("No hay valores numéricos válidos en la columna seleccionada")

        min_val, max_val = min(numeric_values), max(numeric_values)
        size = int(max_val - min_val + 1)
        holes = [[] for _ in range(size)]

        for row in array:
            try:
                value = float(row[column_index])
                index = int(value - min_val)
                holes[index].append(row)
            except ValueError as e:
                print(f"Error: {e}, saltando este valor...")

        sorted_array = []
        for hole in tqdm(holes, desc="Ordenando números", unit="parte"):
            sorted_array.extend(hole)

        return sorted_array

    def _sort_string_data(self, array: List[List[Any]], column_index: int) -> List[List[Any]]:
        """
        Ordena datos de tipo string usando Pigeonhole Sort basado en códigos ASCII.
        :param array: Lista de listas con datos de texto.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        ascii_values = [ord(row[column_index][0].lower()) for row in array if isinstance(row[column_index], str) and row[column_index]]
        if not ascii_values:
            raise ValueError("No hay valores de texto válidos en la columna seleccionada")

        min_char, max_char = min(ascii_values), max(ascii_values)
        size = max_char - min_char + 1
        holes = [[] for _ in range(size)]

        for row in array:
            try:
                index = ord(str(row[column_index])[0].lower()) - min_char
                holes[index].append(row)
            except ValueError as e:
                print(f"Error: {e}, saltando este valor...")

        sorted_array = []
        for hole in tqdm(holes, desc="Ordenando texto", unit="parte"):
            sorted_array.extend(sorted(hole, key=lambda x: str(x[column_index]).lower()))

        return sorted_array
