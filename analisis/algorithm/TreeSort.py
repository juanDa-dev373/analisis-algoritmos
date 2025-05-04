from .SortAlgorithm import SortAlgorithm

class TreeNode:
    """Nodo del árbol para Tree Sort"""
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class TreeSort(SortAlgorithm):
    """Implementación de Tree Sort"""
    def __init__(self):
        self.sorted_data = []
        self.root = None
    
    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if (self._safe_compare(root.val[self.column_index], key[self.column_index]) or 
            (key[self.column_index] == root.val[self.column_index] and key[0] < root.val[0])):
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root
    
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            self.sorted_data.append(root.val)
            self.inorder(root.right)
    
    def sort(self, array, column_index=0):
        self.root = None
        self.column_index = column_index
        for item in array:
            self.root = self.insert(self.root, item)
        self.sorted_data = []
        self.inorder(self.root)
        return self.sorted_data
