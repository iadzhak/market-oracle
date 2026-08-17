import datetime as dt
from typing import Any

import httpx
from textblob import TextBlob

from .base import NewsBaseSource


class NewsApiGetter(NewsBaseSource):

    def __init__(self, base_url: str, api_key: str, news_url: str) -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url,
            params={'apiKey': api_key}
        )
        self.news_url = news_url

    async def get_news(self, token: str, date_to: dt.datetime | None = None) -> dict[str, Any]:
        date_to = date_to or dt.datetime.now()
        params = {
            'q': f'{token.lower()} token',
            'pageSize': 10,
            'language': 'en',
            'to': date_to.isoformat(),
            'sortBy': 'publishedAt',
        }
        response = await self.client.get(self.news_url, params=params)
        return response.json()

    def calculate_news_sentiment(self, news: list[str]) -> tuple[float, float]:
        if len(news) == 0:
            return 0, 0
        p, s = 0, 0
        for n in news:
            testimonial = TextBlob(n)
            p += testimonial.sentiment.polarity
            s += testimonial.sentiment.subjectivity
        return p / len(news), s / len(news)

    def parse_articles(self, data: Any) -> list[str]:
        return [d['description'] for d in data.get('articles', [])]
