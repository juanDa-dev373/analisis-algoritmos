import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EstadisticasProductos:
    def __init__(self, df):
        self.df = df
        self.output = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/assets/estadisticsProducts"))

    def top_autores(self, n=15):
        df = self.clean_sin_valor(self.df, 'Autor')
        ruta = self.output +"/top_autores"
        os.makedirs(ruta, exist_ok=True)
        todos_los_autores = df['Autor'].dropna().str.split(',').explode().str.strip()
        top_autores = todos_los_autores.value_counts().head(n)
        plt.figure(figsize=(20, 10))
        sns.barplot(x=top_autores.index, y=top_autores.values)
        plt.title(f"Top {n} autores con más productos")
        plt.xlabel("Autor")
        plt.ylabel("Cantidad de productos")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(ruta, "top_autores.png"))

    def publicaciones_por_anio_tipo(self):
        ruta = self.output +"/publisher_year_type"
        os.makedirs(ruta, exist_ok=True)
        anio_tipo = self.df.groupby(['Year', 'Type']).size().unstack().fillna(0)
        anio_tipo.plot(kind='bar', stacked=True, figsize=(10, 5), title='Publicaciones por año y tipo de producto')
        plt.xlabel("Año")
        plt.ylabel("Cantidad de productos")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(ruta, "publisher_year_type.png"))

    def distribucion_tipo_producto(self):
        ruta = os.path.join(self.output, "distribuction_type_product")
        os.makedirs(ruta, exist_ok=True)

        tipo_producto = self.df['Type'].value_counts()
        total = tipo_producto.sum()

        etiquetas = [f"{tipo} ({valor / total:.1%})" for tipo, valor in tipo_producto.items()]

        fig, ax = plt.subplots(figsize=(10, 6))

        wedges, _ = ax.pie(
            tipo_producto,
            labels=None,
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
        )

        ax.set_title("Distribución por tipo de producto", fontsize=14)
        ax.set_ylabel("")

        ax.legend(
            wedges,
            etiquetas,
            title="Tipo",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        plt.tight_layout(rect=[0, 0, 0.85, 1])

        plt.savefig(os.path.join(ruta, "distribuction_type_product.png"))
        plt.close()

    def top_journals(self, n=15):
        df = self.clean_sin_valor(self.df, 'Journal')
        ruta = self.output +"/top_journal"
        os.makedirs(ruta, exist_ok=True)
        top_journals = df['Journal'].value_counts().head(n)
        plt.figure(figsize=(10, 10))
        sns.barplot(x=top_journals.index, y=top_journals.values)
        plt.title(f"Top {n} journals con más apariciones")
        plt.xlabel("Journal")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(ruta, "top_journal.png"))

    def top_publishers(self, n=15):
        df = self.clean_sin_valor(self.df, 'Publisher')
        ruta = self.output +"/top_publisher"
        os.makedirs(ruta, exist_ok=True)
        top_publishers = df['Publisher'].value_counts().head(n)
        plt.figure(figsize=(10, 10))
        sns.barplot(x=top_publishers.index, y=top_publishers.values)
        plt.title(f"Top {n} publishers con más apariciones")
        plt.xlabel("Publisher")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(ruta, "top_publishers.png"))
    
    def clean_sin_valor(self, df,  column):
        if column not in df.columns:
            raise KeyError(f"La columna {column} no existe en el DataFrame")

        df[column] = df[column].replace(
            to_replace=r'(?i)^Sin valor$',
            value=pd.NA,
            regex=True
        )

        df_limpio = df.dropna(subset=['Publisher']).copy()

        return df_limpio



if __name__ == "__main__":
    data_path= os.path.join(os.path.dirname(__file__), "../static/assets/Data_Final/datafinalbib.csv")
    df = pd.read_csv(data_path)
    estadisticas = EstadisticasProductos(df)
    estadisticas.top_autores()
    estadisticas.publicaciones_por_anio_tipo()
    estadisticas.distribucion_tipo_producto()
    estadisticas.top_journals()
    estadisticas.top_publishers()