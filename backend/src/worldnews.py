import httpx

from .settings import conf, WorldNewsURLs as url

client = httpx.AsyncClient(
    base_url=conf.WORLDNEWS_API_URL,
    headers={
        'x-api-key': conf.WORLDNEWS_API_KEY
    }
)

async def get_news(search: str):
    params = {
        'text': search,
        'number': 10,
        'language': 'en',
        'sort-direction': 'DESC',
    }
    response = await client.get(url.search_news, params=params)
    return response.json()
