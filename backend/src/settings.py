from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    TOKENS: set[str] = {'BTC', 'ETH', 'BNB', 'DOGE', 'SOL', 'XRP', 'ONDO'}

    NEWS_API_KEY: str = 'edbc73f73de24b09a1eae186b6e8b0d5'
    NEWS_API_URL: str = 'https://newsapi.org/v2'
    NEWS_API_ENDPOINT: str = '/everything'

    CCXT_EXCHANGE: str = 'binance'

    DB_URL: str = 'sqlite+aiosqlite:///db.sqlite3'

    DEFAULT_MODEL_NAME: str = 'default'

    DELTA_DAYS_PREDICT: int = 1

conf = Settings()
