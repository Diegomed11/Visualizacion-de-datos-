# VisualizacionDatos/Proyecto1.py
#Diego Medina Medina
import pandas as pd
import re
import unicodedata
from nltk.corpus import stopwords
import nltk
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer


# --- FUNCIÓN DE LIMPIEZA DE TEXTO ---
def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""
    
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\d+', '', texto)
    
    reemplazos = {
        "servicio social": "servicio_social", "medico interno": "medico_interno",
        "practicas profesionales": "practicas_profesionales", "atencion medica": "atencion_medica",
        "equipo proteccion": "equipo_proteccion"
    }
    for frase, reemplazo in reemplazos.items():
        texto = texto.replace(frase, reemplazo)
        
    palabras = texto.split()
    
    stop_words_es = set(stopwords.words('spanish'))
    palabras_a_eliminar = ['paciente', 'medico', 'practica', 'ser', 'hacer', 'si', 'no', 'pregunta', 'respuesta']
    stop_words_es.update(palabras_a_eliminar)
    
    palabras_limpias = [palabra for palabra in palabras if palabra not in stop_words_es and len(palabra) > 2]
    
    return " ".join(palabras_limpias)

# --- CARGA DE DATOS UNIFICADOS ---
# Busca los archivos CSV en la misma carpeta que el script
ruta_del_script = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else '.'
patron_archivos = os.path.join(ruta_del_script, 'Encuesta.xlsx - *.csv')
lista_archivos_csv = glob.glob(patron_archivos)

if not lista_archivos_csv:
    print(f"Error: No se encontraron archivos CSV con el patrón 'Encuesta.xlsx - *.csv'")
    print("Asegúrate de que este script esté en la misma carpeta que tus archivos de datos.")
    exit()

print(f"Se encontraron {len(lista_archivos_csv)} archivos para unificar:")
lista_de_dataframes = []
for archivo in lista_archivos_csv:
    try:
        df_temporal = pd.read_csv(archivo, encoding='latin1')
        lista_de_dataframes.append(df_temporal)
        print(f" - Archivo '{os.path.basename(archivo)}' leído correctamente.")
    except Exception as e:
        print(f"No se pudo leer el archivo {os.path.basename(archivo)}. Error: {e}")

if not lista_de_dataframes:
    print("No se pudo cargar ningún archivo. El programa se detendrá.")
    exit()

df = pd.concat(lista_de_dataframes, ignore_index=True)
print("\nTodos los archivos han sido unificados.")

# Quitar espacios, puntos, y hacer nombres únicos
df.columns = df.columns.str.strip().str.replace(r'[^\w\s]', '_', regex=True)

# Asegurar unicidad de nombres
cols = pd.Series(df.columns)
for dup in cols[cols.duplicated()].unique():
    indices = cols[cols == dup].index
    for i, idx in enumerate(indices):
        if i == 0:
            continue
        cols[idx] = f"{dup}_{i}"
df.columns = cols


print(list(df.columns))

# --- LIMPIEZA FINAL PARA LOOKER ---
def limpiar_celda(celda):
    if isinstance(celda, str):
        celda = celda.replace('\n', ' ').replace('\r', ' ')  # elimina saltos de línea
        celda = celda.replace('"', "'")  # evita conflicto de comillas
        celda = celda.strip()
    return celda

df = df.applymap(limpiar_celda)

# Guardar CSV limpio con comillas controladas
df.to_csv("encuesta_para_looker.csv", index=False, encoding='utf-8', sep=',', quoting=1)


try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    print("Descargando lista de stopwords de NLTK...")
    nltk.download('stopwords')
    print("Descarga completa.")
    
# --- ANÁLISIS ESTADÍSTICO DESCRIPTIVO ---
print("\n--- ANÁLISIS DESCRIPTIVO ---")
print("\nPorcentaje por Sexo:")
print(df['Sexo'].value_counts(normalize=True) * 100)
print(f"\nPromedio de Edad: {df['Edad'].mean():.2f}")
print("\nPorcentaje de Participación por Perfil:")
print(df['Usted es'].value_counts(normalize=True) * 100)

