import datetime as dt
from typing import Any

from faker import Faker
from textblob import TextBlob

from .base import NewsBaseSource


class FakeNewsApiGetter(NewsBaseSource):

    def __init__(self) -> None:
        self.fake = Faker()

    async def get_news(self, token: str, date_to: dt.datetime | None = None) -> dict[str, Any]:
        result = {'articles': []}
        for _ in range(10):
            result['articles'].append({
                'description': self.fake.text()
            })
        return result

    def calculate_news_sentiment(self, news: list[str]) -> tuple[float, float]:
        if len(news) == 0:
            return 0, 0
        p, s, count = 0, 0, 0
        for n in news:
            if not n:
                continue
            testimonial = TextBlob(n)
            p += testimonial.sentiment.polarity
            s += testimonial.sentiment.subjectivity
            count += 1
        if count == 0:
            return 0.5, 0.5  # вернем средние значения чтобы не сильно влиять
        return p / count, s / count

    def parse_articles(self, data: Any) -> list[str]:
        return [d['description'] for d in data.get('articles', [])]
