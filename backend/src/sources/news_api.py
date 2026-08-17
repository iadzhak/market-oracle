import datetime as dt

import httpx

NEWS_API_KEY = 'edbc73f73de24b09a1eae186b6e8b0d5'
NEWS_API_URL = 'https://newsapi.org/v2'

NEWS_URL_EVERYTHING = '/everything'

client = httpx.AsyncClient(
    base_url=NEWS_API_URL,
    params={'apiKey': NEWS_API_KEY}
)

async def get_news(token: str, date_to: dt.datetime | None = None):
    """Возвращает новости по убыванию даты."""
    date_to = date_to or dt.datetime.now()
    params = {
        'q': f'{token.lower()} token',
        'pageSize': 10,
        'language': 'en',
        'to': date_to.isoformat(),
        'sortBy': 'publishedAt',
    }
    response = await client.get(NEWS_URL_EVERYTHING, params=params)
    return response.json()


date_to = dt.datetime.now() - dt.timedelta(days=10)

params = {
    'apiKey': NEWS_API_KEY,
    'q': 'btc token',
    'pageSize': 10,
    'language': 'en',
    'to': date_to.isoformat(),
    'sortBy': 'publishedAt',
}

url = '/everything'

response = client.get(url, params=params)
data = response.json()



for article in data['articles']:
    print(article['publishedAt'], article['title'])
    print(article['content'])
    print(article['description'])
    print(article['url'])
    print()