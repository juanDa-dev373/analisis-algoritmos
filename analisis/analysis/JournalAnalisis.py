import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram


def cargar_datos(path: str, max_rows: int = 50) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df['Abstract'].notnull()].drop_duplicates(subset=['Abstract'])
    return df.head(max_rows)


def preprocesar_texto(df: pd.DataFrame) -> 'scipy.sparse.csr_matrix':
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['Abstract'])
    return tfidf_matrix


def generar_dendrograma(tfidf_matrix, titulos, output_path: str):
    linkage_matrix = linkage(tfidf_matrix.toarray(), method='ward')
    
    plt.figure(figsize=(16, 8))
    dendrogram(linkage_matrix, labels=titulos, leaf_rotation=90)
    plt.title('Dendrograma - Agrupamiento Jerárquico (Ward)')
    plt.xlabel('Artículos')
    plt.ylabel('Distancia')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.show()


def aplicar_agglomerative(tfidf_matrix, df: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
    model = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    labels = model.fit_predict(tfidf_matrix.toarray())
    df['Cluster'] = labels
    
    return df


def mostrar_resultados(df: pd.DataFrame):
    print("\nResumen de agrupamiento jerárquico con AgglomerativeClustering:\n")
    print(df[['Title', 'Cluster']].sort_values(by='Cluster'))


def main():
    print("Iniciando análisis jerárquico de abstracts científicos...\n")
    
    ruta_csv= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv"),
    ruta_imagen='../static/assets/Dendrograma/dendrograma_ward.png'
    
    df = cargar_datos(ruta_csv)
    tfidf_matrix = preprocesar_texto(df)
    
    generar_dendrograma(tfidf_matrix, df['Title'].values, ruta_imagen)
    
    df_clusterizado = aplicar_agglomerative(tfidf_matrix, df)
    mostrar_resultados(df_clusterizado)


if __name__ == "__main__":
    main()
