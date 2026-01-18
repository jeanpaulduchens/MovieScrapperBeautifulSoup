# MovieScrapperBeautifulSoup

Proyecto para scrappear películas de IMDB del año 2018 usando dos enfoques:

- **scrappingGraphqlApi.py**: Utiliza la API GraphQL interna de IMDB para obtener los datos de las películas de forma eficiente, sin necesidad de cargar la web ni interactuar con JavaScript.
- **scrappingPlaywright.py**: Usa Playwright para automatizar la navegación y BeautifulSoup para parsear el HTML, simulando la interacción humana (más lento y propenso a fallos si IMDB cambia su estructura).

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

### Scrapping con GraphQL API

```bash
python scrappingGraphqlApi.py
```
Este script realiza peticiones directas a la API de IMDB y obtiene los resultados en formato JSON.

### Scrapping con Playwright y BeautifulSoup

```bash
python scrappingPlaywright.py
```
Este script abre el navegador en modo headless, navega por la web de IMDB y extrae la información de las películas usando BeautifulSoup.

> **Nota:** El método con Playwright es más lento y puede fallar si IMDB cambia su frontend o si hay problemas de red.

## Dependencias principales

- requests
- playwright
- beautifulsoup4
- lxml

Consulta `requirements.txt` para la lista completa.

## Notas adicionales

- El script de GraphQL requiere analizar el tráfico de red de IMDB para obtener los parámetros correctos de la API.
- El script de Playwright requiere tener instalado Chromium (Playwright lo instala automáticamente con `playwright install`).

---
Autor: Jean Paul Duchens Pacheco
Fecha: 2026