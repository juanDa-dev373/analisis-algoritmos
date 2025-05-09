import pandas as pd
import re
import csv
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DataHandler:
    def __init__(self, data_path, category_path):
        self.data_path = data_path
        self.category_path = category_path
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def _load_and_prepare_all_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        df['Abstract'] = df['Abstract'].fillna('').apply(self.preprocess)
        return df

    def load_and_prepare(self)-> pd.DataFrame:
        extra = self.read_csv_basic(self.data_path)
        df = pd.DataFrame(extra)
        try:
            df['Abstract'] = df['Abstract'].fillna('').apply(self.preprocess)
        except Exception as e:
             print("Error en el preprocesamiento:", e)
        tfidf_matrix = TfidfVectorizer(stop_words='english').fit_transform(df['Abstract'])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        similarity_scores = similarity_matrix.sum(axis=1)
        top_indices = similarity_scores.argsort()[-50:][::-1]
        return df.iloc[top_indices].reset_index(drop=True)
    
    def preprocess(self, text: str) -> str:
        words = word_tokenize(text.lower())
        words = [self.lemmatizer.lemmatize(w) for w in words if w.isalpha() and w not in self.stop_words]
        return ' '.join(words)

    def _load_categories_from_txt(self) -> dict:
        categorias = {}
        with open(self.category_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        categoria_actual = None
        for line in lines:
            if line in {"Habilidades", "Conceptos Computationales", "Actitudes", "Propiedades psicométricas", "Herramienta de evaluación",
                        "Diseño de investigación", "Nivel de escolaridad", "Medio", "Estrategia", "Herramienta"}:
                categoria_actual = line
                categorias[categoria_actual] = []
            else:
                categorias[categoria_actual].append(line.lower())
        return categorias
    
    def _compute_frequencies(self, categorias, df):
        frecuencias_categoria = {}
        for categoria, variables in categorias.items():
            frecuencias = defaultdict(int)
            for var in variables:
                sinonimos = var.split('-')
                for abstract in df['Abstract']:
                    if any(s in abstract for s in sinonimos):
                        frecuencias[var] += sum(abstract.count(s) for s in sinonimos)
            frecuencias_categoria[categoria] = dict(frecuencias)
        return frecuencias_categoria
    
    def read_csv_basic(self, path):
        data = []
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)  # Usa encabezados como claves
                for row in reader:
                    abstract = row.get("Abstract", "sin valor").strip().lower()  # obtiene y limpia
                    if abstract and abstract not in {"sin valor"}:  # solo si no está vacío
                        data.append(row)
            print(f"Leídas {len(data)} filas válidas con Abstract desde el archivo CSV.")
            return data
        except FileNotFoundError:
            print(f"Archivo no encontrado: {path}")
        except Exception as e:
            print(f"Error leyendo el archivo CSV: {e}")
