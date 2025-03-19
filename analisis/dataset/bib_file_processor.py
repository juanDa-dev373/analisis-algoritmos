import pandas as pd
import bibtexparser
import re
from typing import List, Dict

import requests

class BibFileProcessor:
    """Clase encargada de procesar archivos .bib y convertirlos en DataFrame."""
    def __init__(self, source: str, related_abstracts: List[str]):
        self.source = source
        self.related_abstracts = related_abstracts
    
    def clean_and_transform_bib(self, file_path: str) -> pd.DataFrame:
        with open(file_path, encoding='utf-8') as bibfile:
            bib_database = bibtexparser.load(bibfile)
        
        records = [self._transform_entry(entry) for entry in bib_database.entries]
        return pd.DataFrame(records)

    def _transform_entry(self, entry: Dict[str, str]) -> Dict[str, str]:
        year_value = re.sub(r'\D+$', '', entry.get('year', 'Sin Valor'))
        title, author = entry.get('title', 'Sin Valor'), entry.get('author', 'Sin Valor').split(',')[0]
        abstract = entry.get('abstract', 'Sin Valor')
        
        return {
            'Autor': entry.get('author', 'Sin Valor'), 'Title': title, 'Year': year_value,
            'Volume': entry.get('volume', 'Sin Valor'), 'Issue': entry.get('number', 'Sin Valor'),
            'Start Page': entry.get('pages', 'Sin Valor').split('-')[0] if 'pages' in entry else 'Sin Valor',
            'End Page': entry.get('pages', 'Sin Valor').split('-')[1] if 'pages' in entry and '-' in entry['pages'] else 'Sin Valor',
            'Abstract': abstract, 'DOI': entry.get('doi', 'Sin Valor'), 'Database': self.source
        }

class AbstractFetcher:
    """Clase responsable de obtener abstracts desde Google Books API."""
    API_URL = "https://www.googleapis.com/books/v1/volumes"

    @staticmethod
    def get_related_abstracts(topic: str = "Computational Thinking", max_results: int = 5) -> List[str]:
        params = {'q': f'intitle:{topic}', 'langRestrict': 'en', 'maxResults': max_results}
        try:
            response = requests.get(AbstractFetcher.API_URL, params=params, timeout=5)
            if response.status_code == 200:
                return [item['volumeInfo'].get('description', 'Sin Valor') for item in response.json().get('items', []) if 'description' in item['volumeInfo']]
        except requests.RequestException:
            pass
        return []