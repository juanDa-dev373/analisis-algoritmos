import math
from .SortAlgorithm import SortAlgorithm
from tqdm import tqdm
from typing import List, Any

class BucketSort(SortAlgorithm):

    def sort(self, array: List[List[Any]], column_index: int = 0) -> List[List[Any]]:
        """
        Ordena una lista de listas utilizando Bucket Sort.
        :param array: Lista de listas con los datos.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        if not array:
            raise ValueError("El dataset está vacío o no tiene datos")

        primer_valor = array[0][column_index]

        if self._is_numeric(primer_valor):
            return self._sort_numeric_data(array, column_index)
        elif isinstance(primer_valor, str):
            return self._sort_string_data(array, column_index)
        else:
            raise ValueError("No se reconoce el tipo de datos en la columna seleccionada")

    def _sort_numeric_data(self, array: List[List[Any]], column_index: int) -> List[List[Any]]:
        """
        Ordena datos numéricos utilizando Bucket Sort.
        :param array: Lista de listas con datos numéricos.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        valores_numericos = [float(item[column_index]) for item in array if self._is_numeric(item[column_index])]
        if not valores_numericos:
            raise ValueError("No hay valores numéricos válidos en la columna seleccionada")

        min_value, max_value = min(valores_numericos), max(valores_numericos)
        bucket_count = int(max_value - min_value + 1)
        buckets = [[] for _ in range(bucket_count)]

        for item in array:
            try:
                valor = float(item[column_index])
                if math.isnan(valor):
                    raise ValueError(f"NaN detectado en {valor}")
                index = int(valor) - int(min_value)
                buckets[index].append(item)
            except ValueError as e:
                print(f"⚠️ Error: {e}, saltando este valor...")

        sorted_data = []
        for bucket in tqdm(buckets, desc="Ordenando números", unit="parte"):
            sorted_data.extend(sorted(bucket, key=lambda x: x[column_index]))

        return sorted_data

    def _sort_string_data(self, array: List[List[Any]], column_index: int) -> List[List[Any]]:
        """
        Ordena datos de tipo string utilizando Bucket Sort basado en códigos ASCII.
        :param array: Lista de listas con datos de texto.
        :param column_index: Índice de la columna a ordenar.
        :return: Lista ordenada.
        """
        valores_ascii = [ord(item[column_index][0]) for item in array if isinstance(item[column_index], str) and item[column_index]]
        if not valores_ascii:
            raise ValueError("No hay valores de texto válidos en la columna seleccionada")

        min_value, max_value = min(valores_ascii), max(valores_ascii)
        bucket_count = max_value - min_value + 1
        buckets = [[] for _ in range(bucket_count)]

        for item in array:
            try:
                index = ord(str(item[column_index])[0]) - min_value
                buckets[index].append(item)
            except ValueError as e:
                print(f"⚠️ Error: {e}, saltando este valor...")

        sorted_data = []
        for bucket in tqdm(buckets, desc="Ordenando texto", unit="parte"):
            sorted_data.extend(sorted(bucket, key=lambda x: x[column_index]))

        return sorted_data

    @staticmethod
    def _is_numeric(valor: Any) -> bool:
        """
        Verifica si un valor es numérico o una cadena numérica.
        :param valor: Valor a evaluar.
        :return: True si es numérico, False si no.
        """
        return isinstance(valor, (int, float)) or (isinstance(valor, str) and valor.replace('.', '', 1).isdigit())
