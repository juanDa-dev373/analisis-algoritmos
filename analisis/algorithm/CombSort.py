from .Sort_Algorithm import SortAlgorithm

class CombSort:
    def sort(self, data, column_index=2):
        if not data:
            return data

        if not isinstance(data, list) or not isinstance(data[0], tuple):
            raise ValueError("Los datos deben ser una lista de tuplas")

        n = len(data)
        gap = n
        shrink = 1.3
        sorted_flag = False

        while not sorted_flag:
            gap = max(1, int(gap / shrink))
            sorted_flag = True

            for i in range(n - gap):
                if data[i][column_index] > data[i + gap][column_index]:
                    data[i], data[i + gap] = data[i + gap], data[i]
                    sorted_flag = False

        return data
