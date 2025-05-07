import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class DrawDendogram:
    def _generate_dendrograms(self):
        os.makedirs(self.output_path + "/dendrograms", exist_ok=True)
        abstracts = self.df['Abstract'].tolist()
        titles = self.df['Title'].fillna('Sin título').tolist()

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(abstracts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        distance_matrix = 1 - similarity_matrix

        methods = ['ward', 'average']
        for method in methods:
            linkage_matrix = linkage(distance_matrix, method=method)
            plt.figure(figsize=(18, 10))
            dendrogram(linkage_matrix, labels=titles, leaf_rotation=90)
            plt.title(f"Dendrograma de Agrupamiento - Método: {method.capitalize()}")
            plt.xlabel("Artículos")
            plt.ylabel("Distancia")
            plt.tight_layout()
            output_file = os.path.join(self.output_path + "/dendrograms", f"abstracts_dendrogram_{method}.png")
            plt.savefig(output_file, dpi=300)
            plt.close()

            # Comparar con categorías (solo para evaluar calidad de cluster)
            cluster_labels = fcluster(linkage_matrix, t=5, criterion='maxclust')
            true_labels = self._generate_true_labels()
            ari = adjusted_rand_score(true_labels, cluster_labels)
            print(f"ARI (Adjusted Rand Index) para método {method}: {ari:.4f}")

    def _generate_true_labels(self):
        """
        Se asigna un índice entero a cada categoría que aparece en cada abstract.
        Se usará para comparar con clustering real.
        """
        label_map = {cat: i for i, cat in enumerate(self.categorias)}
        labels = []
        for abstract in self.df['Abstract']:
            found = False
            for cat, variables in self.categorias.items():
                if any(var in abstract for var in variables):
                    labels.append(label_map[cat])
                    found = True
                    break
            if not found:
                labels.append(-1)  # Sin categoría encontrada
        return labels            