from pydantic_settings import BaseSettings

DEFAULT_TOKENS_AND_SEARCH = {
    'bitcoin': 'bitcoin',
    'ethereum': 'ethereum',
    'solana': 'solana',
    'binancecoin': 'binance',
    'cardano': 'cardano',
    'ripple': 'ripple',
    'dogecoin': 'doge token',
    'tontoken': 'ton token'
}

NEWS_API_KEY = 'edbc73f73de24b09a1eae186b6e8b0d5'
NEWS_API_URL = 'https://newsapi.org/v2'

class Settings(BaseSettings):
    TOKENS_AND_SEARCH: dict[str, str] = DEFAULT_TOKENS_AND_SEARCH  # id from coingecko and search phrase for news

    TOKENS: set[str] = set(DEFAULT_TOKENS_AND_SEARCH.keys())

    COINGECKO_API_KEY: str = 'CG-PepHaJMtCeuzCxdswZAM5Em7'
    COINGECKO_API_URL: str = 'https://api.coingecko.com/api/v3'

    WORLDNEWS_API_KEY: str = 'e8cf3e386178414ea8c58654720274a8'
    WORLDNEWS_API_URL: str = 'https://api.worldnewsapi.com/'

    NEWS_API_KEY: str = 'edbc73f73de24b09a1eae186b6e8b0d5'
    NEWS_API_URL: str = 'https://newsapi.org/v2'
    NEWS_API_ENDPOINT: str = '/everything'

    CCXT_EXCHANGE: str = 'binance'

    DB_URL: str = 'sqlite+aiosqlite:///db.sqlite3'

    model_config = {'env_file': '.env', 'env_file_encoding': 'utf-8'}


conf = Settings()


class CoinGeckoURLs:
    coins_list = '/coins/list'
    history = '/coins/{id}/ohlc'


class WorldNewsURLs:
    search_news = '/search-news'
