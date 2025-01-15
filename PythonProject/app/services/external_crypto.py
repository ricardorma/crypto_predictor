# app/services/external_crypto.py
import httpx
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from xml.etree import ElementTree as ET
from pytrends.request import TrendReq

class ExternalCryptoService:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    async def fetch_news_from_google(self, symbol: str, max_results: int = 10):
        """
            Obtiene noticias relacionadas con una criptomoneda desde Google News RSS.
            Realiza análisis de sentimiento usando VADER.
            :param symbol: Símbolo o nombre de la criptomoneda.
            :param max_results: Número máximo de noticias a obtener.
            :return: Lista de noticias procesadas con análisis de sentimiento.
        """
        query = f"{symbol} cryptocurrency"
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise Exception(f"Error al obtener noticias: {response.text}")

            root = ET.fromstring(response.text)
            items = root.findall(".//item")[:max_results]

            processed_news = []
            for item in items:
                title = item.find("title").text
                pub_date = item.find("pubDate").text
                link = item.find("link").text
                sentiment = self.analyzer.polarity_scores(title)

                processed_news.append({
                    "title": title,
                    "published_at": pub_date,
                    "url": link,
                    "sentiment": "positive" if sentiment["compound"] > 0 else "negative" if sentiment["compound"] < 0 else "neutral"
                })

            return processed_news

    async def fetch_reddit_data(self, symbol: str, max_results: int = 10):
        """
            Obtiene menciones de Reddit relacionadas con una criptomoneda usando Pushshift API.
            Realiza análisis de sentimiento con VADER.
            :param symbol: Nombre o símbolo de la criptomoneda.
            :param max_results: Número máximo de resultados a obtener.
            :return: Lista de menciones procesadas con análisis de sentimiento.
        """
        url = f"https://api.pushshift.io/reddit/search/comment/?q={symbol}&size={max_results}&sort=desc"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise Exception(f"Error al obtener datos de Reddit: {response.text}")
            data = response.json()["data"]

        results = []
        for comment in data:
            sentiment = self.analyzer.polarity_scores(comment["body"])
            results.append({
                "comment": comment["body"],
                "created_at": comment["created_utc"],
                "sentiment": "positive" if sentiment["compound"] > 0 else "negative" if sentiment["compound"] < 0 else "neutral"
            })

        return results

    def fetch_google_trends_data(self, symbol: str, timeframe: str = "today 3-m"):
        """
            Obtiene datos de Google Trends para una criptomoneda específica.
            :param symbol: Nombre o símbolo de la criptomoneda.
            :param timeframe: Intervalo de tiempo (por defecto últimos 3 meses).
            :return: Lista de datos de tendencias (fecha y popularidad).
        """
        pytrends = TrendReq()
        query = f"{symbol} cryptocurrency"
        pytrends.build_payload([query], timeframe=timeframe)

        trends_data = pytrends.interest_over_time()
        if trends_data.empty:
            raise Exception("No se encontraron datos de tendencias.")

        results = []
        for date, row in trends_data.iterrows():
            results.append({"date": date.strftime("%Y-%m-%d"), "popularity": row[query]})
        return results