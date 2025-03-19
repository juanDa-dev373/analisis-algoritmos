from django.test import SimpleTestCase
from analisis.algorithm.TreeSort import TreeSort

class TreeSortTestCase(SimpleTestCase):
    def test_tree_sort(self):
        data = [(1, 'A', 5), (2, 'B', 3), (3, 'C', 8), (4, 'D', 1)]
        sorter = TreeSort()
        sorted_data = sorter.sort(data)

        expected_data = [(4, 'D', 1), (2, 'B', 3), (1, 'A', 5), (3, 'C', 8)]
        self.assertEqual(sorted_data, expected_data)
