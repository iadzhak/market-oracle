import httpx

from .settings import conf, CoinGeckoURLs as URL

limits = httpx.Limits(max_connections=1)
client = httpx.AsyncClient(
    base_url=conf.COINGECKO_API_URL,
    headers={'x-cg-demo-api-key': conf.COINGECKO_API_KEY},
    limits=limits,
)


async def coins_list():
    response = await client.get(URL.coins_list)
    return response.json()


async def download_history(coingecko_id: str):
    params = {
        'vs_currency': 'usd',
        'days': '1'
    }
    response = await client.get(URL.history.format(id=coingecko_id), params=params)
    return response.json()


async def calculate_trend_score(token: str):
    pass