columna_conflictos = next((col for col in df.columns if col.startswith('12.')), None)
if columna_conflictos:
    df[columna_conflictos] = df[columna_conflictos].replace({'Sï¿½': 'Sí'})
    conflict_by_profile = df.groupby('Usted es')[columna_conflictos].value_counts(normalize=True).unstack().fillna(0) * 100
    print("\nPorcentaje de Conflictos por Perfil:")
    print(conflict_by_profile)
else:
    print("\nAdvertencia: No se encontró la columna de conflictos")


# --- ANÁLISIS DE TEXTO (NLP) ---
print("\n--- ANÁLISIS DE TEXTO (NLP) ---")

preguntas_a_analizar = ['13_', '14_', '15_']

for prefijo in preguntas_a_analizar:
    columna_texto_largo = next((col for col in df.columns if col.startswith(prefijo)), None)
    if not columna_texto_largo:
        print(f"\nAdvertencia: No se encontró ninguna columna que comience con '{prefijo}'. Saltando análisis.")
        continue

    print(f"\n--- Analizando y generando gráficas para la pregunta: '{columna_texto_largo}' ---\n")
    
    df['texto_limpio'] = df[columna_texto_largo].apply(limpiar_texto)
    corpus_completo = " ".join(df['texto_limpio'].dropna())
    corpus_lista = df['texto_limpio'].dropna().tolist()

    if not corpus_completo:
        print("No hay texto que analizar para esta pregunta después de la limpieza.")
        continue

    # --- GUARDAR NUBE DE PALABRAS ---
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis', collocations=False).generate(corpus_completo)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    nombre_archivo_wc = f"nube_palabras_{prefijo.replace('.', '')}.png"
    plt.savefig(nombre_archivo_wc, bbox_inches='tight')
    plt.close()
    print(f"Imagen de Nube de Palabras guardada como: {nombre_archivo_wc}")

    # --- CÁLCULO DE FRECUENCIAS Y GUARDADO ---
    vectorizer = CountVectorizer()
    tdm = vectorizer.fit_transform(corpus_lista)
    palabras = vectorizer.get_feature_names_out()
    frecuencias = tdm.sum(axis=0).tolist()[0]
    df_frecuencias = pd.DataFrame({'Palabra': palabras, 'Frecuencia': frecuencias}).sort_values(by='Frecuencia', ascending=False).reset_index(drop=True)
    nombre_archivo_frec = f"df_frecuencias_{prefijo.replace('.', '')}.csv"
    df_frecuencias.to_csv(nombre_archivo_frec, index=False)
    
    # --- GUARDAR HISTOGRAMA DE FRECUENCIAS ---
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Frecuencia', y='Palabra', data=df_frecuencias.head(20), palette='plasma')
    plt.title(f'Histograma de Frecuencia (Pregunta {prefijo})')
    plt.xlabel('Frecuencia Absoluta')
    plt.ylabel('Palabra')
    nombre_archivo_hist = f"histograma_frecuencias_{prefijo.replace('.', '')}.png"
    plt.savefig(nombre_archivo_hist, bbox_inches='tight')
    plt.close()
    print(f"Imagen de Histograma guardada como: {nombre_archivo_hist}")

    # --- ANÁLISIS DE CORRELACIÓN Y GUARDADO ---
    top_10_palabras = df_frecuencias['Palabra'].head(10).tolist()
    tdm_df = pd.DataFrame(tdm.toarray(), columns=palabras)
    tdm_top10 = tdm_df[top_10_palabras]
    matriz_correlacion = tdm_top10.corr(method='pearson')
    nombre_archivo_corr = f"matriz_correlacion_{prefijo.replace('.', '')}.csv"
    matriz_correlacion.to_csv(nombre_archivo_corr, index_label='Palabra')

    # --- GUARDAR MAPA DE CALOR DE CORRELACIÓN ---
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Matriz de Correlación (Pregunta {prefijo})')
    nombre_archivo_heatmap = f"mapa_calor_correlacion_{prefijo.replace('.', '')}.png"
    plt.savefig(nombre_archivo_heatmap, bbox_inches='tight')
    plt.close()
    print(f"Imagen de Mapa de Calor guardada como: {nombre_archivo_heatmap}")

print("Todos los archivos CSV para el dashboard y las imágenes PNG para el reporte han sido generados.")


