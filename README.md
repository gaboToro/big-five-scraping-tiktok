# TikTok Scraper Pro & Big Five NLP Profiler

Un scraper avanzado y con interfaz gráfica para extraer datos de perfiles y publicaciones de TikTok, integrado con un motor de Procesamiento de Lenguaje Natural (NLP). Desarrollado en Python, utiliza **Playwright** y **BeautifulSoup** para la extracción segura de datos, y modelos de **Hugging Face** para realizar un perfilado psicológico basado en el modelo de los Cinco Grandes (OCEAN).

## Características

- **Interfaz Gráfica (GUI):** Fácil de usar gracias a su interfaz nativa construida con `tkinter`. Muestra resultados y análisis en tiempo real.
- **Análisis NLP (Big Five):** Utiliza `sentence-transformers` para generar embeddings del texto del creador y calcula la similitud semántica contra anclajes de personalidad (Apertura, Responsabilidad, Extraversión, Amabilidad, Neuroticismo).
- **Validación de Corpus:** Filtro inteligente que exige un mínimo de 50 palabras combinadas (bio + descripciones) para evitar análisis basados en ruido estadístico.
- **Evasión de Bloqueos:** Reutiliza cookies de sesión (`storage_state`).
- **Navegación Orgánica:** Simula clics humanos para abrir los videos en ventanas emergentes, evitando errores HTTP 403.
- **Extracción de Perfil y Publicaciones:** Obtiene Seguidores, Seguidos, Likes totales, Biografía y métricas/texto de los 15 videos más recientes.
- **Exportación JSON:** Guarda todos los datos estructurados y el análisis psicológico automáticamente en la carpeta `reports/`.

## 📂 Estructura del Proyecto
    scraping-tiktok/
    ├── reports/                # Informes JSON generados por el scraper
    ├── src/                    # Código fuente del proyecto
    │   ├── __init__.py         
    │   ├── main.py             # Orquestador del pipeline de extracción
    │   ├── post_scraper.py     # Lógica de extracción de videos individuales
    │   ├── profile_scraper.py  # Lógica de extracción del perfil principal
    │   └── session_manager.py  # Generador de cookies para evasión de bots
    ├── gui.py                  # Interfaz gráfica principal (Punto de entrada)
    ├── requirements.txt        # Dependencias del proyecto
    └── README.md               # Documentación

## Requisitos e Instalación

Asegúrate de tener **Python 3.8+** instalado.

1. **Clona el repositorio:**
   ```bash
   git clone [https://github.com/gabo_toro/scraping-tiktok.git](https://github.com/gabo_toro/scraping-tiktok.git)
   cd scraping-tiktok

2. **Crea y activa un entorno virtual (Recomendado):**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

3. **Instala las dependencias:**
   ```bash
   pip install requirements.txt

4. **Instala el navegador Chromium para Playwright:**
   ```bash
   playwright install chromium

## Uso

El proyecto está diseñado para ser utilizado principalmente a través de su interfaz gráfica.

1. Ejecuta la aplicación desde la raíz del proyecto:
   ```bash
   python gui.py

2. Ingresar el nombre de usuario de TikTok (en. @tiktok)

3. Haz click en "**Extraer Datos**"

**Nota sobre la IA:** La primera vez que ejecutes un análisis, el sistema descargará el modelo de lenguaje de Hugging Face (all-MiniLM-L6-v2, ~80 MB) de forma automática en segundo plano.


### Gestión de Cookies y CAPTCHAs
Si es la primera vez que ejecutas el programa (o si has borrado las cookies), el scraper necesita generar una sesión validada:
* Se abrirá un navegador de Chromium de forma visible durante **45 segundos**.
* **Tu tarea:** Navega brevemente por la página de inicio o **resuelve el CAPTCHA** si aparece.
* Al finalizar el tiempo, el sistema guardará tu sesión en `tiktok_cookies.json` y continuará con la extracción de forma invisible (`headless`).

## ⚠️ Descargo de Responsabilidad

Este proyecto ha sido creado con fines **estrictamente educativos**. El web scraping de plataformas como TikTok está sujeto a sus Términos de Servicio. El uso excesivo o comercial de esta herramienta puede resultar en el bloqueo permanente de tu dirección IP o cuenta de TikTok. Úsalo con responsabilidad y respetando los límites de la plataforma.