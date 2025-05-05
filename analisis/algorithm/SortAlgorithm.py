
from abc import ABC, abstractmethod

class SortAlgorithm(ABC):
    @abstractmethod
    def sort(self, array, column_index=0):
        pass

    def _safe_compare(self, a, b):
        """Convierte los valores a un tipo común antes de compararlos."""
        if a is None and b is None:
            return False  # o True dependiendo del comportamiento esperado
        if a is None:
            return False  # None es considerado "menor"
        if b is None:
            return False
        try:
            return float(a) > float(b)
        except (ValueError, TypeError):
            return str(a) > str(b)

    def _safe_compare_major_equal(self, a, b):
        """Convierte los valores a un tipo común antes de compararlos."""
        if a is None and b is None:
            return False  # o True dependiendo del comportamiento esperado
        if a is None:
            return False  # None es considerado "menor"
        if b is None:
            return False
        try:
            return float(a) >= float(b)  # Si ambos valores pueden ser números, los comparamos como números
        except ValueError:
            return str(a) >= str(b)  # Si hay un error, los comparamos como cadenas
        
    def _safe_convert(self, value):
        """Convierte los valores a un tipo común antes de usarlos en min/max."""
        return float(value)  # Intenta convertir a número

    @staticmethod
    def _is_numeric(value: any) -> bool:
        """
        Verifica si un valor es numérico o una cadena numérica.
        :param value: Valor a evaluar.
        :return: True si es numérico, False si no.
        """
        return isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit())
