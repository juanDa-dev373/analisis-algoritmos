from .Sort_Algorithm import SortAlgorithm
from tqdm import tqdm


class BucketSort(SortAlgorithm):
    
    def sort(self, array):
        self.data = array
        min_year = min(item[2] for item in self.data)
        max_year = max(item[2] for item in self.data)
        bucket_count = max_year - min_year + 1
        buckets = [[] for _ in range(bucket_count)]
        
        for item in self.data:
            index = item[2] - min_year
            buckets[index].append(item)
        
        sorted_data = []
        for bucket in tqdm(buckets, desc="Ordenando", unit="parte"):
            sorted_data.extend(sorted(bucket, key=lambda x: x[2]))
        
        return sorted_data