Análisis de Percepción del Personal de Salud Durante la Pandemia COVID-19

Este proyecto realiza un análisis exhaustivo de una encuesta aplicada a 6,020 estudiantes y profesionales del área de la salud en México para entender su percepción y experiencias durante la pandemia de COVID-19. El análisis abarca desde estadísticas descriptivas hasta procesamiento de lenguaje natural (NLP) sobre las respuestas abiertas.

El resultado final incluye un conjunto de datos limpios, archivos de análisis para visualización y un script de Python completamente automatizado que reproduce todo el proceso. Los datos generados se utilizan para alimentar un dashboard interactivo en Google Looker Studio.

metodología

El proyecto se divide en dos fases principales, ambas ejecutadas por un único script de Python:

Fase 1: Unificación y Limpieza de Datos:

Unificación: Se leen 7 archivos CSV originales, correspondientes a diferentes perfiles de encuestados, y se consolidan en un único DataFrame.

Limpieza de Nombres de Columna: Se corrigen nombres de columna duplicados (ej. Especifique) añadiendo sufijos numéricos para hacerlos únicos.

Limpieza de Celdas: Se normalizan los datos en las celdas para eliminar caracteres problemáticos (saltos de línea, comillas dobles) que podrían causar errores durante la subida a plataformas de BI.

Generación de Archivo Maestro: Se guarda el resultado como encuesta_para_looker.csv, el archivo principal para el dashboard.

Fase 2: Análisis Estadístico y de Texto (NLP):

Análisis Descriptivo: Se calculan estadísticas clave como la distribución por sexo, promedio de edad, participación por perfil profesional y el porcentaje de conflictos éticos/académicos reportados.

Análisis de Texto (Preguntas 13, 14 y 15): Para cada pregunta de texto abierto, se aplica un pipeline de NLP que incluye:

Conversión a minúsculas y eliminación de acentos.

Eliminación de números, puntuación y caracteres especiales.

Sustitución de términos clave (ej. "servicio social" -> "servicio_social").

Eliminación de stopwords (palabras vacías en español).

Generación de Entregables: El script genera automáticamente todos los archivos necesarios para el reporte y el dashboard:

Archivos CSV: Tablas de frecuencia y matrices de correlación para cada pregunta.

Imágenes PNG: Nubes de palabras, histogramas de frecuencia y mapas de calor de correlación para el reporte en PDF.

🛠️ Tecnologías Utilizadas

Lenguaje: Python 3

Librerías Principales:

pandas para manipulación y limpieza de datos.

nltk para procesamiento de lenguaje natural (stopwords).

scikit-learn para la vectorización de texto (matriz de términos).

matplotlib y seaborn para la generación de gráficas estáticas.

wordcloud para la creación de nubes de palabras.

Herramienta de Visualización: Google Looker Studio

🚀 Cómo Ejecutar este Proyecto

Sigue estos pasos para replicar el análisis en tu propia máquina.

1. Prerrequisitos

Tener Python 3.8 o superior instalado.

Tener pip (el gestor de paquetes de Python) disponible en la terminal.

2. Configuración del Entorno

Es una buena práctica trabajar en un ambiente virtual.

# 1. Clona este repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>

# 2. Crea y activa un ambiente virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
# source venv/bin/activate

# 3. Instala las dependencias necesarias
pip install pandas nltk scikit-learn matplotlib seaborn wordcloud


3. Estructura de Archivos

Para que el script funcione correctamente, asegúrate de que tu carpeta principal contenga:

El script principal: Codigo_Fuente_Final_Integrado.py

Los 7 archivos CSV originales de la encuesta (ej. Encuesta.xlsx - Técnicos.csv, etc.).

4. Ejecución

Con el ambiente virtual activado y los archivos en su lugar, simplemente ejecuta el siguiente comando en tu terminal:

python Codigo_Fuente_Final_Integrado.py
