import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from colorama import Style, init, Fore
from analisis.dataset.data_saver import DataSaver
from analisis.dataset.data_saver import DataUnifier

# Inicializar colorama
init(autoreset=True)

if __name__ == "__main__":
    print(Style.BRIGHT + Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "  ***   Sistema Unificador de Datos Bibliográficos   ***")
    print(Fore.CYAN + "=" * 60)
    
    # Directorio de archivos .bib
    directorio_bib = "analisis/static/assets/Data_Base"  # Modifica con tu directorio real
    
    # Fuentes asociadas a los archivos .bib
    sources = ['IEEE', 'ScienceDirect', 'ACM']  # Asegurar que la lista sea suficiente para los archivos encontrados
    
    # Procesar y unificar datos
    unifier = DataUnifier(directorio_bib, sources)
    unified_df, duplicated_df = unifier.unify_bib_files()

    # Limpiar DataFrame unificado
    unified_df = DataSaver.clean_empty_columns(unified_df)
    
    # Guardar resultados
    DataSaver.save_to_bib(unified_df, 'analisis/static/assets/Data_Final/datafinalbib.bib')
    DataSaver.save_to_bib(duplicated_df, 'analisis/static/assets/Data_Final/duplicated_records.bib')
    DataSaver.save_to_csv(unified_df, 'analisis/static/assets/Data_Final/datafinalbib.csv')
    DataSaver.save_to_csv(duplicated_df, 'analisis/static/assets/Data_Final/duplicated_records.csv')
    print("Proceso completado. Registros únicos y duplicados guardados.")
