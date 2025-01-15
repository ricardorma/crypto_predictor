# Crypto Prediction API

## 📋 Descripción del Proyecto

Crypto Prediction API es una aplicación diseñada para proporcionar análisis y predicciones sobre los precios de criptomonedas, utilizando datos históricos, precios en tiempo real y tendencias sociales. El objetivo principal del proyecto es facilitar la toma de decisiones en el mercado de criptomonedas mediante predicciones basadas en modelos estadísticos avanzados y análisis de datos en múltiples frentes.

El proyecto utiliza **modelos ARIMA (AutoRegressive Integrated Moving Average)** para realizar predicciones sobre los precios de criptomonedas, un enfoque estadístico sólido para el análisis de series temporales. Además, incluye múltiples funcionalidades que integran datos externos para proporcionar un contexto más amplio, como tendencias sociales, menciones en plataformas populares y noticias relacionadas.

---

## 🧠 Machine Learning y Modelos de Predicción

Para realizar las predicciones de precios, el proyecto utiliza el modelo ARIMA, que es particularmente eficaz para capturar patrones en series temporales. ARIMA combina tres componentes principales:
- **AR (AutoRegresión)**: Utiliza las relaciones entre observaciones anteriores en la serie de tiempo.
- **I (Integración)**: Hace que los datos sean estacionarios mediante diferenciación.
- **MA (Promedio Móvil)**: Modela el error en términos de relaciones pasadas.

Este modelo es adecuado para datos financieros y permite predicciones a corto y largo plazo en intervalos como días (`1d`) o semanas (`1w`).

---

## 🛠️ Tecnologías Utilizadas

El proyecto utiliza tecnologías modernas para ofrecer una solución eficiente y escalable:

### Backend
- **FastAPI**: Framework web para construir APIs rápidas y robustas.
- **SQLAlchemy**: ORM para la gestión de la base de datos.
- **Statsmodels**: Biblioteca utilizada para implementar modelos ARIMA.
- **Pandas y NumPy**: Para el procesamiento y análisis de datos.

### Base de Datos
- **PostgreSQL**: Base de datos utilizada para almacenar datos históricos de precios de criptomonedas.

### Contenedores
- **Docker**: Para garantizar un entorno reproducible y facilitar el despliegue de la aplicación.

### APIs Externas
- **Binance API**: Para obtener datos históricos y precios en tiempo real de criptomonedas.
- **Google Trends API**: Para analizar tendencias relacionadas con criptomonedas.
- **Reddit API**: Para obtener menciones sociales relevantes.
- **Google News**: Para obtener noticias relacionadas con criptomonedas.

---

## 🚀 Funcionalidades Principales

1. **Predicción de Precios**:
   - Predicción a corto y largo plazo utilizando el modelo ARIMA.
   - Generación de recomendaciones basadas en los resultados (`comprar`, `vender` o `mantener`).

2. **Datos Históricos**:
   - Descarga y almacenamiento de datos históricos en intervalos de `1d` y `1w`.

3. **Precios en Tiempo Real**:
   - Integración con Binance para obtener precios actuales.

4. **Tendencias Sociales**:
   - Análisis de tendencias con datos de Google Trends.

5. **Menciones en Redes Sociales**:
   - Seguimiento de menciones en Reddit y otras plataformas.

6. **Noticias de Criptomonedas**:
   - Obtención de noticias relevantes sobre criptomonedas para mejorar el análisis contextual.

---
